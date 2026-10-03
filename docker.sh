#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
IMAGE="inr-anatomy-atlas:0.7.2"
CONTAINER="inr-anatomy-atlas"
PORT="${PORT:-5173}"

case "${1:-start}" in
  stop)
    docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
    echo "INR Anatomy Atlas stopped."
    exit 0
    ;;
  restart)
    ;;
  start|"") ;;
  logs)
    exec docker logs -f "$CONTAINER"
    ;;
  *) echo "Usage: ./docker.sh [start|restart|stop|logs]"; exit 2 ;;
esac

# The complete model is bundled; historical cached models are not imported.
./anatomy.sh ensure-reference

docker build -t "$IMAGE" .
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --rm --name "$CONTAINER" -p "${PORT}:80" "$IMAGE" >/dev/null

echo "INR Anatomy Atlas started."
echo "Local:     http://localhost:${PORT}"
if command -v tailscale >/dev/null 2>&1; then
  TS_IP="$(tailscale ip -4 2>/dev/null | head -n1 || true)"
  if [ -n "$TS_IP" ]; then echo "Tailscale: http://${TS_IP}:${PORT}"; fi
fi
echo "Stop:      ./docker.sh stop"
