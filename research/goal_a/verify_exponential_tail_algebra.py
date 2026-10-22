"""Exact Bessel-tail constraint identities and rational special-function audit."""

from fractions import Fraction as Q
from hashlib import sha256
import json
import math
from pathlib import Path
import mpmath as mp

from verify_null_infinity_algebra import sym
from verify_horizon_seed import I


def bessel_point(x,order):
    x=Q(x)
    if not 0<=x<=1 or order not in (0,1):raise ValueError('Bessel audit domain')
    terms=[(-1)**k*(x/2)**(2*k+order)/
        (math.factorial(k)*math.factorial(k+order)) for k in range(25)]
    total=sum(terms,Q(0));next_term=(x/2)**(50+order)/(math.factorial(25)*math.factorial(25+order))
    return I(total-next_term,total)


def number(x):
    x=Q(x);return mp.mpf(x.numerator)/x.denominator


def main():
    x,j0,j1,gamma,xi,R,e,D=map(sym,('x','j0','j1','gamma','xi','R','e','D'))
    dv=dict(x=-gamma*x,j0=gamma*x*j1,j1=-gamma*x*j0+gamma*j1)
    radius=R*j0;charge=R-e*R*R*xi*x*x*(j0*j0+j1*j1)/(2*D)
    claims=dict(raychaudhuri=radius.total(dv).total(dv)+gamma*gamma*x*x*radius,
        positive_charge_flux=charge.total(dv)-e*R*R*xi*gamma*x*x*j0*j0/D,
        bessel_norm_derivative=(j0*j0+j1*j1).total(dv)-2*gamma*j1*j1,
        cumulative_charge_derivative=(x*x*(j0*j0+j1*j1)).total(dv)+2*gamma*x*x*j0*j0)
    for name,p in claims.items():
        if p.terms:raise ArithmeticError('tail algebra '+name)
    # At x=1/64 the next alternating term is much smaller than 1e-70.
    # Resolve both rational endpoints instead of comparing rounded midpoints.
    mp.mp.dps=220;comparisons=0
    for order in (0,1):
        for j in range(65):
            xq=Q(j,64);enclosure=bessel_point(xq,order);actual=mp.besselj(order,number(xq))
            if not number(enclosure.lo)<=actual<=number(enclosure.hi):
                raise ArithmeticError('Bessel rational point enclosure')
            comparisons+=1
    result=dict(status='PASS',exact_identities=list(claims),rational_Bessel_point_comparisons=comparisons,
        precision_digits=mp.mp.dps,scope='null constraint identities only; no spacetime or critical curve proof',
        actual_smooth_onset_certified=False,complete_PDE_rectangle_certified=False,goal_A_proved=False)
    folder=Path(__file__).resolve().parent
    names=['verify_exponential_tail_algebra.py','verify_null_infinity_algebra.py','verify_horizon_seed.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'EXPONENTIAL_TAIL_ALGEBRA_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
