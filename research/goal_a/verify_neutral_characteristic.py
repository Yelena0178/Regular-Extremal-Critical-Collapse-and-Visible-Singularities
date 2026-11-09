"""Manufactured spacetime and centre benchmarks; not PDE error certification."""

from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import numpy as np
from neutral_characteristic import (
    CharacteristicConfiguration, evolve, flat_initial, flat_wave,
    flat_wave_derivative, flrw_exact, flrw_initial, geometry, constraint_residuals)


def main():
    runs = []
    for n in (96, 192, 384):
        cfg = CharacteristicConfiguration(steps=n)
        flat_cfg = replace(cfg, freeze_geometry=True, final_u=4.4)
        flat = evolve(flat_initial, flat_cfg)
        curved = evolve(flrw_initial, cfg)
        errors = {}
        for label, data in (("flat", flat), ("FLRW", curved)):
            maxima = {"r": 0., "S": 0., "phi": 0., "psi": 0., "axis_phi": 0.}
            for i, u in enumerate(data["u"]):
                for j in range(i, n+1):
                    v = data["v"][j]
                    if label == "FLRW":
                        exact = flrw_exact(float(u), float(v))
                    else:
                        scalar = (2*flat_wave_derivative(float(u)) if j == i else
                                  2*(flat_wave(float(v))-flat_wave(float(u)))/(v-u))
                        exact = {"r": (v-u)/2, "S": 0., "phi": scalar}
                    for key in ("r", "S", "phi"):
                        maxima[key] = max(maxima[key], abs(float(data[key][i, j])-exact[key]))
                    maxima["psi"] = max(maxima["psi"], abs(float(data["psi"][i, j])
                                                          -exact["r"]*exact["phi"]))
                    if j == i:
                        maxima["axis_phi"] = max(maxima["axis_phi"],
                                                abs(float(data["phi"][i, j])-exact["phi"]))
            errors[label] = maxima
        i = int(round(2.2/(cfg.outer_v/n)))
        j = int(round(4.7/(cfg.outer_v/n)))
        observed = geometry(curved, i, j) if len(curved["u"]) > i+1 else None
        axis_index = int(round(2./(cfg.outer_v/n)))
        central_geometry = geometry(curved, axis_index-2, axis_index+2, True)
        central_mu = central_geometry["Hawking_mass"]/central_geometry["r"]**3
        constraints = constraint_residuals(curved)
        run = {"configuration": asdict(cfg), "flat_configuration": asdict(flat_cfg),
               "flat_errors": errors["flat"],
               "FLRW_errors": errors["FLRW"], "flat_report": flat["report"],
               "FLRW_report": curved["report"], "FLRW_trapped_sample": observed,
               "heldout_constraints": constraints, "central_mu_at_t2": central_mu,
               "central_mu_exact": 1/16}
        runs.append(run)
        print(json.dumps({"n": n, "flat": errors["flat"], "FLRW": errors["FLRW"],
                          "stop": curved["report"]["stop_reason"],
                          "sample": observed, "constraints": constraints,
                          "central_mu": central_mu}), flush=True)
    for run in runs:
        if run["FLRW_report"]["stop_reason"] or run["flat_report"]["stop_reason"]:
            raise ArithmeticError("manufactured evolution stopped early")
        if run["flat_errors"]["psi"] > 1e-10 or run["flat_errors"]["r"] > 1e-12:
            raise ArithmeticError("analytic flat-wave comparison")
        if not (run["FLRW_trapped_sample"]["theta_out"] < 0
                and run["FLRW_trapped_sample"]["theta_in"] < 0):
            raise ArithmeticError("known FLRW trapped sample was missed")
    for coarse, fine in zip(runs, runs[1:]):
        for key in ("r", "S", "phi"):
            if fine["FLRW_errors"][key] >= coarse["FLRW_errors"][key]/2.5:
                raise ArithmeticError("manufactured field errors fail to decrease")
        if fine["flat_errors"]["axis_phi"] >= coarse["flat_errors"]["axis_phi"]/8:
            raise ArithmeticError("flat centre pulse crossing accuracy")
        if abs(fine["central_mu_at_t2"]-1/16) >= abs(coarse["central_mu_at_t2"]-1/16)/1.2:
            raise ArithmeticError("central Hawking-mass coefficient fails to converge")
        for key in ("u_constraint", "v_constraint"):
            if fine["heldout_constraints"][key] >= coarse["heldout_constraints"][key]/2:
                raise ArithmeticError("held-out null constraints fail to decrease")
    if abs(runs[-1]["central_mu_at_t2"]-1/16) >= 1e-4:
        raise ArithmeticError("central mass coefficient is inaccurate")
    # Preserve the rejected fixed-axis/geometric-lapse variant as a failed
    # control. Its pointwise fields can look convergent while m/r^3 is biased.
    controls = []
    for n in (96, 192):
        bad_cfg = CharacteristicConfiguration(steps=n, centre_cells=4,
                                             arithmetic_omega2_average=False)
        data = evolve(flrw_initial, bad_cfg)
        k = round(2./(bad_cfg.outer_v/n))
        g = geometry(data, k-2, k+2, True)
        value = g["Hawking_mass"]/g["r"]**3
        controls.append({"steps": n, "central_mu": value, "exact": 1/16})
    if abs(controls[-1]["central_mu"]-1/16) < .001:
        raise ArithmeticError("failed axis variant was not rejected")
    folder = Path(__file__).resolve().parent
    result = {"evidence": "E0_manufactured_characteristic_benchmarks", "runs": runs,
              "rejected_axis_variant": controls,
              "goal_A_proved": False, "rigorous_PDE_error": False}
    result["source_sha256"] = {
        name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
        for name in ("neutral_characteristic.py", "verify_neutral_characteristic.py")}
    target = folder/"NEUTRAL_CHARACTERISTIC_RESULTS_2026-10-16.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
