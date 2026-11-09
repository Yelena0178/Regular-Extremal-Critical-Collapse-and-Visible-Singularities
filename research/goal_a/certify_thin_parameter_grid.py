"""Full graded-grid validation uniform in cap, length and positive thin width."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import time
import numpy as np
from thin_onset_reference import boundaries
from thin_parameter_boundary import certify
from graded_transport import mesh,evolve,derivatives,propagate
from interval_transport_grid import V,coefficients,cell_bounds
from verify_interval_transport_grid import arithmetic_checks


def main():
    start=time.monotonic();base=Path(__file__).resolve().parent
    with np.errstate(over='raise',invalid='raise',divide='raise',under='ignore'):
        arithmetic=arithmetic_checks();out,inc,p,_=boundaries()
        v=mesh(p['v_cap'],31*p['v_end']/32);nu=384;nv=len(v)-1
        print(json.dumps(dict(stage='parameter_reference',steps_u=nu,steps_v=nv)),flush=True)
        data=evolve(out,inc,p['v_end']/2,v,nu);x=data['state'];xu,xv,xuv=derivatives(data,v)
        if not all(np.isfinite(a).all() for a in [x,xu,xv,xuv]):raise ArithmeticError('nonfinite reference')
        if not np.all(x[:,0,3:]==[-.5,0,0]) or not np.all(xu[:,0,3:]==0):raise ArithmeticError('vacuum edge')
        boundary,edge=certify(x[0],xv[0],v,base)
        print(json.dumps(dict(stage='parameter_boundary',**edge)),flush=True)
        hu=V.rational(Q(p['v_end']/2)/nu);widths=[V.rational(b-a) for a,b in zip(v,v[1:])]
        hv=V(np.array([float(h.lo) for h in widths]),np.array([float(h.hi) for h in widths]))
        low=np.empty((nu,nv,6));high=np.empty_like(low);delta=np.empty_like(low)
        for first in range(0,nu,8):
            last=min(nu,first+8);sl=slice(first,last+1)
            c=coefficients(x[sl],xu[sl],xv[sl],xuv[sl],hu,hv[:,None])
            B,d=cell_bounds(c,hu,hv[:,None,None]);low[first:last]=B.lo;high[first:last]=B.hi;delta[first:last]=d
            if first%32==0:print(json.dumps(dict(stage='parameter_cells',rows_complete=last)),flush=True)
        radii,report=propagate(low,high,delta,hu,hv,boundary,
            lambda diagonal,margin:print(json.dumps(dict(stage='parameter_propagation',diagonal=diagonal,margin=margin)),flush=True))
        endpoint=V((V(x[-1,-1])-V(radii[-1,-1])).lo,(V(x[-1,-1])+V(radii[-1,-1])).hi)
        trapped=2*endpoint[5]-endpoint[0]
        if trapped.lo<=0 or endpoint.lo[0]<=0 or endpoint.lo[1]<=0 or endpoint.hi[3]>=0:
            raise ArithmeticError('parameter-box trapping not certified')
        result=dict(status='PASS',scope='all cap/length parameters in the stated box and all 0<w<=2^-40',
            **report,boundary=edge,steps_u=nu,steps_v=nv,endpoint_error_radii=radii[-1,-1].tolist(),
            endpoint_lower=endpoint.lo.tolist(),endpoint_upper=endpoint.hi.tolist(),
            strict_2m_minus_r_lower=float(trapped.lo),uniform_parameter_box_trapping_certified=True,
            complete_AF_Cauchy_realization=False,goal_A_proved=False,arithmetic_checks=arithmetic,
            arithmetic_assumptions=['correctly rounded IEEE-754 binary64 operations','gradual underflow',
                                    'correct nextafter','Python integer and Fraction arithmetic'],
            elapsed_seconds=time.monotonic()-start,
            array_sha256={name:sha256(np.ascontiguousarray(a).tobytes()).hexdigest() for name,a in
                          [('nodes',x),('du',xu),('dv',xv),('duv',xuv),('low',low),('high',high),
                           ('residual_upper',delta),('boundary',boundary),('radii',radii)]},
            exact_v_mesh_sha256=sha256(json.dumps([str(a) for a in v]).encode()).hexdigest())
    sources=['certify_thin_parameter_grid.py','thin_parameter_boundary.py','thin_boundary_certificate.py',
             'thin_onset_reference.py','graded_transport.py','interval_transport_grid.py',
             'verify_interval_transport_grid.py','certify_onset_boundary.py','verify_horizon_seed.py',
             'neutral_transport.py','neutral_onset_input.py','FIRST_JET_CHECKS_2026-10-16.json',
             'ONSET_BOUNDARY_CERTIFICATE_2026-10-16.json']
    result['source_sha256']={name:sha256((base/name).read_bytes()).hexdigest() for name in sources}
    (base/'THIN_PARAMETER_GRID_CERTIFICATE_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['source_sha256','array_sha256']},indent=2),flush=True)


if __name__=='__main__':main()
