#!/usr/bin/env python3
"""Check source bytes and audit metadata; this does not verify any theorem."""
from pathlib import Path
import csv,hashlib,json

ROOT=Path(__file__).resolve().parent.parent
V=ROOT/'verification'
def get(name):return json.loads((V/name).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)

lemmas=get('LEMMAS.json'); claims=get('CLAIMS.json'); inputs=get('INPUTS.json')
graph=get('dependency_graph.json'); included=get('INCLUDED_SOURCE_MAP.json'); baseline=get('BASELINE.json')
require(len(lemmas)==23,'Expected 23 original drafts')
require({x['id'] for x in lemmas}=={f'L{i:03}' for i in range(1,24)},'Original draft IDs incomplete')
lookup={}
for x in included:
    p=ROOT/x['package_path']
    require(p.is_file(),f"Missing included source: {x['package_path']}")
    require(digest(p)==x['sha256'],f"Source bytes differ: {x['package_path']}")
    lookup[x['original_path']]=p
archive={x['path']:x for x in baseline['archive_entries']}
require(len(archive)==203,'Original archive inventory count differs')
report=(ROOT/'RECCVS_Stage0_Dependency_Audit_2026-10-11.md').read_text()
for x in baseline['inputs']:
    require(x['sha256'] in report,'Human-readable baseline hash differs from JSON')
require(f"{len(claims)}项核心结论" in report,'Human-readable claim count differs')
require(f"{len(inputs)}个输入节点" in report,'Human-readable input count differs')
require(f"{len(graph['proof_edges'])}条直接依赖边" in report,'Human-readable edge count differs')
for x in included:
    if x['original_path'].startswith('RECCVS/'):
        require(x['original_path'] in archive,f"Source absent from frozen archive: {x['original_path']}")
        require(x['sha256']==archive[x['original_path']]['sha256'],f"Source hash differs from baseline: {x['original_path']}")
    else:
        require(x['original_path'].startswith('attachment:'),'Unknown source origin')
        name=x['original_path'].split(':',1)[1]
        candidates=[a for a in baseline['inputs'] if a['filename']==name]
        require(len(candidates)==1 and candidates[0]['sha256']==x['sha256'],'Attachment hash differs')
for x in lemmas:
    require(digest(ROOT/x['proposed_path'])==x['sha256'],f"Draft hash differs: {x['id']}")
    require(x['original_path'] in lookup,'Draft has no included-source map')

ids=[x['id'] for x in inputs+claims]
require(len(ids)==len(set(ids)),'Duplicate audit node ID')
known=set(ids)
require({x['id'] for x in graph['nodes']}==known,'Graph and catalog node sets differ')
for x in inputs+claims:
    require(all(d in known for d in x['dependencies']),f"Undefined dependency in {x['id']}")
for x in claims:
    require(x['lemma'] in {v['id'] for v in lemmas},'Unknown draft for claim')
    for s in [x['source']]+x.get('additional_sources',[]):
        p=lookup[s['original_path']]; lines=p.read_text().splitlines()
        require(digest(p)==s['sha256'],'Claim source hash differs')
        require(1<=s['start_line']<=s['end_line']<=len(lines),'Claim source line range invalid')
        require(lines[s['start_line']-1]==s['heading'],'Claim source heading differs')
for x in inputs:
    for s in x['sources']:
        require(s['original_path'] in lookup,f"Input source missing from package: {s['original_path']}")
        require(digest(lookup[s['original_path']])==s['sha256'],'Input source hash differs')

expected={(d,x['id']) for x in inputs+claims for d in x['dependencies']}
actual={(e['source'],e['target']) for e in graph['proof_edges']}
require(expected==actual,'Graph edges and catalog dependencies differ')
require(len(actual)==len(graph['proof_edges']),'Duplicate direct edge')
adj={x:[] for x in known}; indegree={x:0 for x in known}
for a,b in actual:
    adj[a].append(b);indegree[b]+=1
queue=sorted(x for x in known if indegree[x]==0); order=[]
while queue:
    x=queue.pop(0);order.append(x)
    for y in sorted(adj[x]):
        indegree[y]-=1
        if indegree[y]==0:queue.append(y);queue.sort()
require(len(order)==len(known),'Direct dependency graph contains a cycle')
for e in graph['application_or_explanatory_edges']:
    require(e['source'] in known and e['target'] in known,'Application edge ID undefined')

csvrows=list(csv.DictReader((V/'SOURCE_MAP.csv').open()))
require(len(csvrows)==23,'Source CSV count differs')
for r in csvrows:
    match=[x for x in lemmas if x['id']==r['id']]
    require(len(match)==1 and all(r[k]==match[0][k] for k in r),'Source CSV differs from lemma JSON')

package_checksums=V/'PACKAGE_FILES_SHA256.json'
if package_checksums.exists():
    for x in json.loads(package_checksums.read_text()):
        p=ROOT/x['path']; require(p.is_file() and digest(p)==x['sha256'],f"Package file differs: {x['path']}")

result={
 'scope':'SOURCE_BYTES_AND_AUDIT_METADATA_ONLY',
 'original_drafts':len(lemmas),'claim_records':len(claims),'input_records':len(inputs),
 'included_source_files':len(included),'frozen_archive_entries':len(archive),
 'direct_edges':len(actual),'undefined_ids':[], 'directed_cycles':[],
 'topological_order':order,
 'mathematical_truth_verified':False,'historical_math_certificates_reexecuted':False,
 'finite_amplitude_root_certified':False,'pde_evolution_performed':False,
 'status':'AUDIT_METADATA_CONSISTENT'
}
(V/'CHECK_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='topological_order'},ensure_ascii=False,indent=2))
