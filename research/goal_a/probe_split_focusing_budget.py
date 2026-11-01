"""Resolve focusing costs on rays crossing the previous first negative samples.

The observer is read-only. Quadrature and interpolation remain uncertified.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from charge_preserving_shell import ShellParameters
from split_direction_shell import SplitDirectionShell
from centered_cauchy_diamond import axis_state, evolve_centered
from screen_charge_preserving_shell import Diagnostics

ROOT=Path(__file__).resolve().parent
RAYS=(2775/256,2790/256)


class FocusingBudget(Diagnostics):
    def __init__(self,data,time):
        super().__init__(data,time)
        self.rays={str(u):{'u':u} for u in RAYS}
        self.traces={str(u):[] for u in RAYS}
        self.charge_state={}

    def __call__(self,t,x,state):
        super().__call__(t,x,state)
        for key,ray in self.rays.items():
            if ray.get('final_time')!=t:
                continue
            y=self.interpolate(x,state,t-ray['u'])
            r,phi,V=y[0],y[8]+1j*y[9],(y[2]+1j*y[3])/y[0]
            current=.6*r*r*np.imag(phi*np.conjugate(V))
            if key not in self.charge_state:
                self.charge_state[key]={'last_t':t,'last_current':current,'integral':0.}
            else:
                old=self.charge_state[key]
                old['integral']+=(t-old['last_t'])*(old['last_current']+current)  # dv=2dt
                old.update(last_t=t,last_current=current)
            F,Fa,H=map(float,ray['integrals'])
            self.traces[key].append({
                'time':t,'radius':float(r),'Q':float(y[10]),
                'expansion':ray['final_expansion'],'entry_expansion':ray['initial_expansion'],
                'focusing':F,'amplitude_cost':Fa,'phase_cost':F-Fa,
                'minimum_charge_cost':ray['minimum_charge_cost'],
                'phase_excess':ray['phase_excess'],'capacity':H,
                'necessary_slack':ray['initial_expansion']-Fa-ray['minimum_charge_cost'],
                'raychaudhuri_defect':ray['final_expansion']-ray['initial_expansion']+F,
                'charge_integral_defect':float(y[10]-ray['initial_Q']-self.charge_state[key]['integral']),
                'amplitude_squared':float(abs(phi)**2),
            })

    def report(self):
        result=super().report()
        records=[]
        for key,rows in self.traces.items():
            first=next((row for row in rows if row['expansion']<0),None)
            records.append({'u':float(key),'samples':rows,'first_negative':first,
                            'max_charge_integral_defect':max((abs(r['charge_integral_defect']) for r in rows),default=0.),
                            'max_raychaudhuri_defect':max((abs(r['raychaudhuri_defect']) for r in rows),default=0.)})
        result['target_ray_traces']=records
        result['limitations'].append('entry is first sampled positive-radius point, not an exact axis limit')
        return result


def run(steps):
    data=SplitDirectionShell(ShellParameters(amplitude=.4,frequency=.15,direction=.8),-.8,
                            exterior_width=50.)
    observer=FocusingBudget(data,15.)
    result=evolve_centered(data.state_at_proper,axis_state(.5,0j),0j,
                          data.proper_max,15.,steps,observer=observer)
    for key in ('x','state','initial_state'):
        result.pop(key,None)
    result.update(initial_data=data.summary(),diagnostics=observer.report(),requested_time=15.,
                  requested_steps=steps,finite_PDE_error_certified=False,
                  full_future_classified=False,goal_A_proved=False)
    if steps==512 and result['completed']:
        original=ROOT/'SPLIT_DA08_DQM08_T15_N512_2026-11-01.json'
        old=json.loads(original.read_text(encoding='utf-8'))
        if any(abs(result['worst'][k]-v)>1e-12 for k,v in old['worst'].items()):
            raise ArithmeticError('new observer changed the previous evolution')
        if result['first_negative_sample']!=old['first_negative_sample']:
            raise ArithmeticError('new observer changed the first negative sample')
        result['observer_regression']={'passed':True,'baseline':original.name,
                                       'baseline_sha256':sha256(original.read_bytes()).hexdigest(),
                                       'scope':'same 512-step worst and first-negative samples'}
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--steps',type=int,choices=(512,1024),required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=run(args.steps)
    names=['probe_split_focusing_budget.py','split_direction_shell.py','charge_preserving_shell.py',
           'screen_charge_preserving_shell.py','centered_cauchy_diamond.py','charged_cauchy_diamond.py','charged_lobatto.py']
    result['source_sha256']={name:sha256((ROOT/name).read_bytes()).hexdigest() for name in names}
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    compact=[]
    for ray in result['diagnostics']['target_ray_traces']:
        first=ray['first_negative']
        compact.append({'u':ray['u'],'first_negative':first,
                        'max_charge_integral_defect':ray['max_charge_integral_defect'],
                        'max_raychaudhuri_defect':ray['max_raychaudhuri_defect']})
    print(json.dumps({'completed':result['completed'],'steps':args.steps,
                      'observer_regression':result.get('observer_regression'),'rays':compact},indent=2))
