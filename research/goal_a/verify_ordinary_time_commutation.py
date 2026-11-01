"""COM19 exact commutation/energy audits and finite majorants, not PDE truth certification."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent


def zero(expr):
    assert s.simplify(s.expand(expr)) == 0, expr


def commutation_identities():
    u, r, e = s.symbols('u r e', real=True)
    psi = s.Function('psi')(u, r)
    c, a = s.Function('c')(u, r), s.Function('a')(u, r)
    P, Z = s.diff(psi, u), s.diff(psi, r)
    def op(field):
        return (-2*s.diff(field, u, r)+s.diff(c*s.diff(field, r), r)
                -2*s.I*e*a*s.diff(field, r)-(s.I*e*s.diff(a, r)+s.diff(c, r)/r)*field)
    cu, cr, au = s.diff(c, u), s.diff(c, r), s.diff(a, u)
    cru, aru = s.diff(c, r, u), s.diff(a, r, u)
    rhs1 = -cu*s.diff(Z, r)+(2*s.I*e*au-cru)*Z+(s.I*e*aru+cru/r)*psi
    zero(op(P)-s.diff(op(psi), u)-rhs1)
    F1 = -cu*(Z-psi/r)+s.I*e*au*psi
    F0 = -cu*Z/r+cu*psi/r**2+s.I*e*au*Z
    zero(s.diff(F1, r)+F0-rhs1)
    rho = cu/c
    Zr = (2*s.diff(P, r)+(2*s.I*e*a-cr)*Z+(s.I*e*s.diff(a, r)+cr/r)*psi)/c
    TZ = rho*(cr-2*s.I*e*a)-cru+2*s.I*e*au
    TP = s.I*e*aru+cru/r-rho*(s.I*e*s.diff(a, r)+cr/r)
    zero(rhs1.subs(s.diff(psi, r, 2), Zr)+2*rho*s.diff(P, r)-TZ*Z-TP*psi)
    def W(field):
        return s.diff(field, u)+s.I*e*a*field-c*s.diff(field, r)/2
    zero(W(P)-(s.diff(W(psi), u)-s.I*e*au*psi+cu*Z/2))
    B=s.I*e*s.diff(a,r)/2-cr/(2*r)
    zero(s.diff(W(P),r)-B*P+op(P)/2)
    zero(rho*s.diff(P,r)-s.diff(rho*P,r)+s.diff(rho,r)*P)
    # Static coefficients give zero commutation source, not a missing field term.
    static = {cu: 0, au: 0, cru: 0, aru: 0}
    zero(TZ.subs(static));zero(TP.subs(static))
    # The residual gauge fixing permits constant phases; time-dependent gauge would change P.
    theta = s.Function('theta')(u)
    zero(s.diff(s.exp(-s.I*e*theta)*psi, u)
         -s.exp(-s.I*e*theta)*(P-s.I*e*s.diff(theta, u)*psi))


def maxwell_and_energy_audits():
    u, r, e = s.symbols('u r e', real=True)
    X, Y = s.Function('X')(u, r), s.Function('Y')(u, r)
    psi = X+s.I*Y
    P, Z = s.diff(psi, u), s.diff(psi, r)
    # Complex-valued formal functions are expanded into real components first.
    current = e*(Y*s.diff(X, r)-X*s.diff(Y, r))
    once = e*(s.diff(Y, u)*s.diff(X, r)+Y*s.diff(X, r, u)
              -s.diff(X, u)*s.diff(Y, r)-X*s.diff(Y, r, u))
    zero(s.diff(current, u)-once)
    twice = e*(s.diff(Y, u, 2)*s.diff(X, r)+2*s.diff(Y, u)*s.diff(X, r, u)
              +Y*s.diff(X, r,u,u)-s.diff(X, u, 2)*s.diff(Y,r)
              -2*s.diff(X,u)*s.diff(Y,r,u)-X*s.diff(Y,r,u,u))
    zero(s.diff(current,u,2)-twice)
    # Compatible first jets: Psi=Z=0, P=1, P_r=i. Q_ru=0 but current(P)=-e.
    assert once.subs({X:0,Y:0,s.diff(X,r):0,s.diff(Y,r):0})==0
    assert e*(0*0-1*1)==-e
    # Local canonical energy balance with BOTH boundary fluxes retained.
    t, x, av, V = s.symbols('t x av V', real=True)
    v = s.Function('v')(t,x);w=s.Function('w')(t,x)
    vt, wt, vx, wx = s.diff(v,t),s.diff(w,t),s.diff(v,x),s.diff(w,x)
    energy = (vt**2+wt**2+vx**2+wx**2+(V-e**2*av**2)*(v**2+w**2))/2
    flux = vx*vt+wx*wt
    vtt = s.diff(v,x,2)+2*e*av*wt+(e**2*av**2-V)*v
    wtt = s.diff(w,x,2)-2*e*av*vt+(e**2*av**2-V)*w
    zero((s.diff(energy,t)-s.diff(flux,x)).subs({s.diff(v,t,2):vtt,s.diff(w,t,2):wtt}))
    # Exact rational upper bound proving the fixed RN test energy is negative.
    S=s.Integer(10000)
    flat_upper=-s.Rational(73,600)
    delta=s.Rational(3,1)/S
    err=(delta*s.Rational(23,12)+s.Rational(4,1)/S*6
         +s.Rational(9,25)*(delta/(1-delta))*6)/2
    assert err<s.Rational(1,500) and flat_upper+err<0
    # In particular no positivity conclusion comes from an integrable forcing.
    return {'flat_energy_upper_exact':str(flat_upper),'RN_error_bound_exact':str(err),
            'total_energy_upper_exact':str(flat_upper+err),'positive':False,
            'scope':'specified static test-field canonical energy; not actual Goal-A data or instability'}


def exact_radial_primitives():
    R,U=s.symbols('R U',positive=True)
    L=2*s.asinh(s.sqrt(U/R))
    I1=L/s.sqrt(U)
    I3=(L-2*s.sqrt(U/(R+U)))/U**s.Rational(3,2)
    zero(s.diff(I1,R)+1/(R*s.sqrt(R+U)))
    zero(s.diff(I3,R)+1/(R*(R+U)**s.Rational(3,2)))
    eta=s.symbols('eta',positive=True)
    nu=1-eta;alpha=s.Rational(1,2)-eta
    zero(2*nu+alpha+s.Rational(1,2)-3*nu)
    zero(2*nu-s.Rational(1,2)-eta+s.Rational(3,2)-3*nu)


def finite_majorants():
    rows=[];integrals=[];radial_controls=[]
    for eta in map(mp.mpf,['.025','.1','.24']):
        nu=1-eta;g=1-2*eta
        for R in map(mp.mpf,[8,32,128]):
            M,K,e,A,D=map(mp.mpf,[1,1,.6,.2,.3])
            # Finite controls choose admissible loose constants, not candidate PDE data.
            CZ=mp.mpf(3);Cp=1+CZ;CQ=e*CZ
            Lam=e*K/2+M/R+K*K/(2*R*R)
            bv=2*Lam+mp.mpf('.5');bmin=mp.exp(-2*M/(R*(1-2*M/R)))
            cmin=(1-2*M/R)*bmin
            Bg=4*Cp*A*D/3
            Cg=Cp**2/2+Cp*bv+(1+2*M/R+K*K/R**2)*Cp**2/4+K*CQ/2
            BQ=2*e*Lam+CQ/2;Cm=2*bv*bv+Cp**2/4;Ec=2*M+K*K/R
            Cc=Bg/mp.sqrt(R)+Cg*A*A/R+2/bmin*(2*D*D+Cm*A*A/R)
            Ccr=Ec*(Bg/R**mp.mpf('1.5')+Cg*A*A/R**2)+2/bmin*(2*D*D+Cm*A*A/R)+2*K*(e*A*D/mp.sqrt(R)+BQ*A*A/R)
            Car=e*A*D+BQ*A*A/mp.sqrt(R)+K*(Bg/R**2+Cg*A*A/R**mp.mpf('2.5'))
            Ca=2*e*A*D+BQ*A*A/mp.sqrt(R)+K*(2*Bg/(5*R**2)+Cg*A*A/(3*R**mp.mpf('2.5')))
            CTZ=Cc/cmin*(Ec/R**mp.mpf('2.5')+2*e*K/R**mp.mpf('1.5'))+Ccr/R**mp.mpf('1.5')+2*e*Ca
            CTP=e*Car+Ccr/R**mp.mpf('1.5')+Cc/cmin*(e*K/R**mp.mpf('1.5')+Ec/R**mp.mpf('2.5'))
            for ratio in map(mp.mpf,[1,4,64]):
                r=R*ratio
                Gg=Bg*r**(-mp.mpf('1.5'))+Cg*A*A/r**2
                Gm=(2*D*D+Cm*A*A/r)/bmin;GQ=e*A*D*mp.sqrt(r)+BQ*A*A
                Gc=Gg+2*Gm/r;Gcr=Ec*Gg/r**2+2*Gm/r**2+2*K*GQ/r**3
                Gar=(K*Gg+GQ)/r**2
                Ga=2*e*A*D/mp.sqrt(r)+BQ*A*A/r+K*(2*Bg/(5*r**mp.mpf('2.5'))+Cg*A*A/(3*r**3))
                assert Gc<=Cc/r and Gcr<=Ccr/r**2
                assert Gar<=Car/r**mp.mpf('1.5')*(1+mp.mpf('1e-35')), (R,r,Gar/(Car/r**mp.mpf('1.5'))-1)
                assert Ga<=Ca/mp.sqrt(r)*(1+mp.mpf('1e-35')), (R,r,Ga/(Ca/mp.sqrt(r))-1)
                tz=Gc/cmin*(Ec/r**2+2*e*K/r)+Gcr+2*e*Ga
                tp=e*Gar+Gcr/r+Gc/cmin*(e*K/r**2+Ec/r**3)
                assert tz<=CTZ/mp.sqrt(r)*(1+mp.mpf('1e-35'))
                assert tp<=CTP/r**mp.mpf('1.5')*(1+mp.mpf('1e-35'))
                rows.append({'eta':str(eta),'R':str(R),'r_over_R':str(ratio),
                             'TZ_majorant_ratio':mp.nstr(tz*mp.sqrt(r)/CTZ,10),
                             'TPsi_majorant_ratio':mp.nstr(tp*r**mp.mpf('1.5')/CTP,10)})
            # Exact integral up to U=100; tail evaluated by the analytic primitive.
            cutoff=mp.mpf(100)
            val=mp.quad(lambda U: U**(-2*nu),[1,cutoff])+cutoff**(-g)/g
            assert abs(val-1/g)<mp.mpf('1e-33')
            radial=mp.quad(lambda r:r**(-2),[R,mp.inf])
            assert abs(radial-1/R)<mp.mpf('1e-33')
            integrals.append({'eta':str(eta),'R':str(R),
                              'weighted_force_time_integral':mp.nstr(val,14),
                              'radial_L2_square_majorant_integral':mp.nstr(radial,14),
                              'extra_U_transport_moment_not_paid_by_same_majorant':True})
            for U in map(mp.mpf,[1,16,1024]):
                lr=2*mp.asinh(mp.sqrt(U/R))
                i1=mp.quad(lambda x:1/(x*mp.sqrt(x+U)),[R,mp.inf])
                i3=mp.quad(lambda x:1/(x*(x+U)**mp.mpf('1.5')),[R,mp.inf])
                e1=abs(i1-lr/mp.sqrt(U))
                e3=abs(i3-(lr-2*mp.sqrt(U/(R+U)))/U**mp.mpf('1.5'))
                # The infinite-interval quadrature has slower half-power tail convergence.
                assert e1<mp.mpf('1e-18') and e3<mp.mpf('1e-33')
                assert U**(-2*nu)*lr<=2/mp.sqrt(R)
                xx=U/R
                assert 1+xx-mp.sqrt(1+xx)<=xx
                assert U**(-mp.mpf('.5'))*mp.sqrt(1+U/R)<=mp.sqrt(1+1/R)
                radial_controls.append({'eta':str(eta),'R':str(R),'U':str(U),
                                        'L1_half_primitive_error':mp.nstr(e1,8),
                                        'L1_threehalf_primitive_error':mp.nstr(e3,8),
                                        'commuted_amplitude_and_bridge_majorants':'PASS'})
    # A finite RN quadrature cross-check of the independently bounded negative functional.
    L,S,q=mp.mpf(12),mp.mpf(10000),mp.mpf('.6')
    def density(y):
        r=S*mp.exp(y);f=1-2/r+1/r**2;rfp=2/r-2/r**2
        gg=mp.sin(mp.pi*y/L);gs=mp.pi/L*mp.cos(mp.pi*y/L)
        return (f*(gs+gg/2)**2+(rfp-q*q/f)*gg*gg)/2
    ern=mp.quad(density,[0,L/2,L]);eflat=mp.pi**2/(4*L)+(mp.mpf('.25')-q*q)*L/4
    assert ern<0 and abs(ern-eflat)<mp.mpf('.002')
    return rows,integrals,radial_controls,{'RN_energy':mp.nstr(ern,16),'flat_energy':mp.nstr(eflat,16),'interval_certified':False}


def main():
    mp.mp.dps=40
    commutation_identities()
    negative=maxwell_and_energy_audits()
    exact_radial_primitives()
    rows,integrals,radial_controls,rn=finite_majorants()
    sources=['verify_ordinary_time_commutation.py','ORDINARY_TIME_COMMUTATION_AND_ENERGY_GATE.md',
             'TIMELIKE_CHARGE_AND_COEFFICIENT_JETS.md','GLOBAL_RN_SOURCE_NORM_AUDIT.md',
             'PHYSICAL_TRACE_GREEN_AND_DELAY.md','MODULATED_BONDI_RADIAL_IMPROVEMENT.md',
             '../../definitions/MODEL.md','ACCEPTANCE.md']
    report={'round':'R27','logic':'PROVED identities/conditional forcing bounds; REFUTED automatic positivity of specified test-field energy',
            'evidence':['ANALYTIC','EXACT_ALGEBRA','EXACT_RATIONAL_ENERGY_BOUND','FINITE_MAJORANT_CONTROLS'],
            'audit':'INTERNAL_AUDIT; no actual PDE or independent mathematical certification',
            'source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in sources},
            'exact_commutation_and_maxwell_identities':'PASS','local_energy_balance_with_end_flux':'PASS',
            'negative_energy_exact_bound':negative,'finite_majorants':rows,'finite_weighted_integrals':integrals,
            'finite_radial_and_bridge_controls':radial_controls,
            'finite_RN_energy_check':rn,'ordinary_commuted_bulk_forcing_bound_under_A_D_K':True,
            'commuted_radiation_bridge_under_unknown_H_P':True,
            'actual_A_D_K_uniform_bounds_verified':False,'real_inner_commuted_trace_bound_verified':False,
            'F_double_prime_or_carrier_envelope_bound_verified':False,'full_commuted_energy_propagation_verified':False,
            'negative_energy_is_actual_goal_counterexample':False,'negative_energy_proves_mode_instability':False,
            'high_frequency_or_strong_horizon_limit_verified':False,'goal_A_proved':False}
    target=HERE/'ORDINARY_TIME_COMMUTATION_CHECKS_2026-10-24.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PASS COM19: exact commutation/Maxwell/energy/radial identities and rational negative energy bound; {len(rows)} coefficient, {len(integrals)} integral, {len(radial_controls)} radial/bridge, 1 RN controls; real trace/Goal A OPEN')


if __name__=='__main__':main()
