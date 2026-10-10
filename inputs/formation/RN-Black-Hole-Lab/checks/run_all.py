from pathlib import Path
import subprocess, sys, json
base=Path(__file__).resolve().parent
scripts=sorted(p for p in base.rglob('*.py') if p.name!='run_all.py')
results=[]
for p in scripts:
    r=subprocess.run([sys.executable,str(p)],cwd=p.parent,text=True,capture_output=True)
    results.append({'script':str(p.relative_to(base)), 'exit_code':r.returncode, 'stdout':r.stdout,'stderr':r.stderr})
    print(str(p.relative_to(base))+': '+('PASS' if r.returncode==0 else 'FAIL'),flush=True)
report={'scope':'execution of finite algebra checks only; no independent analytic verification','results':results}
(base/'PACKAGING_RUN.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
sys.exit(0 if all(x['exit_code']==0 for x in results) else 1)
