"""TRACE17 exact structures and finite Mellin controls, not actual-input certification."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent


def zero(expr):
    assert s.simplify(s.expand(expr)) == 0, expr


def check_series_and_input_structure():
    a, b, y, n0, n1 = s.symbols('a b y n0 n1')
    for N in range(1, 5):
        series = n0+(b*n1-a*n0)*sum((-a)**(n-1)*y**n for n in range(1, N+1))
        remainder = (b*n1-a*n0)*(-a)**N*y**(N+1)/(1+a*y)
        zero((n0+b*y*n1)/(1+a*y)-series-remainder)
    u, omega, nu, Omega, gamma = s.symbols('u omega nu Omega gamma', positive=True)
    theta = s.Function('theta')(u)
    amp = s.Function('amp')(u)
    phase = s.exp(s.I*(omega*u-theta))
    v = omega-s.diff(theta, u)
    boundary = phase*amp/(s.I*v)
    zero(s.diff(boundary, u)-phase*amp-phase*s.diff(amp/(s.I*v), u))
    for k in range(1, 5):
        theta_prime = Omega+gamma/(1+u)
        zero(s.diff(theta_prime, u, k)*(1+u)**k-(-1)**k*s.factorial(k)*gamma/(1+u))
    for k in range(5):
        envelop = (1+u)**(-nu)
        rising = s.rf(nu, k)
        zero(s.diff(envelop, u, k)-(-1)**k*rising*(1+u)**(-nu-k))
    # Inner-cone target exponent is exactly nu, unlike the radiation exponent.
    eta = s.symbols('eta', positive=True)
    zero((s.Rational(1, 2)-eta)+s.Rational(1, 2)-(1-eta))


def mode_and_gamma_controls():
    modes, gamma_values, periodic = [], [], []
    R = mp.mpf(1)
    for q in map(mp.mpf, ['.6', '1']):
        beta = mp.sqrt(q*q-mp.mpf('.25'))
        A = mp.gamma(-2j*beta)/mp.gamma(mp.mpf('.5')-1j*beta+1j*q)
        B = mp.gamma(2j*beta)/mp.gamma(mp.mpf('.5')+1j*beta+1j*q)
        cp, cm = mp.mpf('.5')+1j*(beta-q), mp.mpf('.5')-1j*(beta+q)
        bb = A/B
        aa = bb*cp/cm
        kappa = abs(aa)*mp.exp(mp.pi*beta)
        assert kappa < 1 and abs(bb-aa) > 0
        coefficients = []
        primitive_sum = mp.mpf(0)
        for n in range(1, 41):
            alpha = 2*n*beta
            exact = abs(mp.gamma(1-1j*alpha))**(-1)
            identity = mp.sqrt(mp.sinh(mp.pi*alpha)/(mp.pi*alpha))
            relative = abs(exact/identity-1)
            assert relative < mp.mpf('1e-48')
            coefficient = (-2*(bb-aa)/cm)*(-aa)**(n-1)/mp.gamma(-1j*alpha)
            coefficients.append(coefficient)
            primitive_sum += abs((-2*(bb-aa)/cm)*(-aa)**(n-1)/mp.gamma(1-1j*alpha))
            if n in (1, 10, 20, 40):
                gamma_values.append({'q': str(q), 'n': n, 'Gamma_identity_relative_error': mp.nstr(relative, 9), 'partial_absolute_primitive_sum': mp.nstr(primitive_sum, 16)})
        def tail_profile(x):
            z = mp.exp(-2j*beta*x)
            val = mp.mpc(0)
            for coefficient in reversed(coefficients): val = (val+coefficient)*z
            return val
        period = mp.pi/beta
        total = mp.mpf(0)
        for k in range(256):
            value = tail_profile(period*(k+mp.mpf('.5'))/256)
            total += abs(value)**2/mp.sqrt(abs(value)**2+mp.mpf('.01'))
        mean = total/256
        assert mean > 0
        periodic.append({'q': str(q), 'kappa': mp.nstr(kappa, 16), 'truncated_tail_terms': 40, 'periodic_grid_points': 256, 'positive_phase_alignment_mean': mp.nstr(mean, 16), 'one_log_period_integral': mp.nstr(period*mean, 16), 'four_log_periods_integral': mp.nstr(4*period*mean, 16)})
        wf = lambda z: mp.whitw(-1j*q, 1j*beta, z)
        for r in map(mp.mpf, [1, 4, 16, 64]):
            ell = r/R
            for rho in map(mp.mpf, ['.001', '.00001']):
                for sign in (-1, 1):
                    omega = sign*rho/r
                    zR, zr = -2j*omega*R, -2j*omega*r
                    bop = zR*mp.diff(wf, zR)-(zR/2+1j*q)*wf(zR)
                    theta = omega*(r-R)-q*mp.log(ell)
                    exact = -2*R*mp.exp(-1j*theta)*wf(zr)/bop
                    yy = zR**(2j*beta)
                    leading = -2*mp.sqrt(R*r)*ell**(1j*q)/cm*(ell**(-1j*beta)+bb*yy*ell**(1j*beta))/(1+aa*yy)
                    normalized = abs(exact-leading)/(mp.sqrt(R*r)*rho)
                    assert mp.isfinite(normalized) and normalized < mp.mpf('1e5')
                    modes.append({'q': str(q), 'r_over_R': str(ell), 'abs_omega_r': str(rho), 'sign_omega': sign, 'scaled_small_mode_remainder': mp.nstr(normalized, 14)})
    return modes, gamma_values, periodic


def envelope_moment_controls():
    controls = []
    R = mp.mpf(1)
    for r in map(mp.mpf, [1, 4, 16]):
        for ratio in map(mp.mpf, [4, 16]):
            t = r*ratio
            bound = lambda tau: mp.sqrt(R)*(R+tau)**(-mp.mpf('.5'))*mp.sqrt(r/(r+tau))
            integral = 2*mp.quad(lambda tau: tau*bound(tau), [0, R, r, t/2])
            normalized = integral/(mp.sqrt(R*r)*t)
            assert 0 < normalized < 10
            controls.append({'r': str(r), 't_over_r': str(ratio), 'normalized_kernel_moment_envelope': mp.nstr(normalized, 16)})
    return controls


def main():
    mp.mp.dps = 60
    check_series_and_input_structure()
    receipt = json.loads((HERE/'DLMF_MELLIN_GAMMA_RECEIPT_2026-10-24_R25.json').read_text())
    assert len(receipt['entries']) == 2 and receipt['raw_page_bytes_saved_or_hashed'] is False
    modes, gamma_values, periodic = mode_and_gamma_controls()
    moment = envelope_moment_controls()
    names = ['verify_full_space_trace.py', 'FULL_SPACE_PHYSICAL_TRACE_AUDIT.md',
             'DLMF_MELLIN_GAMMA_RECEIPT_2026-10-24_R25.json', 'PHYSICAL_TRACE_LOW_FREQUENCY.md',
             'UNIFORM_UPPER_KERNEL_AND_FUTURE_LOCALIZATION.md', 'DLMF_KUMMER_EULER_RECEIPT_2026-10-24_R24.json',
             'TAIL_CURRENT_AND_CARRIER_AUDIT.md', '../../definitions/MODEL.md', 'ACCEPTANCE.md']
    result = {
        'claim_ids': ['TRACE17.1', 'TRACE17.2', 'TRACE17.3', 'TRACE17.4', 'TRACE17.5', 'TRACE17.6'],
        'logic': 'PROVED for auxiliary pure-boundary kernels, H-only mapping refutation and carrier-compatible sufficient trace class; actual trace inputs/body/high-frequency/Goal A OPEN',
        'evidence': ['ANALYTIC', 'EXACT_ALGEBRA', 'PRIMARY_GAMMA_IDENTITIES', 'FINITE_MODE_MELLIN_AND_MOMENT_CONTROLS'],
        'audit': 'INTERNAL_AUDIT',
        'checks': ['finite geometric-series remainder',
                   'nonstationary integration-by-parts sign and envelope/phase conormal orders',
                   'Gamma modulus, primitive summability and nonzero periodic tail',
                   'finite-radius small-frequency mode expansion and kernel moment envelope'],
        'mode_controls': modes,
        'gamma_primitive_controls': gamma_values,
        'periodic_alignment_controls': periodic,
        'kernel_moment_controls': moment,
        'finite_controls_are_interval_certificates': False,
        'analytic_uniform_operator_norm_machine_certified': False,
        'H_eta_alone_suffices_for_auxiliary_full_A': False,
        'H_only_failure_is_D001_counterexample': False,
        'pure_boundary_full_A_with_extra_trace_conditions_proved': True,
        'nonzero_carrier_channel_excluded': False,
        'final_constant_carrier_assumed': False,
        'actual_trace_channel_conditions_verified': False,
        'actual_uniform_A_eta_verified': False,
        'worldtube_H_tail_verified': False,
        'finite_radius_body_source_estimate_verified': False,
        'full_high_frequency_verified': False,
        'horizon_strong_limit_verified': False,
        'goal_A_proved': False,
        'source_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names},
    }
    (HERE/'FULL_SPACE_TRACE_CHECKS_2026-10-24.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: series/nonstationary/envelope identities; 32 mode, 8 Gamma, 2 periodic and 6 moment controls')
    print('LIMIT: H-only refutation is auxiliary; actual extra trace inputs, finite-r body, high frequency and Goal A remain open')


if __name__ == '__main__':
    main()
