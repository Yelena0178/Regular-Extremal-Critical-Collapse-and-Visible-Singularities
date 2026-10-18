"""A different E0 candidate: an infinite exponential charged scalar tail.

Exact analytic null constraints replace finite-time RN gluing. The finite
Goursat experiments below do not prove smoothness at onset, criticality,
global evolution, or an asymptotically flat Cauchy realization.
"""

from dataclasses import dataclass,asdict
from hashlib import sha256
import json
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import j0,j1

from charged_lobatto import evolve


@dataclass(frozen=True)
class Tail:
    c: float = 1.
    frequency_ratio: float = 1.
    decay: float = 1.
    coupling: float = .6


def characteristic_data(cfg):
    c,xi,gamma,e=cfg.c,cfg.frequency_ratio,cfg.decay,cfg.coupling
    if not (0<c<=1 and xi>0 and gamma>0 and e==.6):raise ValueError('tail parameter domain')
    omega=xi*gamma;a=c/np.sqrt(1+xi*xi);Bc=j0(c)**2+j1(c)**2
    R=2*gamma/(e*a*a*omega*Bc)
    f0=j0(c);fp0=gamma*c*j1(c)
    cap=2*R*f0;scale=2*R*fp0
    def values(v):
        x=c*np.exp(-gamma*np.asarray(v));f=j0(x)
        fp=gamma*x*j1(x);q=1-(x*x/(c*c))*(j0(x)**2+j1(x)**2)/Bc
        phi=a*np.exp((-gamma-1j*omega)*np.asarray(v))
        return f,fp,q,phi
    def ode(v,y):
        f,fp,q,phi=values(v)
        return [1-q*q/(f*f)]
    # Proposal only; the accompanying analytic inequalities, not this solve,
    # establish H>0 for the exact cone.
    H=solve_ivp(ode,(0.,12/gamma),[f0/fp0],method='DOP853',rtol=3e-13,atol=2e-14,dense_output=True,max_step=.05/gamma)
    if not H.success:raise ArithmeticError(H.message)
    def outgoing(V):
        v=(V-cap)/scale;f,fp,q,phi=values(v);h=H.sol(v)[0]
        r=R*f;k=r/(scale*h);theta=r*(-gamma-1j*omega)*phi/scale
        return np.array([r,k,theta.real,theta.imag])
    def incoming(u):
        return np.array([(cap-u)/2,.5,0.,0.,-.5,0.,0.,0.,a,0.,0.,0.])
    return outgoing,incoming,cap,scale,R,values,dict(amplitude=a,radius=R,cap=cap,
        scale=scale,initial_H=f0/fp0,Bc=Bc)


def run(cfg,n=48,T=4.,fraction=.95):
    start=time.monotonic()
    out,inc,cap,S,R,values,parameters=characteristic_data(cfg)
    mesh=cap+S*np.linspace(0.,T/cfg.decay,n+1)
    part=evolve(out,inc,fraction*cap,mesh,n)
    x=part['state'];r,k,m,nu=x[...,0],x[...,1],x[...,7],x[...,4]
    lam=k*(1-2*m/r)
    # Independent centered differential constraints, strictly diagnostics.
    du=fraction*cap/n;dv=S*T/(cfg.decay*n)
    rv=(r[1:-1,2:]-r[1:-1,:-2])/(2*dv)
    r_constraint=rv-lam[1:-1,1:-1]
    endpoint=x[-1,-1]
    return dict(configuration=asdict(cfg),n=n,dimensionless_T=T,U_fraction=fraction,
        parameters=parameters,endpoint_lambda=float(lam[-1,-1]),
        minimum_sampled_lambda=float(lam.min()),minimum_sampled_radius=float(r.min()),
        maximum_sampled_nu=float(nu.max()),endpoint_state=endpoint.tolist(),
        radius_constraint_max=float(abs(r_constraint).max()),
        iterations=part['iteration_report'],elapsed_seconds=time.monotonic()-start,
        evidence='E0 finite C0-onset analytic-tail cone only',
        actual_smooth_seed_certified=False,global_no_trapping_proved=False,goal_A_proved=False)


def main(n=48,refine=False):
    records=[]
    configs=[Tail(c,xi) for c in (.5,.75,1.) for xi in (.5,1.,2.)]
    if refine:configs=[Tail(.5,1.),Tail(.75,1.),Tail(1.,1.)]
    for cfg in configs:
        try:record=run(cfg,n)
        except (ArithmeticError,ValueError,FloatingPointError) as error:
            record=dict(configuration=asdict(cfg),n=n,failure=str(error),goal_A_proved=False)
        records.append(record)
        print(json.dumps({key:record[key] for key in ['configuration','n','endpoint_lambda',
            'minimum_sampled_lambda','radius_constraint_max','failure'] if key in record}),flush=True)
    folder=Path(__file__).resolve().parent
    names=['exponential_tail_candidate.py','charged_lobatto.py']
    result=dict(runs=records,scope='new infinite-tail constraint seed; finite Goursat experiment',
        actual_smooth_seed_certified=False,full_AF_Cauchy_realization=False,goal_A_proved=False,
        source_sha256={name:sha256((folder/name).read_bytes()).hexdigest() for name in names})
    name=f'EXPONENTIAL_TAIL_SCREEN_N{n}_2026-10-17.json'
    (folder/name).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,default=48)
    parser.add_argument('--refine',action='store_true');args=parser.parse_args()
    main(args.n,args.refine)
