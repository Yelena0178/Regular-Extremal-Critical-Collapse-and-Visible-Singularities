"""LOW05 exact source/scaling identities and finite RN ODE controls, not PDE certification."""
from hashlib import sha256
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import sympy as s


def zero(expr,label):
    if s.simplify(s.expand(expr))!=0:
        raise ArithmeticError(label)


def main():
    u,r=s.symbols('u r',real=True,positive=True)
    e,Q=s.symbols('e Q',real=True)
    f=s.Function('f',real=True)(r)
    dc=s.Function('dc',real=True)(u,r); da=s.Function('da',real=True)(u,r)
    psi=s.Function('psi')(u,r)
    def L(c,a):
        return (-2*s.diff(psi,u,r)+s.diff(c*s.diff(psi,r),r)
                -2*s.I*e*a*s.diff(psi,r)-(s.I*e*s.diff(a,r)+s.diff(c,r)/r)*psi)
    F1=-dc*(s.diff(psi,r)-psi/r)+s.I*e*da*psi
    F0=-dc*s.diff(psi,r)/r+dc*psi/r**2+s.I*e*da*s.diff(psi,r)
    zero(L(f,Q/r)-L(f+dc,Q/r+da)-s.diff(F1,r)-F0,
         'actual time-varying coefficient error is first-order divergence source')
    if s.simplify(L(f,Q/r)-L(f+dc,Q/r+da)-s.diff(F1-s.I*e*da*psi,r)-F0)==0:
        raise ArithmeticError('missing electric divergence source not rejected')
    eta=s.Function('eta')(u)
    original=L(f+dc,Q/r+da)
    cutoff=original.xreplace({psi:eta*psi}).doit()
    zero(cutoff-eta*original+2*s.diff(eta,u)*s.diff(psi,r),
         'actual null-time cutoff retains terminal source')
    rho,omega,M,qq=s.symbols('rho omega M qq',positive=True)
    QQ=s.symbols('QQ',real=True)
    ff=1-2*M*omega/rho+QQ**2*omega**2/rho**2
    RR=s.Function('R')(rho)
    scaled=(s.diff(ff*s.diff(RR,rho),rho)
            +((1-qq/rho)**2/ff-s.diff(ff,rho)/rho)*RR)
    static=omega**2*ff**2*s.diff(RR,rho,2)+omega**2*ff*s.diff(ff,rho)*s.diff(RR,rho)
    static+=(omega**2*(1-qq/rho)**2-omega**2*ff*s.diff(ff,rho)/rho)*RR
    zero(static-omega**2*ff*scaled,'full RN scaled Sturm equation')
    # Divergence forcing is absorbed into momentum, not differentiated in the norm.
    x=s.symbols('x',real=True)
    RX=s.Function('RX')(x); G1=s.Function('G1')(x); G0=s.Function('G0')(x); V=s.Function('V')(x)
    P=s.diff(RX,x)-G1
    zero(s.diff(P,x)+V*RX-G0-(s.diff(RX,x,2)+V*RX-s.diff(G1,x)-G0),
         'modified momentum source has no derivative of G1')
    # Complete reference radial phase in the transformed source.
    kk,fp=s.symbols('kk fp',real=True,nonzero=True)
    theta_r=-kk/fp; Fv,Fvr,Fz=s.symbols('Fv Fvr Fz')
    zero(fp*(Fvr+Fz)-(fp*(Fvr-s.I*theta_r*Fv)+fp*Fz-s.I*kk*Fv),
         'source phase transformation includes minus i k G1')
    if s.simplify(fp*(Fvr+Fz)-(fp*(Fvr-s.I*theta_r*Fv)+fp*Fz))==0:
        raise ArithmeticError('missing phase source correction not rejected')
    # Adiabatic amplitudes and non-positive-frequency reference energy identity.
    kval,kx,U,theta=s.symbols('kval kx U theta',real=True,positive=True)
    ar,ai,br,bi=s.symbols('ar ai br bi',real=True)
    Ap=ar+s.I*ai; Am=br+s.I*bi
    Rv=(s.exp(s.I*theta)*Ap+s.exp(-s.I*theta)*Am)/s.sqrt(kval)
    Pv=s.I*s.sqrt(kval)*(s.exp(s.I*theta)*Ap-s.exp(-s.I*theta)*Am)
    Rxx=-(kval**2-U)*Rv
    Bp=s.sqrt(kval)*Rv-s.I*Pv/s.sqrt(kval)
    Bpx=kx*Rv/(2*s.sqrt(kval))+s.sqrt(kval)*Pv-s.I*Rxx/s.sqrt(kval)+s.I*Pv*kx/(2*kval**s.Rational(3,2))
    Ap_deriv=s.exp(-s.I*theta)*(Bpx-s.I*kval*Bp)/2
    Ap_expected=-s.I*U*Ap/(2*kval)+(kx/(2*kval)-s.I*U/(2*kval))*s.exp(-2*s.I*theta)*Am
    zero(Ap_deriv-Ap_expected,'exact outward adiabatic amplitude matrix')
    zero(s.im(s.conjugate(Rv)*Pv)-(ar*ar+ai*ai-br*br-bi*bi),'signed flux in adiabatic amplitudes')
    norm=lambda z:s.expand(z*s.conjugate(z))
    zero(norm(Pv)+kval**2*norm(Rv)-2*kval*(norm(Ap)+norm(Am)),
         'adiabatic amplitude energy normalization')
    # Actual forced asymptotic-model profile, with zero anchor value and derivative.
    qa=s.Rational(3,5); ra=qa/2; rb=2*qa
    forced_profile=(rho-ra)**2
    forcing=s.diff(forced_profile,rho,2)+(1-qa/rho)**2*forced_profile
    assert forced_profile.subs(rho,ra)==0 and s.diff(forced_profile,rho).subs(rho,ra)==0
    KE=s.integrate((s.diff(forced_profile,rho)**2+forced_profile**2)/rho,(rho,ra,rb))
    HC=s.integrate(rho*forcing**2,(rho,ra,rb))
    HW=s.integrate(forcing**2/rho,(rho,ra,rb))
    assert all(float(v)>0 for v in [KE,HC,HW])
    # r=rho/omega and H=omega^2*forcing determine these factors exactly.
    scaled_energy=omega**2*KE; correct_G0=omega**2*HC; wrong_G0=omega**4*HW
    zero(scaled_energy/correct_G0-KE/HC,'natural nondivergence source scaling')
    zero(scaled_energy/wrong_G0-omega**-2*KE/HW,'wrong source weight loses two low-frequency powers')
    # Real time coefficient moves an input outside the critical band into it.
    ts=s.symbols('ts',real=True)
    mixed=s.integrate(s.cos(2*ts)*s.exp(3*s.I*ts)*s.exp(-s.I*ts),(ts,0,2*s.pi))/(2*s.pi)
    pure=s.integrate(s.exp(3*s.I*ts)*s.exp(-s.I*ts),(ts,0,2*s.pi))/(2*s.pi)
    zero(mixed-s.Rational(1,2),'real coefficient generates lower output frequency')
    zero(pure,'input has zero lower-frequency projection')
    # Finite RN fundamental-matrix controls, not a certificate of an omega limit.
    q=.6; mass=charge=1.; aa=q/2; bb=2*q
    Cq=2+5/(8*aa*aa); controls=[]
    for w in [.02,.01,.005]:
        def ode(z,y):
            fv=1-2*mass*w/z+charge*charge*w*w/(z*z)
            fz=2*mass*w/(z*z)-2*charge*charge*w*w/(z**3)
            mat=np.array([[0,1/fv],[-((1-q/z)**2/fv-fz/z),0.]])
            return (mat@y.reshape(2,2)).ravel()
        sol=solve_ivp(ode,(aa,bb),np.eye(2).ravel(),rtol=2e-12,atol=2e-13,max_step=.002,dense_output=True)
        if not sol.success: raise ArithmeticError(sol.message)
        mats=sol.sol(np.linspace(aa,bb,301)).T.reshape(-1,2,2)
        determinants=np.linalg.det(mats)
        state=mats@np.array([1.,1.j])
        signed=np.imag(np.conjugate(state[:,0])*state[:,1])
        energies=np.sum(np.abs(state)**2,axis=1)
        det_error=float(np.max(np.abs(determinants-1)))
        flux_error=float(np.max(np.abs(signed-1)))
        if det_error>2e-9 or flux_error>2e-9 or np.min(energies)<2-2e-9:
            raise ArithmeticError('finite RN transfer flux control')
        if np.max(energies)>2*math.exp(2*Cq*(bb-aa)):
            raise ArithmeticError('uniform analytic transfer envelope')
        controls.append(dict(omega=w,scaled_interval=[aa,bb],determinant_error=det_error,
                             scaled_signed_flux_error=flux_error,scaled_energy_min=float(np.min(energies)),
                             scaled_energy_max=float(np.max(energies))))
    root=Path(__file__).resolve().parent
    names=['verify_low_frequency_shell.py','LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md',
           'COULOMB_RENORMALIZATION_AND_MELLIN_GATE.md','FAR_ZONE_RP_AND_COULOMB_BALANCE.md',
           'ACTUAL_BONDI_COMPLETENESS_BRIDGE.md','GLOBAL_RN_SOURCE_NORM_AUDIT.md',
           '../../definitions/MODEL.md','ACCEPTANCE.md']
    report=dict(claim_ids=[f'LOW05.{i}' for i in range(1,6)],
                logic='PROVED for listed exact identities and scoped controls; uniform estimates, Jost existence and Parseval argument are analytic',
                evidence=['EXACT_ALGEBRA','EXACT_SCALING_COUNTERCONTROL','FINITE_FIXED_RN_ODE_CONTROLS'],
                audit='INTERNAL_AUDIT',
                checks=['actual dynamic coefficient divergence source with no coefficient time derivatives',
                        'null-time cutoff source', 'full RN scaled Sturm operator',
                        'modified momentum removes derivative of divergence source',
                        'complete reference source phase',
                        'adiabatic amplitude matrix, energy and signed flux',
                        'source-weight low-frequency scaling and real-coefficient band mixing',
                        'three finite RN matrix determinant and signed-flux controls'],
                negative_controls=['omitted electric divergence term leaves nonzero residual',
                                   'omitted reference phase source correction leaves nonzero residual',
                                   'wrong G0 source weight creates omega^-2 ratio',
                                   'time-dependent real multiplication does not preserve critical band'],
                finite_RN_controls=controls,
                forced_model_control={n:str(v) for n,v in dict(scaled_energy_coefficient=KE,
                                      correct_source_coefficient=HC,wrong_source_coefficient=HW).items()},
                analytic_scope='fixed-q uniform finite shell and reference outer mode; actual divergence/source bound and finite cutoff inequality under explicit Coulomb potential hypothesis',
                actual_Coulomb_potential_bootstrap_verified=False,other_frequency_regions_closed=False,
                global_RN_inverse_Wronskian_bound_verified=False,
                actual_weighted_radiation_flux_verified=False,late_charge_limit_verified=False,
                RN_convergence_verified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'LOW_FREQUENCY_SHELL_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: LOW05 exact actual/source and RN scaling/amplitude identities; three finite RN transfer controls; Coulomb/global closure/Goal A OPEN')


if __name__=='__main__':
    main()
