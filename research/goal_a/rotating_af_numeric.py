"""Smooth free profiles from E0 past slices, followed by constraint re-solving.

Flat blends of finite Taylor polynomials define C-infinity functions over the
reals. Binary64 evaluation and numerical constraint positivity remain E0. This
does NOT preserve the original characteristic seed exactly.
"""
import json
from pathlib import Path
from hashlib import sha256
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
from constraint_contraction import Profile, rhs, reconstruct
from incoming_family import exterior_minimum
from rotating_past_slice import transition


def step(t):
    h = transition(t)
    hp = 0. if h == 0 or h == 1 else h*(1-h)*(1/t**2+1/(1-t)**2)
    return h, hp


class SmoothFreeProfile:
    def __init__(self, arrays, width):
        self.r = np.asarray(arrays['r'])
        if width <= 0 or not np.isfinite(width) or np.any(np.diff(self.r) <= 0):
            raise ValueError('positive width and strictly increasing radii required')
        # Three complex columns; ell remains real. Derivative jets come from a
        # spline only at the nodes; the actual interpolant uses flat blends.
        values = np.column_stack([arrays['phi'], arrays['chi'], arrays['ell']])
        spline = CubicSpline(self.r, values)
        self.jets = np.stack([
            spline(self.r), spline(self.r, 1), spline(self.r, 2)/2, spline(self.r, 3)/6], axis=1)
        self.jets[0, :, :2] = 0.  # Exact vacuum onset, not fitted nonzero jets.
        # The graph is identically ell=0 in this terminal tail, by construction.
        tail = arrays['v'] >= arrays['v'][0]+1.06*(arrays['v'][-1]-arrays['v'][0])/1.125
        self.jets[tail, :, 2] = 0.
        self.width = width
        self.hleft = min(self.r[1]-self.r[0], self.r[0]/8)
        self.hright = self.r[-1]-self.r[-2]
        self.inner = self.r[0]/2
        self.outer = self.r[-1]+self.hright+width
        self.profile = Profile(self.inner, self.outer, self.free)
        self.breaks = np.unique(np.r_[self.inner, self.r[0]-self.hleft,
                                     self.r, self.r[-1]+self.hright, self.outer])

    def polynomial(self, i, r):
        x = r-self.r[i]
        a, b, c, d = self.jets[i]
        return a+x*(b+x*(c+x*d)), b+x*(2*c+3*x*d)

    @staticmethod
    def blend(a, ap, b, bp, t, length):
        h, hp = step(t)
        return (1-h)*a+h*b, (1-h)*ap+h*bp+(hp/length)*(b-a)

    def values(self, r):
        zero = np.zeros(3, dtype=complex)
        if r <= self.inner or r >= self.outer:
            return zero, zero
        if r < self.r[0]:
            constant = self.jets[0, 0]
            joint = self.r[0]-self.hleft
            if r < joint:
                return self.blend(zero, zero, constant, zero,
                                  (r-self.inner)/(joint-self.inner), joint-self.inner)
            value, derivative = self.polynomial(0, r)
            return self.blend(constant, zero, value, derivative,
                              (r-joint)/self.hleft, self.hleft)
        if r > self.r[-1]:
            constant = self.jets[-1, 0]
            joint = self.r[-1]+self.hright
            if r < joint:
                value, derivative = self.polynomial(-1, r)
                return self.blend(value, derivative, constant, zero,
                                  (r-self.r[-1])/self.hright, self.hright)
            return self.blend(constant, zero, zero, zero,
                              (r-joint)/self.width, self.width)
        i = min(np.searchsorted(self.r, r, side='right')-1, len(self.r)-2)
        length = self.r[i+1]-self.r[i]
        a, ap = self.polynomial(i, r)
        b, bp = self.polynomial(i+1, r)
        return self.blend(a, ap, b, bp, (r-self.r[i])/length, length)

    def free(self, r):
        value, derivative = self.values(r)
        return value[0], derivative[0], value[1], float(value[2].real), float(derivative[2].real)


def solve(smooth, parameter, tolerance=2e-10):
    if not 0 <= parameter <= 1:
        raise ValueError('contraction parameter must be in [0,1]')
    profile = smooth.profile
    profile.validate()
    state = np.array([0., 1.])
    radii, states = [profile.inner], [state.copy()]
    # Each blend interval is resolved separately; a global adaptive solver could
    # skip a narrow collar whose sources vanish at its endpoints.
    for left, right in zip(smooth.breaks[:-1], smooth.breaks[1:]):
        sol = solve_ivp(lambda r, y: rhs(r, y, profile, parameter), (left, right), state,
                        method='DOP853', rtol=tolerance, atol=tolerance/100,
                        max_step=(right-left)/3)
        if not sol.success:
            raise ArithmeticError(sol.message)
        radii.extend(sol.t[1:])
        states.extend(sol.y[:, 1:].T)
        state = sol.y[:, -1]
    radii, states = np.array(radii), np.array(states)
    Q, f = states[-1]
    mass = profile.outer*(1-f)/2+Q*Q/(2*profile.outer)
    tail_min = exterior_minimum(mass, Q, profile.outer)
    if tail_min <= 0:
        raise ArithmeticError('RN exterior not everywhere untrapped')
    rows = [reconstruct(r, y[1], y[0], profile, parameter) for r, y in zip(radii, states)]
    result = dict(parameter=parameter, tolerance=tolerance, inner=profile.inner, outer=profile.outer,
        ADM_mass=float(mass), ADM_charge=float(Q), ADM_mass_minus_abs_charge=float(mass-abs(Q)),
        minimum_sampled_f=float(min(states[:, 1])), analytic_tail_minimum_binary64=float(tail_min),
        minimum_sampled_expansion_out=float(min(row['expansion_out'] for row in rows)),
        maximum_sampled_expansion_in=float(max(row['expansion_in'] for row in rows)),
        integration_nodes=len(radii), all_radius_error_certified=False,
        exact_original_seed_preserved=False, future_evolved=False, goal_A_proved=False)
    return result, dict(r=radii, Q=states[:, 0], f=states[:, 1])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('slice', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--parameters', type=float, nargs='+', default=[0., .5, 1.])
    parser.add_argument('--tolerance', type=float, default=2e-10)
    args = parser.parse_args()
    source = json.loads(args.slice.read_text(encoding='utf-8'))
    with np.load(args.slice.with_suffix('.npz')) as data:
        smooth = SmoothFreeProfile(dict(data), width=source['depth'])
    runs = []
    for parameter in args.parameters:
        try:
            result, arrays = solve(smooth, parameter, args.tolerance)
            # Keep each solved member for independent reconstruction checks.
            np.savez_compressed(args.output.with_name(args.output.stem+f'_S{parameter:g}.npz'), **arrays)
        except (ArithmeticError, ValueError, FloatingPointError) as error:
            result = dict(parameter=parameter, failure=str(error), goal_A_proved=False)
        runs.append(result)
        print(json.dumps(result), flush=True)
    folder = Path(__file__).resolve().parent
    names = ['rotating_af_numeric.py', 'rotating_past_slice.py', 'constraint_contraction.py', 'incoming_family.py']
    report = dict(source_slice=str(args.slice.name), source_slice_sha256=sha256(args.slice.read_bytes()).hexdigest(),
        source_array_sha256=sha256(args.slice.with_suffix('.npz').read_bytes()).hexdigest(),
        source_sha256={name: sha256((folder/name).read_bytes()).hexdigest() for name in names},
        runs=runs, evidence='E0 AF constraint re-solving of explicit smooth approximant profiles',
        full_AF_realization_certified=False, original_characteristic_seed_exact=False,
        early_future_screen_passed=False, critical_three_branch_theorem=False)
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
