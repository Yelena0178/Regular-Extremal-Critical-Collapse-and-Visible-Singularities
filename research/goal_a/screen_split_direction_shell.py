"""Bounded center-inclusive probe of independent envelope and phase directions."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from charge_preserving_shell import ShellParameters
from split_direction_shell import SplitDirectionShell
from centered_cauchy_diamond import axis_state, evolve_centered
from screen_charge_preserving_shell import Diagnostics


def run(da,dq,time,steps):
    parameters=ShellParameters(amplitude=.4,frequency=.15,direction=da)
    data=SplitDirectionShell(parameters,dq,exterior_width=max(10.,2*time+2*parameters.radius))
    observer=Diagnostics(data,time)
    result=evolve_centered(data.state_at_proper,axis_state(.5,0j),0j,
                          data.proper_max,time,steps,observer=observer)
    for key in ('x','state','initial_state'):
        result.pop(key,None)
    result.update(initial_data=data.summary(),diagnostics=observer.report(),requested_time=time,
                  requested_steps=steps,finite_PDE_error_certified=False,
                  full_future_classified=False,positive_mass_long_residence_proved=False,goal_A_proved=False)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--envelope-direction',type=float,default=.8)
    parser.add_argument('--phase-direction',type=float,required=True)
    parser.add_argument('--time',type=float,default=15.)
    parser.add_argument('--steps',type=int,default=256)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not np.isfinite(args.time) or args.time<=0 or args.steps<16:
        parser.error('positive time and at least 16 steps required')
    try:
        result=run(args.envelope_direction,args.phase_direction,args.time,args.steps)
    except (ArithmeticError,ValueError) as error:
        result={'completed':False,'failure':str(error),'requested_time':args.time,'requested_steps':args.steps,
                'envelope_direction':args.envelope_direction,'phase_direction':args.phase_direction,
                'finite_PDE_error_certified':False,'full_future_classified':False,'goal_A_proved':False}
    folder=Path(__file__).resolve().parent
    names=['screen_split_direction_shell.py','split_direction_shell.py','charge_preserving_shell.py',
           'screen_charge_preserving_shell.py','centered_cauchy_diamond.py','charged_cauchy_diamond.py','charged_lobatto.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:result.get(k) for k in ['completed','failure','failed_time','first_negative_sample','worst']},indent=2))
