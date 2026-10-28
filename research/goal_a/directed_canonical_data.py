"""Exact free-profile direction change, with numerical constraint reconstruction.

chi_d=(1-d)chi-d*phi_r, so the initial incoming derivative is multiplied
by 1-d before the geometry is re-solved. No future inference from this identity.
"""
from fractions import Fraction
import numpy as np
from canonical_cauchy_data import CanonicalCauchyData


class DirectedCanonicalData(CanonicalCauchyData):
    def __init__(self, path, parameter=1.001, direction=Fraction(1), **kwargs):
        self.direction = Fraction(direction)
        if not 0 <= self.direction <= 1:
            raise ValueError('direction must lie in [0,1]')
        super().__init__(path, parameter, **kwargs)

    def free(self, radius):
        phi, gradient, chi, ell, ellp = super().free(radius)
        d = float(self.direction)
        return phi, gradient, (1-d)*chi-d*gradient, ell, ellp

    def summary(self):
        result = super().summary()
        result.update(direction=dict(numerator=self.direction.numerator,denominator=self.direction.denominator),
            profile_change='chi_d=(1-d)*chi-d*phi_r, fixed phi and ell; then common scaling s',
            original_certified_parameter_interval=None,
            initial_positivity_certificate='requires separate directed-profile certificate')
        return result

    def initial_diagnostics(self):
        records=[]
        for left,right,sol in self.solutions[:-1]:
            for r in np.linspace(left,right,5):
                Q,f,*_ = sol(r)
                phi,g,chi,ell,_ = self.free(r)
                D=f+(r*ell)**2
                V=np.sqrt(D)*(chi+g)/2
                P=np.sqrt(D)*(chi-g)/2
                records.append((r,f,abs(V),abs(P),Q))
        rows=np.asarray(records)
        j=int(np.argmin(rows[:,1]))
        return dict(minimum_sampled_f=float(rows[j,1]),radius_at_minimum=float(rows[j,0]),
                    maximum_incoming_Dv_phi=float(max(rows[:,2])),
                    maximum_outgoing_Du_phi=float(max(rows[:,3])),
                    samples=len(rows),all_radius_positivity_certified=False)


if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    from hashlib import sha256
    from centered_cauchy_diamond import axis_state, evolve_centered
    parser=argparse.ArgumentParser()
    parser.add_argument('input',type=Path)
    parser.add_argument('--parameter',type=float,default=1.001)
    parser.add_argument('--direction',type=Fraction,required=True)
    parser.add_argument('--time',type=float,default=0.)
    parser.add_argument('--steps',type=int,default=1024)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    data=DirectedCanonicalData(args.input,args.parameter,args.direction)
    result=dict(initial_data=data.summary(),initial_diagnostics=data.initial_diagnostics(),
                finite_PDE_error_certified=False,full_future_classified=False,goal_A_proved=False)
    if args.time>0:
        outcome=evolve_centered(data.state_at_proper,axis_state(.5,0j),0j,data.proper_max,args.time,args.steps)
        if outcome['completed']:
            arrays={key:outcome.pop(key) for key in ('x','state','initial_state')}
            np.savez_compressed(args.output.with_suffix('.npz'),**arrays)
        result['evolution']=outcome
    folder=Path(__file__).resolve().parent
    names=['directed_canonical_data.py','canonical_cauchy_data.py','centered_cauchy_diamond.py',
           'charged_cauchy_diamond.py','charged_lobatto.py','constraint_contraction.py',
           'rotating_af_numeric.py','certify_rotating_af_barrier.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    brief={key:val for key,val in result.items() if key not in ('source_sha256','evolution')}
    if 'evolution' in result:
        brief['evolution']={key:val for key,val in result['evolution'].items() if key not in ('axis','history')}
    print(json.dumps(brief,indent=2))
