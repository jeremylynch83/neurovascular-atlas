#!/bin/sh
set -eu
cd "$(dirname "$0")"
CMD="${1:-help}"; shift || true
DATA="$PWD/anatomy-source/topbrain"
IMAGE="inr-anatomy-builder:0.3"
case "$CMD" in
  setup)
    docker build -f Dockerfile.anatomy -t "$IMAGE" . ;;
  download)
    mkdir -p "$DATA/raw"
    docker image inspect "$IMAGE" >/dev/null 2>&1 || docker build -f Dockerfile.anatomy -t "$IMAGE" .
    docker run --rm -v "$PWD:/work" "$IMAGE" python tools/topbrain/download_topbrain.py anatomy-source/topbrain/raw ;;
  inspect)
    docker image inspect "$IMAGE" >/dev/null 2>&1 || docker build -f Dockerfile.anatomy -t "$IMAGE" .
    docker run --rm -v "$PWD:/work" "$IMAGE" python tools/topbrain/inspect_topbrain.py anatomy-source/topbrain/raw ;;
  build)
    CASE="${1:-}"
    if [ -z "$CASE" ]; then echo "Usage: ./anatomy.sh build <case-id, e.g. 001>"; exit 2; fi
    docker image inspect "$IMAGE" >/dev/null 2>&1 || docker build -f Dockerfile.anatomy -t "$IMAGE" .
    docker run --rm -v "$PWD:/work" "$IMAGE" python tools/topbrain/build_topbrain.py anatomy-source/topbrain/raw "$CASE"
    python3 tools/validate_anatomy.py --build ;;
  *)
    echo "TopBrain v0.3 anatomy pipeline"
    echo "  ./anatomy.sh download       download official TopBrain v3 (about 2 GB)"
    echo "  ./anatomy.sh inspect        inventory/score available paired cases"
    echo "  ./anatomy.sh build 001      generate scan-derived meshes for a case"
    echo "  ./anatomy.sh setup          pre-build the Python anatomy container" ;;
esac
