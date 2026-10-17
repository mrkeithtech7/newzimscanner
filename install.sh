#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"
command -v python3 >/dev/null || { echo "python3 is required (install it with: pkg install python)" >&2; exit 1; }
python3 - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise SystemExit("Python 3.10 or later is required")
print(f"Python {sys.version.split()[0]} ready")
PY
chmod +x kts
echo "KEITH TECH SCANNER installed in $DIR"
echo "Run: python3 main.py (or ./kts)"
