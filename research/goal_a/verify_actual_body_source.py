"""Exact structures and finite controls for BODY11, not a uniform/PDE certifier."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent


def zero(expr):
    assert s.simplify(s.expand(expr)) == 0, expr


def asymptotic_polynomials():
    z, lam, mass, charge, q = s.symbols('z lam mass charge q', real=True)
    f = 1-2*mass*lam*z+charge**2*lam**2*z**2
    dr = lambda expr: -z**2*s.diff(expr, z)
    residuals = []
    for eps in (-1, 1):
        operator = lambda expr: s.expand(f*dr(dr(expr))+(dr(f)+2*s.I*(eps-q*z))*dr(expr)+(s.I*q*z**2-dr(f)*z)*expr)
        polynomial = s.Integer(1)
        for n in range(1, 7):
            cn = s.Symbol('cn')
            test = polynomial+cn*z**n
            coefficient = operator(test).coeff(z, n+1)
            zero(s.diff(coefficient, cn)+2*s.I*eps*n)
            value = s.expand(-coefficient.subs(cn, 0)/s.diff(coefficient, cn))
            assert s.Poly(value, lam, mass, charge, q) is not None
            polynomial = s.expand(polynomial+value*z**n)
            if n == 1: zero(value-eps*q/2)
        residual = operator(polynomial)
        for n in range(0, 8): zero(residual.coeff(z, n))
        residuals.append((eps, residual, (z, lam, mass, charge, q)))
    return residuals


def check_fixed_r_and_weights():
    rho, lam, rr = s.symbols('rho lam rr', positive=True)
    # Fixed-r D differs from fixed-rho D by rho*d_rho, including a radial derivative.
    y = s.exp(-lam)/rho+lam**2/rho**2
    L = lambda expr: lam*s.diff(expr, lam)+rho*s.diff(expr, rho)
    substituted = y.subs(rho, lam*rr)
    zero(lam*s.diff(substituted, lam)-L(y).subs(rho, lam*rr))
    Yr = lam*s.diff(y, rho)
    zero(lam*s.diff(Yr.subs(rho, lam*rr), lam)-L(Yr).subs(rho, lam*rr))
    # Derivation of the retarded outer equation from R=e^(i theta)*Y.
    r = s.symbols('r', positive=True)
    f, k = s.Function('f')(r), s.Function('k')(r)
    Y, theta = s.Function('Y')(r), s.Function('theta')(r)
    R = s.exp(s.I*theta)*Y
    expr = (f*s.diff(f*s.diff(R, r), r)+(k**2-f*s.diff(f, r)/r)*R)/(f*s.exp(s.I*theta))
    expr = expr.subs(s.diff(theta, r, 2), s.diff(k/f, r)).subs(s.diff(theta, r), k/f)
    expected = f*s.diff(Y, r, 2)+(s.diff(f, r)+2*s.I*k)*s.diff(Y, r)+(s.I*s.diff(k, r)-s.diff(f, r)/r)*Y
    zero(expr-expected)
    # The compatible model satisfies exactly the amplitude and Z envelopes.
    U, eta, amp = s.symbols('U eta amp', positive=True)
    psi = amp*U**(-s.Rational(1, 2)+eta)*s.sqrt(r/(r+U))
    Z = amp*s.Rational(1, 2)*U**(s.Rational(1, 2)+eta)*r**(-s.Rational(1, 2))*(r+U)**(-s.Rational(3, 2))
    zero(s.diff(psi, r)-Z)
    zero(U**(1-eta)*psi-amp*s.sqrt(r)*s.sqrt(U/(r+U)))
    zero(U**(1-eta)*Z-amp/(2*s.sqrt(r))*(U/(r+U))**s.Rational(3, 2))


def check_bondi_and_radial_integrals():
    U, end, h, R, r = s.symbols('U end h R r', positive=True)
    primitive = (U**(-h)-end**(-h))/h
    zero(s.diff(primitive, U)+U**(-1-h))
    zero(s.diff(-r**(-h)/h, r)-r**(-1-h))
    zero(s.diff(-1/r, r)-r**(-2))
    zero(s.diff(-2*U**s.Rational(3, 2)/s.sqrt(r+U), r)-(U/(r+U))**s.Rational(3, 2))
    # Sum exactly the four integrated source majorants in B10.
    A, Cz, G, d = s.symbols('A Cz G d', positive=True)
    term = 2*(1+Cz)*G*A/R+(1+Cz)*d*A*R**(-h)/h
    zero(term-(1+Cz)*A*(2*G/R+d*R**(-h)/h))
    # Positivity of f requires far-radius bounds, not M0 >= Q0.
    zero((1-2*s.Rational(1, 4)/4+1/4**2)-s.Rational(15, 16))
    # Exact complex Hardy balance, including the inner boundary before integration.
    real_part, imag_part = s.Function('real')(r), s.Function('imag')(r)
    point_phi_sq = real_part**2+imag_part**2
    point_grad_sq = s.diff(real_part, r)**2+s.diff(imag_part, r)**2
    point_Z_sq = s.diff(r*real_part, r)**2+s.diff(r*imag_part, r)**2
    zero(point_Z_sq-r**2*point_grad_sq-s.diff(r*point_phi_sq, r))
    T, C, M = s.symbols('T C M', positive=True)
    zero((2*C/T)**2*T*(4*M)-16*C**2*M/T)


def finite_controls(residuals):
    mp.mp.dps = 45
    controls = []
    for eps, expr, symbols in residuals:
        fn = s.lambdify(symbols, expr, 'mpmath')
        for lam in [mp.mpf('.01'), mp.mpf('.001')]:
            for rho in [mp.mpf(4), mp.mpf(8), mp.mpf(16)]:
                # M0 < |Q0| deliberately tests far-ODE rather than black-hole assumptions.
                scaled = abs(fn(1/rho, lam, mp.mpf('.25'), mp.mpf(1), mp.mpf('.6')))*rho**8
                assert mp.isfinite(scaled) and scaled < 10**6
                controls.append({'sign': eps, 'lambda': str(lam), 'rho': str(rho), 'rho8_abs_residual': mp.nstr(scaled, 16)})
    h = mp.mpf(1)/4
    R = mp.mpf(8)
    radial = []
    for L in [mp.mpf(100), mp.mpf(1000), mp.mpf(10000)]:
        divergent = mp.quad(lambda r: 1/r, [R, L])
        convergent = mp.quad(lambda r: r**(-1-h), [R, L])
        assert abs(divergent-mp.log(L/R)) < mp.mpf('1e-35')
        assert abs(convergent-(R**(-h)-L**(-h))/h) < mp.mpf('1e-35')
        radial.append({'outer_radius': str(L), 'constant_charge_norm': mp.nstr(divergent, 16), 'decaying_charge_norm': mp.nstr(convergent, 16)})
    cutoff = []
    for T in [mp.mpf(16), mp.mpf(64), mp.mpf(256)]:
        U = 1+mp.mpf('1.5')*T
        # A=1 and |z'(alpha)|=1: exact lower bound from one cutoff time.
        lower = 2*(U/T)*mp.sqrt(U/(R+U))
        assert lower > 1
        cutoff.append({'T': str(T), 'model_cutoff_norm_lower_bound': mp.nstr(lower, 16)})
    # Analytic interpolation is split at U/r=1; this grid is only a negative-error control.
    for exponent in [mp.mpf('.1'), mp.mpf('.25'), mp.mpf('.49')]:
        for ratio in [mp.mpf('1e-6'), mp.mpf('.1'), mp.mpf(1), mp.mpf(10), mp.mpf('1e6')]:
            assert mp.sqrt(ratio/(1+ratio)) <= ratio**exponent
    return controls, radial, cutoff


def main():
    residuals = asymptotic_polynomials()
    check_fixed_r_and_weights()
    check_bondi_and_radial_integrals()
    asymptotic, radial, cutoff = finite_controls(residuals)
    names = ['verify_actual_body_source.py', 'ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md',
             'LOW_FREQUENCY_SYMBOL_AND_TIME_TRANSFER.md', 'WORLD_TUBE_RADIATION_TRANSFER.md',
             'MODULATED_BONDI_RADIAL_IMPROVEMENT.md', 'TAIL_CURRENT_AND_CARRIER_AUDIT.md',
             'FAR_ZONE_RP_AND_COULOMB_BALANCE.md', 'LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md',
             '../../definitions/MODEL.md', 'ACCEPTANCE.md']
    result = {
        'claim_ids': ['BODY11.1', 'BODY11.2', 'BODY11.3', 'BODY11.4', 'BODY11.5', 'BODY11.6'],
        'logic': 'PROVED for scoped far-reference source kernels and actual finite-window terminal-freezing source estimate; cutoff/causal/full-spatial/high-frequency and Goal A OPEN',
        'evidence': ['ANALYTIC', 'EXACT_ALGEBRA', 'FINITE_ASYMPTOTIC_AND_RADIAL_CONTROLS'],
        'audit': 'INTERNAL_AUDIT',
        'checks': ['six-order outer polynomial recurrence for both frequency signs',
                   'fixed-r versus scaled conormal differentiation',
                   'retarded wave equation and compatible envelope derivative',
                   'finite-end Bondi primitive and radial/source/cutoff primitives',
                   'exact complex Hardy boundary balance and actual weak cutoff scaling'],
        'finite_asymptotic_residual_controls': asymptotic,
        'radial_source_norm_controls': radial,
        'cutoff_negative_control': cutoff,
        'negative_controls': ['constant charge mismatch is logarithmic in the chosen absolute source norm',
                              'A/Z envelopes alone do not make the full cutoff source norm tend to zero'],
        'uniform_analytic_source_kernels_machine_certified': False,
        'terminal_freezing_assumes_final_charge': False,
        'far_reference_requires_mass_charge_inequality': False,
        'actual_low_frequency_body_error_estimated_with_explicit_inputs': True,
        'actual_future_cutoff_removed': False,
        'actual_cutoff_source_unweighted_L2_vanishes': True,
        'actual_filtered_radiation_cutoff_local_limit_exists': True,
        'actual_uniform_A_eta_verified': False,
        'worldtube_H_tail_verified': False,
        'full_spatial_A_or_high_frequency_verified': False,
        'horizon_strong_limit_verified': False,
        'goal_A_proved': False,
        'source_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names},
    }
    (HERE/'ACTUAL_BODY_SOURCE_CHECKS_2026-10-23.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: six-order signed recurrence, retarded/fixed-r/envelope and integral identities; 12 finite residual and 6 norm controls')
    print('LIMIT: analytic uniform kernels, actual cutoff removal, A/H/full-space/high-frequency and Goal A are not machine-certified')


if __name__ == '__main__':
    main()
