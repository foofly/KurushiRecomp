#!/usr/bin/env bash
# Local packaging helper. It expects an executable built locally from game
# sources generated from the user's disc. Do not run this in CI or upload its
# output: the compiled game contains material derived from the original game.
# Autofilled by tools/new_project_layout/setup_project.{sh,ps1}.
#
# Packages the local executable, runtime data, bundled OpenBIOS, mod catalog,
# and overlay toolchain. No game source or disc data is copied by this script.
#
# Usage:
#   scripts/package_prebuilt_release.sh <build-dir> <artifact-tag> [recompiler-build-dir]
#
# Writes: dist/kurushi-<VERSION>-<artifact-tag>.zip
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="${1:-}"
ARTIFACT_TAG="${2:-}"
RECOMPILER_BUILD="${3:-build-recompiler}"

if [[ -z "${BUILD_DIR}" || -z "${ARTIFACT_TAG}" ]]; then
  echo "usage: $0 <build-dir> <artifact-tag> [recompiler-build-dir]" >&2
  exit 2
fi

PACKAGER="${ROOT}/psxrecomp/tools/package_game_release.sh"
if [[ ! -f "${PACKAGER}" ]]; then
  echo "error: missing ${PACKAGER} (psxrecomp submodule predates bundled releases -- bump it)" >&2
  exit 1
fi
chmod +x "${PACKAGER}" 2>/dev/null || true

EXTRA=()
# Overlay shard cache. It is compiled from the disc and remains local. A
# developer may supply it for local experiments:
#   PSX_OVERLAY_CACHE_ROOT=/path/to/cache scripts/package_prebuilt_release.sh ...
if [[ -n "${PSX_OVERLAY_CACHE_ROOT:-}" ]]; then
  EXTRA+=(--overlay-cache-root "${PSX_OVERLAY_CACHE_ROOT}")
else
  EXTRA+=(--ship-without-overlay-cache-because \
    "no local overlay cache supplied; the runtime compiles needed overlays from the user's disc")
fi
# Extra docs shipped at the zip root (DISC.md tells players which dump works).
for _doc in DISC.md; do
  if [[ -f "${ROOT}/${_doc}" ]]; then
    EXTRA+=(--doc "${_doc}")
  fi
done

cd "${ROOT}"
exec bash "${PACKAGER}" \
  --root "${ROOT}" \
  --build-dir "${BUILD_DIR}" \
  --artifact "${ARTIFACT_TAG}" \
  --zip-prefix kurushi \
  --exe-name Kurushi_Recompiled \
  --display-name "Kurushi Recompiled" \
  --recompiler-build "${RECOMPILER_BUILD}" \
  --version-env RELEASE_VERSION \
  --disc-hint "your legally owned Kurushi disc" \
  "${EXTRA[@]}"
