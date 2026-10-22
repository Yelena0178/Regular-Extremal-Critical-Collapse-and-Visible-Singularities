"""A-EVOL02: constrained areal-radius evolution with dynamic lapse/shift.

State rows are phi, P=b*Pi, face W=-n(r), log(alpha). W occupies the N
radial midpoints; its last array entry is unused. All other rows are nodal.
This module supplies exploratory numerics, not an analytic or interval certificate.
"""
from dataclasses import dataclass
import math
import numpy as np
from polar_evolution import (first_derivative, second_derivative, initial_fields,
                             geometry as polar_geometry)


class ShiftEvolutionStop(ValueError):
    def __init__(self, reason, context):
        super().__init__(reason)
        self.context = context


@dataclass(frozen=True)
class ShiftConfiguration:
    steps: int = 256
    outer_radius: float = 48.
    final_time: float = 4.
    cfl: float = 0.15
    amplitude: float = 0.1
    frequency: float = 0.2
    coupling: float = 0.6
    lapse_floor: float = 1e-6
    stop_at_trapped_candidate: bool = False
    slicing: str = "1+log"


def odd_derivative(values, h):
    out = first_derivative(values, h, regular_center=False)
    out[0] = values[1]/h
    return out


def nodal_w(r, faces):
    out = np.empty_like(r)
    out[1:-1] = (faces[:-2]+faces[1:-1])/2
    out[0] = 0 if r[0] == 0 else (3*faces[0]-faces[1])/2
    out[-1] = (3*faces[-2]-faces[-3])/2
    return out


def radial_divergence(r, face_values):
    """Exact radial volumes; adjoint of the nodal-to-face gradient at r=0."""
    rf = (r[:-1]+r[1:])/2
    flux = rf*rf*face_values[:-1]
    out = np.empty_like(r, dtype=face_values.dtype)
    if r[0] == 0:
        out[0] = flux[0]/(rf[0]**3/3)
    else:
        boundary = (3*face_values[0]-face_values[1])/2
        out[0] = (flux[0]-r[0]**2*boundary)/((rf[0]**3-r[0]**3)/3)
    out[1:-1] = (flux[1:]-flux[:-1])/((rf[1:]**3-rf[:-1]**3)/3)
    out[-1] = out[-2]  # the outer nodal RHS is held fixed
    return out


def shifted_geometry(r, state, coupling=0.6, inner_mass=0., inner_charge=0.):
    phi, canonical = state[:2]
    w = nodal_w(r, state[2].real)
    logalpha = state[3].real
    if np.max(np.abs(state[2:].imag)) > 1e-12:
        raise ValueError("nonreal geometry state")
    h = float(r[1]-r[0])
    regular = r[0] == 0
    gradient = first_derivative(phi, h, regular)
    pm = (canonical[:-1]+canonical[1:])/2
    xm = (gradient[:-1]+gradient[1:])/2
    fm = (phi[:-1]+phi[1:])/2
    wm = state[2, :-1].real
    source_mid = np.abs(pm)**2+np.abs(xm)**2
    cross_mid = np.real(pm*np.conjugate(xm))
    source = np.abs(canonical)**2+np.abs(gradient)**2
    cross = np.real(canonical*np.conjugate(gradient))
    radius_mid = (r[:-1]+r[1:])/2
    volume = (r[1:]**3-r[:-1]**3)/3
    q = np.empty_like(r)
    q[0] = inner_charge
    q[1:] = inner_charge+np.cumsum(coupling*volume*np.imag(fm*np.conjugate(pm)))
    qm = (q[:-1]+q[1:])/2
    electric = h*qm**2/(2*radius_mid**2)
    vacuum = (source[:-1] == 0) & (source[1:] == 0) & (r[:-1] > 0)
    vi = np.flatnonzero(vacuum)
    electric[vi] = q[vi]**2*(1/r[vi]-1/r[vi+1])/2
    aa = radius_mid+volume*source_mid/2
    bb = volume*wm*cross_mid
    cc_offset = electric-radius_mid*(1+wm*wm)
    m = np.empty_like(r)
    m[0] = inner_mass
    for i in range(len(r)-1):
        cc = 2*m[i]+cc_offset[i]
        discriminant = bb[i]*bb[i]-4*aa[i]*cc
        if discriminant <= 0:
            raise ShiftEvolutionStop("radial quadratic unresolved; outcome UNKNOWN", {
                "radial_midpoint": float(radius_mid[i]), "cell": i,
                "discriminant": float(discriminant), "previous_mass": float(m[i]),
                "midpoint_W": float(wm[i]),
            })
        zmid = (-bb[i]+math.sqrt(discriminant))/(2*aa[i])
        if zmid <= 0:
            raise ValueError("nonpositive spatial metric root")
        m[i+1] = m[i]+volume[i]*(
            source_mid[i]*zmid*zmid/2+wm[i]*zmid*cross_mid[i])+electric[i]
    safe = np.where(r == 0, 1, r)
    hawking_delta = 1-2*m/safe
    spatial_delta = hawking_delta+w*w
    if np.min(spatial_delta) <= 0:
        raise ValueError("spatial metric lost positivity; outcome UNKNOWN")
    z = np.sqrt(spatial_delta)
    alpha = np.exp(logalpha)
    if not np.all(np.isfinite(alpha)) or np.min(alpha) <= 0:
        raise ValueError("invalid lapse")
    beta = alpha*w
    c = alpha*z
    integrand = alpha*q/(z*safe**2)
    segments = h*(integrand[:-1]+integrand[1:])/2
    potential = np.empty_like(r)
    potential[-1] = q[-1]/r[-1]
    potential[:-1] = potential[-1]+np.cumsum(segments[::-1])[::-1]
    return dict(mass=m, charge=q, z=z, alpha=alpha, beta=beta, speed=c,
                potential=potential, gradient=gradient, source=source, cross=cross,
                hawking_delta=hawking_delta, spatial_delta=spatial_delta, w=w)


def shifted_rhs(r, state, coupling=0.6, frozen_lapse=False, slicing="1+log"):
    g = shifted_geometry(r, state, coupling)
    return shifted_rhs_with_geometry(r, state, g, coupling, frozen_lapse, slicing), g


def shifted_rhs_with_geometry(r, state, g, coupling=0.6, frozen_lapse=False, slicing="1+log"):
    h = float(r[1]-r[0])
    regular = r[0] == 0
    phi, canonical = state[:2]
    faces, logalpha = state[2].real, state[3].real
    w = g["w"]
    alpha, z, beta, c = g["alpha"], g["z"], g["beta"], g["speed"]
    x = g["gradient"]
    dl = first_derivative(logalpha, h, regular)
    dc = first_derivative(c, h, regular)
    ddphi = second_derivative(phi, h)
    safe = np.where(r == 0, 1, r)
    rf = (r[:-1]+r[1:])/2
    af = (alpha[:-1]+alpha[1:])/2
    pf = (canonical[:-1]+canonical[1:])/2
    xf = (x[:-1]+x[1:])/2
    m3 = g["mass"]/safe**3
    q3 = g["charge"]/safe**3
    if regular:
        m3[0] = abs(canonical[0])**2/6
        q3[0] = coupling*(phi[0]*canonical[0].conjugate()).imag/3
    m3f, q3f = (m3[:-1]+m3[1:])/2, (q3[:-1]+q3[1:])/2
    spatial_f = 1-2*rf*rf*m3f+faces[:-1]**2
    if np.min(spatial_f) <= 0:
        raise ValueError("nonpositive face spatial metric")
    betaf = af*faces[:-1]
    source_f = np.abs(pf)**2+np.abs(xf)**2
    face_derivative = np.empty_like(faces[:-1])
    face_derivative[1:-1] = (faces[2:-1]-faces[:-3])/(2*h)
    face_derivative[0] = ((faces[1]+faces[0])/(2*h) if regular
                           else (-3*faces[0]+4*faces[1]-faces[2])/(2*h))
    face_derivative[-1] = (3*faces[-2]-4*faces[-3]+faces[-4])/(2*h)
    w_t = np.zeros_like(r)
    w_t[:-1] = (betaf*face_derivative-spatial_f*(alpha[1:]-alpha[:-1])/h
        +af*(rf*m3f+rf*spatial_f*source_f/2-rf**3*q3f*q3f/2))
    advective_flux = np.zeros_like(canonical)
    advective_flux[:-1] = betaf*pf
    div_advection = radial_divergence(r, advective_flux)
    phi_t = beta*x+c*canonical-1j*coupling*g["potential"]*phi
    p_t = c*ddphi+(2*c/safe+dc)*x+div_advection-1j*coupling*g["potential"]*canonical
    trace_k = radial_divergence(r, faces)-r*z*g["cross"]
    if slicing not in ("1+log", "harmonic"):
        raise ValueError("unknown slicing")
    gauge_coefficient = 2 if slicing == "1+log" else alpha
    log_t = beta*dl-gauge_coefficient*trace_k
    if frozen_lapse:
        log_t[:] = 0.
    if regular:
        p_t[0] = (3*c[0]*ddphi[0]+div_advection[0]
                  -1j*coupling*g["potential"][0]*canonical[0])
    result = np.stack((phi_t, p_t, w_t.astype(complex), log_t.astype(complex)))
    result[:, -1] = 0
    return result


def shifted_propagation_residuals(r, state, coupling=0.6, slicing="1+log"):
    flow, g = shifted_rhs(r, state, coupling, slicing=slicing)
    eps = 1e-5
    plus = shifted_geometry(r, state+eps*flow, coupling)
    minus = shifted_geometry(r, state-eps*flow, coupling)
    mt = (plus["mass"]-minus["mass"])/(2*eps)
    qt = (plus["charge"]-minus["charge"])/(2*eps)
    expected_mt = r*r*g["alpha"]*g["z"]*(
        g["w"]*g["z"]*g["source"]
        +(g["z"]**2+g["w"]**2)*g["cross"])
    expected_qt = coupling*r*r*np.imag(state[0]*np.conjugate(
        g["speed"]*g["gradient"]+g["beta"]*state[1]))
    h = float(r[1]-r[0])
    b = 1/g["z"]
    bt_over_b = ((1/plus["z"]-1/minus["z"])/(2*eps))/b
    safe = np.where(r == 0, 1, r)
    w_over_r = g["w"]/safe
    w_over_r[0] = state[2, 0].real/((r[0]+r[1])/2)
    kr = radial_divergence(r, state[2].real)-2*w_over_r-r*g["z"]*g["cross"]
    expected_bt = (-g["alpha"]*kr+g["beta"]*first_derivative(b, h)/b
                   +first_derivative(g["beta"], h, False))
    expected_bt[0] = 0
    return {
        "mass_time_propagation": float(np.max(abs(mt-expected_mt))),
        "charge_time_propagation": float(np.max(abs(qt-expected_qt))),
        "spatial_metric_time_propagation": float(np.max(abs(bt_over_b-expected_bt))),
    }


def evolve_shifted(cfg):
    if cfg.coupling != 0.6 or cfg.steps < 32 or cfg.outer_radius <= 21:
        raise ValueError("invalid fixed-model grid")
    if not 0 < cfg.cfl <= 0.25 or cfg.final_time < 0:
        raise ValueError("invalid time domain or CFL")
    if cfg.slicing not in ("1+log", "harmonic"):
        raise ValueError("unknown slicing")
    r = np.linspace(0., cfg.outer_radius, cfg.steps+1)
    fields = initial_fields(r, cfg.amplitude, cfg.frequency)
    initial_g = polar_geometry(r, fields)
    state = np.vstack((fields, np.zeros_like(r), np.log(initial_g["alpha"]))).astype(complex)
    t, tau, iterations = 0., 0., 0
    axis = [(t, tau, float(abs(state[0, 0])))]
    minimum_hawking_delta = 1.
    minimum_spatial_delta = 1.
    maximum_speed = 0.
    initial_mass = None
    initial_charge = None
    minimum_lapse = 1.
    h = cfg.outer_radius/cfg.steps
    last_geometry = {}
    first_trapped = None
    def stage_rhs(values, stage_time):
        try:
            return shifted_rhs(r, values, slicing=cfg.slicing)
        except ValueError as exc:
            context = dict(getattr(exc, "context", {}))
            context.update(last_completed_time=float(t), failed_stage_time=float(stage_time),
                           completed_iterations=iterations, last_geometry=last_geometry,
                           first_numeric_trapped_observation=first_trapped)
            raise ShiftEvolutionStop(str(exc), context) from exc
    while t < cfg.final_time-1e-13:
        k1, g1 = stage_rhs(state, t)
        last_geometry = {
            "minimum_hawking_delta": float(np.min(g1["hawking_delta"])),
            "minimum_spatial_delta": float(np.min(g1["spatial_delta"])),
            "minimum_lapse": float(np.min(g1["alpha"])),
            "maximum_absolute_face_W": float(np.max(abs(state[2].real))),
        }
        safe = np.where(r == 0, 1, r)
        theta_plus = 2*(g1["z"]-g1["w"])/safe
        theta_minus = -2*(g1["z"]+g1["w"])/safe
        indices = np.flatnonzero((r > 0) & (theta_plus < -.01) & (theta_minus < -.01))
        if first_trapped is None and len(indices):
            index = int(indices[np.argmin(theta_plus[indices])])
            first_trapped = {
                "coordinate_time": float(t), "radius": float(r[index]),
                "theta_plus": float(theta_plus[index]), "theta_minus": float(theta_minus[index]),
                "Hawking_mass": float(g1["mass"][index]),
                "charge": float(g1["charge"][index]), "W": float(g1["w"][index]),
                "z": float(g1["z"][index]), "lapse": float(g1["alpha"][index]),
                "actual_strict_trapped_sphere_certified": False,
            }
        if first_trapped is not None and cfg.stop_at_trapped_candidate:
            break
        if initial_mass is None:
            initial_mass = float(g1["mass"][-1]+g1["charge"][-1]**2/(2*r[-1]))
            initial_charge = float(g1["charge"][-1])
        gauge_speed = (g1["z"]*np.sqrt(2*g1["alpha"]) if cfg.slicing == "1+log"
                       else g1["speed"])
        speed = max(float(np.max(abs(g1["beta"])+g1["speed"])),
                    float(np.max(abs(g1["beta"])+gauge_speed)))
        dt = min(cfg.final_time-t, cfg.cfl*h/speed)
        k2, g2 = stage_rhs(state+dt*k1/2, t+dt/2)
        k3, g3 = stage_rhs(state+dt*k2/2, t+dt/2)
        k4, g4 = stage_rhs(state+dt*k3, t+dt)
        for g in (g1, g2, g3, g4):
            minimum_hawking_delta = min(minimum_hawking_delta, float(np.min(g["hawking_delta"])))
            minimum_spatial_delta = min(minimum_spatial_delta, float(np.min(g["spatial_delta"])))
            minimum_lapse = min(minimum_lapse, float(np.min(g["alpha"])))
            gauge_speed = (g["z"]*np.sqrt(2*g["alpha"]) if cfg.slicing == "1+log"
                           else g["speed"])
            maximum_speed = max(maximum_speed,
                float(np.max(abs(g["beta"])+gauge_speed)),
                float(np.max(abs(g["beta"])+g["speed"])))
            if np.min(g["alpha"]) < cfg.lapse_floor:
                raise ValueError("lapse floor reached; outcome UNKNOWN")
        state += dt*(k1+2*k2+2*k3+k4)/6
        tau += dt*(g1["alpha"][0]+2*g2["alpha"][0]+2*g3["alpha"][0]+g4["alpha"][0])/6
        t += dt
        iterations += 1
        if not np.all(np.isfinite(state)):
            raise ValueError("nonfinite state")
        axis.append((t, tau, float(abs(state[0, 0]))))
    final = shifted_geometry(r, state)
    report = {
        "completed_time": t, "center_proper_time": float(tau), "iterations": iterations,
        "minimum_sampled_hawking_delta": minimum_hawking_delta,
        "minimum_sampled_spatial_delta": minimum_spatial_delta,
        "maximum_observed_characteristic_speed": maximum_speed,
        "initial_ADM_mass_estimate": initial_mass,
        "mass_boundary_drift": float(final["mass"][-1]+final["charge"][-1]**2/(2*r[-1])-initial_mass),
        "charge_boundary_drift": float(final["charge"][-1]-initial_charge),
        "minimum_sampled_lapse": minimum_lapse,
        "classification": "UNKNOWN_finite_time_only",
        "rigorous_PDE_error_bound": False,
        "first_numeric_trapped_observation": first_trapped,
        "stopped_at_trapped_candidate": bool(first_trapped and cfg.stop_at_trapped_candidate),
    }
    return r, state, report, np.asarray(axis)
