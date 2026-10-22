"""Reproducible finite-time amplitude exploration, with no outcome classifier."""
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
from polar_evolution import Configuration, evolve, geometry, propagation_residuals


def run():
    base = Configuration(steps=1024, outer_radius=64., final_time=24.,
                         frequency=0.2)
    experiments = []
    configs = [replace(base, amplitude=a) for a in (0.25, 0.5, 1., 2.)]
    configs += [replace(base, amplitude=2., frequency=f, steps=1280,
                        outer_radius=80., final_time=40.) for f in (0., 0.1, 0.2)]
    for config in configs:
        try:
            r, fields, report = evolve(config)
            g = geometry(r, fields)
            index = int(np.argmin(abs(r-8.)))
            report.update({
                "configuration": asdict(config),
                "central_scalar_absolute_value": float(abs(fields[0, 0])),
                "finite_radius_observation": float(r[index]),
                "Hawking_mass_inside_finite_radius": float(g["mass"][index]),
                "charge_inside_finite_radius": float(g["charge"][index]),
                "independent_propagation_residuals":
                    propagation_residuals(r, fields),
            })
            # This observer is on a spatial slice, not at null infinity.
            report["final_Bondi_mass"] = "UNKNOWN"
            report["final_Bondi_charge"] = "UNKNOWN"
        except ValueError as exc:
            report = {"configuration": asdict(config), "stop_reason": str(exc),
                      "classification": "UNKNOWN_computational_stop"}
            report["stop_context"] = getattr(exc, "context", {})
        experiments.append(report)
    folder = Path(__file__).resolve().parent
    output = {
        "date": "2026-10-16",
        "evidence": "E0_single_grid_finite_time_exploration",
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "goal_A_proved": False, "dispersion_formation_bracket_certified": False,
        "experiments": experiments,
        "scope": "finite_slice_observations_only_not_final_parameters",
        "remaining": ["grid_error_envelope", "horizon_regular_coordinates",
                      "all_future_dispersion", "Bondi_extraction", "exact_extremality"],
    }
    output["source_sha256"] = {
        name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
        for name in ("polar_evolution.py", "incoming_family.py", "explore_polar_family.py")
    }
    target = folder/"FINITE_TIME_SCAN_2026-10-16.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"result": str(target), "samples": len(experiments),
                      "classification": "UNKNOWN_for_all_samples"}))


if __name__ == "__main__":
    run()
