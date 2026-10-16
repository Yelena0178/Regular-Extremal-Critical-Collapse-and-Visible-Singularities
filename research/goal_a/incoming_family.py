"""Exploratory Cauchy constraint solver for A-INC01; no spacetime evolution.

Only the Python standard library is required. Floating-point output carries no
rigorous interval, all-radius positivity, or global-future certification.
"""
from dataclasses import dataclass
import cmath
import math


@dataclass(frozen=True)
class Parameters:
    amplitude: float = 0.5
    frequency: float = 0.2
    coupling: float = 0.6
    inner: float = 1.0
    outer: float = 21.0

    def validate(self):
        values = (self.amplitude, self.frequency, self.coupling,
                  self.inner, self.outer)
        if not all(math.isfinite(x) for x in values):
            raise ValueError("non-finite parameter")
        if self.coupling != 0.6:
            raise ValueError("this experiment fixes e=3/5")
        if not 0 < self.inner < self.outer:
            raise ValueError("require 0 < inner < outer")


def bump(r, p):
    """C-infinity closed-shell bump psi and its analytic radial derivative."""
    width = p.outer - p.inner
    x = (r - p.inner) / width
    if not 0 < x < 1:
        return 0.0, 0.0
    z = x * (1 - x)
    psi = math.exp(4 - 1 / z)
    # Underflow to zero in an endpoint layer is numerical, not a finite cutoff.
    derivative = psi * (1 - 2*x) / (width*z*z)
    return psi, derivative


def rhs(r, state, p):
    m, q = state
    delta = 1 - 2*m/r
    if delta <= 0 or not math.isfinite(delta):
        raise ValueError("Delta <= 0 at RK stage; reject areal-coordinate data")
    psi, dpsi = bump(r, p)
    a2 = p.amplitude**2
    source = dpsi*dpsi + (dpsi-psi/r)**2 + 2*(p.frequency*psi)**2
    return (q*q/(2*r*r) + a2*delta*source/2,
            p.coupling*p.frequency*a2*psi*psi)


def exterior_minimum(mass, charge, outer):
    if mass <= 0:
        return 1.0  # infimum at spatial infinity
    if charge == 0:
        return 1 - 2*mass/outer + charge*charge/outer**2
    critical = charge*charge/mass
    radius = max(outer, critical)
    return 1 - 2*mass/radius + charge*charge/radius**2


def integrate(p, steps):
    p.validate()
    if not isinstance(steps, int) or steps < 16:
        raise ValueError("steps must be an integer >= 16")
    h = (p.outer - p.inner)/steps
    state = (0.0, 0.0)
    rows = [(p.inner, *state)]
    for i in range(steps):
        r = p.inner+i*h
        k1 = rhs(r, state, p)
        s2 = tuple(v+h*k/2 for v, k in zip(state, k1))
        k2 = rhs(r+h/2, s2, p)
        s3 = tuple(v+h*k/2 for v, k in zip(state, k2))
        k3 = rhs(r+h/2, s3, p)
        s4 = tuple(v+h*k for v, k in zip(state, k3))
        k4 = rhs(r+h, s4, p)
        state = tuple(v+h*(b+2*c+2*d+e)/6
                      for v, b, c, d, e in zip(state, k1, k2, k3, k4))
        if not all(math.isfinite(v) for v in state):
            raise ValueError("non-finite state")
        if 1-2*state[0]/(r+h) <= 0:
            raise ValueError("Delta <= 0 at endpoint")
        rows.append((p.inner+(i+1)*h, *state))
    mass = state[0]+state[1]**2/(2*p.outer)
    if exterior_minimum(mass, state[1], p.outer) <= 0:
        raise ValueError("non-positive analytic exterior minimum")
    return rows


def fields(row, p):
    r, m, q = row
    psi, dpsi = bump(r, p)
    delta = 1-2*m/r
    root = math.sqrt(delta)
    phase = cmath.exp(-1j*p.frequency*r)
    phi = p.amplitude*psi*phase/r
    pi = p.amplitude*root*(dpsi-1j*p.frequency*psi)*phase/r
    dr_phi = p.amplitude*(dpsi-psi/r-1j*p.frequency*psi)*phase/r
    jr = -(pi*dr_phi.conjugate()).real
    kr = -p.amplitude**2*root*(
        dpsi*(dpsi-psi/r)+(p.frequency*psi)**2)/r
    return {"metric_a": 1/root, "phi": phi, "pi": pi, "dr_phi": dr_phi,
            "electric_r": q*root/r**2, "kr": kr, "jr": jr,
            "rho": (q*q/r**4+abs(pi)**2+delta*abs(dr_phi)**2)/2,
            "delta": delta}


def derivative(values, i, h):
    return (values[i-2]-8*values[i-1]+8*values[i+1]-values[i+2])/(12*h)


def residuals(rows, p, mutation=None):
    """Independent reconstruction in the original 3+1 constraint equations.

    The Hamiltonian check differentiates the metric, not the ODE m variable.
    Gauss differentiates the reconstructed electric flux; source is calculated
    from the complex field product. Mutations check sign/omitted-K sensitivity.
    """
    f = [fields(row, p) for row in rows]
    h = rows[1][0]-rows[0][0]
    metric = [x["metric_a"] for x in f]
    flux = [row[0]**2*x["metric_a"]*x["electric_r"]
            for row, x in zip(rows, f)]
    rphi = [row[0]*x["phi"] for row, x in zip(rows, f)]
    maxima = dict(hamiltonian=0.0, gauss=0.0, momentum=0.0, incoming=0.0)
    for i in range(2, len(rows)-2):
        r = rows[i][0]
        x = f[i]
        aa = x["metric_a"]
        curvature = 2*(1-aa**-2)/r**2+4*derivative(metric, i, h)/(r*aa**3)
        source = p.coupling*(x["phi"]*x["pi"].conjugate()).imag
        if mutation == "reverse_gauss":
            source = -source
        kr = 0.0 if mutation == "omit_extrinsic_curvature" else x["kr"]
        vals = {
            "hamiltonian": curvature-4*x["rho"],
            "gauss": derivative(flux, i, h)/(aa*r*r)-source,
            "momentum": 2*kr/r-2*x["jr"],
            "incoming": r*x["pi"]-derivative(rphi, i, h)/aa,
        }
        for name, value in vals.items():
            maxima[name] = max(maxima[name], abs(value))
    return maxima


def simpson(values, h):
    if (len(values)-1) % 2:
        raise ValueError("Simpson requires an even number of panels")
    return h*(values[0]+values[-1]+4*sum(values[1:-1:2])
              +2*sum(values[2:-1:2]))/3


def profile_integrals(p, steps=8192):
    if steps < 16 or steps % 2:
        raise ValueError("even quadrature steps >=16 required")
    h = (p.outer-p.inner)/steps
    values = [bump(p.inner+i*h, p) for i in range(steps+1)]
    aa = simpson([d*d for _, d in values], h)
    bb = simpson([v*v for v, _ in values], h)
    return aa, bb


def summary(rows, p):
    radius, m, q = rows[-1]
    mass = m+q*q/(2*radius)
    return {
        "ADM_mass_estimate": mass, "ADM_charge_estimate": q,
        "absolute_ADM_ratio_estimate": abs(q)/mass if mass else None,
        "minimum_sampled_delta": min(1-2*m/r for r, m, _ in rows),
        "analytic_exterior_minimum_evaluated_in_float":
            exterior_minimum(mass, q, radius),
        "exact_family_all_radius_positivity": {
            "analytic_proof_applies":
                p.inner == 1 and p.outer == 21 and p.coupling == 0.6
                and abs(p.amplitude) <= 2 and abs(p.frequency) <= 0.25,
            "lower_bound_if_applicable": "32/851",
            "proof": "EXACT_INITIAL_BUDGET.md section 4",
        },
        "floating_ODE_approximation_error_certified": False,
        "outcome": "UNKNOWN_no_spacetime_evolution",
    }
