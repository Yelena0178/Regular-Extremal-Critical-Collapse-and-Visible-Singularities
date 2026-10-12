#!/usr/bin/env python3
"""Verify immutable package bytes only, never mathematical correctness.
数学结论：GPT 主张，未经外部独立审查。
"""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'verification/PACKAGE_MANIFEST.json').read_text())
bad=[]
for row in manifest['files']:
    p=ROOT/row['path']
    if not p.is_file():bad.append({'path':row['path'],'reason':'missing'});continue
    b=p.read_bytes()
    if len(b)!=row['size'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append({'path':row['path'],'reason':'bytes differ'})
report={'scope':'IMMUTABLE_PACKAGE_BYTES_ONLY','files_checked':len(manifest['files']),'status':'PASS' if not bad else 'FAIL','issues':bad,'excluded_runtime_outputs':manifest['excluded_runtime_outputs'],'mathematical_label':'GPT 主张，未经外部独立审查','mathematical_correctness_certified':False}
(ROOT/'verification/PACKAGE_VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
if bad:raise SystemExit(1)
