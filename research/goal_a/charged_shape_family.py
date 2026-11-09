"""Independent C0 null cones with fixed coupling and variable frozen R.

These are finite characteristic data, not beta=0 points of a Cauchy curve.
No smoothing, nonlinear endpoint lift or future terminal state is certified.
"""

from dataclasses import dataclass,asdict
from hashlib import sha256
import json
import math
from pathlib import Path

import numpy as np

from new_shape_jets import early_fields,integrate,jet_rhs
from charged_piecewise_screen import piecewise
from charged_graded_screen import point_constraints


@dataclass(frozen=True)
class Shape:
    radius: float = 10.
    amplitude: float = .7
    radius_ratio: float = .125
    coupling: float = .6
    rtol: float = 2e-12
    atol: float = 2e-16
    max_step: float = .01


def characteristic_data(cfg):
    R,Phi,rho,e=cfg.radius,cfg.amplitude,cfg.radius_ratio,cfg.coupling
    if e!=.6 or not 0<Phi<1 or not 0<rho<1:raise ValueError('invalid fixed-e shape')
    c=math.cos(Phi);K=Phi*c*c*(1-rho*rho)/2
    s=(e*R*K)**2/(1+(e*R*K)**2)
    v2=s/(s+Phi*math.tan(Phi));v1=v2*rho**(1/s)
    f0=rho*c*(c-s*math.sin(Phi)/Phi)
    p0=rho*c*(Phi*math.sin(Phi)+s*c)/v1
    if f0<=0 or p0<=0:raise ValueError('no positive regular cap')
    rate=math.sqrt(s*(1-s))/Phi
    def charge(x):
        y=min(max(x,v1),v2)/v2
        return e*R*Phi*math.sqrt(s*(1-s))*c*c*(y**(2*s)-rho*rho)/(2*s)
    base=dict(s=s,rate=rate,v1=v1,v2=v2,C=c/v2**s,D=0.,f0=f0,p0=p0,
              fb=1.,pb=0.,qf=charge(v2),charge=charge)
    fields=early_fields(base,cfg)
    state=np.array([f0/p0,0.,0.,0.],dtype=complex)
    jets=[];potentials=[];A0=0j
    for field,end in fields:
        def ode(z,state):
            f,fx,q,phi,phiz,dx=field(z)
            return dx*jet_rhs(R*f,R*fx,R*q,phi,phiz/dx,state,e)
        sol=integrate(ode,(0.,end),state,cfg)
        jets.append(sol);state=sol.y[:,-1]
        def potential(z,state):
            f,fx,q,phi,phiz,dx=field(z)
            return [-q*dx/(2*R*f*f)]
        potential_sol=integrate(potential,(0.,end),[A0],cfg)
        potentials.append(potential_sol);A0=potential_sol.y[0,-1]
    minimum_H=min(float(np.min(sol.sol(np.linspace(sol.t[0],sol.t[-1],1025))[0].real)) for sol in jets)
    if minimum_H<=0:raise ValueError('C0 incoming expansion budget failed')
    S=2*R*p0;cap=2*R*f0
    def outgoing(V,piece=None):
        x=(V-cap)/S
        if piece==0 or (piece is None and x<=v1):j,z=0,max(0.,x/v1)
        elif piece==1 or (piece is None and x<=v2):j,z=1,math.log(x/v1)
        else:j,z=2,(x-v2)/(1-v2)
        f,fx,q,phi,phiz,dx=fields[j][0](z)
        H,T,P,K=jets[j].sol(z);H=float(H.real)
        r=R*f;nu=-S*H/(4*r);theta=r*phiz/(dx*S)
        if V==cap:theta=0j
        zz=r*P/(-H/(4*r));lam=R*fx/S
        A=float(potentials[j].sol(z)[0].real)*S
        return np.array([r,-1/(4*nu),theta.real,theta.imag,nu,zz.real,zz.imag,
                         r*(1+4*nu*lam)/2,phi.real,phi.imag,R*q,A])
    def incoming(U):return np.array([(cap-U)/2,.5,0.,0.,-.5,0.,0.,0.,0.,0.,0.,0.])
    return outgoing,incoming,base,S,cap,dict(min_sampled_H=minimum_H,
        cap_radius=cap/2,onset_length=S*v1,terminal_Q=R*base['qf'],s=s)


def meshes(base,S,cap,n):
    transition=cap+.00390625
    if transition>=cap+S*base['v1']:raise ValueError('graded layer does not fit')
    on=np.array([cap]+[cap+2.**(j-20) for j in range(13)]+
                list(np.linspace(transition,cap+S*base['v1'],n+1)[1:]))
    ch=cap+S*base['v1']*np.exp(np.linspace(0.,math.log(base['v2']/base['v1']),n+1))
    off=cap+S*np.linspace(base['v2'],1.,n+1)
    return [on,ch,off]


def run(cfg,n):
    out,inc,base,S,cap,parameters=characteristic_data(cfg)
    parts=piecewise(out,inc,.95*cap,meshes(base,S,cap,n),n)
    last=parts[-1]['state'];r,k,m,nu=last[...,0],last[...,1],last[...,7],last[...,4]
    lam=k*(1-2*m/r)
    return dict(configuration=asdict(cfg),n=n,parameters=parameters,
                endpoint_lambda=float(lam[-1,-1]),endpoint_Q=float(last[-1,-1,10]),
                endpoint_nu=float(nu[-1,-1]),endpoint_r=float(r[-1,-1]),
                fixed_points=[point_constraints(parts[1],n//2,n//2),point_constraints(parts[2],n//2,n//2)],
                evidence='E0_auxiliary_C0_cone_charged_screen',actual_smooth_seed_certified=False,
                global_no_trapping_proved=False,goal_A_proved=False)


def main():
    runs=[]
    for R in (10.,11.,12.,14.,16.):
        for n in (48,96):
            record=run(Shape(radius=R),n);runs.append(record)
            print(json.dumps(dict(R=R,n=n,endpoint_lambda=record['endpoint_lambda'],
                                  endpoint_Q=record['endpoint_Q'],parameters=record['parameters'])),flush=True)
    folder=Path(__file__).resolve().parent
    result=dict(runs=runs,scope='finite pre-axis C0 shapes, e=3/5 fixed',
                full_AF_Cauchy_realization=False,goal_A_proved=False)
    names=['charged_shape_family.py','new_shape_jets.py','charged_piecewise_screen.py',
           'charged_characteristic_screen.py','charged_graded_screen.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'CHARGED_SHAPE_FAMILY_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
