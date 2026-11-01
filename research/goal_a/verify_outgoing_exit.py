"""Exact algebra checks for A-EXIT01; no global evolution claims."""
import sympy as s


def main():
    a, w, e, r, p, d, h, phase, q = s.symbols(
        'a w e r p d h phase q', real=True
    )
    phi = a * p * s.exp(s.I * phase) / r
    phi_r = a * (d - p / r + s.I * w * p) * s.exp(s.I * phase) / r
    pi = -a * h * (d + s.I * w * p) * s.exp(s.I * phase) / r
    current = e * s.im(phi * s.conjugate(pi))
    jr = -s.re(pi * s.conjugate(phi_r))
    P = d * (d - p / r) + w**2 * p**2
    S = d**2 + (d - p / r)**2 + 2 * w**2 * p**2
    scalar_energy_twice = pi * s.conjugate(pi) + h**2 * phi_r * s.conjugate(phi_r)
    residuals = {
        'gauss': current - e * w * a**2 * h * p**2 / r**2,
        'momentum': r * jr - a**2 * h * P / r,
        'hamiltonian': r**2 * (scalar_energy_twice + q**2 / r**4) / 2
            - (q**2 / (2 * r**2) + a**2 * h**2 * S / 2),
        'outgoing': r * pi + h * (r * phi_r + phi),
        'quadratic_bound': 3*d**2 + 2*(r**-2 + w**2)*p**2 - S - (d+p/r)**2,
    }
    for name, residual in residuals.items():
        if s.simplify(s.expand_complex(residual)) != 0:
            raise RuntimeError(f'{name}: nonzero symbolic residual')
        print(f'{name}: EXACT_ZERO')
    # A single reversal of Pi must fail the positive-charge Gauss formula.
    wrong = -current - e * w * a**2 * h * p**2 / r**2
    if s.simplify(wrong) == 0:
        raise RuntimeError('Gauss sign negative control was not rejected')
    print('single_Pi_sign_reversal: REJECTED')
    print('Scope: constraint algebra only; full dispersion remains unproved.')


if __name__ == '__main__':
    main()
