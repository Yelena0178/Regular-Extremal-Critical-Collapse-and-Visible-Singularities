"""BOND02 exact metric/field identities and scoped controls, not nonlinear PDE certification."""
from hashlib import sha256
import json
from pathlib import Path
import math
import sympy as s
from scipy.integrate import solve_ivp


def zero(expr,label):
    if s.simplify(s.expand(expr))!=0:
        raise ArithmeticError(label)


def main():
    u,r=s.symbols('u r',real=True,positive=True)
    B=s.Function('B',real=True)(u,r); C=s.Function('C',real=True)(u,r)
    coords=[u,r]; g=s.Matrix([[-B*C,-B],[-B,0]]); inv=g.inv()
    Gamma=[[[s.simplify(sum(inv[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in range(2)))
             for c in range(2)] for b in range(2)] for a in range(2)]
    N=[1,-C/2]
    for a in range(2):
        zero(s.diff(N[a],r)+sum(Gamma[a][1][j]*N[j] for j in range(2)),
             'ingoing N parallel along outgoing ray')
    alpha=s.diff(B,u)/B-s.diff(C,r)/2-C*s.diff(B,r)/(2*B)
    for a in range(2):
        accel=sum(N[j]*s.diff(N[a],coords[j]) for j in range(2))
        accel+=sum(Gamma[a][j][k]*N[j]*N[k] for j in range(2) for k in range(2))
        zero(accel-alpha*N[a],'ingoing non-affinity')
    zero(Gamma[1][1][1]-s.diff(B,r)/B,'physical outgoing affine weight')
    # Independent scalar/constraint expansion at a point.
    b,m,Q,e=s.symbols('b m Q e',real=True,nonzero=True)
    ar,ai,pr,pi=s.symbols('ar ai pr pi',real=True)
    U=ar+s.I*ai; X=pr+s.I*pi
    norm=lambda x:s.expand(x*s.conjugate(x))
    f=1-2*m/r; c=b*f
    mr=Q*Q/(2*r*r)+r*r*f*norm(X)/2
    br=b*r*norm(X); fr=-2*mr/r+2*m/r**2
    zero(br*f+b*fr-b*(2*m/r**2-Q*Q/r**3),'radial C cancellation')
    mu=-r*r*norm(U)/b+r*r*f*s.re(U*s.conjugate(X))
    zero(mu-c*mr/2+r*r*norm(U-c*X/2)/b+c*Q*Q/(4*r*r),
         'ingoing mass flux including electromagnetic pressure')
    if s.simplify(br*f+b*fr-b*(2*m/r**2+Q*Q/r**3))==0:
        raise ArithmeticError('wrong electric sign negative control')
    psi=s.Function('psi')(u,r); aa=s.Function('a',real=True)(u,r)
    cc=s.Function('c',real=True)(u,r); phi=psi/r
    Dt=lambda value:s.diff(value,u)+s.I*e*aa*value
    box=(Dt(-r*r*s.diff(phi,r))+s.diff(-r*r*Dt(phi)+cc*r*r*s.diff(phi,r),r))/r
    reduced=-2*s.diff(psi,u,r)+cc*s.diff(psi,r,2)+(s.diff(cc,r)-2*s.I*e*aa)*s.diff(psi,r)
    reduced-=(s.I*e*s.diff(aa,r)+s.diff(cc,r)/r)*psi
    zero(box-reduced,'independent charged 4D radial wave operator')
    W=Dt(psi)-cc*s.diff(psi,r)/2
    zero(s.diff(W,r)-(s.I*e*s.diff(aa,r)/2-s.diff(cc,r)/(2*r))*psi+reduced/2,
         'radial reduced ingoing derivative')
    Z=s.diff(psi,r)
    transport=Dt(Z)-cc*s.diff(Z,r)/2-s.diff(cc,r)*Z/2
    transport+=(s.I*e*s.diff(aa,r)/2+s.diff(cc,r)/(2*r))*psi
    zero(transport+reduced/2,'radial derivative transport')
    # Charge nQ flux written in reduced variables; the radius term is real.
    wr,wi,psr,psi_im=s.symbols('wr wi psr psi_im',real=True)
    pval=psr+s.I*psi_im; wval=wr+s.I*wi
    zero(r*r*s.im((pval/r)*s.conjugate(wval/r+c*pval/(2*r*r)))
         -s.im(pval*s.conjugate(wval)),'reduced Maxwell n-current')
    R0=s.symbols('R0',positive=True)
    ell=s.log(r/R0)
    primitive=(ell**2+4*ell+5)/r
    zero(s.diff(primitive,r)+(1+ell)**2/r**2,'integrable logarithmic bootstrap tail')
    # Finite-energy, vanishing-amplitude boundary ODE countercontrol.
    L,S=s.symbols('L S',positive=True,real=True)
    F=s.exp(s.I*L)/s.sqrt(L)
    Fprime=(s.I-1/(2*L))*F/S
    energy=1/(S*S*L)+1/(4*S*S*L**3)
    zero(norm(Fprime)-energy,'slow-phase radiation energy')
    zero(s.im(F*s.conjugate(Fprime))+1/(S*L),'nonintegrable boundary charge current')
    zero(e/(S*L)+e*s.im(F*s.conjugate(Fprime)),'exact boundary charge balance')
    zero(s.Rational(5,4)-S*S*energy-(L-1)*(5*L*L+L+1)/(4*L**3),
         'integrable energy upper bound for L>=1')
    tt,epsilon=s.symbols('tt epsilon',positive=True)
    zero(s.diff((1+tt)**(-epsilon)/epsilon,tt)+(1+tt)**(-1-epsilon),
         'conditional weighted flux tail integral')
    controls=[]; mass=1.; charge=.8; T=10.
    for radius in [50.,100.,200.]:
        ffun=lambda rr:1-2*mass/rr+charge*charge/(rr*rr)
        sol=solve_ivp(lambda t,y:[-ffun(y[0])/2],(0,T),[radius],
                      rtol=1e-12,atol=1e-13,max_step=.1)
        if not sol.success: raise ArithmeticError(sol.message)
        affine=2*(radius-sol.y[0,-1])/ffun(radius)
        rho=radius-T/2
        K=lambda rr:2*mass/(rr*(1-2*mass/rr))
        lower=T*math.exp(-K(rho)-mass*T/(rho*rho))
        upper=T*math.exp(K(radius)+2*mass/(rho*(1-2*mass/rho)))
        if not lower<=affine<=upper:
            raise ArithmeticError('RN affine comparison control')
        controls.append(dict(R=radius,T=T,affine_length=float(affine),
                             lower_bound=lower,upper_bound=upper,
                             relative_difference_from_unit_time=abs(affine/T-1)))
    if not all(controls[i+1]['relative_difference_from_unit_time']<controls[i]['relative_difference_from_unit_time'] for i in range(2)):
        raise ArithmeticError('affine normalization control')
    root=Path(__file__).resolve().parent
    names=['verify_actual_bondi_bridge.py','ACTUAL_BONDI_COMPLETENESS_BRIDGE.md',
           'CENTER_ESCAPE_CHARACTERISTIC_EXTENSION.md','REGULAR_CENTER_BONDI_MATCHING.md',
           'FINITE_BONDI_EXTERIOR_REALIZATION.md','MARGINAL_SEED_CAUSAL_INTERFACE.md',
           'OUTGOING_NULL_INFINITY.md','../../definitions/MODEL.md',
           '../../reviews/NEWSTAGE0_STAGE1_2026-10-12/RECCVS_NewStage0_Stage1_2026-10-12/details/02_OUTCOMES_MASS_AND_CRITICALITY.md',
           '../../reviews/STAGE0_SELF_REVIEW_2026-10-11/verification/sources/literature/1107.0949.txt']
    report=dict(claim_ids=[f'BOND02.{i}' for i in range(1,9)],
                logic='PROVED for listed exact identities; actual exterior analytic proof is separate',
                evidence=['EXACT_ALGEBRA','FIXED_RN_FINITE_CONTROLS','BOUNDARY_ODE_COUNTERCONTROL'],
                audit='INTERNAL_AUDIT',
                checks=['metric connection and parallel ingoing null normalization','outgoing affine parameter',
                        'radial optical cancellation','complete ingoing mass square',
                        'independent charged wave and both reduced transports','reduced Maxwell flux',
                        'logarithmic charge bootstrap tail','finite-energy vanishing-amplitude charge-divergent boundary balance',
                        'conditional weighted radiation tail integral'],
                negative_controls=['wrong electric sign fails radial cancellation',
                                   'finite energy plus F->0 does not imply Q_B late limit in boundary ODEs'],
                RN_controls=controls,boundary_countercontrol_is_actual_EMCSF_solution=False,
                analytic_source='ACTUAL_BONDI_COMPLETENESS_BRIDGE.md BOND02.1-BOND02.7',
                actual_seed_numerical_PDE_certified=False,late_charge_limit_verified=False,
                weighted_actual_radiation_flux_verified=False,
                horizon_final_parameter_agreement_verified=False,RN_convergence_verified=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'ACTUAL_BONDI_BRIDGE_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: BOND02 exact geometry, flux and wave identities; finite RN/ODE controls only, actual exterior theorem analytic, late charge/RN/Goal A OPEN')


if __name__=='__main__':
    main()
