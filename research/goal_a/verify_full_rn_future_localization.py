"""LOCAL23: auxiliary finite controls; no actual EMCSF evolution or uniform certificate."""
from pathlib import Path
import hashlib
import json
import math
import platform

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp, simpson
import sympy as sp

from verify_static_geometry_rn_robin import outgoing_series

HERE=Path(__file__).resolve().parent


def exact_checks():
    r,b,c,Q,v2,p2=sp.symbols('r b c Q v2 p2',positive=True)
    mu=-r*r*v2/b+c*c*r*r*p2/(4*b)
    mr=Q*Q/(2*r*r)+r*r*c*p2/(2*b)
    assert sp.simplify(mu-c*mr/2+r*r*v2/b+c*Q*Q/(4*r*r))==0
    f,fr,k,kr,y,yp,p,pp=sp.symbols('f fr k kr y yp p pp',nonzero=True)
    ypp=-((fr+2*sp.I*k)*yp+(sp.I*kr-fr/r)*y)/f
    ppp=-((fr-2*sp.I*k)*pp+(-sp.I*kr-fr/r)*p)/f
    current_derivative=fr*(p*yp-pp*y)+f*(p*ypp-ppp*y)+2*sp.I*kr*p*y+2*sp.I*k*(pp*y+p*yp)
    assert sp.simplify(current_derivative)==0
    R,obs,L=sp.Integer(1),sp.Integer(3),sp.Integer(5)
    s=sp.symbols('s',real=True)
    gout=sp.exp(-s);Tout=s*s;Tin=9*sp.exp(-(s-3))
    raw=-2*sp.exp(-1)-2*sp.integrate(Tout*sp.diff(gout,s),(s,R,obs))-2*sp.integrate(Tin*sp.diff(gout,s),(s,obs,L))
    split=-18*sp.exp(-3)+2*sp.integrate(sp.diff(Tout,s)*gout,(s,R,obs))-2*sp.integrate(Tin*sp.diff(gout,s),(s,obs,L))
    assert sp.simplify(raw-split)==0
    h,x,rr=sp.symbols('h x rr',positive=True)
    norm2=rr**2/(2*h)+rr/(2*h*h)+1/(4*h**3)
    assert sp.simplify(sp.integrate((rr+x)**2*sp.exp(-2*h*x),(x,0,sp.oo))-norm2)==0
    return {'incoming_mass_identity':True,'P_Y_bilinear_current_conserved':True,
            'finite_radial_split_and_endpoint_signs':True,
            'omitted_diagonal_negative_control_error':float(18*sp.exp(-3)),
            'weighted_incoming_exponential_norm':str(norm2),
            'scope_of_negative_controls':'specified integration/majorant steps; not a D001 counterexample'}


def cq(fun,a,b):
    return complex(quad(lambda x:fun(x).real,a,b,epsabs=2e-10,epsrel=2e-9,limit=220)[0],
                   quad(lambda x:fun(x).imag,a,b,epsabs=2e-10,epsrel=2e-9,limit=220)[0])


def complex_case(q,R,wr,hi,rtol=3e-11):
    M=1.;Q=q/.6;omega=(wr+1j*hi)/R;lam=abs(omega);zeta=omega/lam;x0=lam*R
    mu=M*lam;vv=Q*Q*lam*lam;end=96.
    ff=lambda x:1-2*mu/x+vv/x**2
    fp=lambda x:2*mu/x**2-2*vv/x**3
    kk=lambda x:zeta-q/x
    def yrhs(x,z):
        y,yp=z
        return [yp,-((fp(x)+2j*kk(x))*yp+(1j*q/x**2-fp(x)/x)*y)/ff(x)]
    opts=dict(method='DOP853',rtol=rtol,atol=rtol*1e-3,dense_output=True)
    ys=solve_ivp(yrhs,(end,x0),outgoing_series(q,zeta,mu,vv,end,16),**opts)
    assert ys.success
    y0,yp0=ys.sol(x0);dscaled=ff(x0)*yp0+2j*kk(x0)*y0
    def prhs(x,z):
        p,pp,theta=z
        return [pp,-((fp(x)-2j*kk(x))*pp+(-1j*q/x**2-fp(x)/x)*p)/ff(x),kk(x)/ff(x)]
    ps=solve_ivp(prhs,(x0,end),np.array([1/dscaled,0j,0j]),**opts)
    assert ps.success
    grid=np.geomspace(x0,end,900)
    yy=ys.sol(grid);pv=ps.sol(grid)
    current=ff(grid)*(pv[0]*yy[1]-pv[1]*yy[0])+2j*kk(grid)*pv[0]*yy[0]
    err=float(np.max(abs(current-1)))
    assert err<3e-7,err
    forward_errors=[]
    for endx in [2*x0,1.,8.]:
        pe,pp,te=ps.sol(endx)
        def integrand(t):
            pt,_,tt=ps.sol(t)
            return np.exp(2j*(te-tt))*(1j*q/t**2+fp(t)/t)*pt
        rhs=cq(integrand,x0,endx)/ff(endx)
        forward_errors.append(abs(rhs-pp)/(1+abs(pp)))
    assert max(forward_errors)<3e-7,forward_errors
    weighted=float(math.sqrt(simpson(grid**2*abs(pv[1])**2,x=grid)))
    return {'q':q,'R':R,'omega_R_real':wr,'omega_R_imag':hi,'scaled_outer_endpoint':end,
            'max_bilinear_current_error':err,'forward_integral_errors':forward_errors,
            'max_scaled_P':float(max(abs(pv[0]))),'max_Y':float(max(abs(yy[0]))),
            'finite_scaled_weighted_P_prime_norm':weighted,
            'norm_to_height_profile':weighted/(1+zeta.imag**(-1.5)),
            'finite_grid_not_spatial_infinity_certificate':True}


def transport_controls():
    rows=[];M=2.;R=4.;b=.8;c=.5;e=.6
    for duration in [1.,10.,100.]:
        for frequency in [0.,3.]:
            for initial in [0.,1.]:
                r0=R+duration
                def rhs(t,z):
                    r=r0-c*t/2
                    flux=math.sqrt(2*M/duration)*math.sin(math.pi*t/duration)*np.exp(1j*frequency*t)
                    a=1/r
                    return [math.sqrt(b)*flux-(c/(2*r)+1j*e*a)*z[0],abs(flux)**2]
                sol=solve_ivp(rhs,(0,duration),np.array([initial+0j,0j]),method='DOP853',rtol=2e-11,atol=2e-12,dense_output=True)
                assert sol.success
                grid=np.linspace(0,duration,301);zz=sol.sol(grid)
                envelope=initial+np.sqrt(M*grid)
                assert np.max(abs(zz[0])-envelope)<2e-9
                assert abs(zz[1,-1].real-M)<2e-8
                rows.append({'duration':duration,'frequency':frequency,'B0':initial,
                             'flux_budget_error':abs(zz[1,-1].real-M),
                             'max_transport_to_envelope':float(np.max(abs(zz[0,1:])/envelope[1:])),
                             'scope':'auxiliary covariant transport with prescribed L2 flux; not an EMCSF solution'})
    return rows


def kernel_budget_controls():
    rows=[]
    for R in [1.,16.]:
        for h in [.001,.1,1.]:
            decay_norm=math.sqrt(R*R/(2*h)+R/(2*h*h)+1/(4*h**3))
            polynomial_norm=1/(h*math.sqrt(R))
            profile=(decay_norm+polynomial_norm)/(1+h**(-1.5))
            assert profile<40
            rows.append({'R':R,'height':h,'weighted_P_prime_majorant_to_profile':profile})
    neg=[]
    for r in [2.,20.,200.]:
        h=.1
        norm=math.sqrt(r*r/(2*h)+r/(2*h*h)+1/(4*h**3))
        neg.append({'observer':r,'weighted_incoming_majorant_norm':norm})
    assert neg[-1]['weighted_incoming_majorant_norm']>10*neg[0]['weighted_incoming_majorant_norm']
    return rows,neg


def time_controls():
    rows=[]
    for T in [10.,1000.,1000000.]:
        for ratio in [0.,.5]:
            for N in [4,6]:
                cut=quad(lambda z:math.sqrt(z)*(1/T+z-ratio)**(-N),1,2,epsabs=1e-11)[0]
                future=quad(lambda z:math.sqrt(z)*(1/T+z-ratio)**(-N),1,np.inf,epsabs=1e-11)[0]
                assert 0<cut<2**(N+2) and 0<future<2**(N+3)
                rows.append({'T':T,'u_over_T':ratio,'N':N,'cut_to_T_half_minus_N':cut,
                             'future_to_T_three_halves_minus_N':future})
    return rows


def main():
    exact=exact_checks()
    modes=[complex_case(q,R,wr,hi) for q,R in [(.6,32.),(1.,128.)] for wr in [-.03,.03] for hi in [.0003,.003,.015]]
    transport=transport_controls();budgets,negative=kernel_budget_controls();times=time_controls()
    files=['FULL_RN_FUTURE_LOCALIZATION.md','verify_full_rn_future_localization.py',
           'verify_static_geometry_rn_robin.py','STATIC_GEOMETRY_FREEZING_AND_RN_ROBIN.md',
           'FINITE_RADIUS_RN_GREEN_AND_LOCAL_BODY.md','UNIFORM_UPPER_KERNEL_AND_FUTURE_LOCALIZATION.md',
           'INFINITE_RADIAL_RN_BODY_TRANSFER.md','TIMELIKE_CHARGE_AND_COEFFICIENT_JETS.md',
           'MODULATED_BONDI_RADIAL_IMPROVEMENT.md','ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md',
           'ACCEPTANCE.md','../../definitions/MODEL.md']
    report={'claim':'LOCAL23','status':'PASS','audit':'INTERNAL_AUDIT',
            'logic':'scoped analytic implications in proof; actual Goal A OPEN',
            'evidence':['EXACT_ALGEBRA','FINITE_COMPLEX_ODE_CONTROL','FINITE_TRANSPORT_CONTROL','FINITE_QUADRATURE_CONTROL'],
            'actual_PDE_evolution':False,'uniform_analytic_or_infinite_time_machine_certificate':False,
            'python':platform.python_version(),'scipy':scipy.__version__,'exact':exact,
            'complex_modes':modes,'transport_controls':transport,'kernel_budget_controls':budgets,
            'weighted_incoming_negative_controls':negative,'time_controls':times,
            'source_sha256':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in files}}
    path=HERE/'FULL_RN_FUTURE_LOCALIZATION_CHECKS_2026-10-27.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','complex_modes':len(modes),'forward_integral_controls':sum(len(x['forward_integral_errors']) for x in modes),
                      'transport_controls':len(transport),'kernel_budget_controls':len(budgets),'time_controls':len(times),
                      'max_bilinear_current_error':max(x['max_bilinear_current_error'] for x in modes),
                      'max_forward_integral_error':max(max(x['forward_integral_errors']) for x in modes),
                      'report':str(path)},ensure_ascii=False))


if __name__=='__main__':main()
