# Kurushi Recompiled

An experimental native recompile of the USA release of *I.Q: Intelligent Qube*, built with [PSXRecomp](https://github.com/mstan/psxrecomp).

The project provides a launcher and a setup package. You supply your own game disc image; the launcher generates and builds the game locally. Disc images, retail BIOS files, and generated game code are not included.

## Play

Download the ZIP for your platform from the [v0.1.0 release](https://github.com/foofly/KurushiRecomp/releases/tag/v0.1.0). Future versions will be listed on the [Releases page](https://github.com/foofly/KurushiRecomp/releases).

| Platform | Artifact |
| --- | --- |
| Linux x64 | `kurushi-0.1.0-linux-x64.zip` |
| Linux ARM64 | `kurushi-0.1.0-linux-arm64.zip` |
| Windows x64 | `kurushi-0.1.0-windows-x64.zip` |
| macOS Intel | `kurushi-0.1.0-macos-intel.zip` |
| macOS Apple Silicon | `kurushi-0.1.0-macos-arm64.zip` |

Download `SHA256SUMS` from the same release if you want to verify the ZIP. On Linux or macOS, put it beside the downloaded ZIP and run `sha256sum -c SHA256SUMS`. On Windows, compare the output of `Get-FileHash .\kurushi-0.1.0-windows-x64.zip -Algorithm SHA256` with the Windows entry in `SHA256SUMS`.

Extract the ZIP and run `Kurushi_Recompiled` (`Kurushi_Recompiled.exe` on Windows). On macOS, run `chmod +x ./Kurushi_Recompiled` first if needed.

On first launch, the setup screen asks for your legally obtained USA disc image. For a CUE/BIN dump, choose the `.cue` file. Choose **Generate & rebuild** to create the playable game on your computer. Windows and Linux x64 download the build toolchain automatically when needed. macOS downloads CMake, Ninja, and Python automatically, but Apple’s Command Line Tools must be installed first (`xcode-select --install` in Terminal). Linux ARM64 needs CMake, Ninja, Python 3, and C/C++ compilers installed from the system package manager because no portable ARM64 toolchain is currently published. When the build finishes, the launcher opens the game and remembers the disc path. Use **Load Disc Image** in the launcher to choose or change the image for a later launch.

The v0.1.0 downloads predate automatic toolchain downloads on Linux and macOS; they require the native build tools to be installed.

The setup package includes the project source, PSXRecomp tools, and the launcher; it does not include game data. Portable build tools are downloaded from the upstream [RetroPorting Toolchains releases](https://github.com/RetroPortingToolKit/RetroPorting-Toolchains/releases) and stored in the user’s toolchain cache. Windows, Linux x64, and macOS need an internet connection the first time the launcher prepares the build. macOS also requires Apple’s Command Line Tools. Linux ARM64 users need to install the listed build tools themselves.

Each versioned `vX.Y.Z` tag builds and publishes all five platform ZIPs together. For in-progress builds, see the [Actions workflow](https://github.com/foofly/KurushiRecomp/actions/workflows/cross-platform-build.yml); those artifacts expire after 14 days.

## Controls

Player 1 uses the first attached SDL gamepad by default. The D-pad moves, Cross selects, marks, or captures, Triangle activates Advantage Zones, Square speeds up cube rotation, and Options pauses. The launcher provides controller configuration and remapping.

## Enhancements

The launcher's Mods page includes optional Fit widescreen, Faster CD loading, Anti-aliasing, and Smooth motion. Internal Resolution, PGXP Precision, Rewind, and other framework features are also available there. Higher resolutions and some visual options require OpenGL. Smooth motion blends presentation frames without changing game simulation speed; moving objects can show trails.

## Compatibility

The USA build has been played with a PS5 controller. Full-game completion, complete compatibility, and gameplay parity have not been established. See [docs/compatibility.md](docs/compatibility.md) for the current validation scope.

## Build from source

The setup package is intended for players. To build manually from a checkout, initialize the submodules, build the code generators, generate from your own disc, then build the runtime:

```sh
git clone --recurse-submodules https://github.com/foofly/KurushiRecomp.git
cd KurushiRecomp
bash psxrecomp/tools/ci/build_emitters.sh

python3 psxrecomp/psxrecomp_cli.py generate \
  --no-toolchain-download \
  --config game.toml \
  --project-root . \
  --disc "/path/to/your/I.Q.cue"

./tools/build-playtest.sh
```

Generated game code is written to the ignored `generated/` directory. The build helper applies the anti-aliasing framework patch if needed. Run `./tools/build-playtest.sh --help` for build options.

## Project boundaries and license

Do not commit or upload game disc images, extracted game executables, generated game code, memory-card saves, captured gameplay, or retail BIOS files. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependency notices.

Project-authored material is offered under [PolyForm Noncommercial 1.0.0](LICENSE). That license covers only material the project owner has rights to license; it grants no rights to *Kurushi*, game assets, or third-party components.
