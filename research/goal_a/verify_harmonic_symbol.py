"""Exact principal-symbol algebra checks, not a PDE well-posedness proof."""
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    bt = transpose(b)
    return [[sum((x*y for x, y in zip(row, col)), F(0)) for col in bt]
            for row in a]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def check(alpha, z, w):
    if alpha <= 0 or z <= 0:
        raise ValueError("positive lapse and spatial metric required")
    beta, c = alpha*w, alpha*z
    lp, lm = beta+c, beta-c
    # Real/imaginary Z values are arbitrary frozen background derivatives.
    zp, zm = (F(3, 2), F(-2, 3)), (F(-4, 5), F(7, 4))
    lambdas = [lp, lm, lp, lm, lp, lm]
    matrix = [[F(0) for _ in range(6)] for _ in range(6)]
    diagonal = [[F(0) for _ in range(6)] for _ in range(6)]
    transform = identity(6)
    for i, value in enumerate(lambdas):
        matrix[i][i] = diagonal[i][i] = value
    for slot, value in zip((0, 2), zp):
        b = alpha*(w+z)*value/z
        matrix[slot][5] = b
        transform[slot][5] = b/(lp-lm)
    for slot, value in zip((1, 3), zm):
        b = alpha*(z-w)*value/z
        matrix[slot][4] = b
        transform[slot][4] = b/(lm-lp)
    if multiply(transform, matrix) != multiply(diagonal, transform):
        raise RuntimeError("characteristic transformation identity failed")
    symmetrizer = multiply(transpose(transform), transform)
    ha = multiply(symmetrizer, matrix)
    if ha != transpose(ha):
        raise RuntimeError("principal symmetrizer identity failed")
    return {"alpha": str(alpha), "z": str(z), "W": str(w),
            "lambda_plus": str(lp), "lambda_minus": str(lm),
            "regime": "horizon" if w == z else ("inside" if w > z else "outside")}


def run():
    samples = []
    for alpha, z, multiplier in itertools.product(
            (F(1, 2), F(1), F(3, 2)), (F(1, 2), F(1), F(3, 2)), (F(0), F(1), F(2))):
        samples.append(check(alpha, z, multiplier*z))
    for alpha, z in ((F(0), F(1)), (F(1), F(0))):
        try:
            check(alpha, z, F(1))
        except ValueError:
            pass
        else:
            raise RuntimeError("degenerate geometric input was not rejected")
    folder = Path(__file__).resolve().parent
    output = {
        "date": "2026-10-16", "evidence": "exact_finite_principal_algebra",
        "samples": samples, "sample_count": len(samples),
        "goal_A_proved": False, "full_PDE_wellposedness_proved": False,
        "scope": "frozen_positive_radius_symbol_only",
        "source_sha256": {name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
                          for name in ("verify_harmonic_symbol.py", "HARMONIC_PRINCIPAL_SYMBOL.md")},
    }
    target = folder/"HARMONIC_SYMBOL_RESULTS_2026-10-16.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"result": str(target), "exact_samples": len(samples),
                      "goal_A_proved": False}))


if __name__ == "__main__":
    run()
