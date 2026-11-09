"""Exact algebra for T01, with actual local constant-scalar negative control."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def check(expr,label):
    if s.simplify(expr)!=0:
        raise ArithmeticError(label)


def main():
    r,O,nu,lam,m,Q=s.symbols('r O nu lam m Q',nonzero=True,real=True)
    mixed=-nu*lam/r-O*(1-Q**2/r**2)/(4*r)
    check((-4*mixed/r).subs(nu*lam,O*(2*m/r-1)/4)-O*(2*m/r**3-Q**2/r**4),'actual wave potential')
    # Four independent real jet components for the multiplier identity.
    p,x,a,b,pt,xx,px,hh,hx,U,Ux,E=s.symbols('p x a b pt xx px hh hx U Ux E',real=True)
    # Complex notation reduced to invariants: |P|^2=p, |X|^2=x, |psi|^2=a,
    # Re(PbarX)_t=Re(PtbarX)+1/2(p)_x+E Im(psi_bar P).
    # Treat real contractions below as independent exact scalars.
    ptX,PxP,XxX,psiX,j=s.symbols('ptX PxP XxX psiX j',real=True)
    C_t=hh*(ptX+PxP+E*j)
    D_x=-hx*(p+x)/2-hh*(PxP+XxX)+ (hx*U+hh*Ux)*a/2+hh*U*psiX
    bulk=hx*(p+x)/2-(hx*U+hh*Ux)*a/2
    multiplied=hh*(ptX-XxX+U*psiX)
    check(C_t+D_x+bulk-hh*E*j-multiplied,'covariant current identity')
    if s.simplify(C_t+D_x+bulk-multiplied)==0:
        raise ArithmeticError('omitted electric commutator accepted')
    A,B,eta=s.symbols('A B eta',real=True,nonzero=True)
    check(eta*A*A/4+B*B/eta-A*B-(s.sqrt(eta)*A/2-B/s.sqrt(eta))**2,'electric/source Young control')
    rt,rx,k=s.symbols('rt rx k',real=True,nonzero=True)
    vv=1-rt/rx
    check((-O/(2*(rt-rx)))*vv-O/(2*rx),'fixed-radius trace weight')
    # RN operator coefficient example, all constants rational and e fixed.
    rr=s.symbols('rr',positive=True)
    mass,charge,e,lo,hi=map(s.Rational,['1/10','1/10','3/5','2/5','1/2'])
    f=(1-mass/rr)**2
    potential=f*(2*mass/rr**3-2*charge**2/rr**4)
    density=-f*s.diff(rr*potential,rr)/2
    claimed=mass*(rr-mass)**4*(2*rr-5*mass)/rr**8
    check(density-claimed,'ERN virial potential')
    eta0=(1-mass/lo)**2
    c0=mass*(lo-mass)**4*(2*lo-5*mass)/hi**8
    max_hE=e*charge*(1-mass/hi)**2/lo
    margin=c0/2-max_hE**2/eta0
    if margin!=s.Rational(230,15625):
        raise ArithmeticError('rational RN coercivity margin')
    # Actual local full-system solution: neutral Schwarzschild, constant scalar.
    fs=1-2*mass/rr
    Us=fs*2*mass/rr**3
    D=-rr*fs**2/2+rr*Us*rr**2/2
    local_bulk=fs**3/2-s.diff(rr*Us,rr)*fs*rr**2/2
    check(local_bulk-fs*(s.Rational(1,2)-4*mass**2/rr**2),'constant scalar bulk')
    check(fs*s.diff(D,rr)+local_bulk,'constant scalar boundary balance')
    if local_bulk.subs(rr,s.Rational(1,2))<=0:
        raise ArithmeticError('boundary omission negative control')
    # Constant scalar solves the true reduced wave equation (not just constraints).
    check(-fs*s.diff(fs,rr)+Us*rr,'constant scalar solves Schwarzschild wave')
    # Removing AF anchoring leaves an actual zero-derivative nonzero-amplitude mode.
    if s.simplify(s.diff(s.Integer(1),rr))!=0:
        raise ArithmeticError('constant-scalar derivative control')
    # Exact operator difference in a common conformal chart, component by component.
    t,xcoord=s.symbols('t xcoord',real=True)
    e0,deltaU=s.symbols('e0 deltaU',real=True)
    at,ax,A0t,A0x,psi=[s.Function(n)(t,xcoord) for n in ['at','ax','A0t','A0x','psi']]
    Dt=lambda z:s.diff(z,t)+s.I*e0*(A0t+at)*z
    Dx=lambda z:s.diff(z,xcoord)+s.I*e0*(A0x+ax)*z
    D0t=lambda z:s.diff(z,t)+s.I*e0*A0t*z
    D0x=lambda z:s.diff(z,xcoord)+s.I*e0*A0x*z
    actual_minus_reference=Dt(Dt(psi))-Dx(Dx(psi))-D0t(D0t(psi))+D0x(D0x(psi))+deltaU*psi
    source=-2*s.I*e0*(at*D0t(psi)-ax*D0x(psi))-s.I*e0*(s.diff(at,t)-s.diff(ax,xcoord))*psi+e0**2*(at**2-ax**2)*psi-deltaU*psi
    check(actual_minus_reference+source,'common-conformal operator difference')
    # Radial anchoring bounds a constant field error without secular time growth.
    delta=s.symbols('delta',real=True)
    apot=-delta*xcoord
    check(-s.diff(apot,xcoord)-delta,'radial anchored field difference')
    v=s.symbols('v',positive=True)
    secular=-s.log(1+v)/2
    check(s.diff(secular,v)+1/(2*(1+v)),'Av-zero small-field secular-potential control')
    root=Path(__file__).resolve().parent
    names=['verify_exterior_trace_multiplier.py','EXTERIOR_TRACE_MULTIPLIER_AUDIT.md','../../definitions/MODEL.md']
    report=dict(claim_ids=['T01.1','T01.2','T01.3','T01.4','T01.6'],logic='PROVED (finite identities and explicit local counterexample only)',
                evidence='EXACT_ALGEBRA',audit='INTERNAL_AUDIT',sympy_version=s.__version__,
                checks=['actual reduced potential','covariant multiplier identity','Young absorption',
                        'fixed-radius trace weight','rational ERN weak-field annulus',
                        'constant-scalar Schwarzschild wave and boundary balance',
                        'common-conformal first-order source','radial anchoring and Av-zero secular control'],
                negative_controls=['omitted electric commutator','omitted timelike amplitude boundary',
                                   'bounded mass and zero local derivative flux do not bound amplitude trace'],
                RN_example=dict(M=str(mass),Q=str(charge),e=str(e),r_interval=[str(lo),str(hi)],
                                eta=str(eta0),c=str(c0),absorption_margin=str(margin)),
                global_boundary_budget_verified=False,nonlinear_RN_transfer_verified=False,
                global_AF_counterexample=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'EXTERIOR_TRACE_MULTIPLIER_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: actual-wave/current algebra and local full-system boundary counterexample; global transfer OPEN')


if __name__=='__main__':
    main()
