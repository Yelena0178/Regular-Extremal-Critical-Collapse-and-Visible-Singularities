"""E0 feasibility forecast for A-GOUR01, never a validated PDE certificate."""

import hashlib
import json
from pathlib import Path
import numpy as np
from neutral_transport import TransportConfiguration, evolve, geometry, onset_boundaries
from transport_defect import residual_forecast, tube_forecast


def main():
    folder = Path(__file__).resolve().parent
    outgoing,incoming,p = onset_boundaries(.05)
    old = json.loads((folder/'NEUTRAL_ONSET_SCAN_2026-10-16.json').read_text(encoding='utf-8'))
    reference = [r for r in old['runs'] if r['input']['smoothing_fraction']==.05][-1]['fixed_point']
    runs = []
    for n in (48,96,192,384):
        cfg = TransportConfiguration(steps_u=n,steps_v=n,final_u=p['v_end']/2,
                                     initial_v=p['v_cap'],final_v=31*p['v_end']/32)
        data = evolve(outgoing,incoming,cfg)
        low,high,residual = residual_forecast(data)
        forecasts = []
        boundary_cases = [1e-10] if n < 192 else [1e-10,[1e-6,1e-6,1e-3,0.,0.,0.]]
        for boundary in boundary_cases:
            forecast = tube_forecast(data,low,high,residual,boundary_error=boundary)
            if forecast['completed']:
                x,M = data['state'][-1,-1],np.array(forecast['endpoint_radii'])
                forecast['hypothetical_2m_minus_r_lower_float'] = float(2*(x[5]-M[5])-(x[0]+M[0]))
            forecasts.append(forecast)
        run = {**data['report'],'input':p,'fixed_point':geometry(data['state'][-1,-1]),
               'maximum_float_residual_forecast':np.max(residual,axis=(0,1)).tolist(),
               'forecasts':forecasts}
        runs.append(run)
        print(json.dumps({'n':n,'fixed_point':run['fixed_point'],'forecasts':forecasts}),flush=True)
    last = runs[-1]['fixed_point']
    comparison = {key:abs(last[key]-reference[key]) for key in ('r','nu','lambda','Omega2')}
    if max(comparison.values()) >= 1e-5:
        raise ArithmeticError('independent transport/diamond sample discrepancy')
    sources = ['neutral_transport.py','transport_defect.py','explore_transport_tube.py',
               'neutral_onset_input.py','FIRST_JET_CHECKS_2026-10-16.json',
               'RATIONAL_GOURSAT_CERTIFICATION.md','NEUTRAL_ONSET_SCAN_2026-10-16.json']
    result = {'evidence':'E0_float_tube_feasibility_with_assumed_boundary_errors',
              'goal_A_proved':False,'rigorous_PDE_error':False,
              'actual_strict_trapping_certified':False,'runs':runs,
              'independent_diamond_sample_differences':comparison,
              'no_claim':['outward_rounding','certified_boundary_errors','original_eta_layer',
                          'global_centre_future','formal_exclusion_of_A_JET01'],
              'source_sha256':{s:hashlib.sha256((folder/s).read_bytes()).hexdigest() for s in sources}}
    target = folder/'TRANSPORT_TUBE_FORECAST_2026-10-16.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
