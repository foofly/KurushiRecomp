#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(tr -d '[:space:]' < "$ROOT/VERSION")"
PAYLOAD="$ROOT/dist/stage-setup-linux-x64"
META="$(mktemp -d "${TMPDIR:-/tmp}/kurushi-appimage-meta.XXXXXXXX")"
trap 'rm -rf "$META"' EXIT

if [[ ! -d "$PAYLOAD" ]]; then
  echo "missing Linux setup payload: $PAYLOAD" >&2
  exit 1
fi

sed \
  -e "s|@APP_NAME@|Kurushi|g" \
  -e "s|@EXE_NAME@|Kurushi_Recompiled|g" \
  -e "s|@PAYLOAD_DIR@|kurushi|g" \
  -e "s|@ARTIFACT_NAME@|kurushi|g" \
  -e "s|@VERSION@|$VERSION|g" \
  "$ROOT/packaging/linux/AppRun" > "$META/AppRun"
chmod 0755 "$META/AppRun"
rm -f "$ROOT/dist/kurushi-$VERSION-linux-x86_64.AppImage" \
  "$ROOT/dist/kurushi-$VERSION-linux-x86_64.AppImage.sha256"

bash "$ROOT/psxrecomp/tools/package_appimage.sh" \
  --payload "$PAYLOAD" \
  --exe-name Kurushi_Recompiled \
  --payload-name kurushi \
  --app-run "$META/AppRun" \
  --desktop-file "$ROOT/packaging/linux/kurushi.desktop" \
  --icon "$ROOT/assets/psxrecomp.png" \
  --output "$ROOT/dist/kurushi-$VERSION-linux-x86_64.AppImage" \
  --prune-unreferenced-libs
