#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 tools/validate_anatomy.py --build
python3 tools/build-loading-packs.py
node tools/build-viewer-catalogue.mjs
