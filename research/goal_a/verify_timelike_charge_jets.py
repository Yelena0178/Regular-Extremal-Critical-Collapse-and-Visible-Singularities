"""JET18 identities and envelope controls; no actual global PDE certification."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent


def zero(expr):
    assert s.simplify(s.expand(expr)) == 0, expr


def exact_identities():
    e, c, r, b, f, Q, ar, cr = s.symbols('e c r b f Q ar cr', real=True, nonzero=True)
    xr, xi, zr, zi, wr, wi = s.symbols('xr xi zr zi wr wi', real=True)
    psi, Z, W = xr+s.I*xi, zr+s.I*zi, wr+s.I*wi
    Du = W+c*Z/2
    qr = e*s.im(psi*s.conjugate(Z))
    nq = -e*s.im(psi*s.conjugate(W))
    qu = nq+c*qr/2
    zero(qu-(c*qr-e*s.im(psi*s.conjugate(Du))))
    # Omitting the second half of c Q_r really fails, e.g. Psi=1,Z=i.
    wrong = s.expand(qu-(c*qr/2-e*s.im(psi*s.conjugate(Du))))
    assert wrong.subs({xr: 1, xi: 0, zr: 0, zi: 1}) != 0
    p = (Z-psi/r)/r
    v = (W+c*psi/(2*r))/r
    nm = -r*r*s.Abs(v)**2/b-c*Q*Q/(4*r*r)
    mr = Q*Q/(2*r*r)+r*r*f*s.Abs(p)**2/2
    fixed = -r*r*s.Abs(v)**2/b+c*c*r*r*s.Abs(p)**2/(4*b)
    zero((nm+c*mr/2-fixed).subs(f, c/b))
    # Original scalar equation: verify n p from the reduced W_r identity.
    pr, pi = s.symbols('pr pi', real=True)
    pp = pr+s.I*pi
    ph = psi/r
    vv = (W+c*psi/(2*r))/r
    Br = s.I*e*ar/2-cr/(2*r)
    derivative_v = Br*psi/r-W/r**2+cr*psi/(2*r**2)+c*Z/(2*r**2)-c*psi/r**3
    np = derivative_v+cr*pp/2-s.I*e*ar*ph
    rhs = -vv/r+(c/(2*r)+cr/2)*pp-s.I*e*ar*ph/2
    zero((np-rhs).subs(Z, r*pp+psi/r))
    # Differentiate log b constraint along n; integrate with AF end = 0.
    qrad = e*r*r*s.im(ph*s.conjugate(pp))
    n_beta = -c*s.Abs(pp)**2/2+2*r*s.re(s.conjugate(pp)*rhs)
    dr_n_logb = n_beta-cr*r*s.Abs(pp)**2/2
    wanted = (c+r*cr)*s.Abs(pp)**2/2-2*s.re(s.conjugate(pp)*vv)+ar*qrad/r
    zero(dr_n_logb-wanted)
    # Neutral B, charged W: the commutator sign matters.
    u, rr = s.symbols('u rr', real=True)
    aa, ww = s.Function('aa')(u, rr), s.Function('ww')(u, rr)
    zero(s.diff(s.diff(ww, u)+s.I*e*aa*ww, rr)
         -(s.diff(s.diff(ww, rr), u)+s.I*e*aa*s.diff(ww, rr))
         -s.I*e*s.diff(aa, rr)*ww)
    gg, qus, mus = s.symbols('gamma Q_u m_u', real=True)
    # Product rule for a_r=-b Q/r^2, c_r=b(2m/r^2-Q^2/r^3).
    mm = s.symbols('m', real=True)
    zero(-b*(gg*Q+qus)/r**2-(-b*gg*Q/r**2-b*qus/r**2))
    crr = b*(2*mm/r**2-Q**2/r**3)
    zero(gg*crr+b*(2*mus/r**2-2*Q*qus/r**3)
         -(s.diff(crr, b)*b*gg+s.diff(crr, mm)*mus+s.diff(crr, Q)*qus))
    # Gauge rephasing has no missing -c Z/2 term.
    theta = s.Function('theta')(u)
    ps = s.Function('psi')(u)
    zero(s.diff(s.exp(s.I*theta)*ps, u)
         -s.exp(s.I*theta)*(s.diff(ps, u)+s.I*s.diff(theta, u)*ps))


def exact_envelopes():
    eta = s.symbols('eta', positive=True)
    nu, g, h = 1-eta, 1-2*eta, s.Rational(1, 2)-2*eta
    zero(2*nu-(1+g))
    assert s.simplify(g-h) == s.Rational(1, 2)
    U = s.symbols('U', positive=True)
    zero(s.diff(-U**(-g)/g, U)-U**(-2*nu))
    # Chirped Bondi-ODE control: radiation A/D bounds do not imply the new rate.
    Omega = s.symbols('Omega', positive=True)
    alpha = s.Rational(1, 2)-eta
    F = U**(-alpha)*s.exp(2*s.I*Omega*s.sqrt(U))
    zero(s.im(F*s.conjugate(s.diff(F, U)))+Omega*U**(-1-h))
    zero(s.Abs(s.diff(F, U))**2*U**(2*nu)-(Omega**2+alpha**2/U))
    # Powers in the optical coefficient estimates, including EM term.
    r = s.symbols('r', positive=True)
    for power in [s.Rational(5, 2), 3, s.Rational(7, 2), 4]:
        antiderivative = r**(1-power)/(power-1)
        zero(s.diff(antiderivative, r)+r**(-power))
    y, gp = s.symbols('y gp', positive=True)
    logder = (s.Rational(3, 2)-gp)/y-s.Rational(3, 2)/(1+y)
    zero(logder.subs(y, (s.Rational(3, 2)-gp)/gp))
    # First source term is decreasing in U for g>1/2, not r^{-g}.
    first_logder = (s.Rational(1, 2)-gp)/U-1/(2*(r+U))
    zero(first_logder-((s.Rational(1, 2)-gp)*r-gp*U)/(U*(r+U)))
    # Exact radial integral for its correct (r+1)^(-1/2) envelope.
    primitive = s.log((s.sqrt(r+1)+1)/(s.sqrt(r+1)-1))
    zero(s.diff(primitive, r)+1/(r*s.sqrt(r+1)))


def finite_controls():
    charge, source, saturation, gamma = [], [], [], []
    for eta in map(mp.mpf, ['.025', '.1', '.24']):
        g = 1-2*eta
        cg = (1-2*g/3)**(mp.mpf('1.5')-g)*(2*g/3)**g
        for R in map(mp.mpf, [1, 4, 64]):
            for U in map(mp.mpf, [1, 16, 1024]):
                V = 4*U
                val = mp.quad(lambda x: x**(-1-g), [U, V])
                rhs = (U**(-g)-V**(-g))/g
                assert abs(val-rhs) < mp.mpf('1e-38')
                charge.append({'eta': str(eta), 'R': str(R), 'U': str(U),
                               'time_integral_error': mp.nstr(abs(val-rhs), 7)})
                first = U**(-g)*mp.sqrt(U/(R+U))
                second = U**(-g)*(U/(R+U))**mp.mpf('1.5')
                assert first <= (R+1)**(-mp.mpf('.5'))*(1+mp.mpf('1e-38'))
                assert second <= cg*R**(-g)*(1+mp.mpf('1e-38'))
                source.append({'eta': str(eta), 'r': str(R), 'U': str(U),
                               'first_ratio': mp.nstr(first*mp.sqrt(R+1), 10),
                               'second_ratio': mp.nstr(second/(cg*R**(-g)), 10)})
            exact = mp.log((mp.sqrt(R+1)+1)/(mp.sqrt(R+1)-1))
            assert exact <= 2/mp.sqrt(R)
            # Numerical quadrature checks the displayed gamma majorant constant.
            A, D, Lam, Cp, CQ, K, Lc = map(mp.mpf, ['.2', '.3', '.7', '2', '.6', '1', '1.8'])
            Bv = 2*Lam+mp.mpf('.5')
            Bg = 4*Cp*A*D/3
            Cg = Cp**2/2+Cp*Bv+Lc*Cp**2/4+K*CQ/2
            val = Cp**2*A**2/(2*R**2)+mp.quad(
                lambda x: 2*Cp*A*D*x**(-mp.mpf('2.5'))
                +(2*Cp*Bv+Lc*Cp**2/2+K*CQ)*A**2*x**(-3), [R, mp.inf])
            bound = Bg*R**(-mp.mpf('1.5'))+Cg*A**2/R**2
            assert abs(val-bound) < mp.mpf('1e-38')
            gamma.append({'eta': str(eta), 'R': str(R), 'integral_error': mp.nstr(abs(val-bound), 8)})
        # A countercontrol to uniformly replacing the first radial half-power by g.
        ratios = []
        for R in map(mp.mpf, [10**2, 10**6, 10**12]):
            ratio = (R+1)**(-mp.mpf('.5'))/(R**(-g))
            ratios.append(mp.nstr(ratio, 12))
        assert mp.mpf(ratios[-1]) > mp.mpf(ratios[0])
        saturation.append({'eta': str(eta), 'ratio_against_false_r_minus_g': ratios})
    return charge, source, saturation, gamma


def main():
    mp.mp.dps = 45
    exact_identities()
    exact_envelopes()
    charge, source, saturation, gamma = finite_controls()
    names = ['verify_timelike_charge_jets.py', 'TIMELIKE_CHARGE_AND_COEFFICIENT_JETS.md',
             'MODULATED_BONDI_RADIAL_IMPROVEMENT.md', 'COULOMB_RENORMALIZATION_AND_MELLIN_GATE.md',
             'ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md', 'FULL_SPACE_PHYSICAL_TRACE_AUDIT.md',
             '../../definitions/MODEL.md', 'ACCEPTANCE.md']
    report = {
        'round': 'R26', 'logic': 'PROVED only for the stated identities and conditional estimates',
        'evidence': ['ANALYTIC', 'EXACT_ALGEBRA', 'FINITE_ENVELOPE_QUADRATURE'],
        'audit': 'INTERNAL_AUDIT; no independent or interval PDE certification',
        'source_sha256': {n: hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names},
        'exact_identities': 'PASS: Maxwell orientation, fixed-r mass cancellation, optical transport, commutator, coefficient product rules and gauge identity',
        'exact_envelopes': 'PASS: temporal integral, radial powers, maximum and saturated source envelope',
        'finite_charge_integrals': charge,
        'finite_source_envelopes': source,
        'finite_radial_saturation_countercontrols': saturation,
        'finite_optical_integrals': gamma,
        'actual_new_global_PDE_simulation': False,
        'A_D_K_uniform_input_verified': False,
        'improved_charge_freezing_under_A_D_K': True,
        'coefficient_first_time_variation_under_A_D_K': True,
        'actual_trace_channel_conditions_verified': False,
        'F_double_prime_estimate_verified': False,
        'finite_radius_full_body_source_verified': False,
        'high_frequency_and_horizon_limit_verified': False,
        'goal_A_proved': False,
    }
    target = HERE/'TIMELIKE_CHARGE_JETS_CHECKS_2026-10-24.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'PASS JET18: exact identities; {len(charge)} charge, {len(source)} source, '
          f'{len(saturation)} saturation, {len(gamma)} optical controls; actual uniform tail OPEN')


if __name__ == '__main__':
    main()
