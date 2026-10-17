"""Centre-normalized neutral onset of the candidate's early outgoing cone."""

from dataclasses import dataclass
import json
import math
from pathlib import Path
from scipy.integrate import solve_ivp


def smooth_step(x):
    if x <= 0:
        return 0., 0.
    if x >= 1:
        return 1., 0.
    exponent = 1/x-1/(1-x)
    if exponent > 700:
        return 0., 0.
    if exponent < -700:
        return 1., 0.
    value = 1/(1+math.exp(exponent))
    return value, value*(1-value)*(1/x**2+1/(1-x)**2)


@dataclass(frozen=True)
class NeutralOnset:
    radius: float = 5.
    coupling: float = .6
    field_amplitude: float = .5
    smoothing_fraction: float = .05
    radius_ratio: float | None = None
    s_override: float | None = None
    cap_radius_override: float | None = None
    affine_width_override: float | None = None
    input_reference: str = "centre_normalized_C0_auxiliary_limit"

    @classmethod
    def from_first_jet_report(cls, smoothing_fraction=.05):
        folder = Path(__file__).resolve().parent
        report = json.loads((folder/"FIRST_JET_CHECKS_2026-10-16.json").read_text(encoding="utf-8"))
        run = report["runs"][-1]
        cfg = run["configuration"]
        if cfg["coupling"] != .6 or cfg["radius"] != 5. or cfg["amplitude"] != .5:
            raise ValueError("unexpected frozen first-jet input")
        s, beta = run["parameters"]["s"], cfg["beta"]
        v2 = s/(s+.5*math.tan(.5))
        v1 = v2*.5**(1/s)
        width = beta*run["centre_normalized_affine_window_length_0_1"]*v1
        return cls(smoothing_fraction=smoothing_fraction, s_override=s,
                   cap_radius_override=run["r_initial"], affine_width_override=width,
                   input_reference="FIRST_JET_CHECKS last run: beta=0.003, C0 early segment")

    def parameters(self):
        phi = self.field_amplitude
        ratio = phi if self.radius_ratio is None else self.radius_ratio
        if not 0 < ratio < 1:
            raise ValueError("require 0 < radius_ratio < 1")
        K = phi*math.cos(phi)**2*(1-ratio*ratio)/2
        if self.coupling != .6:
            raise ValueError("this screening fixes e=3/5")
        eR_squared_K2 = (self.coupling*self.radius*K)**2
        s = (eR_squared_K2/(1+eR_squared_K2) if self.s_override is None else self.s_override)
        r0 = (self.radius*ratio*math.cos(phi)*(math.cos(phi)-s/phi*math.sin(phi))
              if self.cap_radius_override is None else self.cap_radius_override)
        affine_width = (self.radius*ratio*math.cos(phi)
                        *(phi*math.sin(phi)+s*math.cos(phi))
                        if self.affine_width_override is None else self.affine_width_override)
        budget = None
        if self.s_override is None and self.cap_radius_override is None:
            tau = math.tan(phi)
            v2 = s/(s+phi*tau)
            t = ratio**(1/s)
            a = ratio*ratio
            power = 1-2*s
            third = a*a*(-math.log(t) if abs(power) < 1e-12 else
                         -math.expm1(power*math.log(t))/power)
            primitive = (1-a*t)/(1+2*s)-2*a*(1-t)+third
            h0 = s*t*(1-s*tau/phi)/(s+phi*tau)**2
            total = v2*primitive/(math.cos(phi)**2*(1-a)**2)+(1-v2)*tau/phi
            budget = {"H0": h0, "H1": h0+1-total,
                      "evidence": "E0_C0_closed_form_only"}
        return {"s_C0": s, "r_cap": r0, "v_cap": 2*r0,
                "v_onset_width": 2*affine_width,
                "v_end": 2*(r0+affine_width),
                "field_amplitude": phi, "smoothing_fraction": self.smoothing_fraction,
                "radius_ratio": ratio,
                "fixed_coupling": self.coupling, "target_radius": self.radius,
                "input_reference": self.input_reference,
                "outer_null_constraint_budget_C0": budget}

    def make_initial(self):
        p = self.parameters()
        start, length, end = p["v_cap"], p["v_onset_width"], p["v_end"]
        phi, epsilon = self.field_amplitude, self.smoothing_fraction
        if not 0 <= epsilon < .5:
            raise ValueError("invalid onset smoothing fraction")

        def field(v):
            if v <= start:
                return 0., 0.
            x = (v-start)/length
            if epsilon == 0 or x >= epsilon:
                return phi*x, phi/length
            chi, chip = smooth_step(x/epsilon)
            return phi*x*chi, phi/length*(chi+x/epsilon*chip)

        def radial_rhs(v, state):
            _, derivative = field(v)
            return (state[1], -state[0]*derivative*derivative)

        radius = solve_ivp(radial_rhs, (start, end), (p["r_cap"], .5),
                           method="DOP853", rtol=2e-12, atol=2e-14,
                           max_step=length/256, dense_output=True)
        if not radius.success or min(radius.y[0]) <= 0:
            raise ValueError("initial Raychaudhuri integration failed")
        p["endpoint_area_radius_numeric"] = float(radius.y[0, -1])
        p["endpoint_outgoing_derivative_numeric"] = float(radius.y[1, -1])

        def initial(v):
            if v <= start:
                return v/2, 0., 0.
            rr = float(radius.sol(v)[0])
            return rr, 0., field(v)[0]

        return initial, p
