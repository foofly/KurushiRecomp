#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "${1:-}" == "--help" ]]; then
    echo 'Usage: ./tools/build-playtest.sh [build-directory]'
    echo 'Default: build-release. KURUSHI_BUILD_JOBS defaults to 4.'
    echo 'Requires already generated game and OpenBIOS C; see README.md.'
    exit 0
fi
build_dir="${1:-$project_dir/build-release}"
[[ "$build_dir" = /* ]] || build_dir="$project_dir/$build_dir"
if [[ ! -f "$project_dir/generated/SCUS_941.81_dispatch.c" || ! -f "$project_dir/psxrecomp/generated/OpenBIOS_full.c" ]]; then
    echo 'Generated game/OpenBIOS sources missing. Follow README.md generation steps.' >&2
    exit 1
fi
framework_patch="$project_dir/psxrecomp-post-aa.patch"
if ! rg -q 'int psx_mod_set_post_aa\(' "$project_dir/psxrecomp/runtime/include/mod_plugins.h"; then
    git -C "$project_dir/psxrecomp" apply --check "$framework_patch"
    git -C "$project_dir/psxrecomp" apply "$framework_patch"
fi
cmake -S "$project_dir" -B "$build_dir" -G Ninja \
    -DCMAKE_BUILD_TYPE=Release -DPSX_EXECUTION_PROFILE=REFERENCE \
    -DPSX_GL_BATCH_IMPL=LLE -DPSX_ENABLE_VULKAN=OFF -DPSX_DEBUG_TOOLS=ON
cmake --build "$build_dir" --target psx-runtime --parallel "${KURUSHI_BUILD_JOBS:-4}"
