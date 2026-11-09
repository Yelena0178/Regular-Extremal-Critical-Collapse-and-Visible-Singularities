"""E0 past-strip extraction for the two rotating seeds, not an AF certificate.

The graph is inside a numerical characteristic strip.  Interpolation and ODE
errors are not enclosed.  Returned arrays do not define a complete C-infinity
Cauchy datum; the regular cap and AF free-data extension must still be supplied.
"""
from dataclasses import asdict
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import RectBivariateSpline, CubicSpline
from early_charged_pulse_candidate import Pulse, characteristic_data
from charged_lobatto import evolve
from constraint_contraction import scalar_mass_source


def transition(t):
    if t <= 0:
        return 0.
    if t >= 1:
        return 1.
    # Logistic form of exp(-1/t)/(exp(-1/t)+exp(-1/(1-t))).
    exponent = 1/t-1/(1-t)
    return 0. if exponent > 700 else 1. if exponent < -700 else 1/(1+np.exp(exponent))


def pullback(state, p, phase=0.):
    """Area-radius free fields in radial gauge, D=|grad_Sigma r|^2.

    phase' in graph coordinate v must be e*p*A_u, with phase zero at the cap.
    The returned gradient is d(phi_radial)/dr only for that phase evolution.
    """
    r, kappa, tr, ti, nu, zr, zi, m, pr, pi, Q, Au = state
    if not (r > 0 and kappa > 0 and nu < 0 and p < 0):
        raise ValueError('positive radius/kappa, negative nu and spacelike slope required')
    f = 1-2*m/r
    lam = kappa*f
    omega2 = -4*kappa*nu
    radial_speed = lam+p*nu
    if f <= 0 or radial_speed <= 0:
        raise ValueError('untrapped positive radial orientation required')
    lapse_on_graph = np.sqrt(-omega2*p)
    rootD = radial_speed/lapse_on_graph
    P = nu*complex(zr, zi)/r
    pv = complex(tr, ti)/r
    rotation = np.exp(1j*phase)
    return dict(r=r, Q=Q, m=m, f=f, D=rootD**2,
                phi=rotation*complex(pr, pi),
                gradient=rotation*(p*P+pv)/radial_speed,
                chi=rotation*(-p*P+pv)/radial_speed,
                ell=-(lam-p*nu)/(r*lapse_on_graph),
                radial_speed=radial_speed, lam=lam, omega2=omega2,
                expansion_out=4*lam/(r*lapse_on_graph),
                expansion_in=4*p*nu/(-r*lapse_on_graph))


def compute(cfg, n=48, depth_ratio=.08):
    if not isinstance(n, int) or n < 16 or n % 8:
        raise ValueError('n must be a positive multiple of 8, at least 16')
    if not 0 < depth_ratio <= .1:
        raise ValueError('depth_ratio must be in (0,.1]')
    out, inc, cap, scale, radius, parameters = characteristic_data(cfg)
    depth = depth_ratio*radius
    # A finite zero longitudinal-field tail; no RN open set is imposed.
    v = cap+scale*np.arange(n+n//8+1)/n
    data = evolve(out, inc, -depth, v, n)
    states = data['state'][::-1]
    u = data['u'][::-1]
    splines = [RectBivariateSpline(u, v, states[..., j]) for j in range(12)]
    logomega = RectBivariateSpline(u, v, np.log(-4*states[..., 1]*states[..., 4]))

    def state_at(U, V):
        if not (-depth <= U <= 0 and v[0] <= V <= v[-1]):
            raise ArithmeticError('graph left the computed strip')
        return np.array([sp.ev(U, V) for sp in splines])

    p0 = -depth/(4*scale)

    def slope(U, V, state):
        t = (V-cap)/scale
        weight = transition((t-1)/.04)
        lam = state[1]*(1-2*state[7]/state[0])
        return (1-weight)*p0+weight*lam/state[4]

    def graph_rhs(V, y):
        x = state_at(y[0], V)
        p = slope(y[0], V, x)
        if p >= 0:
            raise ArithmeticError('graph lost spacelike character')
        return [p, .6*p*x[11]]

    graph = solve_ivp(graph_rhs, (v[0], v[-1]), [-depth/3, 0.],
                      method='DOP853', rtol=2e-11, atol=2e-13,
                      max_step=scale/(4*n), dense_output=True)
    if not graph.success:
        raise ArithmeticError(graph.message)
    vs = np.linspace(v[0], v[-1], 4*(len(v)-1)+1)
    us, phase = graph.sol(vs)
    rows, slopes, raw, log_u, log_v = [], [], [], [], []
    for U, V, angle in zip(us, vs, phase):
        x = state_at(U, V)
        p = slope(U, V, x)
        rows.append(pullback(x, p, angle))
        slopes.append(p)
        raw.append(x)
        log_u.append(logomega.ev(U, V, dx=1))
        log_v.append(logomega.ev(U, V, dy=1))
    fields = {key: np.array([row[key] for row in rows]) for key in rows[0]}
    slopes, raw = np.array(slopes), np.array(raw)
    speed, r = fields['radial_speed'], fields['r']
    if np.any(np.diff(r) <= 0):
        raise ArithmeticError('sampled area-radius graph is not monotone')

    def derivative(values):
        return CubicSpline(vs, values).derivative()(vs)

    ellprime = derivative(fields['ell'])/speed
    J = np.real(fields['chi']*np.conj(fields['gradient']))
    k_constraint = fields['ell']+r*ellprime-r*np.sqrt(fields['D'])*J
    # Independently differentiate the graph normal using its 2D Christoffels.
    k_geometric = -(derivative(slopes)+slopes**2*np.array(log_u)
                    -slopes*np.array(log_v))/(2*np.sqrt(fields['omega2'])*(-slopes)**1.5)
    source = np.array([scalar_mass_source(row['r'], row['f'], row['gradient'],
                                         row['chi'], row['ell']) for row in rows])
    residual_arrays = dict(
        radial_transport=derivative(r)-speed,
        scalar_radial_gauge=derivative(fields['phi'])/speed-fields['gradient'],
        charge=derivative(fields['Q'])/speed-.6*r*r*np.imag(fields['phi']*np.conj(fields['chi'])),
        hawking_mass=derivative(fields['m'])/speed-fields['Q']**2/(2*r*r)-source,
        radial_extrinsic_curvature=k_geometric-k_constraint)
    # A compact subdomain avoids endpoint spline derivatives and isolates the
    # matter-bearing region. Full sampled extrema are recorded separately.
    t = (vs-cap)/scale
    bulk = (t >= .08) & (t <= .92)
    residuals = {key: float(np.max(np.abs(value[bulk]))) for key, value in residual_arrays.items()}
    tail = t >= 1.06
    gauge_omission = derivative(raw[:, 8]+1j*raw[:, 9])/speed-(
        fields['gradient']*np.exp(-1j*phase))
    terminal = {key: (dict(real=float(value[-1].real), imag=float(value[-1].imag))
                     if np.iscomplexobj(value) else float(value[-1]))
                for key, value in fields.items()}
    summary = dict(configuration=asdict(cfg), n=n, depth=depth, parameters=parameters,
        strip=dict(u_min=float(u[0]), u_max=float(u[-1]), v_min=float(v[0]), v_max=float(v[-1])),
        graph=dict(u_start=float(us[0]), u_end=float(us[-1]),
                   minimum_sampled_f=float(min(fields['f'])),
                   minimum_sampled_lambda=float(min(fields['lam'])),
                   minimum_sampled_expansion_out=float(min(fields['expansion_out'])),
                   maximum_sampled_expansion_in=float(max(fields['expansion_in'])),
                   maximum_tail_abs_ell=float(max(abs(fields['ell'][tail]))),
                   final_radial_gauge_phase=float(phase[-1])),
        bulk_residuals=residuals,
        omitted_gauge_bulk_residual=float(max(abs(gauge_omission[bulk]))),
        algebraic_metric_identity=float(max(abs(fields['D']-(fields['f']+(r*fields['ell'])**2)))),
        terminal=terminal, iterations=data['iteration_report'],
        evidence='E0 interpolated actual-seed past strip and finite spatial graph',
        rigorous_PDE_error=False, complete_AF_free_data=False,
        certified_C_infinity_profile=False, critical_curve_located=False, goal_A_proved=False)
    arrays = dict(v=vs, u=us, phase=phase, slope=slopes, ellprime=ellprime,
                  k_geometric=k_geometric, k_constraint=k_constraint, **fields)
    return summary, arrays


if __name__ == '__main__':
    import argparse
    import json
    from hashlib import sha256
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=48)
    parser.add_argument('--amplitude', type=float, default=.2)
    parser.add_argument('--frequency', type=float, default=8.)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    summary, arrays = compute(Pulse(args.amplitude, args.frequency), args.n)
    names = ['rotating_past_slice.py', 'early_charged_pulse_candidate.py',
             'charged_lobatto.py', 'constraint_contraction.py', '../../definitions/MODEL.md']
    folder = Path(__file__).resolve().parent
    summary['source_sha256'] = {name: sha256((folder/name).read_bytes()).hexdigest() for name in names}
    args.output.write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    np.savez_compressed(args.output.with_suffix('.npz'), **arrays)
    print(json.dumps(summary, indent=2))
