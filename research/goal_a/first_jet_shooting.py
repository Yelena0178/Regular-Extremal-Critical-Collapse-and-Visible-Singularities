"""E0 first-transverse-jet shooting on a null cone, not a spacetime certificate.

The early C0 Schneider-shaped segment is compressed to [0,beta]. A late
constant-phase smooth pulse beta*W*g carries no additional Gauss charge.
The residual uses the full D001 charged wave transport.
"""

from dataclasses import asdict, dataclass
import cmath
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root


@dataclass(frozen=True)
class ShootingConfiguration:
    beta: float = .001
    coupling: float = .6
    radius: float = 5.
    amplitude: float = .5
    rtol: float = 2e-10
    atol: float = 2e-12
    max_step: float = .04

    def validate(self):
        if self.coupling != .6 or self.radius != 5. or self.amplitude != .5:
            raise ValueError("this shooting experiment fixes e=3/5, R=5, Phi=1/2")
        if not 0 <= self.beta < .1:
            raise ValueError("require 0 <= beta < 0.1; beta=0 is an auxiliary limit")


def late_bump(y):
    if not 0 < y < 1:
        return 0., 0.
    z = y*(1-y)
    value = math.exp(4-1/z)
    return value, value*(1-2*y)/(z*z)


def harmonic_transfer(value, derivative, rate, displacement):
    angle = rate*displacement
    cosine, sine = math.cos(angle), math.sin(angle)
    return (cosine*value+sine*derivative/rate,
            -rate*sine*value+cosine*derivative)


def prepare_radius(s, late_value, late_derivative, cfg):
    phi, beta = cfg.amplitude, cfg.beta
    if not .10 < s < .24:
        raise ValueError("s outside the exploratory regular parameter box")
    c = math.sqrt(s*(1-s))
    lam = c/phi
    v2 = s/(s+phi*math.tan(phi))
    v1 = v2*phi**(1/s)
    rate_off = phi/(1-v2)
    f2, p2 = harmonic_transfer(late_value, late_derivative, rate_off, v2-1)
    matrix = np.array([[v2**s, v2**(1-s)],
                       [s*v2**(s-1), (1-s)*v2**(-s)]])
    C, D = np.linalg.solve(matrix, np.array([f2, p2]))
    f1 = C*v1**s+D*v1**(1-s)
    p1 = s*C*v1**(s-1)+(1-s)*D*v1**(-s)
    f0, p0 = harmonic_transfer(f1, p1, phi/v1, -v1)
    if min(f0, f1, f2, late_value) <= 0 or p0 <= 0:
        raise ValueError("nonpositive radius or initial outgoing expansion")

    def charge(x):
        if x <= v1:
            return 0.
        x = min(x, v2)
        integral = (
            C*C*(x**(2*s)-v1**(2*s))/(2*s)
            + 2*C*D*(x-v1)
            + D*D*(x**(2-2*s)-v1**(2-2*s))/(2-2*s)
        )
        return cfg.coupling*cfg.radius*phi*c*integral

    return {"s": s, "c": c, "lam": lam, "v1": v1, "v2": v2,
            "C": C, "D": D, "f0": f0, "p0": p0, "f1": f1, "p1": p1,
            "f2": f2, "p2": p2, "charge": charge, "qf": charge(v2)}


def integrate_piece(function, state, end, cfg):
    result = solve_ivp(function, (0., end), np.asarray(state, dtype=float),
                       method="DOP853", rtol=cfg.rtol, atol=cfg.atol,
                       max_step=cfg.max_step, dense_output=True)
    if not result.success or not np.isfinite(result.y).all():
        raise ValueError("ODE integration failed: "+str(result.message))
    return result


def evaluate(parameters, cfg, diagnostics=False):
    cfg.validate()
    s, wr, wi = map(float, parameters)
    W = complex(wr, wi)
    beta, R, e, phi = cfg.beta, cfg.radius, cfg.coupling, cfg.amplitude
    amplitude_squared = beta*beta*abs(W)**2
    if abs(W) > 4.:
        raise ValueError("W outside exploratory box")

    def backward_rhs(y, values):
        _, gp = late_bump(y)
        return (values[1], -amplitude_squared*gp*gp*values[0])

    backward = solve_ivp(backward_rhs, (1., 0.), (1., 0.), method="DOP853",
                         rtol=cfg.rtol, atol=cfg.atol, max_step=cfg.max_step,
                         dense_output=True)
    if not backward.success:
        raise ValueError("late radial backward integration failed")
    fb, fyb = backward.y[:, -1]
    # The early coordinate is x=v/beta, so its terminal derivative is
    # beta/(1-beta) times the late y derivative.
    base = prepare_radius(s, fb, beta/(1-beta)*fyb, cfg)
    lam, v1, v2 = base["lam"], base["v1"], base["v2"]
    phase1, phase2 = cmath.exp(-1j*lam*math.log(v1)), cmath.exp(-1j*lam*math.log(v2))
    qf = base["qf"]

    # On the early segment, H/beta and J/beta obey regular equations even
    # at the nonphysical auxiliary value beta=0.
    def early_rhs(f, fx, q, field, field_derivative, dx_dz, state):
        Hhat = state[0]
        nuhat = -Hhat/(4*R*f)
        moment = (-nuhat*field_derivative
                  - 1j*e*q/(4*f)*field*dx_dz)
        return (dx_dz*(1-q*q/(f*f)), moment.real, moment.imag)

    def on_rhs(z, state):
        x = v1*z
        f, fx = harmonic_transfer(base["f0"], base["p0"], phi/v1, x)
        return early_rhs(f, fx, 0., phi*phase1*z, phi*phase1, v1, state)

    initial = (base["f0"]/base["p0"], 0., 0.)
    on = integrate_piece(on_rhs, initial, 1., cfg)
    log_ratio = math.log(v2/v1)

    def charging_rhs(z, state):
        x = v1*math.exp(z)
        f = base["C"]*x**s+base["D"]*x**(1-s)
        fx = s*base["C"]*x**(s-1)+(1-s)*base["D"]*x**(-s)
        field = phi*cmath.exp(-1j*lam*math.log(x))
        return early_rhs(f, fx, base["charge"](x), field, -1j*lam*field, x, state)

    charging = integrate_piece(charging_rhs, on.y[:, -1], log_ratio, cfg)

    def off_rhs(z, state):
        x = v2+(1-v2)*z
        f, fx = harmonic_transfer(fb, beta/(1-beta)*fyb, phi/(1-v2), x-1)
        return early_rhs(f, fx, qf, phi*phase2*(1-z), -phi*phase2, 1-v2, state)

    off = integrate_piece(off_rhs, charging.y[:, -1], 1., cfg)
    Hhat_end, jre, jim = off.y[:, -1]
    Jbase = complex(jre, jim)

    # Late scalar beta*W*g has zero longitudinal current. Integrate the
    # coefficient C such that J_late/beta=C*W, using integration by parts.
    def late_rhs(y, state):
        f, fy = backward.sol(y)
        H = state[0]
        Hy = (1-beta)*(1-qf*qf/(f*f))
        nu_y = -Hy/(4*R*f)+H*fy/(4*R*f*f)
        g, _ = late_bump(y)
        coefficient = (nu_y-1j*e*qf*(1-beta)/(4*f))*g
        return (Hy, coefficient.real, coefficient.imag)

    late = integrate_piece(late_rhs, (beta*Hhat_end, 0., 0.), 1., cfg)
    coefficient = complex(late.y[1, -1], late.y[2, -1])
    residual_moment = Jbase+coefficient*W
    residual = np.array([qf-1, residual_moment.real, residual_moment.imag])
    if not np.isfinite(residual).all():
        raise ValueError("nonfinite residual")
    if not diagnostics:
        return residual
    Hhat_samples = np.concatenate([p.sol(np.linspace(0, p.t[-1], 257))[0]
                                  for p in (on, charging, off)])
    H_late_samples = late.sol(np.linspace(0, 1, 513))[0]
    # Held-out quadratures, independent of the closed Gauss primitive and
    # the integration-by-parts form used by the late moment ODE.
    nodes, weights = np.polynomial.legendre.leggauss(64)
    nodes, weights = (nodes+1)/2, weights/2
    q_integral = 0.
    coefficient_direct = 0j
    for y, weight in zip(nodes, weights):
        x = v1*math.exp(log_ratio*y)
        f_charge = base["C"]*x**s+base["D"]*x**(1-s)
        q_integral += weight*log_ratio*e*R*phi*base["c"]*f_charge*f_charge
        f, _ = backward.sol(y)
        H = late.sol(y)[0]
        nu = -H/(4*R*f)
        g, gp = late_bump(y)
        coefficient_direct += weight*(-nu*gp-1j*e*qf*(1-beta)*g/(4*f))
    return {
        "configuration": asdict(cfg),
        "parameters": {"s": s, "W_real": wr, "W_imag": wi,
                       "physical_late_amplitude": beta*abs(W)},
        "scaled_residual": residual.tolist(),
        "unscaled_charge_error": R*residual[0],
        "unscaled_J_real": beta*residual[1],
        "unscaled_J_imag": beta*residual[2],
        "base_J_over_beta": [Jbase.real, Jbase.imag],
        "late_coefficient": [coefficient.real, coefficient.imag],
        "heldout_Gauss_integral_error": float(abs(q_integral-qf)),
        "heldout_late_wave_form_error": float(abs(coefficient_direct-coefficient)),
        "q_final": qf, "r_initial": R*base["f0"],
        "centre_normalized_affine_window_length_0_1":
            None if beta == 0 else R*base["p0"]/beta,
        "centre_normalized_affine_length_vertex_to_endpoint":
            None if beta == 0 else R*base["p0"]/beta+R*base["f0"],
        "min_sampled_H_over_beta_on_early_segment": float(np.min(Hhat_samples)),
        "min_sampled_H_on_late_segment": float(np.min(H_late_samples)),
        "min_sampled_H": float(min(beta*np.min(Hhat_samples), np.min(H_late_samples))),
        "min_sampled_late_radius": float(R*np.min(backward.sol(np.linspace(0, 1, 513))[0])),
        "evidence": "E0_C0_early_segment_float_shooting",
        "smooth_early_rounding_resolved": False,
        "rigorous_root_box": False, "goal_A_proved": False,
    }


def limit_start(cfg):
    phi = cfg.amplitude
    K = phi*math.cos(phi)**2*(1-phi*phi)/2
    s0 = 9*K*K/(1+9*K*K)
    diagnostic = evaluate((s0, 0., 0.), ShootingConfiguration(
        beta=0., rtol=cfg.rtol, atol=cfg.atol, max_step=cfg.max_step), True)
    J = complex(*diagnostic["base_J_over_beta"])
    coefficient = complex(*diagnostic["late_coefficient"])
    W0 = -J/coefficient
    return np.array([s0, W0.real, W0.imag])


def solve_first_jet(cfg, initial=None):
    start = limit_start(cfg) if initial is None else np.array(initial, dtype=float)
    result = root(lambda p: evaluate(p, cfg), start, method="hybr", options={"xtol": 2e-9})
    report = evaluate(result.x, cfg, True)
    report["root_solver"] = {"success": bool(result.success), "message": str(result.message),
                             "function_evaluations": int(result.nfev)}
    return result.x, report
