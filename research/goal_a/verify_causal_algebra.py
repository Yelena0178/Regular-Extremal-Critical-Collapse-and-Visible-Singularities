"""Exact finite algebra for A-GEO01/A-RET01, not a PDE certificate.

Run from any directory; uses only Python's standard library.
Checks use explicit exceptions so that python -O retains every check.
"""

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


NAMES = ("r", "m", "M", "Q", "kappa", "ell2", "Omega2", "scalar_focusing")
ZERO = (0,) * len(NAMES)


class Laurent:
    """Sparse multivariate Laurent polynomials over the rational numbers."""

    def __init__(self, terms=None):
        self.terms = {e: F(c) for e, c in (terms or {}).items() if c}

    @staticmethod
    def lift(value):
        if isinstance(value, Laurent):
            return value
        return Laurent({ZERO: F(value)})

    def __add__(self, other):
        terms = dict(self.terms)
        for exponent, coefficient in self.lift(other).terms.items():
            terms[exponent] = terms.get(exponent, F(0)) + coefficient
        return Laurent(terms)

    __radd__ = __add__

    def __neg__(self):
        return Laurent({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + -self.lift(other)

    def __rsub__(self, other):
        return self.lift(other) + -self

    def __mul__(self, other):
        terms = {}
        for left, a in self.terms.items():
            for right, b in self.lift(other).terms.items():
                exponent = tuple(x + y for x, y in zip(left, right))
                terms[exponent] = terms.get(exponent, F(0)) + a * b
        return Laurent(terms)

    __rmul__ = __mul__

    def __pow__(self, power):
        if not isinstance(power, int):
            raise TypeError("Only integer powers are used")
        if power < 0:
            if len(self.terms) != 1:
                raise ValueError("Negative power requires a nonzero monomial")
            (exponent, coefficient), = self.terms.items()
            return Laurent({tuple(power * x for x in exponent): coefficient**power})
        result = self.lift(1)
        for _ in range(power):
            result = result * self
        return result

    def __truediv__(self, other):
        return self * self.lift(other)**-1

    def derivative(self, name):
        index = NAMES.index(name)
        terms = {}
        for exponent, coefficient in self.terms.items():
            if exponent[index]:
                result = list(exponent)
                result[index] -= 1
                key = tuple(result)
                terms[key] = terms.get(key, F(0)) + coefficient * exponent[index]
        return Laurent(terms)

    def substitute(self, **replacements):
        result = self.lift(0)
        for exponent, coefficient in self.terms.items():
            term = self.lift(coefficient)
            for name, power in zip(NAMES, exponent):
                if power:
                    term = term * replacements.get(name, symbol(name))**power
            result = result + term
        return result


def symbol(name):
    exponent = list(ZERO)
    exponent[NAMES.index(name)] = 1
    return Laurent({tuple(exponent): F(1)})


def require_equal(left, right, message):
    difference = Laurent.lift(left) - right
    if difference.terms:
        raise ArithmeticError(message + ": nonzero Laurent polynomial")


def require_different(left, right, message):
    if not (Laurent.lift(left) - right).terms:
        raise ArithmeticError(message + ": negative control was accepted")


def checks():
    r, m, mass, charge, kappa, ell2, omega2, focusing = map(symbol, NAMES)
    results = []

    # Double-null Hessian plus the angular warped-product term. The scalar
    # focusing variable is nonnegative analytically but algebraically free.
    r_uv = -omega2 * m / (2 * r**2) + omega2 * charge**2 / (4 * r**3)
    orbit_uv_product = (kappa + ell2 / r**2) / omega2
    direct_hessian = (
        -r * focusing + 2 * r_uv * orbit_uv_product
        + (1 - 2 * m / r) * ell2 / r**3
    )
    formula = (
        -r * focusing - kappa * m / r**2 + kappa * charge**2 / (2 * r**3)
        + ell2 / r**3 * (1 - 3 * m / r + charge**2 / (2 * r**2))
    )
    require_equal(direct_hessian, formula, "double-null and angular composition")
    results.append("exact_double_null_angular_composition")

    # Independent first integral in static RN: rdot^2 = E^2 - V_eff.
    metric_f = 1 - 2 * mass / r + charge**2 / r**2
    effective_potential = metric_f * (kappa + ell2 / r**2)
    rn_from_potential = -F(1, 2) * effective_potential.derivative("r")
    rn_from_hessian = formula.substitute(
        m=mass - charge**2 / (2 * r), scalar_focusing=Laurent.lift(0)
    )
    require_equal(rn_from_hessian, rn_from_potential, "independent RN effective potential")
    results.append("exact_RN_effective_potential_identity")
    require_equal(
        rn_from_potential.substitute(ell2=Laurent.lift(0), kappa=Laurent.lift(1)),
        -mass / r**2 + charge**2 / r**3,
        "radial RN timelike acceleration",
    )
    require_equal(
        rn_from_potential.substitute(ell2=Laurent.lift(0), kappa=Laurent.lift(0)),
        0,
        "radial RN affine null acceleration",
    )
    require_equal(
        rn_from_potential.substitute(
            Q=Laurent.lift(0), kappa=Laurent.lift(0), r=3 * mass
        ),
        0,
        "Schwarzschild photon sphere radius",
    )
    results.extend(("radial_timelike_RN", "radial_null_RN", "Schwarzschild_photon_sphere"))

    wrong_mass = formula.substitute(m=mass, scalar_focusing=Laurent.lift(0))
    require_different(wrong_mass, rn_from_potential, "Hawking mass replaced by RN M")
    wrong_charge = (
        -r * focusing - kappa * m / r**2
        + ell2 / r**3 * (1 - 3 * m / r)
    )
    require_different(wrong_charge, direct_hessian, "electromagnetic terms omitted")
    results.extend(("reject_wrong_mass_identity", "reject_missing_electromagnetic_terms"))

    # Finite-interval integration by parts in the polynomial class Q=sum a_i r^i.
    # The boundary term at R is retained. This checks its sign independently
    # of the inequality argument, which is supplied in the analytic document.
    for coefficients in ({3: F(1)}, {3: F(2), 5: F(-3), 7: F(1, 4)}):
        q = sum((coefficient * r**power for power, coefficient in coefficients.items()),
                Laurent.lift(0))
        require_equal(
            (q**2 / r).derivative("r"),
            2 * q * q.derivative("r") / r - q**2 / r**2,
            "finite-interval Hardy boundary sign",
        )
    results.append("Hardy_integration_by_parts_boundary_sign")

    s, s0, gamma, mu, delta = F(2, 3), F(5, 4), F(3, 4), F(1, 10), F(1, 100)
    margins = (
        1 - 2 * mu, s - F(1, 2), 1 - s,
        gamma - F(1, 2), 1 - gamma, 1 + gamma - 2 * s,
    )
    if not (F(1, 2) < s < 1 < s0 < F(3, 2)
            and s0 == gamma + F(1, 2) and 4 * delta < min(margins)
            and mu < 1 - gamma):
        raise ArithmeticError("source exponent restrictions")
    tails = {
        "charge": 1 - 2 * s,
        "scalar_energy": -2 * s,
        "electromagnetic_energy": 1 - 4 * s,
    }
    if any(exponent >= 0 for exponent in tails.values()):
        raise ArithmeticError("retarded bounds fail to decay")
    results.append("strict_source_exponents_and_retarded_decay")
    return {
        "checks_passed": results,
        "source_parameters": {
            "s": str(s), "s0": str(s0), "gamma": str(gamma),
            "mu": str(mu), "delta_upper_bound": str(delta),
            "four_delta": str(4 * delta), "minimum_required_margin": str(min(margins)),
        },
        "retarded_power_exponents": {key: str(value) for key, value in tails.items()},
    }


def main():
    folder = Path(__file__).resolve().parent
    report = {
        "scope": "exact finite algebra only; not an analytic or PDE certificate",
        "arithmetic": "fractions.Fraction sparse Laurent polynomials",
        **checks(),
    }
    names = (
        "CAUSAL_COMPLETENESS.md", "RETARDED_CAUCHY_BOUNDS.md",
        "KL_INTERFACE_AUDIT.md", Path(__file__).name,
    )
    report["source_sha256"] = {
        name: sha256((folder / name).read_bytes()).hexdigest() for name in names
    }
    output = folder / "CAUSAL_ALGEBRA_RESULTS_2026-10-16.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "passed": len(report["checks_passed"]),
        "scope": report["scope"],
        "report": output.name,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
