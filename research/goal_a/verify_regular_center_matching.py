"""CENTER03 exact constraint identities and finite ODE controls; no PDE certification."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import beta, betainc


def zero(value, label):
    if s.simplify(s.expand(value)) != 0:
        raise ArithmeticError(label)


def main():
    r,L,e,c,t,x=s.symbols('r L e c t x', positive=True, real=True)
    m,q,v,psi,dp,h=s.symbols('m q v psi dp h', real=True)
    ar,ai,br,bi,D,b=s.symbols('ar ai br bi D b', real=True)
    a=ar+s.I*ai; z=br+s.I*bi
    norm=lambda z:s.expand(z*s.conjugate(z))
    zero(((D+b*s.sqrt(D))*norm(a+z)+(D-b*s.sqrt(D))*norm(a-z))/4
         -D*(norm(a)+norm(z))/2-b*s.sqrt(D)*s.re(a*s.conjugate(z)),
         'general angular-curvature positive square identity')
    phi=psi/L; chi=-s.I*c*psi/L**2
    zero(e*(L*x)**2*s.im(phi*s.conjugate(chi))*L-e*c*x*x*psi*psi,
         'scaled signed Gauss source')
    f=1-2*m/(L*x)
    charge_energy=(L*x)**2*f*((c*psi/L**2)**2+(dp/L**2)**2)*L/2
    neutral_energy=(L*x)**2*f*(t*h/L**s.Rational(3,2))**2*L/2
    A=x*x*((c*c*psi*psi+dp*dp)/L+t*t*h*h)/2
    zero(charge_energy+neutral_energy-f*A,'scaled mass source')
    rhs=q*q/(2*L*x*x)+f*A
    sensitivity=s.diff(rhs,m)*v+s.diff(rhs,t)
    zero(sensitivity+2*A*v/(L*x)-f*t*x*x*h*h,'neutral sensitivity equation')
    M=s.symbols('M',real=True)
    rn=M-q*q/(2*r)
    zero(s.diff(rn,r)-q*q/(2*r*r),'electrovacuum mass continuation')
    # Kommemi v2 (20)-(25), phi_K=phi/sqrt(4*pi), same e,A,Q.
    dk=a/s.sqrt(4*s.pi); pk=z/s.sqrt(4*s.pi)
    zero(4*s.pi*norm(dk)-norm(a),'source Raychaudhuri normalization')
    zero(2*s.pi*s.I*e*r*r*(pk*s.conjugate(dk)-s.conjugate(pk)*dk)
         +e*r*r*s.im(z*s.conjugate(a)),'source u-current orientation')
    zero(2*s.pi*s.I*e*r*r*(s.conjugate(pk)*dk-pk*s.conjugate(dk))
         -e*r*r*s.im(z*s.conjugate(a)),'source v-current orientation')
    au,om,nu,lam=s.symbols('au om nu lam',real=True)
    pu,pv,puv,field=s.symbols('pu pv puv field')
    av=-om**2*q/(2*r*r)
    covariant_half=(2*puv+2*s.I*e*au*pv+s.I*e*av*field
                    +2*nu*pv/r+2*lam*(pu+s.I*e*au*field)/r)/2
    source_wave=puv+(nu*pv+lam*pu)/r+s.I*e*(au*(pv+lam*field/r)-om**2*q*field/(4*r*r))
    zero(source_wave-covariant_half,'source wave commutator normalization')
    # Polynomial control is C5 across its cutoffs, not the C-infinity theorem input.
    y=s.symbols('y',real=True)
    bump=(4*y*(1-y))**6
    I=s.integrate((1+y)**2*bump*bump,(y,0,1))
    J=s.integrate((1+y)**2*s.diff(bump,y)**2,(y,0,1))
    E=s.integrate((2+y)**2*bump*bump,(y,0,1))/2
    primitive=s.integrate((1+y)**2*bump*bump,y)
    zero(s.diff(primitive,y)-(1+y)**2*bump*bump,'exact charge primitive')
    if not (I>0 and J>0 and E>0):
        raise ArithmeticError('nonzero bump integrals')
    weights=np.array([beta(13,13),2*beta(14,13),beta(15,13)])
    If=float(I); Ef=float(E); Jf=float(J)
    def profile(x,shift):
        u=x-shift
        if not 0<u<1: return 0.,0.
        base=4*u*(1-u)
        return base**6,24*(1-2*u)*base**5
    def charge(x,target):
        if x<=1: return 0.
        if x>=2: return target
        u=x-1
        return target*float(weights@np.array([betainc(13,13,u),betainc(14,13,u),betainc(15,13,u)]))/float(weights.sum())
    samples=[]
    cases=[(target,0.,0.,scale) for target in [-1.,1.] for scale in [128.,256.]]
    cases.extend([(1.,.4,.5,256.),(-1.,-.4,.5,256.)])
    for target,seed_q,seed_mass,scale in cases:
        coef=(target-seed_q)/(.6*If)
        Cq=((abs(seed_q)+abs(target-seed_q))**2+coef**2*If+Jf)/2
        mu=seed_mass+.8
        T=np.sqrt(3*(mu-seed_mass)/Ef)
        cap=seed_mass+Cq+T*T*Ef
        if not (scale>4*cap and Cq/scale<mu-seed_mass):
            raise ArithmeticError('quantitative shell assumptions')
        def integrate(amplitude):
            def ode(x,state):
                mass,sens=state
                ps,dps=profile(x,1); hs,_=profile(x,2)
                flux=x*x*((coef*coef*ps*ps+dps*dps)/scale+amplitude**2*hs*hs)/2
                ff=1-2*mass/(scale*x); qq=seed_q+charge(x,target-seed_q)
                return [qq*qq/(2*scale*x*x)+ff*flux,
                        -2*flux*sens/(scale*x)+ff*amplitude*x*x*hs*hs]
            sol=solve_ivp(ode,(1,4),[seed_mass-seed_q**2/(2*scale),0.],rtol=2e-11,atol=1e-13,max_step=.02,dense_output=True)
            if not sol.success: raise ArithmeticError(sol.message)
            return sol
        low=integrate(0.); high=integrate(T)
        if not (low.y[0,-1]<mu<high.y[0,-1]):
            raise ArithmeticError('mass bracket')
        tuned=brentq(lambda amp:integrate(amp).y[0,-1]-mu,0,T,xtol=2e-12)
        sol=integrate(tuned); xx=np.linspace(1,4,1201); masses=sol.sol(xx)[0]
        minf=float(np.min(1-2*masses/(scale*xx)))
        derivative=float(sol.y[1,-1]); dt=1e-4
        finite_difference=(integrate(tuned+dt).y[0,-1]-integrate(tuned-dt).y[0,-1])/(2*dt)
        if minf<=.5 or derivative<=0 or abs(derivative-finite_difference)>1e-7:
            raise ArithmeticError('positivity or sensitivity control')
        if abs(sol.y[0,-1]-mu)>1e-9 or abs(seed_q+charge(4,target-seed_q)-target)>1e-14:
            raise ArithmeticError('boundary matching control')
        samples.append(dict(q=target,seed_q=seed_q,seed_ADM_mass=seed_mass,L=scale,target_mass=mu,matched_mass=float(sol.y[0,-1]),
                            t=float(tuned),mass_without_neutral=float(low.y[0,-1]),
                            min_f_sample=minf,mass_t_derivative=derivative,
                            sensitivity_difference=abs(derivative-finite_difference)))
    root=Path(__file__).resolve().parent
    names=['verify_regular_center_matching.py','REGULAR_CENTER_BONDI_MATCHING.md',
           'FINITE_BONDI_EXTERIOR_REALIZATION.md','CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md',
           '../../definitions/MODEL.md',
           '../../reviews/STAGE0_SELF_REVIEW_2026-10-11/verification/sources/literature/1107.0949.txt']
    report=dict(claim_ids=['CENTER03.1','CENTER03.2','CENTER03.3','CENTER03.4','CENTER03.5','CENTER03.6'],
                logic='PROVED for exact identities; finite ODE samples are controls; analytic center and finite-transfer theorems separate',
                evidence=['EXACT_ALGEBRA','FINITE_ODE_NUMERICS'],audit='INTERNAL_AUDIT',
                exact_checks=['general angular-curvature positive source','signed charge scaling',
                              'mass scaling','neutral-shell sensitivity','electrovacuum continuation','charge primitive',
                              'Kommemi Raychaudhuri, signed Maxwell currents and wave normalization'],
                bump_control='polynomial C5 only; analytic proof uses C-infinity compact bumps',
                bump_integrals=dict(I=str(I),J=str(J),E=str(E)),samples=samples,
                negative_controls=['charged-only mass below target in all six cases',
                                   'negative matching mass excluded analytically by positive source'],
                analytic_existence_source='REGULAR_CENTER_BONDI_MATCHING.md CENTER03.2-CENTER03.4',
                finite_domain_transfer_analytic_source='REGULAR_CENTER_BONDI_MATCHING.md CENTER03.5; Kommemi v2 Proposition 2.1 and checked model map',
                Cauchy_source_hypotheses_checked=True,numerical_PDE_transfer_certified=False,
                full_future_certified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'REGULAR_CENTER_MATCHING_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: CENTER03 identities, source normalization and six signed-charge/mass controls; center/finite-transfer analytic proofs separate, full future and Goal A OPEN')


if __name__=='__main__':
    main()
