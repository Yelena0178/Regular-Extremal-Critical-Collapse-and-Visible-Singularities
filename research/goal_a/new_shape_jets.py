"""Finite-beta two-jet shooting for the fixed R=10 candidate (E0 only).

No historical R=5 module is modified. The early cone remains C0 at joints;
positive smoothing and root-box certification are separate obligations.
"""

from dataclasses import dataclass, asdict
from hashlib import sha256
import cmath
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import root

from first_jet_shooting import harmonic_transfer, late_bump
from second_jet_shooting import pulses


@dataclass(frozen=True)
class Configuration:
    beta: float = .001
    radius: float = 10.
    coupling: float = .6
    amplitude: float = .7
    radius_ratio: float = .125
    rtol: float = 2e-11
    atol: float = 2e-17
    max_step: float = .02

    def validate(self):
        if (self.radius,self.coupling,self.amplitude,self.radius_ratio) != (10.,.6,.7,.125):
            raise ValueError('fixed new shape required')
        if not 0 < self.beta < .01:
            raise ValueError('finite positive beta below 0.01 required')


def integrate(fun, interval, initial, cfg):
    sol = solve_ivp(fun,interval,np.asarray(initial,dtype=complex),method='DOP853',
                    rtol=cfg.rtol,atol=cfg.atol,max_step=cfg.max_step,dense_output=True)
    if not sol.success or not np.isfinite(sol.y).all():
        raise ArithmeticError(sol.message)
    return sol


def prepare(s, fb, pb, cfg):
    if not .57 < s < .63:
        raise ValueError('s outside prospective new-shape box')
    Phi = cfg.amplitude
    c = math.sqrt(s*(1-s)); rate = c/Phi
    v2 = s/(s+Phi*math.tan(Phi))
    v1 = v2*cfg.radius_ratio**(1/s)
    f2,p2 = harmonic_transfer(fb,pb,Phi/(1-v2),v2-1)
    matrix = [[v2**s,v2**(1-s)],[s*v2**(s-1),(1-s)*v2**(-s)]]
    C,D = np.linalg.solve(matrix,[f2,p2])
    f1 = C*v1**s+D*v1**(1-s)
    p1 = s*C*v1**(s-1)+(1-s)*D*v1**(-s)
    f0,p0 = harmonic_transfer(f1,p1,Phi/v1,-v1)
    if min(f0,f1,f2,fb) <= 0 or p0 <= 0:
        raise ArithmeticError('nonpositive early cone geometry')
    def charge(x):
        x = min(max(x,v1),v2)
        integral = (C*C*(x**(2*s)-v1**(2*s))/(2*s)+2*C*D*(x-v1)
                    +D*D*(x**(2-2*s)-v1**(2-2*s))/(2-2*s))
        return cfg.coupling*cfg.radius*Phi*c*integral
    return dict(s=s,rate=rate,v1=v1,v2=v2,C=C,D=D,f0=f0,p0=p0,
                fb=fb,pb=pb,qf=charge(v2),charge=charge)


def early_fields(base,cfg):
    Phi = cfg.amplitude; v1,v2,rate = base['v1'],base['v2'],base['rate']
    ph1,ph2 = cmath.exp(-1j*rate*math.log(v1)),cmath.exp(-1j*rate*math.log(v2))
    def on(z):
        f,fx = harmonic_transfer(base['f0'],base['p0'],Phi/v1,v1*z)
        return f,fx,0.,Phi*ph1*z,Phi*ph1,v1
    def charging(z):
        x = v1*math.exp(z); s = base['s']; C,D = base['C'],base['D']
        f = C*x**s+D*x**(1-s)
        fx = s*C*x**(s-1)+(1-s)*D*x**(-s)
        field = Phi*cmath.exp(-1j*rate*math.log(x))
        return f,fx,base['charge'](x),field,-1j*rate*field,x
    def off(z):
        x = v2+(1-v2)*z
        f,fx = harmonic_transfer(base['fb'],base['pb'],Phi/(1-v2),x-1)
        return f,fx,base['qf'],Phi*ph2*(1-z),-Phi*ph2,1-v2
    return [(on,1.),(charging,math.log(v2/v1)),(off,1.)]


def limit_start(cfg):
    Phi,rho,e,R = cfg.amplitude,cfg.radius_ratio,cfg.coupling,cfg.radius
    K = Phi*math.cos(Phi)**2*(1-rho*rho)/2
    s = (e*R*K)**2/(1+(e*R*K)**2)
    base = prepare(s,1.,0.,cfg)
    state = [base['f0']/base['p0'],0j]
    for field,end in early_fields(base,cfg):
        def rhs(z,state):
            f,fx,q,phi,phiz,dx = field(z)
            H,J = state
            nu = -H/(4*R*f)
            return [dx*(1-q*q/(f*f)),-nu*phiz-1j*e*q*phi*dx/(4*f)]
        state = integrate(rhs,(0.,end),state,cfg).y[:,-1]
    I = quad(lambda x:late_bump(x)[0],0,1,epsabs=1e-13,epsrel=1e-13)[0]
    W0 = state[1]/(1j*e*I/4)
    W1,W2 = 15*W0/4,-3*W0/4
    return np.array([s,W1.real,W1.imag,W2.real,W2.imag])


def jet_rhs(r,lam,Q,field,V,state,e):
    H,T,P,K = state
    nu = -H/(4*r); a,b,c = nu/r,lam/r,1j*e*Q/(4*r*r)
    ruv = -nu*lam/r-(1-Q*Q/(r*r))/(4*r)
    au = (T*nu-r*abs(P)**2)/r-nu*nu/(r*r)
    bu = ruv/r-nu*lam/(r*r)
    Qu = -e*r*r*(field*np.conj(P)).imag
    cu = 1j*e*(Qu+Q*(T-2*nu/r))/(4*r*r)
    return np.array([1-Q*Q/(r*r),
        -2*(P*np.conj(V)).real+1/(2*r*r)+2*nu*lam/(r*r)-Q*Q/r**4,
        -a*V-b*P-c*field,
        -b*K+(a*b-bu-3*c)*P+(a*a-au)*V-(a*c+cu)*field])


def evaluate(parameters,cfg,diagnostics=False,return_solution=False):
    cfg.validate()
    s,w1r,w1i,w2r,w2i = map(float,parameters)
    W = np.array([complex(w1r,w1i),complex(w2r,w2i)])
    beta,R,e = cfg.beta,cfg.radius,cfg.coupling
    def radial(y,z):
        _,gp = pulses(y)
        return [z[1],-beta**2*abs(W@gp)**2*z[0]]
    backward = integrate(radial,(1.,0.),[1.,0.],cfg)
    fb,fyb = backward.y[:,-1].real
    base = prepare(s,fb,beta/(1-beta)*fyb,cfg)
    state = np.array([beta*base['f0']/base['p0'],0.,0.,0.],dtype=complex)
    pieces = []
    for fields,end in early_fields(base,cfg):
        def rhs(z,state):
            f,fx,q,phi,phiz,dx = fields(z)
            dv = beta*dx
            return dv*jet_rhs(R*f,R*fx/beta,R*q,phi,phiz/dv,state,e)
        sol = integrate(rhs,(0.,end),state,cfg)
        pieces.append(sol); state = sol.y[:,-1]
    def late(y,state):
        f,fy = backward.sol(y).real
        g,gp = pulses(y)
        return (1-beta)*jet_rhs(R*f,R*fy/(1-beta),R*base['qf'],
                                beta*(W@g),beta*(W@gp)/(1-beta),state,e)
    sol = integrate(late,(0.,1.),state,cfg); pieces.append(sol)
    H,T,P,K = sol.y[:,-1]
    residual = np.array([base['qf']-1,(P/beta).real,(P/beta).imag,(K/beta).real,(K/beta).imag])
    if return_solution:
        return base,backward,pieces,W
    if not diagnostics:
        return residual
    minimum_H = min(float(np.min(piece.sol(np.linspace(piece.t[0],piece.t[-1],513))[0].real))
                    for piece in pieces)
    cap = R*base['f0']
    length = 2*R*base['p0']*base['v1']
    return dict(configuration=asdict(cfg),parameters=list(parameters),scaled_residual=residual.tolist(),
                min_sampled_H=minimum_H,terminal_Q=R*base['qf'],
                centre_normalized_cap_radius=cap,centre_normalized_onset_length=length,
                centre_normalized_cone_length_after_onset_start=2*R*base['p0']/beta,
                evidence='E0_C0_two_jet_shooting',smooth_layer_resolved=False,
                rigorous_root_box=False,goal_A_proved=False)


def main():
    runs = []
    for beta in (.003,.001,.0003,.0001):
        cfg = Configuration(beta=beta)
        initial = limit_start(cfg)
        sol = root(lambda p:evaluate(p,cfg),initial,method='hybr',options={'xtol':2e-9})
        report = evaluate(sol.x,cfg,True)
        report.update(solver_success=bool(sol.success),solver_message=str(sol.message),
                      passes_sampled_H_screen=bool(report['min_sampled_H']>0))
        runs.append(report)
        print(json.dumps(report),flush=True)
    folder = Path(__file__).resolve().parent
    result = dict(evidence='E0_new_shape_finite_beta_two_jet_roots',runs=runs,
                  smooth_member_certified=False,full_AF_Cauchy_realization=False,goal_A_proved=False)
    names = ['new_shape_jets.py','first_jet_shooting.py','second_jet_shooting.py']
    result['source_sha256'] = {name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'NEW_SHAPE_JETS_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
