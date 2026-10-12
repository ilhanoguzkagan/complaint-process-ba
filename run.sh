#!/usr/bin/env bash
# Regenerate everything: data -> analysis -> UAT pack. Uses $PYTHON if set, else python3.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
"$PY" scripts/generate_data.py
"$PY" scripts/analyse.py
"$PY" scripts/build_uat.py
