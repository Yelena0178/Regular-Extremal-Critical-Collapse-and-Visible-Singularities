"""Horizon-coordinate, held-out propagation, and proper-clock gauge comparisons."""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import math
import numpy as np
from areal_shift_evolution import (ShiftConfiguration, evolve_shifted,
    shifted_geometry, shifted_rhs_with_geometry, shifted_propagation_residuals,
    radial_divergence, odd_derivative)
from polar_evolution import Configuration, evolve, first_derivative


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def orders(errors):
    return [math.log(a/b, 2) for a, b in zip(errors, errors[1:])]


def rn_functions(radius, mass=1., charge=.4):
    dd = 1-2*mass/radius+charge**2/radius**2
    z = 1/np.sqrt(2-dd)
    return z, (1-dd)*z


def run():
    grids = (64, 128, 256, 512)
    mass, charge = 1., .4
    rn_results = []
    probe_faces = ((np.linspace(.5, 8., grids[0]+1)[:-1]
                    +np.linspace(.5, 8., grids[0]+1)[1:])/2)[2:-2]
    for n in grids:
        r = np.linspace(.5, 8., n+1)
        z, w = rn_functions(r)
        rf = (r[:-1]+r[1:])/2
        _, face_w = rn_functions(rf)
        face_array = np.r_[face_w, 0.]
        state = np.stack((np.zeros_like(r), np.zeros_like(r), face_array, np.log(z))).astype(complex)
        g = shifted_geometry(r, state, inner_mass=mass-charge**2/(2*r[0]),
                             inner_charge=charge)
        flow = shifted_rhs_with_geometry(r, state, g, frozen_lapse=True)
        rn_results.append({
            "steps": n,
            "mass_error": float(np.max(abs(g["mass"]-(mass-charge**2/(2*r))))),
            "spatial_metric_error": float(np.max(abs(g["z"]-z))),
            "angular_equation_error_fixed_probe_points":
                float(np.max(abs(np.interp(probe_faces, rf, flow[2, :-1].real)))),
            "angular_equation_error_moving_interior": float(np.max(abs(flow[2, 2:-3]))),
            "minimum_hawking_delta": float(np.min(g["hawking_delta"])),
            "minimum_spatial_delta": float(np.min(g["spatial_delta"])),
            "minimum_outgoing_expansion": float(np.min(2*(g["z"]-w)/r)),
        })
    rn_orders = orders([x["angular_equation_error_fixed_probe_points"] for x in rn_results])
    require(all(1.8 < value < 2.2 for value in rn_orders),
            "RN angular equation did not converge")
    require(rn_results[-1]["spatial_metric_error"]
            < rn_results[0]["spatial_metric_error"]/20, "RN spatial reconstruction")
    # Independent complex-step derivatives of the exact RN functions, including
    # the region between the outer and inner horizons. This does not test 1+log
    # stationarity: the KS lapse is frozen only for this angular identity.
    radii = np.array([.5, .75, 1., 1.5, 2., 3., 6.])
    eps = 1e-25
    z, w = rn_functions(radii)
    zz, ww = rn_functions(radii+1j*eps)
    da, dw = zz.imag/eps, ww.imag/eps
    beta = z*w
    identity = beta*dw-z*z*da+z*(
        (mass-charge**2/(2*radii))/radii**2-charge**2/(2*radii**3))
    exact_identity_error = float(np.max(abs(identity)))
    require(exact_identity_error < 1e-12, "exact RN angular identity")
    spectra = []
    for n in (16, 32, 64):
        r = np.linspace(0., 1., n+1)
        h = 1/n
        rf = (r[:-1]+r[1:])/2
        mat = np.zeros((2*n, 2*n))
        for j in range(2*n):
            ll, ww = np.zeros(n+1), np.zeros(n+1)
            if j < n:
                ll[j] = 1
            else:
                ww[j-n] = 1
            mat[:, j] = np.r_[-2*radial_divergence(r, ww)[:n], -np.diff(ll)/h]
        volumes = np.r_[rf[0]**3/3, (rf[1:]**3-rf[:-1]**3)/3]
        weights = np.r_[volumes, 2*h*rf*rf]
        ha = weights[:, None]*mat
        skew_error = float(np.max(abs(ha+ha.T)))
        max_real = float(np.max(np.linalg.eigvals(mat).real))
        require(skew_error < 1e-12 and max_real < 1e-8,
                "linear flat gauge mode is unstable")
        old_mat = np.zeros((2*n-1, 2*n-1))
        safe = np.where(r == 0, 1, r)
        for j in range(2*n-1):
            ll, ww = np.zeros(n+1), np.zeros(n+1)
            if j < n:
                ll[j] = 1
            else:
                ww[j-n+1] = 1
            dw = odd_derivative(ww, h)
            wr = ww/safe
            wr[0] = dw[0]
            old_mat[:, j] = np.r_[-2*(dw+2*wr)[:n], -first_derivative(ll, h)[1:n]]
        old_growth = float(np.max(np.linalg.eigvals(old_mat).real))
        require(old_growth > .1/h, "rejected collocated gauge stencil not detected")
        spectra.append({"steps": n, "weighted_skew_error": skew_error,
                        "maximum_eigenvalue_real_part": max_real,
                        "rejected_collocated_stencil_growth_real_part": old_growth})
    traces = []
    for n in (32, 64, 128, 256):
        r = np.linspace(0., 1., n+1)
        rf = (r[:-1]+r[1:])/2
        state = np.stack((1+.2*r*r, -1j*(1+.3*r*r),
                          np.r_[.1*rf, 0.], -.1*r*r)).astype(complex)
        g = shifted_geometry(r, state)
        traces.append({
            "steps": n, "mass_trace_error": float(abs(g["mass"][1]/r[1]**3-1/6)),
            "charge_trace_error": float(abs(g["charge"][1]/r[1]**3-.6/3)),
        })
    require(all(1.8 < x < 2.2 for x in orders([t["mass_trace_error"] for t in traces])),
            "center mass trace with nonzero W")
    results, proper_errors, residuals, fields_list = [], [], [], []
    polar_axes = {}
    for n in grids:
        cfg = ShiftConfiguration(steps=n, final_time=4.)
        r, state, report, axis = evolve_shifted(cfg)
        results.append(report)
        fields_list.append(state)
        residuals.append(shifted_propagation_residuals(r, state))
        _, _, old = evolve(Configuration(steps=n, final_time=4., record_axis=True))
        old_axis = np.asarray(old["axis_trace"])
        polar_axes[n] = old_axis
        end_tau = min(axis[-1, 1], old_axis[-1, 1])
        tau_grid = np.linspace(0., end_tau, 257)
        phi_new = np.interp(tau_grid, axis[:, 1], axis[:, 2])
        phi_old = np.interp(tau_grid, old_axis[:, 1], old_axis[:, 2])
        proper_errors.append(float(np.max(abs(phi_new-phi_old))))
    differences = []
    for a, b in zip(fields_list, fields_list[1:]):
        restricted = b[:, ::2].copy()
        restricted[2, :-1] = (b[2, :-1:2]+b[2, 1:-1:2])/2
        restricted[2, -1] = 0
        differences.append(float(np.max(abs(a-restricted))))
    convergence = orders(differences)
    for key in ("mass_time_propagation", "charge_time_propagation",
                "spatial_metric_time_propagation"):
        require(residuals[-1][key] < residuals[0][key]/15,
                "held-out shifted propagation did not decrease: "+key)
    require(all(1.5 < x < 2.5 for x in convergence), "shifted fields grid convergence")
    require(proper_errors[-1] < proper_errors[0]/15, "proper-clock gauge comparison")
    harmonic_reports, harmonic_errors, harmonic_residuals = [], [], []
    for n in grids[1:]:
        cfg = ShiftConfiguration(steps=n, final_time=4., slicing="harmonic")
        r, state, report, axis = evolve_shifted(cfg)
        harmonic_reports.append(report)
        harmonic_residuals.append(shifted_propagation_residuals(r, state, slicing="harmonic"))
        old_axis = polar_axes[n]
        tau_grid = np.linspace(0., min(axis[-1, 1], old_axis[-1, 1]), 257)
        harmonic_errors.append(float(np.max(abs(
            np.interp(tau_grid, axis[:, 1], axis[:, 2])
            -np.interp(tau_grid, old_axis[:, 1], old_axis[:, 2])))))
    require(harmonic_errors[-1] < harmonic_errors[0]/10, "harmonic proper-clock comparison")
    for key in harmonic_residuals[0]:
        require(harmonic_residuals[-1][key] < harmonic_residuals[0][key]/10,
                "harmonic propagation residual: "+key)
    _, zero, zero_report, _ = evolve_shifted(ShiftConfiguration(
        steps=32, final_time=1., amplitude=0.))
    require(np.max(abs(zero)) == 0, "Minkowski zero state")
    output = {
        "date": "2026-10-16", "evidence": "E0_coordinate_and_weak_field_benchmarks",
        "goal_A_proved": False, "genuine_formation_certified": False,
        "actual_strict_trapped_sphere_certified": False,
        "rigorous_PDE_error_bound": False,
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "configuration": asdict(ShiftConfiguration(final_time=4.)),
        "grids": grids, "RN_horizon_ring": rn_results,
        "RN_angular_equation_orders": rn_orders,
        "RN_complex_step_identity_error": exact_identity_error,
        "linear_flat_gauge_spectral_and_energy_checks": spectra,
        "center_Taylor_trace_with_nonzero_W": traces,
        "weak_field_reports": results, "grid_differences": differences,
        "observed_orders": convergence,
        "independent_propagation_residuals": residuals,
        "axis_scalar_absolute_value_difference_at_common_proper_time": proper_errors,
        "harmonic_weak_field": {
            "grids": grids[1:], "reports": harmonic_reports,
            "axis_absolute_scalar_proper_clock_errors": harmonic_errors,
            "independent_propagation_residuals": harmonic_residuals,
        },
        "zero_state_report": zero_report,
        "scope": "RN_ring_is_not_regular_center_collapse;axis_agreement_is_not_isometry_proof",
        "remaining": ["strong_field_grid_and_gauge_control", "finite_error_certificate",
                      "entire_negative_dispersion_branch", "exact_extremal_endpoint"],
    }
    folder = Path(__file__).resolve().parent
    output["source_sha256"] = {
        name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
        for name in ("areal_shift_evolution.py", "verify_areal_shift.py",
                     "AREAL_SHIFT_EVOLUTION.md", "polar_evolution.py", "incoming_family.py")
    }
    target = folder/"AREAL_SHIFT_RESULTS_2026-10-16.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"result": str(target), "RN_orders": rn_orders,
                      "field_orders": convergence, "proper_clock_errors": proper_errors,
                      "last_propagation": residuals[-1], "goal_A_proved": False}))


if __name__ == "__main__":
    run()
