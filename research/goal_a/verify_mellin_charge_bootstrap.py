"""INNER06 exact Mellin/flux identities and scoped controls; no actual B_sigma proof."""
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
    r=s.symbols('r',positive=True)
    f=s.Function('f',positive=True)(r)
    q,w=s.symbols('q w',real=True)
    z=s.symbols('z',real=True)
    Yfun=s.Function('Y')
    Y=Yfun(s.log(r)); Ys=s.diff(Yfun(z),z).subs(z,s.log(r)); Yss=s.diff(Yfun(z),z,2).subs(z,s.log(r))
    A=r*s.diff(f,r)/f; As=r*s.diff(A,r)
    R=s.sqrt(r/f)*Y
    mode=f*s.diff(f*s.diff(R,r),r)+((w-q/r)**2-f*s.diff(f,r)/r)*R
    log_potential=(w*r-q)**2/f**2-s.Rational(1,4)-A/2-As/2-A*A/4
    zero(mode-(f/r)**s.Rational(3,2)*(Yss+log_potential*Y),'complete RN Mellin equation')
    zero(As-A-r*r*s.diff(f,r,2)/f+A*A,'logarithmic metric derivative identity')
    G1=s.Function('G1')(r); G0=s.Function('G0')(r)
    J1=s.sqrt(r/f)*G1
    J0=(r/f)**s.Rational(3,2)*G0-(1-A)*J1/2
    zero(r*s.diff(J1,r)+J0-(r/f)**s.Rational(3,2)*(f*s.diff(G1,r)+G0),
         'Mellin divergence forcing with all metric derivatives')
    # Exact flux preservation with general complex jets.
    fr,rr,aa=s.symbols('fr rr aa',positive=True,real=True)
    yr,yi,pr,pi=s.symbols('yr yi pr pi',real=True)
    yy=yr+s.I*yi; pp=pr+s.I*pi
    norm=lambda v:s.expand(v*s.conjugate(v))
    rv=s.sqrt(rr/fr)*yy; rx=s.sqrt(fr/rr)*(pp+(1-aa)*yy/2)
    zero(s.im(s.conjugate(rv)*rx)-s.im(s.conjugate(yy)*pp),'Mellin transform preserves physical signed flux')
    self_flux=s.im(s.conjugate(s.Integer(1))*s.I)
    cross=s.det(s.Matrix([[1,1],[s.I,s.I]]))
    assert self_flux==1 and cross==0
    # Actual forced oscillator, with zero initial data and bounded L2 source.
    beta,ell=s.symbols('beta ell',positive=True,real=True)
    t=s.symbols('t',real=True)
    resonant=(t*s.exp(s.I*beta*t)-s.sin(beta*t)/beta)/(2*s.I*beta*s.sqrt(ell))
    zero(s.diff(resonant,t,2)+beta**2*resonant-s.exp(s.I*beta*t)/s.sqrt(ell),
         'exact coherent resonant source')
    zero(resonant.subs(t,0),'resonant zero position')
    zero(s.diff(resonant,t).subs(t,0),'resonant zero derivative')
    nn=s.symbols('nn',integer=True,positive=True)
    Ln=2*s.pi*nn/beta
    end_y=resonant.subs(t,ell).subs(ell,Ln)
    end_p=s.diff(resonant,t).subs(t,ell).subs(ell,Ln)
    zero(norm(end_p)+beta**2*norm(end_y)-Ln/2,'resonant energy grows with logarithmic interval')
    # Gauge-invariant charge current and the real radius contribution.
    phase,e,c=s.symbols('phase e c',real=True)
    gr,gi,hr,hi=s.symbols('gr gi hr hi',real=True)
    g=gr+s.I*gi; h=hr+s.I*hi
    zero(s.im((s.exp(-s.I*e*phase)*g)*s.conjugate(s.exp(-s.I*e*phase)*h))-s.im(g*s.conjugate(h)),
         'parallel-transported characteristic charge current')
    zero(s.im((rr*g)*s.conjugate(rr*h-c*g/2))-rr**2*s.im(g*s.conjugate(h)),
         'reduced characteristic current removes only real radius term')
    sigma,U=s.symbols('sigma U',positive=True)
    integral=(1-(1+U)**(-sigma))/sigma
    zero(s.diff(integral,U)-(1+U)**(-1-sigma),'weighted characteristic Cauchy integral')
    zero(integral.subs(U,0),'initial weighted integral')
    accum=s.Function('accum')(U)
    zero(s.diff(accum**2/2,U)-accum*s.diff(accum,U),'quadratic total-variation area factor one half')
    budget,delta=s.symbols('budget delta',positive=True)
    zero((e**2*budget/(2*sigma)).subs(budget,sigma*delta/e**2)-delta/2,
         'scalar budget pays half of the coefficient bootstrap')
    # Critical time-weight family: actual phase-loop densities before integration.
    amp,L,kappa,hv,hp=s.symbols('amp L kappa hv hp',real=True,positive=True)
    field=amp*hv*s.exp(s.I*phase)
    derivative=amp*(hp+s.I*kappa*hv)*s.exp(s.I*phase)/L
    zero(norm(derivative)-amp**2*(hp*hp+kappa*kappa*hv*hv)/L**2,
         'critical log-time energy density')
    zero(s.im(field*s.conjugate(derivative))+amp**2*kappa*hv*hv/L,
         'log-time phase loop carries nonzero charge area')
    C0,C1=s.symbols('C0 C1',positive=True)
    critical_E=amp**2*(C1+kappa**2*C0)/L
    charge_shift=e*amp**2*kappa*C0
    zero(charge_shift/critical_E-e*kappa*C0*L/(C1+kappa**2*C0),
         'critical weighted energy does not uniformly control charge shift')
    # Finite RN log-interval controls only, not a limit or full PDE certificate.
    qnum=.6; mass=charge=1.; Ri=10.; alpha=qnum/2
    beta2=qnum*qnum-.25; betanum=math.sqrt(beta2)
    Bbound=2*qnum*alpha+alpha**2/2+(16*qnum*qnum+13)*mass/Ri
    controls=[]
    for frequency in [.02,.002,.0002]:
        lo=0.; hi=math.log(alpha/(frequency*Ri))
        def ode(logr,y):
            rad=Ri*math.exp(logr)
            fv=1-2*mass/rad+charge*charge/(rad*rad)
            fp=2*mass/(rad*rad)-2*charge*charge/(rad**3)
            fpp=-4*mass/(rad**3)+6*charge*charge/(rad**4)
            Aval=rad*fp/fv
            Asval=Aval+rad*rad*fpp/fv-Aval*Aval
            pot=(frequency*rad-qnum)**2/fv**2-.25-Aval/2-Asval/2-Aval*Aval/4
            mat=np.array([[0.,1.],[-pot,0.]])
            return (mat@y.reshape(2,2)).ravel()
        sol=solve_ivp(ode,(lo,hi),np.eye(2).ravel(),rtol=2e-12,atol=2e-13,max_step=.01,dense_output=True)
        if not sol.success: raise ArithmeticError(sol.message)
        matrices=sol.sol(np.linspace(lo,hi,501)).T.reshape(-1,2,2)
        state=matrices@np.array([1.,1.j*betanum])
        flux=np.imag(np.conjugate(state[:,0])*state[:,1])
        energy=np.abs(state[:,1])**2+beta2*np.abs(state[:,0])**2
        error=float(np.max(np.abs(np.linalg.det(matrices)-1)))
        flux_error=float(np.max(np.abs(flux-betanum)))
        if error>2e-9 or flux_error>2e-9: raise ArithmeticError('finite log RN signed-flow control')
        if np.max(energy)>2*beta2*math.exp(Bbound/betanum) or np.min(energy)<2*beta2*math.exp(-Bbound/betanum):
            raise ArithmeticError('analytic Mellin transfer envelope')
        controls.append(dict(omega=frequency,radial_interval=[Ri,alpha/frequency],log_interval_length=hi,
                             determinant_error=error,signed_flux_error=flux_error,
                             energy_min=float(np.min(energy)),energy_max=float(np.max(energy))))
    root=Path(__file__).resolve().parent
    names=['verify_mellin_charge_bootstrap.py','MELLIN_INNER_TRANSFER_AND_CHARGE_BOOTSTRAP.md',
           'LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md','COULOMB_RENORMALIZATION_AND_MELLIN_GATE.md',
           'ACTUAL_BONDI_COMPLETENESS_BRIDGE.md','FAR_ZONE_RP_AND_COULOMB_BALANCE.md',
           '../../definitions/MODEL.md','ACCEPTANCE.md']
    report=dict(claim_ids=[f'INNER06.{i}' for i in range(1,7)],
                logic='PROVED for exact transformations and scoped controls; uniform reference estimates and actual budget implications analytic; actual uniform budget OPEN',
                evidence=['EXACT_ALGEBRA','RESONANT_OSCILLATOR_COUNTERCONTROL','CHARACTERISTIC_PATH_COUNTERCONTROL','FINITE_FIXED_RN_ODE_CONTROLS'],
                audit='INTERNAL_AUDIT',
                checks=['full RN Mellin potential and logarithmic metric derivative',
                        'Mellin divergence source and physical signed flux',
                        'zero-data resonant source and exact growing energy',
                        'parallel-gauge and reduced physical characteristic charge currents',
                        'positive-exponent time weight and one-half charge area factor',
                        'scalar-to-coefficient bootstrap algebra',
                        'critical log-time phase-loop densities',
                        'three finite RN logarithmic transfer and signed-flow controls'],
                negative_controls=['nonzero individual signed flux does not bound cross Wronskian',
                                   'bare log-L2 forcing has energy growth equal to half the interval length',
                                   'critical time-weight energy can tend to zero with fixed nonzero path charge'],
                finite_RN_controls=controls,
                path_countercontrol_is_actual_EMCSF_solution=False,
                actual_uniform_incoming_weighted_budget_verified=False,
                actual_Coulomb_potential_bootstrap_closed=False,
                global_RN_inverse_Wronskian_bound_verified=False,
                actual_weighted_radiation_flux_verified=False,late_charge_limit_verified=False,
                horizon_parameter_agreement_verified=False,RN_convergence_verified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'MELLIN_CHARGE_BOOTSTRAP_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: INNER06 exact Mellin/charge/time-weight identities and scoped countercontrols; three finite RN log transfers; actual weighted budget/Goal A OPEN')


if __name__=='__main__':
    main()
