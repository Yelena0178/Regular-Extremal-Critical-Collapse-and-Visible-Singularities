"""Exploratory neutral double-null evolution including a regular axis.

This is a finite-grid diamond method, not a PDE error certificate. r^2 is
evolved using (r^2)_uv=-Omega^2/2; psi=r*phi avoids division in the wave
operator. An optional shrinking Taylor band treats the axis; an exact vacuum
cap mode avoids that closure altogether on pre-arrival causal rectangles.
"""

from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True)
class CharacteristicConfiguration:
    steps: int = 192
    outer_v: float = 4.8
    final_u: float = 2.4
    centre_cells: int | None = None
    iterations: int = 8
    iteration_tolerance: float = 3e-12
    iteration_failure_tolerance: float = 1e-8
    max_abs_log_omega2: float = 30.
    freeze_geometry: bool = False
    arithmetic_omega2_average: bool = True
    exact_flat_cap_v: float | None = None


def flat_wave(v):
    if not 2. < v < 4.:
        return 0.
    x = (v-2.)/2.
    return math.exp(4-1/(x*(1-x)))


def flat_wave_derivative(v):
    if not 2. < v < 4.:
        return 0.
    x = (v-2.)/2.
    return flat_wave(v)*(1-2*x)/(2*x*x*(1-x)*(1-x))


def flat_initial(v):
    return v/2., 0., 0. if v == 0 else 2*flat_wave(v)/v


def flrw_exact(u, v, collapse_time=4.):
    t, x = (u+v)/2., (v-u)/2.
    s = 1-t/collapse_time
    if s <= 0:
        raise ValueError("FLRW comparison passed its singular time")
    a = math.sqrt(s)
    phi = math.sqrt(3)/2*math.log(s)
    adot = -1/(2*collapse_time*a)
    return {"r": a*x, "S": math.log(s), "phi": phi,
            "nu": (-a+adot*x)/2, "lambda": (a+adot*x)/2}


def flrw_initial(v):
    data = flrw_exact(0., v)
    return data["r"], data["S"], data["phi"]


def evolve(initial, cfg):
    if cfg.steps < 16 or not 0 < cfg.final_u < cfg.outer_v:
        raise ValueError("invalid finite characteristic grid")
    n = cfg.steps
    h = cfg.outer_v/n
    centre_cells = (int(math.ceil(math.sqrt(n))) if cfg.centre_cells is None
                    else cfg.centre_cells)
    rows = min(int(round(cfg.final_u/h)), n-3)+1
    u, v = np.arange(rows)*h, np.arange(n+1)*h
    r = np.full((rows, n+1), np.nan)
    S = np.full_like(r, np.nan)
    psi = np.full_like(r, np.nan)
    phi = np.full_like(r, np.nan)
    for j, advanced in enumerate(v):
        rr, ss, pp = initial(float(advanced))
        r[0, j], S[0, j], phi[0, j], psi[0, j] = rr, ss, pp, rr*pp
    if cfg.exact_flat_cap_v is not None:
        if not cfg.final_u < cfg.exact_flat_cap_v < cfg.outer_v:
            raise ValueError("exact vacuum-cap mode requires U < v_cap < v_max")
        indices = np.where(v <= cfg.exact_flat_cap_v)[0]
        if (np.max(abs(r[0, indices]-v[indices]/2)) > 1e-11
                or np.max(abs(S[0, indices])) > 1e-11
                or np.max(abs(phi[0, indices])) > 1e-11):
            raise ValueError("input does not have the requested exact Minkowski cap")
    if abs(r[0, 0]) > 1e-12:
        raise ValueError("initial cone must have a regular vertex at v=0")
    maximum_iteration_change = 0.
    last_row, stop = rows-1, None
    axis_closure_uses = 0
    for i in range(1, rows):
        # Same central time t=i*h, radial offsets h and 2h. These samples
        # already exist on the preceding u rows.
        r1 = r[i-1, i+1]
        if cfg.exact_flat_cap_v is not None:
            # Causal vacuum region is known exactly; do not extrapolate
            # an axis value from points outside that region.
            a_axis, phi_axis = 1., 0.
        elif i >= 2:
            r2 = r[i-2, i+2]
            a_axis = (8*r1-r2)/(6*h)
            phi_axis = (4*phi[i-1, i+1]-phi[i-2, i+2])/3
        else:
            # Only a startup approximation; manufactured convergence checks
            # cover this row as well. The collapse input has a flat cap.
            a_axis = r1/h
            phi_axis = phi[i-1, i+1]
        if a_axis <= 0 or not math.isfinite(a_axis):
            last_row, stop = i-1, "nonpositive axis elementary-flatness estimate"
            break
        r[i, i], psi[i, i], phi[i, i] = 0., 0., phi_axis
        S[i, i] = 0. if cfg.freeze_geometry else 2*math.log(a_axis)
        for j in range(i, n):
            if cfg.exact_flat_cap_v is not None and v[j+1] <= cfg.exact_flat_cap_v:
                r[i, j+1], S[i, j+1] = (v[j+1]-u[i])/2, 0.
                psi[i, j+1], phi[i, j+1] = 0., 0.
                continue
            # S=(i-1,j), E=(i-1,j+1), W=(i,j), N=(i,j+1).
            rs, re, rw = r[i-1, j], r[i-1, j+1], r[i, j]
            ss, se, sw = S[i-1, j], S[i-1, j+1], S[i, j]
            ps, pe, pw = psi[i-1, j], psi[i-1, j+1], psi[i, j]
            fs, fe, fw = phi[i-1, j], phi[i-1, j+1], phi[i, j]
            sn = se+sw-ss
            pn = pe+pw-ps
            if not math.isfinite(sn) or abs(sn) > cfg.max_abs_log_omega2:
                last_row, stop = i-1, "predictor lapse guard"
                break
            omega2_predictor = ((math.exp(ss)+math.exp(se)+math.exp(sw)+math.exp(sn))/4
                                if cfg.arithmetic_omega2_average else math.exp((ss+se+sw+sn)/4))
            wn = re*re+rw*rw-rs*rs-h*h*omega2_predictor/2
            change = 0.
            try:
                for _ in range(cfg.iterations):
                    if wn <= 0 or abs(sn) > cfg.max_abs_log_omega2:
                        raise ValueError("nonpositive r^2 or lapse guard")
                    rn = math.sqrt(wn)
                    fn = pn/rn
                    rc = (rs+re+rw+rn)/4
                    sc = (ss+se+sw+sn)/4
                    omega2c = ((math.exp(ss)+math.exp(se)+math.exp(sw)+math.exp(sn))/4
                               if cfg.arithmetic_omega2_average else math.exp(sc))
                    fu = (fw+fn-fs-fe)/(2*h)
                    fv = (fe+fn-fs-fw)/(2*h)
                    ru = (rw+rn-rs-re)/(2*h)
                    rv = (re+rn-rs-rw)/(2*h)
                    if cfg.freeze_geometry:
                        A = 0.
                        new_s = 0.
                        new_w = ((v[j+1]-u[i])/2)**2
                    else:
                        if j-i < centre_cells:
                            axis_closure_uses += 1
                            # r_uv/r -> -(phi_u phi_v)/3 at a smooth axis.
                            # The smooth-field closure error is O(r^2).
                            # The default band has width O(sqrt(h)); this is
                            # a consistency statement, not a convergence proof.
                            A = -fu*fv/3
                        else:
                            A = -(ru*rv+omega2c/4)/(rc*rc)
                        new_s = se+sw-ss+h*h*(-2*fu*fv-2*A)
                        new_w = re*re+rw*rw-rs*rs-h*h*omega2c/2
                    new_p = pe+pw-ps+h*h*A*(ps+pe+pw+pn)/4
                    change = max(abs(new_s-sn), abs(new_w-wn), abs(new_p-pn))
                    sn, wn, pn = new_s, new_w, new_p
                    if change < cfg.iteration_tolerance:
                        break
                if wn <= 0 or not all(math.isfinite(x) for x in (sn, wn, pn)):
                    raise ValueError("nonfinite diamond or nonpositive r^2")
                if change > cfg.iteration_failure_tolerance:
                    raise ValueError("diamond iteration did not converge")
                maximum_iteration_change = max(maximum_iteration_change, change)
                r[i, j+1], S[i, j+1], psi[i, j+1] = math.sqrt(wn), sn, pn
                phi[i, j+1] = pn/r[i, j+1]
            except (ValueError, OverflowError) as exc:
                last_row, stop = i-1, str(exc)
                break
        if stop:
            break
    keep = slice(0, last_row+1)
    return {"u": u[keep], "v": v, "r": r[keep], "S": S[keep],
            "psi": psi[keep], "phi": phi[keep],
            "report": {"completed_u": float(u[last_row]), "stop_reason": stop,
                       "maximum_last_iteration_change": maximum_iteration_change,
                       "axis_band_cells": centre_cells,
                       "axis_band_coordinate_width": centre_cells*h/2,
                       "axis_closure_cell_iterations": axis_closure_uses,
                       "exact_flat_cap_v": cfg.exact_flat_cap_v,
                       "evidence": "E0_neutral_axis_diamond_evolution",
                       "strict_trapping_certified": False}}


def geometry(data, i, j, fourth_order=False):
    if i < 1 or i+1 >= len(data["u"]) or j < i+3 or j+1 >= len(data["v"]):
        raise ValueError("geometry sample needs an interior two-sided stencil")
    h = data["v"][1]-data["v"][0]
    r = data["r"]
    radius = float(r[i, j])
    if fourth_order:
        if i < 2 or i+2 >= len(data["u"]) or j+2 >= len(data["v"]) or j < i+4:
            raise ValueError("fourth-order geometry needs a wider interior stencil")
        nu = float((r[i-2, j]-8*r[i-1, j]+8*r[i+1, j]-r[i+2, j])/(12*h))
        lam = float((r[i, j-2]-8*r[i, j-1]+8*r[i, j+1]-r[i, j+2])/(12*h))
    else:
        nu = float((r[i+1, j]-r[i-1, j])/(2*h))
        lam = float((r[i, j+1]-r[i, j-1])/(2*h))
    omega2 = math.exp(float(data["S"][i, j]))
    mass = radius*(1+4*nu*lam/omega2)/2
    return {"r": radius, "nu": nu, "lambda": lam, "Omega2": omega2,
            "Hawking_mass": mass, "theta_out": 4*lam/math.sqrt(omega2)/radius,
            "theta_in": 4*nu/math.sqrt(omega2)/radius}


def constraint_residuals(data, minimum_gap=.5, u_bounds=None, v_bounds=None):
    """Held-out two null Raychaudhuri equations on a fixed positive-radius set."""
    r, S, phi = data["r"], data["S"], data["phi"]
    h = data["v"][1]-data["v"][0]
    maxima = {"u_constraint": 0., "v_constraint": 0.}
    count = 0
    for i in range(2, len(data["u"])-2):
        if u_bounds is not None and not u_bounds[0] <= data["u"][i] <= u_bounds[1]:
            continue
        first = max(i+4, i+int(math.ceil(minimum_gap/h)))
        for j in range(first, len(data["v"])-2):
            if v_bounds is not None and not v_bounds[0] <= data["v"][j] <= v_bounds[1]:
                continue
            radius = r[i, j]
            if not math.isfinite(radius):
                continue
            ru = (r[i-2, j]-8*r[i-1, j]+8*r[i+1, j]-r[i+2, j])/(12*h)
            rv = (r[i, j-2]-8*r[i, j-1]+8*r[i, j+1]-r[i, j+2])/(12*h)
            suu = (-r[i-2, j]+16*r[i-1, j]-30*r[i, j]+16*r[i+1, j]-r[i+2, j])/(12*h*h)
            svv = (-r[i, j-2]+16*r[i, j-1]-30*r[i, j]+16*r[i, j+1]-r[i, j+2])/(12*h*h)
            Su = (S[i-2, j]-8*S[i-1, j]+8*S[i+1, j]-S[i+2, j])/(12*h)
            Sv = (S[i, j-2]-8*S[i, j-1]+8*S[i, j+1]-S[i, j+2])/(12*h)
            pu = (phi[i-2, j]-8*phi[i-1, j]+8*phi[i+1, j]-phi[i+2, j])/(12*h)
            pv = (phi[i, j-2]-8*phi[i, j-1]+8*phi[i, j+1]-phi[i, j+2])/(12*h)
            maxima["u_constraint"] = max(maxima["u_constraint"], abs(float(suu-Su*ru+radius*pu*pu)))
            maxima["v_constraint"] = max(maxima["v_constraint"], abs(float(svv-Sv*rv+radius*pv*pv)))
            count += 1
    maxima["stencil_points"] = count
    return maxima
