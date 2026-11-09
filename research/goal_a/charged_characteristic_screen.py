"""E0 horizon-regular charged characteristic evolution, fixed e=3/5.

State r,k,Re(theta),Im(theta),nu,Re(z),Im(z),m,Re(phi),Im(phi),Q,A_u.
First four fields have u inflow; all others have v inflow. No axis treatment,
smooth-root certificate, finite-PDE error enclosure or terminal classification.
"""

from dataclasses import replace
from hashlib import sha256
import json
import math
from pathlib import Path

import numpy as np

from new_shape_jets import Configuration, evaluate, early_fields, integrate


def rhs(x,e=.6):
    r,k,tr,ti,nu,zr,zi,m,pr,pi,Q,A = x
    theta,z,phi = complex(tr,ti),complex(zr,zi),complex(pr,pi)
    f = 1-2*m/r
    a = k*(2*m-Q*Q/r)/(r*r)
    Du_theta = -k*nu*f*z/r-1j*e*k*nu*Q*phi/r
    theta_u = Du_theta-1j*e*A*theta
    z_v = -theta/r-a*z+1j*e*k*Q*phi/r
    phi_v = theta/r
    return np.array([nu,k*nu*abs(z)**2/r,theta_u.real,theta_u.imag,
                     a*nu,z_v.real,z_v.imag,Q*Q*k*f/(2*r*r)+abs(theta)**2/(2*k),
                     phi_v.real,phi_v.imag,e*r*(phi*np.conj(theta)).imag,2*k*nu*Q/(r*r)])


def boundary(parameters,cfg):
    base,back,pieces,W = evaluate(parameters,cfg,return_solution=True)
    beta,R,e = cfg.beta,cfg.radius,cfg.coupling
    S = 2*R*base['p0']/beta
    cap = 2*R*base['f0']
    fields = early_fields(base,cfg)
    potentials=[]; A0=0j
    for field,end in fields:
        def potential_rhs(z,state):
            f,fx,q,phi,phiz,dx=field(z)
            return [-beta*q*dx/(2*R*f*f)]
        sol=integrate(potential_rhs,(0.,end),[A0],cfg)
        potentials.append(sol); A0=sol.y[0,-1]
    def outgoing(V,piece=None):
        x=(V-cap)/(S*beta)
        if piece == 0 or (piece is None and x <= base['v1']):
            j,z=0,max(0.,x/base['v1'])
        elif piece == 1 or (piece is None and x <= base['v2']):
            j,z=1,math.log(x/base['v1'])
        else:
            j,z=2,(x-base['v2'])/(1-base['v2'])
        f,fx,q,phi,phiz,dx=fields[j][0](z)
        H,T,P,K=pieces[j].sol(z)
        H=float(H.real); r=R*f; nu=-S*H/(4*r)
        if H <= 0:raise ArithmeticError('boundary incoming expansion has wrong sign')
        theta=r*phiz/(beta*dx*S)
        if V == cap:theta=0j
        lam=R*fx/(beta*S)
        zz=r*P/(-H/(4*r))
        A=float(potentials[j].sol(z)[0].real)*S
        m=(r+4*nu*lam*r)/2
        return np.array([r,-1/(4*nu),theta.real,theta.imag,nu,zz.real,zz.imag,m,
                         phi.real,phi.imag,R*q,A])
    def incoming(U):
        return np.array([(cap-U)/2,.5,0.,0.,-.5,0.,0.,0.,0.,0.,0.,0.])
    return outgoing,incoming,base,S,cap


def mesh(base,S,cap,beta,n):
    # Piecewise mesh follows the actual on/log-charge/off coordinates.
    first=np.linspace(0.,base['v1'],n+1)
    second=base['v1']*np.exp(np.linspace(0.,math.log(base['v2']/base['v1']),n+1))
    third=np.linspace(base['v2'],1.,n+1)
    x=np.concatenate([first,second[1:],third[1:]])
    return cap+S*beta*x


def evolve(outgoing,incoming,U,v,nu):
    u=np.linspace(0.,U,nu+1);du=U/nu
    x=np.empty((nu+1,len(v),12));values=np.empty_like(x)
    for j,at in enumerate(v):x[0,j]=outgoing(float(at));values[0,j]=rhs(x[0,j])
    for i,at in enumerate(u):
        value=incoming(float(at))
        if i==0 and np.max(abs(value-x[0,0]))>1e-9:raise ArithmeticError('charged corner mismatch')
        x[i,0]=value;values[i,0]=rhs(value)
    for i in range(1,nu+1):
        for j in range(1,len(v)):
            dv=v[j]-v[j-1];h=np.array([du]*4+[dv]*8)
            fixed=np.concatenate([x[i-1,j,:4]+du*values[i-1,j,:4]/2,
                                  x[i,j-1,4:]+dv*values[i,j-1,4:]/2])
            value=np.concatenate([x[i-1,j,:4],x[i,j-1,4:]])
            for iteration in range(32):
                new=fixed+h*rhs(value)/2
                change=np.max(abs(new-value));value=new
                if change<2e-12:break
            if (change>2e-9 or not np.isfinite(value).all() or
                    value[0]<=0 or value[1]<=0 or value[4]>=0):
                raise ArithmeticError(f'charged E0 cell failed at {i},{j}: {change}')
            x[i,j]=value;values[i,j]=rhs(value)
    return dict(u=u,v=v,state=x)


def diagnostics(data):
    x=data['state'];r,k,nu,m=x[...,0],x[...,1],x[...,4],x[...,7]
    lam=k*(1-2*m/r)
    # Ignore boundary joints and a full near-corner buffer in reported minima.
    mask=np.ones(lam.shape,dtype=bool);mask[:2]=False;mask[-2:]=False
    mask[:,:2]=False;mask[:,-2:]=False
    at=np.unravel_index(np.argmin(np.where(mask,lam,np.inf)),lam.shape)
    i,j=at
    fixed=[]
    n=len(data['u'])-1;du=data['u'][1]-data['u'][0]
    for jj in (len(data['v'])//2,5*(len(data['v'])-1)//6):
        ii=n//2;xx=x[ii,jj]
        xu=(x[ii-2,jj]-8*x[ii-1,jj]+8*x[ii+1,jj]-x[ii+2,jj])/(12*du)
        offsets=data['v'][jj-2:jj+3]-data['v'][jj]
        scale=max(abs(offsets));normalized=offsets/scale
        weights=np.linalg.solve(np.array([normalized**k for k in range(5)]),[0.,1.,0.,0.,0.])/scale
        xv=np.sum(x[ii,jj-2:jj+3]*weights[:,None],axis=0)
        rr,kk,nn,mm,QQ,AA=xx[0],xx[1],xx[4],xx[7],xx[10],xx[11]
        pp,zz=complex(*xx[8:10]),complex(*xx[5:7]);ff=1-2*mm/rr
        scalar=complex(*xu[8:10])+1j*.6*AA*pp-nn*zz/rr
        charge=xu[10]+.6*rr*nn*(pp*np.conj(zz)).imag
        mass=xu[7]-QQ*QQ*nn/(2*rr*rr)-ff*nn*abs(zz)**2/2
        fixed.append(dict(u=float(data['u'][ii]),v=float(data['v'][jj]),r=float(rr),
                          lambda_value=float(lam[ii,jj]),Q=float(QQ),
                          heldout_constraint_residuals=dict(radius=float(xv[0]-kk*ff),
                              scalar=float(abs(scalar)),charge=float(charge),mass=float(mass))))
    return dict(minimum_sampled_lambda=float(lam[at]),minimum_location=[float(data['u'][i]),float(data['v'][j])],
                state_at_minimum=x[at].tolist(),minimum_sampled_r=float(r.min()),
                endpoint_lambda=float(lam[-1,-1]),endpoint_Q=float(x[-1,-1,10]),fixed_points=fixed)


def main():
    folder=Path(__file__).resolve().parent
    roots=json.loads((folder/'NEW_SHAPE_JETS_2026-10-17.json').read_text())
    selected=roots['runs'][-2]
    cfg=Configuration(**selected['configuration'])
    out,inc,base,S,cap=boundary(selected['parameters'],cfg)
    runs=[]
    for n in (48,96,192):
        record=dict(steps_u=n,steps_per_piece=n,beta=cfg.beta,evidence='E0_C0_charged_pre_axis',
                    completed=False,actual_trapping_certified=False,smooth_seed_transfer=False)
        try:
            v=mesh(base,S,cap,cfg.beta,n)
            data=evolve(out,inc,.95*cap,v,n)
            record.update(completed=True,**diagnostics(data))
        except (ArithmeticError,ValueError,FloatingPointError) as error:
            record['failure']=str(error)
        runs.append(record);print(json.dumps(record),flush=True)
    result=dict(runs=runs,source_root_beta=cfg.beta,goal_A_proved=False,
                finite_PDE_error_certified=False,full_AF_Cauchy_realization=False)
    names=['charged_characteristic_screen.py','new_shape_jets.py','first_jet_shooting.py',
           'second_jet_shooting.py','NEW_SHAPE_JETS_2026-10-17.json','../../definitions/MODEL.md']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'NEW_SHAPE_CHARGED_SCREEN_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
