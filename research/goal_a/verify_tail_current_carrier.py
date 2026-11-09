"""CARRIER07 exact actual wave/current kernels and scoped tail controls, not a decay proof."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def zero(expr,label):
    if s.simplify(s.expand(expr))!=0:
        raise ArithmeticError(label)


def main():
    u=s.symbols('u',real=True,nonnegative=True)
    r,U=s.symbols('r U',positive=True,real=True)
    Omega=s.symbols('Omega',real=True,nonzero=True)
    C,e=s.symbols('C e',positive=True,real=True)
    norm=lambda v:s.expand(v*s.conjugate(v))
    F=C*s.exp(-s.I*Omega*u)/(1+u)
    Fp=s.diff(F,u)
    energy=C*C*(Omega**2/(1+u)**2+1/(1+u)**4)
    current=Omega*C*C/(1+u)**2
    zero(norm(Fp)-energy,'carrier ordinary radiation energy')
    zero(s.im(F*s.conjugate(Fp))-current,'carrier charge current is integrable')
    zero(Fp+s.I*Omega*F+C*s.exp(-s.I*Omega*u)/(1+u)**2,
         'demodulated derivative differs from ordinary derivative')
    if s.simplify(Fp+C*s.exp(-s.I*Omega*u)/(1+u)**2)==0:
        raise ArithmeticError('discarding nonzero carrier frequency was not rejected')
    Mf,Qf=s.symbols('Mf Qf',real=True)
    MB=Mf+C*C*(Omega**2/(1+u)+1/(3*(1+u)**3))
    QB=Qf+e*Omega*C*C/(1+u)
    zero(s.diff(MB,u)+energy,'exact carrier Bondi mass balance')
    zero(s.diff(QB,u)+e*current,'exact carrier Bondi charge balance')
    sigma=s.symbols('sigma',positive=True)
    zero(s.diff(U**sigma/sigma,U)-U**(sigma-1),'positive weighted carrier divergent primitive')
    zero(s.diff(s.log(U),U)-1/U,'critical weighted carrier logarithmic primitive')
    # Independently reconstruct the actual W_r identity from the complete wave operator.
    psi=s.Function('psi')(u,r); aa=s.Function('a',real=True)(u,r); cc=s.Function('c',real=True)(u,r)
    W=s.diff(psi,u)+s.I*e*aa*psi-cc*s.diff(psi,r)/2
    wave=(-2*s.diff(psi,u,r)+s.diff(cc*s.diff(psi,r),r)
          -2*s.I*e*aa*s.diff(psi,r)-(s.I*e*s.diff(aa,r)+s.diff(cc,r)/r)*psi)
    coeff=s.I*e*s.diff(aa,r)/2-s.diff(cc,r)/(2*r)
    zero(2*(s.diff(W,r)-coeff*psi)+wave,'actual complete reduced wave gives radial W kernel')
    # Exact radial kernel and amplitude cancellation, valid at all U/r.
    kernel=2*(s.sqrt(1+U/r)-1)/U
    zero(s.diff(kernel,r)+1/(r*r*s.sqrt(1+U/r)),'exact two-scale radial integral')
    assert s.limit(kernel,r,s.oo)==0
    profile=1/s.sqrt(1+U/r)
    zero(profile*(s.sqrt(1+U/r)-1)-(1-profile),'amplitude cancels radial square-root growth')
    if s.simplify(kernel-1/r)==0:
        raise ArithmeticError('discarding two-scale kernel structure was not rejected')
    # Actual characteristic reduced current has no radius-only imaginary contribution.
    pr,pi,wr,wi,c=s.symbols('pr pi wr wi c',real=True)
    phi=pr+s.I*pi; Nphi=wr+s.I*wi
    zero(s.im((r*phi)*s.conjugate(r*Nphi-c*phi/2))-r*r*s.im(phi*s.conjugate(Nphi)),
         'actual reduced characteristic Maxwell current')
    h=s.symbols('h',positive=True)
    zero(s.diff(U**(-h)/h,U)+U**(-1-h),'integrable current and mass tail primitive')
    eta=s.symbols('eta',nonnegative=True)
    zero((-1-(s.Rational(1,2)-2*eta))-(-s.Rational(3,2)+2*eta),
         'charge-current time exponent')
    zero((-1-(1-2*eta))-(-2+2*eta),'mass and radial-current time exponent')
    # Potential bound integrates the full b-1 error, rather than setting b=1.
    sr=s.symbols('sr',positive=True)
    Delta,M,Q0=s.symbols('Delta M Q0',positive=True)
    pot=s.integrate(Delta/sr**2+4*M*Q0/sr**3,(sr,r,s.oo))
    zero(pot-Delta/r-2*M*Q0/r**2,'actual potential comparison retains optical error')
    root=Path(__file__).resolve().parent
    receipt=json.loads((root/'RN_TAIL_PRIMARY_RECEIPT_2026-10-23_R15.json').read_text(encoding='utf-8'))
    assert receipt['source_url']=='https://arxiv.org/html/2603.28861v1'
    assert any(n['element_id']=='S4.I1.i3.p1' and n['math_count']>0 for n in receipt['selected_nodes'])
    names=['verify_tail_current_carrier.py','TAIL_CURRENT_AND_CARRIER_AUDIT.md',
           'RN_TAIL_PRIMARY_RECEIPT_2026-10-23_R15.json',
           'MELLIN_INNER_TRANSFER_AND_CHARGE_BOOTSTRAP.md','ACTUAL_BONDI_COMPLETENESS_BRIDGE.md',
           'LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md','GLOBAL_RN_SOURCE_NORM_AUDIT.md',
           '../../definitions/MODEL.md','ACCEPTANCE.md']
    report=dict(claim_ids=[f'CARRIER07.{i}' for i in range(1,7)],
                logic='PROVED for exact kernel/current and scoped carrier controls; actual uniform A_eta/D_eta and terminal-charge application CONDITIONAL',
                evidence=['EXACT_ALGEBRA','BOUNDARY_ODE_CARRIER_COUNTERCONTROL','PRIMARY_SOURCE_AUDIT'],
                audit='INTERNAL_AUDIT',
                checks=['ordinary and demodulated carrier derivatives',
                        'exact carrier mass and charge Bondi balance',
                        'divergent positive/critical weighted radiation primitives',
                        'independent actual W_r wave identity',
                        'exact two-scale radial kernel and amplitude-current cancellation',
                        'actual characteristic charge current',
                        'integrable current/mass tail powers and full optical potential error',
                        'primary-read receipt identifies precise official radiation-derivative clause'],
                negative_controls=['omitting the carrier in an ordinary derivative leaves a nonzero residual',
                                   'ordinary weighted radiation budget diverges while carrier charge current is integrable',
                                   'replacing the exact two-scale kernel by its fixed-U/r approximation is not an identity'],
                boundary_countercontrol_is_actual_EMCSF_solution=False,
                original_INNER06_conditional_theorems_invalidated=False,
                generic_extremal_RN_decay_automatically_pays_B_sigma=False,
                actual_uniform_A_eta_D_eta_verified=False,actual_Coulomb_potential_bootstrap_closed=False,
                late_charge_limit_verified=False,horizon_parameter_agreement_verified=False,
                RN_convergence_verified=False,goal_A_proved=False,
                primary_source_receipt='RN_TAIL_PRIMARY_RECEIPT_2026-10-23_R15.json',
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'TAIL_CURRENT_CARRIER_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: CARRIER07 exact actual radial/current kernels and carrier Bondi countercontrols; primary scope audited; actual A/D decay/Goal A OPEN')


if __name__=='__main__':
    main()
