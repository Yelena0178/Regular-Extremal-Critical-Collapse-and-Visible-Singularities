"""Check audit packaging, immutable source hashes and exact conditional arithmetic.

This is not a theorem checker, PDE verifier or nonlinear root certificate.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
def read(relative): return json.loads((ROOT/relative).read_text())

matrix=read('audit/ASSUMPTION_MATRIX.json')['rows']
assert [r['id'] for r in matrix]==[f'A{i:02d}' for i in range(1,46)]
assert all(r['verdict'] in {'通过','需修正','暂不可调用'} for r in matrix)
issues=read('audit/ISSUES.json')
assert [i['id'] for i in issues]==[f'S1-{i:02d}' for i in range(1,10)]
assert all(i['severity'] in {'严重','中等','轻微'} for i in issues)

manifest=read('SOURCE_MANIFEST.json')['sources']
for item in manifest:
    data=(ROOT/item['archived_path']).read_bytes()
    assert len(data)==item['bytes']
    assert hashlib.sha256(data).hexdigest()==item['sha256']
    original=Path(item['original_path'])
    if original.is_file(): assert original.read_bytes()==data

expected=read('verification/EXACT_ARITHMETIC.json')
actual=json.loads(subprocess.check_output([sys.executable,str(ROOT/'sources/experiments/check_first_period_thresholds.py')], text=True))
assert actual==expected==read('sources/experiments/first_period_threshold_certificate.json')
assert actual['finite_amplitude_root_certified'] is False

nodes={n['id']:n for n in read('audit/DEPENDENCY_REFINEMENT.json')['nodes']}
assert nodes['L023.MGEOM']['root_required'] is False
assert 'FLIFT' not in nodes['L023.MGEOM']['dependencies']
visited=set(); stack=set()
def walk(node):
    if node not in nodes or node in visited: return
    assert node not in stack, 'explicit suggested dependency cycle'
    stack.add(node)
    for parent in nodes[node]['dependencies']: walk(parent)
    stack.remove(node); visited.add(node)
for node in nodes: walk(node)

result=dict(
    checks_passed=True,
    assumption_count=len(matrix),
    verdict_counts=dict(Counter(r['verdict'] for r in matrix)),
    issue_count=len(issues),
    severity_counts=dict(Counter(i['severity'] for i in issues)),
    immutable_sources_count=len(manifest),
    source_hashes_and_available_originals_match=True,
    exact_arithmetic_matches_archived_certificate=True,
    explicit_suggested_dependency_cycles=0,
    geometric_threshold_root_separation_preserved=True,
    nonlinear_root_certified=False,
    pde_evolution_performed=False,
    full_proof_transfer_and_continuation_certified=False,
    original_proofs_modified=False,
)
(ROOT/'verification/CHECK_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
