"""Narrow, reproducible E0 shooting along decreasing auxiliary beta."""

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
import scipy
from first_jet_shooting import ShootingConfiguration, limit_start, solve_first_jet


def main():
    base = ShootingConfiguration()
    start = limit_start(base)
    auxiliary_limit_start = start.copy()
    runs = []
    for beta in (.01, .003, .001, .0003):
        cfg = replace(base, beta=beta)
        try:
            point, report = solve_first_jet(cfg, start)
            start = point
        except (ValueError, FloatingPointError) as exc:
            report = {"beta": beta, "status": "UNKNOWN", "error": str(exc)}
        runs.append(report)
        print(json.dumps({"beta": beta, "residual": report.get("scaled_residual"),
                          "H_min": report.get("min_sampled_H"),
                          "parameters": report.get("parameters"),
                          "error": report.get("error")}), flush=True)
    folder = Path(__file__).resolve().parent
    result = {
        "evidence": "E0_C0_early_segment_only", "goal_A_proved": False,
        "runtime": {"python": platform.python_version(), "numpy": np.__version__,
                    "scipy": scipy.__version__},
        "limit_start": auxiliary_limit_start.tolist(), "runs": runs,
        "no_claim": ["rigorous_root_box", "smooth_rounding_resolution",
                     "complete_RN_gluing", "regular_centre_future",
                     "Cauchy_family", "criticality"],
    }
    result["source_sha256"] = {
        name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
        for name in ("first_jet_shooting.py", "explore_first_jet.py")
    }
    target = folder/"FIRST_JET_EXPLORATION_2026-10-16.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
