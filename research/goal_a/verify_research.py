"""Reproduce initial-constraint experiments and exact balance-law examples."""
from dataclasses import asdict, replace
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
from incoming_family import (Parameters, integrate, profile_integrals,
                             residuals, summary)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run():
    # Analytic input bounds are proved in EXACT_INITIAL_BUDGET.md. Only their
    # rational combination, not the exponential-function proof, is checked here.
    amplitude_limit = F(1, 8)
    c1, cq, c2 = F(281, 20), F(3), F(1263, 14)
    mass_bound = c1*amplitude_limit**2+c2*amplitude_limit**4
    delta_bound = 1-2*mass_bound
    require(mass_bound == F(69259, 286720), "rational initial mass budget")
    require(delta_bound == F(74101, 143360) and delta_bound > F(1, 2),
            "strict continuous-radius bootstrap margin")
    charge_lower = F(3, 5)*F(1, 5)*amplitude_limit**2*F(10, 27)
    require(charge_lower == F(1, 1440), "explicit nonzero charge budget")
    kappa, source_max = F(3, 5), F(801, 400)
    finite_amplitude_delta = (1-kappa*kappa)/(1+2*4*source_max)
    require(finite_amplitude_delta == F(32, 851) and finite_amplitude_delta > 0,
            "finite-amplitude Delta barrier budget")
    p = Parameters()
    grids = (256, 512, 1024, 2048)
    runs = [integrate(p, n) for n in grids]
    comparisons = []
    for coarse, fine in zip(runs, runs[1:]):
        comparisons.append(max(abs(x-y)
            for c, f in zip(coarse, fine[::2])
            for x, y in zip(c[1:], f[1:])))
    orders = [math.log(a/b, 2) for a, b in zip(comparisons, comparisons[1:])]
    require(all(3.7 < o < 4.3 for o in orders), "RK4 convergence not observed")
    residual_series = [residuals(rows, p) for rows in runs]
    last = residual_series[-1]
    require(last["hamiltonian"] < 1e-8, "Hamiltonian residual")
    require(last["gauss"] < 1e-8, "Gauss residual")
    require(last["momentum"] < 1e-12, "momentum residual")
    require(last["incoming"] < 1e-7, "incoming preparation residual")
    bad_q = residuals(runs[-1], p, "reverse_gauss")["gauss"]
    bad_k = residuals(runs[-1], p, "omit_extrinsic_curvature")["momentum"]
    require(bad_q > 100*max(last["gauss"], 1e-12), "Gauss sign mutation not detected")
    require(bad_k > 100*max(last["momentum"], 1e-12), "K omission not detected")
    conjugate = integrate(replace(p, frequency=-p.frequency), grids[-1])
    symmetry_error = max(max(abs(c[1]-d[1]), abs(c[2]+d[2]))
                         for c, d in zip(runs[-1], conjugate))
    require(symmetry_error < 1e-14, "charge conjugation symmetry")
    zero = integrate(replace(p, amplitude=0.0), grids[0])
    require(all(m == q == 0 for _, m, q in zero), "Minkowski initial data")
    rejected = []
    for label, invalid in [
        ("nan_amplitude", replace(p, amplitude=float("nan"))),
        ("wrong_fixed_coupling", replace(p, coupling=0.7)),
        ("invalid_shell", replace(p, outer=p.inner)),
    ]:
        try:
            integrate(invalid, 64)
        except ValueError:
            rejected.append(label)
        else:
            raise RuntimeError("invalid input was not rejected: "+label)
    aa, bb = profile_integrals(p)
    aa2, bb2 = profile_integrals(p, 4096)
    require(max(abs(aa-aa2), abs(bb-bb2)) < 1e-10, "quadrature comparison")
    omega = math.sqrt(aa/bb)
    optimum = p.coupling/(2*omega)
    weak = []
    leading = aa+p.frequency**2*bb
    for amplitude in (0.2, 0.1, 0.05):
        pp = replace(p, amplitude=amplitude)
        data = summary(integrate(pp, 2048), pp)
        data["amplitude"] = amplitude
        data["relative_leading_mass_error"] = abs(
            data["ADM_mass_estimate"]/(amplitude**2*leading)-1)
        weak.append(data)
    require(weak[-1]["relative_leading_mass_error"]
            < weak[0]["relative_leading_mass_error"]/10, "small-amplitude limit")
    scan = []
    for amplitude in (0.25, 0.5, 1.0, 2.0, 4.0):
        pp = replace(p, amplitude=amplitude, frequency=omega)
        try:
            entry = summary(integrate(pp, 2048), pp)
            entry["amplitude"] = amplitude
        except ValueError as exc:
            entry = {"amplitude": amplitude, "rejected": str(exc),
                     "outcome": "UNKNOWN_coordinate_data_rejected"}
        scan.append(entry)
    # Exact counterexample to interchange of parameter and late-time limits.
    mass = F(3, 2)
    exact = []
    for n in (2, 4, 8, 16):
        pp = -F(1, n)
        u = F(10)
        tail = mass/(1+pp*pp*u)
        quantile = 1/(pp*pp)  # theta=1/2
        require(mass/(1+pp*pp*quantile) == mass/2, "exact quantile identity")
        exact.append({"p": str(pp), "tail_at_u_10": str(tail),
                      "half_mass_time": str(quantile)})
    result = {
        "date": "2026-10-16",
        "evidence_scope": "initial_constraint_grid_experiment_and_exact_abstract_examples",
        "goal_A_proved": False, "spacetime_evolution_performed": False,
        "rigorous_float_error_bound": False,
        "analytic_initial_parameter_rectangle": {
            "amplitude_absolute_maximum": str(amplitude_limit),
            "frequency_absolute_maximum": "1/4",
            "mass_upper_bound": str(mass_bound),
            "all_radius_delta_lower_bound": str(delta_bound),
            "explicit_member_charge_strict_lower_bound": str(charge_lower),
            "proof": "EXACT_INITIAL_BUDGET.md",
            "scope": "continuous_initial_ODE_only_not_spacetime",
        },
        "analytic_finite_amplitude_rectangle": {
            "amplitude_absolute_maximum": "2",
            "frequency_absolute_maximum": "1/4",
            "charge_to_radius_upper_bound": str(kappa),
            "all_radius_delta_lower_bound": str(finite_amplitude_delta),
            "proof": "EXACT_INITIAL_BUDGET.md section 4",
            "scope": "continuous_initial_ODE_only_not_spacetime",
        },
        "parameters": asdict(p), "grids": grids,
        "successive_grid_differences": comparisons, "observed_orders": orders,
        "original_constraint_residuals": residual_series,
        "mutant_residuals": {"reversed_gauss": bad_q, "omitted_K": bad_k},
        "charge_conjugation_error": symmetry_error,
        "rejected_inputs": rejected,
        "profile": {"A_estimate": aa, "B_estimate": bb,
                    "optimal_frequency_estimate": omega,
                    "leading_maximum_ADM_ratio_estimate": optimum,
                    "Poincare_upper_bound_float": p.coupling*(p.outer-p.inner)/(2*math.pi)},
        "small_amplitude_comparison": weak,
        "fixed_shell_amplitude_scan": scan,
        "exact_balance_examples_not_EMCSF_solutions": exact,
        "remaining": ["actual_evolution", "Bondi_extraction_continuity",
                      "full_future_dispersion", "genuine_formation",
                      "exact_positive_mass_extremal_endpoint",
                      "subextremal_positive_branch"],
    }
    base = Path(__file__).resolve().parent
    result["source_sha256"] = {
        name: hashlib.sha256((base/name).read_bytes()).hexdigest()
        for name in ("incoming_family.py", "verify_research.py",
                     "ACCEPTANCE.md", "INCOMING_CONSTRAINT_FAMILY.md",
                     "BONDI_TAIL_OBSTRUCTION.md", "EXACT_INITIAL_BUDGET.md")
    }
    output = base/"RESULTS_2026-10-16.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n",
                      encoding="utf-8")
    print(json.dumps({"result": str(output), "observed_orders": orders,
                      "finest_residuals": last,
                      "optimal_frequency_estimate": omega,
                      "goal_A_proved": False}, ensure_ascii=False))


if __name__ == "__main__":
    run()
