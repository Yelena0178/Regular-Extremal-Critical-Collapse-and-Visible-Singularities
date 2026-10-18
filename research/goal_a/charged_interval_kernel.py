"""Outward binary64 residual/Jacobian kernel for twelve charged fields.

This kernel alone proves no candidate spacetime or input boundary bounds.
Arithmetic assumptions are those of interval_transport_grid.V.
"""

from fractions import Fraction as Q
import numpy as np

from interval_transport_grid import V,zeros,assign,add,multiply,derivative,bernstein
from verify_null_infinity_algebra import sym


NAMES=('r','k','tr','ti','n','zr','zi','m','pr','pi','Q','A')


def symbolic_rhs():
    r,k,tr,ti,n,zr,zi,m,pr,pi,q,a=map(sym,NAMES);e=Q(3,5)
    f=1-2*m/r;rate=k*(2*m-q*q/r)/r**2
    return (n,k*n*(zr*zr+zi*zi)/r,
        -k*n*f*zr/r+e*k*n*q*pi/r+e*a*ti,
        -k*n*f*zi/r-e*k*n*q*pr/r-e*a*tr,
        rate*n,-tr/r-rate*zr-e*k*q*pi/r,
        -ti/r-rate*zi+e*k*q*pr/r,
        q*q*k*f/(2*r*r)+(tr*tr+ti*ti)/(2*k),tr/r,ti/r,
        e*r*(pi*tr-pr*ti),2*k*n*q/r**2)


def coefficients(x,xu,xv,xuv,hu,hv):
    shape=(x.shape[0]-1,x.shape[1]-1,12,4,4);g=zeros(shape)
    for i in (0,1):
        for j in (0,1):
            sl=(slice(i,x.shape[0]-1+i),slice(j,x.shape[1]-1+j))
            assign(g,(Ellipsis,i,j),V(x[sl]))
            assign(g,(Ellipsis,i+2,j),hu*V(xu[sl]))
            assign(g,(Ellipsis,i,j+2),hv*V(xv[sl]))
            assign(g,(Ellipsis,i+2,j+2),hu*hv*V(xuv[sl]))
    H=((1,0,0,0),(0,0,1,0),(-3,3,-2,-1),(2,-2,1,1))
    first=zeros(shape);result=zeros(shape)
    for i in range(4):
        total=V(0.)
        for j in range(4):
            if H[i][j]:total=total+H[i][j]*g[...,j,:]
        assign(first,(Ellipsis,i,slice(None)),total)
    for i in range(4):
        total=V(0.)
        for j in range(4):
            if H[i][j]:total=total+H[i][j]*first[...,:,j]
        assign(result,(Ellipsis,slice(None),i),total)
    return result


def residual_numerators(c,hu,hv):
    r,k,tr,ti,n,zr,zi,m,pr,pi,q,a=[c[...,j,:,:] for j in range(12)]
    d=[derivative(c[...,j,:,:],0 if j<4 else 1,hu if j<4 else hv) for j in range(12)]
    e=V.rational(Q(3,5));r2=multiply(r,r);r3=multiply(r2,r)
    kn=multiply(k,n);q2=multiply(q,q);gap=add(r,-2*m)
    b=add(2*multiply(m,r),-q2);knq=multiply(kn,q)
    zz=add(multiply(zr,zr),multiply(zi,zi));tt=add(multiply(tr,tr),multiply(ti,ti))
    return [add(d[0],-n),
        add(multiply(r,d[1]),-multiply(kn,zz)),
        add(add(multiply(r2,d[2]),multiply(multiply(kn,gap),zr)),
            add(-e*multiply(multiply(knq,pi),r),-e*multiply(multiply(a,ti),r2))),
        add(add(multiply(r2,d[3]),multiply(multiply(kn,gap),zi)),
            add(e*multiply(multiply(knq,pr),r),e*multiply(multiply(a,tr),r2))),
        add(multiply(r3,d[4]),-multiply(kn,b)),
        add(add(multiply(r3,d[5]),multiply(tr,r2)),
            add(multiply(multiply(k,b),zr),e*multiply(multiply(multiply(k,q),pi),r2))),
        add(add(multiply(r3,d[6]),multiply(ti,r2)),
            add(multiply(multiply(k,b),zi),-e*multiply(multiply(multiply(k,q),pr),r2))),
        add(add(2*multiply(multiply(k,r3),d[7]),-multiply(multiply(multiply(k,k),q2),gap)),
            -multiply(r3,tt)),
        add(multiply(r,d[8]),-tr),add(multiply(r,d[9]),-ti),
        add(d[10],-e*multiply(r,add(multiply(pi,tr),-multiply(pr,ti)))),
        add(multiply(r2,d[11]),-2*knq)]


def cell_bounds(c,hu,hv):
    B=bernstein(c)
    if np.any(B.lo[...,0]<=0) or np.any(B.lo[...,1]<=0):raise ArithmeticError('charged denominator nonpositive')
    r,k=V(B.lo[...,0]),V(B.lo[...,1]);r2=r*r;r3=r2*r
    denominators=[V(1),r,r2,r2,r3,r3,r3,2*k*r3,r,r,V(1),r2]
    delta=np.stack([(V(bernstein(p).absolute())/den).hi
                    for p,den in zip(residual_numerators(c,hu,hv),denominators)],axis=-1)
    if not np.isfinite(delta).all():raise ArithmeticError('nonfinite charged residual')
    return B,delta


FIELDS=symbolic_rhs()
JACOBIAN=[[p.partial(name) for name in NAMES] for p in FIELDS]


def evaluate(poly,states,cache=None):
    cache={} if cache is None else cache
    total=V(0.)
    for monomial,coefficient in poly.terms.items():
        term=V.rational(coefficient)
        for name,power in monomial:
            if (name,power) not in cache:cache[name,power]=states[name]**power
            term=term*cache[name,power]
        total=total+term
    return total


def jacobian_upper(low,high):
    if np.any(low[...,0]<=0) or np.any(low[...,1]<=0):raise ArithmeticError('charged Jacobian domain')
    states={name:V(low[...,j],high[...,j]) for j,name in enumerate(NAMES)}
    result=np.empty(low.shape[:-1]+(12,12));cache={}
    for i,row in enumerate(JACOBIAN):
        for j,poly in enumerate(row):result[...,i,j]=evaluate(poly,states,cache).absolute()
    if not np.isfinite(result).all():raise ArithmeticError('nonfinite charged Jacobian')
    return result
