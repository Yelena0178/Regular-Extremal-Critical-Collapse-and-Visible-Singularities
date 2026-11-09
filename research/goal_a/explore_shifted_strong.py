"""Fixed-time charged strong-field comparisons, not an actual trapping proof."""
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
from areal_shift_evolution import (
    ShiftConfiguration, evolve_shifted, shifted_geometry, shifted_propagation_residuals)


def run():
    base = ShiftConfiguration(outer_radius=80., final_time=37.4, amplitude=2.,
                              frequency=.2, slicing="harmonic")
    runs, arrays = [], []
    for n in (512, 1024, 2048):
        cfg = replace(base, steps=n)
        try:
            r, state, report, _ = evolve_shifted(cfg)
            g = shifted_geometry(r, state)
            index = int(np.argmin(abs(r-.9375)))
            radius = float(r[index])
            report.update({
                "configuration": asdict(cfg),
                "fixed_sphere": {
                    "radius": radius, "theta_plus": float(2*(g["z"][index]-g["w"][index])/radius),
                    "theta_minus": float(-2*(g["z"][index]+g["w"][index])/radius),
                    "Hawking_mass": float(g["mass"][index]), "charge": float(g["charge"][index]),
                    "spatial_delta": float(g["spatial_delta"][index]),
                    "hawking_delta": float(g["hawking_delta"][index]),
                },
                "propagation_residuals": shifted_propagation_residuals(r, state, slicing=cfg.slicing),
            })
            arrays.append((n, state))
        except ValueError as exc:
            report = {"configuration": asdict(cfg), "stop_reason": str(exc),
                      "context": getattr(exc, "context", {}), "classification": "UNKNOWN"}
        runs.append(report)
        print(json.dumps({"steps": n, "completed_time": report.get("completed_time"),
                          "fixed_sphere": report.get("fixed_sphere"),
                          "stop_reason": report.get("stop_reason")}), flush=True)
    differences = []
    for (nc, coarse), (nf, fine) in zip(arrays, arrays[1:]):
        if nf != 2*nc:
            continue
        restricted = fine[:, ::2].copy()
        restricted[2, :-1] = (fine[2, :-1:2]+fine[2, 1:-1:2])/2
        restricted[2, -1] = 0
        differences.append(float(np.max(abs(coarse-restricted))))
    # Keep a known problematic nonlinear 1+log run as a failed control, not as
    # evidence of an antitrapped region or as a passed evolution.
    control_cfg = replace(base, steps=512, frequency=0., final_time=30., slicing="1+log")
    try:
        _, _, control, _ = evolve_shifted(control_cfg)
        control["configuration"] = asdict(control_cfg)
    except ValueError as exc:
        control = {"configuration": asdict(control_cfg), "stop_reason": str(exc),
                   "context": getattr(exc, "context", {}), "classification": "UNKNOWN"}
    folder = Path(__file__).resolve().parent
    output = {
        "date": "2026-10-16", "evidence": "E0_fixed_time_charged_grid_exploration",
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "goal_A_proved": False, "actual_strict_trapped_sphere_certified": False,
        "runs": runs, "full_state_grid_differences": differences,
        "nonlinear_one_plus_log_control": control,
        "no_claim": ["rigorous_PDE_error", "genuine_formation", "event_horizon",
                     "final_Bondi_parameters", "critical_endpoint", "full_dispersion"],
    }
    output["source_sha256"] = {
        name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
        for name in ("areal_shift_evolution.py", "polar_evolution.py", "incoming_family.py",
                     "explore_shifted_strong.py")
    }
    target = folder/"SHIFT_STRONG_SCAN_2026-10-16.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"result": str(target), "goal_A_proved": False}), flush=True)


if __name__ == "__main__":
    run()
