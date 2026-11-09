"""SHAPE01 bounded experiment; floating numerics, no PDE certificate."""
from pathlib import Path
import sys, json, argparse, hashlib, platform
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source/goal-a/research/goal_a'
sys.path.insert(0,str(SRC))
import numpy as np
import scipy
from charge_preserving_shell import ShellParameters, ChargePreservingShell
from probe_fixed_charge_amplitude import LocatedBudget
from screen_charge_preserving_shell import Diagnostics
from centered_cauchy_diamond import axis_state,evolve_centered

class ShapeShell(ChargePreservingShell):
    def __init__(self,eta,time=15):
        if not -.5<=eta<=.5: raise ValueError('eta outside proved interval')
        self.eta=eta
        super().__init__(ShellParameters(amplitude=.6,frequency=1/15,direction=.8),exterior_width=2*time+20)
    def envelope(self,r):
        a,ap=super().envelope(r)
        factor=np.exp(self.eta*(r-10)/4)
        return a*factor,(ap+self.eta*a/4)*factor
    def frequency(self,r): return np.exp(-2*self.eta*(r-10)/4)/15
    def phase(self,r):
        z=(r-10)/4
        return -.8*4/15*(z if self.eta==0 else -np.expm1(-2*self.eta*z)/(2*self.eta))
    def free(self,r):
        a,ap=self.envelope(r)
        if a==0 and ap==0: return 0j,0j,0j
        w=self.frequency(r); phase=np.exp(1j*self.phase(r))
        return phase*a,phase*(ap-.8j*w*a),phase*(-.8*(ap+a/r)-1j*w*a)
    def constraint_rhs(self,r,y):
        Q,f,_=y
        if f<=0 or not np.isfinite(y).all(): raise ArithmeticError('constraint f lost')
        a,ap=self.envelope(r); w=self.frequency(r)
        S=ap*ap+.64*(ap+a/r)**2+1.64*w*w*a*a
        return [.6*w*r*r*a*a,(1-f)/r-Q*Q/r**3-r*f*S,1/np.sqrt(f)]
    def summary(self):
        out=super().summary()
        out.update(eta=self.eta,phase_direction=-.8,profile='a=.6*b(z)*exp(eta*z), omega=exp(-2*eta*z)/15',analytic_proof='proofs/SHAPE01.md',uniform_analytic_f_lower='(3/7)*exp(-203)',analytic_charge_enclosure_arithmetic_conditional=True)
        return out

def hashes():
    names=['charge_preserving_shell.py','probe_fixed_charge_amplitude.py','probe_split_focusing_budget.py','screen_charge_preserving_shell.py','centered_cauchy_diamond.py','charged_cauchy_diamond.py','charged_lobatto.py']
    paths=[Path(__file__),*(SRC/n for n in names)]
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def run(eta,steps,output,scout=None):
    data=ShapeShell(eta)
    selection=None
    if scout:
        old=json.loads(scout.read_text())
        assert old['initial_data']['eta']==eta and old['source_sha256']==hashes()
        event=old.get('first_negative_sample') or old['worst']
        u=event['time']-event['x']; h=30/old['requested_steps']
        rays=[u-h,u,u+h]
        observer=LocatedBudget(data,15,rays)
        selection=dict(primary_u=u,rays=rays,scout=str(scout),scout_sha256=hashlib.sha256(scout.read_bytes()).hexdigest())
    else: observer=Diagnostics(data,15)
    result=evolve_centered(data.state_at_proper,axis_state(.5,0j),0j,data.proper_max,15,steps,observer=observer)
    for k in ['x','state','initial_state']: result.pop(k,None)
    result.update(initial_data=data.summary(),diagnostics=observer.report(),requested_time=15,requested_steps=steps,ray_selection=selection,source_sha256=hashes(),environment=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()),finite_PDE_error_certified=False,full_future_classified=False,goal_A_proved=False)
    if scout and steps==old['requested_steps']:
        assert result.get('first_negative_sample')==old.get('first_negative_sample') and result['worst']==old['worst']
        result['observer_regression_passed']=True
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result.get(k) for k in ['completed','failed_time','first_negative_sample','worst']},indent=2),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--eta',type=float,choices=[-.5,.5],required=True);p.add_argument('--steps',type=int,choices=[512,1024],required=True);p.add_argument('--scout',type=Path);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists(): raise FileExistsError('preserve existing evidence')
    run(a.eta,a.steps,a.output,a.scout)
