"""Cache a reproducible E0 reference for the exact-input charged cone.

The cache is a proposal for later interval verification, never a certificate.
"""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import time

import numpy as np

from frozen_charged_boundary import R,S,START,F0,P0,FLOAT,proposal,exact_mesh,SPEC
from charged_lobatto import piecewise


def main(n=96):
    start=time.monotonic();folder=Path(__file__).resolve().parent
    U=Q(19,20)*START
    nu=-S/(4*R*P0)
    if (R*F0+nu*U).lo<=0:raise ArithmeticError('axis may enter reference rectangle')
    nf=-float(S)/(4*float(R)*FLOAT[7]);rf=float(R)*FLOAT[6];kf=-1/(4*nf)
    def outgoing(V,piece):return proposal(V,piece)[0]
    def incoming(u):return np.array([rf+nf*u,kf,0.,0.,nf,0.,0.,0.,0.,0.,0.,0.])
    exact=[exact_mesh(n,j) for j in range(3)]
    meshes=[np.array([float(v) for v in edge]) for edge in exact]
    print(json.dumps(dict(stage='frozen_reference',n=n)),flush=True)
    parts,continuity=piecewise(outgoing,incoming,float(U),meshes,n)
    arrays={}
    for j,part in enumerate(parts):
        for key in ('u','v','state','last_v_stages'):arrays[f'piece{j}_{key}']=part[key]
    name=f'FROZEN_CHARGED_REFERENCE_N{n}_2026-10-17.npz'
    target=folder/name;np.savez_compressed(target,**arrays)
    endpoint=parts[-1]['state'][-1,-1];lam=endpoint[1]*(1-2*endpoint[7]/endpoint[0])
    result=dict(status='E0_REFERENCE_ONLY',n=n,exact_U=str(U),exact_meshes=[[str(v) for v in edge] for edge in exact],
                cache=name,cache_sha256=sha256(target.read_bytes()).hexdigest(),
                endpoint_lambda=float(lam),endpoint_state=endpoint.tolist(),
                shared_u_stage_errors=continuity,
                iterations=[part['iteration_report'] for part in parts],
                incoming_radius_lower=str((R*F0+nu*U).lo),elapsed_seconds=time.monotonic()-start,
                actual_PDE_error_certified=False,actual_smooth_seed_certified=False,goal_A_proved=False)
    names=['prepare_frozen_charged_reference.py','charged_lobatto.py','frozen_charged_boundary.py',SPEC]
    result['source_sha256']={source:sha256((folder/source).read_bytes()).hexdigest() for source in names}
    (folder/f'FROZEN_CHARGED_REFERENCE_N{n}_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['status','n','endpoint_lambda','shared_u_stage_errors','elapsed_seconds']}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,default=96)
    main(parser.parse_args().n)
