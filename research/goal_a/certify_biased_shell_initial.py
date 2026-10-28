"""Uniform pointwise f barrier for the exact normalized two-parameter family."""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
from certify_charge_shell_initial import certificate, exponential_bound


def certify():
    base = certificate(1024)
    Qupper = F(base['charge_upper'])
    A, w, inner, outer, W, B = F(2, 5), F(3, 20), F(6), F(14), F(4), F(2)
    # C_beta in [exp(-B), exp(B)], so omega_beta <= omega*exp(2B).
    # a'^2 <= 9 A^2/W^2 and (a'+a/r)^2 <= 2 a'^2+2 a^2/r^2.
    S_upper = 27*A*A/(W*W)+2*A*A/(inner*inner)+2*w*w*A*A*exponential_bound(4*B, True)
    numerator = 1-(Qupper/inner)**2
    denominator = 1+outer*outer*S_upper
    barrier = F(1, 100000)
    margin = numerator-barrier*denominator
    if numerator <= 0 or margin <= 0:
        raise ArithmeticError('uniform pointwise barrier failed')
    return dict(exact_parameters=dict(amplitude='2/5', frequency='3/20', radius=10, width=4,
                                      coupling='3/5', direction_interval=['-1', '1'], bias_interval=['-2', '2']),
                exact_normalization='ratio of positive weighted integrals, not the floating quad result',
                charge_interval_display=base['charge_decimal_display'],
                S_upper=str(S_upper), S_upper_display=float(S_upper),
                pointwise_barrier=str(barrier), strict_crossing_margin=str(margin),
                strict_crossing_margin_display=float(margin),
                lower_barrier_available_display=float(numerator/denominator),
                conclusion='all radii, all parameters in the stated rectangle: 1 >= f > 1/100000',
                assumptions=base['arithmetic_assumptions'],
                future_focusing_certified=False, retained_mass_certified=False, goal_A_proved=False)


if __name__ == '__main__':
    result = certify()
    result['source_sha256'] = {name: sha256(Path(name).read_bytes()).hexdigest() for name in
                              ['certify_biased_shell_initial.py', 'certify_charge_shell_initial.py']}
    Path('BIASED_SHELL_INITIAL_CERTIFICATE_2026-10-22.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('S_upper', 'strict_crossing_margin', 'source_sha256')}, indent=2))
