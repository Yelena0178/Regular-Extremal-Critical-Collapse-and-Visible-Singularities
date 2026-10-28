"""Rational Darboux charge enclosure and analytic all-radius positivity bound.

The target parameters are exact rationals A=2/5, w=3/20, R=10, W=4,
e=3/5 and every real direction d in [-1,1]. Decimal.exp is assumed
correctly rounded. Rational input rounding is directed before exponentiation.
No numerical ODE solution is used in this certificate.
"""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


def exponential_bound(q, upper):
    q = F(q)
    if q < -100:
        return F(1, 2**100) if upper else F(0)
    with localcontext() as ctx:
        ctx.prec = 70
        ctx.rounding = ROUND_CEILING if upper else ROUND_FLOOR
        argument = Decimal(q.numerator)/Decimal(q.denominator)
        result = argument.exp()
        return F(result.next_plus() if upper else result.next_minus())


def bump_squared(z, upper):
    if z == 1:
        return F(0)
    return exponential_bound(-2*z*z/(1-z*z), upper)


def certificate(panels=1024):
    amplitude, frequency, R, W, e = F(2, 5), F(3, 20), F(10), F(4), F(3, 5)
    low, high = F(0), F(0)
    for j in range(panels):
        left, right = F(j, panels), F(j+1, panels)
        # Pair z and -z first; the cross term integrates to zero.
        low += (R*R+W*W*left*left)*bump_squared(right, False)/panels
        high += (R*R+W*W*right*right)*bump_squared(left, True)/panels
    factor = 2*e*frequency*amplitude**2*W
    Qlow, Qhigh = factor*low, factor*high
    inner, outer = R-W, R+W
    if not 0 < Qlow <= Qhigh < inner:
        raise ArithmeticError('charge enclosure does not imply Q(r)<r')
    # |b_z|^2 <= 64/exp(2) < 9. Integration of 2*a*a' is zero.
    Eupper = 36*R*amplitude**2/W + 2*W*amplitude**2/inner + 4*frequency**2*R*W*amplitude**2
    core_lower = inner/outer*exponential_bound(-Eupper, False)
    exterior_barrier = 1-Qhigh**2/outer**2
    full_lower = min(core_lower, exterior_barrier)
    if not full_lower > F(1, 10**7):
        raise ArithmeticError('uniform positive lower bound was not obtained')
    Mlow = Qlow**2/(2*outer)
    return dict(exact_parameters=dict(amplitude='2/5', frequency='3/20', radius=10,
                                      width=4, coupling='3/5', direction_interval=['-1', '1']),
                panels=panels, charge_lower=str(Qlow), charge_upper=str(Qhigh),
                charge_decimal_display=[float(Qlow), float(Qhigh)],
                uniform_integrated_rS_upper=str(Eupper),
                uniform_all_radius_f_lower=str(full_lower),
                uniform_all_radius_f_lower_display=float(full_lower),
                certified_simpler_strict_f_lower='1/10000000',
                uniform_ADM_mass_lower_display=float(Mlow),
                claim='conditional-on-arithmetic analytic initial-data certificate for the whole direction family',
                arithmetic_assumptions=['CPython Decimal.exp correctly rounded',
                                        'Fraction exact integer arithmetic and directed Decimal input rounding'],
                numerical_ODE_used=False, future_focusing_certified=False,
                retained_mass_certified=False, goal_A_proved=False)


if __name__ == '__main__':
    result = certificate()
    result['source_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    Path('CHARGE_SHELL_INITIAL_CERTIFICATE_2026-10-22.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('charge_lower', 'charge_upper', 'uniform_all_radius_f_lower', 'source_sha256')}, indent=2))
