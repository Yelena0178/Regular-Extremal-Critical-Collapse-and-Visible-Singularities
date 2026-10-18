"""E0 tensor Lobatto IIIA characteristic collocation (three stages per axis).

Known-solution convergence is checked separately. No interval arithmetic,
global classification, smooth-root certificate or rigorously bounded error.
"""

import numpy as np


C=np.array([0.,.5,1.])
A=np.array([[0.,0.,0.],[5/24,1/3,-1/24],[1/6,2/3,1/6]])


def rhs(x,e=.6):
    r,k,tr,ti,nu,zr,zi,m,pr,pi,Q,Au=np.moveaxis(np.asarray(x),-1,0)
    theta,z,phi=tr+1j*ti,zr+1j*zi,pr+1j*pi
    f=1-2*m/r;a=k*(2*m-Q*Q/r)/r**2
    tu=-k*nu*f*z/r-1j*e*k*nu*Q*phi/r-1j*e*Au*theta
    zv=-theta/r-a*z+1j*e*k*Q*phi/r;pv=theta/r
    return np.stack([nu,k*nu*abs(z)**2/r,tu.real,tu.imag,a*nu,zv.real,zv.imag,
                     Q*Q*k*f/(2*r*r)+abs(theta)**2/(2*k),pv.real,pv.imag,
                     e*r*(phi*np.conj(theta)).imag,2*k*nu*Q/r**2],axis=-1)


def evolve(outgoing,incoming,U,v,nu,tolerance=3e-13):
    u=np.linspace(0.,U,nu+1);du=U/nu;nv=len(v)-1
    nodes=np.empty((nu+1,nv+1,12));right=np.empty((nv,3,4));edge=np.empty((nu,3,8))
    for j in range(nv):
        for b in range(3):right[j,b]=outgoing(float(v[j]+C[b]*(v[j+1]-v[j])))[:4]
    maximum_iterations=0;maximum_change=0.
    for i in range(nu):
        bottom=np.array([incoming(float(u[i]+c*du))[-8:] for c in C])
        for j in range(nv):
            dv=v[j+1]-v[j]
            x=np.concatenate([np.broadcast_to(right[j],(3,3,4)),
                              np.broadcast_to(bottom[:,None,:],(3,3,8))],axis=-1).copy()
            for iteration in range(80):
                f=rhs(x)
                yu=right[j][None,:,:]+du*np.einsum('aq,qbc->abc',A,f[...,:4])
                zv=bottom[:,None,:]+dv*np.einsum('bq,aqc->abc',A,f[...,4:])
                new=np.concatenate([yu,zv],axis=-1)
                change=float(np.max(abs(new-x)));x=new
                if change<tolerance:break
            if (change>1e-10 or not np.isfinite(x).all() or np.min(x[...,0])<=0 or
                    np.min(x[...,1])<=0 or np.max(x[...,4])>=0):
                raise ArithmeticError(f'Lobatto stage failed at {i},{j}; change={change}')
            maximum_iterations=max(maximum_iterations,iteration+1);maximum_change=max(maximum_change,change)
            right[j]=x[2,:,:4];bottom=x[:,2,4:]
            nodes[i+1,j+1]=x[2,2]
            if i==0:nodes[0,j+1]=x[0,2]
            if j==0:
                nodes[i+1,0]=x[2,0]
                if i==0:nodes[0,0]=x[0,0]
        edge[i]=bottom
    return dict(u=u,v=np.asarray(v),state=nodes,last_v_stages=edge,
                iteration_report=dict(maximum_iterations=maximum_iterations,
                                      maximum_last_change=maximum_change))


def piecewise(outgoing,incoming,U,meshes,nu):
    parts=[];du=U/nu;continuity=[]
    for piece,v in enumerate(meshes):
        if piece==0:
            inc=incoming
        else:
            old=parts[-1]['last_v_stages']
            continuity.append(float(np.max(abs(old[:-1,2]-old[1:,0]))))
            values=np.empty((2*nu+1,8))
            values[0::2]=np.concatenate([old[:,0],old[-1:,2]],axis=0)
            values[1::2]=old[:,1]
            inc=lambda u:values[int(round(2*u/du))]
        data=evolve(lambda V:outgoing(V,piece),inc,U,v,nu)
        parts.append(data)
    return parts,continuity
