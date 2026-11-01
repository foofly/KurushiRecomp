#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ "${1:-}" == "--help" ]]; then
    echo 'Usage: ./play.sh [runtime arguments, e.g. --disc /path/to/game.cue]'
    echo 'KURUSHI_BUILD_DIR selects a build (default: build-release).'
    echo 'KURUSHI_RENDERER selects software or opengl (default: software).'
    echo 'KURUSHI_INTERNAL_RESOLUTION selects 1x..32x, 4k, display, etc. (default: 1x).'
    exit 0
fi
build_dir="${KURUSHI_BUILD_DIR:-$project_dir/build-release}"
[[ "$build_dir" = /* ]] || build_dir="$project_dir/$build_dir"
if [[ ! -x "$build_dir/Kurushi_Recompiled" ]]; then
    echo "Missing executable: $build_dir/Kurushi_Recompiled" >&2
    echo 'Run ./tools/build-playtest.sh first.' >&2
    exit 1
fi
cd "$project_dir"
runtime_args=(--game "$project_dir/game.toml" --memcard-dir "$project_dir/saves")
launcher_requested=0
for arg in "$@"; do
    if [[ "$arg" == "--launcher" ]]; then
        launcher_requested=1
        break
    fi
done
if [[ "$launcher_requested" == 0 ]]; then
    runtime_args+=(--no-launcher)
fi
if [[ -n "${KURUSHI_RENDERER:-}" ]]; then
    runtime_args+=(--renderer "$KURUSHI_RENDERER")
elif [[ "$launcher_requested" == 0 ]]; then
    runtime_args+=(--renderer software)
fi
if [[ -n "${KURUSHI_INTERNAL_RESOLUTION:-}" ]]; then
    export PSX_INTERNAL_RESOLUTION="$KURUSHI_INTERNAL_RESOLUTION"
fi
export PSX_HLE_SCHEDULER=0
exec "$build_dir/Kurushi_Recompiled" "${runtime_args[@]}" "$@"
