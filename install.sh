#!/usr/bin/env bash
set -euo pipefail
command -v git >/dev/null 2>&1 || { echo 'FAIL: git is required' >&2; exit 1; }
mm_python="$(command -v python3 || command -v python || true)"
[[ -n "$mm_python" ]] || { echo 'FAIL: Python 3.10+ is required' >&2; exit 1; }
mm_entry="$("$mm_python" -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve())' "$0")"
mm_root="$(dirname "$mm_entry")"
"$mm_python" "$mm_root/scripts/stack.py" install "$@"
exec bash "$mm_root/verify.sh"
