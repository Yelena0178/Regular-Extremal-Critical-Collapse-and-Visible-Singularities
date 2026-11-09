"""Scoped identities and finite controls for SYMBOL10; not a PDE proof checker."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s


HERE = Path(__file__).resolve().parent


def zero(expr):
    assert s.simplify(s.expand(expr)) == 0, expr


def check_signed_amplitudes():
    # Independent differentiation of the scaled wave and phase variables.
    f, fr, rho, kap, kr = s.symbols('f fr rho kap kr', positive=True)
    v, p, phase = s.symbols('v p phase', real=True)
    variables = (f, rho, kap, v, p, phase)
    for eps in (-1, 1):
        potential = f * fr / rho
        rates = (fr, 1, kr, p/f, -(kap**2-potential)*v/f, eps*kap/f)
        plus = s.exp(-s.I*phase)*(s.sqrt(kap)*v-s.I*eps*p/s.sqrt(kap))/2
        minus = s.exp(s.I*phase)*(s.sqrt(kap)*v+s.I*eps*p/s.sqrt(kap))/2
        def dr(expr):
            return sum(s.diff(expr, z)*rate for z, rate in zip(variables, rates))
        n11 = -s.I*eps*fr/(2*rho*kap)
        n12 = (kr/(2*kap)-s.I*eps*fr/(2*rho*kap))*s.exp(-2*s.I*phase)
        n21 = (kr/(2*kap)+s.I*eps*fr/(2*rho*kap))*s.exp(2*s.I*phase)
        zero(dr(plus)-n11*plus-n12*minus)
        zero(dr(minus)-n21*plus+n11*minus)


def check_parameter_mellin_and_moving_end():
    lam, r, q, f, a = s.symbols('lam r q f a', positive=True)
    for eps in (-1, 1):
        potential = (eps*lam*r-q)**2/f**2
        current = potential
        for order in range(1, 5):
            current = lam*s.diff(current, lam)
            zero(current-(2**order*(lam*r)**2-2*eps*q*lam*r)/f**2)
            integral = s.integrate(4*(2**order*lam**2*r**2+2*q*lam*r)/r, (r, 0, a/lam))
            zero(integral-(2**(order+1)*a**2+8*q*a))
    # A fully explicit function validates conversion at a moving s endpoint.
    x, beta = s.symbols('x beta', real=True)
    w = lam**2*s.exp(s.I*beta*x)+lam*s.cos(x)
    endpoint = -s.log(lam)
    data = w.subs(x, endpoint)
    zero((lam*s.diff(w, lam)).subs(x, endpoint)-lam*s.diff(data, lam)-s.diff(w, x).subs(x, endpoint))
    data_s = s.diff(w, x).subs(x, endpoint)
    zero((lam*s.diff(s.diff(w, x), lam)).subs(x, endpoint)-lam*s.diff(data_s, lam)-s.diff(w, x, 2).subs(x, endpoint))
    # Differentiate a formal homogeneous equation to check the binomial source.
    V = s.Function('V')(lam, x)
    W = s.Function('W')(lam, x)
    dop = lambda expr: lam*s.diff(expr, lam)
    def power_d(expr, n):
        for _ in range(n): expr = dop(expr)
        return expr
    for order in range(1, 5):
        zero(power_d(V*W, order)-sum(s.binomial(order, ell)*power_d(V, ell)*power_d(W, order-ell) for ell in range(order+1)))


def check_phase_and_weighted_boundary():
    # Long-range phase must be retained; differentiating a moving endpoint is not free.
    lam, b, q, X, fb = s.symbols('lam b q X fb', nonzero=True, real=True)
    # D[epsilon*lam*X(b/lam)-q*H(b/lam)], with X_r=1/f, H_r=1/(r*f).
    for eps in (-1, 1):
        direct = eps*lam*X + (eps*lam/fb-q/((b/lam)*fb))*(-b/lam)
        zero(direct-(eps*lam*X-(eps*b-q)/fb))
    # Frequency differentiation is ordinary lambda differentiation converted to D.
    lam = s.symbols('lam', positive=True)
    w = s.Function('w')(lam)
    zero(s.diff(w, lam, 2)-((lam*s.diff(lam*s.diff(w, lam), lam))-lam*s.diff(w, lam))/lam**2)
    # Physical p=du(h)+g, cancellation of the time derivative by kernel differentiation.
    zeta, zetap, psi, du_psi, Z, c, ref, rstar, e, aa = s.symbols('zeta zetap psi du_psi Z c ref rstar e aa')
    h = zeta*psi
    du_h = zetap*psi+zeta*du_psi
    dn = du_psi+s.I*e*aa*psi-c*Z/2
    g = s.I*e*aa*h-2*zeta*dn-2*zetap*psi-(c-ref)*h/rstar
    expected = c*zeta*Z-(du_h+s.I*e*aa*h)-(c-ref)*h/rstar
    zero(du_h+g-expected)
    # Exact conversion of the A envelope to the fixed-worldtube h norm.
    U, rr = s.symbols('U rr', positive=True)
    zero(U/(1+U/rr)-rr*U/(U+rr))


def finite_convolution_controls():
    mp.mp.dps = 40
    eta = mp.mpf(1)/8
    values = []
    for t in [mp.mpf(2), mp.mpf(16), mp.mpf(128), mp.mpf(1024)]:
        row = {'t': str(t)}
        for alpha, target, label in [(mp.mpf('.5'), mp.mpf('.5')-eta, 'amplitude'), (mp.mpf('1.5'), 1-eta, 'first_derivative'), (mp.mpf('2.5'), 1-eta, 'second_derivative')]:
            integrand = lambda v: (1+abs(t-v))**(-alpha)*(1+v)**(-1+eta)
            integral = mp.quad(integrand, [0, t/2, t, 3*t/2, mp.inf])
            norm = (1+t)**target*integral
            assert mp.isfinite(norm) and norm < 50
            row[label+'_weighted_majorant'] = mp.nstr(norm, 16)
        values.append(row)
    endpoint = []
    for t in [mp.mpf(16), mp.mpf(256), mp.mpf(4096)]:
        kernel = lambda x: mp.re((1+1j*x)**(-mp.mpf('.5')))/mp.sqrt(mp.pi)
        # Lower bound integrates only the past part of a g supported up to 2T.
        val = mp.quad(lambda v: kernel(t-v)/(1+v), [0, t/2, t])
        endpoint.append({'T': str(t), 'sqrtT_convolution': mp.nstr(mp.sqrt(t)*val, 16)})
    assert mp.mpf(endpoint[-1]['sqrtT_convolution']) > mp.mpf(endpoint[0]['sqrtT_convolution'])
    return values, endpoint


def source_hashes():
    names = ['verify_low_frequency_symbol.py', 'LOW_FREQUENCY_SYMBOL_AND_TIME_TRANSFER.md',
             'WORLD_TUBE_RADIATION_TRANSFER.md', 'LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md',
             'MELLIN_INNER_TRANSFER_AND_CHARGE_BOOTSTRAP.md', 'TAIL_CURRENT_AND_CARRIER_AUDIT.md',
             'FAR_ZONE_RP_AND_COULOMB_BALANCE.md', '../../definitions/MODEL.md', 'ACCEPTANCE.md']
    return {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names}


def main():
    check_signed_amplitudes()
    check_parameter_mellin_and_moving_end()
    check_phase_and_weighted_boundary()
    convolution, endpoint = finite_convolution_controls()
    result = {
        'claim_ids': ['SYMBOL10.1', 'SYMBOL10.2', 'SYMBOL10.3', 'SYMBOL10.4'],
        'logic': 'PROVED for scoped reference symbol/time maps and actual finite-window boundary contribution; actual source/A/H/Goal A OPEN',
        'evidence': ['ANALYTIC', 'EXACT_ALGEBRA', 'FINITE_CONVOLUTION_QUADRATURE_CONTROLS'],
        'audit': 'INTERNAL_AUDIT',
        'checks': ['signed adiabatic matrix for both real-frequency signs',
                   'four Mellin conormal coefficient derivatives and integral bounds',
                   'moving endpoint conversion and four Leibniz commutators',
                   'long-range phase endpoint, physical momentum and A-to-h conversion'],
        'finite_convolution_controls': convolution,
        'endpoint_negative_control': endpoint,
        'negative_controls': ['amplitude-only symbols allow arbitrary delayed packets',
                              'eta=0 general half-integral map has logarithmic loss'],
        'analytic_uniform_symbol_estimate_machine_certified': False,
        'actual_body_source_estimate_verified': False,
        'actual_uniform_A_eta_verified': False,
        'worldtube_H_tail_verified': False,
        'frequency_derivatives_are_charge_parameter_derivatives': False,
        'future_cutoff_fully_removed': False,
        'horizon_strong_limit_verified': False,
        'goal_A_proved': False,
        'source_sha256': source_hashes(),
    }
    out = HERE/'LOW_FREQUENCY_SYMBOL_CHECKS_2026-10-23.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: signed/moving-boundary/commutator identities; 12 finite weighted convolutions and 3 endpoint controls')
    print('LIMIT: no machine certification of analytic uniform symbol theorem, actual body sources, A/H tails or Goal A')


if __name__ == '__main__':
    main()
