"""Verify current declared bytes against FILE_MANIFEST.json (not mathematics)."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'FILE_MANIFEST.json').read_text())
for item in manifest['files']:
    path = root / item['path']
    if not path.is_file():
        raise SystemExit('Missing file: ' + item['path'])
    if path.stat().st_size != item['size_bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise SystemExit('Changed file: ' + item['path'])
print('PASS:', len(manifest['files']), 'files match the current byte manifest')
print('This verifies bytes only; it does not certify the mathematical claims.')
