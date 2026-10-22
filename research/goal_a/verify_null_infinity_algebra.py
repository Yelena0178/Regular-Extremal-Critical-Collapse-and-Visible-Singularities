"""Finite exact algebra for A-NULL01; no PDE or global geometry certification."""

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


class P:
    """Sparse Laurent polynomials with rational coefficients and i**2 = -1."""

    def __init__(self, terms=None):
        canonical = {}
        for monomial, coefficient in (terms or {}).items():
            powers = {}
            for name, power in monomial:
                powers[name] = powers.get(name, 0) + power
            imaginary_power = powers.pop("i", 0) % 4
            if imaginary_power >= 2:
                coefficient = -coefficient
            if imaginary_power % 2:
                powers["i"] = 1
            key = tuple(sorted((name, power) for name, power in powers.items() if power))
            canonical[key] = canonical.get(key, F(0)) + F(coefficient)
        self.terms = {key: value for key, value in canonical.items() if value}

    @staticmethod
    def lift(value):
        return value if isinstance(value, P) else P({(): F(value)})

    def __add__(self, other):
        terms = dict(self.terms)
        for key, value in self.lift(other).terms.items():
            terms[key] = terms.get(key, F(0)) + value
        return P(terms)

    __radd__ = __add__

    def __neg__(self):
        return P({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + -self.lift(other)

    def __rsub__(self, other):
        return self.lift(other) + -self

    def __mul__(self, other):
        terms = {}
        for left, a in self.terms.items():
            for right, b in self.lift(other).terms.items():
                key = left + right
                terms[key] = terms.get(key, F(0)) + a * b
        return P(terms)

    __rmul__ = __mul__

    def __pow__(self, power):
        if not isinstance(power, int):
            raise TypeError("integer powers only")
        if power < 0:
            if len(self.terms) != 1:
                raise ValueError("only monomials may have negative powers")
            (key, value), = self.terms.items()
            return P({tuple((name, exponent * power) for name, exponent in key): value**power})
        result = self.lift(1)
        for _ in range(power):
            result = result * self
        return result

    def __truediv__(self, other):
        return self * self.lift(other)**-1

    def partial(self, variable):
        result = P()
        for key, value in self.terms.items():
            powers = dict(key)
            exponent = powers.get(variable, 0)
            if exponent:
                powers[variable] -= 1
                result = result + P({tuple(powers.items()): value * exponent})
        return result

    def total(self, derivatives):
        return sum((self.partial(name) * value for name, value in derivatives.items()), P())

    def substitute(self, replacements):
        result = P()
        for key, value in self.terms.items():
            term = self.lift(value)
            for name, power in key:
                term = term * replacements.get(name, sym(name))**power
            result = result + term
        return result

    def conjugate(self):
        pairs = {
            "psi": "psib", "psib": "psi", "h": "hb", "hb": "h",
            "v": "vb", "vb": "v", "hr": "hrb", "hrb": "hr",
        }
        result = P()
        for key, value in self.terms.items():
            sign = -1 if dict(key).get("i", 0) else 1
            transformed = tuple((pairs.get(name, name), power) for name, power in key)
            result = result + P({transformed: sign * value})
        return result


def sym(name):
    return P({((name, 1),): F(1)})


def imag(value):
    return -sym("i") * (value - value.conjugate()) / 2


def equal(left, right, label):
    if (P.lift(left) - right).terms:
        raise ArithmeticError("failed exact identity: " + label)


def different(left, right, label):
    if not (P.lift(left) - right).terms:
        raise ArithmeticError("negative control was accepted: " + label)


def checks():
    names = ("r", "G", "b", "m", "Q", "e", "psi", "psib", "h", "hb",
             "v", "vb", "hr", "hrb", "hu", "br", "Au", "Aur", "i")
    r, G, b, m, Q, e, psi, psib, h, hb, v, vb, hr, hrb, hu, br, Au, Aur, i = map(sym, names)
    passed = []

    # The two radial Einstein equations, with complex fields algebraically free.
    D = 1 - 2 * m / r
    radial_norm = (h - psi / r) * (hb - psib / r)
    G_r = G * radial_norm / r
    m_r = D * radial_norm / 2 + Q**2 / (2 * r**2)
    b_r_from_constraints = G_r * D + G * (-2 * m_r / r + 2 * m / r**2)
    b_r_geometric = G * (2 * m / r**2 - Q**2 / r**3)
    equal(b_r_from_constraints, b_r_geometric, "radial scalar energy cancellation")
    passed.append("exact_radial_Einstein_scalar_cancellation")
    different(
        G_r * D + G * (-2 * (D * radial_norm / 2) / r + 2 * m / r**2),
        b_r_geometric, "missing radial electric energy",
    )
    passed.append("reject_missing_radial_electric_energy")

    # Expand the divergence-form charged wave operator before simplifying.
    # v = D_u psi, whereas hu is the ordinary partial_u h.
    phi = psi / r
    phi_r = h / r - psi / r**2
    phi_rr = hr / r - 2 * h / r**2 + 2 * psi / r**3
    psi_u = v - i * e * Au * psi
    phi_u = psi_u / r
    phi_ur = hu / r - psi_u / r**2
    divergence_wave = (
        -2 * r**2 * phi_ur - 2 * r * phi_u
        - i * e * (2 * r**2 * Au * phi_r + 2 * r * Au * phi + r**2 * Aur * phi)
        + (2 * r * b + r**2 * br) * phi_r + r**2 * b * phi_rr
    )
    h_rhs = b * hr / 2 + (br / 2 - i * e * Au) * h + (-br / (2 * r) - i * e * Aur / 2) * psi
    equal(divergence_wave / (-2 * r), hu - h_rhs, "charged wave transport")
    passed.append("independent_divergence_wave_transport")
    different(
        hu - (b * hr / 2 + (br / 2 - i * e * Au) * h - br * psi / (2 * r)),
        divergence_wave / (-2 * r), "omitted potential-gradient commutator",
    )
    passed.append("reject_omitted_charged_commutator")
    # Apply the D001 orientation Aur = -G Q/r^2.
    oriented_rhs = b * hr / 2 + (br / 2 - i * e * Au) * h + (-br / (2 * r) + i * e * G * Q / (2 * r**2)) * psi
    equal(
        h_rhs.substitute({"Aur": -G * Q / r**2}), oriented_rhs,
        "potential gradient orientation",
    )
    different(
        h_rhs.substitute({"Aur": G * Q / r**2}), oriented_rhs,
        "wrong sign of potential gradient",
    )
    passed.append("D001_potential_gradient_orientation")
    passed.append("reject_wrong_potential_gradient_sign")

    # Independently differentiate the Gauss and temporal Maxwell currents,
    # using the charged wave transport and the covariant derivative commutator.
    Q_r = e * imag(psi * hb)
    Q_u = -e * imag(psi * vb) + b * Q_r
    v_r = h_rhs + i * e * Au * h + i * e * Aur * psi
    du = {
        "psi": psi_u, "psib": psi_u.conjugate(),
        "h": h_rhs, "hb": h_rhs.conjugate(),
    }
    dr = {
        "r": P.lift(1), "psi": h, "psib": hb, "h": hr, "hb": hrb,
        "v": v_r, "vb": v_r.conjugate(), "b": br,
    }
    equal(Q_r.total(du), Q_u.total(dr), "Maxwell compatibility from charged wave")
    passed.append("independent_Maxwell_Gauss_time_compatibility")
    different(Q_r.total(du), (-e * imag(psi * vb)).total(dr), "omitted Maxwell advection")
    passed.append("reject_omitted_Maxwell_advection")

    # Independent mixed stress component r^2 T_u^r, with the inverse Bondi
    # metric applied before rewriting phi=psi/r. The electric mixed component
    # is zero in spherical symmetry.
    stress_product = (v / r) * (-vb / (G * r) + b * (hb / r - psib / r**2) / G)
    mixed_stress = r**2 * (stress_product + stress_product.conjugate()) / 2
    radiation_cross = v * (hb - psib / r)
    mass_flux = -v * vb / G + b * (radiation_cross + radiation_cross.conjugate()) / (2 * G)
    equal(mixed_stress, mass_flux, "Bondi mass flux from mixed stress tensor")
    passed.append("independent_mixed_stress_mass_flux")

    # An independent electrovac specialization: RN radial f'(r).
    mass = sym("M")
    rn_f = 1 - 2 * mass / r + Q**2 / r**2
    rn_b_r = 2 * (mass - Q**2 / (2 * r)) / r**2 - Q**2 / r**3
    equal(rn_f.partial("r"), rn_b_r, "RN radial lapse derivative")
    passed.append("RN_electrovac_radial_identity")

    # Chain rule under du_B/du=G_infinity; no interchange of limits.
    gi = sym("G_infinity")
    radiation = sym("radiation_squared")
    equal((-radiation / gi) / gi, -radiation / gi**2, "unit Bondi flux")
    passed.append("Bondi_mass_flux_time_normalization")

    cutoff_lower_bound = F(19, 20)**2 * F(7, 8)
    if not cutoff_lower_bound > F(3, 4):
        raise ArithmeticError("actual-ray cutoff exit margin")
    gamma, delta = F(3, 4), F(1, 100)
    if not (gamma - delta > 0 and 1 - 2 * delta > 0 and 1 - delta > 0):
        raise ArithmeticError("optical bootstrap integrability")
    passed.append("strict_cutoff_exit_and_integrable_optical_exponents")
    return {
        "checks_passed": passed,
        "cutoff_exit": {
            "time_condition": "t >= 8(1+u), u >= 0",
            "rho_over_one_plus_t_lower_bound": str(cutoff_lower_bound),
            "required_lower_bound": "3/4",
            "strict_margin": str(cutoff_lower_bound - F(3, 4)),
        },
        "optical_exponents": {
            "gamma": str(gamma), "delta_upper_bound": str(delta),
            "nonlinear_integral_power": str(delta),
            "time_derivative_decay_power": str(-2 + 2 * delta),
        },
    }


def main():
    folder = Path(__file__).resolve().parent
    result = {
        "scope": "finite exact algebra only; not analytic or PDE certification",
        "arithmetic": "sparse Laurent polynomials over rational complex numbers",
        **checks(),
    }
    names = ("SMALL_DATA_NULL_INFINITY.md", "SMALL_DATA_DISPERSION.md", Path(__file__).name)
    result["source_sha256"] = {
        name: sha256((folder / name).read_bytes()).hexdigest() for name in names
    }
    output = folder / "NULL_INFINITY_ALGEBRA_RESULTS_2026-10-16.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": len(result["checks_passed"]), "scope": result["scope"],
                      "report": output.name}, ensure_ascii=False))


if __name__ == "__main__":
    main()
