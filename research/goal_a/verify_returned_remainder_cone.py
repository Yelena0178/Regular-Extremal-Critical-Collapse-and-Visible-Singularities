"""RETURN15 exact scalings and finite cone/convolution controls, not PDE certification."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent


def zero(expr):
    assert s.simplify(s.expand(expr)) == 0, expr


def check_remainder_and_density():
    Y, Yr, omega, k = s.symbols('Y Yr omega k', nonzero=True)
    E1 = (Yr+2*s.I*k*Y)/(2*s.I*omega)-1
    zero(E1-((Y-1)+(k/omega-1)*Y+Yr/(2*s.I*omega)))
    r, R, u, z = s.symbols('r R u z', positive=True)
    transform = s.Matrix([u, u+2*(r-R)]).jacobian([u, r])
    zero(transform.det()-2)
    rr = R+(z-u)/2
    zero(rr+(1+u)-(R+1+z/2+u/2))
    zero(s.diff(-2*s.log(rr), u)-1/rr)
    zero(s.diff(2/rr, u)-1/rr**2)
    a, eta = s.symbols('a eta', positive=True)
    primitive = ((1+z)**a-1)/a
    zero(s.diff(primitive, z)-(1+z)**(a-1))
    beta, nu, h = s.Rational(1, 2)-eta, 1-eta, s.Rational(1, 2)-2*eta
    aa = 3*eta
    zero(nu-beta-s.Rational(1, 2))
    zero(s.Rational(3, 2)-aa-nu-h)
    # Exact relation of F0's electric weight to the F1 electric weight.
    U = s.symbols('U', positive=True)
    f1_weight = U**(-s.Rational(1, 2)+eta-h)/(r*s.sqrt(r+U))
    f0_weight = U**(s.Rational(1, 2)+eta-h)/(r*(r+U)**s.Rational(3, 2))
    zero(f0_weight/f1_weight-U/(r+U))
    # The required logarithmic absorption carries R^{-h}; no hidden log R.
    x, hh, nn = s.symbols('x hh nn', positive=True)
    zero((R*x)**(-nn-hh)*x**hh-R**(-hh)*(R*x)**(-nn))
    fun = (1+s.log(x))/x**hh
    critical = s.exp(1/hh-1)
    zero(s.diff(fun, x).subs(x, critical))


def finite_controls():
    mp.mp.dps = 40
    eta = mp.mpf(1)/8
    beta, nu, h, a = mp.mpf('.5')-eta, 1-eta, mp.mpf('.5')-2*eta, 3*eta
    density = []
    for R in map(mp.mpf, [4, 16]):
        for ratio in map(mp.mpf, ['.25', '1', '8', '64']):
            z = R*ratio
            def geo(u):
                rr, U = R+(z-u)/2, 1+u
                return mp.mpf('.5')*U**(-beta)/(rr**2*mp.sqrt(rr+U))
            def electric(u):
                rr, U = R+(z-u)/2, 1+u
                return mp.mpf('.5')*U**(a-1)/(rr*mp.sqrt(rr+U))
            qg = mp.quad(geo, [0, z/2, z])
            qe = mp.quad(electric, [0, z/2, z])
            ng, ne = qg*R*(R+z)**nu, qe*R**h*(R+z)**nu
            assert 0 < ng < 100 and 0 < ne < 100
            density.append({'R': str(R), 'z_over_R': str(ratio), 'metric_target_normalized': mp.nstr(ng, 16), 'electric_target_normalized': mp.nstr(ne, 16)})
    convolution = []
    for R in map(mp.mpf, [1, 4]):
        for ratio in map(mp.mpf, [0, 1, 16, 128]):
            t = R*ratio
            parts = [0, 1, mp.inf] if t == 0 else [0, t/2, t, 3*t/2, mp.inf]
            row = {'R': str(R), 't_over_R': str(ratio)}
            for alpha, weight, label in [(mp.mpf('.5'), beta, 'amplitude'), (mp.mpf('1.5'), nu, 'derivative')]:
                integral = mp.quad(lambda z: (R+z)**(-nu)*(1+abs(t-z))**(-alpha), parts)
                val = integral*(R+t)**weight
                assert 0 < val < 100
                row[label+'_target_normalized'] = mp.nstr(val, 16)
            convolution.append(row)
    log_controls = []
    for gap in map(mp.mpf, ['.25', '.05', '.01']):
        x = mp.exp(1/gap)
        val = (1+mp.log(x))/x**gap
        assert abs(val-mp.exp(-1)*(1+1/gap)) < mp.mpf('1e-35')
        log_controls.append({'h': str(gap), 'log_gain_at_exp_one_over_h': mp.nstr(val, 16)})
    assert mp.mpf(log_controls[-1]['log_gain_at_exp_one_over_h']) > mp.mpf(log_controls[0]['log_gain_at_exp_one_over_h'])
    return density, convolution, log_controls


def main():
    check_remainder_and_density()
    density, convolution, log_controls = finite_controls()
    names = ['verify_returned_remainder_cone.py', 'RETURNED_REMAINDER_CONE_ESTIMATE.md',
             'PHYSICAL_TRACE_GREEN_AND_DELAY.md', 'PHYSICAL_TRACE_LOW_FREQUENCY.md',
             'ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md', 'MODULATED_BONDI_RADIAL_IMPROVEMENT.md',
             'LOW_FREQUENCY_SYMBOL_AND_TIME_TRANSFER.md', '../../definitions/MODEL.md', 'ACCEPTANCE.md']
    result = {
        'claim_ids': ['RETURN15.1', 'RETURN15.2', 'RETURN15.3', 'RETURN15.4', 'RETURN15.5'],
        'logic': 'PROVED for returned remainder rad_eta and full non-cutoff low-frequency body amplitude with explicit actual A/D/K/q inputs; main-return derivative/late cutoff/full-space/Goal A OPEN',
        'evidence': ['ANALYTIC', 'EXACT_ALGEBRA', 'FINITE_DENSITY_CONVOLUTION_AND_LOG_CONTROLS'],
        'audit': 'INTERNAL_AUDIT',
        'checks': ['outgoing E1 leading cancellation',
                   'retarded change of variables/Jacobian and radial primitives',
                   'source weight ratio and cone exponent margins',
                   'logarithmic absorption carries R^{-h}'],
        'density_controls': density,
        'convolution_controls': convolution,
        'log_gap_negative_controls': log_controls,
        'delay_removed_before_symbol_estimate': True,
        'returned_remainder_amplitude_estimated_with_inputs': True,
        'returned_remainder_derivative_estimated_with_inputs': True,
        'all_non_cutoff_low_frequency_body_amplitude_estimated_with_inputs': True,
        'analytic_uniform_kernel_bounds_machine_certified': False,
        'leading_returned_derivative_tail_verified': False,
        'full_body_future_cutoff_removed': False,
        'negative_time_kernel_bound_uniform_in_radius_verified': False,
        'actual_W_set_to_zero': False,
        'actual_uniform_A_eta_verified': False,
        'worldtube_H_tail_verified': False,
        'full_spatial_A_or_high_frequency_verified': False,
        'horizon_strong_limit_verified': False,
        'goal_A_proved': False,
        'source_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names},
    }
    (HERE/'RETURNED_REMAINDER_CHECKS_2026-10-24.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: E1/Jacobian/source/log identities; 8 cone-density, 8 paired-convolution and 3 gap controls')
    print('LIMIT: no machine certification of uniform kernels; main derivative, body cutoff, full A/H/high-frequency/Goal A open')


if __name__ == '__main__':
    main()
