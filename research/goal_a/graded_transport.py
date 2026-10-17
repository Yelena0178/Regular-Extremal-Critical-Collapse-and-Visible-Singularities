"""Graded v meshes; reused outward cell kernel, local-width propagation."""

from fractions import Fraction as Q
import numpy as np
from neutral_transport import rhs,jacobian,fourth_derivative
from interval_transport_grid import V,jacobian_upper,up


def mesh(cap,end,regular_cells=384):
    cap,end=Q(cap),Q(end);delta=Q(1,2**20)
    start=cap+4096*delta
    return [cap]+[cap+delta*2**j for j in range(13)]+[
        start+(end-start)*Q(j,regular_cells) for j in range(1,regular_cells+1)]


def evolve(outgoing,incoming,u_end,v_exact,nu=384):
    u=np.linspace(0.,u_end,nu+1);v=np.array([float(x) for x in v_exact])
    x=np.empty((nu+1,len(v),6));f=np.empty_like(x);du=u[1]
    for j,w in enumerate(v):x[0,j]=outgoing(w);f[0,j]=rhs(x[0,j])
    for i,w in enumerate(u):
        value=incoming(w)
        if i==0 and np.max(abs(value-x[0,0]))>1e-10:raise ArithmeticError('corner mismatch')
        x[i,0]=value;f[i,0]=rhs(value)
    for i in range(1,nu+1):
        for j in range(1,len(v)):
            dv=float(v_exact[j]-v_exact[j-1]);h=np.array([du]*3+[dv]*3)
            base=np.concatenate([x[i-1,j,:3]+du*f[i-1,j,:3]/2,
                                 x[i,j-1,3:]+dv*f[i,j-1,3:]/2])
            value=np.concatenate([x[i-1,j,:3],x[i,j-1,3:]])
            for _ in range(16):
                new=base+h*rhs(value)/2;change=np.max(abs(new-value));value=new
                if change<2e-13:break
            if change>2e-10 or not np.isfinite(value).all() or value[0]<=0 or value[1]<=0 or value[3]>=0:
                raise ArithmeticError(f'numerical reference failed at {i},{j}')
            x[i,j]=value;f[i,j]=rhs(value)
    return dict(u=u,v=v,state=x,rhs=f)


def v_derivative(x,v_exact):
    result=np.empty_like(x);count=len(v_exact)
    for j in range(count):
        first=min(max(j-2,0),count-5);indices=np.arange(first,first+5)
        offsets=np.array([float(v_exact[k]-v_exact[j]) for k in indices])
        scale=max(abs(offsets));s=offsets/scale
        matrix=np.array([s**k for k in range(5)])
        weights=np.linalg.solve(matrix,np.array([0.,1.,0.,0.,0.]))/scale
        result[:,j]=np.sum(x[:,indices]*weights[None,:,None],axis=1)
    # The exact constant vacuum traces must remain exact, rather than carrying
    # irrelevant cancellation noise into the incoming Hermite boundary.
    return result


def derivatives(data,v_exact):
    x,f=data['state'],data['rhs'];xu=fourth_derivative(x,0,data['u'][1]);xv=v_derivative(x,v_exact)
    xu[...,:3]=f[...,:3];xv[...,3:]=f[...,3:]
    J=jacobian(x);xuv=np.empty_like(x)
    xuv[...,:3]=np.einsum('...ij,...j->...i',J[...,:3,:],xv)
    xuv[...,3:]=np.einsum('...ij,...j->...i',J[...,3:,:],xu)
    return xu,xv,xuv


def propagate(low,high,delta,hu,hv,boundary,progress=None):
    nu,nv=delta.shape[:2];radii=np.broadcast_to(boundary,(nu+1,nv+1,6)).copy()
    least=np.inf;sign_lower=np.array([np.inf]*3)
    for diagonal in range(nu+nv-1):
        ii=np.arange(max(0,diagonal-nv+1),min(nu-1,diagonal)+1);jj=diagonal-ii
        lengths=V(np.column_stack([np.full(len(ii),float(hu.lo))]*3+[hv.lo[jj]]*3),
                  np.column_stack([np.full(len(ii),float(hu.hi))]*3+[hv.hi[jj]]*3))
        edge=np.concatenate([radii[ii,jj+1,:3],radii[ii+1,jj,3:]],axis=-1)
        M=up(edge+lengths.hi*delta[ii,jj]+1e-9)
        for attempt in range(32):
            lo=(V(low[ii,jj])-V(M)).lo;hi=(V(high[ii,jj])+V(M)).hi
            if np.any(lo[...,0]<=0) or np.any(lo[...,1]<=0) or np.any(hi[...,3]>=0):
                raise ArithmeticError(f'nonpositive tube on graded diagonal {diagonal}')
            L=jacobian_upper(lo,hi);total=V(delta[ii,jj])
            for j in range(6):total=total+V(L[...,j])*V(M[...,j,None])
            margin=V(M)-V(edge)-lengths*total;passed=np.min(margin.lo,axis=-1)>0
            if passed.all():break
            matrix=np.eye(6)-lengths.hi[...,None]*L
            proposal=np.linalg.solve(matrix,(edge+lengths.hi*delta[ii,jj])[...,None])[...,0]
            if not np.isfinite(proposal).all() or np.min(proposal)<0:raise ArithmeticError('invalid graded proposal')
            candidate=up(edge+1.08*np.maximum(proposal-edge,0)+1e-9)
            M=np.where(passed[:,None],M,np.maximum(M,candidate))
        else:raise ArithmeticError(f'graded inequalities failed at {diagonal}')
        if not np.isfinite(margin.lo).all():raise ArithmeticError('nonfinite graded margin')
        least=min(least,float(np.min(margin.lo)))
        sign_lower=np.minimum(sign_lower,[np.min(lo[...,0]),np.min(lo[...,1]),np.min(-hi[...,3])])
        radii[ii+1,jj+1]=M
        if progress and diagonal%96==0:progress(diagonal,least)
    return radii,dict(verified_cells=nu*nv,minimum_strict_margin=least,
                     global_tube_lower_r_k_minus_nu=sign_lower.tolist())
