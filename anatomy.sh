#!/bin/sh
set -eu
cd "$(dirname "$0")"
case "${1:-help}" in
  ensure-reference|sync|validate|build) python3 tools/validate_anatomy.py --build ;;
  migrate-local) : ;; # Compatibility with the existing installer. Leave old data untouched.
  where) pwd ;;
  *) echo "INR Anatomy Atlas v0.8.2: prebuilt combined anatomy. Run ./anatomy.sh validate" ;;
esac
