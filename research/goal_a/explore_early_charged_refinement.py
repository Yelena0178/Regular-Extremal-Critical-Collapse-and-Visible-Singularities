"""Refinement and saved proposals for the two surviving smooth charged pulses."""

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import time
import numpy as np

from early_charged_pulse_candidate import Pulse,characteristic_data
from charged_lobatto import evolve


def main(resolutions=(48,96)):
    folder=Path(__file__).resolve().parent;records=[];caches=[]
    for cfg in (Pulse(.2,8.),Pulse(.3,4.)):
        label=f'A{round(100*cfg.amplitude)}_W{round(cfg.frequency)}'
        for n in resolutions:
            start=time.monotonic();out,inc,cap,S,R,parameters=characteristic_data(cfg)
            record=dict(configuration=asdict(cfg),n=n,parameters=parameters)
            try:
                with np.errstate(over='raise',invalid='raise',divide='raise',under='ignore'):
                    data=evolve(out,inc,.95*cap,cap+S*np.linspace(0.,1.,n+1),n)
                x=data['state'];r,k,m,nu=x[...,0],x[...,1],x[...,7],x[...,4]
                lam=k*(1-2*m/r);index=np.unravel_index(np.argmin(lam),lam.shape)
                interior=lam[1:];where=np.unravel_index(np.argmin(interior),interior.shape)
                # Exact constraints give lambda=0 at the outgoing endpoint;
                # the numerical sign there measures drift, not trapping.
                record.update(endpoint_lambda=float(lam[-1,-1]),
                    minimum_sampled_lambda=float(lam[index]),minimum_index=[int(i) for i in index],
                    minimum_sampled_lambda_u_positive=float(interior[where]),
                    minimum_u_positive_index=[int(where[0]+1),int(where[1])],
                    outgoing_endpoint_lambda_drift=float(lam[0,-1]),
                    minimum_sampled_radius=float(r.min()),maximum_sampled_nu=float(nu.max()),
                    endpoint_state=x[-1,-1].tolist(),outgoing_terminal_state=x[0,-1].tolist(),
                    first_transverse_scalar_at_terminal=[float(nu[0,-1]*x[0,-1,j]/r[0,-1]) for j in (5,6)],
                    iterations=data['iteration_report'])
                name=f'EARLY_CHARGED_{label}_N{n}_2026-10-17.npz'
                np.savez_compressed(folder/name,**{k:data[k] for k in ('u','v','state','last_v_stages')})
                record.update(cache=name,cache_sha256=sha256((folder/name).read_bytes()).hexdigest())
                caches.append(name)
            except (ArithmeticError,ValueError,FloatingPointError) as error:record['failure']=str(error)
            record.update(elapsed_seconds=time.monotonic()-start,evidence='E0 only',
                actual_smooth_seed_certified=False,goal_A_proved=False)
            records.append(record)
            print(json.dumps({k:record[k] for k in ('configuration','n','endpoint_lambda',
                'minimum_sampled_lambda_u_positive','outgoing_endpoint_lambda_drift',
                'first_transverse_scalar_at_terminal','failure') if k in record}),flush=True)
    names=['explore_early_charged_refinement.py','early_charged_pulse_candidate.py','charged_lobatto.py']
    result=dict(runs=records,scope='refinement of independent smooth charged-onset seeds',
        complete_PDE_error_certified=False,global_no_trapping_proved=False,
        full_AF_Cauchy_realization=False,critical_curve_constructed=False,goal_A_proved=False,
        source_sha256={name:sha256((folder/name).read_bytes()).hexdigest() for name in names})
    suffix='_'.join(map(str,resolutions))
    (folder/f'EARLY_CHARGED_REFINEMENT_{suffix}_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,nargs='+',default=[48,96])
    main(tuple(parser.parse_args().n))
