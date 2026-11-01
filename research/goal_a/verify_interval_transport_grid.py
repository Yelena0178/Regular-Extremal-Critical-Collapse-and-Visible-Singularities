"""Exact-rational cross-checks for the outward binary64 grid kernel."""

from fractions import Fraction as Q
import json
import random
import numpy as np
from interval_transport_grid import V,coefficients,cell_bounds,shared_derivatives,jacobian_upper
from neutral_transport import TransportConfiguration,evolve,onset_boundaries
from rational_transport_cell import hermite_cell,cell_quantities


def require(ok,message):
    if not ok:raise ArithmeticError(message)


def contains(interval,exact):
    return Q(float(interval.lo))<=exact<=Q(float(interval.hi))


def arithmetic_checks():
    require(np.finfo(np.float64).nmant==52,'binary64 precision')
    tiny=np.nextafter(np.float64(0),np.float64(1))
    require(tiny>0 and tiny*2>tiny,'gradual underflow')
    require(contains(V(tiny)/2,Q(float(tiny))/2),'subnormal division')
    rng=random.Random(20261017)
    for _ in range(256):
        a=float(rng.uniform(-100,100));b=float(rng.uniform(-100,100))
        for value,exact in [(V(a)+V(b),Q(a)+Q(b)),(V(a)*V(b),Q(a)*Q(b)),
                            (V(a)/V(b),Q(a)/Q(b))]:
            require(contains(value,exact),'rational arithmetic cross-check')
    for a in [Q(1,3),Q(-1,7),Q(10**30,7)]:
        require(contains(V.rational(a),a),'rational conversion')
    require(not contains(V(.1+.2),Q(.1)+Q(.2)),'unwidened arithmetic negative control')
    try:V(-1,1).reciprocal()
    except ArithmeticError:pass
    else:raise ArithmeticError('zero interval accepted')
    return dict(exact_basic_operation_comparisons=768,negative_controls=2,
                subnormal_check=True)


def main():
    with np.errstate(over='raise',invalid='raise',divide='raise',under='ignore'):
        arithmetic=arithmetic_checks()
        outgoing,incoming,p=onset_boundaries(.05)
        cfg=TransportConfiguration(steps_u=24,steps_v=24,final_u=p['v_end']/2,
                                   initial_v=p['v_cap'],final_v=31*p['v_end']/32)
        data=evolve(outgoing,incoming,cfg);x=data['state']
        xu,xv,xuv=shared_derivatives(data)
        hu=Q(cfg.final_u)/24;hv=(Q(cfg.final_v)-Q(cfg.initial_v))/24
        records=[]
        for i,j in [(8,12),(17,19),(23,23)]:
            sl=(slice(i,i+2),slice(j,j+2))
            polys=hermite_cell(x[sl].tolist(),xu[sl].tolist(),xv[sl].tolist(),xuv[sl].tolist(),hu,hv)
            c=coefficients(x[sl],xu[sl],xv[sl],xuv[sl],V.rational(hu),V.rational(hv))
            for k,poly in enumerate(polys):
                actual={}
                for monomial,value in poly.terms.items():
                    powers=dict(monomial);actual[powers.get('u',0),powers.get('v',0)]=value
                for a in range(4):
                    for b in range(4):
                        require(contains(c[0,0,k,a,b],actual.get((a,b),Q(0))),'exact Hermite coefficient')
            B,delta=cell_bounds(c,V.rational(hu),V.rational(hv))
            M=[Q(1,1000)]*6
            Br,dr,Lr=cell_quantities(polys,hu,hv,M)
            for k in range(6):
                require(Q(float(B.lo[0,0,k]))<=Br[k][0] and Q(float(B.hi[0,0,k]))>=Br[k][1],
                        'exact Bernstein range')
                require(Q(float(delta[0,0,k]))>=dr[k],'exact residual upper bound')
            lo=(V(B.lo[0,0])-V(.001)).lo;hi=(V(B.hi[0,0])+V(.001)).hi
            L=jacobian_upper(lo,hi)
            # The rational reference computes cancellations between Jacobian
            # terms. The batch kernel deliberately uses the triangle bound.
            for a in range(6):
                for b in range(6):require(Q(float(L[a,b]))>=Lr[a][b],'rational Jacobian bound')
            records.append(dict(cell=[i,j],exact_coefficient_checks=96,
                                max_residual=float(np.max(delta))))
        print(json.dumps(dict(status='PASS',arithmetic=arithmetic,cells=records,
                              full_grid_certified=False),indent=2))


if __name__=='__main__':main()
