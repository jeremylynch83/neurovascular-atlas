#!/usr/bin/env bash
# Stable INR Anatomy Atlas updater/launcher.
# Keep this script in one folder. For each release, copy the new
# inr-anatomy-atlas-v*.zip beside it and run:  ./inr-anatomy.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_ROOT="${INR_ATLAS_HOME:-$HOME/INR-Anatomy-Atlas}"
DATA_ROOT="${INR_ANATOMY_DATA:-$HOME/INR-Anatomy-Data}"
RELEASES="$INSTALL_ROOT/releases"
CURRENT="$INSTALL_ROOT/current"
CONTAINER="inr-anatomy-atlas"
PORT="${PORT:-5173}"
mkdir -p "$RELEASES" "$DATA_ROOT"

usage() {
  cat <<EOF
INR Anatomy Atlas

  ./inr-anatomy.sh          install/update from newest ZIP beside this script, build and run
  ./inr-anatomy.sh restart  restart current release
  ./inr-anatomy.sh stop     stop atlas
  ./inr-anatomy.sh logs     follow container logs
  ./inr-anatomy.sh status   show installed release and container status

Persistent anatomy data: $DATA_ROOT
EOF
}

find_latest_zip() {
  find "$SCRIPT_DIR" -maxdepth 1 -type f -name 'inr-anatomy-atlas-v*.zip' -printf '%f\n' \
    | sort -V | tail -n1
}

print_urls() {
  echo "Open:      http://localhost:${PORT}"
  if command -v tailscale >/dev/null 2>&1; then
    local ip
    ip="$(tailscale ip -4 2>/dev/null | head -n1 || true)"
    [ -n "$ip" ] && echo "Tailscale: http://${ip}:${PORT}"
  fi
}

health_check() {
  local i
  for i in $(seq 1 30); do
    if curl -fsS "http://localhost:${PORT}/" >/dev/null 2>&1; then return 0; fi
    sleep 1
  done
  return 1
}

case "${1:-update}" in
  stop)
    docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
    echo "INR Anatomy Atlas stopped."
    exit 0 ;;
  logs)
    exec docker logs -f "$CONTAINER" ;;
  status)
    if [ -L "$CURRENT" ]; then echo "Current: $(readlink -f "$CURRENT")"; else echo "Current: none"; fi
    docker ps --filter "name=^/${CONTAINER}$"
    print_urls
    exit 0 ;;
  restart)
    if [ ! -L "$CURRENT" ]; then echo "No installed release. Put a release ZIP beside this script and run ./inr-anatomy.sh" >&2; exit 1; fi
    (cd "$(readlink -f "$CURRENT")" && INR_ANATOMY_DATA="$DATA_ROOT" PORT="$PORT" ./docker.sh restart)
    if ! health_check; then echo "ERROR: Atlas did not pass health check." >&2; exit 1; fi
    print_urls
    exit 0 ;;
  update|"") ;;
  help|-h|--help) usage; exit 0 ;;
  *) usage; exit 2 ;;
esac

command -v docker >/dev/null 2>&1 || { echo "ERROR: Docker is not installed or not in PATH." >&2; exit 1; }
command -v unzip >/dev/null 2>&1 || { echo "ERROR: unzip is required." >&2; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "ERROR: curl is required." >&2; exit 1; }

ZIP_NAME="$(find_latest_zip)"
[ -n "$ZIP_NAME" ] || { echo "ERROR: No inr-anatomy-atlas-v*.zip found beside $0" >&2; exit 1; }
ZIP="$SCRIPT_DIR/$ZIP_NAME"
VERSION="${ZIP_NAME%.zip}"
DEST="$RELEASES/$VERSION"
STAGE="$RELEASES/.${VERSION}.staging.$$"
OLD_CURRENT=""
[ -L "$CURRENT" ] && OLD_CURRENT="$(readlink -f "$CURRENT")"

# Give older pre-persistent installs one chance to migrate source/generated anatomy.
if [ -n "$OLD_CURRENT" ] && [ -x "$OLD_CURRENT/anatomy.sh" ]; then
  (cd "$OLD_CURRENT" && INR_ANATOMY_DATA="$DATA_ROOT" ./anatomy.sh migrate-local >/dev/null 2>&1 || true)
fi

rm -rf "$STAGE"
mkdir -p "$STAGE"
echo "Installing $ZIP_NAME ..."
unzip -q "$ZIP" -d "$STAGE"

# Accept either flat release ZIPs or a single enclosing folder.
ROOT="$STAGE"
shopt -s nullglob dotglob
entries=("$STAGE"/*)
if [ "${#entries[@]}" -eq 1 ] && [ -d "${entries[0]}" ]; then ROOT="${entries[0]}"; fi
shopt -u nullglob dotglob

[ -f "$ROOT/package.json" ] || { rm -rf "$STAGE"; echo "ERROR: Release ZIP does not contain package.json." >&2; exit 1; }
chmod +x "$ROOT/docker.sh" "$ROOT/anatomy.sh" "$ROOT/build-anatomy.sh" 2>/dev/null || true

# Build and start candidate before making it current. Existing TopBrain source is reused.
set +e
(cd "$ROOT" && INR_ANATOMY_DATA="$DATA_ROOT" PORT="$PORT" ./docker.sh restart)
rc=$?
set -e
if [ "$rc" -ne 0 ] || ! health_check; then
  echo "ERROR: New release failed to build/start or did not pass health check." >&2
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
  if [ -n "$OLD_CURRENT" ] && [ -x "$OLD_CURRENT/docker.sh" ]; then
    echo "Restoring previous release..."
    (cd "$OLD_CURRENT" && INR_ANATOMY_DATA="$DATA_ROOT" PORT="$PORT" ./docker.sh start) || true
  fi
  rm -rf "$STAGE"
  exit 1
fi

rm -rf "$DEST"
if [ "$ROOT" = "$STAGE" ]; then
  mv "$STAGE" "$DEST"
else
  mv "$ROOT" "$DEST"
  rm -rf "$STAGE"
fi
ln -sfn "$DEST" "$INSTALL_ROOT/.current.new"
mv -Tf "$INSTALL_ROOT/.current.new" "$CURRENT"

echo
echo "✓ Release extracted"
echo "✓ Persistent anatomy reused from $DATA_ROOT"
echo "✓ Docker image built"
echo "✓ Container started"
echo "✓ Health check passed"
echo "Current:   $DEST"
print_urls
