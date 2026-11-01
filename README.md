# Kurushi Recompiled

An experimental native build of the USA release of *I.Q: Intelligent Qube*, powered by [PSXRecomp](https://github.com/mstan/psxrecomp).

This repository contains project configuration, enhancement code, and build tools. It does **not** include the game disc, extracted executable, generated game code, screenshots, or retail BIOS. You need to provide your own legally obtained disc image. Generated files are derived locally and must not be committed or uploaded.

## Build

Initialize the framework submodules and build the code generators:

```sh
git submodule update --init --recursive
bash psxrecomp/tools/ci/build_emitters.sh
```

Place the matching USA CUE/BIN files under `disc/`, or keep them elsewhere and pass the CUE path to the generation command:

```sh
python3 psxrecomp/psxrecomp_cli.py generate \
  --no-toolchain-download \
  --config game.toml \
  --project-root . \
  --disc "/path/to/your/I.Q.cue"
./tools/build-playtest.sh
```

The generated game C stays in the ignored `generated/` directory. `build-playtest.sh` also applies the small tracked PSXRecomp API patch required by the anti-aliasing option. Use `./tools/build-playtest.sh --help` for build options.

For a normal direct launch, run `./play.sh`. Open the launcher with `./play.sh --launcher`. If the game disc is outside `disc/`, pass it explicitly:

```sh
./play.sh --disc "/path/to/your/I.Q.cue"
```

## Run a CI build

The [Cross-platform build workflow](https://github.com/foofly/KurushiRecomp/actions/workflows/cross-platform-build.yml) builds setup hosts for Linux x64, Linux ARM64, Windows x64, macOS Intel, and Apple Silicon. Each artifact is retained for 14 days. These hosts do not contain game code or a disc image. They open the first-run wizard, where you select your own disc and generate the game locally.

First, clone the source with its submodules. The setup wizard needs the local PSXRecomp CLI and source tree to generate and rebuild the game. Apply the tracked anti-aliasing API patch as well:

```sh
git clone --recurse-submodules https://github.com/foofly/KurushiRecomp.git
cd KurushiRecomp
if ! grep -q 'int psx_mod_set_post_aa(' psxrecomp/runtime/include/mod_plugins.h; then
  git -C psxrecomp apply "$PWD/psxrecomp-post-aa.patch"
fi
```

For Windows PowerShell, use this patch check instead:

```powershell
if (-not (Select-String -Quiet -Path psxrecomp/runtime/include/mod_plugins.h -Pattern 'int psx_mod_set_post_aa\(')) {
  git -C psxrecomp apply (Join-Path $PWD 'psxrecomp-post-aa.patch')
}
```

Open the workflow link, choose a successful run, and download the artifact matching your platform:

| Platform | Artifact |
| --- | --- |
| Linux x64 | `kurushi-linux-x64-setup-host` |
| Linux ARM64 | `kurushi-linux-arm64-setup-host` |
| Windows x64 | `kurushi-windows-x64-setup-host` |
| macOS Intel | `kurushi-macos-intel-setup-host` |
| macOS Apple Silicon | `kurushi-macos-arm64-setup-host` |

Extract the downloaded artifact into the root of the cloned project, alongside `game.toml` and the `psxrecomp/` directory. Allow it to merge the included runtime folders. Start the executable from the project root:

- **Linux x64 / ARM64:** run `./Kurushi_Recompiled` in a terminal.
- **Windows x64:** run `Kurushi_Recompiled.exe`, or in PowerShell use `./Kurushi_Recompiled.exe`.
- **macOS Intel / Apple Silicon:** in Terminal, run `chmod +x ./Kurushi_Recompiled && ./Kurushi_Recompiled`.

In the launcher, use the setup wizard to browse to your legally obtained matching USA disc image (select the `.cue` when you have a CUE/BIN dump), then choose **Generate & rebuild**. The wizard uses the cloned source and generates game code locally, rebuilds the runtime, and relaunches it. Generated code and the disc image stay on your machine. See [Build](#build) for the manual equivalent. CI artifacts are temporary setup hosts, not releases or prebuilt game binaries.

## Enhancements

The launcher Mods page contains optional Fit widescreen, Faster CD loading, Anti-aliasing, and Smooth motion features. Internal Resolution, PGXP Precision, Rewind, and other framework features are available in the same Mods page. Higher resolutions and some visual options require OpenGL. Smooth motion blends presentation frames without changing the game's simulation speed; moving objects can show trails.

## Controls and compatibility

Player 1 uses the first attached SDL gamepad by default. The game uses a digital pad; D-pad moves, Cross selects/marks/captures, Triangle activates Advantage Zones, Square speeds cube rotation, and Options pauses. The framework launcher provides controller configuration and remapping.

The USA build has been user-played with a PS5 controller. This is an experimental project: full-game completion, complete compatibility, and gameplay parity have not been established. See `docs/compatibility.md` for the current validation scope.

## Project boundaries

Do not commit or distribute disc images, extracted executables, generated game C, memory-card saves, captured gameplay images, or compiled game binaries. Do not add proprietary BIOS files. The included OpenBIOS source/binary is supplied by the framework under its own license. Check licenses and distribution rights for all dependencies and assets before publishing releases.

Project-authored material is offered under [PolyForm Noncommercial 1.0.0](LICENSE), for noncommercial use. This license applies only to material the project owner has rights to license; it grants no rights to Kurushi, game assets, or third-party components. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependency licenses.
