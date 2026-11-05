#!/usr/bin/env python3
"""Portable emitter toolchains must activate on every supported host."""
import importlib.util
import os
import shutil
import sys
from pathlib import Path
import subprocess
import tempfile
import types
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("kurushi_cli", ROOT / "psxrecomp/psxrecomp_cli.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class ToolchainTests(unittest.TestCase):
    def test_pack_activates_on_linux_macos_and_windows(self):
        for platform in ("linux", "darwin", "win32"):
            with self.subTest(platform=platform), \
                    mock.patch.object(cli, "sys", types.SimpleNamespace(platform=platform)), \
                    mock.patch.object(cli, "resolve_toolchain_bin", return_value=Path("pack/bin")), \
                    mock.patch.object(cli, "toolchain_bin_runs", return_value=True), \
                    mock.patch("toolchain_pack.activate_toolchain_bin") as activate:
                self.assertTrue(cli.activate_embedded_toolchain(ROOT))
                activate.assert_called_once_with(Path("pack/bin"), log=None)

    def test_broken_pack_is_not_activated(self):
        with mock.patch.object(cli, "resolve_toolchain_bin", return_value=Path("broken/bin")), \
                mock.patch.object(cli, "toolchain_bin_runs", return_value=False), \
                mock.patch("toolchain_pack.activate_toolchain_bin") as activate:
            self.assertFalse(cli.activate_embedded_toolchain(ROOT))
            activate.assert_not_called()

    def test_native_posix_tools_can_reach_configuration(self):
        # ensure_toolchain can succeed by finding native tools without a pack.
        # The emitter build must accept that result and reach source discovery.
        for platform in ("linux", "darwin"):
            with self.subTest(platform=platform), \
                    mock.patch.object(cli, "sys", types.SimpleNamespace(platform=platform)), \
                    mock.patch.object(cli, "activate_embedded_toolchain", return_value=False), \
                    mock.patch.object(cli, "ensure_toolchain_for_rebuild", return_value=True), \
                    mock.patch.object(cli, "_which_tool", return_value=Path("native/tool")), \
                    mock.patch.object(cli, "recompiler_source_dir", side_effect=LookupError("source discovery")):
                with self.assertRaisesRegex(LookupError, "source discovery"):
                    cli._build_recompiler_targets(ROOT, mock.Mock(), ("psxrecomp-game",))

    @unittest.skipUnless(sys.platform == "linux" and shutil.which("rsync"), "Linux rsync staging check")
    def test_staging_preserves_dependency_headers(self):
        script = (ROOT / "psxrecomp/tools/package_setup_host.sh").read_text()
        function = script[script.index("copy_tree_filtered() {"):script.index('if [[ ! -d "${ROOT}/psxrecomp" ]]')]
        start = script.index('copy_tree_filtered "${ROOT}/psxrecomp"')
        invocation = script[start:script.index('copy_tree_filtered "${ROOT}/recomp-ui"', start)]
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            stage = Path(tmp) / "stage"
            inputs = ("generated/game.c", "recompiler/lib/rabbitizer/include/generated/InstrId_enum.h",
                      "recompiler/lib/rabbitizer/cplusplus/include/generated/UniqueId_enum_class.hpp")
            for rel in inputs:
                path = project / "psxrecomp" / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture")
            environment = dict(os.environ, ROOT=str(project), STAGE=str(stage))
            subprocess.run(["bash", "-e", "-c", function + "\n" + invocation], env=environment, check=True)
            self.assertFalse((stage / "psxrecomp/generated").exists())
            for rel in inputs[1:]:
                self.assertTrue((stage / "psxrecomp" / rel).is_file(), rel)

    @unittest.skipUnless(os.environ.get("KURUSHIRECOMP_TEST_TOOLCHAIN"), "set KURUSHIRECOMP_TEST_TOOLCHAIN for a real compiler smoke test")
    def test_mounted_appimage_toolchain_compiles_on_host(self):
        pack = Path(os.environ["KURUSHIRECOMP_TEST_TOOLCHAIN"])
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ):
            project = Path(tmp)
            (project / "toolchain").symlink_to(pack, target_is_directory=True)
            self.assertTrue(cli.activate_embedded_toolchain(project))
            (project / "main.c").write_text('#include <stdio.h>\nint main(void) { puts("portable compiler works"); return 0; }\n')
            (project / "CMakeLists.txt").write_text("cmake_minimum_required(VERSION 3.20)\nproject(smoke C)\nadd_executable(smoke main.c)\n")
            build = project / "build"
            configured = subprocess.run([
                str(pack / "bin/cmake"), "-S", str(project), "-B", str(build), "-G", "Ninja",
                "-DCMAKE_C_COMPILER=" + str(pack / "bin/clang"),
                "-DCMAKE_MAKE_PROGRAM=" + str(pack / "bin/ninja"),
            ], capture_output=True, text=True)
            self.assertEqual(configured.returncode, 0, configured.stdout + configured.stderr)
            built = subprocess.run([str(pack / "bin/cmake"), "--build", str(build), "--parallel", "2"], capture_output=True, text=True)
            self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
            result = subprocess.run([str(build / "smoke")], check=True, capture_output=True, text=True)
            self.assertEqual(result.stdout.strip(), "portable compiler works")


if __name__ == "__main__":
    unittest.main()
