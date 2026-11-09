"""Two prespecified amplitude/frequency contrasts at exactly fixed charge profile.

New reports preserve the earlier split-direction code and evidence bytes.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from charge_preserving_shell import ShellParameters
from split_direction_shell import SplitDirectionShell
from centered_cauchy_diamond import axis_state, evolve_centered
from screen_charge_preserving_shell import Diagnostics
from probe_split_focusing_budget import FocusingBudget

ROOT=Path(__file__).resolve().parent


class FixedChargeAmplitudeShell(SplitDirectionShell):
    def __init__(self,scale,time):
        self.scale=Fraction(scale)
        if not Fraction(3,4)<=self.scale<=Fraction(3,2):
            raise ValueError('scale outside the stated compact initial family')
        self.exact_amplitude=Fraction(2,5)*self.scale
        self.exact_frequency=Fraction(3,20)/(self.scale*self.scale)
        params=ShellParameters(amplitude=float(self.exact_amplitude),
                               frequency=float(self.exact_frequency),direction=.8)
        super().__init__(params,-.8,exterior_width=max(10.,2*time+20.))

    def summary(self):
        result=super().summary()
        result.update(amplitude_scale=str(self.scale),
                      exact_amplitude=str(self.exact_amplitude),
                      exact_frequency=str(self.exact_frequency),
                      exact_charge_product=str(self.exact_amplitude**2*self.exact_frequency),
                      analytic_initial_scope='s in [3/4,3/2], A=2s/5, omega=3/(20s^2), da=4/5, dq=-4/5, R=10,W=4',
                      analytic_initial_claim='AMP01.1; see FIXED_CHARGE_AMPLITUDE_REVIEW_2026-11-01.md',
                      uniform_analytic_f_lower_bound='(3/7)*exp(-4238/125); conditional on inherited charge enclosure')
        return result


class LocatedBudget(FocusingBudget):
    def __init__(self,data,time,rays):
        super().__init__(data,time)
        self.rays={str(u):{'u':u} for u in rays}
        self.traces={str(u):[] for u in rays}
        self.charge_state={}


def check_sources(report):
    for source,digest in report['source_sha256'].items():
        if sha256((ROOT/source).read_bytes()).hexdigest()!=digest:
            raise ValueError('scout source changed: '+source)


def run(scale,time,steps,scout_path=None):
    data=FixedChargeAmplitudeShell(scale,time)
    scout=None
    selection=None
    if scout_path is not None:
        scout=json.loads(scout_path.read_text(encoding='utf-8'))
        check_sources(scout)
        if scout['initial_data']['amplitude_scale']!=str(Fraction(scale)) or scout['requested_time']!=time:
            raise ValueError('scout parameters differ')
        event=scout.get('first_negative_sample') or scout['worst']
        u=event['time']-event['x']
        h=2*time/scout['requested_steps']
        rays=(u-h,u,u+h)
        observer=LocatedBudget(data,time,rays)
        selection={'scout':scout_path.name,'scout_sha256':sha256(scout_path.read_bytes()).hexdigest(),
                   'event_type':'first_negative' if scout.get('first_negative_sample') else 'minimum_sampled_lambda',
                   'event':event,'rays':rays,'primary_u':u}
    else:
        observer=Diagnostics(data,time)
    result=evolve_centered(data.state_at_proper,axis_state(.5,0j),0j,
                          data.proper_max,time,steps,observer=observer)
    for key in ('x','state','initial_state'):
        result.pop(key,None)
    result.update(initial_data=data.summary(),diagnostics=observer.report(),
                  requested_time=time,requested_steps=steps,ray_selection=selection,
                  finite_PDE_error_certified=False,full_future_classified=False,
                  positive_mass_long_residence_proved=False,goal_A_proved=False)
    if scout is not None and steps==scout['requested_steps']:
        same_worst=result.get('worst')==scout.get('worst')
        same_first=result.get('first_negative_sample')==scout.get('first_negative_sample')
        if not same_worst or not same_first:
            raise ArithmeticError('new observer changed recorded evolution samples')
        result['observer_regression']={'passed':True,'scope':'same worst and first-negative samples'}
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scale',choices=('3/4','3/2'),required=True)
    parser.add_argument('--time',type=float,default=15.)
    parser.add_argument('--steps',type=int,choices=(512,1024),default=512)
    parser.add_argument('--scout',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not 0<args.time<=30:
        parser.error('this bounded probe allows 0 < time <= 30')
    result=run(args.scale,args.time,args.steps,args.scout)
    names=['probe_fixed_charge_amplitude.py','probe_split_focusing_budget.py',
           'split_direction_shell.py','charge_preserving_shell.py',
           'screen_charge_preserving_shell.py','centered_cauchy_diamond.py',
           'charged_cauchy_diamond.py','charged_lobatto.py']
    result['source_sha256']={name:sha256((ROOT/name).read_bytes()).hexdigest() for name in names}
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    compact={k:result.get(k) for k in ['completed','failed_time','first_negative_sample','worst','ray_selection','observer_regression']}
    if 'target_ray_traces' in result['diagnostics']:
        compact['rays']=[{'u':r['u'],'first_negative':r['first_negative'],
                          'max_raychaudhuri_defect':r['max_raychaudhuri_defect']} for r in result['diagnostics']['target_ray_traces']]
    print(json.dumps(compact,indent=2))
