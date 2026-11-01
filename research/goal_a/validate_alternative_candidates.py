"""Recheck evidence identities and scope for the two alternative strategies."""

from hashlib import sha256
import json
from pathlib import Path


def require(ok,message):
    if not ok:raise ArithmeticError(message)


def main():
    folder=Path(__file__).resolve().parent
    reports=['FROZEN_CHARGED_U_BOUNDARY_2026-10-17.json',
        'FROZEN_CHARGED_U_BOUNDARY_AUDIT_2026-10-17.json','CHARGED_U_KERNEL_CHECKS_2026-10-17.json',
        'EARLY_CHARGED_CONSTRAINT_CERTIFICATE_N2048_2026-10-17.json',
        'EARLY_CHARGED_CONSTRAINT_AUDIT_2026-10-17.json','EXPONENTIAL_TAIL_ALGEBRA_2026-10-17.json',
        'EXPONENTIAL_TAIL_SCREEN_N24_2026-10-17.json','EXPONENTIAL_TAIL_SCREEN_N48_2026-10-17.json',
        'EARLY_CHARGED_PULSE_SCREEN_N24_2026-10-17.json',
        'EARLY_CHARGED_REFINEMENT_48_96_2026-10-17.json','EARLY_CHARGED_REFINEMENT_192_2026-10-17.json',
        'EARLY_CHARGED_REFINEMENT_AUDIT_2026-10-17.json']
    sources=0;caches=0;loaded={}
    for name in reports:
        report=json.loads((folder/name).read_text());loaded[name]=report
        require(report['goal_A_proved'] is False,'scope inflation '+name)
        for source,want in report['source_sha256'].items():
            require(sha256((folder/source).read_bytes()).hexdigest()==want,'stale source '+source)
            sources+=1
        for run in report.get('runs',[]):
            if 'cache' in run:
                require(sha256((folder/run['cache']).read_bytes()).hexdigest()==run['cache_sha256'],
                    'stale candidate cache '+run['cache']);caches+=1
    for name in reports[:6]:require(loaded[name]['status']=='PASS','failed supporting result '+name)
    pairs=['frozen_charged_u_boundary','frozen_charged_u_boundary_audit','charged_u_kernel_checks',
        'early_charged_constraint_certificate','early_charged_constraint_audit',
        'early_charged_refinement_audit','exponential_tail_algebra']
    for base in pairs:
        require((folder/(base+'.log')).read_bytes()==(folder/(base+'_optimized.log')).read_bytes(),
            'ordinary/optimized difference '+base)
    finest=loaded['EARLY_CHARGED_REFINEMENT_192_2026-10-17.json']['runs']
    require(len(finest)==2 and all(r['minimum_sampled_lambda_u_positive']>0 for r in finest),
        'finest E0 diagnostic changed')
    summary=dict(status='VERIFIED_CONSTRAINT_AND_E0_ARTIFACTS',
        source_hashes_checked=sources,candidate_cache_hashes_checked=caches,
        ordinary_optimized_comparisons=len(pairs),certified_null_constraint_seeds=2,
        certified_null_constraint_cells=4096,certified_two_dimensional_cells_for_new_seeds=0,
        finest_grid=192,finest_E0_endpoint_lambda=[r['endpoint_lambda'] for r in finest],
        no_trapping_PDE_certificate=False,full_AF_Cauchy_realization=False,
        same_critical_curve=False,global_three_branch_terminal_states=False,goal_A_proved=False,
        report_sha256={name:sha256((folder/name).read_bytes()).hexdigest() for name in reports},
        document_sha256=sha256((folder/'ALTERNATIVE_CHARGED_CANDIDATES.md').read_bytes()).hexdigest(),
        validator_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    (folder/'ALTERNATIVE_CANDIDATES_VALIDATION_2026-10-17.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('report_sha256','document_sha256','validator_sha256')},indent=2))


if __name__=='__main__':main()
