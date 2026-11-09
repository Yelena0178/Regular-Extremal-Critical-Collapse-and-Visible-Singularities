"""Receipt for four finite optical diagnostics, not a completion gate."""
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
import scipy


def main():
    root=Path(__file__).resolve().parent
    names=['INCOMING_OPTICAL_D05_T13p5_N768_2026-10-23.json',
           'INCOMING_OPTICAL_D05_T13p5_N1536_2026-10-23.json',
           'INCOMING_OPTICAL_D08_T20_N1024_2026-10-23.json',
           'INCOMING_OPTICAL_D08_T20_N2048_2026-10-23.json']
    runs=[]
    for name in names:
        data=json.loads((root/name).read_text(encoding='utf-8'))
        matching=all((root/n).is_file() and sha256((root/n).read_bytes()).hexdigest()==h
                     for n,h in data['source_sha256'].items())
        if not matching or not data['completed'] or data['goal_A_proved']:
            raise ArithmeticError('missing/source-stale or misclassified diagnostic: '+name)
        diag=data['diagnostics']; rays=diag['rays']
        runs.append(dict(report=name,report_sha256=sha256((root/name).read_bytes()).hexdigest(),
                         sources_match_current=matching,completed=data['completed'],
                         time=data['requested_time'],steps=data['requested_steps'],
                         min_f_r_ge_quarter=diag['minimum_f_r_ge_quarter'],
                         min_lambda_r_ge_quarter=diag['minimum_lambda_r_ge_quarter'],
                         maximum_log_k_defect=max(r['maximum_log_k_defect'] for r in rays),
                         maximum_mixed_defect=max(r['maximum_mixed_transport_defect'] for r in rays),
                         all_sampled_rays_decrease_in_radius=all(r['radius_strictly_decreasing'] for r in rays),
                         first_half_radius_layers=[dict(v=r['v'],**r['first_half_radius_layer']) for r in rays]))
    pairs=[]
    for i,j in [(0,1),(2,3)]:
        pairs.append(dict(coarse=runs[i]['report'],fine=runs[j]['report'],
                          log_k_defect_ratio=runs[i]['maximum_log_k_defect']/runs[j]['maximum_log_k_defect'],
                          mixed_defect_ratio=runs[i]['maximum_mixed_defect']/runs[j]['maximum_mixed_defect']))
    report=dict(evidence='EXPERIMENTAL',logic='finite diagnostic receipt only',audit='INTERNAL_AUDIT',
                numpy_version=np.__version__,scipy_version=scipy.__version__,runs=runs,refinement=pairs,
                finite_PDE_error_certified=False,continuous_inequality_premises_certified=False,
                positive_mass_extremal_endpoint_proved=False,goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in
                               ['audit_incoming_optical_depth.py','INCOMING_OPTICAL_DEPTH_GATE.md']})
    (root/'INCOMING_OPTICAL_SCREEN_AUDIT_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: four finite reports source-matched; refinement ratios: '+json.dumps(pairs))


if __name__=='__main__':
    main()
