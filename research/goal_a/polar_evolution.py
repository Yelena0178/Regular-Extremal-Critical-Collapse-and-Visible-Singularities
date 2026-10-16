"""Finite-time exploratory EMCSF evolution; see POLAR_EVOLUTION.md.

NumPy is required. No interval error control, horizon penetration, Bondi
extraction, or global-future classification is implemented.
"""
from dataclasses import dataclass
import math
import numpy as np
from incoming_family import Parameters, bump


class EvolutionStop(ValueError):
    """A computational/gauge stop, with no spacetime outcome implication."""
    def __init__(self, message, time, dt, minimum_delta, iterations):
        super().__init__(message)
        self.context = {
            "last_completed_time": time, "attempted_dt": dt,
            "minimum_sampled_stage_delta": minimum_delta,
            "completed_iterations": iterations,
            "classification": "UNKNOWN_coordinate_stop",
        }


@dataclass(frozen=True)
class Configuration:
    steps: int = 256
    outer_radius: float = 48.0
    final_time: float = 8.0
    cfl: float = 0.2
    amplitude: float = 0.1
    frequency: float = 0.2
    coupling: float = 0.6
    flat_background: bool = False
    minimum_delta: float = 0.05

    def validate(self):
        if self.steps < 32 or self.outer_radius <= 21:
            raise ValueError("insufficient grid or exterior buffer")
        if not 0 < self.cfl <= 0.3 or self.final_time < 0:
            raise ValueError("invalid time step or final time")
        if self.coupling != 0.6:
            raise ValueError("fixed e=3/5 required")
        if not all(math.isfinite(v) for v in (
                self.outer_radius, self.final_time, self.cfl,
                self.amplitude, self.frequency, self.minimum_delta)):
            raise ValueError("nonfinite configuration")


def first_derivative(values, h, regular_center=True):
    result = np.empty_like(values)
    result[1:-1] = (values[2:]-values[:-2])/(2*h)
    result[0] = 0 if regular_center else (-3*values[0]+4*values[1]-values[2])/(2*h)
    result[-1] = (3*values[-1]-4*values[-2]+values[-3])/(2*h)
    return result


def second_derivative(values, h):
    result = np.empty_like(values)
    result[1:-1] = (values[2:]-2*values[1:-1]+values[:-2])/h**2
    result[0] = 2*(values[1]-values[0])/h**2
    result[-1] = 0
    return result


def initial_fields(r, amplitude, frequency):
    p = Parameters(amplitude=amplitude, frequency=frequency)
    profile = np.array([bump(float(s), p) for s in r])
    phase = np.exp(-1j*frequency*r)
    safe = np.where(r == 0, 1, r)
    phi = amplitude*profile[:, 0]*phase/safe
    canonical = amplitude*(profile[:, 1]-1j*frequency*profile[:, 0])*phase/safe
    return np.stack((phi, canonical))


def geometry(r, fields, coupling=0.6, flat=False, inner_mass=0., inner_charge=0.):
    """Radial constraints with fields (phi,P) and a regular center or RN annulus."""
    phi, canonical = fields
    h = float(r[1]-r[0])
    regular = r[0] == 0
    gradient = first_derivative(phi, h, regular)
    if flat:
        zero = np.zeros_like(r)
        one = np.ones_like(r)
        return dict(mass=zero, charge=zero, alpha=one, metric_b=one,
                    delta=one, potential=zero, speed=one, gradient=gradient)
    if regular and (inner_mass != 0 or inner_charge != 0):
        raise ValueError("regular center cannot carry point mass/charge")
    source = np.abs(canonical)**2+np.abs(gradient)**2
    phi_mid = (phi[:-1]+phi[1:])/2
    p_mid = (canonical[:-1]+canonical[1:])/2
    x_mid = (gradient[:-1]+gradient[1:])/2
    source_mid = np.abs(p_mid)**2+np.abs(x_mid)**2
    mid_r = (r[:-1]+r[1:])/2
    radial_volume = (r[1:]**3-r[:-1]**3)/3
    q = np.empty_like(r)
    q[0] = inner_charge
    q[1:] = inner_charge+np.cumsum(coupling*radial_volume*np.imag(
        phi_mid*np.conjugate(p_mid)))
    mid_q = (q[:-1]+q[1:])/2
    # m' + r*S*m = r^2*S/2 + Q^2/(2r^2) is linear. Implicit
    # midpoint gives m[i+1]=u[i]*m[i]+v[i], evaluated by prefix products.
    coefficient = mid_r*source_mid
    denominator = 1+h*coefficient/2
    ratio = (1-h*coefficient/2)/denominator
    # Integrate the known r^2 weight exactly. Unweighted midpoint gives a
    # persistent 25% error in Q/r^3 and m/r^3 at the first center cell.
    offset = (radial_volume*source_mid/2+h*mid_q**2/(2*mid_r**2))/denominator
    vacuum = ((source[:-1] == 0) & (source[1:] == 0) & (r[:-1] > 0))
    indices = np.flatnonzero(vacuum)
    offset[indices] = q[indices]**2*(1/r[indices]-1/r[indices+1])/2
    if np.min(ratio) <= 0:
        raise ValueError("radial recurrence unresolved; physical outcome UNKNOWN")
    product = np.cumprod(ratio)
    if np.min(product) < 1e-200:
        raise ValueError("radial prefix-product range exceeded")
    m = np.empty_like(r)
    m[0] = inner_mass
    m[1:] = product*(inner_mass+np.cumsum(offset/product))
    safe = np.where(r == 0, 1, r)
    delta = 1-2*m/safe
    if np.min(delta) <= 0:
        raise ValueError("nonpositive Delta after radial integration")
    metric = 1/np.sqrt(delta)
    lapse_gradient = (1/delta-1)/(2*safe)+r*source/2-q*q/(2*delta*safe**3)
    if regular:
        lapse_gradient[0] = 0
    log_segments = h*(lapse_gradient[:-1]+lapse_gradient[1:])/2
    log_segments[indices] = np.log(delta[indices+1]/delta[indices])/2
    logalpha = np.concatenate(([0.], np.cumsum(log_segments)))
    alpha = np.exp(logalpha-logalpha[-1])*math.sqrt(float(delta[-1]))
    integrand = alpha*metric*q/safe**2
    segments = h*(integrand[:-1]+integrand[1:])/2
    # Exact RN primitive on every noncentral matter-free segment.
    segments[indices] = (alpha[indices]*metric[indices]*q[indices]
                         *(1/r[indices]-1/r[indices+1]))
    potential = np.empty_like(r)
    potential[-1] = q[-1]/r[-1]
    potential[:-1] = potential[-1]+np.cumsum(segments[::-1])[::-1]
    if not all(np.all(np.isfinite(x)) for x in (m, q, alpha, potential)) or np.min(alpha) <= 0:
        raise ValueError("nonfinite constraint solution")
    return dict(mass=m, charge=q, alpha=alpha, metric_b=metric, delta=delta,
                potential=potential, speed=alpha/metric, gradient=gradient)


def evolution_rhs(r, fields, coupling=0.6, flat=False, reverse_potential=False):
    g = geometry(r, fields, coupling, flat)
    phi, canonical = fields
    h = float(r[1]-r[0])
    c = g["speed"]
    dc = first_derivative(c, h)
    dphi = g["gradient"]
    ddphi = second_derivative(phi, h)
    potential = -g["potential"] if reverse_potential else g["potential"]
    phi_t = c*canonical-1j*coupling*potential*phi
    safe = np.where(r == 0, 1, r)
    p_t = c*ddphi+(2*c/safe+dc)*dphi-1j*coupling*potential*canonical
    p_t[0] = 3*c[0]*ddphi[0]-1j*coupling*potential[0]*canonical[0]
    phi_t[-1] = p_t[-1] = 0
    return np.stack((phi_t, p_t)), g


def propagation_residuals(r, fields, coupling=0.6, reverse_potential=False):
    """Differentiate the radial solution along the computed scalar flow.

    E4 is not solved by the constrained scheme, so its residual is an independent
    compatibility diagnostic. This directional difference is not a rigorous bound.
    """
    flow, g = evolution_rhs(r, fields, coupling, reverse_potential=reverse_potential)
    eps = 1e-5
    plus = geometry(r, fields+eps*flow, coupling)
    minus = geometry(r, fields-eps*flow, coupling)
    mt = (plus["mass"]-minus["mass"])/(2*eps)
    qt = (plus["charge"]-minus["charge"])/(2*eps)
    phi, canonical = fields
    x = g["gradient"]
    expected_qt = coupling*g["speed"]*r*r*np.imag(phi*np.conjugate(x))
    expected_mt = r*r*g["alpha"]/g["metric_b"]**3*np.real(
        canonical*np.conjugate(x))
    potential = -g["potential"] if reverse_potential else g["potential"]
    dp = first_derivative(potential, float(r[1]-r[0]))
    safe = np.where(r == 0, 1, r)
    expected_dp = -g["alpha"]*g["metric_b"]*g["charge"]/safe**2
    return {
        "mass_propagation_max": float(np.max(np.abs(mt-expected_mt))),
        "charge_propagation_max": float(np.max(np.abs(qt-expected_qt))),
        "potential_gradient_max_interior": float(np.max(np.abs(dp[1:-1]-expected_dp[1:-1]))),
    }


def evolve(config):
    config.validate()
    r = np.linspace(0., config.outer_radius, config.steps+1)
    h = config.outer_radius/config.steps
    fields = initial_fields(r, config.amplitude, config.frequency)
    initial_g = geometry(r, fields, config.coupling, config.flat_background)
    g = initial_g
    t, iterations = 0., 0
    maximum_speed = float(np.max(g["speed"]))
    minimum_delta = float(np.min(g["delta"]))
    while t < config.final_time-1e-13:
        dt = min(config.final_time-t, config.cfl*h/float(np.max(g["speed"])))
        k1, g1 = evolution_rhs(r, fields, config.coupling, config.flat_background)
        k2, g2 = evolution_rhs(r, fields+dt*k1/2, config.coupling, config.flat_background)
        k3, g3 = evolution_rhs(r, fields+dt*k2/2, config.coupling, config.flat_background)
        k4, g4 = evolution_rhs(r, fields+dt*k3, config.coupling, config.flat_background)
        stage_speed = max(float(np.max(s["speed"])) for s in (g1, g2, g3, g4))
        maximum_speed = max(maximum_speed, stage_speed)
        minimum_delta = min(minimum_delta,
                            *(float(np.min(s["delta"])) for s in (g1, g2, g3, g4)))
        if dt*stage_speed/h > 0.4:
            raise ValueError("stage CFL diagnostic exceeded")
        if minimum_delta < config.minimum_delta:
            raise EvolutionStop("polar coordinate stop; physical outcome UNKNOWN",
                                t, dt, minimum_delta, iterations)
        fields = fields+dt*(k1+2*k2+2*k3+k4)/6
        if not np.all(np.isfinite(fields)):
            raise ValueError("nonfinite evolving scalar")
        t += dt
        iterations += 1
        g = g4
    final_g = geometry(r, fields, config.coupling, config.flat_background)
    initial_mass = float(initial_g["mass"][-1]+initial_g["charge"][-1]**2/(2*r[-1]))
    final_mass = float(final_g["mass"][-1]+final_g["charge"][-1]**2/(2*r[-1]))
    report = {
        "time": t, "iterations": iterations, "minimum_sampled_delta": minimum_delta,
        "maximum_observed_coordinate_speed": maximum_speed,
        "initial_ADM_mass_estimate": initial_mass,
        "mass_boundary_drift": final_mass-initial_mass,
        "charge_boundary_drift": float(final_g["charge"][-1]-initial_g["charge"][-1]),
        "outer_buffer_scalar_max": float(np.max(np.abs(fields[:, r > r[-1]-4]))),
        "estimated_travel_distance": t*maximum_speed,
        "initial_boundary_gap": config.outer_radius-21.,
        "finite_boundary_independence_proved": False,
        "classification": "UNKNOWN_finite_time_only",
    }
    return r, fields, report
