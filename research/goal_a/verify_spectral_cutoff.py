"""CUTOFF12 structures and finite controls; not a certifier of actual tails."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent


def zero(expr):
    assert s.simplify(s.expand(expr)) == 0, expr


def check_radial_integration_and_sign():
    r, R = s.symbols('r R', positive=True)
    d, F, B = s.symbols('d F B', complex=True)
    # Variables here represent the already-conjugated reference mode and Fourier field.
    y = 1-d/r
    g = F+B/r
    lhs = s.integrate(y*s.diff(g, r), (r, R, s.oo))
    rhs = F-y.subs(r, R)*g.subs(r, R)-s.integrate(s.diff(y, r)*g, (r, R, s.oo))
    zero(lhs-rhs)
    zero(lhs.subs(B, 0))
    # A dropped infinity boundary would give -F for an identically zero radial source.
    zero((rhs-F).subs(B, 0)+F)
    omega, chi, integral = s.symbols('omega chi integral', nonzero=True)
    contribution = chi/(2*s.I*omega)*(-2)*integral
    zero((-s.I*omega)*contribution-chi*integral)


def check_radial_dual_and_scaling():
    lam, R, a, b, r = s.symbols('lam R a b r', positive=True)
    # a <= lambda*r <= b is a finite scaled band; coefficients are envelope constants.
    inside = s.integrate(lam*r, (r, R, a/lam))
    transition = (b-a)/lam
    outside = s.integrate(1/(lam**2*r**2), (r, b/lam, s.oo))
    zero(inside+transition+outside-((a**2/2+b-a+1/b)/lam-lam*R**2/2))
    T, M, C = s.symbols('T M C', positive=True)
    # Weighted actual field G/r = eta_T*phi; h_T is a genuine trace, not free data.
    zero((C/T)**2*T*(16*M)-16*C**2*M/T)
    zero((C/T)**2*T*(4*M*R)-4*C**2*M*R/T)
    # The growth bound for F gives the eta_T' F term of C4.
    flux_growth_integral = s.integrate(M*r, (r, T, 2*T))
    zero(flux_growth_integral-s.Rational(3, 2)*M*T**2)
    eps, alpha = s.symbols('eps alpha', positive=True)
    derivative = [eps**(-1)/T, s.sqrt(R/T), eps**(-s.Rational(1, 2))/s.sqrt(T)]
    amplitude = [eps**(-2)/T, R*eps**(-s.Rational(1, 2))/s.sqrt(T), eps**(-s.Rational(3, 2))/s.sqrt(T)]
    exponents_d = [alpha-1, -s.Rational(1, 2), (alpha-1)/2]
    exponents_a = [2*alpha-1, (alpha-1)/2, (3*alpha-1)/2]
    for term, power, coefficient in zip(derivative, exponents_d, [1, s.sqrt(R), 1]):
        zero(term.subs(eps, T**(-alpha))-coefficient*T**power)
    for term, power, coefficient in zip(amplitude, exponents_a, [1, R, 1]):
        zero(term.subs(eps, T**(-alpha))-coefficient*T**power)
    assert all(power.subs(alpha, s.Rational(1, 4)) < 0 for power in exponents_a)
    assert all(power.subs(alpha, s.Rational(3, 4)) < 0 for power in exponents_d)


def check_slow_packet_scaling():
    u, T, eta = s.symbols('u T eta', positive=True)
    psi = s.Function('psi')
    f = T**(-s.Rational(1, 2)+eta)*psi(u/T)
    expected_derivative = T**(-s.Rational(3, 2)+eta)*s.Subs(s.diff(psi(u), u), u, u/T)
    zero(s.diff(f, u)-expected_derivative)
    zero((T**(-s.Rational(3, 2)+eta))**2*T-T**(-2+2*eta))
    zero((T**(-s.Rational(1, 2)+eta)*T)**2/T-T**(2*eta))


def finite_controls():
    mp.mp.dps = 40
    radial = []
    R, a, b = mp.mpf(8), mp.mpf('.15'), mp.mpf('2.2')
    for lam in [mp.mpf('.001'), mp.mpf('.0001'), mp.mpf('.00001')]:
        estimate = lam*((a*a/2+b-a+1/b)/lam-lam*R*R/2)
        assert estimate > 0 and estimate < 4
        radial.append({'lambda': str(lam), 'lambda_times_radial_envelope_integral': mp.nstr(estimate, 16)})
    rates = []
    for T in [mp.mpf(32), mp.mpf(256), mp.mpf(2048)]:
        ea = T**(-mp.mpf(1)/4)
        ed = T**(-mp.mpf(3)/4)
        aval = ea**(-2)/T+R*ea**(-mp.mpf('.5'))/mp.sqrt(T)+ea**(-mp.mpf('1.5'))/mp.sqrt(T)
        dval = ed**(-1)/T+mp.sqrt(R/T)+ed**(-mp.mpf('.5'))/mp.sqrt(T)
        rates.append({'T': str(T), 'amplitude_alpha_1_4_envelope': mp.nstr(aval, 16), 'derivative_alpha_3_4_envelope': mp.nstr(dval, 16)})
    assert mp.mpf(rates[-1]['amplitude_alpha_1_4_envelope']) < mp.mpf(rates[0]['amplitude_alpha_1_4_envelope'])
    assert mp.mpf(rates[-1]['derivative_alpha_3_4_envelope']) < mp.mpf(rates[0]['derivative_alpha_3_4_envelope'])
    def bump(x):
        return mp.exp(4-1/((x-1)*(2-x))) if 1 < x < 2 else mp.mpf(0)
    def bump_derivative(x):
        if not 1 < x < 2: return mp.mpf(0)
        v = (x-1)*(2-x)
        return bump(x)*(3-2*x)/v**2
    energy = mp.quad(lambda x: bump_derivative(x)**2, [1, mp.mpf('1.5'), 2])
    eta = mp.mpf(1)/8
    packets = []
    for T in [mp.mpf(16), mp.mpf(64), mp.mpf(256)]:
        weighted_peak = (1+mp.mpf('1.5')*T)**(mp.mpf('.5')-eta)*T**(-mp.mpf('.5')+eta)
        derivative_energy = T**(-2+2*eta)*energy
        assert weighted_peak > 1
        packets.append({'T': str(T), 'weighted_amplitude_at_peak': mp.nstr(weighted_peak, 16), 'derivative_energy': mp.nstr(derivative_energy, 16)})
    assert mp.mpf(packets[-1]['derivative_energy']) < mp.mpf(packets[0]['derivative_energy'])
    return radial, rates, packets


def main():
    check_radial_integration_and_sign()
    check_radial_dual_and_scaling()
    check_slow_packet_scaling()
    radial, rates, packets = finite_controls()
    names = ['verify_spectral_cutoff.py', 'RADIAL_DIVERGENCE_AND_SPECTRAL_CUTOFF.md',
             'ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md', 'WORLD_TUBE_RADIATION_TRANSFER.md',
             'LOW_FREQUENCY_SYMBOL_AND_TIME_TRANSFER.md', 'FAR_ZONE_RP_AND_COULOMB_BALANCE.md',
             'ACTUAL_BONDI_COMPLETENESS_BRIDGE.md', '../../definitions/MODEL.md', 'ACCEPTANCE.md']
    result = {
        'claim_ids': ['CUTOFF12.1', 'CUTOFF12.2', 'CUTOFF12.3', 'CUTOFF12.4', 'CUTOFF12.5'],
        'logic': 'PROVED for scoped actual cutoff removal in fixed/shrinking frequency bands using mass inputs; zero-frequency joint cancellation and full weighted tails/Goal A OPEN',
        'evidence': ['ANALYTIC', 'EXACT_ALGEBRA', 'FINITE_ENVELOPE_AND_PACKET_CONTROLS'],
        'audit': 'INTERNAL_AUDIT',
        'checks': ['radial integration by parts with both endpoints and Fourier sign',
                   'weighted dual-kernel envelope integral and actual input scalings',
                   'shrinking-band exponents for amplitude and derivative',
                   'slow-packet time/energy/Fourier scaling'],
        'finite_radial_controls': radial,
        'finite_rate_controls': rates,
        'slow_packet_negative_control': packets,
        'negative_controls': ['dropping infinity term creates nonzero output for zero radial source',
                              'spectral-band convergence and small flux do not imply full weighted-amplitude convergence'],
        'actual_mass_inputs_require_uniform_A_H': False,
        'actual_cutoff_removed_on_fixed_nonzero_bands': True,
        'actual_cutoff_amplitude_removed_above_T_minus_alpha_for_alpha_below_1_3': True,
        'actual_cutoff_derivative_removed_above_T_minus_alpha_for_alpha_below_1': True,
        'analytic_uniform_reference_kernels_machine_certified': False,
        'joint_zero_frequency_cancellation_verified': False,
        'full_weighted_cutoff_removed': False,
        'actual_uniform_A_eta_verified': False,
        'worldtube_H_tail_verified': False,
        'full_spatial_A_or_high_frequency_verified': False,
        'horizon_strong_limit_verified': False,
        'goal_A_proved': False,
        'source_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names},
    }
    (HERE/'SPECTRAL_CUTOFF_CHECKS_2026-10-23.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: two-endpoint/Fourier identities, radial/scaling exponents and 9 finite envelope/packet controls')
    print('LIMIT: no machine certification of analytic kernels, joint zero frequency, weighted/full-space tails or Goal A')


if __name__ == '__main__':
    main()
