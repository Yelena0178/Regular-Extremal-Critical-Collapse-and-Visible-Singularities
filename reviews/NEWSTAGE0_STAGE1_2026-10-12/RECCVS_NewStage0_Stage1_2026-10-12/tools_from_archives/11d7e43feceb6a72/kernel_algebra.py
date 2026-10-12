"""Exact algebra checks for L012; these do not certify PDE continuation."""
import sympy as s

x, y, xi, zeta, h, tau, f = s.symbols(
    "x y xi zeta h tau f", nonnegative=True
)
kernel = 1 - 2 * (x - xi) * (y - zeta) / (
    (1 + x * y) * (1 + xi * zeta)
)
checks = {
    "terminal_operator": s.factor(
        s.diff(kernel, x, y) + 2 * kernel / (1 + x * y) ** 2
    ),
    "source_operator": s.factor(
        s.diff(kernel, xi, zeta) + 2 * kernel / (1 + xi * zeta) ** 2
    ),
    "first_characteristic_boundary": s.factor(kernel.subs(x, xi) - 1),
    "second_characteristic_boundary": s.factor(kernel.subs(y, zeta) - 1),
    "geometric_integral_primitive": s.factor(
        s.diff(f ** 2 / (2 * (1 + f * tau) ** 2), f)
        - f / (1 + f * tau) ** 3
    ),
}
for name, residual in checks.items():
    print(f"{name}: {residual}")
    if residual != 0:
        raise SystemExit(f"Failed exact identity: {name}")
print("Only the displayed algebraic identities have been checked.")
