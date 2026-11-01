"""Necessary charge-capacity screen with measured geometry/amplitude held fixed.

This does not construct a modified solution or rule out the candidate family.
"""
from hashlib import sha256
import argparse
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def summarize():
    rows=[]
    sources={}
    for steps in (512,1024):
        name=f'SPLIT_FOCUSING_RAYS_N{steps}_2026-11-01.json'
        path=ROOT/name
        obj=json.loads(path.read_text(encoding='utf-8'))
        if not obj['completed']:
            raise ValueError('incomplete focusing probe')
        for source,digest in obj['source_sha256'].items():
            if sha256((ROOT/source).read_bytes()).hexdigest()!=digest:
                raise ValueError('stale source: '+source)
        sources[name]=sha256(path.read_bytes()).hexdigest()
        budgets={row['u']:row for row in obj['diagnostics']['null_ray_budgets']}
        for ray in obj['diagnostics']['target_ray_traces']:
            first=ray['first_negative']
            if first is None:
                raise ValueError('expected diagnostic crossing was absent')
            q0=budgets[ray['u']]['initial_Q']
            B=first['entry_expansion']-first['amplitude_cost']
            H,r=first['capacity'],first['radius']
            if not all(math.isfinite(x) and x>0 for x in (B,H,r,first['focusing'])):
                raise ValueError('invalid denominator in capacity diagnostic')
            qcap=abs(q0)+.6*math.sqrt(H*B)
            h_required=max(r-abs(q0),0.)**2/(.36*B)
            rows.append({'steps':steps,'u':ray['u'],'time':first['time'],
                         'radius':r,'charge':first['Q'],'entry_charge':q0,
                         'entry_expansion':first['entry_expansion'],
                         'total_focusing':first['focusing'],
                         'amplitude_cost':first['amplitude_cost'],
                         'amplitude_share_of_focusing':first['amplitude_cost']/first['focusing'],
                         'phase_cost':first['phase_cost'],
                         'minimum_charge_cost':first['minimum_charge_cost'],
                         'phase_excess':first['phase_excess'],
                         'remaining_budget_after_amplitude':B,
                         'slack_after_minimum_phase_cost':B-first['minimum_charge_cost'],
                         'capacity_H':H,'recorded_abs_Q_over_r':abs(first['Q'])/r,
                         'necessary_charge_cap_with_frozen_inputs':qcap,
                         'necessary_charge_cap_over_r':qcap/r,
                         'required_H_for_abs_Q_equal_r_with_fixed_other_inputs':h_required,
                         'required_H_multiplier':h_required/H,
                         'raychaudhuri_defect_at_crossing':first['raychaudhuri_defect'],
                         'charge_defect_at_crossing':first['charge_integral_defect']})
    sources['summarize_split_focusing.py']=sha256(Path(__file__).read_bytes()).hexdigest()
    return {'claim':'FOCUS01 conditional necessary screen on recorded finite trajectories',
            'rows':rows,'source_sha256':sources,
            'frozen_inputs':['amplitude cost','weighted amplitude capacity','entry expansion','entry charge','radius'],
            'limitations':['finite sampled trajectories without a PDE error certificate',
                           'an optimized phase changes the real geometry and amplitude',
                           'endpoint budget is necessary only; every earlier prefix must also be controlled',
                           'does not exclude other parameters or a purely asymptotic endpoint'],
            'finite_PDE_error_certified':False,'goal_A_proved':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=summarize()
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    for row in result['rows']:
        print(json.dumps({k:row[k] for k in ['steps','u','amplitude_share_of_focusing',
                                             'slack_after_minimum_phase_cost','recorded_abs_Q_over_r',
                                             'necessary_charge_cap_over_r','required_H_multiplier']}))
