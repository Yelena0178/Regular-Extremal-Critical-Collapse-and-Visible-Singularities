"""Rational interval certificate for A-HOR01's null-constraint seed.

The certificate proves only the finite interval inequalities used by the
analytic smoothing argument. A separate floating-point first-jet diagnostic
is explicitly not an interval or spacetime certificate.
"""

from fractions import Fraction as F
from hashlib import sha256
import cmath
import json
import math
from pathlib import Path


DEN = 1 << 192


def down(value):
    scaled = value * DEN
    return F(scaled.numerator // scaled.denominator, DEN)


def up(value):
    return -down(-value)


class I:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = F(lo), F(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def lift(value):
        return value if isinstance(value, I) else I(value)

    def __add__(self, other):
        other = self.lift(other)
        return I(down(self.lo + other.lo), up(self.hi + other.hi))

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -self.lift(other)

    def __rsub__(self, other):
        return self.lift(other) + -self

    def __mul__(self, other):
        other = self.lift(other)
        values = (self.lo * other.lo, self.lo * other.hi,
                  self.hi * other.lo, self.hi * other.hi)
        return I(down(min(values)), up(max(values)))

    __rmul__ = __mul__

    def reciprocal(self):
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        return I(down(1 / self.hi), up(1 / self.lo))

    def __truediv__(self, other):
        return self * self.lift(other).reciprocal()

    def __rtruediv__(self, other):
        return self.lift(other) * self.reciprocal()

    def __pow__(self, exponent):
        if exponent < 0:
            return self.reciprocal()**-exponent
        result = I(1)
        for _ in range(exponent):
            result = result * self
        return result


def trig_half():
    x = F(1, 2)
    cosine = sum(((-1)**n * x**(2*n) / math.factorial(2*n) for n in range(21)), F(0))
    sine = sum(((-1)**n * x**(2*n+1) / math.factorial(2*n+1) for n in range(21)), F(0))
    cr = x**42 / math.factorial(42)
    sr = x**43 / math.factorial(43)
    return I(down(cosine-cr), up(cosine+cr)), I(down(sine-sr), up(sine+sr))


def log_two():
    count = 48
    lower = 2 * sum((F(1, (2*n+1)*3**(2*n+1)) for n in range(count)), F(0))
    tail = F(9, 4) * F(1, (2*count+1)*3**(2*count+1))
    return I(down(lower), up(lower+tail))


def exp_positive(x):
    if not (0 <= x.lo <= x.hi <= 5):
        raise ValueError("exp certificate is restricted to [0,5]")
    order = 72
    term, total = I(1), I(1)
    for k in range(1, order+1):
        term = term * x / k
        total = total + term
    # Each successive positive term after order+1 has ratio <=5/(order+2).
    tail = F(5)**(order+1) / math.factorial(order+1) / (1-F(5, order+2))
    return I(total.lo, up(total.hi+tail))


def seed_bounds(s, cosine, sine, ln2):
    phi = F(1, 2)
    a = phi**2
    tau = sine / cosine
    t = exp_positive(ln2 / s).reciprocal()
    v2 = s / (s + phi*tau)
    h0 = s*t*(1-s*tau/phi) / (s+phi*tau)**2
    middle_primitive = (
        1/(1+2*s) - 2*a + a*a/(1-2*s)
        - 8*a*s*s*t/(1-4*s*s)
    )
    charge_integral = v2*middle_primitive / (cosine**2 * (1-a)**2)
    off_integral = (1-v2)*tau/phi
    h1 = h0 + 1 - charge_integral - off_integral
    k2 = (phi*cosine**2*(1-a)/2)**2 * (1-s)/s
    return {"H0": h0, "H1": h1, "k_squared": k2}


def interval_certificate():
    product = I(-3, -2)*I(-5, 7)
    if not (product.lo <= -21 and product.hi >= 15):
        raise ArithmeticError("signed interval product enclosure")
    try:
        I(-1, 1).reciprocal()
    except ZeroDivisionError:
        pass
    else:
        raise ArithmeticError("zero-containing inverse was accepted")
    cosine, sine = trig_half()
    ln2 = log_two()
    count = 256
    left, right = F(3, 20), F(17, 100)
    minimum_h0, minimum_h1 = None, None
    cells = []
    for j in range(count):
        low = left + (right-left)*F(j, count)
        high = left + (right-left)*F(j+1, count)
        bounds = seed_bounds(I(low, high), cosine, sine, ln2)
        h0, h1 = bounds["H0"].lo, bounds["H1"].lo
        if not (h0 > F(1, 1024) and h1 > F(1, 1024)):
            raise ArithmeticError(f"constraint margin failed in cell {j}")
        minimum_h0 = h0 if minimum_h0 is None else min(minimum_h0, h0)
        minimum_h1 = h1 if minimum_h1 is None else min(minimum_h1, h1)
        # Compact certificate: lower bounds rounded down to 20 binary places.
        lower_dyadic = lambda x: F((x*(1 << 20)).numerator // (x*(1 << 20)).denominator, 1 << 20)
        cells.append([str(low), str(high), str(lower_dyadic(h0)), str(lower_dyadic(h1))])
    low_charge = seed_bounds(I(left), cosine, sine, ln2)["k_squared"]
    high_charge = seed_bounds(I(right), cosine, sine, ln2)["k_squared"]
    if not low_charge.lo > (F(1, 3)+F(1, 256))**2:
        raise ArithmeticError("lower-s positive charge bracket")
    if not high_charge.hi < (F(1, 3)-F(1, 256))**2:
        raise ArithmeticError("upper-s negative charge bracket")
    all_charge = seed_bounds(I(left, right), cosine, sine, ln2)["k_squared"]
    if not (all_charge.lo > F(1, 16) and all_charge.hi < F(1, 4)):
        raise ArithmeticError("uniform normalized charge range")
    if not (cosine.lo > F(7, 8) and sine.hi < F(1, 2)):
        raise ArithmeticError("elementary trigonometric bounds")
    rejected = seed_bounds(I(F(7, 50)), cosine, sine, ln2)["H1"]
    if not rejected.hi < 0:
        raise ArithmeticError("known failed incoming-expansion control was not rejected")

    # Exact conservative implications used in the smoothing proof.
    smoothing_width = F(1, 1 << 160)
    sqrt_width = F(1, 1 << 80)
    derivative_error = 30 * 512 * sqrt_width
    if not derivative_error < F(1, 1 << 66):
        raise ArithmeticError("H1 smoothing error")
    potential_error = (1024+derivative_error)*derivative_error
    if not potential_error < F(1, 1 << 55):
        raise ArithmeticError("Raychaudhuri coefficient error")
    if not 16*potential_error < F(1, 1 << 51):
        raise ArithmeticError("relative-radius Volterra contraction")
    return {
        "arithmetic": "Fraction intervals; outward rounding at 192 binary places",
        "elementary_functions": "rational Taylor bounds with explicit remainder",
        "s_interval": [str(left), str(right)],
        "partition_cells": count,
        "minimum_H0_lower_bound": str(minimum_h0),
        "minimum_H1_lower_bound": str(minimum_h1),
        "uniform_constraint_margin_proved": "1/1024",
        "charge_endpoint_margin_proved": "1/256",
        "normalized_charge_range_proved": "1/4 < k(s) < 1/2",
        "negative_control": {"s": "7/50", "H1_upper_bound": str(rejected.hi),
                             "accepted_as_legal_seed": False},
        "smoothing_width": str(smoothing_width),
        "smoothing_derivative_L2_error_upper_bound": str(derivative_error),
        "potential_L1_error_upper_bound": str(potential_error),
        "smoothed_constraint_margin_from_analysis": "greater than 1/2048",
        "partition_lower_bound_certificate": cells,
    }


def baseline_profile(s, v):
    """C0 baseline only; this does not resolve the smooth transition layers."""
    phi, radius, coupling = .5, 5., .6
    alpha = math.atan(s/phi)
    tau = math.tan(phi)
    v2 = s/(s+phi*tau)
    t = phi**(1/s)
    v1 = v2*t
    lam = math.sqrt(s*(1-s))/phi
    h0 = s*t*(1-s*tau/phi)/(s+phi*tau)**2
    a = phi*phi
    factor = v2/(math.cos(phi)**2*(1-a)**2)

    def middle_integral(y):
        return factor * (
            (y**(1+2*s)-t**(1+2*s))/(1+2*s)
            - 2*a*(y-t) + a*a*(y**(1-2*s)-t**(1-2*s))/(1-2*s)
        )

    if v < v1:
        angle = phi*(1-v/v1)+alpha
        f = math.cos(phi)/math.cos(alpha)*phi*math.cos(angle)
        fv = math.cos(phi)/math.cos(alpha)*phi*phi/v1*math.sin(angle)
        field = phi*cmath.exp(-1j*lam*math.log(v1))*v/v1
        q, integral = 0., 0.
    elif v <= v2:
        y = v/v2
        f, fv = math.cos(phi)*y**s, math.cos(phi)*s*y**s/v
        field = phi*cmath.exp(-1j*lam*math.log(v))
        q = (y**(2*s)-a)/(1-a)
        integral = middle_integral(y)
    else:
        angle = phi*(1-v)/(1-v2)
        f, fv = math.cos(angle), phi/(1-v2)*math.sin(angle)
        field = phi*cmath.exp(-1j*lam*math.log(v2))*(1-v)/(1-v2)
        q = 1.
        integral = middle_integral(1.)+(1-v2)/phi*(tau-math.tan(angle))
    h = h0+v-integral
    nu = -h/(4*radius*f)
    nu_v = -nu*fv/f - (1-q*q/(f*f))/(4*radius*f)
    # D001 wave equation: (r D_u phi)' = -nu phi' - i e Q phi/(4r).
    # After integration by parts, phi=0 at both endpoints:
    kernel = nu_v - 1j*coupling*q/(4*f)
    return kernel*field


def simpson_complex(function, count):
    if count % 2:
        raise ValueError("even Simpson grid required")
    total = function(0.) + function(1.)
    for j in range(1, count):
        total += (4 if j % 2 else 2)*function(j/count)
    return total/(3*count)


def first_jet_diagnostic():
    phi = .5
    K = phi*math.cos(phi)**2*(1-phi**2)/2
    s = 9*K*K/(1+9*K*K)
    v2 = s/(s+phi*math.tan(phi))
    v1 = v2*phi**(1/s)
    log_ratio = math.log(v2/v1)
    radius = 5.
    centre_width = radius*(phi*phi*math.cos(phi)*math.sin(phi)
                           + phi*s*math.cos(phi)**2)
    r_on = radius*phi*math.cos(phi)
    h0_over_v1 = (1-s*math.tan(phi)/phi)/(s+phi*math.tan(phi))
    m_on = r_on*(1-s*(1+h0_over_v1))/2
    values = []
    for count in (1024, 2048, 4096):
        on = simpson_complex(lambda x: baseline_profile(s, v1*x)*v1, count)
        middle = simpson_complex(
            lambda x: baseline_profile(s, v1*math.exp(log_ratio*x))
            * v1*math.exp(log_ratio*x)*log_ratio, count)
        off = simpson_complex(
            lambda x: baseline_profile(s, v2+(1-v2)*x)*(1-v2), count)
        value = (on+middle+off)/5.
        values.append({"steps_per_piece": count, "Du_phi_at_end_real": value.real,
                       "Du_phi_at_end_imag": value.imag, "modulus": abs(value)})
    return {
        "evidence": "E0_float_C0_baseline_only",
        "s_C0": s, "v1_C0": v1, "v2_C0": v2,
        "centre_normalized_turn_on_budget_C0": {
            "affine_width": centre_width,
            "endpoint_area_radius": r_on,
            "endpoint_Hawking_mass": m_on,
            "mass_over_affine_width": m_on/centre_width,
            "endpoint_charge": 0.,
            "scope": "finite C0 segment budget; not an applicable trapping theorem",
        },
        "runs": values,
        "no_claim": ["interval_error", "smooth_root_value", "smooth_layer_resolution",
                     "RN_jet_matching", "regular_centre_future", "criticality"],
    }


def linearized_RN_jet_test():
    radius, charge, mass_h, coupling = F(5), F(5), F(5, 2), F(3, 5)
    real_kernel = 2*mass_h/radius**2-charge**2/radius**3
    response = -coupling*charge/(4*radius**2)
    if not (real_kernel == 0 and response == F(-3, 100)):
        raise ArithmeticError("linearized RN transverse-jet consistency test")
    return {
        "arithmetic": "exact Fraction",
        "real_mass_kernel": str(real_kernel),
        "Du_phi_linear_response_imaginary_coefficient": str(response),
        "multiplies": "epsilon times integral of a nonnegative nonzero smooth bump",
        "scope": "local linearized compatibility; not a global collapse counterexample",
    }


def main():
    folder = Path(__file__).resolve().parent
    result = {
        "scope": "null-constraint seed and finite rational inequalities; not goal A",
        "coupling": "3/5", "fixed_endpoint_area_radius": "5",
        "analytic_smoothing_existence_argument": "SMOOTH_HORIZON_CONSTRAINT_SEED.md",
        "interval_certificate": interval_certificate(),
        "linearized_RN_first_jet_test": linearized_RN_jet_test(),
        "first_transverse_jet_diagnostic": first_jet_diagnostic(),
    }
    names = ("SMOOTH_HORIZON_CONSTRAINT_SEED.md", "SCHNEIDER_2026_INTERFACE_AUDIT.md",
             Path(__file__).name)
    result["source_sha256"] = {
        name: sha256((folder/name).read_bytes()).hexdigest() for name in names
    }
    output = folder/"HORIZON_SEED_RESULTS_2026-10-16.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({
        "partition_cells": result["interval_certificate"]["partition_cells"],
        "constraint_margin": result["interval_certificate"]["uniform_constraint_margin_proved"],
        "numeric_first_jet_modulus": result["first_transverse_jet_diagnostic"]["runs"][-1]["modulus"],
        "scope": result["scope"], "report": output.name,
    }))


if __name__ == "__main__":
    main()
