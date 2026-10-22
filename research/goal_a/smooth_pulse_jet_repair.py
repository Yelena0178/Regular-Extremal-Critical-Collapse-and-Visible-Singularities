"""E0 two-jet repair of the new C-infinity charged-onset pulses.

The complete radial constraint problem is solved again for every control.
No root box, no no-trapping certificate and no global classification.
"""

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp,quad
from scipy.optimize import root

from early_charged_pulse_candidate import Pulse,scalar
from new_shape_jets import jet_rhs


def bump(t):
    if t<=0 or t>=1:return 0.,0.
    d=4*t*(1-t);b=np.exp(1-1/d)
    return b,4*(1-2*t)*b/(d*d)


def pulses(y):
    g1,p1=bump(3*y);g2,p2=bump(3*y-2)
    return np.array([g1,g2]),3*np.array([p1,p2])


def integrate(fun,interval,initial,tolerance=2e-12):
    sol=solve_ivp(fun,interval,initial,method='DOP853',rtol=tolerance,
        atol=tolerance*1e-4,max_step=abs(interval[1]-interval[0])/96,dense_output=True)
    if not sol.success or not np.isfinite(sol.y).all():raise ArithmeticError(sol.message)
    return sol


class RepairedCone:
    def __init__(self,cfg,epsilon,parameters,tolerance=2e-12):
        if not 0<epsilon<.5 or cfg.coupling!=.6:raise ValueError('fixed-e repair domain')
        self.cfg,self.epsilon=cfg,epsilon
        self.L=(1-epsilon)/epsilon
        self.Z=np.array([complex(*parameters[:2]),complex(*parameters[2:])])
        def radial(y,state):
            g,gp=pulses(y)
            return [state[1],-epsilon*epsilon*abs(self.Z@gp)**2*state[0]]
        self.late_radial=integrate(radial,(1.,0.),[1.,0.],tolerance)
        fb,pb=self.late_radial.y[:,-1]
        def early_radial(t,state):
            field,V=scalar(t,cfg)
            current=cfg.frequency*abs(field)**2
            return [state[1],-abs(V)**2*state[0],state[0]**2*current]
        self.early_radial=integrate(early_radial,(1.,0.),[fb,pb/self.L,0.],tolerance)
        f0,p0,negative_charge=self.early_radial.y[:,-1]
        sample=np.linspace(0.,1.,385)
        self.min_f=min(float(self.early_radial.sol(sample)[0].min()),
                       float(self.late_radial.sol(sample)[0].min()))
        if min(f0,p0,-negative_charge,self.min_f)<=0:raise ArithmeticError('repair lost sampled positive radius or cap')
        self.C=-negative_charge;self.R=1/(cfg.coupling*self.C)
        self.S=2*self.R*p0;self.cap=2*self.R*f0
        def early_jets(t,state):
            f,fp,remaining=self.early_radial.sol(t)
            field,V=scalar(t,cfg);q=1+remaining/self.C
            return jet_rhs(self.R*f,self.R*fp,self.R*q,field,V,state,cfg.coupling)
        self.early_jets=integrate(early_jets,(0.,1.),np.array([f0/p0,0.,0.,0.],dtype=complex),tolerance)
        H,T,P,K=self.early_jets.y[:,-1]
        def late_jets(y,state):
            H,tau,P,k=state;f,fy=self.late_radial.sol(y);g,gp=pulses(y)
            unscaled=np.array([H,tau/epsilon,P,k/epsilon])
            field=epsilon*(self.Z@g);V=epsilon*(self.Z@gp)/self.L
            value=jet_rhs(self.R*f,self.R*fy/self.L,self.R,field,V,unscaled,cfg.coupling)
            return value*np.array([self.L,epsilon*self.L,self.L,epsilon*self.L])
        self.late_jets=integrate(late_jets,(0.,1.),np.array([H,epsilon*T,P,epsilon*K]),tolerance)

    def residual(self):
        H,tau,P,k=self.late_jets.y[:,-1]
        return np.array([self.R*P.real,self.R*P.imag,self.R**2*k.real,self.R**2*k.imag])

    def report(self):
        H,tau,P,k=self.late_jets.y[:,-1];sample=np.linspace(0.,1.,1025)
        min_H=min(float(self.early_jets.sol(sample)[0].real.min()),
                  float(self.late_jets.sol(sample)[0].real.min()))
        physical_P=self.S*P;physical_K=self.S*self.S*k/self.epsilon
        return dict(configuration=asdict(self.cfg),epsilon=self.epsilon,late_length=self.L,
            parameters=[z for w in self.Z for z in (float(w.real),float(w.imag))],
            actual_pulse_amplitudes=[float(abs(w)*self.epsilon) for w in self.Z],
            radius=self.R,scale=self.S,cap=self.cap,minimum_sampled_f=self.min_f,
            minimum_sampled_H=min_H,scaled_residual=self.residual().tolist(),
            physical_first_jet=[float(physical_P.real),float(physical_P.imag)],
            physical_second_jet=[float(physical_K.real),float(physical_K.imag)],
            evidence='E0 smooth constraint and two-jet shooting',
            exact_root_certified=False,no_trapping_certified=False,goal_A_proved=False)

    def outgoing(self,V,piece=0):
        t=(V-self.cap)/self.S
        if piece==0:
            at=np.clip(t,0.,1.);f,fp,_=self.early_radial.sol(at)
            field,pt=scalar(at,self.cfg);H=self.early_jets.sol(at)[0].real
        else:
            y=np.clip((t-1)/self.L,0.,1.);f,fy=self.late_radial.sol(y)
            g,gp=pulses(y);pt=self.epsilon*(self.Z@gp)/self.L
            H=self.late_jets.sol(y)[0].real
        r=self.R*f;k=r/(self.S*H);theta=r*pt/self.S
        return np.array([r,k,theta.real,theta.imag])

    def incoming(self,u):
        return np.array([(self.cap-u)/2,.5,0.,0.,-.5,0.,0.,0.,0.,0.,0.,0.])


def limit_start(cfg):
    baseline=RepairedCone(cfg,.1,np.zeros(4))
    P=baseline.early_jets.y[2,-1];c=1j*cfg.coupling/(4*baseline.R)
    integral=quad(lambda t:bump(t)[0],0,1,epsabs=1e-13,epsrel=1e-13)[0]
    z0=P/(c*integral);z1,z2=15*z0/4,-3*z0/4
    return np.array([z1.real,z1.imag,z2.real,z2.imag])


def solve(cfg,epsilon,initial=None,tolerance=2e-12):
    initial=limit_start(cfg) if initial is None else initial
    fun=lambda values:RepairedCone(cfg,epsilon,values,tolerance).residual()
    sol=root(fun,initial,method='hybr',options={'xtol':1e-9,'maxfev':80})
    model=RepairedCone(cfg,epsilon,sol.x,tolerance)
    return model,dict(solver_success=bool(sol.success),solver_message=str(sol.message),evaluations=int(sol.nfev))


def main(epsilons=(.25,.1,.03)):
    records=[];start=time.monotonic()
    for cfg in (Pulse(.2,8.),Pulse(.3,4.)):
        for epsilon in epsilons:
            try:
                cone,solver=solve(cfg,epsilon);record=cone.report()|solver
            except (ArithmeticError,ValueError,FloatingPointError) as error:
                record=dict(configuration=asdict(cfg),epsilon=epsilon,failure=str(error),goal_A_proved=False)
            records.append(record)
            print(json.dumps(record),flush=True)
    folder=Path(__file__).resolve().parent
    names=['smooth_pulse_jet_repair.py','early_charged_pulse_candidate.py','new_shape_jets.py']
    result=dict(runs=records,elapsed_seconds=time.monotonic()-start,
        scope='finite smooth two-jet roots; no rigorous root boxes or future proof',
        full_AF_Cauchy_realization=False,critical_curve_constructed=False,goal_A_proved=False,
        source_sha256={name:sha256((folder/name).read_bytes()).hexdigest() for name in names})
    (folder/'SMOOTH_PULSE_JET_REPAIR_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--eps',type=float,nargs='+',default=[.25,.1,.03])
    main(tuple(parser.parse_args().eps))
