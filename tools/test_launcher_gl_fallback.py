#!/usr/bin/env python3
"""Render launcher UI through production SDL code with Mesa capped at GL 3.0."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROBE = r'''#include "common/launcher_platform.h"
#include "imgui.h"
#include "imgui_impl_opengl3.h"
#include <SDL3/SDL_opengl.h>
#include <cstdio>
extern "C" void launcher_boot_timing_mark(const char*) {}
int main() {
    LauncherPlatform platform;
    if (!launcher_platform_open(&platform, "Launcher GL compatibility probe", 320, 240)) return 1;
    std::printf("GL: %s\n", glGetString(GL_VERSION));
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO();
    io.IniFilename = nullptr;
    io.DisplaySize = ImVec2(320, 240);
    io.DeltaTime = 1.0f / 60.0f;
    if (!ImGui_ImplOpenGL3_Init(nullptr)) return 2;
    ImGui_ImplOpenGL3_NewFrame();
    ImGui::NewFrame();
    ImGui::Begin("Compatibility check");
    ImGui::Text("Launcher renders on GL 3.0");
    ImGui::End();
    ImGui::Render();
    glViewport(0, 0, 320, 240);
    glClear(GL_COLOR_BUFFER_BIT);
    ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
    if (glGetError() != GL_NO_ERROR) return 3;
    ImGui_ImplOpenGL3_Shutdown();
    ImGui::DestroyContext();
    launcher_platform_close(&platform);
    return 0;
}
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cc", default="cc")
    parser.add_argument("--cxx", default="c++")
    parser.add_argument("--sdl-source", type=Path, required=True)
    parser.add_argument("--sdl-build", type=Path, required=True)
    parser.add_argument("--sdl-library", type=Path)
    args = parser.parse_args()
    ui = ROOT / "recomp-ui/src"
    imgui = ui / "third_party/imgui"
    includes = ["-I" + str(ui), "-I" + str(imgui), "-I" + str(imgui / "backends"),
                "-I" + str(args.sdl_source.resolve() / "include"),
                "-I" + str(args.sdl_build.resolve() / "include")]
    with tempfile.TemporaryDirectory(prefix="kurushi-launcher-gl-") as tmp:
        work = Path(tmp)
        probe = work / "probe.cpp"
        probe.write_text(PROBE)
        common = ["-DLNG_SDL3", "-DSDL_MAIN_HANDLED", "-ffunction-sections", "-fdata-sections", *includes]
        subprocess.run([args.cc, *common, "-c", str(ui / "common/launcher_platform_sdl3.c"), "-o", str(work / "platform.o")], check=True)
        binary = work / "probe"
        subprocess.run([args.cxx, *common, "-std=c++17", "-no-pie", str(probe), str(work / "platform.o"),
                        *[str(imgui / name) for name in ("imgui.cpp", "imgui_draw.cpp", "imgui_tables.cpp", "imgui_widgets.cpp", "backends/imgui_impl_opengl3.cpp")],
                        str(args.sdl_library.resolve() if args.sdl_library else args.sdl_build.resolve() / "libSDL3.a"), "-Wl,--gc-sections", "-l:libGL.so.1", "-ldl", "-lm", "-lpthread", "-o", str(binary)], check=True)
        base = dict(os.environ, SDL_VIDEO_DRIVER="offscreen", LIBGL_ALWAYS_SOFTWARE="1", LNG_SCRIPT="probe", LNG_TEST_HIDDEN="1")
        for label, overrides in (("default", {}), ("GL 3.0 fallback", {"MESA_GL_VERSION_OVERRIDE": "3.0", "MESA_GLSL_VERSION_OVERRIDE": "130"})):
            result = subprocess.run([str(binary)], env=dict(base, **overrides), capture_output=True, text=True)
            print(label + ":\n" + result.stdout + result.stderr, flush=True)
            assert result.returncode == 0, result.returncode
            if overrides:
                assert "using OpenGL 3.0 fallback context" in result.stderr
    print("PASS: default and GL 3.0 launcher contexts render ImGui")


if __name__ == "__main__":
    main()
