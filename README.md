# Kurushi Recompiled

An experimental native recompile of the USA release of *I.Q: Intelligent Qube*, built with [PSXRecomp](https://github.com/mstan/psxrecomp).

The project provides a launcher and a setup package. You supply your own game disc image; the launcher generates and builds the game locally. Disc images, retail BIOS files, and generated game code are not included.

## Play

Download the ZIP for your platform from the [latest release](https://github.com/foofly/KurushiRecomp/releases/latest). Linux x64 users can also download the AppImage.

| Platform | Artifact |
| --- | --- |
| Linux x64 | `kurushi-<version>-linux-x86_64.AppImage` or `kurushi-<version>-linux-x64.zip` |
| Linux ARM64 | `kurushi-<version>-linux-arm64.zip` |
| Windows x64 | `kurushi-<version>-windows-x64.zip` |
| macOS Intel | `kurushi-<version>-macos-intel.zip` |
| macOS Apple Silicon | `kurushi-<version>-macos-arm64.zip` |

Download `SHA256SUMS` from the same release if you want to verify a download. On Linux or macOS, put it beside the file and run `sha256sum -c SHA256SUMS`. On Windows, compare the output of `Get-FileHash .\kurushi-<version>-windows-x64.zip -Algorithm SHA256` with its entry in `SHA256SUMS`.

For a Linux AppImage, run `chmod +x ./kurushi-<version>-linux-x86_64.AppImage` once, then launch it. The AppImage bundles Linux runtime libraries and stores settings, saves, and generated files in your user data directory. The Linux x64 ZIP is an alternative if you prefer an extracted folder. For other platforms, extract the ZIP and run `Kurushi_Recompiled` (`Kurushi_Recompiled.exe` on Windows). On macOS, run `chmod +x ./Kurushi_Recompiled` first if needed.

On first launch, the setup screen asks for your legally obtained USA disc image. For a CUE/BIN dump, choose the `.cue` file. Choose **Generate & rebuild** to create the playable game on your computer. Windows, Linux x64, and macOS releases include their platform build tools, so the launcher does not need to download a toolchain. macOS still requires Apple’s Command Line Tools (`xcode-select --install` in Terminal). Linux ARM64 has no published portable toolchain pack and requires CMake, Ninja, Python 3, and C/C++ compilers from the system package manager. When the build finishes, the launcher opens the game and remembers the disc path. Use **Load Disc Image** in the launcher to choose or change the image for a later launch.

Linux x64 releases are built against Ubuntu 22.04 system libraries to improve compatibility with SteamOS and older distributions. The AppImage bundles additional runtime libraries; it does not bundle a Linux kernel or graphics driver. Steam Deck use has not yet been verified.

The v0.1.0 and v0.1.1 downloads do not include the build tools. Use v0.1.2 or newer for bundled tools on Windows, Linux x64, and macOS.

The setup package includes the project source, PSXRecomp tools, launcher, and platform build toolchain where available; it does not include game data. Bundled toolchain components retain their upstream licenses and notices under `toolchain/`. The Linux x64 ZIP is larger because it includes the compiler and dependencies. Linux ARM64 users need to install the listed build tools themselves.

Each versioned `vX.Y.Z` tag builds and publishes all five platform ZIPs together, plus the Linux x64 AppImage. For in-progress builds, see the [Actions workflow](https://github.com/foofly/KurushiRecomp/actions/workflows/cross-platform-build.yml); those artifacts expire after 14 days.

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
