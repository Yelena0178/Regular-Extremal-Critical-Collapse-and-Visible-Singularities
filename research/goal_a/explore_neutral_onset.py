"""Finite causal-domain onset screening. All outcomes remain E0."""

from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import numpy as np
from neutral_characteristic import CharacteristicConfiguration, evolve, geometry, constraint_residuals
from neutral_onset_input import NeutralOnset


def summarize(data):
    candidate = None
    h = data["v"][1]-data["v"][0]
    for i in range(2, len(data["u"])-2):
        for j in range(i+5, len(data["v"])-2):
            radius = data["r"][i, j]
            if radius < .05:
                continue
            nu = (data["r"][i+1, j]-data["r"][i-1, j])/(2*h)
            lam = (data["r"][i, j+1]-data["r"][i, j-1])/(2*h)
            if nu < 0 and (candidate is None or lam < candidate["lambda"]):
                candidate = {"u": float(data["u"][i]), "v": float(data["v"][j]),
                             **geometry(data, i, j)}
    centre = []
    for i in range(2, len(data["u"])-2):
        derivative = (data["phi"][i+1, i+1]-data["phi"][i-1, i-1])/(2*h)
        proper_derivative = derivative/np.exp(data["S"][i, i]/2)
        centre.append(float(20*proper_derivative**4/3))
    return {**data["report"], "minimum_sampled_lambda_with_nu_negative": candidate,
            "maximum_sampled_central_K": max(centre, default=0.),
            "classification": "UNKNOWN", "actual_strict_trapping_certified": False}


def main():
    runs = []
    for epsilon in (.1, .05, .025, 0.):
        model = NeutralOnset.from_first_jet_report(smoothing_fraction=epsilon)
        initial, parameters = model.make_initial()
        for n in (192, 384, 768):
            cfg = CharacteristicConfiguration(steps=n, outer_v=parameters["v_end"],
                                               final_u=.54*parameters["v_end"],
                                               centre_cells=0,
                                               exact_flat_cap_v=parameters["v_cap"])
            data = evolve(initial, cfg)
            report = {"input": parameters, "configuration": asdict(cfg), **summarize(data)}
            i, j = n//2, 31*n//32
            report["fixed_point"] = {"u_fraction": "1/2", "v_fraction": "31/32",
                                     "u": float(data["u"][i]), "v": float(data["v"][j]),
                                     **geometry(data, i, j, True)}
            V = parameters["v_end"]
            report["heldout_local_constraints"] = constraint_residuals(
                data, u_bounds=(.45*V, .52*V), v_bounds=(.9*V, .99*V))
            report["heldout_full_constraints"] = constraint_residuals(data)
            runs.append(report)
            print(json.dumps({"epsilon": epsilon, "n": n,
                              "completed_u": report["completed_u"],
                              "stop": report["stop_reason"],
                              "fixed_point": report["fixed_point"],
                              "local_constraints": report["heldout_local_constraints"],
                              "central_K": report["maximum_sampled_central_K"]}), flush=True)
    folder = Path(__file__).resolve().parent
    result = {
        "evidence": "E0_neutral_onset_finite_causal_domain", "goal_A_proved": False,
        "runs": runs,
        "no_claim": ["rigorous_PDE_error", "actual_strict_trapping", "black_hole",
                     "critical_endpoint", "complete_future", "original_eta_layer_resolution"],
    }
    result["source_sha256"] = {
        name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
        for name in ("neutral_characteristic.py", "neutral_onset_input.py", "explore_neutral_onset.py",
                     "FIRST_JET_CHECKS_2026-10-16.json")
    }
    target = folder/"NEUTRAL_ONSET_SCAN_2026-10-16.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
