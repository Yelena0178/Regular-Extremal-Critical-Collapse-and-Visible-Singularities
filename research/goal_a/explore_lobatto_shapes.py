"""E0 fourth-order shape screening, with exact one-sided C0 input convention."""

from hashlib import sha256
import cmath
import json
import math
from pathlib import Path

import numpy as np

from charged_shape_family import Shape,characteristic_data
from charged_lobatto import piecewise
from charged_graded_screen import point_constraints


def run(cfg,n):
    out,inc,base,S,cap,parameters=characteristic_data(cfg)
    def right_out(V,piece):
        state=out(V,piece)
        if piece==0 and V==cap:
            theta=cfg.radius*base['f0']*cfg.amplitude*cmath.exp(-1j*base['rate']*math.log(base['v1']))/(S*base['v1'])
            state[2:4]=[theta.real,theta.imag]
        return state
    meshes=[np.linspace(cap,cap+S*base['v1'],n+1),
            cap+S*base['v1']*np.exp(np.linspace(0.,math.log(base['v2']/base['v1']),n+1)),
            cap+S*np.linspace(base['v2'],1.,n+1)]
    parts,continuity=piecewise(right_out,inc,.95*cap,meshes,n)
    state=parts[-1]['state'];last=state[-1,-1]
    lam=state[...,1]*(1-2*state[...,7]/state[...,0])
    region=lam[2:-2,2:-2]
    return dict(R=cfg.radius,n=n,parameters=parameters,
                endpoint_lambda=float(last[1]*(1-2*last[7]/last[0])),endpoint_Q=float(last[10]),
                endpoint_r=float(last[0]),endpoint_nu=float(last[4]),
                sampled_off_segment_minimum_lambda=float(region.min()),
                fixed_points=[point_constraints(parts[1],n//2,n//2),point_constraints(parts[2],n//2,n//2)],
                continuous_u_stage_errors=continuity,
                joint_r_k_errors=[float(np.max(abs(parts[j]['state'][:,-1,:2]-parts[j+1]['state'][:,0,:2])))
                                  for j in range(2)],
                iterations=[part['iteration_report'] for part in parts],
                evidence='E0_tensor_Lobatto_C0_cone',actual_smooth_solution_certified=False,
                no_trapping_certified=False,goal_A_proved=False)


def main():
    runs=[]
    for R in (10.,11.,12.,14.):
        for n in (24,48,96):
            try:
                result=run(Shape(radius=R),n)
            except (ArithmeticError,ValueError,FloatingPointError) as error:
                result=dict(R=R,n=n,evidence='E0_failure',failure=str(error),goal_A_proved=False)
            runs.append(result)
            print(json.dumps({key:result[key] for key in ['R','n','endpoint_lambda','endpoint_Q','failure']
                              if key in result}),flush=True)
    folder=Path(__file__).resolve().parent
    result=dict(runs=runs,scope='independent C0 cones, fixed e=3/5, E0 only',
                actual_smooth_seed_transferred=False,full_AF_Cauchy_realization=False,goal_A_proved=False)
    names=['explore_lobatto_shapes.py','charged_shape_family.py','charged_lobatto.py',
           'new_shape_jets.py','charged_graded_screen.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'CHARGED_LOBATTO_SHAPES_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
