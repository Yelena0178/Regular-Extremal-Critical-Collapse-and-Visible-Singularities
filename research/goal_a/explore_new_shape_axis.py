"""E0 post-arrival stress test; no inference from axis closures to exact PDE."""

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

from neutral_onset_input import NeutralOnset
from neutral_characteristic import CharacteristicConfiguration, evolve, geometry, constraint_residuals
from explore_neutral_onset import summarize


def main():
    runs = []
    for epsilon in (.05, .025):
        model = NeutralOnset(radius=10., field_amplitude=.7, radius_ratio=.125,
                             smoothing_fraction=epsilon,
                             input_reference='R=10 prospective resolved onset; not the eta=2^-200 root')
        initial, p = model.make_initial()
        for n in (192, 384, 768):
            cfg = CharacteristicConfiguration(steps=n, outer_v=p['v_end'],
                                               final_u=.75*p['v_end'])
            data = evolve(initial, cfg)
            report = dict(input=p, configuration=asdict(cfg), **summarize(data))
            V = p['v_end']
            i, j = 3*n//8, 7*n//8
            if i+2 < len(data['u']):
                report['fixed_after_arrival_point'] = dict(
                    u_fraction='3/8', v_fraction='7/8', **geometry(data,i,j,True))
            report['heldout_after_arrival_constraints'] = constraint_residuals(
                data,minimum_gap=.2,u_bounds=(.3*V,.45*V),v_bounds=(.7*V,.95*V))
            runs.append(report)
            print(json.dumps(dict(epsilon=epsilon,n=n,completed_u=report['completed_u'],
                                  stop=report['stop_reason'],
                                  fixed_point=report.get('fixed_after_arrival_point'),
                                  minimum_sampled=report['minimum_sampled_lambda_with_nu_negative'],
                                  constraints=report['heldout_after_arrival_constraints'])),flush=True)
    folder = Path(__file__).resolve().parent
    result = dict(evidence='E0_post_arrival_axis_closure_stress_test',runs=runs,
                  actual_trapping_certified=False,original_thin_smooth_seed_transferred=False,
                  complete_future_classified=False,goal_A_proved=False)
    names = ['explore_new_shape_axis.py','neutral_characteristic.py','neutral_onset_input.py',
             'explore_neutral_onset.py']
    result['source_sha256'] = {name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'NEW_SHAPE_AXIS_EXPLORATION_2026-10-17.json').write_text(
        json.dumps(result,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
