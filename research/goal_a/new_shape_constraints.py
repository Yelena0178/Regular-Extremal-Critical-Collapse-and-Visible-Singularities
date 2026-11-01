"""Exact rational bounds for a new fixed-e, R=10 null-cone candidate.

Only C0 constraint inequalities are computed here. The smooth existence
argument and its scope are given in NEW_SHAPE_CONSTRAINTS.md.
"""

from fractions import Fraction as F
from hashlib import sha256
import json
import math
from pathlib import Path

from verify_horizon_seed import I, down, up, log_two, exp_positive


PHI, RHO, RADIUS, COUPLING = F(7, 10), F(1, 8), F(10), F(3, 5)
LEFT, RIGHT = F(59, 100), F(3, 5)


def trigonometric_bounds(x):
    if not F(0) <= x <= F(1):
        raise ValueError("Taylor bounds require 0 <= x <= 1")
    cosine = sum(((-1)**n*x**(2*n)/math.factorial(2*n)
                  for n in range(21)), F(0))
    sine = sum(((-1)**n*x**(2*n+1)/math.factorial(2*n+1)
                for n in range(21)), F(0))
    cr, sr = x**42/math.factorial(42), x**43/math.factorial(43)
    return I(down(cosine-cr), up(cosine+cr)), I(down(sine-sr), up(sine+sr))


def bounds(s):
    cosine, sine = trigonometric_bounds(PHI)
    tau = sine/cosine
    # rho=1/8: t=rho**(1/s); 3 log(2)/s lies inside [0,5].
    t = exp_positive(3*log_two()/s).reciprocal()
    v2 = s/(s+PHI*tau)
    v1 = v2*t
    a = RHO**2
    h0 = s*t*(1-s*tau/PHI)/(s+PHI*tau)**2
    primitive = 1/(1+2*s)-2*a+a*a/(1-2*s)-8*a*s*s*t/(1-4*s*s)
    h1 = h0+1-v2*primitive/(cosine**2*(1-a)**2)-(1-v2)*tau/PHI
    k2 = (PHI*cosine**2*(1-a)/2)**2*(1-s)/s
    f0 = RHO*cosine*(cosine-s*sine/PHI)
    p0 = RHO*cosine*(PHI*sine+s*cosine)/v1
    return dict(H0=h0, H1=h1, k_squared=k2, f0=f0, p0=p0, v1=v1, v2=v2)


def rational_certificate(count=128):
    minimum = {key: None for key in ("H0", "H1", "f0", "p0", "v1")}
    maximum_p0 = F(0)
    partition = []
    for j in range(count):
        lo = LEFT+(RIGHT-LEFT)*F(j, count)
        hi = LEFT+(RIGHT-LEFT)*F(j+1, count)
        b = bounds(I(lo, hi))
        thresholds = dict(H0=F(1, 512), H1=F(1, 128), f0=F(1, 64),
                          p0=F(1, 2), v1=F(1, 128))
        for key, threshold in thresholds.items():
            if b[key].lo <= threshold:
                raise ArithmeticError(f"{key} failed on cell {j}")
            minimum[key] = b[key].lo if minimum[key] is None else min(minimum[key], b[key].lo)
        if b['p0'].hi >= 128:
            raise ArithmeticError("initial radial derivative bound")
        if b['k_squared'].lo <= F(1, 64) or b['k_squared'].hi >= F(1, 16):
            raise ArithmeticError("charge normalization interval")
        maximum_p0 = max(maximum_p0, b['p0'].hi)
        partition.append([str(lo), str(hi), str(b['H0'].lo), str(b['H1'].lo)])
    target, margin = 1/(COUPLING*RADIUS), F(1, 2048)
    lower, upper = bounds(I(LEFT))['k_squared'], bounds(I(RIGHT))['k_squared']
    if lower.lo <= (target+margin)**2 or upper.hi >= (target-margin)**2:
        raise ArithmeticError("charge-root bracket")

    # Explicit conservative bounds used by the analytic smoothing argument.
    eta, sqrt_eta = F(1, 2**200), F(1, 2**100)
    dphi_l2 = 30*512*sqrt_eta
    potential_l1 = (1024+dphi_l2)*dphi_l2
    if dphi_l2 >= F(1, 2**86) or potential_l1 >= F(1, 2**75):
        raise ArithmeticError("smooth-profile coefficient bounds")
    kernel = 4096*potential_l1
    if kernel >= F(1, 2**63):
        raise ArithmeticError("relative-radius contraction")
    return dict(
        status="PASS", evidence="exact_rational_C0_constraint_inequalities",
        fixed_parameters={"e": str(COUPLING), "R": str(RADIUS), "Phi": str(PHI), "rho": str(RHO)},
        s_interval=[str(LEFT), str(RIGHT)], partition_cells=count,
        minimum_lower_bounds={key: str(value) for key, value in minimum.items()},
        maximum_p0_upper=str(maximum_p0),
        normalized_charge_target=str(target), charge_bracket_margin=str(margin),
        endpoint_k_squared={"left_lower": str(lower.lo), "right_upper": str(upper.hi)},
        H_uniform_margin="1/512", normalized_charge_range="1/8 < k < 1/4",
        smoothing_width=str(eta), derivative_L2_error_upper=str(dphi_l2),
        potential_L1_error_upper=str(potential_l1), volterra_kernel_upper=str(kernel),
        arithmetic="Fraction intervals rounded outward to 192 binary places; rational Taylor remainders",
        smooth_existence_requires_analytic_argument=True,
        finite_domain_nontrapping_certified=False, full_AF_Cauchy_realization=False,
        transverse_matching_certified=False, goal_A_proved=False,
        partition_lower_bounds=partition)


def main():
    folder = Path(__file__).resolve().parent
    result = rational_certificate()
    result['source_sha256'] = {
        name: sha256((folder/name).read_bytes()).hexdigest()
        for name in ('new_shape_constraints.py', 'verify_horizon_seed.py', 'NEW_SHAPE_CONSTRAINTS.md')}
    target = folder/'NEW_SHAPE_CONSTRAINT_CERTIFICATE_2026-10-17.json'
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'partition_lower_bounds'}, indent=2))


if __name__ == '__main__':
    main()
