"""Exact-rational cross-checks of the charged outward polynomial kernel."""

from fractions import Fraction as Q
from hashlib import sha256
from math import comb
import json
from pathlib import Path

import numpy as np

from charged_interval_kernel import (NAMES,FIELDS,JACOBIAN,V,coefficients,
    residual_numerators,cell_bounds,jacobian_upper)
from verify_null_infinity_algebra import sym
from verify_neutral_transport import evaluate as exact_value
from rational_transport_cell import interval_evaluate
from verify_horizon_seed import I
from charged_lobatto import rhs
from verify_interval_transport_grid import arithmetic_checks


def require(ok,message):
    if not ok:raise ArithmeticError(message)


def fixed_bernstein(poly,nu,nv):
    terms=[]
    for monomial,c in poly.terms.items():
        powers=dict(monomial)
        require(not(set(powers)-{'u','v'}),'non-polynomial residual')
        a,b=powers.get('u',0),powers.get('v',0)
        require(0<=a<=nu and 0<=b<=nv,'residual degree')
        terms.append((a,b,c))
    values=[sum((c*Q(comb(i,a),comb(nu,a))*Q(comb(j,b),comb(nv,b))
                 for a,b,c in terms if a<=i and b<=j),Q(0))
            for i in range(nu+1) for j in range(nv+1)]
    return min(values),max(values)


def main():
    arithmetic=arithmetic_checks()
    u,v=sym('u'),sym('v')
    polys=[4+u/8+v/16+u**3*v**2/256,
           Q(1,2)+u/64+v/128,Q(1,8)+u/32+v/64,-Q(1,4)+u*v/128,
           -Q(1,2)-u/128,Q(1,4)+u*v/64,-Q(1,8)+u*u*v/256,
           Q(3,2)+v/32,Q(1,4)+u/64-v/128,Q(1,8)+u/32+v*v/128,
           Q(3,4)+u/128+v/256,Q(1,8)+u/64+u*v/128]
    hu,hv=Q(1,8),Q(1,16)
    arrays=[np.empty((2,2,12)) for _ in range(4)]
    for i in (0,1):
        for j in (0,1):
            for k,p in enumerate(polys):
                point=dict(u=Q(i),v=Q(j))
                derivatives=[p,p.partial('u')/hu,p.partial('v')/hv,p.partial('u').partial('v')/(hu*hv)]
                for a,d in zip(arrays,derivatives):a[i,j,k]=float(exact_value(d,point))
    c=coefficients(*arrays,V.rational(hu),V.rational(hv))
    count=0
    for k,p in enumerate(polys):
        terms={}
        for monomial,coef in p.terms.items():
            powers=dict(monomial);terms[powers.get('u',0),powers.get('v',0)]=coef
        for a in range(4):
            for b in range(4):
                want=terms.get((a,b),Q(0))
                require(Q(float(c.lo[0,0,k,a,b]))<=want<=Q(float(c.hi[0,0,k,a,b])),
                        'exact charged Hermite coefficient')
                count+=1
    B,delta=cell_bounds(c,V.rational(hu),V.rational(hv))
    r,k=sym('r'),sym('k')
    denominators=[sym('one'),r,r*r,r*r,r**3,r**3,r**3,2*k*r**3,r,r,sym('one'),r*r]
    numerators=residual_numerators(c,V.rational(hu),V.rational(hv))
    exact_B=[fixed_bernstein(p,3,3) for p in polys]
    rmin,kmin=exact_B[0][0],exact_B[1][0]
    lower_den=[Q(1),rmin,rmin*rmin,rmin*rmin,rmin**3,rmin**3,rmin**3,
               2*kmin*rmin**3,rmin,rmin,Q(1),rmin*rmin]
    for index,(field,den,num) in enumerate(zip(FIELDS,denominators,numerators)):
        derivative=polys[index].partial('u' if index<4 else 'v')/(hu if index<4 else hv)
        expression=den*(sym('di')-field)
        exact=expression.substitute(dict(zip(NAMES,polys))|dict(di=derivative,one=1))
        lo,hi=fixed_bernstein(exact,num.lo.shape[-2]-1,num.lo.shape[-1]-1)
        require(Q(float(delta[0,0,index]))>=max(abs(lo),abs(hi))/lower_den[index],
                'exact charged residual enclosure '+str(index))
    low=np.array([float(a-Q(1,1024)) for a,b in exact_B])
    high=np.array([float(b+Q(1,1024)) for a,b in exact_B])
    L=jacobian_upper(low[None],high[None])[0]
    point={name:I(Q(float(low[j])),Q(float(high[j]))) for j,name in enumerate(NAMES)}
    checks=0
    for i,row in enumerate(JACOBIAN):
        for j,p in enumerate(row):
            exact=interval_evaluate(p,point)
            require(Q(float(L[i,j]))>=max(abs(exact.lo),abs(exact.hi)),'charged Jacobian enclosure')
            checks+=1
    centre={name:(a+b)/2 for name,(a,b) in zip(NAMES,exact_B)}
    values=np.array([float(exact_value(p,centre)) for p in FIELDS])
    require(np.max(abs(values-rhs(np.array([float(centre[name]) for name in NAMES]))))<2e-15,
            'symbolic and independent vector charged rhs')
    wrong=low.copy();wrong[0]=0.
    try:jacobian_upper(wrong[None],high[None])
    except ArithmeticError:pass
    else:raise ArithmeticError('zero radius box accepted')
    result=dict(status='PASS',exact_Hermite_coefficients=count,exact_residual_components=12,
                rational_Jacobian_comparisons=checks,zero_radius_rejected=True,
                arithmetic_checks=arithmetic,
                scope='finite outward kernel only; actual candidate boundary and all cells not certified',
                actual_candidate_PDE_certified=False,goal_A_proved=False)
    folder=Path(__file__).resolve().parent
    names=['verify_charged_interval_kernel.py','charged_interval_kernel.py','interval_transport_grid.py',
           'rational_transport_cell.py','verify_horizon_seed.py','charged_lobatto.py',
           'verify_null_infinity_algebra.py','verify_interval_transport_grid.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'CHARGED_INTERVAL_KERNEL_CHECKS_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
