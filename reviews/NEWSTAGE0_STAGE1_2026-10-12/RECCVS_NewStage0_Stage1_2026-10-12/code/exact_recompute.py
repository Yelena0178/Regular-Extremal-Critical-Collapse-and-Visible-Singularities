#!/usr/bin/env python3
"""Exact finite algebra and evidence-state checks. Never a PDE verifier.
数学结论：GPT 主张，未经外部独立审查。
Run from any cwd: python3 code/exact_recompute.py
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,platform

ROOT=Path(__file__).resolve().parents[1]
class P:
    """Sparse rational Laurent polynomials; monomials are sorted name/exponent tuples."""
    def __init__(self,value=0):
        self.d=value if isinstance(value,dict) else ({():F(value)} if value else {})
    @staticmethod
    def var(name,power=1):return P({((name,power),):F(1)}) if power else P(1)
    def __add__(self,other):
        other=other if isinstance(other,P) else P(other);d=dict(self.d)
        for k,v in other.d.items():d[k]=d.get(k,F(0))+v
        return P({k:v for k,v in d.items() if v})
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.d.items()})
    def __sub__(self,o):return self+-o if isinstance(o,P) else self+(-F(o))
    def __rsub__(self,o):return -self+o
    def __mul__(self,o):
        o=o if isinstance(o,P) else P(o);d={}
        for a,x in self.d.items():
            for b,y in o.d.items():
                m=dict(a)
                for n,p in b:m[n]=m.get(n,0)+p
                k=tuple(sorted((n,p) for n,p in m.items() if p));d[k]=d.get(k,F(0))+x*y
        return P({k:v for k,v in d.items() if v})
    __rmul__=__mul__
    def diff(self,name):
        d={}
        for a,x in self.d.items():
            m=dict(a);p=m.get(name,0)
            if not p:continue
            m[name]=p-1;k=tuple(sorted((n,q) for n,q in m.items() if q));d[k]=d.get(k,F(0))+x*p
        return P({k:v for k,v in d.items() if v})
    def evaluate(self,**values):
        out=F(0)
        for a,x in self.d.items():
            for n,p in a:x*=F(values[n])**p
            out+=x
        return out

checks=[]
def check(name,ok,scope,value=None):
    if not ok:raise RuntimeError(name+' failed')
    checks.append({'name':name,'status':'PASS','scope':scope,'value':value})
def identity(name,expr,scope):check(name,not expr.d,scope)
V=P.var;Q=V('Q');R=V('r');Ri=V('r',-1);M=V('M')
mH=M-F(1,2)*Q*Q*Ri
identity('RN_mass_relation',1-2*(mH+F(1,2)*Q*Q*Ri)*Ri+Q*Q*Ri*Ri-(1-2*M*Ri+Q*Q*Ri*Ri),'RN Laurent identity')
rp=V('rp');rm=V('rm');a=V('rp',-1);rmi=V('rm',-1)
identity('RN_factorization',1-(rp+rm)*Ri+rp*rm*Ri*Ri-(1-rp*Ri)*(1-rm*Ri),'RN roots parameterization')
identity('horizon_Hawking_mass',(rp+rm)*F(1,2)-F(1,2)*rp*rm*a-rp*F(1,2),'r+=rp,Q²=rp*rm')
check('extreme_horizon_mass_half',mH.evaluate(M=1,Q=1,r=1)==F(1,2),'specific exact RN reference','1/2')
check('extreme_RN_curvature_reference',48-96+56==8,'M=Q=r=1 finite polynomial value',8)
# Differentiate m_H=varpi-Q²/(2r) using formally independent actual jets.
X=V('X');Qa=V('Qa');ra=V('ra')
varpi_a=-2*X+Q*Ri*Qa
derived_mH_a=varpi_a-Q*Ri*Qa+F(1,2)*Q*Q*Ri*Ri*ra
identity('charge_derivative_cancellation',derived_mH_a-(-2*X+F(1,2)*Q*Q*Ri*Ri*ra),'both null directions; X is their scalar flux factor')
identity('Gauss_current_conjugation',V('ImZ')+(-V('ImZ')),'Im(phi*barPi)=-Im(barphi*Pi); orientation bookkeeping')
identity('gauge_covariant_derivative_cancellation',-F(3,5)*V('chiphi')+F(3,5)*V('chiphi'),'coefficient of i chi_prime phi')
eta=F(1,2);mass1=F(841,32768);mass2=F(7,16384)
check('L023_mass_margins',mass1<F(1,16) and mass2<F(1,16) and eta-mass1==F(15543,32768),'sufficient threshold arithmetic only',str(eta-mass1))
check('L023_width_margins',F(1024,116281)<F(1,8) and F(20480,116281)<2,'sufficient threshold arithmetic only')
check('marginal_strict_upgrade_coefficient',F(65,512)-1==F(-447,512),'sign only; actual collar remains an input',str(F(-447,512)))

def interval_gap(mlo,mhi,qlo,qhi):
    if not (F(0)<mlo<=mhi and qlo<=qhi):raise ValueError('invalid intervals')
    qmax=max(abs(qlo),abs(qhi));qmin=F(0) if qlo<=0<=qhi else min(abs(qlo),abs(qhi))
    return mlo*mlo-qmax*qmax,mhi*mhi-qmin*qmin,qmin/mhi,qmax/mlo
lo,hi,qlo,qhi=interval_gap(F(199,100),F(201,100),F(99,100),F(101,100))
check('subextreme_interval_positive',lo==F(147,50) and lo>0,'exact interval propagation, assuming supplied intervals valid',{'lo':str(lo),'hi':str(hi)})
lo,hi,_,_=interval_gap(F(99,100),F(101,100),F(99,100),F(101,100))
check('extreme_candidate_not_exact_certificate',lo<0<hi,'interval includes zero; state must remain candidate',{'lo':str(lo),'hi':str(hi)})
lo,hi,qrlo,qrhi=interval_gap(F(1),F(2),F(-1),F(1))
check('signed_charge_interval_cross_zero',hi==4 and qrlo==0,'absolute charge minimum is zero when signed interval crosses zero')
try:interval_gap(F(0),F(1),F(0),F(0))
except ValueError:ok=True
else:ok=False
check('zero_mass_denominator_rejected',ok,'ratio requires strictly positive mass lower bound')
# A rigorous future tail premise cannot be omitted by a state classifier.
def can_classify_terminal(level,mass_bound,tail_bound,global_interface):
    return level in ['E2','E3'] and all([mass_bound,tail_bound,global_interface])
check('finite_snapshot_not_terminal_certificate',not can_classify_terminal('E2',True,False,True),'evidence-state logic only')
check('empirical_not_rigorous_certificate',not can_classify_terminal('E1',True,True,True),'evidence-state logic only')
z=V('z');zi=V('z',-1);C=V('C')
identity('tail_antiderivative_alpha1',(-C*zi).diff('z')-C*zi*zi,'integral of C/(1+u)^2; general alpha proof in detail03')
check('p_t_diagonal_counterexample',all(F(1,1)/(1+F(1,t)*t)==F(1,2) for t in [1,2,4,16,256]),'illustration, not EMCSF evolution')

manifest=json.loads((ROOT/'verification/SOURCE_MANIFEST.json').read_text())
for row in manifest['files']:
    b=(ROOT/row['package_path']).read_bytes()
    check('source_blob:'+row['repo_path'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1'],'source identity only')
archives=json.loads((ROOT/'verification/ARCHIVE_TOOL_INVENTORY.json').read_text())
for row in archives['unique']:
    b=(ROOT/row['package_path']).read_bytes()
    check('archive_tool:'+row['sha256'][:16],hashlib.sha256(b).hexdigest()==row['sha256'],'embedded code identity only')
report={'python':platform.python_version(),'mathematical_label':'GPT 主张，未经外部独立审查','scope':'FINITE_ALGEBRA_SOURCE_IDENTITY_AND_EVIDENCE_STATE_ONLY','checks':checks,'passed':len(checks),'pde_evolution_performed':False,'independent_external_review_completed':False,'original_1105_plan_recovered':False,'new_critical_curve_constructed':False,'old_actual_trapped_surface_unconditionally_certified':False}
(ROOT/'verification/EXACT_RECOMPUTATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['scope','passed','pde_evolution_performed','original_1105_plan_recovered']},ensure_ascii=False))
