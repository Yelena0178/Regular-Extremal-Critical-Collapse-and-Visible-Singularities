"""Horizon-regular rational neutral transport system; numerical solver is E0.

State order: r, kappa, theta=r*phi_v, nu=r_u, z=r*phi_u/nu, m.
The first three components evolve in u, the other three in v.
"""

from dataclasses import dataclass, asdict
import math
import numpy as np
from scipy.integrate import solve_ivp
from neutral_onset_input import NeutralOnset, smooth_step


def rhs(x):
    r, k, t, n, z, m = x
    return np.array((n, k*n*z*z/r, -k*n*z*(1-2*m/r)/r,
                     2*k*m*n/(r*r), -t/r-2*k*m*z/(r*r), t*t/(2*k)))


def jacobian(x):
    r, k, t, n, z, m = np.moveaxis(np.asarray(x), -1, 0)
    result = np.zeros(np.shape(r)+(6, 6))
    result[..., 0, 3] = 1
    result[..., 1, 0] = -k*n*z*z/r**2
    result[..., 1, 1] = n*z*z/r
    result[..., 1, 3] = k*z*z/r
    result[..., 1, 4] = 2*k*n*z/r
    result[..., 2, 0] = k*n*z/r**2-4*k*m*n*z/r**3
    result[..., 2, 1] = -n*z/r+2*m*n*z/r**2
    result[..., 2, 3] = -k*z/r+2*k*m*z/r**2
    result[..., 2, 4] = -k*n/r+2*k*m*n/r**2
    result[..., 2, 5] = 2*k*n*z/r**2
    result[..., 3, 0] = -4*k*m*n/r**3
    result[..., 3, 1] = 2*m*n/r**2
    result[..., 3, 3] = 2*k*m/r**2
    result[..., 3, 5] = 2*k*n/r**2
    result[..., 4, 0] = t/r**2+4*k*m*z/r**3
    result[..., 4, 1] = -2*m*z/r**2
    result[..., 4, 2] = -1/r
    result[..., 4, 4] = -2*k*m/r**2
    result[..., 4, 5] = -2*k*z/r**2
    result[..., 5, 1] = -t*t/(2*k*k)
    result[..., 5, 2] = t/k
    return result


def geometry(x):
    r, k, t, n, z, m = map(float, x)
    lam = k*(1-2*m/r)
    omega2 = -4*k*n
    return {"r": r, "kappa": k, "theta": t, "nu": n, "z": z, "m": m,
            "lambda": lam, "Omega2": omega2,
            "theta_out": 4*lam/math.sqrt(omega2)/r,
            "theta_in": 4*n/math.sqrt(omega2)/r}


@dataclass(frozen=True)
class TransportConfiguration:
    steps_u: int = 96
    steps_v: int = 96
    final_u: float = 2.4
    initial_v: float = 3.18590740224706
    final_v: float = 4.694709557334082
    max_iterations: int = 16
    iteration_tolerance: float = 2e-13
    failure_tolerance: float = 2e-10


def evolve(outgoing, incoming, cfg):
    u = np.linspace(0., cfg.final_u, cfg.steps_u+1)
    v = np.linspace(cfg.initial_v, cfg.final_v, cfg.steps_v+1)
    du, dv = u[1], v[1]-v[0]
    if not 0 < cfg.final_u < cfg.initial_v < cfg.final_v:
        raise ValueError("positive-radius pre-axis rectangle required")
    data = np.empty((len(u), len(v), 6))
    values = np.empty_like(data)
    for j, advanced in enumerate(v):
        data[0, j] = outgoing(float(advanced))
        values[0, j] = rhs(data[0, j])
    for i, retarded in enumerate(u):
        incoming_value = np.asarray(incoming(float(retarded)))
        if i == 0 and np.max(abs(incoming_value-data[0, 0])) > 1e-10:
            raise ValueError("inconsistent corner data")
        data[i, 0] = incoming_value
        values[i, 0] = rhs(data[i, 0])
    maximum_change = 0.
    for i in range(1, len(u)):
        for j in range(1, len(v)):
            base = np.concatenate((data[i-1, j, :3]+du*values[i-1, j, :3]/2,
                                   data[i, j-1, 3:]+dv*values[i, j-1, 3:]/2))
            scale = np.array((du/2,)*3+(dv/2,)*3)
            x = base.copy()
            for iteration in range(cfg.max_iterations):
                new = base+scale*rhs(x)
                change = float(np.max(abs(new-x)))
                x = new
                if change < cfg.iteration_tolerance:
                    break
            if (change > cfg.failure_tolerance or not np.all(np.isfinite(x))
                    or x[0] <= 0 or x[1] <= 0 or x[3] >= 0):
                raise ArithmeticError(f"E0 transport cell failed at {(i,j)}; change={change}")
            maximum_change = max(maximum_change, change)
            data[i, j] = x
            values[i, j] = rhs(x)
    return {"u": u, "v": v, "state": data, "rhs": values,
            "report": {"configuration": asdict(cfg), "maximum_last_iteration_change": maximum_change,
                       "evidence": "E0_rational_transport_trapezoid",
                       "rigorous_PDE_error": False, "actual_strict_trapping_certified": False}}


def onset_boundaries(epsilon=.05):
    if not 0 < epsilon < .5:
        raise ValueError('this transport entry requires a resolved positive onset smoothing')
    model = NeutralOnset.from_first_jet_report(epsilon)
    p = model.parameters()
    cap, length, amplitude = p["v_cap"], p["v_onset_width"], p["field_amplitude"]

    def field_prime(v):
        x = (v-cap)/length
        if x <= 0:
            return 0.
        if epsilon == 0 or x >= epsilon:
            return amplitude/length
        chi, chip = smooth_step(x/epsilon)
        return amplitude/length*(chi+x/epsilon*chip)

    def boundary_rhs(v, y):
        r, lam, z = y
        q = field_prime(v)
        k, m = r/v, (r-v*lam)/2
        return (lam, -r*q*q, -q-2*k*m*z/(r*r))

    solution = solve_ivp(boundary_rhs, (cap, p["v_end"]), (p["r_cap"], .5, 0.),
                         method="DOP853", rtol=2e-12, atol=2e-14,
                         max_step=length/384, dense_output=True)
    if not solution.success:
        raise ArithmeticError("boundary numerical ODE failed")

    def outgoing(v):
        r, lam, z = solution.sol(v)
        return np.array((r, r/v, r*field_prime(v), -v/(4*r), z, (r-v*lam)/2))

    def incoming(u):
        return np.array((p["r_cap"]-u/2, .5, 0., -.5, 0., 0.))

    return outgoing, incoming, p


def fourth_derivative(data, axis, spacing):
    """Fourth-order first derivative, including one-sided endpoint stencils."""
    f = np.moveaxis(data, axis, 0)
    if len(f) < 5:
        raise ValueError("five nodes required")
    d = np.empty_like(f)
    d[2:-2] = (f[:-4]-8*f[1:-3]+8*f[3:-1]-f[4:])/(12*spacing)
    d[0] = (-25*f[0]+48*f[1]-36*f[2]+16*f[3]-3*f[4])/(12*spacing)
    d[1] = (-3*f[0]-10*f[1]+18*f[2]-6*f[3]+f[4])/(12*spacing)
    d[-1] = (25*f[-1]-48*f[-2]+36*f[-3]-16*f[-4]+3*f[-5])/(12*spacing)
    d[-2] = (3*f[-1]+10*f[-2]-18*f[-3]+6*f[-4]-f[-5])/(12*spacing)
    return np.moveaxis(d, 0, axis)


def hermite_coefficients(data):
    """Continuous bicubic interpolation; this construction is floating-point E0."""
    x, f = data["state"], data["rhs"]
    du, dv = data["u"][1], data["v"][1]-data["v"][0]
    xu, xv = fourth_derivative(x, 0, du), fourth_derivative(x, 1, dv)
    xu[..., :3] = f[..., :3]
    xv[..., 3:] = f[..., 3:]
    J = jacobian(x)
    xuv = np.empty_like(x)
    xuv[..., :3] = np.einsum("...ij,...j->...i", J[..., :3, :], xv)
    xuv[..., 3:] = np.einsum("...ij,...j->...i", J[..., 3:, :], xu)
    g = np.zeros((len(x)-1, x.shape[1]-1, 6, 4, 4))
    for i in (0, 1):
        for j in (0, 1):
            cut = (slice(i, len(x)-1+i), slice(j, x.shape[1]-1+j))
            g[..., i, j] = x[cut]
            g[..., i+2, j] = du*xu[cut]
            g[..., i, j+2] = dv*xv[cut]
            g[..., i+2, j+2] = du*dv*xuv[cut]
    H = np.array(((1,0,0,0),(0,0,1,0),(-3,3,-2,-1),(2,-2,1,1)), dtype=float)
    return np.einsum("ab,...bc,dc->...ad", H, g, H)
