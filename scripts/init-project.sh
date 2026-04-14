#!/usr/bin/env bash
# Initialize Python backend (venv + pip) or print hints for Node/PHP.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KIND="${1:-}"
TARGET="${2:-}"

usage() {
  echo "Usage: $0 <django|flask|vue|react|angular> <path-to-project>"
  exit 1
}

[[ -n "$KIND" && -n "$TARGET" ]] || usage

cd "$ROOT/$TARGET"

case "$KIND" in
  django|flask)
    python3 -m venv .venv
    # shellcheck source=/dev/null
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Python venv ready at $TARGET/.venv"
    ;;
  vue|react)
    npm install
    echo "Node modules installed in $TARGET"
    ;;
  angular)
    npm install
    echo "Node modules installed in $TARGET"
    ;;
  *)
    usage
    ;;
esac
