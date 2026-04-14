#!/usr/bin/env python3
"""
Copy a PolyStack backend or frontend template to a new directory.
Usage:
  python copy-template.py backend flask_vue my_api
  python copy-template.py frontend vue-template my-vue-app
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser(description="Copy PolyStack template folder")
    p.add_argument("kind", choices=("backend", "frontend"))
    p.add_argument("name", help="Template folder name, e.g. flask_vue or vue-template")
    p.add_argument("dest", help="Destination folder name (created under backend/ or frontend/)")
    args = p.parse_args()

    if args.kind == "backend":
        src = ROOT / "backend" / _backend_subdir(args.name) / args.name
        dst = ROOT / "backend" / _backend_subdir(args.name) / args.dest
    else:
        src = ROOT / "frontend" / args.name
        dst = ROOT / "frontend" / args.dest

    if not src.is_dir():
        print(f"Source not found: {src}", file=sys.stderr)
        return 1
    if dst.exists():
        print(f"Destination already exists: {dst}", file=sys.stderr)
        return 1

    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
        ".venv", "venv", "__pycache__", "node_modules", "vendor", ".git",
    ))
    print(f"Copied {src} -> {dst}")
    return 0


def _backend_subdir(template_name: str) -> str:
    if template_name.startswith("django_"):
        return "django"
    if template_name.startswith("laravel_"):
        return "laravel"
    if template_name.startswith("flask_"):
        return "flask"
    raise SystemExit(
        "Backend template name must start with django_, laravel_, or flask_"
    )


if __name__ == "__main__":
    raise SystemExit(main())
