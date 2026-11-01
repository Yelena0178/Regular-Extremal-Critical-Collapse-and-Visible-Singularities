"""E0 Cauchy evolution on a shrinking, positive-radius characteristic wedge.

The state ordering and equations are those of charged_lobatto.rhs. Each new
point has its two characteristic feet on the preceding time row. No artificial
inner/outer boundary data are supplied. No axis or PDE error certificate.
"""
import numpy as np
from charged_lobatto import rhs


def spatial_constraints(x, state):
    """Held-out Einstein/Maxwell/scalar constraints on a completed time row."""
    h = float(x[1]-x[0])
    dx = (state[:-4]-8*state[1:-3]+8*state[3:-1]-state[4:])/(12*h)
    y = state[2:-2]
    flow = rhs(y)
    r, k, nu, m, Q, Au = y[:, 0], y[:, 1], y[:, 4], y[:, 7], y[:, 10], y[:, 11]
    phi, z = y[:, 8]+1j*y[:, 9], y[:, 5]+1j*y[:, 6]
    f = 1-2*m/r
    residuals = dict(radius=dx[:, 0]+nu-k*f,
        scalar=flow[:, 8]+1j*flow[:, 9]-(dx[:, 8]+1j*dx[:, 9])+1j*.6*Au*phi-nu*z/r,
        charge=flow[:, 10]-dx[:, 10]+.6*r*nu*np.imag(phi*np.conj(z)),
        mass=flow[:, 7]-dx[:, 7]-Q*Q*nu/(2*r*r)-f*nu*abs(z)**2/2)
    return dict(maximum_absolute={key: float(max(abs(value))) for key, value in residuals.items()},
                x_range=[float(x[2]), float(x[-3])])


def evolve(initial, x_left, x_right, final_time, time_steps, snapshots=8,
           vacuum_state=None, vacuum_end=None, core_fill_time=0.):
    if not 0 < final_time or time_steps < 4 or not x_left < x_right:
        raise ValueError('invalid wedge controls')
    h = 2*final_time/time_steps
    intervals = int(np.floor((x_right-x_left)/h))
    if intervals <= time_steps+4:
        raise ValueError('Cauchy interval too short for requested diamond wedge')
    x = x_left+h*np.arange(intervals+1)
    state = np.array([initial(float(at)) for at in x])
    initial_state = state.copy()
    flow = rhs(state)
    maximum_iterations = 0
    maximum_change = 0.
    records = []
    first_negative = None
    worst = None

    def record(t, values, positions):
        nonlocal first_negative, worst
        r, k, nu, m = values[:, 0], values[:, 1], values[:, 4], values[:, 7]
        lam = k*(1-2*m/r)
        i = int(np.argmin(lam))
        point = dict(time=float(t), x=float(positions[i]), radius=float(r[i]),
                     lambda_value=float(lam[i]), nu=float(nu[i]),
                     Q=float(values[i, 10]), f=float(1-2*m[i]/r[i]))
        if worst is None or point['lambda_value'] < worst['lambda_value']:
            worst = point
        if first_negative is None and point['lambda_value'] < 0:
            first_negative = point
        return point

    records.append(record(0., state, x))
    core_fill_steps = min(time_steps, int(np.floor(2*core_fill_time/h)))
    if core_fill_steps and (vacuum_state is None or vacuum_end is None or x_left <= h/2
                           or core_fill_steps*h/2+x_left >= vacuum_end):
        raise ValueError('flat-core filling exceeds its domain or touches the axis')
    for step in range(1, time_steps+1):
        if step <= core_fill_steps and step % 2 == 0:
            ghost_x = x[0]-h
            ghost = vacuum_state((step-1)*h/2, float(ghost_x))
            x = np.r_[ghost_x, x]
            state = np.concatenate([ghost[None, :], state])
            flow = np.concatenate([rhs(ghost)[None, :], flow])
        # du=dv=h along the two sides, while the row time advances h/2.
        fixed = np.concatenate([state[1:, :4]+h*flow[1:, :4]/2,
                                state[:-1, 4:]+h*flow[:-1, 4:]/2], axis=1)
        value = np.concatenate([state[1:, :4], state[:-1, 4:]], axis=1)
        for iteration in range(64):
            new = fixed+h*rhs(value)/2
            change = float(np.max(abs(new-value)))
            value = new
            if change < 3e-12:
                break
        if (not np.isfinite(value).all() or change > 1e-9 or np.min(value[:, 0]) <= 0
                or np.min(value[:, 1]) <= 0 or np.max(value[:, 4]) >= 0):
            return dict(completed=False, failure='iteration/regularity stop; outcome UNKNOWN',
                        failed_time=step*h/2, maximum_change=change,
                        last_completed_time=(step-1)*h/2, worst=worst,
                        first_negative_sample=first_negative, history=records)
        x = (x[:-1]+x[1:])/2
        if vacuum_state is not None:
            for j in np.flatnonzero(step*h/2+x <= vacuum_end):
                value[j] = vacuum_state(step*h/2, float(x[j]))
        state, flow = value, rhs(value)
        maximum_iterations = max(maximum_iterations, iteration+1)
        maximum_change = max(maximum_change, change)
        point = record(step*h/2, state, x)
        if step % max(1, time_steps//snapshots) == 0 or step == time_steps:
            records.append(point)
    return dict(completed=True, final_time=final_time, time_steps=time_steps,
                initial_spatial_intervals=intervals, spacing=h,
                initial_x_left=x_left, initial_x_right=x_left+intervals*h,
                core_fill_time=core_fill_steps*h/2,
                maximum_outgoing_coordinate=float(final_time-x[0]),
                final_x_left=float(x[0]), final_x_right=float(x[-1]),
                maximum_iterations=maximum_iterations, maximum_change=maximum_change,
                worst=worst, first_negative_sample=first_negative, history=records,
                final_row_constraints=spatial_constraints(x, state),
                x=x, state=state, initial_state=initial_state,
                evidence='E0 second-order characteristic-foot trapezoidal Cauchy scheme',
                finite_PDE_error_certified=False, full_future_classified=False)


if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    from hashlib import sha256
    from canonical_cauchy_data import CanonicalCauchyData
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('--time', type=float, default=2.)
    parser.add_argument('--steps', type=int, default=128)
    parser.add_argument('--parameter', type=float, default=1.)
    parser.add_argument('--fill-core', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = CanonicalCauchyData(args.input, args.parameter)
    x_left = .04*data.vacuum_proper_end if args.fill_core else .5
    fill_time = .94*data.vacuum_proper_end if args.fill_core else 0.
    result = evolve(data.state_at_proper, x_left, data.proper_max, args.time, args.steps,
                    vacuum_state=data.vacuum_state if args.fill_core else None,
                    vacuum_end=data.vacuum_proper_end if args.fill_core else None,
                    core_fill_time=fill_time)
    if result['completed']:
        arrays = {key: result.pop(key) for key in ('x', 'state', 'initial_state')}
        np.savez_compressed(args.output.with_suffix('.npz'), **arrays)
    result['initial_data'] = data.summary()
    result['goal_A_proved'] = False
    folder = Path(__file__).resolve().parent
    names = ['charged_cauchy_diamond.py', 'canonical_cauchy_data.py', 'charged_lobatto.py',
             'constraint_contraction.py', 'rotating_af_numeric.py', 'certify_rotating_af_barrier.py']
    result['source_sha256'] = {name: sha256((folder/name).read_bytes()).hexdigest() for name in names}
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('history', 'source_sha256')}, indent=2), flush=True)
