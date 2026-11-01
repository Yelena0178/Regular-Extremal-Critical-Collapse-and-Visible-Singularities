"""Evidence audit for the finite Cauchy screen; no PDE-error certification."""
import json
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
import numpy as np


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def lam(state):
    return state[:, 1]*(1-2*state[:, 7]/state[:, 0])


def source_path(folder, name, digest):
    candidates = [folder/name, folder/'checkpoints/canonical_cauchy_v1_2026-10-22'/name]
    for candidate in candidates:
        if candidate.is_file() and sha256(candidate.read_bytes()).hexdigest() == digest:
            return candidate.relative_to(folder).as_posix()
    raise ArithmeticError('unresolved historical source '+name)


def load_run(folder, stem):
    path = folder/(stem+'.json')
    report = json.loads(path.read_text(encoding='utf-8'))
    require(report['completed'] and not report['finite_PDE_error_certified'], 'wrong evidence status')
    info = report['initial_data']
    require(sha256((folder/info['canonical_input']).read_bytes()).hexdigest() == info['canonical_sha256'],
            'canonical input hash drift')
    sources = {name: source_path(folder, name, digest) for name, digest in report['source_sha256'].items()}
    with np.load(path.with_suffix('.npz')) as raw:
        arrays = dict(raw)
    state, x = arrays['state'], arrays['x']
    require(np.isfinite(state).all() and (state[:, 0] > 0).all()
            and (state[:, 1] > 0).all() and (state[:, 4] < 0).all(), 'nonregular stored row')
    require(len(x) == len(state) and (np.diff(x) > 0).all(), 'stored row coordinates')
    final_lambda = lam(state)
    require(report['worst']['lambda_value'] <= float(min(final_lambda))+1e-12, 'inconsistent recorded minimum')
    summary = dict(report=path.name, steps=report['time_steps'], final_time=report['final_time'],
        parameter=info['parameter'], worst=report['worst'], first_negative_sample=report['first_negative_sample'],
        final_minimum_lambda=float(min(final_lambda)),
        final_minimum_location=float(x[np.argmin(final_lambda)]),
        final_constraints=report['final_row_constraints'],
        actual_sources=sources,
        sampled_positive=report['worst']['lambda_value'] > 0,
        continuous_no_trapping_certified=False)
    return summary, arrays


def comparisons(records):
    rows = []
    for (coarse, a), (fine, b) in zip(records, records[1:]):
        x, xf = a['x'], b['x']
        indices = np.rint((x-xf[0])/(xf[1]-xf[0])).astype(int)
        mask = (indices >= 0) & (indices < len(xf))
        indices, x = indices[mask], x[mask]
        require(np.max(abs(xf[indices]-x)) < 1e-10, 'refinement coordinates do not align')
        c, f = a['state'][mask], b['state'][indices]
        near = abs(x-fine['final_minimum_location']) <= .25
        rows.append(dict(coarse_steps=coarse['steps'], fine_steps=fine['steps'],
            maximum_state_difference=float(np.max(abs(c-f))),
            maximum_lambda_difference=float(np.max(abs(lam(c)-lam(f)))),
            lambda_difference_near_final_minimum=float(np.max(abs(lam(c)[near]-lam(f)[near])))))
    finest = records[-1][0]
    xc = records[0][1]['x']
    common_x = float(xc[np.argmin(abs(xc-finest['final_minimum_location']))])
    samples = []
    for summary, arrays in records:
        j = int(np.argmin(abs(arrays['x']-common_x)))
        require(abs(arrays['x'][j]-common_x) < 1e-10, 'common observation point')
        samples.append(float(lam(arrays['state'][j:j+1])[0]))
    return dict(successive_rows=rows, common_x=common_x, lambda_at_common_x=samples,
                second_order_extrapolation=(4*samples[-1]-samples[-2])/3,
                extrapolation_is_error_bound=False)


def main():
    folder = Path(__file__).resolve().parent
    groups = {}
    files = ['audit_canonical_cauchy_screen.py']
    for label in ('A020_W8', 'A030_W4', 'A020_W8_S1001'):
        records = []
        for n in (512, 1024, 2048):
            stem = f'CANONICAL_CAUCHY_{label}_CORE_T4_N{n}_2026-10-22'
            records.append(load_run(folder, stem))
            files += [stem+'.json', stem+'.npz']
        groups[label] = dict(runs=[row[0] for row in records], refinement=comparisons(records))
    longer_stem = 'CANONICAL_CAUCHY_A020_W8_S1001_CORE_T8_N1024_2026-10-22'
    longer, _ = load_run(folder, longer_stem)
    files += [longer_stem+'.json', longer_stem+'.npz']
    base_name = 'ROTATING_CANONICAL_A020_W8_2026-10-21.npz'
    extended_name = 'ROTATING_CANONICAL_A020_W8_S1001_REFERENCE_2026-10-22.npz'
    with np.load(folder/base_name) as base, np.load(folder/extended_name) as extended:
        for key in ('r', 'jets', 'bounds'):
            require(np.array_equal(base[key], extended[key]), 'extension changed the free profile '+key)
    cert_name = 'ROTATING_AF_BARRIER_A020_W8_S1001_N4096_2026-10-22.json'
    cert = json.loads((folder/cert_name).read_text(encoding='utf-8'))
    require(cert['status'] == 'PASS' and cert['segments_checked'] == cert['segments_total'] == 868,
            'incomplete extended initial certificate')
    require(cert['profile_parameter'] == dict(numerator=1001, denominator=1000), 'wrong exact parameter')
    require(Fraction(cert['minimum_certified_lower_f']) > Fraction(3, 10000), 'extended f lower bound')
    require(cert['input_sha256'] == sha256((folder/extended_name).read_bytes()).hexdigest(), 'extended input hash')
    for name, digest in cert['source_sha256'].items():
        require(sha256((folder/name).read_bytes()).hexdigest() == digest, 'certificate source hash')
    files += [base_name, extended_name, cert_name]
    report = dict(status='PASS', groups=groups, longer_screen=longer,
        extended_initial_certificate=dict(report=cert_name, unchanged_free_profile=True,
            exact_parameter='1001/1000', all_radius_lower_f=cert['minimum_certified_lower_f'],
            entire_initial_path_interval=['0', '1001/1000']),
        source_sha256={name: sha256((folder/name).read_bytes()).hexdigest() for name in files},
        early_future_no_trapping_certified=False, original_members_trapping_certified=False,
        dispersion_branch_proved=False, extremal_endpoint_proved=False, goal_A_proved=False)
    (folder/'CANONICAL_CAUCHY_SCREEN_AUDIT_2026-10-22.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=report['status'],
        minima={key: [row['worst']['lambda_value'] for row in val['runs']] for key, val in groups.items()},
        refinements={key: val['refinement'] for key, val in groups.items()},
        extended_initial_certificate=report['extended_initial_certificate'],
        longer_screen_worst=longer['worst'], early_future_no_trapping_certified=False), indent=2))


if __name__ == '__main__':
    main()
