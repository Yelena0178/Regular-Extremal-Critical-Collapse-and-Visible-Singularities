"""Numerical consistency checks for finite-dimensional shooting, not PDE proof."""

from dataclasses import replace
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from first_jet_shooting import (
    ShootingConfiguration, evaluate, late_bump, limit_start, solve_first_jet)
from verify_horizon_seed import first_jet_diagnostic


def jacobian(point, cfg, step):
    columns = []
    for i in range(3):
        increment = np.zeros(3)
        increment[i] = step
        columns.append((evaluate(point+increment, cfg)-evaluate(point-increment, cfg))/(2*step))
    return np.column_stack(columns)


def main():
    base = ShootingConfiguration()
    limit = limit_start(base)
    lim_report = evaluate((limit[0], 0., 0.), replace(base, beta=0.), True)
    independent = first_jet_diagnostic()["runs"][-1]
    old_jet = 5*complex(independent["Du_phi_at_end_real"], independent["Du_phi_at_end_imag"])
    new_jet = complex(*lim_report["base_J_over_beta"])
    if abs(old_jet-new_jet) > 3e-10:
        raise ArithmeticError("independent baseline wave-moment comparison")
    integral, _ = quad(lambda y: late_bump(y)[0], 0., 1., epsabs=1e-13, epsrel=1e-13)
    coefficient = complex(*lim_report["late_coefficient"])
    if abs(coefficient+1j*.6*integral/4) > 3e-12:
        raise ArithmeticError("charged late coefficient at the auxiliary limit")
    s0 = limit[0]
    analytic_charge_slope = -1/(2*s0*(1-s0))
    analytic_determinant = analytic_charge_slope*(.6*integral/4)**2
    Jlim = jacobian(limit, replace(base, beta=0.), 2e-5)
    if abs(np.linalg.det(Jlim)-analytic_determinant) > 3e-7:
        raise ArithmeticError("auxiliary determinant comparison")
    if not np.isfinite(Jlim).all() or analytic_determinant >= 0:
        raise ArithmeticError("auxiliary rank")

    runs = []
    point = limit
    for rtol, atol, max_step in ((2e-9, 2e-11, .06),
                                (2e-10, 2e-12, .04),
                                (2e-11, 2e-13, .02)):
        cfg = replace(base, beta=.003, rtol=rtol, atol=atol, max_step=max_step)
        point, report = solve_first_jet(cfg, point)
        if not report["root_solver"]["success"] or max(abs(np.array(report["scaled_residual"]))) > 2e-9:
            raise ArithmeticError("exploratory root residual")
        if report["min_sampled_H"] <= 0 or report["r_initial"] <= 0:
            raise ArithmeticError("sampled positive-radius or H margin")
        if max(report["heldout_Gauss_integral_error"], report["heldout_late_wave_form_error"]) > 2e-9:
            raise ArithmeticError("independent charge/wave quadratures")
        runs.append(report)
    cfg = replace(base, beta=.003, rtol=2e-11, atol=2e-13, max_step=.02)
    derivatives = [jacobian(point, cfg, step) for step in (1e-4, 5e-5, 2.5e-5)]
    parameter_vectors = [
        np.array([r["parameters"]["s"], r["parameters"]["W_real"], r["parameters"]["W_imag"]])
        for r in runs]
    differences = [float(np.max(abs(b-a))) for a, b in zip(parameter_vectors, parameter_vectors[1:])]
    if max(differences) > 2e-7:
        raise ArithmeticError("root drift across ODE tolerances")
    # Ring sanity check for [[d,0,0],[a,0,c],[b,-c,0]]. Arbitrary-parameter
    # invertibility is proved in the analytic note, independently of samples.
    d, c, a, b = Fraction(-7, 3), Fraction(2, 5), Fraction(8, 7), Fraction(-9, 11)
    determinant = d*(0*0-c*(-c))-0*(a*0-c*b)+0*(a*(-c)-0*b)
    if determinant != d*c*c:
        raise ArithmeticError("exact determinant sanity check")
    folder = Path(__file__).resolve().parent
    result = {
        "evidence": "E0_float_ODE_consistency_and_finite_algebra",
        "goal_A_proved": False, "rigorous_root_box": False,
        "baseline_moment_difference": abs(old_jet-new_jet),
        "late_bump_integral_numeric": integral,
        "auxiliary_limit_point_numeric": limit.tolist(),
        "auxiliary_analytic_charge_slope_numeric": analytic_charge_slope,
        "auxiliary_analytic_determinant_numeric": analytic_determinant,
        "auxiliary_finite_difference_determinant": float(np.linalg.det(Jlim)),
        "runs": runs, "successive_parameter_differences": differences,
        "finite_beta_jacobian_determinants": [float(np.linalg.det(x)) for x in derivatives],
        "finite_beta_jacobian_step_differences":
            [float(np.max(abs(b-a))) for a, b in zip(derivatives, derivatives[1:])],
        "no_claim": ["interval_root_certificate", "explicit_analytic_beta0",
                     "smooth_layer_resolution", "all_higher_transverse_jets",
                     "regular_centre_future", "RN_terminal_geometry", "criticality"],
    }
    result["source_sha256"] = {
        name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
        for name in ("FIRST_TRANSVERSE_JET.md", "first_jet_shooting.py",
                     "verify_first_jet.py", "verify_horizon_seed.py")
    }
    output = folder/"FIRST_JET_CHECKS_2026-10-16.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({
        "consistency": "pass", "auxiliary_determinant": analytic_determinant,
        "parameter_drift": differences, "scope": result["evidence"], "report": output.name,
    }), flush=True)


if __name__ == "__main__":
    main()
