"""Finite algebra and E0 shooting checks; no smooth root box or PDE proof."""

from dataclasses import asdict, replace
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from first_jet_shooting import ShootingConfiguration, late_bump, limit_start
from second_jet_shooting import evaluate_second, initial_second, solve_second
from verify_null_infinity_algebra import sym


def require(ok,message):
    if not ok:
        raise ArithmeticError(message)


def algebra():
    # Real form of the complex matrix [-i t m1,-i t m2; (a+i b)n1,(a+i b)n2].
    t,a,b,m1,m2,n1,n2=map(sym,('t','a','b','m1','m2','n1','n2'))
    matrix=[[0,t*m1,0,t*m2],[-t*m1,0,-t*m2,0],
            [a*n1,-b*n1,a*n2,-b*n2],[b*n1,a*n1,b*n2,a*n2]]
    determinant=0
    for order in permutations(range(4)):
        inversions=sum(order[i]>order[j] for i in range(4) for j in range(i+1,4))
        term=(-1)**inversions
        for row,col in enumerate(order):
            term=term*matrix[row][col]
        determinant=determinant+term
    claimed=t*t*(a*a+b*b)*(m1*n2-m2*n1)**2
    require(not (determinant-claimed).terms,'real determinant')
    I,W=sym('I'),sym('W')
    moments=dict(m1=I/3,m2=I/3,n1=I/18,n2=5*I/18)
    require(not ((m1*n2-m2*n1).substitute(moments)-2*I**2/27).terms,'moment determinant')
    require(not ((m1*15*W/4-m2*3*W/4).substitute(moments)-I*W).terms,'zeroth moment')
    require(not (n1*15*W/4-n2*3*W/4).substitute(moments).terms,'first moment')
    require(bool((n1*W).substitute(moments).terms),'single pulse false cancellation')
    return dict(arithmetic='exact rational Laurent polynomials',identities=4,
                rejected_single_pulse_cancellation=True)


def fd_jacobian(point,cfg,step):
    result=[]
    for i in range(5):
        shift=np.zeros(5);shift[i]=step
        result.append((evaluate_second(point+shift,cfg)-evaluate_second(point-shift,cfg))/(2*step))
    return np.column_stack(result)


def main():
    exact=algebra()
    cfg=ShootingConfiguration(beta=.0003,rtol=2e-11,atol=2e-15,max_step=.02)
    initial=initial_second(cfg)
    I=quad(lambda y:late_bump(y)[0],0,1,epsabs=1e-13,epsrel=1e-13)[0]
    c=1j*cfg.coupling/(4*cfg.radius)
    A=-3*c*c+c/(2*cfg.radius**2)
    old=limit_start(cfg)
    p0=c*I*complex(old[1],old[2])
    probe=np.array([initial[0],.2,-.3,-.4,.1])
    W1,W2=complex(*probe[1:3]),complex(*probe[3:5])
    expected_p=p0-c*I*(W1+W2)/3
    expected_k=-3*c*expected_p+A*I*(W1+5*W2)/18
    prediction=np.array([0,expected_p.real,expected_p.imag,expected_k.real,expected_k.imag])
    limits=[]
    for beta in [.0003,.0001,.00003]:
        observed=evaluate_second(probe,replace(cfg,beta=beta))
        limits.append(dict(beta=beta,max_error=float(np.max(abs(observed-prediction)))))
    require(limits[-1]['max_error']<limits[0]['max_error']/5,'nonzero limit-direction convergence')
    runs=[]
    for beta in [.003,.001,.0003,.0001]:
        point,report=solve_second(replace(cfg,beta=beta))
        require(report['solver_success'],'root solver')
        require(max(abs(x) for x in report['scaled_residual'])<1e-8,'scaled root residual')
        report['passes_sampled_H_screen']=bool(report['min_sampled_H']>0)
        runs.append(report)
    require(not runs[0]['passes_sampled_H_screen'],'retain finite-beta H failure')
    require(all(r['passes_sampled_H_screen'] for r in runs[1:]),'small-beta sampled sign')
    refined=[]
    point=initial
    for rtol,atol,step in [(2e-10,2e-14,.04),(2e-11,2e-15,.02),(2e-12,2e-16,.01)]:
        local=replace(cfg,rtol=rtol,atol=atol,max_step=step)
        point,report=solve_second(local,point)
        require(report['solver_success'] and max(abs(x) for x in report['scaled_residual'])<1e-8,'refined root')
        report['configuration']=asdict(local)
        refined.append(report)
    drift=[float(np.max(abs(np.array(b['parameters'])-np.array(a['parameters']))))
           for a,b in zip(refined,refined[1:])]
    require(max(drift)<2e-6,'tolerance root drift')
    local=replace(cfg,beta=.00003,rtol=2e-12,atol=2e-16,max_step=.01)
    matrices=[fd_jacobian(initial,local,h) for h in [1e-4,5e-5]]
    determinants=[float(np.linalg.det(m)) for m in matrices]
    d=-1/(2*initial[0]*(1-initial[0]))
    analytic=d*abs(c)**2*abs(A)**2*(2*I*I/27)**2
    require(max(abs(x/analytic-1) for x in determinants)<.02,'limit determinant agreement')
    folder=Path(__file__).resolve().parent
    result=dict(evidence='finite_exact_algebra_plus_E0_C0_shooting',exact=exact,
                pulse_integral_numeric=I,auxiliary_initial_parameters=initial.tolist(),
                nonzero_probe_prediction=prediction.tolist(),auxiliary_limit_checks=limits,
                runs=runs,tolerance_runs=refined,successive_root_drift=drift,
                finite_difference_determinants=determinants,analytic_limit_determinant=analytic,
                smooth_layer_resolved=False,rigorous_root_box=False,full_goal_A_proved=False)
    files=['TWO_PULSE_SECOND_JET.md','second_jet_shooting.py','verify_two_pulse_second_jet.py',
           'first_jet_shooting.py','verify_null_infinity_algebra.py','SECOND_TRANSVERSE_JET.md']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in files}
    (folder/'TWO_PULSE_SECOND_JET_CHECKS_2026-10-16.json').write_text(
        json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='PASS',determinants=determinants,analytic=analytic,
                         root_drift=drift,H_screens=[r['min_sampled_H'] for r in runs],
                         limit_checks=limits),indent=2))


if __name__=='__main__':
    main()
