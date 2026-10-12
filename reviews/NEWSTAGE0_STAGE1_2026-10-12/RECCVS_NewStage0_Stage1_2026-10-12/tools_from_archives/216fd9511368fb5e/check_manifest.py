from pathlib import Path
import hashlib
import json
import sys

base=Path(sys.argv[1]); manifest=json.loads((base/'MANIFEST.json').read_text())
for item in manifest['files']:
    path=base/item['path']
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:
        raise SystemExit('Content mismatch: '+item['path'])
print(json.dumps({'status':'STAGE3_MANIFEST_PASS','files':len(manifest['files'])}))
