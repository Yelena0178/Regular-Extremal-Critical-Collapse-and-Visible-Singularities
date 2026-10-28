"""Exact BON01 radial cancellations and nonlinear constraint propagation, not numerical PDE existence."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def check(expr,label):
    if s.simplify(s.expand(expr))!=0:
        raise ArithmeticError(label)


def main():
    z,B,m,Q,e,a,mu,Qu=s.symbols('z B m Q e a mu Qu',real=True,nonzero=True)
    pr,pi,wr,wi,vr,vi,hr,hi=s.symbols('pr pi wr wi vr vi hr hi',real=True)
    psi=pr+s.I*pi; w=wr+s.I*wi; W=vr+s.I*vi; Hz=hr+s.I*hi
    H=psi+z*w; H2=s.expand(H*s.conjugate(H)); W2=s.expand(W*s.conjugate(W))
    f=1-2*m*z; C=B*f
    Bz=-z*B*H2; mz=-(Q*Q+f*H2)/2
    fz=-2*m-2*z*mz; Cz=B*(-2*m+z*Q*Q); az=B*Q
    check(Bz*f+B*fz-Cz,'radial C_z cancellation')
    Wz=-z*(C*Hz+Cz*H)/2+s.I*e*az*psi/2
    psiu=W-s.I*e*a*psi
    wu=Wz-s.I*e*az*psi-s.I*e*a*w
    wz=(Hz-2*w)/z
    wave=2*wu+C*z*z*wz+(2*C*z+z*z*Cz+2*s.I*e*a)*w+(s.I*e*az+z*Cz)*psi
    check(wave,'regular compactified wave transport')
    Qz=e*s.im(psi*s.conjugate(w)); Qzz=e*s.im(psi*s.conjugate(wz))
    Quz=e*s.im(psiu*s.conjugate(w)+psi*s.conjugate(wu))
    EQz=Quz+(Cz*z*z+2*C*z)*Qz+C*z*z*Qzz+e*s.im(w*s.conjugate(W)+psi*s.conjugate(Wz))
    check(EQz,'Maxwell remaining constraint propagation')
    covHu=W-C*z*z*Hz/2-z*z*Cz*H/2-s.I*e*z*az*psi/2
    muz=-Q*Qu+z*mu*H2-f*s.re(H*s.conjugate(covHu))
    Em=mu+W2/B+z*f*s.re(W*s.conjugate(H))
    Emz=muz-Bz/B**2*W2+2/B*s.re(Wz*s.conjugate(W))
    Emz+=(f+z*fz)*s.re(W*s.conjugate(H))+z*f*(s.re(Wz*s.conjugate(H))+s.re(W*s.conjugate(Hz)))
    EQ=Qu+C*z*z*Qz+e*s.im(psi*s.conjugate(W))
    check(Emz-z*H2*Em+Q*EQ,'Einstein mass constraint propagation')
    if s.simplify(s.expand(Emz-z*H2*Em))==0:
        raise ArithmeticError('Maxwell residual incorrectly discarded from mass propagation')
    # Explicit initial zero-scalar RN tail solves all radial equations.
    M0,Q0=s.symbols('M0 Q0',real=True)
    rn_m=M0-Q0**2*z/2
    check(s.diff(rn_m,z)+Q0**2/2,'initial RN tail mass')
    check((1-2*rn_m*z)-(1-2*M0*z+Q0**2*z*z),'initial RN tail f')
    # Induced polar Cauchy slice u'=-1/C, with the actual u constraints used.
    mu_on_shell=-W2/B-z*f*s.re(W*s.conjugate(H))
    Qu_on_shell=-C*z*z*Qz-e*s.im(psi*s.conjugate(W))
    m_slice=-z*z*mz-mu_on_shell/C
    q_slice=-z*z*Qz-Qu_on_shell/C
    free_phi=z*psi; free_chi=z*W/C
    free_derivative=-z*z*H-z*W/C
    check(q_slice-e/z**2*s.im(free_phi*s.conjugate(free_chi)),'Cauchy exterior Gauss constraint')
    norm=lambda value:s.expand(value*s.conjugate(value))
    check(m_slice-Q**2*z*z/2-f/(2*z*z)*(norm(free_chi)+norm(free_derivative)),
          'Cauchy exterior Hamiltonian constraint')
    check(-B*C*(-1/C)**2-2*B*(-1/C)-1/f,'spacelike induced metric')
    root=Path(__file__).resolve().parent
    names=['verify_finite_bondi_constraints.py','FINITE_BONDI_EXTERIOR_REALIZATION.md','../../definitions/MODEL.md']
    report=dict(claim_ids=['BON01.1','BON01.2','BON01.4'],
                logic='PROVED (finite identities only; analytic existence theorem separate)',
                evidence='EXACT_ALGEBRA',audit='INTERNAL_AUDIT',sympy_version=s.__version__,
                checks=['radial cancellation removes w_z from C_z','regular compactified wave',
                        'remaining Maxwell constraint','remaining Einstein mass constraint',
                        'initial exact RN tail','induced Cauchy exterior metric, Gauss and Hamiltonian constraints'],
                negative_controls=['mass constraint retains Maxwell residual'],
                analytic_existence_source='FINITE_BONDI_EXTERIOR_REALIZATION.md, BON01.3',
                numerical_PDE_existence_certified=False,regular_center_Cauchy_matching_verified=False,
                full_future_fixed_radius_verified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'FINITE_BONDI_CONSTRAINT_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: compactified nonlinear constraints and propagation; finite-window analytic theorem separate, Goal A OPEN')


if __name__=='__main__':
    main()
