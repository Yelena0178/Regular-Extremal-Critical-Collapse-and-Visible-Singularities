"""Exact polynomial/outward-rational single-cell kernel for A-GOUR01.

Inflow error bounds are caller-supplied hypotheses. Checking one cell is NOT
a full candidate PDE certificate, and does not validate those hypotheses.
"""

from fractions import Fraction as Q
from math import comb
from verify_null_infinity_algebra import P, sym
from verify_horizon_seed import I


NAMES = ('r','k','t','n','z','m')


def field_polynomials():
    r,k,t,n,z,m = [sym(s) for s in NAMES]
    return (n,k*n*z*z/r,-k*n*z*(1-2*m/r)/r,
            2*k*m*n/r**2,-t/r-2*k*m*z/r**2,t*t/(2*k))


def bernstein_bounds(poly):
    terms = {}
    for monomial, coefficient in poly.terms.items():
        powers = dict(monomial)
        if set(powers)-{'u','v'} or min(powers.values(),default=0) < 0:
            raise ValueError('non-polynomial cell expression')
        key = (powers.get('u',0),powers.get('v',0))
        terms[key] = terms.get(key,Q(0))+coefficient
    degree_u = max((i for i,j in terms),default=0)
    degree_v = max((j for i,j in terms),default=0)
    coefficients = []
    for i in range(degree_u+1):
        for j in range(degree_v+1):
            coefficients.append(sum((c*Q(comb(i,a),comb(degree_u,a))
                                      *Q(comb(j,b),comb(degree_v,b))
                                      for (a,b),c in terms.items() if a<=i and b<=j),Q(0)))
    return min(coefficients),max(coefficients)


def hermite_cell(values, derivative_u, derivative_v, derivative_uv, hu, hv):
    """Rebuild exact polynomials from shared node data [2][2][6].

    Binary floats, if supplied, denote their exact dyadic rational values.
    hu and hv must describe the actual rational mesh, not rounded differences.
    """
    hu,hv = Q(hu),Q(hv)
    if min(hu,hv)<=0:
        raise ValueError('positive mesh lengths required')
    u,v = sym('u'),sym('v')
    def bases(s):
        return ((1-3*s**2+2*s**3,3*s**2-2*s**3),
                (s-2*s**2+s**3,-s**2+s**3))
    (U,Ud),(V,Vd) = bases(u),bases(v)
    result = [P() for _ in range(6)]
    for i in (0,1):
        for j in (0,1):
            for k in range(6):
                result[k] = result[k]+(Q(values[i][j][k])*U[i]*V[j]
                    +hu*Q(derivative_u[i][j][k])*Ud[i]*V[j]
                    +hv*Q(derivative_v[i][j][k])*U[i]*Vd[j]
                    +hu*hv*Q(derivative_uv[i][j][k])*Ud[i]*Vd[j])
    return result


def interval_evaluate(poly, point):
    result = I(0)
    for monomial,coefficient in poly.terms.items():
        term = I(coefficient)
        for name,power in monomial:
            term = term*point[name]**power
        result = result+term
    return result


def cell_quantities(polys, hu, hv, radius):
    """Exact residual bounds, outward 192-bit Jacobian bounds and tube signs."""
    hu,hv = Q(hu),Q(hv)
    M = [Q(x) for x in radius]
    if len(polys)!=6 or len(M)!=6 or min(M)<=0 or min(hu,hv)<=0:
        raise ValueError('invalid cell data')
    r,k,t,n,z,m = polys
    B = [bernstein_bounds(poly) for poly in polys]
    if B[0][0]-M[0]<=0 or B[1][0]-M[1]<=0 or B[3][1]+M[3]>=0:
        raise ArithmeticError('cell tube does not preserve r>0, kappa>0, nu<0')
    numerator = (r.partial('u')/hu-n,
        r*k.partial('u')/hu-k*n*z*z,
        r*r*t.partial('u')/hu+k*n*z*(r-2*m),
        r*r*n.partial('v')/hv-2*k*m*n,
        r*r*z.partial('v')/hv+t*r+2*k*m*z,
        2*k*m.partial('v')/hv-t*t)
    denominators = (Q(1),B[0][0],B[0][0]**2,B[0][0]**2,B[0][0]**2,2*B[1][0])
    delta = [max(abs(a),abs(b))/d for (a,b),d in
             zip([bernstein_bounds(poly) for poly in numerator],denominators)]
    point = {name:I(lo-bound,hi+bound) for name,(lo,hi),bound in zip(NAMES,B,M)}
    L = []
    for poly in field_polynomials():
        row = []
        for name in NAMES:
            bound = interval_evaluate(poly.partial(name),point)
            row.append(max(abs(bound.lo),abs(bound.hi)))
        L.append(row)
    return B,delta,L


def verify_cell(polys, hu, hv, radius, inflow_error):
    """Conditional single-cell certificate; inflow bounds are NOT established."""
    M,b = [Q(x) for x in radius],[Q(x) for x in inflow_error]
    if len(b)!=6 or min(b)<0:
        raise ValueError('invalid supplied inflow error')
    B,delta,L = cell_quantities(polys,hu,hv,M)
    h = [Q(hu)]*3+[Q(hv)]*3
    margins = [M[i]-b[i]-h[i]*(delta[i]+sum(L[i][j]*M[j] for j in range(6)))
               for i in range(6)]
    if min(margins)<=0:
        raise ArithmeticError('exact local tube inequalities failed')
    return {'field_ranges':B,'residual_bounds':delta,'lipschitz_bounds':L,
            'strict_margins':margins,'conditional_on_supplied_inflow_errors':True,
            'full_candidate_PDE_certified':False}
