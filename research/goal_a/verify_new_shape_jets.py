"""Independent tolerance and nonzero-direction checks of the new E0 roots."""

from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad

from new_shape_jets import Configuration,evaluate,limit_start
from first_jet_shooting import late_bump


def require(ok,message):
    if not ok:raise ArithmeticError(message)


def main():
    folder=Path(__file__).resolve().parent
    source='NEW_SHAPE_JETS_2026-10-17.json'
    roots=json.loads((folder/source).read_text())
    refined=[]
    for old in roots['runs']:
        require(old['solver_success'],'failed original root solver')
        cfg=Configuration(**old['configuration'])
        tight=replace(cfg,rtol=2e-12,atol=2e-18,max_step=.01)
        new=evaluate(old['parameters'],tight,True)
        error=max(abs(x) for x in new['scaled_residual'])
        require(error<2e-8,'tolerance check residual')
        require((new['min_sampled_H']>0)==old['passes_sampled_H_screen'],'incoming expansion sign changed')
        refined.append(dict(beta=cfg.beta,refined_max_scaled_residual=error,
                            refined_min_sampled_H=new['min_sampled_H']))
    require([x['passes_sampled_H_screen'] for x in roots['runs']]==[False,False,True,True],
            'retain the two finite-beta failures')
    cfg=Configuration(beta=.0003)
    initial=limit_start(cfg)
    I=quad(lambda y:late_bump(y)[0],0,1,epsabs=1e-13,epsrel=1e-13)[0]
    c=1j*cfg.coupling/(4*cfg.radius);A=-3*c*c+c/(2*cfg.radius**2)
    initial_W1,initial_W2=complex(*initial[1:3]),complex(*initial[3:5])
    p0=c*I*(initial_W1+initial_W2)/3
    probe=np.array([initial[0],.2,-.3,-.4,.1])
    W1,W2=complex(*probe[1:3]),complex(*probe[3:5])
    p=p0-c*I*(W1+W2)/3
    k=-3*c*p+A*I*(W1+5*W2)/18
    prediction=np.array([0,p.real,p.imag,k.real,k.imag])
    directions=[]
    for beta in (.0003,.0001,.00003):
        actual=evaluate(probe,replace(cfg,beta=beta))
        directions.append(dict(beta=beta,maximum_error=float(np.max(abs(actual-prediction)))))
    require(directions[-1]['maximum_error']<directions[0]['maximum_error']/5,
            'new shape nonzero limit-direction convergence')
    result=dict(status='PASS',refined_roots=refined,nonzero_directions=directions,
                smooth_root_box_certified=False,actual_smooth_member_certified=False,
                full_AF_Cauchy_realization=False,goal_A_proved=False)
    names=['verify_new_shape_jets.py','new_shape_jets.py','first_jet_shooting.py',source]
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'NEW_SHAPE_JET_CHECKS_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
