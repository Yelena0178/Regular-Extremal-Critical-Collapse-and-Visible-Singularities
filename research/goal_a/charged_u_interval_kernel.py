"""Outward kernel for A-CHG03; retains the original twelve-field ordering."""

from fractions import Fraction as Q
import numpy as np

from charged_interval_kernel import (NAMES,V,coefficients,evaluate,
    symbolic_rhs as original_rhs,residual_numerators as original_residuals)
from interval_transport_grid import add,multiply,derivative,bernstein
from verify_null_infinity_algebra import sym


U_COMPONENTS=(0,1,2,3,7,8,9,10)
V_COMPONENTS=(4,5,6,11)


def symbolic_rhs():
    result=list(original_rhs())
    r,k,tr,ti,n,zr,zi,m,pr,pi,q,a=map(sym,NAMES);e=Q(3,5)
    result[7]=q*q*n/(2*r*r)+(1-2*m/r)*n*(zr*zr+zi*zi)/2
    result[8]=n*zr/r+e*a*pi
    result[9]=n*zi/r-e*a*pr
    result[10]=-e*r*n*(pi*zr-pr*zi)
    return tuple(result)


FIELDS=symbolic_rhs()
JACOBIAN=[[p.partial(name) for name in NAMES] for p in FIELDS]


def residual_numerators(c,hu,hv):
    result=original_residuals(c,hu,hv)
    r,k,tr,ti,n,zr,zi,m,pr,pi,q,a=[c[...,j,:,:] for j in range(12)]
    d={j:derivative(c[...,j,:,:],0,hu) for j in (7,8,9,10)}
    e=V.rational(Q(3,5));r2=multiply(r,r);gap=add(r,-2*m)
    zz=add(multiply(zr,zr),multiply(zi,zi))
    result[7]=add(add(2*multiply(r2,d[7]),-multiply(multiply(q,q),n)),
                  -multiply(multiply(multiply(r,gap),n),zz))
    result[8]=add(add(multiply(r,d[8]),-multiply(n,zr)),
                  -e*multiply(multiply(a,pi),r))
    result[9]=add(add(multiply(r,d[9]),-multiply(n,zi)),
                  e*multiply(multiply(a,pr),r))
    current=add(multiply(pi,zr),-multiply(pr,zi))
    result[10]=add(d[10],e*multiply(multiply(r,n),current))
    return result


def cell_bounds(c,hu,hv):
    B=bernstein(c)
    if np.any(B.lo[...,0]<=0) or np.any(B.lo[...,1]<=0):
        raise ArithmeticError('u-constrained denominator nonpositive')
    r=V(B.lo[...,0]);r2=r*r;r3=r2*r
    den=[V(1),r,r2,r2,r3,r3,r3,2*r2,r,r,V(1),r2]
    delta=np.stack([(V(bernstein(p).absolute())/d).hi
        for p,d in zip(residual_numerators(c,hu,hv),den)],axis=-1)
    if not np.isfinite(delta).all():raise ArithmeticError('nonfinite u-constrained residual')
    return B,delta


def jacobian_upper(low,high):
    if np.any(low[...,0]<=0) or np.any(low[...,1]<=0):
        raise ArithmeticError('u-constrained Jacobian domain')
    states={name:V(low[...,j],high[...,j]) for j,name in enumerate(NAMES)}
    result=np.empty(low.shape[:-1]+(12,12));cache={}
    for i,row in enumerate(JACOBIAN):
        for j,p in enumerate(row):result[...,i,j]=evaluate(p,states,cache).absolute()
    if not np.isfinite(result).all():raise ArithmeticError('nonfinite u-constrained Jacobian')
    return result
