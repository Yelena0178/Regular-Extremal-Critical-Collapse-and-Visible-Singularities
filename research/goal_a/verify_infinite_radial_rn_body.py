"""CONE22 controls. Finite quadrature is not a uniform analytic/PDE certificate."""
from pathlib import Path
import hashlib
import json
import math
import platform

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
import sympy as sp

HERE = Path(__file__).resolve().parent


def exact_checks():
    w,q,s,f,A,y,yp = sp.symbols('w q s f A y yp',nonzero=True)
    expr=A*(yp+2*sp.I*(w-q/s)*y/f)/(2*sp.I*w)
    split=A*y/f+A*(yp-2*sp.I*q*y/(s*f))/(2*sp.I*w)
    assert sp.simplify(expr-split)==0
    U,R = sp.symbols('U R',positive=True)
    h=2/sp.sqrt(U)*sp.asinh(sp.sqrt(U/R))
    assert sp.simplify(sp.diff(h,R)+1/(R*sp.sqrt(R+U)))==0
    primitive=2*sp.asinh(sp.sqrt(s/U))
    assert sp.simplify(sp.diff(primitive,s)-1/(sp.sqrt(s)*sp.sqrt(s+U)))==0
    eta,kappa=sp.symbols('eta kappa',real=True)
    p=sp.Rational(3,2)-3*eta;nu=1-eta;rho=sp.Rational(3,2)-kappa
    assert sp.expand(p+sp.Rational(1,2)-rho-(p+kappa-1))==0
    assert sp.expand(p-nu-(sp.Rational(1,2)-2*eta))==0
    cz,G,d=sp.symbols('cz G d',nonnegative=True)
    B=(1+cz)*(d+G/R)
    assert sp.simplify(B-(d+(1+cz)*G/s)-(cz*d+(1+cz)*G*(1/R-1/s)))==0
    assert sp.simplify(B-(cz*d+(1+cz)*G/s)-(d+(1+cz)*G*(1/R-1/s)))==0
    return {'principal_remainder_split':True,'direct_density_primitive':True,
            'deleted_delay_divergent_primitive':True,'strict_exponent_identities':True,
            'actual_source_package_remainders_nonnegative_for_s_ge_R':True,
            'RN_cone_jacobian':'dl/ds=2/f; ds/dl=f/2'}


def params(eta):
    p=1.5-3*eta;beta=max(1-p,0.);kappa=(beta+eta)/2;rho=1.5-kappa;delta=p+kappa-1
    assert 0<eta<.25 and beta<kappa<eta and delta>0 and 1<rho<1.5
    return p,kappa,rho,delta


def hp(t,p):
    if abs(p-1)<1e-12:return math.log1p(t)
    return math.expm1((1-p)*math.log1p(t))/(1-p)


def qfinite(fun,t):
    # Integrate in v so the late-source endpoint v=0 stays explicitly resolved.
    points=sorted(set([0.,t]+[x for x in [1.,10.,100.,1000.,t/2] if 0<x<t]))
    return sum(quad(fun,a,b,epsabs=2e-12,epsrel=2e-10,limit=150)[0] for a,b in zip(points,points[1:]))


def optical_cones():
    rows=[]
    for q in [.6,1.]:
        R=16.;M=1.;Q=q/.6
        f=lambda s:1-2*M/s+Q*Q/s**2
        for a in [R,8*R]:
            for t in [1.,100.,10000.]:
                flow=solve_ivp(lambda l,z:[f(z[0])/2],(0,t),[a],rtol=2e-12,atol=2e-12,dense_output=True)
                assert flow.success
                for ell in [0.,t/3,t]:
                    ss=float(flow.sol(ell)[0]);assert a+ell/4-1e-8<=ss<=a+ell+1e-8
                    assert .5<=f(ss)<=2
                for eta in [.02,1/6,.24]:
                    p,kap,rho,delta=params(eta)
                    def rem(v):
                        ss=float(flow.sol(t-v)[0])
                        return f(ss)/2*(1+v)**(-p)/(ss*math.sqrt(ss+1+v))
                    h=qfinite(rem,t)
                    model=qfinite(lambda v:(1+v)**(-p)/(a+t-v),t)/math.sqrt(a+1+t)
                    major=2**p*(1+t)**(-p-.5)*math.log(2+t)+2*(1+t)**(-1.5)*hp(t,p)
                    assert h<=8*model*(1+1e-8)+1e-12
                    assert model<=major*(1+1e-8)+1e-12
                    assert hp(t,p)<=(1+t)**kap/delta*(1+1e-12)
                    main=[]
                    for T in [R,R+t,R+10*t]:
                        def actual(v):
                            ss=float(flow.sol(t-v)[0])
                            return f(ss)/2*(1+v)**(-p)/(math.sqrt(ss+1+v)*math.sqrt(ss+T))
                        value=qfinite(actual,t)
                        modelj=qfinite(lambda v:(1+v)**(-p)/math.sqrt(a+t-v+T),t)/math.sqrt(a+1+t)
                        upper=math.sqrt(2)*(2**p+1)*hp(t,p)/(math.sqrt(a+1+t)*math.sqrt(a+t+T))
                        assert value<=4*modelj*(1+1e-8)+1e-12
                        assert modelj<=upper*(1+1e-8)+1e-12
                        main.append({'T':T,'actual_to_model':value/modelj,'model_to_split_majorant':modelj/upper})
                    rows.append({'q':q,'anchor':a,'arrival_time':t,'eta':eta,
                                 'remainder_actual_to_model':h/model,'model_to_split_majorant':model/major,
                                 'main_controls':main})
    return rows


def dyadic_controls():
    R=2.;rows=[]
    for r in [R,100*R]:
        for s in [R,100*R,100000*R]:
            for tau in [0.,R,1000*R,1000000*R]:
                T=R+tau
                for j in [0,1]:
                    rem=0.;main=0.
                    for n in range(-140,1):
                        lam=2.**n/R
                        z=min(math.sqrt(lam*r),1)*min(math.sqrt(lam*s),1)*(1+lam*tau)**(-6)
                        rem+=lam**j*z;main+=lam**(j+1)*z
                    rb=math.sqrt(s)*T**(-.5-j)*math.sqrt(r/(r+T))
                    mb=T**(-1-j)*math.sqrt(s/(s+T))
                    assert rem/rb<30 and main/mb<30
                    rows.append({'r':r,'s':s,'tau':tau,'time_derivative':j,
                                 'remainder_sum_to_bound':rem/rb,'main_sum_to_bound':main/mb})
    return rows


def e_integral(u,kappa,j,R=2.,grid_factor=10.):
    U=1+u;a=u/U
    def integrand(y):
        t=U*y;T=R+abs(u-t)
        return U*(1+t)**kappa/(T**(1+j)*math.sqrt(R+t)*math.sqrt(R+t+T))
    upper=max(2.,2*a)
    pts=[0.,a/2,a,1.5*a,upper]
    offset=R/U
    while offset<2*upper:
        pts.extend(x for x in [a-offset,a+offset] if 0<x<upper)
        offset*=grid_factor
    pts=sorted(set(pts))
    parts=[quad(integrand,l,h,epsabs=1e-11,epsrel=1e-9,limit=220)[0] for l,h in zip(pts,pts[1:])]
    parts.append(quad(integrand,pts[-1],np.inf,epsabs=1e-11,epsrel=1e-9,limit=220)[0])
    future=sum(value for lo,value in zip(pts[:-1],parts[:-1]) if lo>=a)+parts[-1]
    return sum(parts),future


def time_controls():
    rows=[]
    for eta in [.02,1/6,.24]:
        p,kap,rho,delta=params(eta)
        for u in [0.,10.,1000.,1000000.]:
            for j in [0,1]:
                val,future=e_integral(u,kap,j)
                major=(1+u)**(kap-1)*(math.log(3+u) if j==0 else 1)
                assert 0<val/major<40
                assert future>0 and future<=val*(1+2e-7)
                rows.append({'eta':eta,'u':u,'j':j,'kappa':kap,'rho':rho,'delta':delta,
                             'E_to_decay_profile':val/major,'future_fraction':future/val,
                             'target_weighted_value':val*(1+u)**(1-eta)})
    return rows


def derivative_convolutions():
    rows=[];R=2.
    for eta in [.02,1/6,.24]:
        p,kap,rho,delta=params(eta)
        for u in [0.,10.,1000.]:
            U=1+u;a=u/U
            fun=lambda y:U*(R+abs(u-U*y))**(-1.5)*(1+U*y)**(-rho)
            pts=sorted(set([0.,a/2,a,1.5*a,max(2.,2*a)]))
            val=sum(quad(fun,l,h,epsabs=1e-11,epsrel=1e-9,limit=150)[0] for l,h in zip(pts,pts[1:]))
            val+=quad(fun,pts[-1],np.inf,epsabs=1e-11,epsrel=1e-9,limit=150)[0]
            assert val*U**rho<20
            rows.append({'eta':eta,'u':u,'rho':rho,'weighted_convolution':val*U**rho})
    return rows


def negative_controls():
    R=2.;U=11.
    radial=[]
    for L in [1e3,1e6,1e9]:
        value=2*(math.asinh(math.sqrt(L/U))-math.asinh(math.sqrt(R/U)))
        radial.append({'L':L,'deleted_delay_radial_integral':value,'ratio_to_log_L':value/math.log(L)})
    assert all(radial[i+1]['deleted_delay_radial_integral']>radial[i]['deleted_delay_radial_integral']+6 for i in range(2))
    endpoint=[]
    for u in [1e2,1e4,1e6]:
        val,_=e_integral(u,.25,0)
        endpoint.append({'u':u,'eta_endpoint_positive_majorant_weighted':val*(1+u)**.75})
    assert endpoint[-1]['eta_endpoint_positive_majorant_weighted']>endpoint[0]['eta_endpoint_positive_majorant_weighted']+2
    return {'deleted_delay':radial,'eta_quarter_endpoint':endpoint,
            'scope':'positive majorant / specified proof strategy only; not an actual D001 or Green lower-bound counterexample'}


def main():
    exact=exact_checks();cones=optical_cones();dyadics=dyadic_controls();times=time_controls();derivs=derivative_convolutions();negative=negative_controls()
    convergence=[]
    for j in [0,1]:
        kap=params(.24)[1]
        first,_=e_integral(1e6,kap,j,grid_factor=10.)
        refined,_=e_integral(1e6,kap,j,grid_factor=3.)
        relative=abs(first-refined)/abs(refined)
        assert relative<2e-6
        convergence.append({'u':1e6,'eta':.24,'j':j,'grid_factors':[10,3],'relative_difference':relative})
    files=['INFINITE_RADIAL_RN_BODY_TRANSFER.md','verify_infinite_radial_rn_body.py',
           'FINITE_RADIUS_RN_GREEN_AND_LOCAL_BODY.md','STATIC_GEOMETRY_FREEZING_AND_RN_ROBIN.md',
           'ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md','MODULATED_BONDI_RADIAL_IMPROVEMENT.md',
           'ACCEPTANCE.md','../../definitions/MODEL.md']
    report={'claim':'CONE22','status':'PASS','audit':'INTERNAL_AUDIT',
            'logic':'PROVED input-to-output implication in proof; actual Goal A OPEN',
            'evidence':['EXACT_ALGEBRA','FINITE_QUADRATURE_CONTROL','FINITE_OPTICAL_ODE_CONTROL'],
            'actual_PDE_evolution':False,'continuous_parameter_or_all_time_machine_certificate':False,
            'python':platform.python_version(),'scipy':scipy.__version__,'exact':exact,
            'optical_cones':cones,'dyadic_controls':dyadics,'time_controls':times,
            'derivative_convolutions':derivs,'negative_controls':negative,'convergence_controls':convergence,
            'quadrature_repair':'Initial unsplit future-only quadrature missed the narrow t=u peak at large u; replaced by geometric subdivisions shared with the full integral and checked with a denser grid.',
            'source_sha256':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in files}}
    path=HERE/'INFINITE_RADIAL_RN_BODY_CHECKS_2026-10-27.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','RN_cones':len(cones),'cone_main_controls':sum(len(x['main_controls']) for x in cones),
                      'dyadic_controls':len(dyadics),'time_controls':len(times),'derivative_convolutions':len(derivs),
                      'negative_controls':'deleted delay and eta=1/4 positive-majorant endpoint',
                      'max_E_to_decay_profile':max(x['E_to_decay_profile'] for x in times),
                      'report':str(path)},ensure_ascii=False))


if __name__=='__main__':main()
