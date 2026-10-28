"""ROBIN13 exact structures and finite complex controls, not a PDE certifier."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent


def zero(expr):
    assert s.simplify(s.expand(expr)) == 0, expr


def check_wave_trace_and_robin():
    r, u, omega, q = s.symbols('r u omega q', real=True, nonzero=True)
    R, theta = s.Function('R')(r), s.Function('theta')(r)
    phase = s.exp(-s.I*omega*u-s.I*theta)
    field = phase*R
    W = s.diff(field, u)+s.I*q/r*field-s.diff(field, r)/2
    zero((W/phase).subs(s.diff(theta, r), omega-q/r)+(s.diff(R, r)+s.I*(omega-q/r)*R)/2)
    z, beta, A, B = s.symbols('z beta A B', nonzero=True)
    plus, minus = s.Rational(1, 2)+s.I*beta, s.Rational(1, 2)-s.I*beta
    cp, cm = plus-s.I*q, minus-s.I*q
    expansion = A*z**plus+B*z**minus
    robin = z*s.diff(expansion, z)-(z/2+s.I*q)*expansion
    zero(robin-(A*cp*z**plus+B*cm*z**minus-z*expansion/2))
    # i*omega*R_*=-z/2 is the sign that distinguishes the physical W condition.
    radius = s.symbols('radius', positive=True)
    zero((s.I*(omega*radius-q)).subs(omega, s.I*z/(2*radius))-(-z/2-s.I*q))
    qb, bb = s.symbols('qb bb', positive=True, real=True)
    zero((s.Rational(1, 4)+(qb-bb)**2-2*qb*(qb-bb)).subs(bb**2, qb**2-s.Rational(1, 4)))
    zero((s.Rational(1, 4)+(qb+bb)**2-2*qb*(qb+bb)).subs(bb**2, qb**2-s.Rational(1, 4)))


def check_actual_matching_and_rates():
    zeta, zp, psi, du, Z, c, e, aa, a0 = s.symbols('zeta zp psi du Z c e aa a0')
    physical_W = du+s.I*e*aa*psi-c*Z/2
    reference_W_phi = zeta*du+zp*psi+s.I*e*a0*zeta*psi-zeta*Z/2
    matched = zeta*physical_W+zp*psi-s.I*e*(aa-a0)*zeta*psi+(c-1)*zeta*Z/2
    zero(reference_W_phi-matched)
    R, M, T, eta = s.symbols('R M T eta', positive=True)
    # The late cutoff's actual mass input has the exact negative power -eta.
    estimate = (2*T)**(1-eta)/T*2*s.sqrt(M*R)
    zero(estimate-2**(2-eta)*s.sqrt(M*R)*T**(-eta))
    # Pure boundary Green coefficient from W=-d*F/2.
    d, w = s.symbols('d w', nonzero=True)
    F = -2*w/d
    zero(-d*F/2-w)
    # Reference infinity normalization after gauge/static-time phases.
    omega, q, r = s.symbols('omega q r', positive=True)
    normalization = s.exp(-s.I*omega*R)*R**(s.I*q)*(-2*s.I*omega)**(s.I*q)
    asymptotic_mode = s.exp(s.I*omega*r)*(-2*s.I*omega)**(-s.I*q)*r**(-s.I*q)
    desired = s.exp(s.I*omega*(r-R))*R**(s.I*q)*r**(-s.I*q)
    zero(normalization*asymptotic_mode-desired)


def finite_controls():
    mp.mp.dps = 55
    ratios, sectors = [], []
    for q in map(mp.mpf, ['.51', '.6', '1', '3']):
        beta = mp.sqrt(q*q-mp.mpf('.25'))
        A = mp.gamma(-2j*beta)/mp.gamma(mp.mpf('.5')-1j*beta+1j*q)
        B = mp.gamma(2j*beta)/mp.gamma(mp.mpf('.5')+1j*beta+1j*q)
        cp, cm = mp.mpf('.5')+1j*(beta-q), mp.mpf('.5')-1j*(beta+q)
        rho_d = mp.sqrt(mp.cosh(mp.pi*(q+beta))/mp.cosh(mp.pi*(q-beta)))
        rho_w = rho_d*mp.sqrt((q+beta)/(q-beta))
        assert abs(abs(B*cm/(A*cp))/rho_w-1) < mp.mpf('1e-45')
        integral = mp.quad(lambda x: (mp.pi*mp.tanh(mp.pi*x)+1/x)/2, [q-beta, q+beta])
        assert abs(integral-mp.log(rho_w)) < mp.mpf('1e-42')
        assert rho_d*mp.exp(-mp.pi*beta) < 1 < rho_w*mp.exp(-mp.pi*beta)
        ratios.append({'q': str(q), 'Dirichlet_ratio_at_lower_sector_edge': mp.nstr(rho_d*mp.exp(-mp.pi*beta), 17), 'physical_W_ratio_at_lower_sector_edge': mp.nstr(rho_w*mp.exp(-mp.pi*beta), 17)})
        for radius in [mp.mpf('.001'), mp.mpf('.000001')]:
            for angle in [-mp.pi/2, -mp.pi/4, mp.mpf(0), mp.pi/4, mp.pi/2]:
                z = radius*mp.exp(1j*angle)
                fn = lambda v: mp.whitw(-1j*q, 1j*beta, v)
                exact = z*mp.diff(fn, z)-(z/2+1j*q)*fn(z)
                leading = z**mp.mpf('.5')*(A*cp*z**(1j*beta)+B*cm*z**(-1j*beta))
                relative = abs((exact-leading)/leading)
                assert abs(exact) > 0 and relative < mp.mpf('.2')
                sectors.append({'q': str(q), 'abs_z': str(radius), 'arg_z_over_pi': mp.nstr(angle/mp.pi, 8), 'abs_robin_over_sqrt_abs_z': mp.nstr(abs(exact)/mp.sqrt(radius), 16), 'relative_leading_error': mp.nstr(relative, 12)})
    cutoff = []
    for T in map(mp.mpf, [16, 64, 256]):
        # Envelope with eta=1/8, R_*=8, M=1; unspecified theorem constants omitted.
        cutoff.append({'T': str(T), 'boundary_cutoff_tail_envelope': mp.nstr(8*T**(-mp.mpf(1)/8), 16)})
    assert mp.mpf(cutoff[-1]['boundary_cutoff_tail_envelope']) < mp.mpf(cutoff[0]['boundary_cutoff_tail_envelope'])
    return ratios, sectors, cutoff


def main():
    check_wave_trace_and_robin()
    check_actual_matching_and_rates()
    ratios, sectors, cutoff = finite_controls()
    names = ['verify_physical_trace_low_frequency.py', 'PHYSICAL_TRACE_LOW_FREQUENCY.md',
             'WORLD_TUBE_RADIATION_TRANSFER.md', 'DLMF_WHITTAKER_RECEIPT_2026-10-23_R17.json',
             'LOW_FREQUENCY_SYMBOL_AND_TIME_TRANSFER.md', 'ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md',
             'RADIAL_DIVERGENCE_AND_SPECTRAL_CUTOFF.md', 'LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md',
             '../../definitions/MODEL.md', 'ACCEPTANCE.md']
    result = {
        'claim_ids': ['ROBIN13.1', 'ROBIN13.2', 'ROBIN13.3', 'ROBIN13.4', 'ROBIN13.5'],
        'logic': 'PROVED for auxiliary Coulomb W-boundary near-zero denominator/time kernel and exact actual matching/boundary cutoff; body Green/actual W/full Goal A OPEN',
        'evidence': ['ANALYTIC', 'SPECIAL_FUNCTION_PRIMARY_IDENTITIES_REUSED', 'EXACT_ALGEBRA', 'FINITE_COMPLEX_SECTOR_CONTROLS'],
        'audit': 'INTERNAL_AUDIT',
        'checks': ['static/radial-gauge physical W and Robin sign',
                   'indicial Robin coefficients and Gamma ratio',
                   'actual nonhomogeneous W matching and boundary cutoff scaling',
                   'reference outgoing normalization'],
        'coefficient_ratio_controls': ratios,
        'complex_sector_controls': sectors,
        'boundary_cutoff_controls': cutoff,
        'finite_sector_controls_are_interval_certificates': False,
        'analytic_uniform_no_zero_sector_machine_certified': False,
        'auxiliary_operator_is_D001_solution': False,
        'actual_W_set_to_zero': False,
        'near_zero_physical_W_reference_denominator_proved_nonzero': True,
        'reference_boundary_kernel_strictly_causal': False,
        'pure_boundary_late_cutoff_tail_removed_using_actual_mass': True,
        'Robin_body_Green_kernel_estimate_verified': False,
        'full_frequency_mode_stability_verified': False,
        'full_weighted_cutoff_removed': False,
        'actual_uniform_A_eta_verified': False,
        'worldtube_H_tail_verified': False,
        'horizon_strong_limit_verified': False,
        'goal_A_proved': False,
        'source_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names},
    }
    (HERE/'PHYSICAL_TRACE_CHECKS_2026-10-24.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: physical/Robin/matching/normalization identities; 4 ratio, 40 complex-sector and 3 cutoff controls')
    print('LIMIT: analytic no-zero sector is not machine-certified; actual W/body/full-frequency/strong Goal A remain open')


if __name__ == '__main__':
    main()
