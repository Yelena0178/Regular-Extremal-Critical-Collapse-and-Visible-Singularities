"""Independent exact polynomial audit of the u-constrained outward kernel."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import numpy as np

from charged_u_interval_kernel import (NAMES,FIELDS,JACOBIAN,V,U_COMPONENTS,
    coefficients,residual_numerators,cell_bounds,jacobian_upper)
from verify_charged_interval_kernel import require,fixed_bernstein
from verify_neutral_transport import evaluate as exact_value
from verify_null_infinity_algebra import sym
from rational_transport_cell import interval_evaluate
from verify_horizon_seed import I
from charged_lobatto import rhs


def main():
    u,v=sym('u'),sym('v')
    polys=[4+u/8+v/16+u**3*v**2/256,
        Q(1,2)+u/64+v/128,Q(1,8)+u/32+v/64,-Q(1,4)+u*v/128,
        -Q(1,2)-u/128,Q(1,4)+u*v/64,-Q(1,8)+u*u*v/256,
        Q(3,2)+v/32,Q(1,4)+u/64-v/128,Q(1,8)+u/32+v*v/128,
        Q(3,4)+u/128+v/256,Q(1,8)+u/64+u*v/128]
    hu,hv=Q(1,8),Q(1,16);arrays=[np.empty((2,2,12)) for _ in range(4)]
    for i in (0,1):
        for j in (0,1):
            for k,p in enumerate(polys):
                point=dict(u=Q(i),v=Q(j))
                for array,d in zip(arrays,[p,p.partial('u')/hu,p.partial('v')/hv,
                    p.partial('u').partial('v')/(hu*hv)]):array[i,j,k]=float(exact_value(d,point))
    c=coefficients(*arrays,V.rational(hu),V.rational(hv))
    B,delta=cell_bounds(c,V.rational(hu),V.rational(hv))
    r=sym('r');den=[sym('one'),r,r*r,r*r,r**3,r**3,r**3,2*r*r,r,r,sym('one'),r*r]
    nums=residual_numerators(c,V.rational(hu),V.rational(hv))
    exact_B=[fixed_bernstein(p,3,3) for p in polys];rm=exact_B[0][0]
    lower=[Q(1),rm,rm**2,rm**2,rm**3,rm**3,rm**3,2*rm**2,rm,rm,Q(1),rm**2]
    for j,(field,d,num) in enumerate(zip(FIELDS,den,nums)):
        du=j in U_COMPONENTS
        deriv=polys[j].partial('u' if du else 'v')/(hu if du else hv)
        expr=(d*(sym('di')-field)).substitute(dict(zip(NAMES,polys))|dict(di=deriv,one=1))
        lo,hi=fixed_bernstein(expr,num.lo.shape[-2]-1,num.lo.shape[-1]-1)
        require(Q(float(delta[0,0,j]))>=max(abs(lo),abs(hi))/lower[j],
                'exact u-constrained residual '+str(j))
    low=np.array([float(a-Q(1,1024)) for a,b in exact_B])
    high=np.array([float(b+Q(1,1024)) for a,b in exact_B])
    L=jacobian_upper(low[None],high[None])[0]
    box={name:I(Q(float(low[j])),Q(float(high[j]))) for j,name in enumerate(NAMES)}
    for i,row in enumerate(JACOBIAN):
        for j,p in enumerate(row):
            want=interval_evaluate(p,box)
            require(Q(float(L[i,j]))>=max(abs(want.lo),abs(want.hi)),'exact u Jacobian')
    point={name:(a+b)/2 for name,(a,b) in zip(NAMES,exact_B)}
    x=np.array([float(point[name]) for name in NAMES]);expected=rhs(x)
    rr,kk,tr,ti,nu,zr,zi,m,pr,pi,q,a=x
    expected[7]=q*q*nu/(2*rr*rr)+(1-2*m/rr)*nu*(zr*zr+zi*zi)/2
    expected[8]=nu*zr/rr+.6*a*pi;expected[9]=nu*zi/rr-.6*a*pr
    expected[10]=-.6*rr*nu*(pi*zr-pr*zi)
    got=np.array([float(exact_value(p,point)) for p in FIELDS])
    require(np.max(abs(got-expected))<2e-15,'independent u RHS')
    result=dict(status='PASS',exact_residual_components=12,rational_Jacobian_comparisons=144,
        independent_RHS_components=12,U_components=list(U_COMPONENTS),
        scope='outward kernel only',complete_rectangle_certified=False,goal_A_proved=False)
    folder=Path(__file__).resolve().parent
    names=['verify_charged_u_kernel.py','charged_u_interval_kernel.py','charged_interval_kernel.py',
        'interval_transport_grid.py','verify_charged_interval_kernel.py','rational_transport_cell.py',
        'verify_horizon_seed.py','verify_null_infinity_algebra.py','verify_neutral_transport.py','charged_lobatto.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'CHARGED_U_KERNEL_CHECKS_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
