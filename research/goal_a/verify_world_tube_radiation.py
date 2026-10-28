"""TRACE09 exact boundary/Green identities and finite model-root controls, not Goal A."""
from hashlib import sha256
import json
from pathlib import Path
import mpmath as mp
import sympy as s


def zero(expr,label):
    if s.simplify(s.expand(expr))!=0:
        raise ArithmeticError(label)


def main():
    U,R=s.symbols('U R',positive=True)
    shape=(s.sqrt(1+U/R)-1)/s.sqrt(U)
    zero(shape-s.sqrt(U/R)/(s.sqrt(1+U/R)+1)/s.sqrt(R),
         'worldtube correction rationalized kernel')
    zero(s.limit(shape,U,s.oo)-1/s.sqrt(R),'worldtube correction uniform limiting constant')
    x=s.symbols('x',real=True)
    v=s.Function('v')(x); y=s.Function('y')(x); pot=s.Function('V')(x)
    g1=s.Function('G1')(x); g0=s.Function('G0')(x)
    J=v*s.diff(y,x)-(s.diff(v,x)-g1)*y
    residual=s.diff(J,x)-(s.diff(y,x)*g1-y*g0)
    residual=residual.subs(s.diff(v,x,2),-pot*v+s.diff(g1,x)+g0).subs(s.diff(y,x,2),-pot*y)
    zero(residual,'complete modified-momentum Green flux derivative')
    theta=s.Function('theta',real=True)(x); f=s.Function('f',real=True)(x)
    F1=s.Function('F1')(x); F0=s.Function('F0')(x)
    G1=s.exp(s.I*theta)*F1
    G0=f*s.exp(s.I*theta)*F0-s.I*s.diff(theta,x)*G1
    Ybar=s.exp(s.I*theta)*y
    zero(s.diff(y,x)*G1-y*G0-(s.diff(Ybar,x)*F1-f*Ybar*F0),
         'retarded radiation kernel cancellation retains phase source')
    # Neutral flat exact control: two individually logarithmic terms cancel.
    omega=s.symbols('omega',real=True,nonzero=True)
    ym=s.exp(-s.I*omega*x); gp=s.exp(s.I*omega*x)/x; gz=-s.I*omega*gp
    zero(s.diff(ym,x)*gp-ym*gz,'separated 1/x radiation-source terms cancel exactly')
    if s.simplify(s.diff(ym,x)*gp)==0: raise ArithmeticError('omitted phase correction negative control')
    r,u=s.symbols('r u',positive=True,real=True)
    e=s.symbols('e',real=True)
    psi=s.Function('psi')(u,r); zz=s.Function('zeta',real=True)(u)
    cc=s.Function('c',real=True)(u,r); aa=s.Function('a',real=True)(u,r); ff=s.Function('f0',real=True)(r)
    Phi=zz*psi
    Du=lambda z:s.diff(z,u)+s.I*e*aa*z
    W=Du(psi)-cc*s.diff(psi,r)/2
    WPhi=Du(Phi)-cc*s.diff(Phi,r)/2
    zero(WPhi-zz*W-s.diff(zz,u)*psi,'full actual worldtube cutoff derivative')
    pphys=cc*s.diff(Phi,r)-Du(Phi)-(cc-ff)*Phi/r
    zero(pphys-(Du(Phi)-2*zz*W-2*s.diff(zz,u)*psi-(cc-ff)*Phi/r),
         'physical boundary modified momentum uses full trace pair')
    # Exact late-cutoff radial integral of the already proved Z envelope.
    primitive=2*(1-s.sqrt(r/(r+U)))/U
    zero(s.diff(primitive,r)+r**(-s.Rational(1,2))*(r+U)**(-s.Rational(3,2)),
         'radial total variation controlling late cutoff')
    assert s.limit(primitive,r,s.oo)==0
    lam,b,C1,C0=s.symbols('lam b C1 C0',positive=True)
    rb=b/lam
    outside=(C1/(2*lam*rb**2)+C0/rb)/(2*lam)
    zero(outside-C1/(4*b*b)-C0/(2*b),'no additional low-frequency loss in outer source')
    # Whittaker variable transformation, independently checking the sign of kappa.
    q,z=s.symbols('q z',positive=True)
    transformed=((omega-q/r)**2/(-4*omega**2)).subs(r,z/(-2*s.I*omega))
    zero(transformed-(-s.Rational(1,4)-s.I*q/z+q*q/z**2),'external Coulomb Whittaker parameters')
    # Finite complex-root controls only. Existence of an infinite family uses Rouche.
    mp.mp.dps=80
    qn=mp.mpf(3)/5; beta=mp.sqrt(qn*qn-mp.mpf(1)/4)
    Ap=mp.gamma(-2j*beta)/mp.gamma(mp.mpf('.5')-1j*beta+1j*qn)
    Am=mp.gamma(2j*beta)/mp.gamma(mp.mpf('.5')+1j*beta+1j*qn)
    rho=abs(Am/Ap)
    gamma_ratio=mp.sqrt(mp.cosh(mp.pi*(qn+beta))/mp.cosh(mp.pi*(qn-beta)))
    if abs(rho/gamma_ratio-1)>mp.mpf('1e-70'): raise ArithmeticError('gamma modulus coefficient ratio')
    angle=-mp.log(rho)/(2*beta)
    if not -mp.pi/2<angle<0: raise ArithmeticError('upper-half-plane root angle')
    controls=[]
    for n in [-1,-2,-3]:
        ll0=(mp.arg(-Am/Ap)+2*mp.pi*n)/(2*beta)+1j*angle
        fun=lambda ll:mp.whitw(-1j*qn,1j*beta,mp.exp(ll))/mp.exp(ll/2)
        ll=mp.findroot(fun,(ll0-mp.mpf('.001'),ll0+mp.mpf('.001')),tol=mp.mpf('1e-60'),maxsteps=40)
        zn=mp.exp(ll); wn=1j*zn/2
        resid=abs(fun(ll))
        if mp.im(wn)<=0 or mp.re(wn)<=0 or resid>mp.mpf('1e-55'):
            raise ArithmeticError('finite Coulomb-model root control')
        controls.append(dict(n=n,omega_real=mp.nstr(mp.re(wn),35),omega_imag=mp.nstr(mp.im(wn),35),
                             normalized_residual=mp.nstr(resid,10),
                             relative_asymptotic_correction=mp.nstr(abs(mp.exp(ll-ll0)-1),15)))
    root=Path(__file__).resolve().parent
    receipt=json.loads((root/'DLMF_WHITTAKER_RECEIPT_2026-10-23_R17.json').read_text(encoding='utf-8'))
    assert any(n['equation']=='13.14.33' for n in receipt['sources'])
    names=['verify_world_tube_radiation.py','WORLD_TUBE_RADIATION_TRANSFER.md',
           'DLMF_WHITTAKER_RECEIPT_2026-10-23_R17.json','TAIL_CURRENT_AND_CARRIER_AUDIT.md',
           'MODULATED_BONDI_RADIAL_IMPROVEMENT.md','LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md',
           'MELLIN_INNER_TRANSFER_AND_CHARGE_BOOTSTRAP.md','ACTUAL_BONDI_COMPLETENESS_BRIDGE.md',
           '../../definitions/MODEL.md','ACCEPTANCE.md']
    report=dict(claim_ids=[f'TRACE09.{i}' for i in range(1,7)],
                logic='PROVED for exact identities and scoped controls; outer estimates and Rouche family are analytic, actual A/H/global stability OPEN',
                evidence=['EXACT_ALGEBRA','SPECIAL_FUNCTION_PRIMARY_IDENTITIES','FINITE_COMPLEX_ROOT_CONTROLS'],
                audit='INTERNAL_AUDIT',
                checks=['worldtube radial correction factor',
                        'modified Green flux and complete retarded source cancellation',
                        'physical worldtube momentum with cutoff terms',
                        'late-cutoff radial total variation and outer-source scaling',
                        'external Coulomb Whittaker transformation sign',
                        'Gamma coefficient ratio and three finite complex-root controls'],
                negative_controls=['individual logarithmic source terms cannot replace the combined kernel',
                                   'reflecting external-Coulomb Dirichlet model admits growing modes',
                                   'real-axis self flux does not imply absence of upper-half-plane modes'],
                complex_root_controls=controls,complex_root_controls_are_interval_certificates=False,
                infinite_model_root_family_justification='analytic small-z expansion and Rouche proof in TRACE09.5',
                reflecting_model_is_complete_D001=False,reflecting_model_has_actual_seed_zero_initial_tail=False,
                worldtube_H_tail_verified=False,actual_uniform_A_eta_verified=False,
                future_cutoff_fully_removed=False,global_stability_verified=False,
                horizon_strong_limit_verified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'WORLD_TUBE_RADIATION_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: TRACE09 exact trace/Green/source identities and three finite reflecting-model roots; actual A/H/strong RN/Goal A OPEN')


if __name__=='__main__':
    main()
