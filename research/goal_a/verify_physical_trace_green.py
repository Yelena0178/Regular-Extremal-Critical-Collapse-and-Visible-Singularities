"""GREEN14 exact identities and finite cone controls; no full-tail certification."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent


def zero(expr):
    assert s.simplify(s.expand(expr)) == 0, expr


def check_green_endpoints():
    rp, rm, rpp, rmp, k, omega = s.symbols('rp rm rpp rmp k omega', nonzero=True)
    dp, dm = rpp+s.I*k*rp, rmp+s.I*k*rm
    H = (dm*rp-dp*rm)/(-2*s.I*omega)
    Hp = (dm*rpp-dp*rmp)/(-2*s.I*omega)
    wr_sub = {rmp: (rpp*rm-2*s.I*omega)/rp}
    zero((H-1).subs(wr_sub))
    zero(Hp+s.I*k*H)
    zero((H*rpp-Hp*rp-dp).subs(wr_sub))
    zero((H/dp-1/dp).subs(wr_sub))
    zero((Hp+s.I*k*H)/dp)
    r = s.symbols('r')
    R, JH, K, source = (s.Function(n)(r) for n in ['R', 'H', 'k', 'source'])
    current = JH*s.diff(R, r)-s.diff(JH, r)*R
    derivative = s.diff(current, r).subs(s.diff(R, r, 2), source-K**2*R).subs(s.diff(JH, r, 2), -K**2*JH)
    zero(derivative-JH*source)


def check_actual_flux_and_return():
    zeta, zp, psi, Z, W, dc, da, e, R = s.symbols('zeta zp psi Z W dc da e R')
    phi = zeta*psi
    F1 = -dc*(zeta*Z-phi/R)+s.I*e*da*phi
    w0 = zeta*W+zp*psi-s.I*e*da*phi+dc*zeta*Z/2
    effective = zeta*W+zp*psi-s.I*e*da*phi/2+dc*phi/(2*R)
    zero(w0+F1/2-effective)
    assert s.simplify(s.diff(effective, Z)) == 0
    Y, Yr, Yb, Ybr, sigma, phase, k, omega, f0, f1 = s.symbols('Y Yr Yb Ybr sigma phase k omega f0 f1')
    P = (Yb-sigma*phase*Y)/(2*s.I*omega)
    Pr = (Ybr-sigma*phase*(Yr+2*s.I*k*Y))/(2*s.I*omega)
    E1 = (Yr+2*s.I*k*Y)/(2*s.I*omega)-1
    direct = (Yb*f0-Ybr*f1)/(2*s.I*omega)
    returned = sigma*phase*(f1+E1*f1-Y*f0/(2*s.I*omega))
    zero(P*f0-Pr*f1-direct-returned)
    r, R, q, omega = s.symbols('r R q omega', positive=True, real=True)
    theta = omega*(r-R)-q*s.log(r/R)
    zero(s.exp(2*s.I*theta)-s.exp(2*s.I*omega*(r-R))*s.exp(-2*s.I*q*s.log(r/R)))


def check_cone_powers():
    eta = s.symbols('eta', positive=True)
    h, beta, ge, gg = s.Rational(1, 2)-2*eta, s.Rational(1, 2)-eta, 1-3*eta, 1-eta
    zero(ge-beta-h)
    zero(gg-beta-s.Rational(1, 2))
    zero(-s.Rational(1, 2)+eta-h-(-1+3*eta))
    R, t, u = s.symbols('R t u', positive=True)
    r = R+(t-u)/2
    zero(r+(1+u)-(R+1+t/2+u/2))
    zero(s.diff(-2/s.sqrt(R), R)-R**(-s.Rational(3, 2)))


def finite_controls():
    mp.mp.dps = 40
    eta = mp.mpf(1)/8
    h, beta = mp.mpf('.5')-2*eta, mp.mpf('.5')-eta
    ge, gg = 1-3*eta, 1-eta
    cone = []
    for R in map(mp.mpf, [4, 16]):
        for ratio in map(mp.mpf, ['.5', '2', '16', '128']):
            t = R*ratio
            def electric(u):
                rr, U = R+(t-u)/2, 1+u
                return mp.mpf('.5')*U**(-1+3*eta)/mp.sqrt(rr*(rr+U))
            def metric(u):
                rr, U = R+(t-u)/2, 1+u
                return mp.mpf('.5')*U**(-mp.mpf('.5')+eta)*rr**(-mp.mpf('1.5'))*(rr+U)**(-mp.mpf('.5'))
            je = mp.quad(electric, [0, t/2, t])
            jg = mp.quad(metric, [0, t/2, t])
            ne, ng = je*(R+t)**ge, jg*mp.sqrt(R)*(R+t)**gg
            assert 0 < ne < 50 and 0 < ng < 50
            cone.append({'R': str(R), 't_over_R': str(ratio), 'electric_scaled_cone': mp.nstr(ne, 16), 'metric_scaled_cone': mp.nstr(ng, 16)})
    convolution = []
    for t in map(mp.mpf, [0, 1, 8, 64]):
        for gamma in [ge, gg]:
            fn = lambda v: 1/((1+abs(t-v))*(1+v)**gamma)
            parts = [0, 1, mp.inf] if t == 0 else [0, t/2, t, 3*t/2, mp.inf]
            val = mp.quad(fn, parts)*(1+t)**beta
            assert 0 < val < 100
            convolution.append({'t': str(t), 'gamma': str(gamma), 'target_weighted_convolution': mp.nstr(val, 16)})
    def phi(u):
        return mp.exp(4-1/((u-1)*(2-u))) if 1 < u < 2 else mp.mpf(0)
    def psi(v):
        x = v/mp.mpf('.1')
        return mp.exp(1-1/(1-x*x)) if abs(x) < 1 else mp.mpf(0)
    response = mp.quad(lambda v: psi(v)*phi(mp.mpf('1.5')-2*v), [-mp.mpf('.1'), 0, mp.mpf('.1')])
    packets = []
    R = mp.mpf(4)
    for L in map(mp.mpf, [16, 64, 256]):
        old_norm_upper = 3**(1-eta)*mp.quad(lambda v: (L+v)**(-mp.mpf('.5'))*psi(v), [-mp.mpf('.1'), 0, mp.mpf('.1')])
        peak = (1+2*(L-R)+mp.mpf('1.5'))**beta*response
        packets.append({'radial_center': str(L), 'unit_return_model_weighted_response_over_old_norm_upper': mp.nstr(peak/old_norm_upper, 16)})
    assert mp.mpf(packets[-1]['unit_return_model_weighted_response_over_old_norm_upper']) > mp.mpf(packets[0]['unit_return_model_weighted_response_over_old_norm_upper'])
    return cone, convolution, packets


def main():
    check_green_endpoints()
    check_actual_flux_and_return()
    check_cone_powers()
    cone, convolution, packets = finite_controls()
    names = ['verify_physical_trace_green.py', 'PHYSICAL_TRACE_GREEN_AND_DELAY.md',
             'PHYSICAL_TRACE_LOW_FREQUENCY.md', 'ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md',
             'RADIAL_DIVERGENCE_AND_SPECTRAL_CUTOFF.md', 'LOW_FREQUENCY_SYMBOL_AND_TIME_TRANSFER.md',
             'LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md', '../../definitions/MODEL.md', 'ACCEPTANCE.md']
    result = {
        'claim_ids': ['GREEN14.1', 'GREEN14.2', 'GREEN14.3', 'GREEN14.4', 'GREEN14.5'],
        'logic': 'PROVED for full physical-W Green identity, natural boundary cancellation and leading returned amplitude with explicit actual source inputs; returned remainders/derivative/cutoff/full Goal A OPEN',
        'evidence': ['ANALYTIC', 'EXACT_ALGEBRA', 'FINITE_CONE_CONVOLUTION_AND_DELAY_CONTROLS'],
        'audit': 'INTERNAL_AUDIT',
        'checks': ['Green fundamental pair/flux and both inner endpoints',
                   'exact actual effective W cancellation of Z',
                   'direct/returned kernel decomposition and propagation phase',
                   'cone and convolution exponent matching'],
        'cone_controls': cone,
        'convolution_controls': convolution,
        'delayed_packet_negative_control': packets,
        'source_inner_endpoint_retained': True,
        'effective_boundary_Z_cancels': True,
        'propagation_delay_retained': True,
        'leading_returned_actual_amplitude_estimated_with_inputs': True,
        'leading_returned_derivative_tail_verified': False,
        'returned_remainder_kernels_time_estimate_verified': False,
        'negative_time_kernel_bound_uniform_in_radius_verified': False,
        'full_body_future_cutoff_removed': False,
        'actual_W_set_to_zero': False,
        'full_weighted_cutoff_removed': False,
        'actual_uniform_A_eta_verified': False,
        'worldtube_H_tail_verified': False,
        'horizon_strong_limit_verified': False,
        'goal_A_proved': False,
        'source_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names},
    }
    (HERE/'PHYSICAL_TRACE_GREEN_CHECKS_2026-10-24.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: Green/endpoints/effective-W/return/delay identities; 8 cone, 8 convolution and 3 delayed-packet controls')
    print('LIMIT: returned derivative/remainders, spatially uniform negative-time bound, full cutoff/A/H/Goal A are open')


if __name__ == '__main__':
    main()
