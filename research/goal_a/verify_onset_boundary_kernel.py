"""Independent finite checks for A-BOUND01; whole-edge proof has its own runner."""

from fractions import Fraction as F
import json
from certify_onset_boundary import (exp_bound,chi_point,q_jets,hermite,bounds,
                                    compose,field_model,absolute)
from verify_horizon_seed import I
from verify_null_infinity_algebra import sym


def require(ok,label):
    if not ok:
        raise ArithmeticError(label)


def main():
    y,z,C=map(sym,('y','z','C'))
    B=y**-2+z**-2
    B1=-2*y**-3+2*z**-3
    B2=6*y**-4+6*z**-4
    cp=C*(1-C)*B
    cpp=C*(1-C)*((1-2*C)*B**2+B1)
    cppp=C*(1-C)*((1-6*C+6*C**2)*B**3+3*(1-2*C)*B*B1+B2)
    derivative=dict(y=1,z=-1,C=cp)
    require(not (cp.total(derivative)-cpp).terms,'chi second')
    require(not (cpp.total(derivative)-cppp).terms,'chi third')
    q=C+y*cp
    require(not (q.total(derivative)-(2*cp+y*cpp)).terms,'q first')
    require(not (q.total(derivative).total(derivative)-(3*cpp+y*cppp)).terms,'q second')
    require(bool((q.total(derivative)-(cp+y*cpp)).terms),'missing derivative negative control')
    require(exp_bound(F(64,63)).hi<3,'analytic tail constant')
    require(exp_bound(1).lo>2,'exp lower control')
    require(chi_point(F(1,2)).lo<=F(1,2)<=chi_point(F(1,2)).hi,'logistic midpoint')
    # At y=1/2, chi'=2, chi''=0 and chi'''=-16.
    qv=q_jets(I(F(1,2)),F(1),F(1))
    for interval,exact in zip(qv,[F(3,2),F(4),F(-8)]):
        require(interval.lo<=exact<=interval.hi,'independent central derivatives')
    # x^3 on [0,1] is exactly reproduced by a cubic Hermite interpolant.
    poly=hermite(0,1,0,3,F(1))
    require(poly==[0,0,0,1],'Hermite independent cubic')
    rb=bounds(compose(poly,F(1,4),F(1,2)))
    require(rb.lo<=F(1,64) and rb.hi>=F(27,64),'Bernstein restricted cubic')
    for left,right in [(F(0),F(1,64)),(F(63,64),F(1)),(F(1),F(2))]:
        qm,qe,q2m,q2e,qb=field_model(left,right,F(0),F(1),F(1))
        require(qe>=0 and q2e>=0 and absolute(qb)<=2,'tail model')
    try:
        q_jets(I(0,F(1,2)),F(1),F(1))
    except ValueError:
        pass
    else:
        raise ArithmeticError('singular-tail interval accepted')
    print(json.dumps(dict(status='PASS',exact_derivative_identities=4,
        central_derivative_values=[1.5,4,-8],negative_controls=2,
        whole_edge_runner='certify_onset_boundary.py')))


if __name__=='__main__':
    main()
