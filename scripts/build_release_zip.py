#!/usr/bin/env python3
"""
Build a curated ZIP release artifact for BakeBot.

Usage:
  python scripts/build_release_zip.py -v v1.0.0
  python scripts/build_release_zip.py --version v1.0.0 --output-name BakeBot-v1.0.0.zip

By default, the ZIP will be created under ./dist/
Includes only files useful for streamers and excludes secrets, caches, VCS and build artifacts.
"""

import argparse
import hashlib
import os
from pathlib import Path
import sys
import time
import zipfile
import fnmatch

ROOT = Path(__file__).resolve().parents[1]

INCLUDE_DIRS = [
    'bot',
    'install',
    'docs',
]

INCLUDE_FILES = [
    'requirements.txt',
    'README.md',
    'TECHNICAL.md',
]

# Patterns to exclude (directories or files)
EXCLUDE_DIRS = [
    '.git', '.vs', '.vscode', '__pycache__',
    'node_modules', 'env', 'venv', '.venv',
    'logs', 'dist', 'build', '.cache', '.pytest_cache',
]

EXCLUDE_GLOBS = [
    '.env',
    '*.env',
    '*.pyc', '*.pyo',
    '*.sqlite3', '*.db', 'bot_data.sqlite3',
    '*.log',
]


def should_exclude(path: Path) -> bool:
    # Directory exclusion
    parts = set(p.name for p in path.parents) | {path.name}
    for d in EXCLUDE_DIRS:
        if d in parts:
            return True
    # Glob exclusion
    rel = str(path.as_posix())
    for pattern in EXCLUDE_GLOBS:
        if fnmatch.fnmatch(path.name, pattern) or fnmatch.fnmatch(rel, pattern):
            return True
    return False


def add_path(z: zipfile.ZipFile, root: Path, p: Path):
    if p.is_dir():
        for sub in p.rglob('*'):
            if sub.is_file() and not should_exclude(sub):
                arc = sub.relative_to(root)
                z.write(sub, arcname=str(arc).replace('\\', '/'))
    else:
        if not should_exclude(p):
            arc = p.relative_to(root)
            z.write(p, arcname=str(arc).replace('\\', '/'))


def build_zip(version: str, output_name: str | None = None) -> Path:
    ts = time.strftime('%Y%m%d-%H%M%S')
    dist = ROOT / 'dist'
    dist.mkdir(parents=True, exist_ok=True)
    name = output_name or f'BakeBot-{version or ts}.zip'
    out_path = dist / name

    with zipfile.ZipFile(out_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        # Include curated dirs
        for d in INCLUDE_DIRS:
            p = ROOT / d
            if p.exists():
                add_path(z, ROOT, p)
        # Include curated files
        for f in INCLUDE_FILES:
            p = ROOT / f
            if p.exists():
                add_path(z, ROOT, p)

    return out_path


def sha256sum(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description='Build BakeBot ZIP release artifact')
    ap.add_argument('-v', '--version', default='', help='Version tag (e.g., v1.0.0)')
    ap.add_argument('-o', '--output-name', default='', help='Custom output zip file name')
    args = ap.parse_args(argv)

    out = build_zip(args.version, args.output_name or None)
    digest = sha256sum(out)
    print(f'Created: {out} ({out.stat().st_size} bytes)')
    print(f'SHA256:  {digest}')
    print('\nSuggested Release Attachment:')
    print(f'  {out}')


if __name__ == '__main__':
    sys.exit(main())
