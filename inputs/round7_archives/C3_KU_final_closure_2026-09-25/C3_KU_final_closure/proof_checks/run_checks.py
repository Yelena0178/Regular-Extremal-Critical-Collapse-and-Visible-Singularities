from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
checks=['jacobian_check.py','symbolic_checks.py','endpoint_jet_check.py','stability_check.py','interval_checks.py']
lines=[]
for name in checks:
 result=subprocess.run([sys.executable,str(root/'proof_checks'/name)],capture_output=True,text=True)
 lines.append(name+'\n'+result.stdout+result.stderr)
 if result.returncode:
  print('\n'.join(lines));raise SystemExit(result.returncode)
(root/'data/check_log.txt').write_text('\n'.join(lines))
print('\n'.join(lines))
