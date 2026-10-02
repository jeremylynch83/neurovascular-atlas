#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 tools/validate_anatomy.py --build
