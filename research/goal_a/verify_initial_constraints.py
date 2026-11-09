"""Exact constraint-geometry checks for A-IC01; no spacetime evolution."""

from pathlib import Path
import json
import platform

import sympy as s


checks = {}


def require(name, condition):
    if not bool(condition):
        raise RuntimeError(name)
    checks[name] = True


def zero(name, expression):
    require(name, s.simplify(s.trigsimp(expression)) == 0)


r, theta, azimuth = s.symbols("r theta azimuth", positive=True, real=True)
coords = [r, theta, azimuth]
a, k, Q = [s.Function(name)(r) for name in ("a", "k", "Q")]
metric = s.diag(a**2, r**2, r**2 * s.sin(theta)**2)
inverse = metric.inv()
connection = [
    [
        [
            s.simplify(sum(
                inverse[i, ell] * (
                    s.diff(metric[ell, j], coords[n])
                    + s.diff(metric[ell, n], coords[j])
                    - s.diff(metric[j, n], coords[ell])
                ) / 2
                for ell in range(3)
            ))
            for n in range(3)
        ]
        for j in range(3)
    ]
    for i in range(3)
]

ricci = s.zeros(3)
for i in range(3):
    for j in range(3):
        ricci[i, j] = s.simplify(sum(
            s.diff(connection[n][i][j], coords[n])
            - s.diff(connection[n][i][n], coords[j])
            + sum(
                connection[n][i][j] * connection[ell][n][ell]
                - connection[ell][i][n] * connection[n][j][ell]
                for ell in range(3)
            )
            for n in range(3)
        ))
curvature = s.simplify(sum(inverse[i, j] * ricci[i, j]
                           for i in range(3) for j in range(3)))
m = r * (1 - a**-2) / 2
zero("scalar_curvature_from_metric", curvature - 4 * s.diff(m, r) / r**2)

mixed_k = s.diag(k, 0, 0)
trace_k = s.trace(mixed_k)
zero("extrinsic_hamiltonian_cancellation", trace_k**2 - s.trace(mixed_k**2))
momentum = []
for i in range(3):
    divergence = sum(
        s.diff(mixed_k[j, i], coords[j])
        + sum(connection[j][j][ell] * mixed_k[ell, i]
              - connection[ell][j][i] * mixed_k[j, ell]
              for ell in range(3))
        for j in range(3)
    )
    momentum.append(s.simplify(divergence - s.diff(trace_k, coords[i])))
zero("radial_momentum_geometry", momentum[0] - 2 * k / r)
zero("theta_momentum_geometry", momentum[1])
zero("azimuth_momentum_geometry", momentum[2])

u, v, P, S = [s.Function(name)(r) for name in ("u", "v", "P", "S")]
e = s.symbols("e", real=True)
gradient_squared = s.diff(u, r)**2 + s.diff(v, r)**2
pi_squared = P**2 + S**2
rho = (Q**2 / r**4 + pi_squared + gradient_squared / a**2) / 2
mass_source = r**2 * (pi_squared + gradient_squared / a**2) / 2 + Q**2 / (2*r**2)
charge_source = e*a*r**2*(v*P-u*S)
radial_j = -(P*s.diff(u, r) + S*s.diff(v, r))
a_prime = a**3/r * (mass_source - (1-a**-2)/2)
zero("full_hamiltonian_constraint", (curvature - 4*rho).subs(s.diff(a, r), a_prime))
zero("full_radial_momentum_constraint", (momentum[0] - 2*radial_j).subs(k, r*radial_j))

volume_factor = a*r**2*s.sin(theta)
electric_contravariant = Q/(a*r**2)
electric_divergence = s.diff(volume_factor*electric_contravariant, r)/volume_factor
zero("gauss_geometry", electric_divergence-s.diff(Q, r)/(a*r**2))
zero("full_gauss_constraint", (electric_divergence-e*(v*P-u*S)).subs(s.diff(Q, r), charge_source))

A, kap, omega, f, fp, Delta = s.symbols("A kappa omega f fp Delta", real=True)
seed = {u: A*f, v: 0, P: A*kap*fp, S: -A*omega*f,
        s.diff(u, r): A*fp, s.diff(v, r): 0, a: Delta**s.Rational(-1, 2)}
seed_mass = s.simplify(mass_source.subs(seed, simultaneous=True))
seed_charge = s.simplify(charge_source.subs(seed, simultaneous=True))
seed_k = s.simplify((r*radial_j).subs(seed, simultaneous=True))
zero("seed_mass_source", seed_mass - (A**2*r**2*((kap**2+Delta)*fp**2+omega**2*f**2)/2+Q**2/(2*r**2)))
zero("seed_charge_source", seed_charge-e*A**2*omega*r**2*f**2/s.sqrt(Delta))
zero("seed_radial_extrinsic_curvature", seed_k+r*A**2*kap*fp**2)
for name, expression in [("mass", seed_mass), ("charge", seed_charge), ("K", seed_k)]:
    zero("amplitude_sign_gauge_equivalence_"+name, expression.subs(A, -A)-expression)

max_amplitude = s.Rational(1, 8)
bootstrap_compactness = 7*max_amplitude**2+s.Rational(49, 25)*max_amplitude**4
mass_bound = s.Rational(7, 2)*max_amplitude**2+s.Rational(49, 25)*max_amplitude**4
zero("explicit_mass_upper_bound", mass_bound-s.Rational(5649, 102400))
require("bootstrap_strictly_improves_half", bootstrap_compactness < s.Rational(1, 2))
require("mass_below_one_sixteenth", mass_bound < s.Rational(1, 16))
require("global_delta_above_seven_eighths", 1-2*mass_bound > s.Rational(7, 8))
exponential_lower = sum(s.Rational(4)**n/s.factorial(n) for n in range(4))
require("bump_derivative_exponential_bound", exponential_lower > 16)
zero("shell_r_squared_integral", s.integrate(r**2, (r, 1, 2))-s.Rational(7, 3))
zero("shell_inverse_r_squared_integral", s.integrate(r**-2, (r, 1, 2))-s.Rational(1, 2))

report = {
    "scope": "EXACT_INITIAL_CONSTRAINT_GEOMETRY_AND_RATIONAL_BOUNDS_ONLY",
    "python": platform.python_version(),
    "sympy": s.__version__,
    "checks": checks,
    "mass_upper_bound": str(mass_bound),
    "spacetime_evolution_performed": False,
    "complete_dispersion_certified": False,
    "extremal_critical_endpoint_certified": False,
    "goal_A_solved": False,
    "external_independent_review_completed": False,
}
output = Path(__file__).with_name("verification.json")
output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
print(f"PASS: {len(checks)} exact symbolic/rational checks; report: {output}")
print("Scope: initial constraints only. No PDE evolution or solution of goal A.")
