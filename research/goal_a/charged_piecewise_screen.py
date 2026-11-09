"""E0 piecewise C0 evolution with separate one-sided theta traces at joints.

Last eight inflow fields remain continuous. A common theta at a C0 joint
would be the wrong endpoint value for one of the adjacent v quadratures.
"""

from hashlib import sha256
import json
import math
from pathlib import Path

import numpy as np

from charged_characteristic_screen import boundary,evolve,rhs,diagnostics
from charged_graded_screen import point_constraints
from new_shape_jets import Configuration


def join_trace(previous,start,du):
    """Transport the right-sided first four fields along the shared u edge."""
    result=previous.copy();result[0,:4]=start[:4]
    for i in range(1,len(result)):
        old=result[i-1];fixed=old[:4]+du*rhs(old)[:4]/2
        value=result[i].copy();value[:4]=result[i-1,:4]
        for _ in range(32):
            new=fixed+du*rhs(value)[:4]/2
            change=np.max(abs(new-value[:4]));value[:4]=new
            if change<2e-12:break
        if change>2e-9 or not np.isfinite(value).all():raise ArithmeticError('right trace transport failed')
        result[i]=value
    return result


def piecewise(outgoing,incoming,U,meshes,nu):
    parts=[];du=U/nu
    for j,v in enumerate(meshes):
        out=lambda V:outgoing(V,j)
        if j==0:
            inc=incoming
        else:
            trace=join_trace(parts[-1]['state'][:,-1],out(float(v[0])),du)
            inc=lambda u:trace[int(round(u/du))]
        data=evolve(out,inc,U,v,nu)
        parts.append(data)
    return parts


def main():
    folder=Path(__file__).resolve().parent
    source='NEW_SHAPE_JETS_2026-10-17.json';roots=json.loads((folder/source).read_text())
    root=next(run for run in roots['runs'] if run['configuration']['beta']==.0003)
    cfg=Configuration(**root['configuration'])
    out,inc,base,S,cap=boundary(root['parameters'],cfg)
    runs=[]
    for n in (48,96,192,384):
        start=cap+.00390625
        onset=np.array([cap]+[cap+2.**(j-20) for j in range(13)]+
                       list(np.linspace(start,cap+S*cfg.beta*base['v1'],n+1)[1:]))
        charge=cap+S*cfg.beta*base['v1']*np.exp(np.linspace(0.,math.log(base['v2']/base['v1']),n+1))
        off=cap+S*cfg.beta*np.linspace(base['v2'],1.,n+1)
        parts=piecewise(out,inc,.95*cap,[onset,charge,off],n)
        record=dict(n=n,evidence='E0_C0_piecewise_one_sided_traces',
            fixed_points=[point_constraints(parts[1],n//2,n//2),point_constraints(parts[2],n//2,n//2)],
            endpoint_lambda=diagnostics(parts[2])['endpoint_lambda'],
            endpoint_Q=float(parts[2]['state'][-1,-1,10]),
            joint_continuous_field_errors=[float(np.max(abs(parts[j]['state'][:,-1,[0,1,4,5,6,7,8,9,10,11]]-
                parts[j+1]['state'][:,0,[0,1,4,5,6,7,8,9,10,11]]))) for j in range(2)])
        runs.append(record);print(json.dumps(record),flush=True)
    result=dict(runs=runs,scope='separate one-sided theta at C0 joints, not a smooth-root certificate',
                actual_smooth_PDE_certified=False,full_AF_Cauchy_realization=False,goal_A_proved=False)
    names=['charged_piecewise_screen.py','charged_graded_screen.py','charged_characteristic_screen.py',
           'new_shape_jets.py',source]
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'NEW_SHAPE_CHARGED_PIECEWISE_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
