"""E0 two-dimensional forecast using genuinely bounded outgoing edge errors."""

from fractions import Fraction as F
from hashlib import sha256
import json
import math
from pathlib import Path
import numpy as np
from certify_onset_boundary import coarse_boundary_signature
from neutral_transport import (TransportConfiguration,evolve,onset_boundaries,
                               fourth_derivative,geometry)
from transport_defect import residual_forecast,tube_forecast


def main():
    base=Path(__file__).resolve().parent
    certificate=json.loads((base/'ONSET_BOUNDARY_CERTIFICATE_2026-10-16.json').read_text(encoding='utf-8'))
    for source,expected in certificate['source_sha256'].items():
        if sha256((base/source).read_bytes()).hexdigest()!=expected:
            raise ArithmeticError('stale boundary certificate: '+source)
    outgoing,incoming,p=onset_boundaries(.05)
    n=certificate['n']
    cfg=TransportConfiguration(steps_u=n,steps_v=n,final_u=p['v_end']/2,
                               initial_v=p['v_cap'],final_v=31*p['v_end']/32)
    data=evolve(outgoing,incoming,cfg)
    xv=fourth_derivative(data['state'],1,data['v'][1]-data['v'][0])
    signature=coarse_boundary_signature(data['state'][0],xv[0],data['v'][0],data['v'][-1])
    if signature!=certificate['coarse_boundary_sha256']:
        raise ArithmeticError('outgoing polynomial differs from certified polynomial')
    xu=fourth_derivative(data['state'],0,data['u'][1]-data['u'][0])
    if (not np.all(data['state'][:,0,3:]==np.array([-.5,0,0]))
            or not np.all(xu[:,0,3:]==0)):
        raise ArithmeticError('incoming Hermite edge is not the exact vacuum input')
    boundary=[math.nextafter(float(F(x)),math.inf)
              for x in certificate['outgoing_errors_r_k_theta']]+[0.,0.,0.]
    low,high,residual=residual_forecast(data)
    forecast=tube_forecast(data,low,high,residual,boundary_error=boundary)
    result=dict(evidence='E0_2D_forecast_with_verified_inflow_errors',
        certified_boundary_polynomial_matches=True,incoming_vacuum_polynomial_exact=True,
        boundary_error_input=boundary,forecast=forecast,
        fixed_point=geometry(data['state'][-1,-1]),rigorous_PDE_error=False,
        actual_strict_trapping_certified=False,original_eta_seed_transfer=False)
    if forecast['completed']:
        x,M=data['state'][-1,-1],np.array(forecast['endpoint_radii'])
        result['hypothetical_2m_minus_r_lower_float']=float(2*(x[5]-M[5])-(x[0]+M[0]))
    sources=['explore_certified_boundary_tube.py','ONSET_BOUNDARY_CERTIFICATE_2026-10-16.json',
             'neutral_transport.py','transport_defect.py','certify_onset_boundary.py']
    result['source_sha256']={name:sha256((base/name).read_bytes()).hexdigest() for name in sources}
    (base/'CERTIFIED_BOUNDARY_TUBE_FORECAST_2026-10-16.json').write_text(
        json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':
    main()
