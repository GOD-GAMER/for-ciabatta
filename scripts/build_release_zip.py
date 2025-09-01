#!/usr/bin/env python3
"""
Build a streamer-ready ZIP release of BakeBot.

Usage:
  python scripts/build_release_zip.py -v v1.0.0
  python scripts/build_release_zip.py --version v1.0.0 --output-name BakeBot-Streamer-v1.0.0.zip

Creates a clean, streamer-friendly package with setup guides and excludes development files.
"""

import argparse
import hashlib
import os
from pathlib import Path
import sys
import time
import zipfile
import fnmatch
import shutil

ROOT = Path(__file__).resolve().parents[1]

INCLUDE_DIRS = [
    'bot',
    'install', 
    'docs',
    'scripts',  # Include for version management
]

INCLUDE_FILES = [
    'requirements.txt',
    'README.md',
    'STREAMER_README.md',  # Streamer-specific guide
]

# Patterns to exclude (directories or files)
EXCLUDE_DIRS = [
    '.git', '.vs', '.vscode', '__pycache__',
    'node_modules', 'env', 'venv', '.venv',
    'logs', 'dist', 'build', '.cache', '.pytest_cache',
    'sounds',  # Don't include sounds folder (streamer can add their own)
]

EXCLUDE_GLOBS = [
    '.env*',        # All env files
    '*.pyc', '*.pyo',
    '*.sqlite3', '*.db', 'bot_data.sqlite3',  # No existing data
    '*.log',
    '.gitignore', '.gitkeep', '.githooks',    # Git-specific
    'automod.py',   # AutoMod was reverted, don't include
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
    name = output_name or f'BakeBot-Streamer-{version or ts}.zip'
    out_path = dist / name

    print(f"Building streamer package: {name}")
    print("Including directories:", INCLUDE_DIRS)
    print("Including files:", INCLUDE_FILES)

    with zipfile.ZipFile(out_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        # Add a streamer-friendly folder structure comment
        z.comment = b"BakeBot - Twitch Chat Bot for Streamers. Extract and run 'python -m bot.gui' to start!"
        
        # Include curated dirs
        for d in INCLUDE_DIRS:
            p = ROOT / d
            if p.exists():
                print(f"  Adding directory: {d}/")
                add_path(z, ROOT, p)
        
        # Include curated files
        for f in INCLUDE_FILES:
            p = ROOT / f
            if p.exists():
                print(f"  Adding file: {f}")
                add_path(z, ROOT, p)

        # Create empty directories for user data
        z.writestr('sounds/.gitkeep', '# Add your custom sound files here\n')
        
        # Add version info to the zip
        if version:
            z.writestr('VERSION.txt', f'BakeBot {version}\nBuilt: {time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())}\n')

    return out_path


def sha256sum(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description='Build BakeBot streamer-ready ZIP package')
    ap.add_argument('-v', '--version', default='', help='Version tag (e.g., v2.1.0)')
    ap.add_argument('-o', '--output-name', default='', help='Custom output zip file name')
    args = ap.parse_args(argv)

    # Get version from bot/__init__.py if not provided
    if not args.version:
        try:
            init_file = ROOT / 'bot' / '__init__.py'
            if init_file.exists():
                with open(init_file, 'r') as f:
                    for line in f:
                        if line.startswith("__version__ = "):
                            args.version = line.split("'")[1]
                            break
        except Exception:
            pass

    out = build_zip(args.version, args.output_name or None)
    digest = sha256sum(out)
    
    print(f'\n? Streamer package created successfully!')
    print(f'?? File: {out}')
    print(f'?? Size: {out.stat().st_size:,} bytes')
    print(f'?? SHA256: {digest}')
    
    print(f'\n?? Ready for distribution to streamers!')
    print(f'?? Instructions for streamers are in STREAMER_README.md')
    print(f'?? Streamers just need: extract ? pip install -r requirements.txt ? python -m bot.gui')


if __name__ == '__main__':
    sys.exit(main())
