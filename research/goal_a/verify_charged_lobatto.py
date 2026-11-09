"""Independent exact backgrounds and charged RHS comparisons for E0 Lobatto."""

from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from charged_lobatto import rhs,evolve
from charged_characteristic_screen import rhs as scalar_rhs
from verify_neutral_transport import flrw_state


def require(ok,message):
    if not ok:raise ArithmeticError(message)


def main():
    rng=np.random.default_rng(20261017)
    x=rng.uniform(-.5,.5,(4,5,12));x[...,0]=4;x[...,1]=.4;x[...,4]=-.3
    direct=np.array([[scalar_rhs(row) for row in plane] for plane in x])
    require(np.max(abs(rhs(x)-direct))<3e-15,'batch charged RHS')
    M,Q,R=2.,1.,5.
    def flow(s,r):return [(1-2*M/r[0]+Q*Q/r[0]**2)/2]
    forward=solve_ivp(flow,(0.,4.),[R],method='DOP853',rtol=5e-14,atol=5e-15,dense_output=True)
    backward=solve_ivp(flow,(0.,-1.),[R],method='DOP853',rtol=5e-14,atol=5e-15,dense_output=True)
    def rn(u,v):
        s=v-u;r=float((forward if s>=0 else backward).sol(s)[0]);f=1-2*M/r+Q*Q/r**2
        return np.array([r,.5,0.,0.,-f/2,0.,0.,M-Q*Q/(2*r),0.,0.,Q,Q/r])
    def flrw(u,v):
        r,k,t,n,z,m=flrw_state(u,v);phi=np.sqrt(3)/2*np.log(1-(u+v)/8)
        return np.array([r,k,t,0.,n,z,0.,m,phi,0.,0.,0.])
    groups={}
    for label,exact,U,va,vb in [('RN',rn,1.,0.,4.),('FLRW',flrw,2.2,2.6,4.7)]:
        runs=[]
        for n in (8,16,32):
            data=evolve(lambda v:exact(0.,v),lambda u:exact(u,va),U,np.linspace(va,vb,n+1),n)
            err=float(np.max(abs(data['state'][-1,-1]-exact(U,vb))))
            runs.append(dict(n=n,endpoint_error=err,iterations=data['iteration_report']))
        for a,b in zip(runs,runs[1:]):require(b['endpoint_error']<a['endpoint_error']/10,'fourth order '+label)
        groups[label]=runs
    result=dict(status='PASS',batch_RHS_comparisons=20,benchmarks=groups,
                scope='observed fourth order on independent backgrounds only',
                rigorous_PDE_error=False,goal_A_proved=False)
    folder=Path(__file__).resolve().parent
    names=['verify_charged_lobatto.py','charged_lobatto.py','charged_characteristic_screen.py',
           'verify_neutral_transport.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'CHARGED_LOBATTO_CHECKS_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
