#!/usr/bin/env python3
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
init = ROOT / 'bot' / '__init__.py'

pat = re.compile(r"__version__\s*=\s*'([^']+)'")
text = init.read_text(encoding='utf-8')
m = pat.search(text)
if not m:
    print('No __version__ found', file=sys.stderr)
    sys.exit(1)

ver = m.group(1)
parts = ver.split('.')
# normalize to 3 parts
while len(parts) < 3:
    parts.append('0')
major, minor, patch = map(int, parts[:3])
# increment patch
patch += 1
# rollover if any digit hits 9 -> move over a decimal and start back at 1
if patch > 9:
    patch = 1
    minor += 1
    if minor > 9:
        minor = 1
        major += 1
new_ver = f"{major}.{minor}.{patch}"
text = pat.sub(f"__version__ = '{new_ver}'", text)
init.write_text(text, encoding='utf-8')
print(new_ver)
