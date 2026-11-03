#!/usr/bin/env python3
"""Exercise AppRun with a read-only setup payload and a fresh user profile."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AppImageLayoutTest(unittest.TestCase):
    def test_setup_project_survives_relaunch_and_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            appdir = base / "mounted image"
            payload = appdir / "usr/share/kurushi"
            data = base / "user data"
            files = {
                "game.toml": "[game]\n",
                "CMakeLists.txt": "# title build\n",
                "codegen_setup.c": "/* title setup */\n",
                "codegen_setup.h": "/* title setup header */\n",
                "psxrecomp/psxrecomp_cli.py": "# CLI\n",
                "psxrecomp/runtime/runtime.cmake": "# framework\n",
                "psxrecomp/bios/openbios.bin": "bundled BIOS",
                "recomp-ui/CMakeLists.txt": "# UI\n",
                "seeds/ghidra_funcs.txt": "0x8003A838\n",
                "mods/kurushi_widescreen.c": "/* title plugin */\n",
                "mods/preloaded/catalog.toml": "# catalog\n",
                "toolchain/bin/cmake": "bundled tool",
                "input.ini": "bundled input",
                "cache/bundled.cache": "bundled cache",
            }
            for rel, text in files.items():
                path = payload / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
            runtime = appdir / "usr/bin/Kurushi_Recompiled"
            runtime.parent.mkdir(parents=True)
            runtime.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "print(json.dumps(dict(cwd=os.getcwd(), args=sys.argv[1:], "
                "root=os.environ.get('KURUSHIRECOMP_PROJECT_ROOT'), "
                "build=os.environ.get('KURUSHIRECOMP_BUILD_DIR'), "
                "appimage=os.environ.get('APPIMAGE'), "
                "relaunch=os.environ.get('RECOMP_APPIMAGE_PATH'))))\n"
            )
            runtime.chmod(0o755)
            source = (ROOT / "packaging/linux/AppRun").read_text()
            for key, value in {
                "APP_NAME": "Kurushi", "EXE_NAME": "Kurushi_Recompiled",
                "PAYLOAD_DIR": "kurushi", "ARTIFACT_NAME": "kurushi",
                "VERSION": "test",
            }.items():
                source = source.replace("@" + key + "@", value)
            app_run = appdir / "AppRun"
            app_run.write_text(source)
            # Match squashfs permissions: inputs cannot be edited in place.
            for path in payload.rglob("*"):
                path.chmod(0o555 if path.is_dir() else 0o444)
            payload.chmod(0o555)
            env = dict(os.environ, APPDIR=str(appdir),
                       APPIMAGE=str(base / "Kurushi.AppImage"),
                       KURUSHIRECOMP_DATA_DIR=str(data))
            try:
                def launch():
                    result = subprocess.run(
                        ["sh", str(app_run), "--setup-selfcheck", "argument with spaces"],
                        env=env, cwd=base, check=True, capture_output=True, text=True)
                    return json.loads(result.stdout)

                observed = launch()
                self.assertEqual(observed["cwd"], str(data))
                self.assertEqual(observed["root"], str(data))
                self.assertEqual(observed["build"], str(data / "build-release"))
                self.assertEqual(observed["args"], ["--setup-selfcheck", "argument with spaces"])
                self.assertIsNone(observed["appimage"])
                self.assertEqual(observed["relaunch"], env["APPIMAGE"])
                for rel in files:
                    self.assertTrue((data / rel).is_file(), rel)
                self.assertEqual((data / "bios/openbios.bin").read_text(), "bundled BIOS")
                for tree in ("psxrecomp", "recomp-ui", "seeds"):
                    self.assertFalse((data / tree).is_symlink())
                    self.assertTrue(os.access(data / tree, os.W_OK))
                # Simulate Generate & rebuild and player-owned changes. Refreshing
                # shipped sources must preserve generated code, builds and saves.
                preserved = {
                    "generated/SCUS_941.81_dispatch.c": "generated game",
                    "psxrecomp/generated/OpenBIOS_dispatch.c": "generated BIOS",
                    "build-release/product": "built product",
                    "saves/card1.mcd": "player save",
                    "settings.toml": "player settings",
                    "mods/state.toml": "player mod selections",
                    "input.ini": "player input",
                    "cache/bundled.cache": "updated cache",
                }
                for rel, text in preserved.items():
                    path = data / rel
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(text)
                (data / "codegen_setup.c").write_text("stale shipped source")
                launch()
                for rel, text in preserved.items():
                    self.assertEqual((data / rel).read_text(), text, rel)
                self.assertEqual((data / "codegen_setup.c").read_text(), files["codegen_setup.c"])
            finally:
                for path in payload.rglob("*"):
                    path.chmod(0o755 if path.is_dir() else 0o644)
                payload.chmod(0o755)


if __name__ == "__main__":
    unittest.main()
