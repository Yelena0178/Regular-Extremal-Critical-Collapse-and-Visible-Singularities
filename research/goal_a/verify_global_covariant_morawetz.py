"""Exact actual-current residual checks, flat global control, and ERN coefficient audit."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def check(expr,name):
    if s.simplify(expr)!=0:
        raise ArithmeticError(name)


def main():
    t,x=s.symbols('t x',real=True)
    e=s.Rational(3,5)
    r=2+t*t+x; At=t*x; Ax=x*x
    phi=t*t+x+s.I*(t+x*x)
    Dt=lambda z:s.diff(z,t)+s.I*e*At*z
    Dx=lambda z:s.diff(z,x)+s.I*e*Ax*z
    square=lambda z:s.expand(z*s.conjugate(z))
    P=Dt(phi); X=Dx(phi); S=square(phi)
    field=s.diff(Ax,t)-s.diff(At,x); Q=r*r*field # Omega^2=1
    Es=r*r*(square(P)+square(X))/2; Em=Q*Q/(2*r*r)
    F=r*r*s.re(X*s.conjugate(P)); pressure=Es-Em
    scalar_res=Dt(P)-Dx(X)+2/r*(s.diff(r,t)*P-s.diff(r,x)*X)
    jtime=s.im(s.conjugate(phi)*P)
    charge_res=s.diff(Q,x)+e*r*r*jtime
    source=r*r*s.re(scalar_res*s.conjugate(X))+Q/r**2*charge_res
    check(s.diff(F,t)-s.diff(pressure,x)-r*s.diff(r,x)*(square(X)-square(P))
          -Q*Q*s.diff(r**-2,x)/2-source,'actual momentum balance with residuals')
    h=r/(1+r); g=s.diff(r,x)/(1+r)
    C=h*F+r*r*g*s.re(P*s.conjugate(phi))-r*r*s.diff(g,t)*S/2
    D=h*pressure+r*r*g*s.re(X*s.conjugate(phi))-r*r*s.diff(g,x)*S/2
    Ag=(s.diff(r*r*s.diff(g,x),x)-s.diff(r*r*s.diff(g,t),t))/2
    hp=1/(1+r)**2
    K=hp*r*r/2*(s.diff(r,x)*(square(P)+square(X))-2*s.diff(r,t)*s.re(X*s.conjugate(P)))
    K-=Ag*S+hp*s.diff(r,x)*Em+h*Q*Q*s.diff(r**-2,x)/2
    residual=h*source+r*r*g*s.re(scalar_res*s.conjugate(phi))
    check(s.diff(C,t)-s.diff(D,x)+K-residual,'full weighted current with scalar and Maxwell residuals')
    # Independent generic-radius identity removes superficial third derivatives.
    R=s.Function('R')(t,x); rx=s.diff(R,x); rt=s.diff(R,t)
    gg=rx/(1+R); B=s.diff(R,t,2)-s.diff(R,x,2); Z=rx*rx-rt*rt
    actual=(s.diff(R**2*s.diff(gg,x),x)-s.diff(R**2*s.diff(gg,t),t))/2
    formula=-R**2*s.diff(B,x)/(2*(1+R))+R**2*B*rx/(2*(1+R)**2)
    formula+=R*s.diff(Z,x)/(2*(1+R)**2)-R*Z*rx/(1+R)**3
    check(actual-formula,'generic radius amplitude coefficient reduction')
    rr=s.symbols('rr',positive=True)
    flat_h=rr/(1+rr); flat_g=1/(1+rr)
    flat_A=s.diff(rr*rr*s.diff(flat_g,rr),rr)/2
    check(flat_A+rr/(1+rr)**3,'flat positive amplitude weight')
    check(s.diff(flat_h,rr)*rr**2/2-rr**2/(2*(1+rr)**2),'flat derivative weight')
    # Exact independent free-wave normalization and trace.
    b=s.symbols('b',positive=True)
    wave=(s.exp(-(t-b)**2)-s.exp(-(t+b)**2))/b
    energy=s.integrate(8*rr**2*s.exp(-2*rr**2),(rr,0,s.oo))
    check(energy-s.sqrt(s.pi/2),'Gaussian free-wave energy')
    integral=s.integrate(s.exp(-2*(t-b)**2)+s.exp(-2*(t+b)**2)
                         -2*s.exp(-2*(t*t+b*b)),(t,0,s.oo))/b**2
    check(integral-energy*(1-s.exp(-2*b*b))/b**2,'Gaussian amplitude trace integral')
    check(s.limit(wave,b,0)-4*t*s.exp(-t*t),'Gaussian regular center')
    M,rho=s.symbols('M rho',positive=True)
    f=(1-M/rr)**2; ern_g=f/(1+rr)
    ern_A=f*s.diff(rr**2*f*s.diff(ern_g,rr),rr)/2
    lead=s.limit(ern_A.subs(rr,M+rho)/rho**4,rho,0)
    check(lead-3/(M**4*(1+M)),'ERN amplitude sign at horizon')
    if lead.is_positive is not True:
        raise ArithmeticError('flat pointwise coercivity wrongly extended to ERN')
    repaired_h=(rr-2*M)/(rr+M)
    repaired_g=repaired_h*f/rr
    repaired_A=f*s.diff(rr**2*f*s.diff(repaired_g,rr),rr)/2
    check(repaired_A.subs(rr,2*M)-s.Rational(7,576)/M,
          'bounded horizon-sign repair still has interior wrong sign')
    # Exact charged inversion, including the constant horizon-frequency shift.
    coupling,charge=s.symbols('coupling charge',nonzero=True,real=True)
    inv_r=M+M**2/rho
    check(coupling*charge/(M+rho)+coupling*charge/inv_r-coupling*charge/M,
          'charged inversion potential complement')
    Uref=2*M*rho**3/(M+rho)**6
    check(Uref.subs(rho,M**2/rho)-Uref,'inversion of reduced ERN potential')
    xt=rho+2*M*s.log(rho/M)-M**2/rho
    check(s.expand_log(xt.subs(rho,M**2/rho)+xt,force=True),'tortoise reflection')
    if s.simplify(coupling*charge/(M+rho)+coupling*charge/inv_r)==0:
        raise ArithmeticError('neutral inversion without charged phase accepted')
    root=Path(__file__).resolve().parent
    names=['verify_global_covariant_morawetz.py','GLOBAL_COVARIANT_MORAWETZ.md','../../definitions/MODEL.md']
    report=dict(claim_ids=['M01.1','M01.2','M01.3','M01.4','M01.5','M01.6','M01.7'],
                logic='PROVED (checked finite identities/control integrals only)',evidence='EXACT_ALGEBRA',audit='INTERNAL_AUDIT',
                checks=['actual momentum residual','full actual weighted current residual',
                        'generic-radius coefficient reduction','flat positive weights',
                        'Gaussian energy, trace and center','ERN near-horizon coefficient sign',
                        'bounded horizon-sign repair still fails inside the exterior',
                        'charged inversion potential/phase and tortoise reflection'],
                limits=['free-wave estimate is not a nonlinear EMCSF proof',
                        'bounded-weight class obstruction only excludes pointwise coercivity of the stated current',
                        'center regularity and AF boundary coverage must be proved for actual domains',
                        'fixed ERN inversion is not a nonlinear collapse symmetry'],
                Gaussian=dict(energy=str(energy),trace=str(s.simplify(integral))),
                ERN_amplitude_leading_coefficient=str(lead),sympy_version=s.__version__,
                actual_global_decay_verified=False,actual_horizon_identity_verified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'GLOBAL_COVARIANT_MORAWETZ_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: actual coupled multiplier residuals, global free-wave controls and ERN sign audit; Goal A OPEN')


if __name__=='__main__':
    main()
