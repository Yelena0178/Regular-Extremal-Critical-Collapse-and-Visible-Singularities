"""E0 feasibility only: compare resolved onset with a thin-layer boundary.

Sampled boundary differences are NOT interval bounds. This runner never emits
a PDE certificate, even when the downstream conditional inequalities pass.
"""

import json
from pathlib import Path
import numpy as np
from neutral_transport import onset_boundaries,TransportConfiguration,evolve
from transport_defect import residual_forecast
from interval_transport_grid import V,propagate


def main():
    base=Path(__file__).resolve().parent
    out,inc,p=onset_boundaries(.05)
    cert=json.loads((base/'ONSET_BOUNDARY_CERTIFICATE_2026-10-16.json').read_text(encoding='utf-8'))
    n=384;cap=p['v_cap'];end=31*p['v_end']/32
    cfg=TransportConfiguration(steps_u=n,steps_v=n,final_u=p['v_end']/2,initial_v=cap,final_v=end)
    data=evolve(out,inc,cfg)
    low,high,delta=residual_forecast(data)
    boundary=np.zeros((n+1,6));base_error=np.array(cert['outgoing_errors_display'])
    q=p['field_amplitude']/p['v_onset_width']
    for j in range(n):
        v=np.linspace(data['v'][j],data['v'][j+1],65)
        t=v-cap;r=p['r_cap']*np.cos(q*t)+np.sin(q*t)/(2*q)
        target=np.array([r,r/v,r*q]).T
        reference=np.array([out(x)[:3] for x in v])
        boundary[j+1,:3]=base_error+np.max(abs(target-reference),axis=0)+1e-9
    # A thin positive smooth ramp has an O(1) theta discrepancy in the first
    # cell. This is only a trial magnitude; the actual envelope is unproved.
    boundary[1,2]=max(boundary[1,2],1.)
    result=dict(evidence='E0_thin_onset_transfer_feasibility',
                maximum_trial_boundary=np.max(boundary,axis=0).tolist(),
                sampled_boundary_certified=False,actual_thin_layer_transfer=False,
                original_eta_seed_transfer=False,goal_A_proved=False)
    try:
        radii,report=propagate(low,high,delta,V(data['u'][1]),
                               V(data['v'][1]-data['v'][0]),boundary)
        M=radii[-1,-1];x=data['state'][-1,-1]
        result.update(completed=True,endpoint_radii=M.tolist(),conditional_report=report,
                      hypothetical_2m_minus_r_lower=float(2*(x[5]-M[5])-(x[0]+M[0])))
    except ArithmeticError as error:
        result.update(completed=False,failure=str(error))
    (base/'THIN_ONSET_TRANSFER_FORECAST_2026-10-17.json').write_text(
        json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
