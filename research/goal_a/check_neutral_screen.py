"""Audit saved E0 screen artifacts and scope; never certify a continuous PDE."""

import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def main():
    folder = Path(__file__).resolve().parent
    names = ["NEUTRAL_CHARACTERISTIC_RESULTS_2026-10-16.json",
             "NEUTRAL_ONSET_SCAN_2026-10-16.json", "NEUTRAL_SHAPE_SCAN_2026-10-16.json"]
    reports = [json.loads((folder/name).read_text(encoding="utf-8")) for name in names]
    for name, report in zip(names, reports):
        require(report["goal_A_proved"] is False, name+": scope")
        for source, digest in report["source_sha256"].items():
            require(hashlib.sha256((folder/source).read_bytes()).hexdigest() == digest,
                    name+": stale source "+source)
    benchmark, onset, shapes = reports
    require(benchmark["rigorous_PDE_error"] is False, "benchmark scope")
    for report in (onset, shapes):
        require("rigorous_PDE_error" in report["no_claim"], "screen scope")
        for run in report["runs"]:
            cfg, p = run["configuration"], run["input"]
            require(p["fixed_coupling"] == .6, "fixed coupling")
            require(run["classification"] == "UNKNOWN", "classification was upgraded")
            require(run["actual_strict_trapping_certified"] is False
                    and run["strict_trapping_certified"] is False, "trapping scope")
            require(run["stop_reason"] is None, "early numerical stop")
            require(run["axis_closure_cell_iterations"] == 0
                    and cfg["centre_cells"] == 0, "axis approximation used")
            require(cfg["exact_flat_cap_v"] == p["v_cap"]
                    and run["completed_u"] < p["v_cap"], "pre-arrival causal window")
            # Five-point extraction has a two-cell margin before the charged join.
            h = cfg["outer_v"]/cfg["steps"]
            require((31/32)*p["v_end"]+2*h < p["v_end"], "derivative stencil past join")
    observed = []
    for epsilon in (.05, 0.):
        group = [r for r in onset["runs"] if r["input"]["smoothing_fraction"] == epsilon]
        require([r["configuration"]["steps"] for r in group] == [192, 384, 768], "onset grids")
        for key in ("u", "v"):
            values = [r["fixed_point"][key] for r in group]
            require(max(values)-min(values) < 1e-12, "moving comparison point")
        for key in ("r", "lambda", "theta_out"):
            values = [r["fixed_point"][key] for r in group]
            differences = [abs(b-a) for a, b in zip(values, values[1:])]
            require(differences[1] < differences[0]/2, "fixed-point mesh differences: "+key)
        for coarse, fine in zip(group, group[1:]):
            for key in ("u_constraint", "v_constraint"):
                require(fine["heldout_local_constraints"][key]
                        < coarse["heldout_local_constraints"][key]/2,
                        "local held-out constraint differences")
        observed.append({"epsilon": epsilon,
                         "theta_out": [r["fixed_point"]["theta_out"] for r in group],
                         "theta_in": [r["fixed_point"]["theta_in"] for r in group]})
    sources = names+["check_neutral_screen.py", "NEUTRAL_CAUSAL_SCREEN.md",
                     "NEUTRAL_CHARACTERISTIC_METHOD.md"]
    result = {"consistency": "pass", "evidence": "E0_saved_artifact_consistency_only",
              "goal_A_proved": False, "rigorous_PDE_error": False,
              "actual_strict_trapping_certified": False,
              "observed_fixed_point_expansions": observed,
              "source_sha256": {name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
                                for name in sources}}
    target = folder/"NEUTRAL_SCREEN_CHECKS_2026-10-16.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"consistency": "pass", "scope": result["evidence"],
                      "report": target.name}))


if __name__ == "__main__":
    main()
