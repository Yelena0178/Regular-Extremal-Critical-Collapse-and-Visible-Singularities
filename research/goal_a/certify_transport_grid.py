"""Full finite-rectangle validation for the frozen resolved neutral onset."""

from fractions import Fraction as Q
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
import time
import numpy as np
from certify_onset_boundary import coarse_boundary_signature
from interval_transport_grid import (V,coefficients,cell_bounds,shared_derivatives,propagate)
from verify_interval_transport_grid import arithmetic_checks
from neutral_transport import TransportConfiguration,evolve,onset_boundaries


def main():
    start=time.monotonic();base=Path(__file__).resolve().parent
    source='ONSET_BOUNDARY_CERTIFICATE_2026-10-16.json'
    cert=json.loads((base/source).read_text(encoding='utf-8'))
    for name,want in cert['source_sha256'].items():
        if sha256((base/name).read_bytes()).hexdigest()!=want:
            raise ArithmeticError('stale boundary certificate: '+name)
    with np.errstate(over='raise',invalid='raise',divide='raise',under='ignore'):
        arithmetic=arithmetic_checks()
        outgoing,incoming,p=onset_boundaries(.05);n=cert['n']
        cfg=TransportConfiguration(steps_u=n,steps_v=n,final_u=p['v_end']/2,
                                   initial_v=p['v_cap'],final_v=31*p['v_end']/32)
        print(json.dumps(dict(stage='construct_approximation',n=n)),flush=True)
        data=evolve(outgoing,incoming,cfg);x=data['state']
        xu,xv,xuv=shared_derivatives(data)
        if not all(np.isfinite(a).all() for a in [x,xu,xv,xuv]):raise ArithmeticError('nonfinite node')
        if coarse_boundary_signature(x[0],xv[0],cfg.initial_v,cfg.final_v)!=cert['coarse_boundary_sha256']:
            raise ArithmeticError('outgoing polynomial mismatch')
        if not np.all(x[:,0,3:]==[-.5,0,0]) or not np.all(xu[:,0,3:]==0):
            raise ArithmeticError('incoming vacuum polynomial mismatch')
        hu=V.rational(Q(cfg.final_u)/n)
        hv=V.rational((Q(cfg.final_v)-Q(cfg.initial_v))/n)
        low=np.empty((n,n,6));high=np.empty_like(low);delta=np.empty_like(low)
        for first in range(0,n,8):
            last=min(first+8,n);sl=slice(first,last+1)
            c=coefficients(x[sl],xu[sl],xv[sl],xuv[sl],hu,hv)
            B,d=cell_bounds(c,hu,hv)
            low[first:last]=B.lo;high[first:last]=B.hi;delta[first:last]=d
            if first%32==0:print(json.dumps(dict(stage='outward_cell_bounds',rows_complete=last,n=n)),flush=True)
        boundary=np.array([math.nextafter(float(Q(a)),math.inf) for a in cert['outgoing_errors_r_k_theta']]+[0.,0.,0.])
        def progress(diagonal,margin):
            print(json.dumps(dict(stage='outward_propagation',diagonal=diagonal,minimum_margin=margin)),flush=True)
        radii,report=propagate(low,high,delta,hu,hv,boundary,progress)
        M=radii[-1,-1];endpoint=V(x[-1,-1])-V(M,M)
        # Actual point ranges are node value +/- the proved entire-cell radii.
        endpoint=V((V(x[-1,-1])-V(M)).lo,(V(x[-1,-1])+V(M)).hi)
        trapped=2*endpoint[5]-endpoint[0]
        if trapped.lo<=0 or endpoint.lo[0]<=0 or endpoint.lo[1]<=0 or endpoint.hi[3]>=0:
            raise ArithmeticError('strict trapped-sphere signs not certified')
        result=dict(**report,status='PASS',scope='frozen resolved neutral characteristic rectangle',
            arithmetic='outward IEEE-754 binary64 basic operations plus rational boundary certificate',
            arithmetic_assumptions=['correctly rounded binary64 basic operations','gradual underflow',
                                    'correct nextafter','Python integer and Fraction arithmetic'],
            arithmetic_checks=arithmetic,runtime=dict(python=platform.python_version(),numpy=np.__version__),
            exact_rectangle=dict(u_max=str(Q(cfg.final_u)),v_min=str(Q(cfg.initial_v)),v_max=str(Q(cfg.final_v)),n=n),
            shared_exact_dyadic_Hermite=True,outgoing_boundary_sha256=cert['coarse_boundary_sha256'],
            incoming_vacuum_polynomial_exact=True,
            endpoint_error_radii=M.tolist(),endpoint_lower=endpoint.lo.tolist(),endpoint_upper=endpoint.hi.tolist(),
            strict_2m_minus_r_lower=float(trapped.lo),
            finite_rectangle_PDE_certified=True,local_strict_trapped_sphere_certified=True,
            original_eta_seed_transfer=False,complete_AF_Cauchy_realization=False,goal_A_proved=False,
            elapsed_seconds=time.monotonic()-start,
            array_sha256={name:sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
                          for name,a in [('nodes',x),('du',xu),('dv',xv),('duv',xuv),
                                         ('field_low',low),('field_high',high),('residual_upper',delta),('radii',radii)]})
    sources=['interval_transport_grid.py','certify_transport_grid.py','verify_interval_transport_grid.py',
             'neutral_transport.py','certify_onset_boundary.py',source,'RATIONAL_GOURSAT_CERTIFICATION.md']
    result['source_sha256']={name:sha256((base/name).read_bytes()).hexdigest() for name in sources}
    (base/'FULL_TRANSPORT_GRID_CERTIFICATE_2026-10-17.json').write_text(
        json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
