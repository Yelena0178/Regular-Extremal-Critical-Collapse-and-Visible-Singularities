"""Time-reflected Cauchy data: (phi,chi,ell,Q,f)->(phi,-chi,-ell,-Q,f).

Exact constraint symmetry; future dynamics require a new computation/proof.
"""
from canonical_cauchy_data import CanonicalCauchyData


class ReversedCanonicalData(CanonicalCauchyData):
    def free(self, radius):
        phi, gradient, chi, ell, ellp = super().free(radius)
        return phi, gradient, -chi, -ell, -ellp

    def summary(self):
        result=super().summary()
        result.update(profile_change='chi, ell and ell_prime negated; phi and phi_prime fixed',
            constraint_symmetry='Q -> -Q, f -> f, spatial metric unchanged, K -> -K',
            future_classification_inherited=False)
        return result


if __name__ == '__main__':
    import argparse
    import json
    import numpy as np
    from pathlib import Path
    from hashlib import sha256
    from centered_cauchy_diamond import axis_state,evolve_centered
    parser=argparse.ArgumentParser()
    parser.add_argument('input',type=Path)
    parser.add_argument('--parameter',type=float,default=1.001)
    parser.add_argument('--time',type=float,default=8.)
    parser.add_argument('--steps',type=int,default=1024)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    data=ReversedCanonicalData(args.input,args.parameter)
    result=evolve_centered(data.state_at_proper,axis_state(.5,0j),0j,data.proper_max,args.time,args.steps)
    if result['completed']:
        arrays={key:result.pop(key) for key in ('x','state','initial_state')}
        np.savez_compressed(args.output.with_suffix('.npz'),**arrays)
    result.update(initial_data=data.summary(),finite_PDE_error_certified=False,
                  full_future_classified=False,goal_A_proved=False)
    folder=Path(__file__).resolve().parent
    names=['reversed_canonical_data.py','canonical_cauchy_data.py','centered_cauchy_diamond.py',
           'charged_cauchy_diamond.py','charged_lobatto.py','constraint_contraction.py',
           'rotating_af_numeric.py','certify_rotating_af_barrier.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:val for key,val in result.items() if key not in ('axis','history','source_sha256')},indent=2))
