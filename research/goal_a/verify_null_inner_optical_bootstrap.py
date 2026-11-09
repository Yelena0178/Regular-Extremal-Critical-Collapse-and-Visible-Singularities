"""O01.7-10 finite algebra/audit controls; not actual-strip or Goal A certification."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def check(expr, name):
    if s.simplify(expr) != 0:
        raise ArithmeticError(name)


def main():
    r,k,nu,f,q,qu,qv,z2,V2=s.symbols('r k nu f q qu qv z2 V2',nonzero=True,real=True)
    # Recover geometric mass fluxes from D001 renormalized fluxes.
    P2=nu**2*z2/r**2
    O=-4*k*nu
    lam=k*f
    varpi_u=-2*r*r/O*lam*P2+q*qu/r
    varpi_v=-2*r*r/O*nu*V2+q*qv/r
    mu=varpi_u-q*qu/r+q*q*nu/(2*r*r)
    mv=varpi_v-q*qv/r+q*q*lam/(2*r*r)
    check(mu-(nu*q*q/(2*r*r)+nu*f*z2/2),'m_u')
    check(mv-(lam*q*q/(2*r*r)+r*r*V2/(2*k)),'m_v')
    fixed=mv-lam/nu*mu
    check(fixed-(r*r*V2/(2*k)-k*f*f*z2/2),'fixed-r mass derivative')
    # Substituting varpi instead would leave uncancelled charge work.
    wrong=varpi_v-lam/nu*varpi_u
    if s.simplify(wrong-fixed).subs({r:2,k:1,nu:-1,f:s.Rational(1,10),q:1,qu:0,qv:1,z2:1,V2:1}) == 0:
        raise ArithmeticError('renormalized-mass substitution accepted')
    ap,wa,ma,a,b,M,a0=s.symbols('ap wa ma a b M a0',positive=True)
    boundary_term=lam*wa-ap*wa
    check(boundary_term.subs(ap,lam),'outgoing inner endpoint cancellation')
    if boundary_term.subs({k:1,f:1,ap:2,wa:1}) == 0:
        raise ArithmeticError('arbitrary moving endpoint accepted')
    check(M*(1/a-1/b)+M*(1/a0-1/a)-M*(1/a0-1/b),'mass endpoint cancellation')
    d,F,e,q0,L,A,mbdot,trace,alpha=s.symbols('d F e q0 L A mbdot trace alpha',positive=True)
    # O9 after fixed-r mass and weighted Hardy substitutions.
    rhs=4/d*(2*mbdot+F**2*A+2*e**2*q0**2*(L*trace+L**2*A))
    claimed=8/d*mbdot+(4*F**2+8*e**2*q0**2*L**2)/d*A+8*e**2*q0**2*L/d*trace
    check(rhs-claimed,'absorption coefficients')
    check((4*F**2+8*e**2*q0**2*L**2)/d-4/d*(F**2+2*e**2*q0**2*L**2),'smallness budget')
    if s.simplify(d/2-4/d*(d*d/16)-d/4)!=0:
        raise ArithmeticError('remaining damping')
    # A constant field disproves Hardy without its outer trace term.
    rr=s.symbols('rr',positive=True)
    if s.integrate(1,(rr,1,2)) <= 0:
        raise ArithmeticError('Hardy boundary negative control')
    base=1+s.I+(2-rr)+s.I*(2-rr)**2
    weight=1+rr
    square=lambda expr:s.expand(expr*s.conjugate(expr))
    H=s.integrate(weight*square(base),(rr,1,2))
    grad=s.integrate(weight*square(s.diff(base,rr)),(rr,1,2))
    hardy_margin=2*3*square(base.subs(rr,2))+2*grad-H
    if hardy_margin<0:
        raise ArithmeticError('complex monotone-weight Hardy control')
    gauge,coupling_symbol=s.symbols('gauge coupling_symbol',real=True,nonzero=True)
    phase=s.exp(-s.I*coupling_symbol*gauge*rr)
    cov=s.diff(phase*base,rr)+s.I*coupling_symbol*gauge*phase*base
    check(cov-phase*s.diff(base,rr),'covariant radial phase transport')
    if s.simplify(s.diff(phase*base,rr)-phase*s.diff(base,rr))==0:
        raise ArithmeticError('ordinary derivative substituted for covariant derivative')
    if (d/2-4*F*F/d).subs({d:1,F:s.Rational(1,2)})>=0:
        raise ArithmeticError('missing thin-strip smallness not rejected')
    v=s.symbols('v',nonnegative=True)
    h=(1+v)**(-s.Rational(1,4))
    if s.integrate(s.diff(h,v)**2,(v,0,s.oo))!=s.Rational(1,24):
        raise ArithmeticError('trace derivative energy control')
    if s.integrate(h*h,(v,0,s.oo))!=s.oo:
        raise ArithmeticError('decay implies L2 negative control')
    lapse,fpos,kpos,T=s.symbols('lapse fpos kpos T',positive=True)
    dvdt=lapse/(2*kpos*s.sqrt(fpos))
    check(-4*kpos*kpos*fpos*dvdt**2+lapse**2,'fixed-radius lapse conversion')
    check(s.integrate((1+v)**-3,(v,T,s.oo))-1/(2*(1+T)**2),'exit trace tail integral')
    # A rational subextremal RN strip satisfies the smallness premise.
    mass,charge,inner,outer,coupling=map(s.Rational,['5/8','3/8','9/8','23/20','3/5'])
    RN=1-2*mass/rr+charge**2/rr**2
    check(RN.subs(rr,inner),'RN horizon radius')
    cap=charge/inner; margin=1-cap**2; width=outer-inner; upper=RN.subs(rr,outer)
    smallness=margin**2/16-upper**2-2*coupling**2*cap**2*width**2
    if smallness<=0 or upper<=0:
        raise ArithmeticError('subextremal RN thin strip control')
    # Independent floating fixed-area derivative on the exact nonzero-flux FLRW trace.
    import numpy as np
    from scipy.optimize import brentq
    from verify_centered_cauchy_diamond import flrw
    radius,label=.7,1.5
    def at(v0):
        t0=brentq(lambda t0:np.sqrt(1-t0/4)*(v0-t0)-radius,0,v0)
        return flrw(t0,v0-t0)
    y=at(label)
    derivative=(at(label+1e-5)[7]-at(label-1e-5)[7])/2e-5
    exact=radius**2*(y[2]/radius)**2/(2*y[1])-y[1]*(1-2*y[7]/radius)**2*y[5]**2/2
    if abs(derivative-exact)>1e-9:
        raise ArithmeticError('fixed-area FLRW mass flux control')
    root=Path(__file__).resolve().parent
    names=['verify_null_inner_optical_bootstrap.py','INCOMING_OPTICAL_DEPTH_GATE.md',
           'verify_centered_cauchy_diamond.py','OUTGOING_LOCAL_DECAY.md','../../definitions/MODEL.md']
    report=dict(claim_ids=['O01.7','O01.8','O01.9','O01.10','O01.11'],
                logic='PROVED (checked finite identities and explicit controls only)',
                evidence=['EXACT_ALGEBRA','EXPERIMENTAL (FLRW derivative control)'],audit='INTERNAL_AUDIT',
                checks=['geometric mass flux from renormalized mass','fixed-area derivative',
                        'moving-boundary mass cancellation','Hardy absorption constants','remaining damping',
                        'rational subextremal RN thin strip','complex weighted Hardy control',
                        'covariant radial phase transport','fixed-radius lapse/trace conversion and integrable tail'],
                negative_controls=['renormalized mass is not geometric mass',
                                   'arbitrary moving endpoint leaves residual',
                                   'constant field needs Hardy boundary term','decay and derivative L2 do not imply amplitude L2',
                                   'ordinary radial derivative loses gauge term','large f loses absorption'],
                complex_Hardy_control=dict(exact_margin=str(hardy_margin)),
                RN_control=dict(M=str(mass),Q=str(charge),a=str(inner),b=str(outer),
                                smallness_margin=str(smallness)),
                FLRW_fixed_area_control=dict(difference=derivative,formula=float(exact),error=abs(derivative-exact)),
                actual_candidate_strip_verified=False,boundary_trace_integrability_verified=False,
                goal_A_proved=False,sympy_version=s.__version__,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'NULL_INNER_OPTICAL_BOOTSTRAP_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: null-inner optical identities and adversarial controls; candidate/global premises OPEN')


if __name__=='__main__':
    main()
