"""Verify every listed delivery file against its exact SHA-256."""
from pathlib import Path
import hashlib
import json
import sys

root=Path(sys.argv[1]).resolve()
data=json.loads((root/'MANIFEST.json').read_text())
for item in data['files']:
    path=(root/item['path']).resolve()
    if not path.is_relative_to(root):raise SystemExit('Unsafe manifest path')
    raw=path.read_bytes()
    if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:
        raise SystemExit('MANIFEST MISMATCH: '+item['path'])
print(json.dumps(dict(status='DELIVERY_HASHES_PASS',files=len(data['files']),full_root_certified=False)))
