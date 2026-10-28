"""Independent derivative, charge normalization and zero-bias regressions."""
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
import mpmath as mp
import sympy as s
from charge_preserving_shell import ShellParameters, ChargePreservingShell
from biased_charge_shell import BiasedChargeShell
from certify_biased_shell_initial import certify


def verify():
    r, R, W, beta, C, w, d = s.symbols('r R W beta C w d', real=True, nonzero=True)
    theta = d*w*C*W*(1-s.exp(-beta*(r-R)/W))/beta
    assert s.simplify(s.diff(theta, r)-d*w*C*s.exp(-beta*(r-R)/W)) == 0
    p = ShellParameters(amplitude=.4, frequency=.15, direction=.6)
    original = ChargePreservingShell(p)
    zero = BiasedChargeShell(p, 0.)
    radial_grid = np.linspace(6., 14., 513)
    zero_error = float(np.max(abs(original.sol.sol(radial_grid)-zero.sol.sol(radial_grid))))
    assert zero_error < 1e-9
    checks = []
    for bias in [-2., -1., 1., 2.]:
        data = BiasedChargeShell(p, bias)
        opposite = BiasedChargeShell(replace(p, direction=-p.direction), bias)
        geometry_error = float(np.max(abs(data.sol.sol(radial_grid)-opposite.sol.sol(radial_grid))))
        assert geometry_error < 1e-12
        charge_error = abs(data.ADM_charge-original.ADM_charge)
        assert charge_error < 1e-9
        derivative_errors, direction_errors = [], []
        for at in np.linspace(6.2, 13.8, 101):
            h = 1e-4
            phi, gradient, chi = data.free(at)
            numerical = (data.free(at-2*h)[0]-8*data.free(at-h)[0]
                         +8*data.free(at+h)[0]-data.free(at+2*h)[0])/(12*h)
            derivative_errors.append(abs(numerical-gradient))
            incoming, outgoing = phi+at*(chi+gradient), -phi+at*(chi-gradient)
            direction_errors.append(abs(abs(incoming)**2*(1+p.direction)**2
                                        -abs(outgoing)**2*(1-p.direction)**2))
        assert max(derivative_errors) < 1e-8 and max(direction_errors) < 1e-10
        with mp.workdps(60):
            weight = lambda z: (10+4*z)**2*mp.exp(-2*z*z/(1-z*z)) if abs(z)<1 else 0
            integral = mp.quad(weight, [-1, 0, 1])
            tilted = mp.quad(lambda z: weight(z)*mp.exp(-mp.mpf(str(bias))*z), [-1, 0, 1])
            normalization_error = abs(float(integral/tilted)-data.normalization)
        assert normalization_error < 1e-12
        checks.append(dict(bias=bias, normalization=data.normalization,
                           normalization_error_against_60_digits=normalization_error,
                           total_charge_error=charge_error,
                           opposite_direction_geometry_error=geometry_error,
                           maximum_phi_derivative_error=max(derivative_errors),
                           maximum_direction_decomposition_error=max(direction_errors)))
    cert = certify()
    return dict(phase_derivative_identity=True, zero_bias_regression_error=zero_error,
                checks=checks, initial_barrier=cert['pointwise_barrier'],
                normalization_error_certified=False, finite_PDE_error_certified=False, goal_A_proved=False)


def scan():
    rows = []
    for bias in [-2., -1., 0., 1., 2.]:
        for direction in [.5, .8, 1.]:
            p = ShellParameters(amplitude=.4, frequency=.15, direction=direction)
            data = BiasedChargeShell(p, bias, exterior_width=2.)
            row = data.summary()
            rows.append(row)
            print(json.dumps(dict(beta=bias, d=direction, M=row['ADM_mass'], Q=row['ADM_charge'],
                                  f_min=row['minimum_sampled_initial_f'],
                                  inner_charge_fraction=row['charge_fraction_inside_R'])))
    return dict(initial_data=rows, future_focusing_certified=False, goal_A_proved=False)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan', action='store_true')
    args = parser.parse_args()
    result = scan() if args.scan else verify()
    result['source_sha256'] = {name: sha256(Path(name).read_bytes()).hexdigest() for name in
        ['verify_biased_shell.py', 'biased_charge_shell.py', 'charge_preserving_shell.py',
         'certify_biased_shell_initial.py', 'certify_charge_shell_initial.py']}
    name = 'BIASED_SHELL_INITIAL_SCAN_2026-10-22.json' if args.scan else 'BIASED_SHELL_CHECKS_2026-10-22.json'
    Path(name).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    if not args.scan:
        print(json.dumps({k: v for k, v in result.items() if k != 'source_sha256'}, indent=2))
