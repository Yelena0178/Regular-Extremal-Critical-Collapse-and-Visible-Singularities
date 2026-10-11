#!/usr/bin/env python3
"""Verify frozen bytes and audit metadata only, never mathematical validity."""
from pathlib import Path
from collections import Counter
import hashlib,json

ROOT=Path(__file__).resolve().parent.parent
V=ROOT/'verification'
def get(n):return json.loads((V/n).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,msg):
 if not ok:raise ValueError(msg)
claims=get('CLAIMS_v2.json');inputs=get('INPUTS_v2.json');lemmas=get('LEMMAS_v2.json')
graph=get('dependency_graph_v2.json');included=get('INCLUDED_SOURCE_MAP.json')
issues=get('ISSUES.json');assumptions=get('ASSUMPTIONS_v2.json');baseline=get('BASELINE.json')
nodes=inputs+claims;ids=[x['id'] for x in nodes];known=set(ids)
check(len(known)==len(ids),'Duplicate ID')
check({x['id'] for x in lemmas}=={f'L{n:03}' for n in range(1,24)},'Original draft coverage')
check({x['lemma'] for x in claims}=={x['id'] for x in lemmas},'Claim coverage')
lookup={}
archive={x['path']:x for x in baseline['archive_entries']}
for x in included:
 p=ROOT/x['package_path'];check(p.is_file(),'Missing source '+str(p))
 check(digest(p)==x['sha256'],'Modified source '+str(p));lookup[x['original_path']]=p
 if x['original_path'].startswith('RECCVS/'):
  check(archive[x['original_path']]['sha256']==x['sha256'],'Baseline hash mismatch')
for x in lemmas:check(digest(ROOT/x['proposed_path'])==x['sha256'],'Modified draft '+x['id'])
def verifyspan(s):
 p=lookup[s['original_path']];check(digest(p)==s['sha256'],'Source SHA differs')
 lines=p.read_text().splitlines();a=s['start_line'];b=s['end_line']
 check(1<=a<=b<=len(lines),'Invalid span '+s['original_path'])
 check(lines[a-1]==s['heading'],'Span start differs')
for x in claims:
 for s in [x['source']]+x.get('additional_sources',[]):verifyspan(s)
for x in inputs:
 for s in x['sources']:check(digest(lookup[s['original_path']])==s['sha256'],'Input source mismatch')
 for s in x['source_spans']:verifyspan(s)
for x in issues:
 for s in x['evidence']:verifyspan(s)

expected=set()
for x in nodes:
 for d in x['dependencies']:
  check(d in known,'Undefined dependency '+d)
  expected.add((d,x['id'],'common_prerequisite','共同前提'))
 if x.get('case_rules'):
  check(x.get('case_coverage'),'Case coverage justification absent')
  check(len(x['case_rules'])>=2,'Insufficient branches')
  for br in x['case_rules']:
   check(br['condition'] and br['dependencies'],'Branch selector/deps absent')
   for d in br['dependencies']:
    check(d in known,'Undefined case dependency '+d)
    expected.add((d,x['id'],'case_prerequisite',br['condition']))
actual={(e['source'],e['target'],e['kind'],e['condition']) for e in graph['proof_and_condition_edges']}
check(expected==actual,'Edges/catalog differ')
check(len(actual)==len(graph['proof_and_condition_edges']),'Duplicate edge')
check({x['id'] for x in graph['nodes']}==known,'Graph node set differs')
adj={x:[] for x in known};indegree={x:0 for x in known}
for a,b,_,_ in actual:adj[a].append(b);indegree[b]+=1
queue=sorted(x for x in known if not indegree[x]);order=[]
while queue:
 x=queue.pop(0);order.append(x)
 for y in sorted(adj[x]):
  indegree[y]-=1
  if not indegree[y]:queue.append(y);queue.sort()
check(len(order)==len(known),'Registered dependency cycle')
for e in graph['application_or_explanatory_edges']:
 check(e['source'] in known and e['target'] in known,'Unknown instance edge')
for x in assumptions:
 check(x['owner'] in known,'Unknown assumption owner')
 check(x['discharged_for_specific_seed'] in [None,False],'Incorrect automatic discharge')
for x in nodes:check(any(a['owner']==x['id'] for a in assumptions),'Assumption inventory missing '+x['id'])
# The following checks enforce corrected REGISTRATION structure, not its truth.
ci={x['id']:x for x in claims};ii={x['id']:x for x in inputs}
check('M_s(z_c)=c_s' in ii['PERIODIC_PROFILE']['statement'],'Moment coordinate condition absent')
check('FLIFT' not in ii['FENDPOINT']['dependencies'],'Linear module uses later root')
check('FSPHERE' not in ii['FLIFT']['dependencies'],'Root uses later sphere')
check('L015.OUTER' not in ci['L015.LIFETIME']['dependencies'],'Lifetime branches flattened')
check('L018.SIGN' not in ci['L018.ROBIN']['dependencies'],'Robin uses DN theorem')
check(ci['L022.TAIL']['dependencies']==['REPAIR_BUDGET'],'Tail overdependency persists')
check('REPAIR_TO_STRONG' in ci['L023.SMOOTH']['dependencies'],'Strong topology gate absent')
def ancestors(id):
 result=set();todo=[id]
 while todo:
  n=todo.pop()
  for a,b,_,_ in actual:
   if b==n and a not in result:result.add(a);todo.append(a)
 return result
check('FLIFT' not in ancestors('L023.MGEOM'),'Geometry gate inherits root')
check('E021' in ci['L021.FIX']['dependencies'],'Cutoff coefficient evidence absent')
check('NU_NEG' not in ancestors('L003.TIDAL'),'Tidal identity inherits ν sign')
check('VIS' not in ancestors('L010.TRANSPORT'),'Transport inherits global visibility')
count=Counter(x['severity'] for x in issues)
check(dict(count)=={'严重':2,'中等':7,'轻微':2},'Issue count mismatch')
old=get('prior_stage0/CLAIMS.json')
check({x['id'] for x in old}.issubset({x['id'] for x in claims}),'Old claim silently dropped')
report=(ROOT/'RECCVS_Stage0_Self_Review_2026-10-11.md').read_text()
for x in issues:check(x['id'] in report,'Issue absent from report')
for x in lemmas:check(x['id'] in report,'Draft absent from report')
checks=V/'PACKAGE_FILES_SHA256.json'
if checks.exists():
 for x in json.loads(checks.read_text()):
  if x['path']=='verification/CHECK_RESULTS_v2.json':continue
  check(digest(ROOT/x['path'])==x['sha256'],'Package checksum differs '+x['path'])
result=dict(status='SOURCE_AND_REGISTRATION_CHECKS_PASS',scope='FROZEN_BYTES_AND_AUDIT_METADATA_ONLY',drafts=23,claims=len(claims),inputs=len(inputs),source_files=len(included),issues=dict(count),assumption_records=len(assumptions),edges=len(actual),case_joins=[x['id'] for x in claims if x.get('case_rules')],undefined_ids=[],registered_cycles=[],topological_order=order,all_original_claims_retained=True,mathematical_truth_verified=False,case_exhaustiveness_mathematically_proved_by_checker=False,historical_math_certificates_reexecuted=False,finite_amplitude_root_certified=False,pde_evolution_performed=False)
write=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
(V/'CHECK_RESULTS_v2.json').write_text(write)
print(json.dumps({k:v for k,v in result.items() if k!='topological_order'},ensure_ascii=False,indent=2))
