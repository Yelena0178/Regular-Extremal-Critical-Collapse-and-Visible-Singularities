"""E0 corner-graded comparison; the C0 boundary jump remains uncertified."""

from hashlib import sha256
import json
import math
from pathlib import Path

import numpy as np

from new_shape_jets import Configuration
from charged_characteristic_screen import boundary,evolve,diagnostics


def graded_mesh(base,S,cap,beta,n):
    first_end=cap+S*beta*base['v1']
    delta=2.**-20;transition=cap+4096*delta
    if transition>=first_end:raise ValueError('onset too short for this grading')
    first=[cap]+[cap+delta*2**j for j in range(13)]
    first+=list(np.linspace(transition,first_end,n+1)[1:])
    middle=cap+S*beta*base['v1']*np.exp(np.linspace(0.,math.log(base['v2']/base['v1']),n+1))
    final=cap+S*beta*np.linspace(base['v2'],1.,n+1)
    return np.concatenate([first,middle[1:],final[1:]])


def point_constraints(data,i,j):
    x=data['state'];du=data['u'][1]-data['u'][0];xx=x[i,j]
    xu=(x[i-2,j]-8*x[i-1,j]+8*x[i+1,j]-x[i+2,j])/(12*du)
    offsets=data['v'][j-2:j+3]-data['v'][j]
    scale=max(abs(offsets));z=offsets/scale
    weights=np.linalg.solve(np.array([z**k for k in range(5)]),[0.,1.,0.,0.,0.])/scale
    xv=np.sum(x[i,j-2:j+3]*weights[:,None],axis=0)
    r,k,nu,m,Q,A=xx[0],xx[1],xx[4],xx[7],xx[10],xx[11]
    phi,zz=complex(*xx[8:10]),complex(*xx[5:7]);f=1-2*m/r
    return dict(u=float(data['u'][i]),v=float(data['v'][j]),r=float(r),lambda_value=float(k*f),Q=float(Q),
                heldout_constraint_residuals=dict(radius=float(xv[0]-k*f),
                    scalar=float(abs(complex(*xu[8:10])+1j*.6*A*phi-nu*zz/r)),
                    charge=float(xu[10]+.6*r*nu*(phi*np.conj(zz)).imag),
                    mass=float(xu[7]-Q*Q*nu/(2*r*r)-f*nu*abs(zz)**2/2)))


def main():
    folder=Path(__file__).resolve().parent
    source='NEW_SHAPE_JETS_2026-10-17.json';roots=json.loads((folder/source).read_text())
    root=next(run for run in roots['runs'] if run['configuration']['beta']==.0003)
    cfg=Configuration(**root['configuration'])
    out,inc,base,S,cap=boundary(root['parameters'],cfg)
    runs=[]
    for n in (48,96,192):
        v=graded_mesh(base,S,cap,cfg.beta,n)
        data=evolve(out,inc,.95*cap,v,n)
        report=dict(steps_u=n,steps_v=len(v)-1,first_v_width=float(v[1]-v[0]),
                    evidence='E0_graded_C0_charged_pre_axis',**diagnostics(data))
        # Same two physical coordinates on every mesh; extra corner nodes do
        # not shift the quoted sample locations.
        report['fixed_points']=[point_constraints(data,n//2,n+13+n//2),
                                point_constraints(data,n//2,2*n+13+n//2)]
        runs.append(report);print(json.dumps(report),flush=True)
    result=dict(runs=runs,scope='corner grading of the C0 approximation only',
                actual_smooth_PDE_certified=False,actual_trapping_certified=False,
                full_AF_Cauchy_realization=False,goal_A_proved=False)
    names=['charged_graded_screen.py','charged_characteristic_screen.py','new_shape_jets.py',source]
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'NEW_SHAPE_CHARGED_GRADED_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
