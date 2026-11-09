import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,'computations')
from shape_probe import ShapeShell,SRC,hashes
from probe_fixed_charge_amplitude import FixedChargeAmplitudeShell
import numpy as np
from fractions import Fraction
record=json.loads((SRC/'CHARGE_SHELL_INITIAL_CERTIFICATE_2026-10-22.json').read_text())
assert hashlib.sha256((SRC/'certify_charge_shell_initial.py').read_bytes()).hexdigest()==record['source_sha256']
assert Fraction(record['charge_upper'])<6
base=FixedChargeAmplitudeShell('3/2',15)
checks=[]
for eta in [-.5,0,.5]:
 d=ShapeShell(eta); errors=[]; phase_errors=[]
 for r in np.linspace(6.01,13.99,101):
  phi,g,c=d.free(r); a,ap=d.envelope(r); w=d.frequency(r)
  qrhs,frhs,_=d.constraint_rhs(r,[2,.7,0])
  errors.extend([abs(qrhs-.6*r*r*np.imag(phi*np.conj(c))),abs(frhs-((1-.7)/r-4/r**3-r*.7*(abs(g)**2+abs(c)**2))),abs(a*a*w-base.envelope(r)[0]**2/15)])
  h=1e-4; phase_errors.append(abs((d.phase(r+h)-d.phase(r-h))/(2*h)+.8*w))
 assert max(errors)<1e-12 and max(phase_errors)<1e-9
 if eta==0:
  assert max(abs(np.array(d.free(r))-np.array(base.free(r)))).max()<1e-12
  assert abs(d.ADM_mass-base.ADM_mass)<1e-9
 checks.append(dict(eta=eta,max_algebra_error=max(errors),max_phase_derivative_error=max(phase_errors),ADM_mass=d.ADM_mass,ADM_charge=d.ADM_charge,min_sampled_f=d.summary()['minimum_sampled_initial_f']))
assert Fraction(8417,125)*3<203
out=dict(checks=checks,inherited_certificate_source_hash_matched=True,source_sha256=hashes(),scope='finite implementation checks and inherited certificate integrity, not PDE certification',passed=True)
Path('results/SHAPE_INITIAL_CHECKS.json').write_text(json.dumps(out,indent=2))
print(json.dumps(checks,indent=2))
