# Kurushi Recompiled

An experimental native recompile of the USA release of *I.Q: Intelligent Qube*, built with [PSXRecomp](https://github.com/mstan/psxrecomp).

The project provides a launcher and a setup package. You supply your own game disc image; the launcher generates and builds the game locally. Disc images, retail BIOS files, and generated game code are not included.

## Play

Download the matching asset from the [v0.1.6 release](https://github.com/foofly/KurushiRecomp/releases/tag/v0.1.6). Future versions are listed on the [Releases page](https://github.com/foofly/KurushiRecomp/releases).

| Platform | v0.1.6 download |
| --- | --- |
| Linux x64 | `kurushi-0.1.6-linux-x86_64.AppImage` (recommended) or `kurushi-0.1.6-linux-x64.zip` |
| Linux ARM64 | `kurushi-0.1.6-linux-arm64.zip` |
| Windows x64 | `kurushi-0.1.6-windows-x64.zip` |
| macOS Intel | `kurushi-0.1.6-macos-intel.zip` |
| macOS Apple Silicon | `kurushi-0.1.6-macos-arm64.zip` |

To verify a download, also download `SHA256SUMS` from the release. On Linux, compare `sha256sum <filename>` with the matching entry. On macOS, compare `shasum -a 256 <filename>`. On Windows PowerShell, compare `(Get-FileHash .\<filename> -Algorithm SHA256).Hash` with the matching entry in `SHA256SUMS`.

### Linux x64 AppImage

Make the AppImage executable once, then launch it:

```sh
chmod +x ./kurushi-0.1.6-linux-x86_64.AppImage
./kurushi-0.1.6-linux-x86_64.AppImage
```

The AppImage includes the launcher, build tools, and Linux runtime libraries. It does not include a Linux kernel or graphics driver. Settings, saves, and generated game files are stored in your user data directory. On Steam Deck, use Desktop Mode to try it; Steam Deck compatibility has not yet been verified. The AppImage is x86_64 only.

### Linux ZIP

Extract `kurushi-0.1.6-linux-x64.zip`, then run `./Kurushi_Recompiled` from the extracted directory. The Linux x64 build uses Ubuntu 22.04 system libraries for compatibility with older Linux distributions. The ZIP includes the build toolchain. Linux ARM64 users should extract `kurushi-0.1.6-linux-arm64.zip` and run `./Kurushi_Recompiled`; that build requires CMake, Ninja, Python 3, and a C/C++ compiler installed from the system package manager.

### Windows x64

Extract `kurushi-0.1.6-windows-x64.zip` and double-click `Kurushi_Recompiled.exe`. The ZIP includes the Windows build tools.

### macOS

Extract the ZIP for your Mac: use `kurushi-0.1.6-macos-intel.zip` for an Intel Mac or `kurushi-0.1.6-macos-arm64.zip` for Apple Silicon. In Terminal, change to the extracted folder and run:

```sh
chmod +x ./Kurushi_Recompiled
./Kurushi_Recompiled
```

Both macOS builds include the portable build tools, but still require Apple’s Command Line Tools. If needed, install them with `xcode-select --install` in Terminal.

### First launch

The setup screen asks for your legally obtained USA disc image. For a CUE/BIN dump, select the `.cue` file. Choose **Generate & rebuild** to create the playable game on your computer. When the build finishes, the launcher opens the game and remembers the disc path. Use **Load Disc Image** in the launcher to choose or change the image later.

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

## AI usage disclosure

This project has been developed with substantial assistance from AI tools, including OpenAI Codex. AI has been used to write and modify code, build and packaging scripts, documentation, and GitHub workflows, and to help investigate bugs and run tests.

The maintainer directs the work and takes responsibility for the published project. AI-generated changes can contain mistakes, and successful builds and automated tests do not establish full game compatibility. See [Compatibility](#compatibility) for the current testing limits.

This disclosure covers development work in this repository. Game-code generation during setup is performed by PSXRecomp using the disc image you supply.
