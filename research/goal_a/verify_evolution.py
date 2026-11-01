"""Finite-time numerical holdouts for A-EVOL01; not a goal-A certificate."""
from dataclasses import asdict, replace
import hashlib
import json
import math
from pathlib import Path
import platform
import numpy as np
from incoming_family import Parameters, bump, integrate
from polar_evolution import (Configuration, evolve, geometry, initial_fields,
                             propagation_residuals)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pulse(s, amplitude, frequency):
    p = Parameters(amplitude=amplitude, frequency=frequency)
    value, derivative = bump(float(s), p)
    if value == 0:
        second = 0.
    else:
        x = (s-p.inner)/(p.outer-p.inner)
        z = x*(1-x)
        logfirst = (1-2*x)/((p.outer-p.inner)*z*z)
        logsecond = (-2/z**2-2*(1-2*x)**2/z**3)/(p.outer-p.inner)**2
        second = value*(logfirst**2+logsecond)
    phase = np.exp(-1j*frequency*s)
    return (
        amplitude*value*phase,
        amplitude*(derivative-1j*frequency*value)*phase,
        amplitude*(second-2j*frequency*derivative-frequency**2*value)*phase,
    )


def flat_solution(r, t, amplitude, frequency):
    plus = np.array([pulse(t+x, amplitude, frequency) for x in r])
    minus = np.array([pulse(t-x, amplitude, frequency) for x in r])
    safe = np.where(r == 0, 1, r)
    phi = (plus[:, 0]-minus[:, 0])/safe
    canonical = (plus[:, 1]-minus[:, 1])/safe
    center = pulse(t, amplitude, frequency)
    phi[0], canonical[0] = 2*center[1], 2*center[2]
    return np.stack((phi, canonical))


def orders(errors):
    return [math.log(a/b, 2) for a, b in zip(errors, errors[1:])]


def run():
    grids = (128, 256, 512, 1024)
    base = Configuration()
    flat_errors, flat_center_errors = [], []
    for n in grids:
        cfg = replace(base, steps=n, final_time=12., flat_background=True)
        r, fields, _ = evolve(cfg)
        exact = flat_solution(r, cfg.final_time, cfg.amplitude, cfg.frequency)
        flat_errors.append(float(np.max(np.abs(fields-exact))))
        flat_center_errors.append(float(np.max(np.abs(fields[:, 0]-exact[:, 0]))))
    flat_orders = orders(flat_errors)
    require(all(1.7 < order < 2.3 for order in flat_orders),
            "analytic flat wave did not show second-order convergence")
    # Independent static RN ring; this is not a regular-center collapse example.
    rr = np.linspace(3., 48., 1025)
    mass, charge = 1., 0.4
    rn = geometry(rr, np.zeros((2, len(rr)), dtype=complex),
                  inner_mass=mass-charge**2/(2*rr[0]), inner_charge=charge)
    delta = 1-2*mass/rr+charge**2/rr**2
    rn_errors = {
        "metric_b": float(np.max(np.abs(rn["metric_b"]-1/np.sqrt(delta)))),
        "alpha": float(np.max(np.abs(rn["alpha"]-np.sqrt(delta)))),
        "potential": float(np.max(np.abs(rn["potential"]-charge/rr))),
    }
    require(max(rn_errors.values()) < 1e-12, "static RN normalization mismatch")
    # Regular-center Taylor traces, independent of the evolution solution.
    # For phi(0)=1 and P(0)=-i: Q/r^3 -> e/3, m/r^3 -> 1/6.
    center_errors = []
    for n in (32, 64, 128, 256):
        center_r = np.linspace(0., 1., n+1)
        manufactured = np.stack((1+0.2*center_r**2,
                                 -1j*(1+0.3*center_r**2)))
        cg = geometry(center_r, manufactured)
        center_errors.append({
            "steps": n,
            "Q_over_r3_error_at_first_cell": float(abs(cg["charge"][1]/center_r[1]**3-0.6/3)),
            "m_over_r3_error_at_first_cell": float(abs(cg["mass"][1]/center_r[1]**3-1/6)),
        })
    for key in ("Q_over_r3_error_at_first_cell", "m_over_r3_error_at_first_cell"):
        require(all(1.8 < value < 2.2 for value in orders([x[key] for x in center_errors])),
                "regular-center Taylor trace failure: "+key)
    _, zero, zero_report = evolve(replace(base, steps=32, amplitude=0., final_time=1.))
    require(np.max(np.abs(zero)) == 0 and zero_report["mass_boundary_drift"] == 0,
            "zero-data full-model Minkowski baseline")
    charged_runs, charged_reports, residuals = [], [], []
    for n in grids:
        r, fields, report = evolve(replace(base, steps=n))
        charged_runs.append((r, fields))
        report["steps"] = n
        charged_reports.append(report)
        residuals.append(propagation_residuals(r, fields))
    grid_errors = [float(np.max(np.abs(a[1]-b[1][:, ::2])))
                   for a, b in zip(charged_runs, charged_runs[1:])]
    charged_orders = orders(grid_errors)
    require(all(1.65 < order < 2.35 for order in charged_orders),
            "full coupled field grid convergence")
    for key in ("mass_propagation_max", "charge_propagation_max",
                "potential_gradient_max_interior"):
        require(residuals[-1][key] < residuals[0][key]/20,
                "held-out propagation residual did not decrease: "+key)
    for key in ("mass_boundary_drift", "charge_boundary_drift"):
        require(abs(charged_reports[-1][key]) < abs(charged_reports[0][key])/20,
                "boundary conservation drift did not decrease: "+key)
    fine_r, fine_fields = charged_runs[-1]
    # Same dr, independent outer radius; then independent time-step halving.
    larger = replace(base, steps=1280, outer_radius=60.)
    _, larger_fields, larger_report = evolve(larger)
    outer_difference = float(np.max(np.abs(fine_fields-larger_fields[:, :len(fine_r)])))
    _, halfdt_fields, _ = evolve(replace(base, steps=1024, cfl=0.1))
    time_difference = float(np.max(np.abs(fine_fields-halfdt_fields)))
    require(outer_difference < grid_errors[-1]/10, "outer-radius sensitivity too large")
    require(time_difference < grid_errors[-1]/10, "time-step sensitivity too large")
    _, conjugate, _ = evolve(replace(base, steps=256, frequency=-base.frequency))
    conjugation_error = float(np.max(np.abs(conjugate-np.conjugate(charged_runs[1][1]))))
    require(conjugation_error < 1e-12, "full charged evolution conjugation")
    correct = propagation_residuals(fine_r, fine_fields)
    mutant = propagation_residuals(fine_r, fine_fields, reverse_potential=True)
    require(mutant["potential_gradient_max_interior"]
            > 20*correct["potential_gradient_max_interior"],
            "wrong potential sign not detected by Maxwell gradient")
    require(mutant["mass_propagation_max"] > 5*correct["mass_propagation_max"],
            "wrong potential sign not detected by independent energy propagation")
    # Initial metric/charge comparison with the earlier high-order ODE solver.
    p = Parameters(amplitude=base.amplitude, frequency=base.frequency)
    reference = integrate(p, 8192)[-1]
    reference_charge = reference[2]
    reference_mass = reference[1]+reference_charge**2/(2*p.outer)
    initial_errors = []
    for n in grids:
        r = np.linspace(0, base.outer_radius, n+1)
        g = geometry(r, initial_fields(r, base.amplitude, base.frequency))
        mass_estimate = g["mass"][-1]+g["charge"][-1]**2/(2*r[-1])
        initial_errors.append(max(abs(mass_estimate-reference_mass),
                                  abs(g["charge"][-1]-reference_charge)))
    require(all(1.7 < x < 2.3 for x in orders(initial_errors)),
            "evolution initial constraints disagree with independent RK4 family")
    output = {
        "date": "2026-10-16", "evidence": "E0_finite_time_numerical_benchmark",
        "goal_A_proved": False, "rigorous_PDE_error_bound": False,
        "complete_dispersion_certified": False, "Bondi_extraction_performed": False,
        "external_independent_review": False,
        "configuration": asdict(base), "grids": grids,
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "flat_analytic_full_field_errors": flat_errors,
        "flat_analytic_center_errors": flat_center_errors,
        "flat_observed_orders": flat_orders,
        "static_RN_ring_errors": rn_errors,
        "regular_center_Taylor_trace_errors": center_errors,
        "full_coupled_reports": charged_reports,
        "full_coupled_field_grid_differences": grid_errors,
        "full_coupled_observed_orders": charged_orders,
        "independent_propagation_residuals": residuals,
        "larger_outer_radius_report": larger_report,
        "outer_radius_difference_at_fixed_dr": outer_difference,
        "halved_dt_difference_at_fixed_dr": time_difference,
        "charge_conjugation_error": conjugation_error,
        "wrong_potential_sign_residuals": mutant,
        "independent_initial_constraint_errors": initial_errors,
        "not_certified": ["all_future", "all_causal_geodesics", "complete_I_plus",
                          "genuine_black_hole_formation", "exact_RN_endpoint",
                          "parameter_neighborhood_trichotomy"],
    }
    folder = Path(__file__).resolve().parent
    output["source_sha256"] = {
        name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
        for name in ("polar_evolution.py", "verify_evolution.py", "POLAR_EVOLUTION.md",
                     "incoming_family.py")
    }
    target = folder/"EVOLUTION_RESULTS_2026-10-16.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({
        "result": str(target), "flat_orders": flat_orders,
        "coupled_orders": charged_orders, "finest_propagation": residuals[-1],
        "outer_difference": outer_difference, "time_difference": time_difference,
        "goal_A_proved": False,
    }))


if __name__ == "__main__":
    run()
