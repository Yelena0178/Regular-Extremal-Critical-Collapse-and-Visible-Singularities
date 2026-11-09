"""Aggregate finite centered-screen evidence without classifying a spacetime."""
import json
from pathlib import Path
from hashlib import sha256
import numpy as np
from charged_cauchy_diamond import spatial_constraints


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def main():
    folder = Path(__file__).resolve().parent
    names = ['summarize_centered_cauchy_screen.py']

    def read(name):
        names.append(name)
        data = json.loads((folder/name).read_text(encoding='utf-8'))
        for source, digest in data.get('source_sha256', {}).items():
            require(sha256((folder/source).read_bytes()).hexdigest() == digest, 'changed source '+source)
        if 'initial_data' in data:
            initial = data['initial_data']
            require(sha256((folder/initial['canonical_input']).read_bytes()).hexdigest()
                    == initial['canonical_sha256'], 'changed canonical input')
            require(initial['parameter'] == 1.001, 'wrong parameter')
        return data

    rows, arrays = [], []
    common_x = 1.078125  # member of all three final grids; chosen from coarsest minimum
    for n in (800, 1600, 3200):
        name = f'CANONICAL_CENTERED_A020_W8_S1001_T625_N{n}_2026-10-22.json'
        data = read(name)
        require(data['completed'] and data['final_time'] == 6.25, 'incomplete centered screen')
        require(data['final_x_left'] == 0. and not data['finite_PDE_error_certified'], 'wrong scope')
        binary = Path(name).with_suffix('.npz').name
        names.append(binary)
        with np.load(folder/binary) as saved:
            x, y = saved['x'].copy(), saved['state'].copy()
        require(np.isfinite(y).all() and np.all(np.diff(x)>0), 'invalid final grid')
        require(x[0] == 0 and np.all(y[1:,0]>0) and np.all(y[:,1]>0)
                and np.all(y[:,4]<0), 'invalid final chart')
        j = int(np.argmin(abs(x-common_x)))
        require(abs(x[j]-common_x)<1e-12, 'common point absent')
        lam = y[j,1]*(1-2*y[j,7]/y[j,0])
        mask = (x >= .9) & (x <= 1.3)
        neighborhood = spatial_constraints(x[mask], y[mask])
        rows.append(dict(steps=n, worst=data['worst'], first_negative=data['first_negative_sample'],
                         common_point=dict(time=6.25,x=common_x,u=6.25-common_x,
                             radius=float(y[j,0]),lambda_value=float(lam),nu=float(y[j,4]),Q=float(y[j,10])),
                         entire_final_row_constraints=data['final_row_constraints'],
                         negative_signal_neighborhood_constraints=neighborhood,
                         axis_kappa_defect=data['maximum_axis_kappa_defect'],
                         final_axis=data['axis'][-1]))
        arrays.append((x,y))
    comparisons=[]
    for coarse, fine in zip(arrays, arrays[1:]):
        xc,yc=coarse
        xf,yf=fine
        require(len(xf)==2*len(xc)-1 and np.max(abs(xf[::2]-xc))<1e-12,'grids not nested')
        select=(xc>=.9)&(xc<=1.3)
        indices=np.flatnonzero(select)
        lc=yc[indices,1]*(1-2*yc[indices,7]/yc[indices,0])
        lf=yf[2*indices,1]*(1-2*yf[2*indices,7]/yf[2*indices,0])
        comparisons.append(dict(maximum_state_difference=float(np.max(abs(yc-yf[::2]))),
            negative_neighborhood_lambda_difference=float(np.max(abs(lc-lf)))))
    exterior=[]
    for time,n in ((8,2048),(16,2048),(16,4096)):
        data=read(f'CANONICAL_CAUCHY_A020_W8_S1001_CORE_T{time}_N{n}_2026-10-22.json')
        require(data['completed'],'exterior run stopped')
        exterior.append(dict(time=time,steps=n,worst=data['worst'],
            maximum_outgoing_coordinate=data['maximum_outgoing_coordinate']))
    failures=[]
    for n in (1024,2048):
        data=read(f'CANONICAL_CENTERED_A020_W8_S1001_T8_N{n}_2026-10-22.json')
        require(not data['completed'],'expected archived numerical stop')
        failures.append(dict(steps=n,failed_time=data['failed_time'],reason=data['failure'],
                             first_negative=data['first_negative_sample']))
    require(all(row['common_point']['u']>exterior[0]['maximum_outgoing_coordinate'] for row in rows),
            'center signal was not outside the earlier wedge')
    report=dict(status='PASS', evidence='E0 finite-record consistency only', centered_runs=rows,
        successive_grid_comparisons=comparisons, exterior_wedges=exterior, stopped_runs=failures,
        candidate_status='strong negative central samples; early-screen pass not established',
        finite_PDE_error_certified=False, actual_trapped_sphere_certified=False,
        singularity_proved=False, global_endpoint_classified=False, goal_A_proved=False,
        source_sha256={name:sha256((folder/name).read_bytes()).hexdigest() for name in names})
    (folder/'CENTERED_CAUCHY_SCREEN_SUMMARY_2026-10-22.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='PASS',common_points=[r['common_point'] for r in rows],
        comparisons=comparisons,nearby_constraints=[r['negative_signal_neighborhood_constraints'] for r in rows],
        actual_trapped_sphere_certified=False),indent=2))


if __name__ == '__main__':
    main()
