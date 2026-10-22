"""E0 characteristic-foot evolution including a regular axis at u=v.

The axis gauge is A_u=0; A_v=0 everywhere. A non-vacuum axis is
reconstructed from the incoming foot, not prescribed as Minkowski data.
No PDE stability, regularity, or error certificate is claimed.
"""
import numpy as np
from charged_lobatto import rhs
from charged_cauchy_diamond import spatial_constraints


def axis_state(kappa, phi):
    return np.array([0., kappa, 0., 0., -kappa, 0., 0., 0.,
                     complex(phi).real, complex(phi).imag, 0., 0.])


def axis_flow(kappa, V):
    """Continuous regular-axis RHS limit, V=D_v phi at the axis."""
    V = complex(V)
    return np.array([-kappa, 0., -kappa*V.real, -kappa*V.imag,
                     0., -V.real, -V.imag, 0., V.real, V.imag, 0., 0.])


def reconstruct_axis(foot, flow, h):
    """Enforce r=0 and nu=-kappa on the incoming u-segment of length h."""
    k = 2*foot[0]/h+foot[4]
    theta = foot[2]+1j*foot[3]
    theta_u = flow[2]+1j*flow[3]
    V = (2*theta/h+theta_u)/k
    phi = foot[8]+1j*foot[9]
    P = foot[4]*(foot[5]+1j*foot[6])/foot[0]
    phi += h*(P-1j*.6*foot[11]*phi+V)/2
    state = axis_state(k, phi)
    radial_defect = foot[0]+h*(foot[4]-k)/2
    return state, axis_flow(k, V), V, float(radial_defect)


def evolve_centered(initial, initial_axis, initial_V, x_right, final_time, time_steps, axis_method='parity'):
    if time_steps < 8 or time_steps % 2 or final_time <= 0 or x_right <= final_time:
        raise ValueError('positive time, even steps >=8 and nonempty causal domain required')
    if axis_method not in ('parity', 'transport'):
        raise ValueError('unknown axis reconstruction')
    h = 2*final_time/time_steps
    intervals = int(np.floor(x_right/h))
    if intervals-time_steps//2 < 6:
        raise ValueError('outer domain too short')
    x = h*np.arange(intervals+1)
    state = np.vstack([initial_axis, [initial(float(at)) for at in x[1:]]])
    if not np.allclose(initial_axis, axis_state(initial_axis[1], initial_axis[8]+1j*initial_axis[9]),
                       rtol=0, atol=0) or initial_axis[1] <= 0:
        raise ValueError('incompatible regular-axis state')
    flow = np.vstack([axis_flow(initial_axis[1], initial_V), rhs(state[1:])])
    initial_state = state.copy()
    worst = None
    first_negative = None
    axis = [dict(time=0., kappa=float(initial_axis[1]), phi_abs=float(abs(initial_axis[8]+1j*initial_axis[9])),
                 V_abs=float(abs(initial_V)), incoming_radial_defect=0.)]
    history = []
    maximum_change = 0.
    maximum_axis_defect = 0.
    maximum_axis_kappa_defect = 0.

    def record(t):
        nonlocal worst, first_negative
        positive = state[:, 0] > 0
        y, xp = state[positive], x[positive]
        lam = y[:, 1]*(1-2*y[:, 7]/y[:, 0])
        j = int(np.argmin(lam))
        point = dict(time=float(t), x=float(xp[j]), radius=float(y[j, 0]),
                     lambda_value=float(lam[j]), nu=float(y[j, 4]), Q=float(y[j, 10]),
                     f=float(1-2*y[j, 7]/y[j, 0]))
        if worst is None or point['lambda_value'] < worst['lambda_value']:
            worst = point
        if first_negative is None and point['lambda_value'] < 0:
            first_negative = point
        return point

    history.append(record(0.))
    for step in range(1, time_steps+1):
        fixed = np.concatenate([state[1:, :4]+h*flow[1:, :4]/2,
                                state[:-1, 4:]+h*flow[:-1, 4:]/2], axis=1)
        value = np.concatenate([state[1:, :4], state[:-1, 4:]], axis=1)
        for iteration in range(64):
            end_flow = rhs(value)
            new = fixed+h*end_flow/2
            if state[0, 0] == 0:
                # m,Q vanish cubically from a regular axis, so their
                # v-sources vanish quadratically. Trapezoidal h/2
                # gives the wrong leading coefficient (3/2 times exact).
                # Integrate the leading quadratic with h/3 instead.
                new[0, [7, 10]] = h*end_flow[0, [7, 10]]/3
            change = float(np.max(abs(new-value)))
            value = new
            if change < 3e-12:
                break
        if (not np.isfinite(value).all() or change > 1e-9 or np.min(value[:, 0]) <= 0
                or np.min(value[:, 1]) <= 0 or np.max(value[:, 4]) >= 0):
            return dict(completed=False, failure='positive-radius update stopped; outcome UNKNOWN',
                        failed_time=step*h/2, last_completed_time=(step-1)*h/2,
                        worst=worst, first_negative_sample=first_negative, history=history, axis=axis)
        new_x = (x[:-1]+x[1:])/2
        new_flow = rhs(value)
        if step % 2 == 0:
            center, center_flow, V, defect = reconstruct_axis(state[0], flow[0], h)
            kappa_defect = center[1]-state[0, 1]-h*flow[0, 1]/2
            if axis_method == 'parity':
                # In A_u=0 on the axis, phi_x=0 and (D_t phi)_x=0.
                # A_u=O(x^2); odd gauge terms start at x^3, so this
                # two-point even extrapolation has O(h^3) local error.
                near = value[:2]
                phi_near = near[:, 8]+1j*near[:, 9]
                V_near = (near[:, 2]+1j*near[:, 3]
                          +near[:, 4]*(near[:, 5]+1j*near[:, 6]))/(2*near[:, 0])
                phi_axis = (4*phi_near[0]-phi_near[1])/3
                V = (4*V_near[0]-V_near[1])/3
                center = axis_state(center[1], phi_axis)
                center_flow = axis_flow(center[1], V)
            if not np.isfinite(center).all() or center[1] <= 0:
                return dict(completed=False, failure='axis update stopped; outcome UNKNOWN',
                            failed_time=step*h/2, worst=worst, history=history, axis=axis)
            value = np.vstack([center, value])
            new_flow = np.vstack([center_flow, new_flow])
            new_x = np.r_[0., new_x]
            maximum_axis_defect = max(maximum_axis_defect, abs(defect))
            maximum_axis_kappa_defect = max(maximum_axis_kappa_defect, abs(kappa_defect))
            axis.append(dict(time=step*h/2, kappa=float(center[1]),
                             phi_abs=float(abs(center[8]+1j*center[9])), V_abs=float(abs(V)),
                             incoming_radial_defect=defect, incoming_kappa_defect=float(kappa_defect)))
        state, flow, x = value, new_flow, new_x
        maximum_change = max(maximum_change, change)
        point = record(step*h/2)
        if step % max(1, time_steps//16) == 0 or step == time_steps:
            history.append(point)
    return dict(completed=True, final_time=final_time, time_steps=time_steps, spacing=h,
                final_x_left=float(x[0]), final_x_right=float(x[-1]),
                maximum_change=maximum_change, maximum_axis_radial_defect=maximum_axis_defect,
                maximum_axis_kappa_defect=maximum_axis_kappa_defect,
                worst=worst, first_negative_sample=first_negative, history=history, axis=axis,
                final_row_constraints=spatial_constraints(x, state),
                x=x, state=state, initial_state=initial_state,
                evidence='E0 characteristic-foot scheme with regular-axis endpoint reconstruction',
                axis_method=axis_method,
                finite_PDE_error_certified=False, full_future_classified=False)


if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    from hashlib import sha256
    from canonical_cauchy_data import CanonicalCauchyData
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('--parameter', type=float, default=1.001)
    parser.add_argument('--time', type=float, default=8.)
    parser.add_argument('--steps', type=int, default=1024)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = CanonicalCauchyData(args.input, args.parameter)
    result = evolve_centered(data.state_at_proper, axis_state(.5, 0j), 0j,
                             data.proper_max, args.time, args.steps)
    if result['completed']:
        arrays = {key: result.pop(key) for key in ('x', 'state', 'initial_state')}
        np.savez_compressed(args.output.with_suffix('.npz'), **arrays)
    result['initial_data'] = data.summary()
    result['goal_A_proved'] = False
    folder = Path(__file__).resolve().parent
    names = ['centered_cauchy_diamond.py', 'charged_cauchy_diamond.py', 'canonical_cauchy_data.py',
             'charged_lobatto.py', 'constraint_contraction.py', 'rotating_af_numeric.py',
             'certify_rotating_af_barrier.py']
    result['source_sha256'] = {name: sha256((folder/name).read_bytes()).hexdigest() for name in names}
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: val for key, val in result.items() if key not in ('axis', 'history', 'source_sha256')}, indent=2))
