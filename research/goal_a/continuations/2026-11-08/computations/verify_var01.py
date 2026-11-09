"""One baseline tangent ODE; finite differences verify derivatives, not candidates."""
import sys,json,hashlib,platform
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp
from shape_probe import ShapeShell,ROOT

class DirectionShell(ShapeShell):
    def __init__(self,d,c):
        self.d=d; self.c=c
        super().__init__(.5)
    def phase(self,r): return super().phase(r)*self.c/(-.8)
    def free(self,r):
        a,ap=self.envelope(r);w=self.frequency(r);p=np.exp(1j*self.phase(r))
        return p*a,p*(ap+1j*self.c*w*a),p*(-self.d*(ap+a/r)-1j*w*a)
    def constraint_rhs(self,r,y):
        Q,f,_=y;a,ap=self.envelope(r);w=self.frequency(r)
        S=ap*ap+self.d**2*(ap+a/r)**2+(1+self.c**2)*w*w*a*a
        return [.6*w*r*r*a*a,(1-f)/r-Q*Q/r**3-r*f*S,1/np.sqrt(f)]

def main():
    base=DirectionShell(.8,-.8)
    rr=np.linspace(6,14,257)
    records=[]
    for alpha,beta in [(1.,0.),(0.,1.)]:
        def rhs(r,y):
            f=base.sol.sol(r)[1];a,ap=base.envelope(r);w=base.frequency(r);A=ap+a/r
            S=ap**2+.64*A*A+1.64*w*w*a*a
            s=1.6*alpha*A*A-1.6*beta*w*w*a*a
            return [-(1/r+r*S)*y[0]-r*f*s,-.5*f**(-1.5)*y[0]]
        tangent=solve_ivp(rhs,(6,14),[0,0],method='DOP853',rtol=2e-11,atol=2e-13,max_step=1/32,dense_output=True)
        assert tangent.success
        fd,xd=tangent.sol(rr)
        expected_mass=-7*fd[-1]
        differences=[]
        for eps in [1e-3,5e-4]:
            plus=DirectionShell(.8+eps*alpha,-.8+eps*beta)
            minus=DirectionShell(.8-eps*alpha,-.8-eps*beta)
            deriv=(plus.sol.sol(rr)-minus.sol.sol(rr))/(2*eps)
            ef=float(max(abs(deriv[1]-fd))); ex=float(max(abs(deriv[2]-xd)))
            em=abs((plus.ADM_mass-minus.ADM_mass)/(2*eps)-expected_mass)
            assert max(abs(deriv[0]))<1e-9 and ef<2e-5 and ex<.01 and em<2e-4
            differences.append(dict(epsilon=eps,max_f_derivative_error=ef,max_proper_distance_derivative_error=ex,mass_derivative_error=em))
        jrat=[]; identities=[]
        for r in np.linspace(6.2,13.8,97):
            f=base.sol.sol(r)[1];a,ap=base.envelope(r);w=base.frequency(r);dotf=tangent.sol(r)[0]
            J=.6*r*r*np.sqrt(f)*1.8*w*a*a/2
            P=r*f*1.8**2*w*w*a*a/4
            identities.append(abs(P-J*J/(.36*r**3*a*a)))
            jrat.append(dotf/(2*f)-beta/1.8)
        assert max(identities)<1e-13
        records.append(dict(alpha=alpha,beta=beta,mass_derivative=expected_mass,proper_support_derivative=xd[-1],sampled_log_outgoing_current_derivative_range=[min(jrat),max(jrat)],differences=differences,max_phase_cost_identity_error=max(identities)))
    f,nu,F,N,t=sp.symbols('f nu F N t',nonzero=True)
    assert sp.simplify(sp.diff(-(f+t*F)/(4*(nu+t*N)),t).subs(t,0)-(f*N-F*nu)/(4*nu**2))==0
    out=dict(passed=True,records=records,lambda_variation_symbolically_verified=True,scope='initial constraint tangent and exact algebra only; no PDE error bound or future sensitivity',goal_A_proved=False,environment=dict(python=sys.version,platform=platform.platform(),numpy=np.__version__),source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'computations/shape_probe.py',ROOT/'proofs/VAR01_CONSTRAINT_AND_TRANSPORT.md']})
    dest=ROOT/'results/VAR01_INITIAL_TANGENT.json'
    if dest.exists(): raise FileExistsError(dest)
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(records,indent=2))

if __name__=='__main__':main()
