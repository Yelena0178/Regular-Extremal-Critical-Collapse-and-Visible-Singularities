"""Replay existing exact certificates. This is not a PDE or theorem verifier."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / 'experiments'
OUT = ROOT / 'checks/generated'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def run(script, *args, reject=False, optimize=False):
    cmd = [sys.executable] + (['-O'] if optimize else [])
    cmd += [str(EX / script), *map(str, args)]
    completed = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if reject:
        require(completed.returncode != 0, 'Invalid input was accepted: ' + script)
        require('incorrect frozen profile parameters' in completed.stderr or
                'stored profile differs from exact defining expression' in completed.stderr,
                'Invalid input failed for an unexpected reason: ' + completed.stderr[-1200:])
    else:
        require(completed.returncode == 0, script + '\n' + completed.stderr[-2000:])
    return completed


def same_json(generated, original):
    require(json.loads(generated.read_text()) == json.loads(original.read_text()),
            'Certificate mismatch: ' + original.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--with-kernel', action='store_true', help='Require the optional SymPy kernel check')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    profile = OUT / 'profile.json'
    run('freeze_filtered_profile.py', '--K', '8', '--n', '88', '--sigma', '1/20', '--output', profile)
    same_json(profile, EX / 'filtered_K8_n88_sigma1over20.json')
    print('PASS: exact frozen profile regeneration', flush=True)

    j = OUT / 'J_certificate.json'
    run('certify_filtered_J.py', profile, j)
    same_json(j, EX / 'filtered_K8_n88_J_certificate.json')
    print('PASS: global J certificate', flush=True)

    admissible = OUT / 'admissible_certificate.json'
    run('certify_admissible_profile.py', profile, admissible)
    same_json(admissible, EX / 'filtered_K8_n88_admissible_certificate.json')
    print('PASS: admissible leading-family certificate', flush=True)

    optimized = OUT / 'admissible_optimized.json'
    run('certify_admissible_profile.py', profile, optimized, optimize=True)
    same_json(optimized, admissible)
    print('PASS: checks remain effective under Python -O', flush=True)

    threshold = OUT / 'threshold_certificate.json'
    threshold.write_text(run('check_first_period_thresholds.py').stdout)
    same_json(threshold, EX / 'first_period_threshold_certificate.json')
    print('PASS: sufficient first-period thresholds', flush=True)

    run('certify_admissible_profile.py', EX / 'filtered_K8_n44_sigma1over20.json', OUT / 'invalid_n44.json', reject=True)
    data = json.loads(profile.read_text())
    data['J_numerator'][142] = '0'
    tampered = OUT / 'tampered_profile.json'
    tampered.write_text(json.dumps(data))
    run('certify_admissible_profile.py', tampered, OUT / 'invalid_tampered.json', reject=True)
    print('PASS: n=44 and tampered-input rejection', flush=True)

    kernel = 'NOT_RUN_OPTIONAL_SYMPY_CHECK'
    if args.with_kernel:
        require(importlib.util.find_spec('sympy') is not None,
                'Install experiments/requirements-kernel.txt before --with-kernel')
        result = run('kernel_algebra.py')
        (OUT / 'kernel_algebra.txt').write_text(result.stdout)
        kernel = 'PASS_DISPLAYED_IDENTITIES_ONLY'

    report = {
        'snapshot_date': '2026-10-10',
        'python': platform.python_version(),
        'scope': 'EXACT_AUXILIARY_PROFILE_AND_SUFFICIENT_THRESHOLD_ARITHMETIC_ONLY',
        'checks': {
            'profile_regeneration_matches_original': True,
            'global_J_certificate_matches_original': True,
            'admissible_certificate_matches_original': True,
            'optimized_execution_matches_normal': True,
            'threshold_certificate_matches_original': True,
            'n44_rejected': True,
            'tampered_J_rejected': True,
            'optional_kernel_algebra': kernel,
        },
        'profile_sha256': hashlib.sha256(profile.read_bytes()).hexdigest(),
        'finite_amplitude_root_certified': False,
        'actual_spacetime_evolution_performed': False,
        'independent_mathematical_review_completed': False,
    }
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: bounded-scope replay completed; report in checks/generated/report.json')


if __name__ == '__main__':
    main()
