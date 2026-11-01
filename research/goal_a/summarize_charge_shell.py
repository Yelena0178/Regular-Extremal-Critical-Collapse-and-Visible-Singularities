"""Summarize the recorded finite screens without upgrading their evidence."""
import argparse
from hashlib import sha256
import json
from pathlib import Path


def summarize():
    rows = []
    for path in sorted(Path('.').glob('CHARGE_SHELL_A*_2026-10-22.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        if 'diagnostics' not in data:
            continue
        point = data.get('first_negative_sample')
        final = data['diagnostics']['fixed_radius_samples'][-1]
        outer = data['initial_data']['parameters']['radius']+data['initial_data']['parameters']['width']
        gate = next((g for g in final['gates'] if g['radius'] == outer and g['covered']), None)
        sources_match = all(sha256(Path(name).read_bytes()).hexdigest() == digest
                            for name, digest in data['source_sha256'].items())
        row = dict(report=path.name, report_sha256=sha256(path.read_bytes()).hexdigest(),
                   source_hashes_match_current=sources_match,
                   parameters=data['initial_data']['parameters'],
                   requested_time=data['requested_time'], requested_steps=data['requested_steps'],
                   completed=data['completed'], failed_time=data.get('failed_time'),
                   ADM_mass=data['initial_data']['ADM_mass'], ADM_charge=data['initial_data']['ADM_charge'],
                   minimum_sampled_lambda=data['worst']['lambda_value'],
                   first_negative=point,
                   first_negative_abs_Q_over_r=abs(point['Q'])/point['radius'] if point else None,
                   last_mass_diagnostic_time=final['time'],
                   last_mass_diagnostic_axis_time=final['axis_proper_time'],
                   fixed_outer_radius_gate=gate,
                   fixed_outer_radius_mass_fraction=gate['renormalized_mass']/data['initial_data']['ADM_mass'] if gate else None,
                   final_row_residuals=data.get('final_row_constraints', {}).get('maximum_absolute'),
                   maximum_recorded_ray_budget_defect=max(r.get('maximum_transport_defect', 0.)
                       for r in data['diagnostics']['null_ray_budgets']))
        if not sources_match:
            raise ValueError('Source snapshot unavailable or changed for '+path.name)
        rows.append(row)
    result = dict(runs=rows, all_sources_match=True, evidence='finite E0 samples',
                  initial_family_certificate='CHARGE_SHELL_INITIAL_CERTIFICATE_2026-10-22.json',
                  future_focusing_certified=False, positive_mass_long_residence_proved=False,
                  goal_A_proved=False)
    Path('CHARGE_SHELL_SCREEN_SUMMARY_2026-10-22.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    for row in rows:
        print(json.dumps({k: row[k] for k in ['report', 'completed', 'minimum_sampled_lambda',
                          'first_negative_abs_Q_over_r', 'fixed_outer_radius_mass_fraction']}))


def initial_scan():
    from charge_preserving_shell import ShellParameters, ChargePreservingShell
    rows = []
    for w in [.15, .3, .6]:
        for a in [.1, .2, .3, .4, .5]:
            for d in [0., .5, 1.]:
                try:
                    data = ChargePreservingShell(ShellParameters(amplitude=a, frequency=w, direction=d), exterior_width=2.)
                    info = data.summary()
                    row = dict(a=a, w=w, d=d, M=info['ADM_mass'], Q=info['ADM_charge'], f=info['minimum_sampled_initial_f'])
                except ArithmeticError as error:
                    row = dict(a=a, w=w, d=d, error=str(error))
                rows.append(row)
    Path('CHARGE_SHELL_INITIAL_SCAN_2026-10-22.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--initial-scan', action='store_true')
    args = parser.parse_args()
    initial_scan() if args.initial_scan else summarize()
