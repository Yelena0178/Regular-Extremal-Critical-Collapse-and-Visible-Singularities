"""SPACE21: exact identities and bounded auxiliary controls, not a PDE certificate."""
from pathlib import Path
import cmath
import hashlib
import json
import math
import platform

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
import sympy as sp

from verify_static_geometry_rn_robin import outgoing_series

HERE = Path(__file__).resolve().parent


def cq(fun, lo, hi):
    if hi <= lo:
        return 0j
    return complex(quad(lambda s: fun(s).real, lo, hi, epsabs=2e-10, epsrel=2e-10, limit=180)[0],
                   quad(lambda s: fun(s).imag, lo, hi, epsabs=2e-10, epsrel=2e-10, limit=180)[0])


def algebra():
    r, f, fr, k, kr = sp.symbols('r f fr k kr', nonzero=True)
    y, yp, ypp = sp.symbols('y yp ypp')
    gauge = f*ypp+(fr+2*sp.I*k)*yp+(sp.I*kr-k*k/f)*y
    target = f*ypp+(fr+2*sp.I*k)*yp+(sp.I*kr-fr/r)*y
    assert sp.simplify(gauge+(k*k/f-fr/r)*y-target) == 0
    A, B, C, D = sp.symbols('A B C D')
    wr = A*D-C*B
    dp, dm = C+sp.I*k*A, D+sp.I*k*B
    H, Hx = (dm*A-dp*B)/wr, (dm*C-dp*D)/wr
    assert sp.simplify(H-1) == 0
    assert sp.simplify(Hx+sp.I*k) == 0
    assert sp.simplify(H*C-Hx*A-dp) == 0
    e, da, dc, z, psi, W, zp = sp.symbols('e da dc z psi W zp')
    F1 = -dc*(z-psi/r)+sp.I*e*da*psi
    w0 = W+zp-sp.I*e*da*psi+dc*z/2
    assert sp.expand(w0+F1/2-(W+zp-sp.I*e*da*psi/2+dc*psi/(2*r))) == 0
    U, eta = sp.symbols('U eta', positive=True)
    alpha, nu, g = sp.Rational(1,2)-eta, 1-eta, 1-2*eta
    assert sp.expand(nu+g-g-alpha) == sp.Rational(1,2)
    model = U**(-alpha)*sp.sqrt(r/(r+U))
    assert sp.simplify(sp.diff(model,r)/model-U/(2*r*(r+U))) == 0
    return {'gauge_transform':True, 'H_value_derivative_and_Wronskian':True,
            'physical_endpoint_cancellation':True, 'source_saturation_exponent':True,
            'profile_radial_derivative':True,
            'measure_identity':'f(s) dx_s = ds',
            'jump_identity':'f(r) [T_r] = 1; y_r diagonal = F1/f'}


def case(q, R, omega_R, rtol=3e-11):
    M, Q, omega = 1., q/.6, omega_R/R
    lam, zeta = abs(omega), float(np.sign(omega))
    B, L = 64/lam, 4*R
    def f(r): return 1-2*M/r+Q*Q/r**2
    def fp(r): return 2*M/r**2-2*Q*Q/r**3
    def k(r): return omega-q/r
    def rhs(r,state):
        y, yp = state
        return [yp,-((fp(r)+2j*k(r))*yp+(1j*q/r**2-fp(r)/r)*y)/f(r)]
    init = outgoing_series(q,zeta,M*lam,Q*Q*lam*lam,64.,16)
    init[1] *= lam
    J = f(B)*(init[0].conjugate()*init[1]).imag+k(B)*abs(init[0])**2
    assert omega/J > 0
    init *= math.sqrt(omega/J)
    opts = dict(method='DOP853',rtol=rtol,atol=rtol*1e-3,dense_output=True)
    out = solve_ivp(rhs,(B,R),init,**opts)
    hom = solve_ivp(rhs,(R,B),np.array([1.,-2j*k(R)/f(R)],complex),**opts)
    assert out.success and hom.success
    def ys(r): return out.sol(r)
    def hs(r): return hom.sol(r)
    yr, ypr = ys(R)
    dp = f(R)*ypr+2j*k(R)*yr
    sigma = f(R)*ypr.conjugate()/dp
    def theta(s): return quad(lambda t:k(t)/f(t),R,s,epsabs=1e-11,epsrel=1e-11)[0]
    def phase(s): return cmath.exp(2j*theta(s))
    a1, a0 = .13+.05j, (.07-.03j)/R
    def sources(s):
        z = (s-R)/(L-R)
        if z >= 1: return 0j,0j,0j
        h = math.exp(-z)*(1-z)**4
        hp = -math.exp(-z)*(1-z)**3*(5-z)/(L-R)
        return a1*h,a0*h,a1*hp
    w0 = (.2+.1j)/R
    def forced(s,state):
        v = rhs(s,state)
        F1,F0,F1p = sources(s)
        return [v[0],v[1]+(F1p+F0)/f(s)]
    particular = solve_ivp(forced,(R,B),np.array([0.,-2*w0/f(R)],complex),**opts)
    assert particular.success
    yB,ypB = ys(B)
    out_imp = ypB/yB
    hB,hpB = hs(B)
    pB,ppB = particular.sol(B)
    coeff = -(ppB-out_imp*pB)/(hpB-out_imp*hB)
    def direct(r): return particular.sol(r)+coeff*hs(r)
    def kernels(r,s):
        h,hp = hs(min(r,s)); y,yp = ys(max(r,s))
        pref = phase(s)/dp
        if s < r:
            T,Ts = pref*h*y,pref*(hp+2j*k(s)*h/f(s))*y
            Tr,Trs = pref*h*yp,pref*(hp+2j*k(s)*h/f(s))*yp
        else:
            T,Ts = pref*h*y,pref*h*(yp+2j*k(s)*y/f(s))
            Tr,Trs = pref*hp*y,pref*hp*(yp+2j*k(s)*y/f(s))
        return T,Ts,Tr,Trs
    errors, negatives, decomp, jumps = [],[],[],[]
    F1R = sources(R)[0]; weff = w0+F1R/2
    for r in [R,1.7*R,3*R,5*R]:
        points = sorted(set([R,min(max(r,R),L),L]))
        def integrate(fun): return sum(cq(fun,a,b) for a,b in zip(points,points[1:]))
        def body(s):
            T,Ts,Tr,Trs = kernels(r,s); F1,F0,_ = sources(s)
            return T*F0-Ts*F1
        def bodyr(s):
            T,Ts,Tr,Trs = kernels(r,s); F1,F0,_ = sources(s)
            return Tr*F0-Trs*F1
        pred = -2*ys(r)[0]*weff/dp+integrate(body)
        pred_r = -2*ys(r)[1]*weff/dp+sources(r)[0]/f(r)+integrate(bodyr)
        sol,solr = direct(r)
        raw = -2*ys(r)[0]*w0/dp+integrate(lambda s:kernels(r,s)[0]*(sources(s)[1]+sources(s)[2]))
        wrong_measure = -2*ys(r)[0]*w0/dp+integrate(lambda s:kernels(r,s)[0]*(sources(s)[1]+sources(s)[2])/f(s))
        errors.append({'r_over_R':r/R,'solution_relative':abs(pred-sol)/(1+abs(sol)),
                       'radial_relative':abs(pred_r-solr)/(1+abs(solr)),
                       'integration_by_parts':abs(pred-raw)/(1+abs(pred))})
        negatives.append({'r_over_R':r/R,'omit_endpoint_error':abs(ys(r)[0]*F1R/dp),
                          'wrong_ds_over_f_error':abs(wrong_measure-raw),
                          'omit_diagonal_error':abs(sources(r)[0]/f(r))})
        for s in [1.1*R,2*R,3.5*R]:
            yr0,ys0 = ys(r)[0],ys(s)[0]
            first = yr0*ys0.conjugate() if r>=s else cmath.exp(2j*(theta(s)-theta(r)))*yr0.conjugate()*ys0
            dec = (first-sigma*phase(s)*yr0*ys0)/(2j*omega)
            decomp.append(abs(dec-kernels(r,s)[0])/(1+abs(dec)))
        h,hp = hs(r); y,yp = ys(r)
        jump = phase(r)*(h*yp-hp*y)/dp
        jumps.append(abs(f(r)*jump-1))
    errmax = max(v[key] for v in errors for key in ['solution_relative','radial_relative','integration_by_parts'])
    assert errmax < 3e-7, (q,R,omega_R,errors)
    assert max(decomp+jumps) < 3e-7, (decomp,jumps)
    assert min(v['omit_endpoint_error'] for v in negatives) > 1e-4
    assert min(v['wrong_ds_over_f_error'] for v in negatives) > 1e-5
    assert negatives[0]['omit_diagonal_error'] > .1
    delay = 2*quad(lambda s:1/f(s),R,L)[0]
    assert abs(delay-2*(L-R)) > 1
    return {'q':q,'R':R,'omega_R':omega_R,'outer_scaled_radius':64,'series_order':16,
            'errors':errors,'negative_controls':negatives,
            'max_decomposition_error':max(decomp),'max_jump_error':max(jumps),
            'RN_return_delay_at_L':delay,'flat_delay_at_L':2*(L-R),
            'finite_outer_flux_normalization':True}


def convolution_controls():
    rows=[]
    R=2.
    for r in [2.,32.,512.]:
        def b(t):
            T=R+abs(t)
            return T**(-.5)*math.sqrt(r/(r+T))
        for u in [0.,8.,256.]:
            for gamma in [1.28,1.7,2.]:
                for delay in [0.,32.]:
                    fun=lambda v:b(u-v-delay)*(1+v)**(-gamma)
                    split=max(u-delay,0.)
                    val=(quad(fun,0,split,epsabs=1e-10)[0] if split else 0.)
                    val+=quad(fun,split,np.inf,epsabs=1e-10,limit=250)[0]
                    assert 0<val/b(u)<120
                    rows.append({'r':r,'u':u,'gamma':gamma,'delay':delay,'convolution_to_B_ratio':val/b(u)})
    return rows


def dyadic_controls():
    rows=[];R=2.
    for r in [R,64*R,10000*R]:
        for t in [R,100*R,100000*R]:
            val=0.
            for n in range(-100,1):
                lam=2.**n/R
                val+=math.sqrt(R*lam)*min(math.sqrt(lam*r),1)*(1+lam*t)**(-4)
            target=math.sqrt(R)*(R+t)**(-.5)*math.sqrt(r/(r+R+t))
            assert val/target<20
            rows.append({'r':r,'t':t,'positive_dyadic_sum_to_bound_ratio':val/target})
    return rows


def main():
    exact=algebra()
    modes=[case(q,R,wr) for q in [.6,1.] for R in [16.,64.] for wr in [-.2,.06,.2]]
    conv=convolution_controls();dyadic=dyadic_controls()
    receipt_files=['FINITE_RADIUS_RN_GREEN_AND_LOCAL_BODY.md','verify_finite_radius_rn_green.py',
                   'verify_static_geometry_rn_robin.py','STATIC_GEOMETRY_FREEZING_AND_RN_ROBIN.md',
                   'ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md','PHYSICAL_TRACE_GREEN_AND_DELAY.md',
                   'FULL_SPACE_PHYSICAL_TRACE_AUDIT.md','ACCEPTANCE.md','../../definitions/MODEL.md']
    report={'claim':'SPACE21','status':'PASS','logic':'analytic results separately scoped in proof; Goal A OPEN',
            'evidence':['EXACT_ALGEBRA','FINITE_ODE_CONTROL','FINITE_QUADRATURE_CONTROL'],
            'audit':'INTERNAL_AUDIT','actual_PDE_evolution':False,
            'continuous_parameter_or_infinite_time_certificate':False,
            'python':platform.python_version(),'scipy':scipy.__version__,
            'exact':exact,'mode_controls':modes,'convolution_controls':conv,'dyadic_controls':dyadic,
            'source_saturation':'sup_U U^gamma |F1| = d A / sqrt(r), radial integral = d A log(L/R)',
            'source_sha256':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in receipt_files}}
    path=HERE/'FINITE_RADIUS_RN_GREEN_CHECKS_2026-10-26.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    maxsol=max(v['solution_relative'] for m in modes for v in m['errors'])
    maxjump=max(m['max_jump_error'] for m in modes)
    print(json.dumps({'status':'PASS','modes':len(modes),'observations':sum(len(m['errors']) for m in modes),
                      'convolution_controls':len(conv),'dyadic_controls':len(dyadic),
                      'max_solution_relative_error':maxsol,'max_jump_error':maxjump,
                      'report':str(path)},ensure_ascii=False))


if __name__=='__main__':
    main()
