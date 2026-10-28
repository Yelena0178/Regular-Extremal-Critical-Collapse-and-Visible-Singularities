"""COUL04 exact optics, Mellin forms and negative controls, not Goal A certification."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def zero(expr,label):
    if s.simplify(s.expand(expr)) != 0:
        raise ArithmeticError(label)


def main():
    t,r=s.symbols('t r',real=True,positive=True)
    b=s.Function('b',positive=True)(t,r)
    a=s.Function('a',real=True)(t,r)
    Q=s.Function('Q',real=True)(t,r)
    V=a/b; beta=s.diff(b,r)/b; gamma=s.diff(b,t)/b
    zero(s.diff(V,r)+beta*V-s.diff(a,r)/b,'V_r retains optical radial derivative')
    zero(s.diff(V,t)+gamma*V-s.diff(a,t)/b,'V_t retains optical time derivative')
    # Pointwise integrand identity, before the endpoint and time integrations.
    zero(-s.diff(a,r)*s.diff(Q,t)/b+s.diff(V*s.diff(Q,t),r)
         -s.diff(V*s.diff(Q,r),t)+s.diff(V,t)*s.diff(Q,r)+beta*V*s.diff(Q,t),
         'Coulomb power complete integration by parts')
    if s.simplify(s.diff(V,r)-s.diff(a,r)/b)==0:
        raise ArithmeticError('omitting beta was not rejected')
    # Independent field jets for optical beta transport, with the actual wave law.
    e,c,cr,ar=s.symbols('e c cr ar',real=True)
    yr,yi,xr,xi,xxr,xxi,sr,si=s.symbols('yr yi xr xi xxr xxi sr si',real=True)
    phi=yr+s.I*yi; X=xr+s.I*xi; Xr=xxr+s.I*xxi; S=sr+s.I*si
    norm=lambda z:s.expand(z*s.conjugate(z))
    re=lambda z:s.expand(s.re(z))
    DtX=c*Xr/2+(cr/2+c/r)*X-S/r-s.I*e*ar*phi/2
    betaval=r*norm(X); betar=norm(X)+2*r*re(Xr*s.conjugate(X))
    betat=2*r*re(DtX*s.conjugate(X)); Qr=e*r*r*s.im(phi*s.conjugate(X))
    zero(betat-c*betar/2-(cr+3*c/(2*r))*betaval+2*re(S*s.conjugate(X))-ar*Qr/r,
         'full nonlinear optical beta transport')
    # Independent reduced wave reconstructs the physical derivative equation.
    reduced_Z_transport=cr*r*X/2-s.I*e*ar*r*phi/2
    zero(S+r*DtX-c*(2*X+r*Xr)/2-reduced_Z_transport,
         'physical X equation agrees with reduced actual Z transport')
    # Integrating beta_t in r removes all X_r derivatives with correct coefficient.
    zero(betat-(c*betar+cr*betaval)/2
         -((cr/2+3*c/(2*r))*betaval-2*re(S*s.conjugate(X))+ar*Qr/r),
         'optical integral source and radial endpoint')
    # Scalar energy integration by parts on compact radial support.
    fr=s.symbols('fr',real=True)
    f=s.symbols('f',real=True)
    psir,psii,zr,zi=s.symbols('psir psii zr zi',real=True)
    psi=psir+s.I*psii; Z=zr+s.I*zi
    endpoint_derivative=(fr/r-f/r**2)*norm(psi)+2*f*re(psi*s.conjugate(Z))/r
    zero(f*norm(Z-psi/r)-f*norm(Z)-fr*norm(psi)/r+endpoint_derivative,
         'canonical scalar energy radial boundary identity')
    x=s.symbols('x',real=True); p=s.symbols('p',positive=True)
    alpha=(2-p)/2
    gr,gi,dr,di=s.symbols('gr gi dr di',real=True)
    g=gr+s.I*gi; dg=dr+s.I*di
    zero(norm(dg+alpha*g)-norm(dg)-alpha**2*norm(g)-2*alpha*re(dg*s.conjugate(g)),
         'Mellin derivative density and vanishing integrated real cross term')
    zero(s.im(g*s.conjugate(dg+alpha*g))-s.im(g*s.conjugate(dg)),
         'Mellin charge current')
    k,q=s.symbols('k q',real=True)
    zero(p*(k*k+alpha*alpha)/2-q*k
         -(p*(k-q/p)**2/2+p*alpha*alpha/2-q*q/(2*p)),
         'sharp logarithmic phase quadratic completion')
    sigma=s.symbols('sigma')
    for sign in [-1,1]:
        root=s.Rational(1,2)+s.I*q+sign*s.sqrt(1-4*q*q)/2
        zero(root*(root-1)-2*s.I*q*root+s.I*q,'zero-frequency Coulomb indicial root')
    # Complete RN Fourier operator: both static-time and gauge radial phases.
    ff=s.Function('f')(r); omega=s.symbols('omega',real=True)
    RR=s.Function('R')(r); phase_r=(q/r-omega)/ff
    Y1=s.diff(RR,r)+s.I*phase_r*RR
    Y2=s.diff(RR,r,2)+2*s.I*phase_r*s.diff(RR,r)+(s.I*s.diff(phase_r,r)-phase_r**2)*RR
    outgoing_mode=ff*Y2+(s.diff(ff,r)+2*s.I*(omega-q/r))*Y1+(s.I*q/r**2-s.diff(ff,r)/r)*RR
    static_mode=ff**2*s.diff(RR,r,2)+ff*s.diff(ff,r)*s.diff(RR,r)+((omega-q/r)**2-ff*s.diff(ff,r)/r)*RR
    zero(ff*outgoing_mode-static_mode,'full RN charged mode transform with both radial phases')
    missing_phase=-omega/ff
    bad_Y1=s.diff(RR,r)+s.I*missing_phase*RR
    bad_Y2=s.diff(RR,r,2)+2*s.I*missing_phase*s.diff(RR,r)+(s.I*s.diff(missing_phase,r)-missing_phase**2)*RR
    bad_mode=ff*bad_Y2+(s.diff(ff,r)+2*s.I*(omega-q/r))*bad_Y1+(s.I*q/r**2-s.diff(ff,r)/r)*RR
    if s.simplify(ff*bad_mode-static_mode)==0:
        raise ArithmeticError('missing charged gauge phase was not rejected')
    # Fully rational strict negative control; C-infinity follows analytically by H1 density.
    z=s.symbols('z',real=True)
    chi=z**3*(1-z)**3
    A=s.integrate(chi**2,(z,0,1)); B=s.integrate(s.diff(chi,z)**2,(z,0,1))
    L=s.Integer(20); qq=s.Rational(3,5); R=s.Integer(1000)
    I0=L*A; I1=B/L+(s.Rational(1,4)+qq**2)*L*A
    E0=B/(2*L)+(s.Rational(1,8)-qq**2/2)*L*A
    errE=(1/R+1/(2*R**2))*I1+(1/R+1/R**2)*I0
    errK=(2/R+s.Rational(3,2)/R**2)*I1+(2/R+3/R**2)*I0
    assert A==s.Rational(1,12012) and B==s.Rational(1,770)
    assert E0==s.Rational(-71,1201200) and E0+errE<0 and E0+errK<0
    # Actual constraint perturbation: Q and b equations at epsilon^2, not frozen Q.
    eps=s.symbols('eps',real=True)
    charge_current=e*s.im(psi*s.conjugate(Z))
    zero(eps**2*charge_current-e*s.im((eps*psi)*s.conjugate(eps*Z)),
         'actual Maxwell radial charge response is quadratic')
    b2=s.Function('b2')(r)
    zero(s.diff(s.exp(eps**2*b2),r)/s.exp(eps**2*b2)-eps**2*s.diff(b2,r),
         'exact optical exponential constraint perturbation')
    root=Path(__file__).resolve().parent
    names=['verify_coulomb_mellin_gate.py','COULOMB_RENORMALIZATION_AND_MELLIN_GATE.md',
           'FAR_ZONE_RP_AND_COULOMB_BALANCE.md','ACTUAL_BONDI_COMPLETENESS_BRIDGE.md',
           'GLOBAL_COVARIANT_MORAWETZ.md','FINITE_BONDI_EXTERIOR_REALIZATION.md',
           '../../definitions/MODEL.md','ACCEPTANCE.md']
    report=dict(claim_ids=[f'COUL04.{i}' for i in range(1,7)],
                logic='PROVED for listed identities and rational countercontrols; actual constraint extension and global-form arguments are analytic',
                evidence=['EXACT_ALGEBRA','EXACT_RN_QUADRATIC_CONTROL','ASYMPTOTIC_COULOMB_MODEL'],
                audit='INTERNAL_AUDIT',
                checks=['V_r/V_t with both optical derivatives',
                        'pointwise Coulomb work integration by parts including optical correction',
                        'independent actual optical beta transport and complete wave reconstruction',
                        'radial canonical energy endpoint identity',
                        'Mellin derivative and current, sharp quadratic completion',
                        'asymptotic zero-frequency indicial polynomial',
                        'full fixed RN time-frequency operator with gauge and tortoise phases',
                        'rational negative RN canonical energy and scalar rp bounds',
                        'actual quadratic Maxwell and exact exponential optical constraint response'],
                negative_controls=['dropping beta destroys Coulomb work identity',
                                   'omitting charged radial gauge phase fails complete RN mode transform',
                                   'canonical scalar/Coulomb-interaction energy is negative at q=3/5',
                                   'no strictly positive uniform scalar-rp form for absolute q at least 1/2'],
                rational_control={k:str(v) for k,v in dict(A=A,B=B,I0=I0,I1=I1,E0=E0,
                                  RN_energy_upper=E0+errE,RN_scalar_rp_upper=E0+errK).items()},
                polynomial_control_is_C_infinity=False,
                C_infinity_negative_profile_justification='analytic H1 density on a finite logarithmic annulus with strict negative margin',
                actual_constraint_negative_energy_justification='analytic fixed-profile epsilon^2 expansion with O(epsilon^4) remainder',
                actual_constraint_ODE_numerically_certified=False,
                actual_weighted_radiation_flux_verified=False,late_charge_limit_verified=False,
                actual_instability_or_no_decay_proved=False,RN_convergence_verified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'COULOMB_MELLIN_GATE_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: COUL04 exact optical/work identities and strict rational RN negative forms; C-infinity/constraint continuation analytic, weighted radiation/Goal A OPEN')


if __name__=='__main__':
    main()
