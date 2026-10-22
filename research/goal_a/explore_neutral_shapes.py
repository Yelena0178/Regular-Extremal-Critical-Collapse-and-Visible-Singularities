"""E0 comparisons of frozen-coupling shapes; no terminal or global certification."""

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from neutral_characteristic import CharacteristicConfiguration, evolve, geometry, constraint_residuals
from neutral_onset_input import NeutralOnset
from explore_neutral_onset import summarize


def main():
    cases = [
        (5., .5, .25, .05, (384,)),
        (5., .5, .125, .05, (384,)),
        (10., .7, .125, .05, (192, 384, 768)),
        (10., .7, .125, 0., (192, 384, 768)),
    ]
    runs = []
    for radius, amplitude, ratio, epsilon, grids in cases:
        model = NeutralOnset(radius=radius, field_amplitude=amplitude, radius_ratio=ratio,
                             smoothing_fraction=epsilon,
                             input_reference="prospective fixed-e C0 shape; no transverse repair")
        initial, p = model.make_initial()
        for n in grids:
            cfg = CharacteristicConfiguration(
                steps=n, outer_v=p["v_end"], final_u=.95*p["v_cap"],
                centre_cells=0, exact_flat_cap_v=p["v_cap"])
            data = evolve(initial, cfg)
            fraction = 1/2 if .5*p["v_end"] < .9*p["v_cap"] else 5/32
            i, j = round(fraction*n), 31*n//32
            report = {"input": p, "configuration": asdict(cfg), **summarize(data),
                      "fixed_point": {"u_fraction": str(fraction), "v_fraction": "31/32",
                                      **geometry(data, i, j, True)}}
            V = p["v_end"]
            report["heldout_local_constraints"] = constraint_residuals(
                data, u_bounds=((fraction-.015)*V, (fraction+.015)*V),
                v_bounds=(.9*V, .99*V))
            runs.append(report)
            print(json.dumps({"R": radius, "Phi": amplitude, "rho": ratio, "epsilon": epsilon,
                              "n": n, "stop": report["stop_reason"],
                              "fixed_theta_out": report["fixed_point"]["theta_out"],
                              "minimum_lambda": report["minimum_sampled_lambda_with_nu_negative"]["lambda"],
                              "outer_budget": p["outer_null_constraint_budget_C0"]}), flush=True)
    folder = Path(__file__).resolve().parent
    result = {"evidence": "E0_neutral_shape_comparison_before_axis_arrival",
              "goal_A_proved": False, "coupling_fixed": "3/5", "runs": runs,
              "no_claim": ["rigorous_PDE_error", "full_RN_matching", "global_no_trap",
                           "complete_dispersion", "criticality", "smooth_charge_root_certificate"]}
    result["source_sha256"] = {
        name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
        for name in ("neutral_characteristic.py", "neutral_onset_input.py",
                     "explore_neutral_onset.py", "explore_neutral_shapes.py")}
    target = folder/"NEUTRAL_SHAPE_SCAN_2026-10-16.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
