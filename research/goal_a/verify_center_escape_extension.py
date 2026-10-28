"""ESC01 cone identities, artificial-corner rational budgets and finite ODE controls only."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s
from scipy.integrate import solve_ivp
from scipy.special import betainc


def zero(expr,label):
    if s.simplify(s.expand(expr))!=0:
        raise ArithmeticError(label)


def main():
    r,lam,nu,Q,e,power,current=s.symbols('r lam nu Q e power current',real=True,nonzero=True)
    r_v=lam; lam_v=-r*power
    nu_v=-nu*lam/r-(1-Q*Q/(r*r))/(4*r)
    zero(lam*nu+r*nu_v+(1-Q*Q/r**2)/4,'r nu transport')
    varpi=r/2+2*r*nu*lam+Q*Q/(2*r)
    deriv=s.diff(varpi,r)*r_v+s.diff(varpi,lam)*lam_v+s.diff(varpi,nu)*nu_v+s.diff(varpi,Q)*current
    zero(deriv+2*r*r*nu*power-Q*current/r,'cone mass balance')
    M,ell=s.symbols('M ell',real=True,nonzero=True)
    ff=1-2*M/r+Q*Q/r**2; nurn=-ff/(4*ell)
    zero(s.diff(nurn,r)*ell+ nurn*ell/r+(1-Q*Q/r**2)/(4*r),'RN along-cone nu identity')
    zero((r/2+2*r*nurn*ell+Q*Q/(2*r))-M,'RN along-cone constant mass')
    ar,ai,br,bi,bp=s.symbols('ar ai br bi bp',real=True)
    amp=ar+s.I*ai; P=ar+s.I*ai; field=br+s.I*bi
    zero(s.im(amp*bp*s.conjugate(amp)),'fixed-phase charge vanishes')
    chi=-P/(2*nurn); dphi=P/(2*nurn)
    norm=lambda value:s.expand(value*s.conjugate(value))
    zero(chi-2*ell*P/ff,'small spatial momentum from actual normal')
    zero(r*r*ff*(norm(chi)+norm(dphi))/2-4*r*r*ell*ell*norm(P)/ff,
         'outgoing scalar spatial energy')
    # (rP)_v uses the charged commutator. Om^2=1 and A_v=0.
    pv=s.symbols('pv')
    Fuv=Q/(2*r*r)
    dvP=-nu*pv/r-lam*P/r-s.I*e*Fuv*field/2
    wave=2*dvP+s.I*e*Fuv*field+2*nu*pv/r+2*lam*P/r
    zero(wave,'transverse charged transport from independent D001 wave')
    omitted_commutator=2*dvP+2*nu*pv/r+2*lam*P/r
    if s.simplify(omitted_commutator)==0:
        raise ArithmeticError('charged commutator negative control')
    u=s.symbols('u',real=True)
    B=s.integrate(u**6*(1-u)**6,(u,0,1))
    density=u**6*(1-u)**6/B
    cutoff=1-s.integrate(density,(u,0,u))
    K=s.integrate(density**2,(u,0,1))
    zero(cutoff.subs(u,0)-1,'cutoff start')
    zero(cutoff.subs(u,1),'cutoff end')
    for order in range(1,7):
        zero(s.diff(cutoff,u,order).subs(u,0),'cutoff start flatness')
        zero(s.diff(cutoff,u,order).subs(u,1),'cutoff end flatness')
    samples=[]; length=64.; coupling=.6
    P0=.2+.1j
    for divisor in [64,128,256]:
        delta=s.Rational(1,divisor); rr=1+delta/2
        ll=(1-1/rr)**2/2
        bound=(rr+ll*64)*(delta*delta/s.Integer(20))*K/64
        short_lower=rr*(delta*delta/s.Integer(20))*K*s.Integer(64)
        if not (bound<ll/2):
            raise ArithmeticError('exact rational focusing budget')
        if not short_lower>ll:
            raise ArithmeticError('short-cut loss of positive-lambda control')
        aa=-float(delta)*P0
        def ode(v,y):
            radius,lambda_,nu_,pr,pi,spent=y
            u_=v/length
            cut=1-betainc(7,7,u_)
            cp=-(u_**6*(1-u_)**6)/float(B)/length
            phi=aa*cut; phiv=aa*cp; p=pr+1j*pi
            dp=-lambda_*p/radius-nu_*phiv/radius-1j*coupling*phi/(4*radius**2)
            focus=radius*abs(phiv)**2
            return [lambda_,-focus,-nu_*lambda_/radius-(1-1/radius**2)/(4*radius),
                    dp.real,dp.imag,focus]
        sol=solve_ivp(ode,(0,length),[float(rr),float(ll),-.5,P0.real,P0.imag,0.],
                      rtol=1e-11,atol=1e-14,max_step=.2,dense_output=True)
        if not sol.success: raise ArithmeticError(sol.message)
        rc,lc,nc,pr,pi,spent=sol.y[:,-1]
        if not (lc>float(ll-bound)>float(ll)/2 and nc<0 and rc>1):
            raise ArithmeticError('finite cone sign control')
        if abs(float(ll)-lc-spent)>1e-14 or spent>float(bound):
            raise ArithmeticError('focusing accounting')
        mass=rc/2*(1+4*nc*lc)+1/(2*rc)
        def rn_f(radius): return 1-2*mass/radius+1/radius**2
        cP=rc*(pr+1j*pi)
        p5=cP/5; nu5=-rn_f(5)/(4*lc); chi5=-p5/(2*nu5)
        if rn_f(rc)<=0 or rn_f(4)<=0 or rn_f(5)<=0:
            raise ArithmeticError('RN constraint segment')
        abstract_adm=mass+100*lc**2
        if not 4-2*abstract_adm>1:
            raise ArithmeticError('abstract ADM escape budget')
        samples.append(dict(delta=str(delta),initial_lambda=float(ll),
                            rational_focusing_bound=str(bound),bound_fraction_of_initial=float(bound/ll),
                            short_cut_length='1/64',short_cut_focusing_lower_if_lambda_nonnegative=str(short_lower),
                            short_cut_lower_fraction_of_initial=float(short_lower/ll),
                            spent_focus=float(spent),lambda_after_cut=float(lc),
                            nu_after_cut=float(nc),radius_after_cut=float(rc),M_cone=float(mass),
                            artificial_cut_end_affine_v=length,
                            affine_v_to_r5=float(length+(5-rc)/lc),
                            abs_chi_r5=float(abs(chi5)),abs_chi_r5_over_lambda=float(abs(chi5)/lc),
                            abstract_tail_cost_coefficient=100.,abstract_ADM_bound=float(abstract_adm),
                            escape_margin_r4=float(4-2*abstract_adm)))
    root=Path(__file__).resolve().parent
    names=['verify_center_escape_extension.py','CENTER_ESCAPE_CHARACTERISTIC_EXTENSION.md',
           'AF_REALIZATION_WITH_TRANSVERSE_FLUX.md','MARGINAL_SEED_CAUSAL_INTERFACE.md',
           'CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md','REGULAR_CENTER_BONDI_MATCHING.md',
           'ALTERNATIVE_CHARGED_CANDIDATES.md','EARLY_CHARGED_CONSTRAINT_CERTIFICATE_N2048_2026-10-17.json',
           '../../definitions/MODEL.md',
           '../../reviews/STAGE0_SELF_REVIEW_2026-10-11/verification/sources/literature/1107.0949.txt']
    report=dict(claim_ids=['ESC01.1','ESC01.2','ESC01.3','ESC01.4','ESC01.5','ESC01.6'],
                logic='PROVED for listed identities and rational artificial-corner budget; actual-seed theorem is separate analytic proof',
                evidence=['EXACT_ALGEBRA','EXACT_RATIONAL_ABSTRACT_CONTROL','FINITE_ODE_NUMERICS'],
                audit='INTERNAL_AUDIT',
                checks=['cone Raychaudhuri/mixed/mass identities','RN constraints on one null ray',
                        'charged transverse commutator','spatial-normal energy suppression',
                        'C6 polynomial cutoff endpoint identities','three complex-field artificial-corner budgets'],
                cutoff_control='polynomial C6 only; proof uses C-infinity cutoff',
                cutoff_energy_integral=str(K),samples=samples,
                negative_controls=['bound explicitly compared to O(delta^2) initial lambda',
                                   'short-cut exact focusing lower bound exceeds initial lambda if nonnegative lambda were to persist',
                                   'omitted charged commutator leaves nonzero wave residual',
                                   'large affine length retained','RN ray does not imply RN open set'],
                analytic_source='CENTER_ESCAPE_CHARACTERISTIC_EXTENSION.md; finite-germ inputs from AF03 and external source audit retained',
                actual_seed_certificate_replayed=False,actual_seed_delta_range_certified=False,
                actual_PDE_escape_certified_by_computation=False,
                full_Bondi_completeness_bridge_verified=False,RN_final_state_verified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'CENTER_ESCAPE_EXTENSION_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: ESC01 identities and three artificial-corner budgets; actual formation theorem separate analytic proof, strong final-state obligations OPEN')


if __name__=='__main__':
    main()
