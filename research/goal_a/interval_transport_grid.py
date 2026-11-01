"""Outward binary64 interval kernel for A-GOUR01's complete finite grid.

Requires IEEE-754 binary64 basic operations with gradual underflow. Every
arithmetic ufunc is materialized and widened by nextafter; no BLAS contraction
or ordinary floating-point dot product is used to certify an inequality.
Numerical solves may propose radii, but only interval inequalities accept them.
"""

from fractions import Fraction as Q
from math import comb
import numpy as np
from neutral_transport import fourth_derivative,jacobian


def down(x): return np.nextafter(x,-np.inf)
def up(x): return np.nextafter(x,np.inf)


class V:
    def __init__(self,lo,hi=None):
        self.lo=np.asarray(lo,dtype=np.float64)
        self.hi=self.lo if hi is None else np.asarray(hi,dtype=np.float64)

    @staticmethod
    def lift(x): return x if isinstance(x,V) else V(x)

    @staticmethod
    def rational(x):
        x=Q(x);a=float(x)
        if not np.isfinite(a): raise ArithmeticError('nonfinite rational conversion')
        return V(down(a) if Q(a)>x else a,up(a) if Q(a)<x else a)

    def __getitem__(self,index): return V(self.lo[index],self.hi[index])
    def __neg__(self): return V(-self.hi,-self.lo)
    def __add__(self,other):
        other=self.lift(other)
        return V(down(self.lo+other.lo),up(self.hi+other.hi))
    __radd__=__add__
    def __sub__(self,other): return self+-self.lift(other)
    def __rsub__(self,other): return self.lift(other)+-self
    def __mul__(self,other):
        other=self.lift(other)
        products=[self.lo*other.lo,self.lo*other.hi,self.hi*other.lo,self.hi*other.hi]
        lo=down(np.minimum.reduce(products));hi=up(np.maximum.reduce(products))
        zero=((self.lo==0)&(self.hi==0))|((other.lo==0)&(other.hi==0))
        return V(np.where(zero,0.,lo),np.where(zero,0.,hi))
    __rmul__=__mul__
    def reciprocal(self):
        if np.any((self.lo<=0)&(self.hi>=0)): raise ArithmeticError('interval division by zero')
        return V(down(1/self.hi),up(1/self.lo))
    def __truediv__(self,other): return self*self.lift(other).reciprocal()
    def __rtruediv__(self,other): return self.lift(other)*self.reciprocal()
    def __pow__(self,n):
        if n<0:return self.reciprocal()**-n
        out=V(1.)
        for _ in range(n):out=out*self
        return out
    def absolute(self): return np.maximum(np.abs(self.lo),np.abs(self.hi))


def assign(target,index,value):
    value=V.lift(value)
    target.lo[index]=value.lo;target.hi[index]=value.hi


def zeros(shape): return V(np.zeros(shape),np.zeros(shape))


def add(a,b):
    n,m=max(a.lo.shape[-2],b.lo.shape[-2]),max(a.lo.shape[-1],b.lo.shape[-1])
    out=zeros(np.broadcast_shapes(a.lo.shape[:-2],b.lo.shape[:-2])+(n,m))
    sl=(Ellipsis,slice(0,a.lo.shape[-2]),slice(0,a.lo.shape[-1]))
    assign(out,sl,a)
    sl=(Ellipsis,slice(0,b.lo.shape[-2]),slice(0,b.lo.shape[-1]))
    assign(out,sl,out[sl]+b)
    return out


def multiply(a,b):
    out=zeros(np.broadcast_shapes(a.lo.shape[:-2],b.lo.shape[:-2])+
              (a.lo.shape[-2]+b.lo.shape[-2]-1,a.lo.shape[-1]+b.lo.shape[-1]-1))
    for i in range(b.lo.shape[-2]):
        for j in range(b.lo.shape[-1]):
            sl=(Ellipsis,slice(i,i+a.lo.shape[-2]),slice(j,j+a.lo.shape[-1]))
            assign(out,sl,out[sl]+a*b[...,i,j,None,None])
    return out


def derivative(a,axis,h):
    if axis==0:return a[...,1:,:]*np.arange(1,a.lo.shape[-2])[:,None]/h
    return a[...,:,1:]*np.arange(1,a.lo.shape[-1])/h


def bernstein(a):
    n,m=a.lo.shape[-2]-1,a.lo.shape[-1]-1
    first=zeros(a.lo.shape)
    for i in range(n+1):
        value=V(0.)
        for j in range(i+1):value=value+a[...,j,:]*V.rational(Q(comb(i,j),comb(n,j)))
        assign(first,(Ellipsis,i,slice(None)),value)
    second=zeros(a.lo.shape)
    for i in range(m+1):
        value=V(0.)
        for j in range(i+1):value=value+first[...,:,j]*V.rational(Q(comb(i,j),comb(m,j)))
        assign(second,(Ellipsis,slice(None),i),value)
    return V(np.min(second.lo,axis=(-2,-1)),np.max(second.hi,axis=(-2,-1)))


def shared_derivatives(data):
    x,f=data['state'],data['rhs']
    xu=fourth_derivative(x,0,data['u'][1]-data['u'][0])
    xv=fourth_derivative(x,1,data['v'][1]-data['v'][0])
    xu[...,:3]=f[...,:3];xv[...,3:]=f[...,3:]
    J=jacobian(x);xuv=np.empty_like(x)
    # These are arbitrary dyadic nodal derivatives, NOT interval calculations.
    xuv[...,:3]=np.einsum('...ij,...j->...i',J[...,:3,:],xv)
    xuv[...,3:]=np.einsum('...ij,...j->...i',J[...,3:,:],xu)
    return xu,xv,xuv


def coefficients(x,xu,xv,xuv,hu,hv):
    shape=(x.shape[0]-1,x.shape[1]-1,6,4,4)
    g=zeros(shape)
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
        value=V(0.)
        for j in range(4):
            if H[i][j]:value=value+H[i][j]*g[...,j,:]
        assign(first,(Ellipsis,i,slice(None)),value)
    for i in range(4):
        value=V(0.)
        for j in range(4):
            if H[i][j]:value=value+H[i][j]*first[...,:,j]
        assign(result,(Ellipsis,slice(None),i),value)
    return result


def cell_bounds(c,hu,hv):
    B=bernstein(c)
    r,k,t,n,z,m=[c[...,j,:,:] for j in range(6)]
    ru,ku,tu=[derivative(p,0,hu) for p in (r,k,t)]
    nv,zv,mv=[derivative(p,1,hv) for p in (n,z,m)]
    r2=multiply(r,r);kn=multiply(k,n);knz=multiply(kn,z)
    numerators=[add(ru,-n),add(multiply(r,ku),-multiply(knz,z)),
        add(multiply(r2,tu),multiply(knz,add(r,-2*m))),
        add(multiply(r2,nv),-2*multiply(kn,m)),
        add(add(multiply(r2,zv),multiply(t,r)),2*multiply(multiply(k,m),z)),
        add(2*multiply(k,mv),-multiply(t,t))]
    if np.any(B.lo[...,0]<=0) or np.any(B.lo[...,1]<=0):
        raise ArithmeticError('nonpositive reference denominator')
    rmin,kmin=V(B.lo[...,0]),V(B.lo[...,1])
    denominators=[V(1.),rmin,rmin*rmin,rmin*rmin,rmin*rmin,2*kmin]
    delta=np.stack([(V(bernstein(p).absolute())/d).hi for p,d in zip(numerators,denominators)],axis=-1)
    if not all(np.isfinite(a).all() for a in [B.lo,B.hi,delta]):
        raise ArithmeticError('nonfinite cell enclosure')
    return B,delta


def jacobian_upper(low,high):
    r,kmin=V(low[...,0]),V(low[...,1])
    _,k,t,n,z,m=[V(a) for a in np.moveaxis(np.maximum(abs(low),abs(high)),-1,0)]
    L=np.zeros(low.shape[:-1]+(6,6))
    entries={
        (0,3):V(1.),
        (1,0):k*n*z*z/r**2,(1,1):n*z*z/r,(1,3):k*z*z/r,(1,4):2*k*n*z/r,
        (2,0):k*n*z/r**2+4*k*m*n*z/r**3,(2,1):n*z/r+2*m*n*z/r**2,
        (2,3):k*z/r+2*k*m*z/r**2,(2,4):k*n/r+2*k*m*n/r**2,(2,5):2*k*n*z/r**2,
        (3,0):4*k*m*n/r**3,(3,1):2*m*n/r**2,(3,3):2*k*m/r**2,(3,5):2*k*n/r**2,
        (4,0):t/r**2+4*k*m*z/r**3,(4,1):2*m*z/r**2,(4,2):1/r,
        (4,4):2*k*m/r**2,(4,5):2*k*z/r**2,
        (5,1):t*t/(2*kmin*kmin),(5,2):t/kmin}
    for index,value in entries.items():L[...,index[0],index[1]]=value.hi
    return L


def propagate(low,high,delta,hu,hv,boundary,progress=None):
    nu,nv=delta.shape[:2]
    radii=np.broadcast_to(boundary,(nu+1,nv+1,6)).copy()
    lengths=V(np.array([float(hu.lo)]*3+[float(hv.lo)]*3),
              np.array([float(hu.hi)]*3+[float(hv.hi)]*3))
    least=np.inf;sign_lower=np.array([np.inf,np.inf,np.inf])
    for diagonal in range(nu+nv-1):
        ii=np.arange(max(0,diagonal-nv+1),min(nu-1,diagonal)+1)
        jj=diagonal-ii
        edge=np.concatenate([radii[ii,jj+1,:3],radii[ii+1,jj,3:]],axis=-1)
        M=up(edge+lengths.hi*delta[ii,jj]+1e-9)
        for attempt in range(32):
            lo=(V(low[ii,jj])-V(M)).lo;hi=(V(high[ii,jj])+V(M)).hi
            if np.any(lo[...,0]<=0) or np.any(lo[...,1]<=0) or np.any(hi[...,3]>=0):
                raise ArithmeticError(f'nonpositive tube on diagonal {diagonal}')
            L=jacobian_upper(lo,hi)
            total=V(delta[ii,jj])
            for j in range(6):total=total+V(L[...,j])*V(M[...,j,None])
            margin=V(M)-V(edge)-lengths*total
            passed=np.min(margin.lo,axis=-1)>0
            if passed.all():break
            # Numerical proposals do not certify anything. All radii, including
            # already passing cells on this diagonal, are rechecked afterwards.
            matrix=np.eye(6)-lengths.hi[:,None]*L
            proposal=np.linalg.solve(matrix,(edge+lengths.hi*delta[ii,jj])[...,None])[...,0]
            if not np.isfinite(proposal).all() or np.min(proposal)<0:
                raise ArithmeticError(f'invalid radius proposal on diagonal {diagonal}')
            proposed=up(edge+1.08*np.maximum(proposal-edge,0)+1e-9)
            M=np.where(passed[:,None],M,np.maximum(M,proposed))
        else:
            raise ArithmeticError(f'tube inequalities failed on diagonal {diagonal}')
        if not np.isfinite(margin.lo).all():raise ArithmeticError('nonfinite margin')
        least=min(least,float(np.min(margin.lo)))
        sign_lower=np.minimum(sign_lower,[np.min(lo[...,0]),np.min(lo[...,1]),np.min(-hi[...,3])])
        radii[ii+1,jj+1]=M
        if progress and diagonal%96==0:progress(diagonal,least)
    return radii,dict(verified_cells=nu*nv,minimum_strict_margin=least,
                     global_tube_lower_r_k_minus_nu=sign_lower.tolist())
