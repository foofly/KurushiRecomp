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

## Enhancements

The launcher Mods page contains optional Fit widescreen, Faster CD loading, Anti-aliasing, and Smooth motion features. Internal Resolution, PGXP Precision, Rewind, and other framework features are available in the same Mods page. Higher resolutions and some visual options require OpenGL. Smooth motion blends presentation frames without changing the game's simulation speed; moving objects can show trails.

## Controls and compatibility

Player 1 uses the first attached SDL gamepad by default. The game uses a digital pad; D-pad moves, Cross selects/marks/captures, Triangle activates Advantage Zones, Square speeds cube rotation, and Options pauses. The framework launcher provides controller configuration and remapping.

The USA build has been user-played with a PS5 controller. This is an experimental project: full-game completion, complete compatibility, and gameplay parity have not been established. See `docs/compatibility.md` for the current validation scope.

## Project boundaries

Do not commit or distribute disc images, extracted executables, generated game C, memory-card saves, captured gameplay images, or compiled game binaries. Do not add proprietary BIOS files. The included OpenBIOS source/binary is supplied by the framework under its own license. Check licenses and distribution rights for all dependencies and assets before publishing releases.

Project-authored material is offered under [PolyForm Noncommercial 1.0.0](LICENSE), for noncommercial use. This license applies only to material the project owner has rights to license; it grants no rights to Kurushi, game assets, or third-party components. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependency licenses.
