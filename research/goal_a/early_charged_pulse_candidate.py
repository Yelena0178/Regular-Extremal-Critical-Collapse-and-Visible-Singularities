"""Alternative E0 shape: a smooth rotating bump charged throughout its support.

The fixed coupling is .6. Each independent seed has its own radius, chosen
from the terminal charge constraint; these seeds are not a critical curve.
"""

from dataclasses import dataclass,asdict
from hashlib import sha256
import json
from pathlib import Path
import time
import numpy as np
from scipy.integrate import solve_ivp

from charged_lobatto import evolve


@dataclass(frozen=True)
class Pulse:
    amplitude: float = .15
    frequency: float = 4.
    coupling: float = .6


def scalar(v,cfg):
    if v<=0 or v>=1:return 0j,0j
    d=4*v*(1-v);b=np.exp(1-1/d)
    bp=b*4*(1-2*v)/(d*d)
    phase=np.exp(-1j*cfg.frequency*v)
    return cfg.amplitude*b*phase,cfg.amplitude*(bp-1j*cfg.frequency*b)*phase


def characteristic_data(cfg):
    a,w,e=cfg.amplitude,cfg.frequency,cfg.coupling
    if not(a>0 and w>0 and e==.6):raise ValueError('pulse parameters')
    def ray(v,y):
        phi,pv=scalar(v,cfg)
        return [y[1],-abs(pv)**2*y[0]]
    fsol=solve_ivp(ray,(1.,0.),[1.,0.],method='DOP853',rtol=3e-13,atol=2e-14,dense_output=True,max_step=.005)
    if not fsol.success:raise ArithmeticError(fsol.message)
    f0,p0=fsol.y[:,-1]
    if f0<=0 or p0<=0:raise ValueError('nonpositive flat cap')
    def current(v,y):
        f=fsol.sol(v)[0];phi,pv=scalar(v,cfg)
        return [f*f*(phi*pv.conjugate()).imag]
    csol=solve_ivp(current,(0.,1.),[0.],method='DOP853',rtol=3e-13,atol=1e-16,dense_output=True,max_step=.005)
    C=csol.y[0,-1];R=1/(e*C)
    def hprime(v,y):
        f=fsol.sol(v)[0];q=csol.sol(v)[0]/C
        return [1-q*q/(f*f)]
    hsol=solve_ivp(hprime,(0.,1.),[f0/p0],method='DOP853',rtol=3e-13,atol=2e-14,dense_output=True,max_step=.005)
    sampled=np.linspace(0.,1.,2049);hmin=float(hsol.sol(sampled).min())
    if hmin<=0:raise ValueError('nonpositive sampled expansion budget')
    cap=2*R*f0;S=2*R*p0
    def outgoing(V):
        v=np.clip((V-cap)/S,0.,1.);f,fp=fsol.sol(v);h=hsol.sol(v)[0]
        phi,pv=scalar(v,cfg);r=R*f;k=r/(S*h);theta=r*pv/S
        return np.array([r,k,theta.real,theta.imag])
    def incoming(u):return np.array([(cap-u)/2,.5,0.,0.,-.5,0.,0.,0.,0.,0.,0.,0.])
    return outgoing,incoming,cap,S,R,dict(radius=R,cap=cap,scale=S,
        cap_radius_ratio=f0,initial_slope=p0,charge_integral=C,minimum_sampled_H=hmin)


def run(cfg,n=24):
    start=time.monotonic();out,inc,cap,S,R,parameters=characteristic_data(cfg)
    part=evolve(out,inc,.95*cap,cap+S*np.linspace(0.,1.,n+1),n)
    x=part['state'];r,k,m=x[...,0],x[...,1],x[...,7];lam=k*(1-2*m/r)
    return dict(configuration=asdict(cfg),n=n,parameters=parameters,
        endpoint_lambda=float(lam[-1,-1]),minimum_sampled_lambda=float(lam.min()),
        minimum_sampled_radius=float(r.min()),endpoint_state=x[-1,-1].tolist(),
        elapsed_seconds=time.monotonic()-start,iterations=part['iteration_report'],
        evidence='E0 smooth charged constraint pulse; no PDE error bound',
        actual_smooth_seed_certified=False,global_no_trapping_proved=False,goal_A_proved=False)


def main(n=24,refine=False):
    configs=[Pulse(a,w) for a in (.1,.2,.3) for w in (2.,4.,8.)]
    if refine:configs=[Pulse(.1,4.),Pulse(.2,4.),Pulse(.3,4.)]
    records=[]
    with np.errstate(over='raise',invalid='raise',divide='raise',under='ignore'):
        for cfg in configs:
            try:record=run(cfg,n)
            except (ArithmeticError,ValueError,FloatingPointError) as error:
                record=dict(configuration=asdict(cfg),n=n,failure=str(error),goal_A_proved=False)
            records.append(record)
            print(json.dumps({k:record[k] for k in ('configuration','n','endpoint_lambda',
                'minimum_sampled_lambda','parameters','failure') if k in record}),flush=True)
    folder=Path(__file__).resolve().parent;names=['early_charged_pulse_candidate.py','charged_lobatto.py']
    result=dict(runs=records,scope='independent smooth phase-onset seeds, fixed e=.6',
        actual_candidate_PDE_certified=False,full_AF_Cauchy_realization=False,goal_A_proved=False,
        source_sha256={name:sha256((folder/name).read_bytes()).hexdigest() for name in names})
    (folder/f'EARLY_CHARGED_PULSE_SCREEN_N{n}_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,default=24)
    parser.add_argument('--refine',action='store_true');args=parser.parse_args()
    main(args.n,args.refine)
