"""Exact audit of S01 source weights, high-frequency test, and actual commutator."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def check(expr,label):
    if s.simplify(expr)!=0:
        raise ArithmeticError(label)


def main():
    p,eps=s.symbols('p eps',real=True)
    Wpower=p-(1-2*eps)
    Hpower=Wpower-2+6-2
    check(Hpower-(p+1+2*eps),'source H power')
    check((Hpower-4)-(p-3-2*eps)-4*eps,'zero order weight quotient')
    check((Hpower-2)-(p-1-2*eps)-4*eps,'radial derivative weight quotient')
    R,r=s.symbols('R r',positive=True)
    pp,ee=s.Rational(5,4),s.Rational(1,8)
    tail=s.integrate(r**(pp-3+2*ee),(r,R,s.oo))
    check(tail-R**(pp-2+2*ee)/(2-pp-2*ee),'finite r^-2 source tail')
    if s.integrate(r**(pp-3+2*ee),(r,R,s.oo))==s.oo:
        raise ArithmeticError('false nonintegrability claim accepted')
    n,e,delta,x,t=s.symbols('n e delta x t',positive=True)
    Hcoeff=2*e*delta*x*n+e**2*delta**2*x**2
    source=2*s.pi*n*n*s.integrate(Hcoeff**2,(x,1,2))
    energy=2*s.pi*(2*n*n+1)
    check(s.limit(source/(n*n*energy),n,s.oo)-s.Rational(14,3)*e*e*delta*delta,'high frequency derivative loss')
    # Derive the commutator independently from generic time/space potentials.
    tc,xc=s.symbols('tc xc',real=True)
    ee0=s.symbols('ee0',real=True)
    At,Ax,U,psi=[s.Function(name)(tc,xc) for name in ['At','Ax','U','psi']]
    Dt=lambda z:s.diff(z,tc)+s.I*ee0*At*z
    Dx=lambda z:s.diff(z,xc)+s.I*ee0*Ax*z
    L=lambda z:Dt(Dt(z))-Dx(Dx(z))+U*z
    electric=ee0*(s.diff(Ax,tc)-s.diff(At,xc))
    comm=L(Dt(psi))-Dt(L(psi))
    claimed=2*s.I*electric*Dx(psi)+(s.I*s.diff(electric,xc)-s.diff(U,tc))*psi
    check(comm-claimed,'actual covariant time commutator')
    wrong=2*s.I*electric*Dx(psi)+(-s.I*s.diff(electric,xc)-s.diff(U,tc))*psi
    if s.simplify(comm-wrong)==0:
        raise ArithmeticError('wrong electric-gradient sign accepted')
    # Real invariant contractions in the actual energy identity.
    pr,pi,xr,xi,ur,ui,E=s.symbols('pr pi xr xi ur ui E',real=True)
    # Re(i E psi conj(X)) = E Im(conj(psi) X).
    left=s.re(s.I*E*(ur+s.I*ui)*(xr-s.I*xi))
    right=E*s.im((ur-s.I*ui)*(xr+s.I*xi))
    check(left-right,'charged energy work sign')
    # Independently verify the full real energy divergence on arbitrary polynomial jets.
    tr,xs=s.symbols('tr xs',real=True)
    qcoupling=s.Rational(3,5)
    at_poly=tr*xs; ax_poly=xs*xs; u_poly=1+tr*tr*xs
    psi_poly=tr*tr+xs+s.I*(tr+xs*xs)
    dtime=lambda z:s.diff(z,tr)+s.I*qcoupling*at_poly*z
    dspace=lambda z:s.diff(z,xs)+s.I*qcoupling*ax_poly*z
    Pt=dtime(psi_poly); Xx=dspace(psi_poly)
    square=lambda z:s.expand(z*s.conjugate(z))
    density=(square(Pt)+square(Xx)+u_poly*square(psi_poly))/2
    flux=s.re(Xx*s.conjugate(Pt))
    ef=qcoupling*(s.diff(ax_poly,tr)-s.diff(at_poly,xs))
    residual=dtime(Pt)-dspace(Xx)+u_poly*psi_poly
    check(s.diff(density,tr)-s.diff(flux,xs)-ef*s.im(s.conjugate(psi_poly)*Xx)
          -s.diff(u_poly,tr)*square(psi_poly)/2-s.re(residual*s.conjugate(Pt)),
          'actual energy divergence with arbitrary residual')
    # D001 Maxwell signs, transformed from u,v to t,x.
    jr,ji,vr,vi,rrad,rxrad,charge,Omega=s.symbols('jr ji vr vi rrad rxrad charge Omega',real=True)
    scalar=jr+s.I*ji
    Du=ur+s.I*ui; Dv=vr+s.I*vi
    Qu=-qcoupling*rrad**2*s.im(scalar*s.conjugate(Du))
    Qv=qcoupling*rrad**2*s.im(scalar*s.conjugate(Dv))
    jx=s.im(s.conjugate(scalar)*(Dv-Du))
    check(Qu+Qv+qcoupling*rrad**2*jx,'Maxwell transformed charge current')
    Ps=rrad*scalar; Xs=rxrad*scalar+rrad*(Dv-Du)
    check(s.im(s.conjugate(Ps)*Xs)-rrad**2*jx,'rescaled scalar spatial current')
    Qt,coeff,dcoeff=s.symbols('Qt coeff dcoeff',real=True)
    check(-coeff*charge*Qt+(coeff*charge*Qt+charge**2*dcoeff/2)-charge**2*dcoeff/2,
          'Maxwell energy work cancellation with geometric remainder')
    # Full physical (unrescaled scalar) identity, allowing both PDE residuals.
    rad=2+tr*tr+xs*xs
    field=s.diff(ax_poly,tr)-s.diff(at_poly,xs)
    actualQ=rad**2*field  # Omega^2=1; enforce the electric-field definition.
    scalar_residual=residual-u_poly*psi_poly+2/rad*(s.diff(rad,tr)*Pt-s.diff(rad,xs)*Xx)
    current=s.im(s.conjugate(psi_poly)*Xx)
    maxwell_residual=s.diff(actualQ,tr)+qcoupling*rad**2*current
    physical_density=rad**2*(square(Pt)+square(Xx))/2+actualQ**2/(2*rad**2)
    physical_flux=rad**2*flux
    geometry=rad*s.diff(rad,tr)*(square(Xx)-square(Pt))+actualQ**2*s.diff(rad**-2,tr)/2
    check(s.diff(physical_density,tr)-s.diff(physical_flux,xs)-geometry
          -rad**2*s.re(scalar_residual*s.conjugate(Pt))-actualQ/rad**2*maxwell_residual,
          'physical positive energy with scalar/Maxwell residuals')
    # Independent null-to-Cartesian conversion of the actual geometric mass flux.
    uflux,vflux,O2,rad0,Qt0,nu0,lam0=s.symbols('uflux vflux O2 rad0 Qt0 nu0 lam0',real=True)
    mu=nu0*Qt0**2/(2*rad0**2)-2*rad0**2*lam0*uflux/O2
    mv=lam0*Qt0**2/(2*rad0**2)-2*rad0**2*nu0*vflux/O2
    es=rad0**2*(uflux+vflux); em=O2*Qt0**2/(2*rad0**2)
    ff=rad0**2*(vflux-uflux); rtime=nu0+lam0; rspace=lam0-nu0
    check(mv-mu-rspace/O2*(es+em)+rtime/O2*ff,'Einstein mass spatial energy current')
    check(mv+mu-rspace/O2*ff+rtime/O2*(es-em),'Einstein mass temporal pressure current')
    wrong_time=rspace/O2*ff-rtime/O2*(es+em)
    if s.simplify(mv+mu-wrong_time)==0:
        raise ArithmeticError('wrong electromagnetic radial pressure sign accepted')
    # Coupling/sign map: qG=e, AG=-AP and DG=partial-i qG AG.
    AP=s.symbols('AP')
    check(-s.I*e*(-AP)-s.I*e*AP,'wave-operator charge convention')
    root=Path(__file__).resolve().parent
    names=['verify_global_rn_source_norm.py','GLOBAL_RN_SOURCE_NORM_AUDIT.md','../../definitions/MODEL.md']
    report=dict(claim_ids=['S01.1','S01.2','S01.3','S01.4','S01.5','S01.6','S01.7','S01.8'],
                logic='PROVED (finite algebra/power tests and restricted functional counterexamples only)',
                evidence='EXACT_ALGEBRA',audit='INTERNAL_AUDIT',sympy_version=s.__version__,
                checks=['wave-operator sign/product map','source H power','r^-2 radial tail finite',
                        'r^(4 epsilon) weight quotient','n^4 versus n^2 source derivative test',
                        'actual covariant commutator','charged energy-work sign',
                        'full polynomial energy divergence','D001 Maxwell signs and rescaled scalar current',
                        'Maxwell work cancellation with retained geometry remainder',
                        'positive physical energy identity with both PDE residuals',
                        'Einstein mass current and electromagnetic pressure sign'],
                negative_controls=['r^-2 does not automatically diverge','wrong electric-gradient sign rejected',
                                   'uniform coefficient smallness does not imply pointwise same-weight absorption',
                                   'first-order forcing does not have a same-order source-derivative bound',
                                   'electromagnetic radial pressure cannot be replaced by positive total energy'],
                source_theorem=dict(url='https://arxiv.org/pdf/2603.28874v1',
                                    locators=['section 2.8 equations (2.16)-(2.17)','Theorem 3.1 equation (3.1)'],
                                    rho_factors='product, verified against official HTML math alttext',
                                    imported_nonlinear_conclusion=False),
                example_weights=dict(p=str(pp),epsilon=str(ee),radial_tail=str(tail)),
                full_source_budget_verified=False,global_causal_identification_verified=False,
                goal_A_proved=False,
                source_sha256={name:sha256((root/name).read_bytes()).hexdigest() for name in names})
    (root/'GLOBAL_RN_SOURCE_NORM_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: source powers, restricted high-frequency/weight tests, actual covariant commutator; global PDE OPEN')


if __name__=='__main__':
    main()
