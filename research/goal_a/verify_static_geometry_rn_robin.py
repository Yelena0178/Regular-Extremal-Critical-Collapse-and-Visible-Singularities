"""RN20 algebra and finite complex-frequency controls, not interval/PDE certification."""
from __future__ import annotations

import cmath
import hashlib
import json
import math
from functools import lru_cache
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp

HERE = Path(__file__).resolve().parent


def zero(expr):
    assert sp.simplify(sp.expand(expr)) == 0, expr


def algebra():
    b,m,Q,MS,QS,r=sp.symbols('b m Q MS QS r', real=True, nonzero=True)
    f=1-2*m/r;varpi=m+Q**2/(2*r);fs=1-2*MS/r+QS**2/r**2
    zero(b*f-fs-((b-1)*f-2*(varpi-MS)/r+(Q**2-QS**2)/r**2))
    cr=b*(2*m/r**2-Q**2/r**3);fsr=2*MS/r**2-2*QS**2/r**3
    zero(cr-fsr-((b-1)*(2*m/r**2-Q**2/r**3)+2*(varpi-MS)/r**2-2*(Q**2-QS**2)/r**3))
    # The -2 charge coefficient cannot be replaced by -1.
    assert sp.simplify(cr-fsr-((b-1)*(2*m/r**2-Q**2/r**3)+2*(varpi-MS)/r**2-(Q**2-QS**2)/r**3)) != 0
    A,As,k,fv=sp.symbols('A As k f',real=True)
    geom=(-As-1+A)/2+(1-A)**2/4+A*(1-A)/2-A
    zero(geom-(-sp.Rational(1,4)-A/2-As/2-A**2/4))
    # Gauge conjugation of the radial mode equation, without dropping f'.
    t=sp.symbols('t',positive=True);q,w=sp.symbols('q w')
    ff=sp.Function('f')(t);yy=sp.Function('Y')(t);kk=w-q/t
    logprime=sp.I*kk/ff
    conjugated=(ff*(sp.diff(yy,t,2)+2*logprime*sp.diff(yy,t)
                    +(sp.diff(logprime,t)+logprime**2)*yy)
                +sp.diff(ff,t)*(sp.diff(yy,t)+logprime*yy)
                +(kk**2/ff-sp.diff(ff,t)/t)*yy)
    target=ff*sp.diff(yy,t,2)+(sp.diff(ff,t)+2*sp.I*kk)*sp.diff(yy,t)+(sp.I*q/t**2-sp.diff(ff,t)/t)*yy
    zero(conjugated-target)
    # Recurrence for the finite far-zone outgoing asymptotic expansion.
    rho,mu,v,zeta=sp.symbols('rho mu v zeta',nonzero=True)
    coeff=[sp.Integer(1)]
    for n in range(6):
        an=coeff[n];am1=coeff[n-1] if n>=1 else 0;am2=coeff[n-2] if n>=2 else 0
        coeff.append(sp.expand(((n*(n+1)+sp.I*q*(2*n+1))*an-2*mu*n*n*am1+v*n*(n-1)*am2)/(2*sp.I*zeta*(n+1))))
    y=sum(coeff[n]*rho**(-n) for n in range(len(coeff)))
    fr=1-2*mu/rho+v/rho**2
    residual=sp.expand(fr*sp.diff(y,rho,2)+(sp.diff(fr,rho)+2*sp.I*(zeta-q/rho))*sp.diff(y,rho)+(sp.I*q/rho**2-sp.diff(fr,rho)/rho)*y)
    for power in range(2,8):zero(residual.coeff(rho,-power))
    # Mellin perturbation integrals have a finite limit, unlike interval length.
    R,B,lam=sp.symbols('R B lam',positive=True)
    zero(sp.integrate(1/r**2,(r,R,B/lam))-(1/R-lam/B))
    x=sp.symbols('x',positive=True)
    zero(sp.diff(x*sp.log(B/x),x)-(sp.log(B/x)-1))


def freezing_controls():
    rows=[]
    for eta in [.025,.1,.24]:
        g=1-2*eta
        for R in [8.,32.,128.]:
            M,K,e,A,D=1.,2.,.6,.2,.3
            CZ=3.;Cp=1+CZ;CQ=e*CZ;CV=Cp**2/2+K*CQ
            Lam=e*K/2+M/R+K*K/(2*R*R)
            LR=e*A*D*math.sqrt(R)+(2*e*Lam+CQ/2)*A*A
            ER=2*CQ*A*A+LR/g
            GR=2*D*D/g+((Cp*Cp/2+2*CV)*A*A+2*K*ER)/R
            G1=2*D*D/g+(2*CV*A*A+4*K*ER)/R+(Cp*Cp*A*A/2)*(2*M/R**2+K*K/R**3)
            for U in [1.,32.,4096.]:
                rr=R*4
                opt=Cp*Cp*A*A*U**(-g)/(2*rr**2)
                mass=CV*A*A*U**(-g-1)*math.log1p(U/rr)+D*D/g*U**(-g)
                raw=opt+2*mass/rr+2*K*ER*U**(-g)/rr**2
                rawr=opt*(2*M/rr**2+K*K/rr**3)+2*mass/rr**2+4*K*ER*U**(-g)/rr**3
                assert raw<=GR*U**(-g)/rr*(1+1e-12)
                assert rawr<=G1*U**(-g)/rr**2*(1+1e-12)
                rows.append({'eta':eta,'R':R,'U':U,'metric_majorant_ratio':raw/(GR*U**(-g)/rr),'radial_majorant_ratio':rawr/(G1*U**(-g)/rr**2)})
    return rows


def outgoing_series(q,zeta,mu,v,L,N=14):
    aa=[1.+0j]
    for n in range(N):
        am1=aa[n-1] if n>=1 else 0j;am2=aa[n-2] if n>=2 else 0j
        aa.append(((n*(n+1)+1j*q*(2*n+1))*aa[n]-2*mu*n*n*am1+v*n*(n-1)*am2)/(2j*zeta*(n+1)))
    return np.array([sum(a/L**n for n,a in enumerate(aa)),sum(-n*a/L**(n+1) for n,a in enumerate(aa))],dtype=complex)


def mode(q,R,M,Q,x,angle,L=96.,N=14,rtol=2e-11):
    zeta=cmath.exp(1j*angle);lam=x/R;mu=M*lam;v=Q*Q*lam*lam;B=32.
    def ff(rho):return 1-2*mu/rho+v/rho**2
    def fp(rho):return 2*mu/rho**2-2*v/rho**3
    def rhs_outer(rho,state):
        y,yp=state;f=ff(rho)
        return [yp,-((fp(rho)+2j*(zeta-q/rho))*yp+(1j*q/rho**2-fp(rho)/rho)*y)/f]
    outer=solve_ivp(rhs_outer,(L,B),outgoing_series(q,zeta,mu,v,L,N),method='DOP853',rtol=rtol,atol=rtol*1e-4)
    assert outer.success,outer.message
    y,yp=outer.y[:,-1]
    # Keep the common flat anchored phase outside the Mellin solve for scaling.
    def delta_integrand(t):
        rho=math.exp(t)
        return (zeta*rho-q)*(1/ff(rho)-1)
    lo,hi=math.log(x),math.log(B)
    delta=complex(quad(lambda t:delta_integrand(t).real,lo,hi,epsabs=1e-12)[0],quad(lambda t:delta_integrand(t).imag,lo,hi,epsabs=1e-12)[0])
    fB=ff(B);AB=B*fp(B)/fB;pref=math.sqrt(fB/B)*cmath.exp(1j*delta)
    initial=np.array([pref*y,pref*(B*yp+(AB/2-.5+1j*(zeta*B-q)/fB)*y)],dtype=complex)
    beta2=q*q-.25
    def rhs_inner(t,state):
        rho=math.exp(t);f=ff(rho);fr=fp(rho);frr=-4*mu/rho**3+6*v/rho**4
        Af=rho*fr/f;As=Af+rho*rho*frr/f-Af*Af
        VM=(zeta*rho-q)**2/(f*f)-q*q-Af/2-As/2-Af*Af/4
        return [state[1],-(beta2+VM)*state[0]]
    inner=solve_ivp(rhs_inner,(hi,lo),initial,method='DOP853',rtol=rtol,atol=rtol*1e-4)
    assert inner.success,inner.message
    w,ws=inner.y[:,-1];fx=ff(x);Ax=x*fp(x)/fx
    common=cmath.exp(1j*(zeta*(B-x)-q*math.log(B/x)))
    scaled=common*(math.sqrt(fx)*(ws+(1-Ax)*w/2)+1j*(zeta*x-q)*w/math.sqrt(fx))
    return scaled,delta


@lru_cache(None)
def flat_exact(q,x,angle):
    qq=mp.mpf(str(q));xx=mp.mpf(str(x));zeta=mp.e**(1j*mp.mpf(str(angle)))
    beta=mp.sqrt(qq*qq-mp.mpf('.25'));z=-2j*zeta*xx
    N=mp.exp(-1j*zeta*xx)*xx**(1j*qq)*(-2j*zeta)**(1j*qq)
    W=mp.whitw(-1j*qq,1j*beta,z)
    Wp=mp.diff(lambda zz:mp.whitw(-1j*qq,1j*beta,zz),z)
    return complex(mp.sqrt(xx)*N*(-2j*zeta*Wp+1j*(zeta-qq/xx)*W))


def spectral_controls():
    cases=[];flat_checks=[];convergence=[]
    angles=[0.,math.pi/4,math.pi/2,3*math.pi/4,math.pi]
    for q in [.6,1.]:
        for x in [1e-2,1e-5]:
            for angle in angles:
                d0=flat_exact(q,x,angle)
                dnum,_=mode(q,32.,0.,0.,x,angle)
                err=abs(dnum-d0)/max(abs(d0),1e-15)
                assert err<2e-7,(q,x,angle,'flat normalization',err)
                flat_checks.append({'q':q,'omega_R_modulus':x,'arg_omega':angle,'flat_relative_error':err})
                for R in [32.,128.,512.]:
                    M=1.;Q=q/.6;delta=M/R+Q*Q/R**2
                    df,phase=mode(q,R,M,Q,x,angle)
                    ratio=abs(df-d0)/delta
                    assert np.isfinite(ratio) and abs(df)>1e-8
                    cases.append({'q':q,'R':R,'M':M,'Q':Q,'omega_R_modulus':x,'arg_omega':angle,
                                  'delta':delta,'scaled_abs_denominator':abs(df),'difference_over_delta':ratio,
                                  'anchored_phase_difference_abs':abs(phase),
                                  'smallness_threshold_certified':False})
    for q,R,x,angle in [(.6,32.,1e-5,math.pi/2),(1.,512.,1e-5,math.pi),(.6,128.,1e-2,math.pi/4)]:
        d1,_=mode(q,R,1.,q/.6,x,angle)
        d2,_=mode(q,R,1.,q/.6,x,angle,L=144.,N=18,rtol=3e-12)
        err=abs(d1-d2)/abs(d2)
        assert err<2e-7
        convergence.append({'q':q,'R':R,'omega_R_modulus':x,'arg_omega':angle,'relative_change':err})
    return flat_checks,cases,convergence


def main():
    mp.mp.dps=40
    algebra();freezing=freezing_controls()
    flat,cases,conv=spectral_controls()
    names=['verify_static_geometry_rn_robin.py','STATIC_GEOMETRY_FREEZING_AND_RN_ROBIN.md',
           'MODULATED_BONDI_RADIAL_IMPROVEMENT.md','TIMELIKE_CHARGE_AND_COEFFICIENT_JETS.md',
           'PHYSICAL_TRACE_LOW_FREQUENCY.md','LOW_FREQUENCY_SYMBOL_AND_TIME_TRANSFER.md',
           'DLMF_WHITTAKER_RECEIPT_2026-10-23_R17.json','../../definitions/MODEL.md','ACCEPTANCE.md']
    report={'round':'R28','date':'2026-10-26','logic':'PROVED stated conditional freezing and sufficiently-far fixed-reference threshold lemmas; actual global goal OPEN',
            'evidence':['ANALYTIC','EXACT_ALGEBRA','FINITE_COMPLEX_ODE_CONTROLS'],
            'audit':'INTERNAL_AUDIT; numerical controls are neither interval nor uniform-in-parameter certificates',
            'source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names},
            'algebra':'PASS: metric/charge coefficients, mode gauge, Mellin potential and outgoing recurrence',
            'finite_freezing_majorants':freezing,'flat_normalization_checks':flat,'finite_RN_modes':cases,
            'finite_numerical_convergence_checks':conv,
            'maximum_flat_relative_error':max(x['flat_relative_error'] for x in flat),
            'maximum_difference_over_delta':max(x['difference_over_delta'] for x in cases),
            'minimum_sample_scaled_denominator':min(x['scaled_abs_denominator'] for x in cases),
            'explicit_numeric_sufficient_delta_threshold_computed':False,'continuous_upper_half_plane_theorem_machine_certified':False,
            'actual_A_D_K_uniform_input_verified':False,'actual_worldtube_or_carrier_estimate_verified':False,
            'full_finite_radius_Green_body_estimate_verified':False,'full_frequency_mode_stability_verified':False,
            'actual_extremal_endpoint_or_strong_horizon_verified':False,'goal_A_proved':False}
    target=HERE/'STATIC_GEOMETRY_RN_ROBIN_CHECKS_2026-10-26.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PASS RN20: exact identities; {len(freezing)} freezing, {len(flat)} flat normalizations, {len(cases)} complex RN modes, {len(conv)} convergence controls')
    print(f'Max flat error {report["maximum_flat_relative_error"]:.3e}; minimum sampled scaled |d_f| {report["minimum_sample_scaled_denominator"]:.3e}; actual Goal A OPEN')


if __name__=='__main__':main()
