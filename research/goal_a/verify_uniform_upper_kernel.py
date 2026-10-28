"""UPPER16 provenance/identities and finite complex controls, not uniform PDE certification."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent


def zero(expr):
    assert s.simplify(s.expand(expr)) == 0, expr


def check_parameters_gauge_and_rates():
    q, beta = s.symbols('q beta', positive=True, real=True)
    for sign in (-1, 1):
        ss = s.Rational(1, 2)+sign*s.I*beta
        aa, bb = ss+s.I*q, 2*ss
        zero(bb-aa-(ss-s.I*q))
        assert s.re(aa) == s.Rational(1, 2)
        assert s.re(bb-aa) == s.Rational(1, 2)
        # The leading y=0 power is constant in r after the outgoing gauge phase.
        rr, lam = s.symbols('rr lam', positive=True)
        alpha = ss-s.I*q
        zero(s.diff(rr**(-s.I*q)*(lam*rr)**(ss-alpha), rr))
        zero((ss-s.I*q)-alpha)
    r = s.symbols('r', positive=True)
    a, b, Q = (s.Function(n)(r) for n in ['a', 'b', 'Q'])
    hardy = s.diff(r*a**2, r).subs(s.diff(a, r), -b*Q/r**2)
    zero(hardy-(a**2-2*a*b*Q/r))
    # The time-domain radial integration retains both physical endpoints.
    KR, KL, psiR, F, body = s.symbols('KR KL psiR F body')
    original = -2*(KL*F-KR*psiR-body)
    zero(original-2*(KR*psiR+body-KL*F))
    eta, N = s.symbols('eta N', positive=True)
    beta_tail, nu = s.Rational(1, 2)-eta, 1-eta
    zero(beta_tail+s.Rational(1, 2)-N-(1-eta-N))
    zero(nu+s.Rational(1, 2)-N-(s.Rational(3, 2)-eta-N))
    zero(nu+1-N-(2-eta-N))
    # Weighted radial norms of an exponentially damped return mode.
    B, c = s.symbols('B c', positive=True)
    zero(s.integrate(r**2*s.exp(-2*c*B*r), (r, 0, s.oo))-1/(4*c**3*B**3))
    zero(s.integrate(s.exp(-c*B*r), (r, 0, s.oo))-1/(c*B))


def euler_controls():
    values = []
    for q in map(mp.mpf, ['.6', '1']):
        beta = mp.sqrt(q*q-mp.mpf('.25'))
        for sign in (-1, 1):
            ss = mp.mpf('.5')+sign*1j*beta
            aa, bb = ss+1j*q, 2*ss
            factor = mp.gamma(bb)/(mp.gamma(aa)*mp.gamma(bb-aa))
            for z in [mp.mpc('.2', '.3'), mp.mpc('2', '.5'), mp.mpc('.1', '10')]:
                integrand = lambda y: mp.exp(-z*y)*y**(bb-aa-1)*(1-y)**(aa-1)
                integral = mp.quad(integrand, [0, mp.mpf('.5'), 1])
                exact = mp.exp(-z)*mp.hyp1f1(aa, bb, z)
                relative = abs((factor*integral-exact)/exact)
                wrong = abs((factor*integral/mp.gamma(bb)-exact)/exact)
                assert relative < mp.mpf('1e-22') and wrong > mp.mpf('1e-3')
                values.append({'q': str(q), 'sign': sign, 'z_real': str(z.real), 'z_imag': str(z.imag), 'relative_normalized_error': mp.nstr(relative, 9), 'missing_Gamma_b_relative_error': mp.nstr(wrong, 12)})
    return values


def kernel_controls():
    values = []
    R = mp.mpf(1)
    for q in map(mp.mpf, ['.6', '1']):
        beta = mp.sqrt(q*q-mp.mpf('.25'))
        ss_values = [mp.mpf('.5')+1j*beta, mp.mpf('.5')-1j*beta]
        def basis(ss, z):
            aa, bb = ss+1j*q, 2*ss
            mm = mp.hyp1f1(aa, bb, z)
            val = mp.exp(-z/2)*z**ss*mm
            dz = mp.exp(-z/2)*z**ss*((ss/z-mp.mpf('.5'))*mm+(aa/bb)*mp.hyp1f1(aa+1, bb+1, z))
            return val, dz
        for lam in map(mp.mpf, ['.001', '.01']):
            for angle in [mp.mpf(0), mp.pi/6, mp.pi/2, 5*mp.pi/6, mp.pi]:
                omega = lam*mp.exp(1j*angle)
                zR = -2j*omega*R
                norm = mp.exp(-1j*omega*R)*R**(1j*q)*(-2j*omega)**(1j*q)
                wf = lambda z: mp.whitw(-1j*q, 1j*beta, z)
                dplus = norm*((-2j*omega)*mp.diff(wf, zR)+1j*(omega-q/R)*wf(zR))
                atR = [basis(ss, zR) for ss in ss_values]
                matrix = mp.matrix([[atR[0][0], atR[1][0]], [(-2j*omega)*atR[0][1], (-2j*omega)*atR[1][1]]])
                coeff = mp.lu_solve(matrix, mp.matrix([1, -1j*(omega-q/R)]))
                for r in map(mp.mpf, [1, 10, 100, 1000, 10000, 100000]):
                    z = -2j*omega*r
                    basis_r = [basis(ss, z) for ss in ss_values]
                    H = sum(coeff[n]*basis_r[n][0] for n in range(2))
                    Hr = sum(coeff[n]*(-2j*omega)*basis_r[n][1] for n in range(2))
                    theta = omega*(r-R)-q*mp.log(r/R)
                    P = mp.exp(1j*theta)*H/dplus
                    Pr = mp.exp(1j*theta)*(Hr+1j*(omega-q/r)*H)/dplus
                    normalized_P = abs(P)*lam/min(mp.sqrt(lam*r), 1)
                    envelope_Pr = abs(Pr)/(r**(-2)+mp.exp(-mp.mpf('.25')*max(omega.imag, 0)*r))
                    assert mp.isfinite(normalized_P) and normalized_P < mp.mpf('1e8')
                    assert mp.isfinite(envelope_Pr) and envelope_Pr < mp.mpf('1e12')
                    if r == R: assert abs(Pr) < mp.mpf('1e-35')
                    values.append({'q': str(q), 'abs_omega': str(lam), 'arg_omega_over_pi': mp.nstr(angle/mp.pi, 7), 'r': str(r), 'U4_normalized': mp.nstr(normalized_P, 12), 'U5_envelope_ratio': mp.nstr(envelope_Pr, 12)})
    return values


def main():
    mp.mp.dps = 65
    check_parameters_gauge_and_rates()
    receipt = json.loads((HERE/'DLMF_KUMMER_EULER_RECEIPT_2026-10-24_R24.json').read_text())
    assert len(receipt['entries']) == 4 and not receipt['raw_page_bytes_saved_or_hashed']
    euler, kernels = euler_controls(), kernel_controls()
    names = ['verify_uniform_upper_kernel.py', 'UNIFORM_UPPER_KERNEL_AND_FUTURE_LOCALIZATION.md',
             'DLMF_KUMMER_EULER_RECEIPT_2026-10-24_R24.json', 'PHYSICAL_TRACE_GREEN_AND_DELAY.md',
             'PHYSICAL_TRACE_LOW_FREQUENCY.md', 'ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md',
             'RETURNED_REMAINDER_CONE_ESTIMATE.md', 'ACTUAL_BONDI_COMPLETENESS_BRIDGE.md',
             'FAR_ZONE_RP_AND_COULOMB_BALANCE.md', '../../definitions/MODEL.md', 'ACCEPTANCE.md']
    result = {
        'claim_ids': ['UPPER16.1', 'UPPER16.2', 'UPPER16.3', 'UPPER16.4', 'UPPER16.5', 'UPPER16.6', 'UPPER16.7', 'UPPER16.8'],
        'logic': 'PROVED for uniform local upper-plane/negative-time kernels and actual future-body localization in expanding past windows using mass; real W/full-spatial/high-frequency/Goal A OPEN',
        'evidence': ['ANALYTIC', 'PRIMARY_IDENTITIES_CHECKED', 'EXACT_ALGEBRA', 'FINITE_COMPLEX_AND_NORMALIZATION_CONTROLS'],
        'audit': 'INTERNAL_AUDIT',
        'checks': ['Kummer/Whittaker parameters and regularized-to-ordinary Gamma factor',
                   'constant leading radial power and Maxwell Hardy boundary sign',
                   'time-domain two-endpoint cutoff identity',
                   'past-window exponents and weighted exponential norms'],
        'euler_normalization_controls': euler,
        'complex_spatial_kernel_controls': kernels,
        'finite_controls_are_interval_certificates': False,
        'analytic_uniform_kernel_estimate_machine_certified': False,
        'negative_time_kernel_bound_uniform_in_radius_proved': True,
        'actual_late_body_cutoff_removed_in_expanding_past_windows': True,
        'actual_potential_L2_from_mass_proved': True,
        'future_nonlinear_body_localization_from_mass_proved': True,
        'actual_future_W_filtered_functional_localized_by_joint_identity': True,
        'actual_global_charge_bound_assumed_for_mass_inputs': False,
        'actual_W_pointwise_tail_verified': False,
        'full_time_axis_cutoff_rad_norm_removed': False,
        'leading_returned_derivative_tail_verified': False,
        'actual_uniform_A_eta_verified': False,
        'worldtube_H_tail_verified': False,
        'full_spatial_A_or_high_frequency_verified': False,
        'horizon_strong_limit_verified': False,
        'goal_A_proved': False,
        'source_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names},
    }
    (HERE/'UNIFORM_UPPER_KERNEL_CHECKS_2026-10-24.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: normalization/parameters/Hardy/endpoints/rates; 12 Euler and 120 finite complex spatial controls')
    print('LIMIT: analytic uniform kernels and actual strong tails are not machine-certified; W/full-space/high-frequency/Goal A open')


if __name__ == '__main__':
    main()
