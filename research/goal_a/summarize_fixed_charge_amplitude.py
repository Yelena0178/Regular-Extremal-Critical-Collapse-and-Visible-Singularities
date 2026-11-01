"""Audit the two prescribed AMP01 contrasts; no PDE error certificate.

Initial controls use independently reconstructed free-field energies. Ray
capacities hold the recorded geometry/amplitude fixed and are necessary only.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path

import numpy as np
from probe_fixed_charge_amplitude import FixedChargeAmplitudeShell

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def initial_controls():
    base = FixedChargeAmplitudeShell('1', 15.)
    radii = np.linspace(6., 14., 65)
    base_charge = base.sol.sol(radii)[0]
    rows = []
    for scale in ('3/4', '3/2'):
        data = FixedChargeAmplitudeShell(scale, 15.)
        require(data.exact_amplitude**2 * data.exact_frequency == Fraction(3, 125),
                'exact charge product changed')
        q, f, _ = data.sol.sol(radii)
        charge_error = float(np.max(abs(q-base_charge)))
        gauss_error = hamiltonian_error = 0.
        for radius in radii:
            phi, grad, chi = data.free(float(radius))
            yy = data.sol.sol(radius)
            rhs = data.constraint_rhs(radius, yy)
            independent_gauss = .6*radius**2*np.imag(phi*np.conjugate(chi))
            independent_hamiltonian = ((1-yy[1])/radius-yy[0]**2/radius**3
                                       -radius*yy[1]*(abs(grad)**2+abs(chi)**2))
            gauss_error = max(gauss_error, abs(rhs[0]-independent_gauss))
            hamiltonian_error = max(hamiltonian_error, abs(rhs[1]-independent_hamiltonian))
        require(charge_error < 2e-8, 'pointwise initial charge control failed')
        require(gauss_error < 1e-10 and hamiltonian_error < 1e-10,
                'free-field constraint evaluator mismatch')
        require(float(np.min(f)) > 0, 'sampled initial f lost positivity')
        rows.append({'scale': scale, 'radii': len(radii),
                     'maximum_pointwise_charge_difference_from_s1': charge_error,
                     'maximum_gauss_evaluator_difference': gauss_error,
                     'maximum_hamiltonian_evaluator_difference': hamiltonian_error,
                     'minimum_sampled_f': float(np.min(f)),
                     'ADM_mass': data.ADM_mass, 'ADM_charge': data.ADM_charge})
    gradient_bound = Fraction(1096, 75)
    phase_bound = Fraction(72, 125)
    uniform_bound = Fraction(9, 4)*gradient_bound + Fraction(16, 9)*phase_bound
    require(uniform_bound == Fraction(4238, 125), 'bound arithmetic changed')
    return {'rows': rows, 'exact_charge_product': '3/125',
            'gradient_integral_bound_at_s1': str(gradient_bound),
            'phase_integral_bound_at_s1': str(phase_bound),
            'uniform_integral_bound': str(uniform_bound),
            'uniform_analytic_f_lower_bound': '(3/7)*exp(-4238/125)',
            'scope': 'finite evaluator controls plus exact rational arithmetic; not a floating ODE certificate'}


def read_checked(name, sources):
    path = ROOT/name
    obj = json.loads(path.read_text(encoding='utf-8'))
    require(bool(obj.get('source_sha256')), 'missing source receipt: '+name)
    for source, digest in obj['source_sha256'].items():
        require(sha256((ROOT/source).read_bytes()).hexdigest() == digest,
                'stale source: '+source)
    require(obj['finite_PDE_error_certified'] is False and obj['goal_A_proved'] is False,
            'unexpected evidence upgrade: '+name)
    sources[name] = sha256(path.read_bytes()).hexdigest()
    return obj


def ray_rows(obj, scale):
    budgets = {row['u']: row for row in obj['diagnostics']['null_ray_budgets']}
    rows = []
    for ray in obj['diagnostics']['target_ray_traces']:
        first = ray['first_negative']
        require(first is not None, 'expected finite crossing is absent')
        q0 = budgets[ray['u']]['initial_Q']
        B = first['entry_expansion']-first['amplitude_cost']
        H, r = first['capacity'], first['radius']
        require(all(math.isfinite(x) and x > 0 for x in (B, H, r, first['focusing'])),
                'invalid capacity denominator')
        qcap = abs(q0)+.6*math.sqrt(H*B)
        prefix = [x for x in ray['samples'] if x['time'] <= first['time']]
        require(first['time'] <= obj.get('final_time', obj.get('last_completed_time')),
                'crossing lies beyond accepted evolution')
        rows.append({'scale': scale, 'steps': obj.get('requested_steps', obj.get('time_steps')),
                     'u': ray['u'], 'time': first['time'], 'radius': r,
                     'entry_time': budgets[ray['u']]['initial_time'], 'entry_charge': q0,
                     'entry_expansion': first['entry_expansion'],
                     'charge': first['Q'], 'recorded_abs_Q_over_r': abs(first['Q'])/r,
                     'total_focusing': first['focusing'], 'amplitude_cost': first['amplitude_cost'],
                     'amplitude_share': first['amplitude_cost']/first['focusing'],
                     'phase_cost': first['phase_cost'], 'minimum_charge_cost': first['minimum_charge_cost'],
                     'phase_efficiency': first['minimum_charge_cost']/first['phase_cost'],
                     'phase_excess': first['phase_excess'], 'remaining_budget_after_amplitude': B,
                     'slack_after_minimum_phase_cost': first['necessary_slack'],
                     'capacity_H': H, 'necessary_charge_cap_over_r': qcap/r,
                     'frozen_charge_cap_over_recorded_charge': qcap/abs(first['Q']),
                     'required_H_multiplier': max(r-abs(q0), 0.)**2/(.36*B*H),
                     'minimum_sampled_prefix_B': min(x['entry_expansion']-x['amplitude_cost'] for x in prefix),
                     'minimum_sampled_prefix_slack': min(x['necessary_slack'] for x in prefix),
                     'raychaudhuri_defect_at_crossing': first['raychaudhuri_defect'],
                     'maximum_accepted_trace_raychaudhuri_defect': ray['max_raychaudhuri_defect'],
                     'maximum_accepted_trace_charge_integral_defect': ray['max_charge_integral_defect']})
    return rows


def summarize():
    sources, probes, rows, primary = {}, [], [], []
    for scale, label in (('3/4', 'S075'), ('3/2', 'S150')):
        scout_name = f'AMP_{label}_SCOUT_T15_N512_2026-11-01.json'
        scout = read_checked(scout_name, sources)
        for steps in (512, 1024):
            name = f'AMP_{label}_TRACE_T15_N{steps}_2026-11-01.json'
            obj = read_checked(name, sources)
            require(obj['initial_data']['exact_charge_product'] == '3/125', 'charge product receipt mismatch')
            require(obj['ray_selection']['scout_sha256'] == sources[scout_name], 'scout receipt mismatch')
            require(obj['completed'] == (scale == '3/2'), 'review changed completion outcome')
            if steps == 512:
                require(obj['observer_regression']['passed'], 'observer regression failed')
                require(obj['first_negative_sample'] == scout['first_negative_sample']
                        and obj['worst'] == scout['worst'], 'observer changed recorded samples')
            ray_data = ray_rows(obj, scale)
            rows.extend(ray_data)
            selected = next(x for x in ray_data if x['u'] == obj['ray_selection']['primary_u'])
            primary.append(selected)
            global_event = obj['first_negative_sample']
            probes.append({'report': name, 'scale': scale, 'steps': steps,
                           'completed': obj['completed'], 'failure': obj.get('failure'),
                           'last_accepted_time': obj.get('final_time', obj.get('last_completed_time')),
                           'failed_time': obj.get('failed_time'),
                           'global_first_negative_sample': global_event,
                           'global_first_negative_u': global_event['time']-global_event['x'],
                           'primary_u_from_scout': obj['ray_selection']['primary_u'],
                           'final_row_constraints': obj.get('final_row_constraints')})
            if scale == '3/4':
                log = name.replace('.json', '.stderr.log')
                require((ROOT/log).is_file(), 'missing failure stderr: '+log)
                sources[log] = sha256((ROOT/log).read_bytes()).hexdigest()
    baseline = []
    for steps in (512, 1024):
        obj = read_checked(f'SPLIT_FOCUSING_RAYS_N{steps}_2026-11-01.json', sources)
        baseline.extend(ray_rows(obj, '1'))
    base = next(x for x in baseline if x['steps'] == 1024 and x['u'] == 2775/256)
    high = next(x for x in primary if x['steps'] == 1024 and x['scale'] == '3/2')
    comparison = {'baseline_u': base['u'], 'high_amplitude_u': high['u'],
                  'capacity_ratio': high['necessary_charge_cap_over_r']/base['necessary_charge_cap_over_r'],
                  'H_ratio': high['capacity_H']/base['capacity_H'],
                  'remaining_amplitude_budget_ratio': high['remaining_budget_after_amplitude']/base['remaining_budget_after_amplitude'],
                  'radius_squared_ratio': (high['radius']/base['radius'])**2,
                  'scope': 'different actual rays at their own finite crossings; not a matched spacetime causal comparison'}
    sources[Path(__file__).name] = sha256(Path(__file__).read_bytes()).hexdigest()
    return {'claim': 'AMP01 fixed-charge amplitude contrast', 'initial_controls': initial_controls(),
            'probes': probes, 'primary_rows': primary, 'all_target_ray_rows': rows,
            'baseline_rows': baseline, 'high_vs_baseline_N1024': comparison,
            'source_sha256': sources, 'audit_status': 'INTERNAL_AUDIT',
            'limitations': ['finite floating trajectories without a PDE error certificate',
                            'incomplete low-amplitude evolution does not establish a physical singularity',
                            'frozen amplitude/geometry capacities are necessary only; phase optimization changes both',
                            'sampled prefix checks and same-discrete-current residuals are not independent PDE proofs',
                            'no exclusion of the family or a purely asymptotic endpoint'],
            'finite_PDE_error_certified': False, 'full_future_classified': False, 'goal_A_proved': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = summarize()
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'initial_controls': result['initial_controls'],
                      'primary_rows': [{k: row[k] for k in ('scale', 'steps', 'u', 'amplitude_share',
                                                          'necessary_charge_cap_over_r', 'required_H_multiplier')}
                                       for row in result['primary_rows']],
                      'high_vs_baseline_N1024': result['high_vs_baseline_N1024']}, indent=2))
