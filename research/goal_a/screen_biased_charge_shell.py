"""Finite center evolution for the charge-location/direction family."""
import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from charge_preserving_shell import ShellParameters
from biased_charge_shell import BiasedChargeShell
from centered_cauchy_diamond import axis_state, evolve_centered
from screen_charge_preserving_shell import Diagnostics


def run(parameters, bias, time, steps, save_arrays=None):
    data = BiasedChargeShell(parameters, bias, exterior_width=max(10., 2*time+2*parameters.radius))
    observer = Diagnostics(data, time)
    result = evolve_centered(data.state_at_proper, axis_state(.5, 0j), 0j,
                             data.proper_max, time, steps, observer=observer)
    if result['completed']:
        arrays = {key: result.pop(key) for key in ('x', 'state', 'initial_state')}
        if save_arrays:
            np.savez_compressed(save_arrays, **arrays)
    result.update(initial_data=data.summary(), diagnostics=observer.report(),
                  requested_time=time, requested_steps=steps, finite_PDE_error_certified=False,
                  full_future_classified=False, positive_mass_long_residence_proved=False, goal_A_proved=False)
    return result


def source_hashes():
    names = ['biased_charge_shell.py', 'screen_biased_charge_shell.py', 'charge_preserving_shell.py',
             'screen_charge_preserving_shell.py', 'centered_cauchy_diamond.py',
             'charged_cauchy_diamond.py', 'charged_lobatto.py']
    folder = Path(__file__).resolve().parent
    return {name: sha256((folder/name).read_bytes()).hexdigest() for name in names}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--amplitude', type=float, default=.4)
    parser.add_argument('--frequency', type=float, default=.15)
    parser.add_argument('--direction', type=float, default=.8)
    parser.add_argument('--bias', type=float, required=True)
    parser.add_argument('--time', type=float, default=30.)
    parser.add_argument('--steps', type=int, default=1024)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--save-arrays', action='store_true')
    args = parser.parse_args()
    parameters = ShellParameters(amplitude=args.amplitude, frequency=args.frequency, direction=args.direction)
    try:
        result = run(parameters, args.bias, args.time, args.steps,
                     args.output.with_suffix('.npz') if args.save_arrays else None)
    except (ArithmeticError, ValueError) as error:
        result = dict(parameters=asdict(parameters), bias=args.bias, completed=False, failure=str(error),
                      finite_PDE_error_certified=False, full_future_classified=False, goal_A_proved=False)
    result['source_sha256'] = source_hashes()
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result.get(k) for k in ['completed', 'failed_time', 'worst', 'first_negative_sample',
                                              'final_row_constraints']}, indent=2))
