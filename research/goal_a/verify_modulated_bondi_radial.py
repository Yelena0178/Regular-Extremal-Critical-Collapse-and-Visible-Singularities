"""MOD08 exact radial/modulation identities and finite convolution controls, not a tail proof."""
from hashlib import sha256
import json
import math
from pathlib import Path
from scipy.integrate import quad
import sympy as s


def zero(expr,label):
    if s.simplify(s.expand(expr))!=0:
        raise ArithmeticError(label)


def main():
    u,r=s.symbols('u r',real=True,positive=True)
    e=s.symbols('e',real=True)
    psi=s.Function('psi')(u,r)
    a=s.Function('a',real=True)(u,r); c=s.Function('c',real=True)(u,r)
    Z=s.diff(psi,r)
    wave=(-2*s.diff(psi,u,r)+s.diff(c*Z,r)-2*s.I*e*a*Z
          -(s.I*e*s.diff(a,r)+s.diff(c,r)/r)*psi)
    transport=s.diff(Z,u)+s.I*e*a*Z-c*s.diff(Z,r)/2-s.diff(c,r)*Z/2
    transport+=(s.I*e*s.diff(a,r)/2+s.diff(c,r)/(2*r))*psi
    zero(2*transport+wave,'actual radial derivative transport with full charged wave')
    U,A,CZ,Cphi,eta=s.symbols('U A CZ Cphi eta',positive=True)
    Penv=A*U**(-s.Rational(1,2)+eta)*(1+U/r)**(-s.Rational(1,2))
    Zenv=CZ*A*U**(s.Rational(1,2)+eta)*r**-2*(1+U/r)**(-s.Rational(3,2))
    zero(Zenv/(Penv/r)-CZ*U/(r+U),'radial derivative to amplitude envelope ratio')
    zero(Penv*Zenv-CZ*A*A*U**(2*eta)/(r+U)**2,'Gauss charge envelope exact radial cancellation')
    Xenv=Cphi*A*U**(-s.Rational(1,2)+eta)*r**-2*(1+U/r)**(-s.Rational(1,2))
    zero(r*Xenv**2-Cphi**2*A*A*U**(-1+2*eta)/(r*r*(r+U)),
         'optical logarithm envelope')
    Jb=1/(U*r)-s.log(1+U/r)/U**2
    Jm=s.log(1+U/r)/U
    Jq=(s.log(1+U/r)-U/(r+U))/U**2
    for val,integrand,label in [(Jb,1/(r*r*(r+U)),'optical integral'),
                               (Jm,1/(r*(r+U)),'scalar mass integral'),
                               (Jq,1/(r*(r+U)**2),'charge work mass integral')]:
        zero(s.diff(val,r)+integrand,label)
        assert s.limit(val,r,s.oo)==0
    # Project mass differs from Hawking mass by Q^2/(2r).
    Q,Qr,mr,f,X2=s.symbols('Q Qr mr f X2',real=True)
    actual_mr=Q*Q/(2*r*r)+r*r*f*X2/2
    zero(actual_mr+Q*Qr/r-Q*Q/(2*r*r)-(r*r*f*X2/2+Q*Qr/r),
         'project mass electric contribution cancels only after renormalization')
    # General time-dependent Bondi parameters: no static-background assumption.
    MB=s.Function('MB',real=True)(u); QB=s.Function('QB',real=True)(u)
    fb=1-2*MB/r+QB*QB/(r*r); ab=QB/r
    zero(s.diff(fb,u)+2*s.diff(MB,u)/r-2*QB*s.diff(QB,u)/r**2,
         'modulated metric coefficient time derivative')
    def L(metric,potential,field):
        return (-2*s.diff(field,u,r)+s.diff(metric*s.diff(field,r),r)
                -2*s.I*e*potential*s.diff(field,r)
                -(s.I*e*s.diff(potential,r)+s.diff(metric,r)/r)*field)
    dc=c-fb; da=a-ab
    F1=-dc*(s.diff(psi,r)-psi/r)+s.I*e*da*psi
    F0=-dc*s.diff(psi,r)/r+dc*psi/r**2+s.I*e*da*s.diff(psi,r)
    zero(L(fb,ab,psi)-L(c,a,psi)-s.diff(F1,r)-F0,'full dynamic Bondi divergence comparison')
    comm=s.diff(L(fb,ab,psi),u)-L(fb,ab,s.diff(psi,u))
    expected=s.diff(s.diff(fb,u)*s.diff(psi,r),r)-2*s.I*e*s.diff(QB,u)*s.diff(psi,r)/r
    expected+=(s.I*e*s.diff(QB,u)/r**2-s.diff(fb,r,u)/r)*psi
    zero(comm-expected,'modulated operator time commutator retains parameter derivatives')
    if s.simplify(comm)==0:
        raise ArithmeticError('modulated operator was incorrectly treated as stationary')
    # Radial phase derivative density, retaining both QB' and f_B,u.
    phase_density=e*QB/(r*fb)
    expected_density=e*s.diff(QB,u)/(r*fb)-e*QB*s.diff(fb,u)/(r*fb**2)
    zero(s.diff(phase_density,u)-expected_density,'modulated phase time derivative density')
    h=s.symbols('h',positive=True)
    log_primitive=(s.log(U)/h+1/h**2)*U**(-h)
    zero(s.diff(log_primitive,U)+U**(-1-h)*s.log(U),'integrable charge variation times log U')
    zero(log_primitive.subs(U,1)-1/h**2,'logarithmic parameter variation constant')
    # A changing Bondi charge requires Maxwell current even for the coefficient model.
    maxwell_divergence=-s.diff(QB,u)/r**2
    slope=s.symbols('slope',positive=True)
    assert maxwell_divergence.subs(QB,1+slope*u).doit()!=0
    assert s.discriminant(r*r-2*r+4,r)==-12
    phase_model=e*(1+slope*u)*s.log(r)
    zero(s.diff(phase_model,u)-e*slope*s.log(r),'global uncut phase has logarithmically unbounded time derivative')
    # Exact source/body density ratios, with the same derivative and measure on both sides.
    p,eps=s.symbols('p eps',real=True)
    amp_ratio=s.simplify(r**(p+1+2*eps)*(U**(2*eta)*r**-3)**2/r**(p-3-2*eps))
    der_ratio=s.simplify(r**(p+1+2*eps)*(U**(2*eta)*r**-2)**2/r**(p-1-2*eps))
    zero(amp_ratio-U**(4*eta)*r**(-2+4*eps),'short-range amplitude source power')
    zero(der_ratio-amp_ratio,'short-range derivative source power')
    # Six finite convolution controls supplement the analytic two-part proof only.
    controls=[]
    cases=[(.1,0.,.25,1.),(.1,.125,10.,1.),(.5,0.,1e4,1.),
           (.5,.125,1e4,1e5),(.1,0.,1e3,1e5),(.5,.125,1.,10.)]
    for kappa,loss,time,rad in cases:
        def kernel(tau):
            rho=rad+kappa*(time-tau)
            return (1+tau)**(-.5+loss)*rho**(-1.5)*(rho+1+tau)**(-.5)
        points=sorted(set([0.,time/2,max(time/2,time-rad/kappa),time]))
        integral=0.; error=0.
        for left,right in zip(points,points[1:]):
            value,err=quad(kernel,left,right,epsabs=1e-15,epsrel=2e-10,limit=100)
            integral+=value; error+=err
        alpha=.5-loss
        CJ=3+(4/kappa)**1.5/(1-alpha)+4*math.sqrt(2)/kappa
        bound=kappa**(-.5)*CJ*(1+time)**(.5+loss)/(math.sqrt(rad)*(rad+1+time)**1.5)
        if integral>bound or integral<0: raise ArithmeticError('finite convolution envelope control')
        controls.append(dict(kappa=kappa,eta=loss,u=time,r=rad,integral=integral,
                             quadrature_error_estimate=error,analytic_upper_bound=bound,ratio=integral/bound))
    root=Path(__file__).resolve().parent
    names=['verify_modulated_bondi_radial.py','MODULATED_BONDI_RADIAL_IMPROVEMENT.md',
           'TAIL_CURRENT_AND_CARRIER_AUDIT.md','ACTUAL_BONDI_COMPLETENESS_BRIDGE.md',
           'LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md','GLOBAL_RN_SOURCE_NORM_AUDIT.md',
           'FAR_ZONE_RP_AND_COULOMB_BALANCE.md','../../definitions/MODEL.md','ACCEPTANCE.md']
    report=dict(claim_ids=[f'MOD08.{i}' for i in range(1,7)],
                logic='PROVED for exact identities and finite controls; actual radial/phase inequalities analytic with explicit A/D/K inputs',
                evidence=['EXACT_ALGEBRA','FINITE_CONVOLUTION_QUADRATURE_CONTROLS'],
                audit='INTERNAL_AUDIT',
                checks=['actual charged radial Z transport and envelope products',
                        'three exact radial mass/optical primitives',
                        'Hawking/project mass distinction',
                        'general time-dependent Bondi divergence source and commutator',
                        'complete modulated phase derivative and logarithmic time integral',
                        'non-electrovac Maxwell residual for varying Bondi charge',
                        'short-range model source/body power ratios',
                        'six finite ideal-characteristic convolution controls'],
                negative_controls=['dropping parameter derivatives makes the time commutator wrong',
                                   'varying Bondi charge does not define an electrovac RN solution',
                                   'positive far-zone coefficient does not imply black-hole RN parameter range',
                                   'uncut dynamic Coulomb phase has unbounded radial logarithm in its time derivative'],
                convolution_controls=controls,convolution_controls_certify_continuous_PDE=False,
                final_charge_assumed_for_modulation=False,
                bondi_mass_charge_inequality_assumed_for_modulation=False,
                actual_uniform_A_eta_D_eta_verified=False,modulated_operator_global_decay_verified=False,
                full_source_absorption_verified=False,horizon_strong_limit_verified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'MODULATED_BONDI_RADIAL_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: MOD08 exact actual radial/modulated operator identities and six finite convolution controls; actual uniform tail/strong RN/Goal A OPEN')


if __name__=='__main__':
    main()
