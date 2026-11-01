"""Finite E0 screening, including center, fixed-radius mass and null budgets."""
import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from charge_preserving_shell import ShellParameters, ChargePreservingShell
from centered_cauchy_diamond import axis_state, evolve_centered


class Diagnostics:
    def __init__(self, data, final_time):
        p = data.parameters
        self.radii = [p.radius/2, p.radius, data.outer, 2*data.outer]
        self.samples = []
        self.interval = final_time/32
        self.next_sample = 0.
        self.rays = {str(u): dict(u=float(u)) for u in [-data.inner, 0., data.inner, p.radius]}
        self.axis_proper_time = 0.
        self.last_axis = None

    @staticmethod
    def interpolate(x, state, at):
        return np.array([np.interp(at, x, state[:, j]) for j in range(12)])

    def __call__(self, t, x, state):
        if x[0] == 0:
            lapse = 2*state[0, 1]
            if self.last_axis is not None:
                t0, a0 = self.last_axis
                self.axis_proper_time += (t-t0)*(a0+lapse)/2
            self.last_axis = (t, lapse)
        for ray in self.rays.values():
            at = t-ray['u']
            if not x[0] <= at <= x[-1] or at == 0:
                continue
            y = self.interpolate(x, state, at)
            r, k, nu, m, Q = y[0], y[1], y[4], y[7], y[10]
            phi, V = y[8]+1j*y[9], (y[2]+1j*y[3])/r
            omega2 = -4*k*nu
            amplitude2 = abs(phi)**2
            amplitude_v2 = (np.real(np.conj(phi)*V)**2/amplitude2
                             if amplitude2 > 1e-28 else abs(V)**2)
            integrands = np.array([r*abs(V)**2/omega2,
                                   r*amplitude_v2/omega2, r**3*omega2*amplitude2])
            expansion = -(1-2*m/r)/(4*nu)
            if 'previous' not in ray:
                ray.update(initial_time=t, initial_Q=float(Q), initial_expansion=float(expansion),
                           integrals=np.zeros(3), maximum_transport_defect=0.,
                           minimum_necessary_slack=float(expansion))
            else:
                previous_t, previous_integrands = ray['previous']
                # dv=2 dt on u=constant.
                ray['integrals'] += (t-previous_t)*(previous_integrands+integrands)
            F, Fa, H = ray['integrals']
            minimum_charge_cost = (Q-ray['initial_Q'])**2/(.36*H) if H > 1e-28 else 0.
            necessary_slack = ray['initial_expansion']-Fa-minimum_charge_cost
            defect = expansion-ray['initial_expansion']+F
            ray.update(previous=(t, integrands), final_time=t, final_radius=float(r),
                       final_Q=float(Q), final_expansion=float(expansion),
                       minimum_charge_cost=float(minimum_charge_cost),
                       phase_excess=float(F-Fa-minimum_charge_cost),
                       maximum_transport_defect=max(ray['maximum_transport_defect'], abs(float(defect))),
                       minimum_necessary_slack=min(ray['minimum_necessary_slack'], float(necessary_slack)))
        if t+1e-10 < self.next_sample:
            return
        self.next_sample += self.interval
        monotone = bool(np.all(np.diff(state[:, 0]) > 0))
        gates = []
        if monotone:
            for radius in self.radii:
                if not state[0, 0] <= radius <= state[-1, 0]:
                    gates.append(dict(radius=radius, covered=False))
                    continue
                y = self.interpolate(state[:, 0], state, radius)
                m, Q = y[7], y[10]
                gates.append(dict(radius=radius, covered=True, hawking_mass=float(m),
                                  renormalized_mass=float(m+Q*Q/(2*radius)), charge=float(Q),
                                  f=float(1-2*m/radius)))
        self.samples.append(dict(time=t, axis_proper_time=self.axis_proper_time,
                                 areal_radius_monotone=monotone, gates=gates))

    def report(self):
        rays = []
        for original in self.rays.values():
            ray = {k: v for k, v in original.items() if k not in ('previous', 'integrals')}
            if 'integrals' in original:
                ray['integrated_focusing'], ray['amplitude_cost'], ray['weighted_amplitude_capacity'] = map(float, original['integrals'])
            rays.append(ray)
        return dict(fixed_radius_samples=self.samples, null_ray_budgets=rays,
                    axis_proper_time=self.axis_proper_time,
                    limitations=['finite causal diamond, not the whole future',
                                 'interpolated diagnostics and trapezoidal integrals have no certified error',
                                 'finite-radius mass is not final Bondi mass',
                                 'axis proper time uses accepted axis rows only'])


def run(parameters, time, steps, save_arrays=None):
    data = ChargePreservingShell(parameters, exterior_width=max(10., 2*time+2*parameters.radius))
    observer = Diagnostics(data, time)
    result = evolve_centered(data.state_at_proper, axis_state(.5, 0j), 0j,
                             data.proper_max, time, steps, observer=observer)
    if result['completed']:
        arrays = {key: result.pop(key) for key in ('x', 'state', 'initial_state')}
        if save_arrays is not None:
            np.savez_compressed(save_arrays, **arrays)
    result.update(initial_data=data.summary(), diagnostics=observer.report(),
                  requested_time=time, requested_steps=steps,
                  finite_PDE_error_certified=False, full_future_classified=False,
                  positive_mass_long_residence_proved=False, goal_A_proved=False)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--amplitude', type=float, default=.2)
    parser.add_argument('--frequency', type=float, default=.3)
    parser.add_argument('--direction', type=float, default=0.)
    parser.add_argument('--radius', type=float, default=10.)
    parser.add_argument('--width', type=float, default=4.)
    parser.add_argument('--time', type=float, default=20.)
    parser.add_argument('--steps', type=int, default=1024)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--save-arrays', action='store_true')
    args = parser.parse_args()
    parameters = ShellParameters(**{key: getattr(args, key) for key in asdict(ShellParameters())})
    try:
        result = run(parameters, args.time, args.steps,
                     args.output.with_suffix('.npz') if args.save_arrays else None)
    except (ArithmeticError, ValueError) as error:
        result = dict(parameters=asdict(parameters), completed=False, failure=str(error),
                      finite_PDE_error_certified=False, full_future_classified=False, goal_A_proved=False)
    names = ['charge_preserving_shell.py', 'screen_charge_preserving_shell.py',
             'centered_cauchy_diamond.py', 'charged_cauchy_diamond.py', 'charged_lobatto.py']
    folder = Path(__file__).resolve().parent
    result['source_sha256'] = {name: sha256((folder/name).read_bytes()).hexdigest() for name in names}
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('axis', 'history', 'source_sha256', 'diagnostics')}, indent=2))
