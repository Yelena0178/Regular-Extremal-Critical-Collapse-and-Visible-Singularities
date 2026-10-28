"""Exact EF gauge, transverse/weight map, Bondi jet and paired-pulse compatibility checks."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def check(expr,name):
    if s.simplify(expr)!=0:
        raise ArithmeticError(name)


def main():
    M,rho,R=s.symbols('M rho R',positive=True)
    Q,e=s.symbols('Q e',real=True,nonzero=True)
    r=M+rho; inv=M+M*M/rho; f=rho*rho/r**2
    tort=rho+2*M*s.log(rho/M)-M*M/rho
    chi=Q*(s.log(rho/M)-M/rho)
    chi_inv=chi.subs(rho,M*M/rho)
    check(s.diff(tort,rho)-1/f,'tortoise derivative')
    check(s.diff(chi,rho)-Q/(r*f),'ingoing/outgoing gauge derivative')
    check(s.expand_log(chi_inv-chi+Q/M*tort,force=True),'regular EF inversion phase cancellation')
    z=rho/(M*r)
    check(s.diff(z,rho)-1/r**2,'compactified inverse radius derivative')
    hat=s.Function('hat')
    derivative=-s.diff(hat(z)/r,rho)
    zz=s.symbols('zz',real=True)
    expected=hat(z)/r**2-s.Subs(s.diff(hat(zz),zz),zz,z)/r**3
    check(derivative-expected,'regular transverse chain rule')
    F,Z=s.symbols('F Z')
    trace=s.limit(-s.diff((F+Z*z)/r,rho),rho,0)
    check(trace-F/M**2+Z/M**3,'horizon area-normalized transverse coefficient')
    vv=s.symbols('vv',real=True); Fv=s.Function('Fv')(vv)
    omegaH=e*Q/M; phase=s.exp(-s.I*omegaH*vv)
    check(s.diff(phase*Fv,vv)+s.I*omegaH*phase*Fv-phase*s.diff(Fv,vv),
          'horizon gauge frequency cancellation')
    sigma=s.symbols('sigma',real=True)
    lhs=inv**sigma*rho**2/M**2
    rhs=M**(sigma-2)*r**sigma*rho**(2-sigma)
    check(s.powsimp(s.expand_power_base(lhs/rhs,force=True),force=True)-1,'exact radial weight Jacobian')
    rho0=s.symbols('rho0',positive=True)
    finite=s.integrate(rho**s.Rational(1,2)*(s.Rational(3,4)*rho**(-s.Rational(1,4)))**2,(rho,0,rho0))
    check(finite-s.Rational(9,16)*rho0,'degenerate weighted norm does not bound derivative')
    # Exact outgoing EF divergence operator, derived independently from metric fluxes.
    u=s.symbols('u',real=True)
    psi=s.Function('psi')(u,R); qB=s.Function('qB')(u); mass=s.Function('mass')(u)
    c2=s.Function('c2')(u); a2=s.Function('a2')(u)
    C=1-2*mass/R+c2/R**2; Au=qB/R+a2/R**2
    Du=lambda value:s.diff(value,u)+s.I*e*Au*value
    scalar=psi/R
    operator=(Du(-R**2*s.diff(scalar,R))+s.diff(-R**2*Du(scalar)+R**2*C*s.diff(scalar,R),R))/R
    claimed=-2*s.diff(psi,u,R)+C*s.diff(psi,R,2)+(s.diff(C,R)-2*s.I*e*Au)*s.diff(psi,R)
    claimed-= (s.I*e*s.diff(Au,R)+s.diff(C,R)/R)*psi
    check(operator-claimed,'outgoing EF reduced wave operator')
    FF=s.Function('F')(u); ZZ=s.Function('Z')(u); YY=s.Function('Y')(u)
    jet=FF+ZZ/R+YY/R**2
    jetop=operator.subs(psi,jet).doit()
    coefficient=s.limit(R**2*jetop,R,s.oo)
    check(coefficient-2*s.diff(ZZ,u)-s.I*e*qB*FF,'Bondi first-jet transport')
    time=s.symbols('time',positive=True)
    alpha=s.Rational(1,2); beta=s.Rational(2)
    tail=time**(-alpha+s.I*beta)
    primitive=-s.I*e*Q*time**(1-alpha+s.I*beta)/(2*(1-alpha+s.I*beta))
    check(s.diff(primitive,time)+s.I*e*Q*tail/2,'slow-tail jet growth coefficient')
    # Exact radiation pulse algebra; polynomial bump is a finite integral control only.
    v,omega=s.symbols('v omega',real=True)
    bump=(1-v*v)**4
    H=bump*s.exp(s.I*omega*v)
    pulse=s.diff(H,v); pulsed=s.diff(pulse,v)
    j=s.simplify(s.im(s.expand_complex(pulse*s.conjugate(pulsed))))
    formula=omega*bump*s.diff(bump,v,2)-2*omega*s.diff(bump,v)**2-omega**3*bump**2
    check(j-formula,'pulse charged flux density')
    check(H.subs(v,1)-H.subs(v,-1),'zero unweighted pulse moment')
    charged=s.integrate(j,(v,-1,1))
    rhsflux=-3*omega*s.integrate(s.diff(bump,v)**2,(v,-1,1))-omega**3*s.integrate(bump*bump,(v,-1,1))
    check(charged-rhsflux,'pulse charge after integration by parts')
    charge_control=s.simplify(-s.Rational(3,5)*charged.subs(omega,1))
    if charge_control<=0:
        raise ArithmeticError('zero pulse moment wrongly forced zero charge')
    energy=s.integrate(s.simplify(s.expand_complex(pulsed*s.conjugate(pulsed))).subs(omega,1),(v,-1,1))
    Qi,I0,J0,dq=s.symbols('Qi I0 J0 dq')
    total=(Qi*I0+J0)-((Qi+dq)*I0+J0)
    check(total.subs(I0,0),'paired pulses cancel charge-weighted moment')
    root=Path(__file__).resolve().parent
    names=['verify_regular_ef_inversion.py','REGULAR_EF_INVERSION_AND_TRANSVERSE_GATE.md',
           'OUTGOING_NULL_INFINITY.md','TWO_PULSE_SECOND_JET.md','../../definitions/MODEL.md']
    report=dict(claim_ids=['E01.1','E01.2','E01.3','E01.4','E01.5'],
                logic='PROVED (checked finite algebra, weights and boundary-ODE compatibility only)',
                evidence='EXACT_ALGEBRA',audit='INTERNAL_AUDIT',sympy_version=s.__version__,
                checks=['EF gauge and inversion phase','transverse horizon coefficient','radial weight Jacobian',
                        'degenerate norm countercontrol','outgoing EF wave divergence and first jet',
                        'zero pulse moment with nonzero charge','paired charge-weighted cancellation'],
                pulse_control=dict(shape='(1-v^2)^4 inside [-1,1]; finite regularity control, not C-infinity certificate',
                                   charge_per_pulse=str(charge_control),mass_loss_per_pulse=str(energy),
                                   coupling='3/5',frequency=1),
                actual_scattering_realization=False,nonlinear_inversion_verified=False,
                actual_horizon_identity_verified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'REGULAR_EF_INVERSION_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: regular EF, transverse/weight maps and charge-compatible moment screen; center/scattering realization OPEN')


if __name__=='__main__':
    main()
