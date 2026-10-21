#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 tools/source-storage.py restore
python3 tools/validate_anatomy.py --build
python3 tools/build-loading-packs.py
python3 tools/source-storage.py pack
node tools/build-viewer-catalogue.mjs
