"""E0 C0-early cone shooting for two transverse jets; not a PDE certificate."""

import cmath
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
from first_jet_shooting import (ShootingConfiguration, late_bump,
                                prepare_radius, harmonic_transfer, limit_start)


def pulses(y):
    g1,d1=late_bump(3*y)
    g2,d2=late_bump(3*y-2)
    return np.array([g1,g2]),3*np.array([d1,d2])


def integrate(fun, interval, initial, cfg):
    out=solve_ivp(fun,interval,np.asarray(initial,dtype=complex),method='DOP853',
                  rtol=cfg.rtol,atol=cfg.atol,max_step=cfg.max_step,dense_output=True)
    if not out.success or not np.isfinite(out.y).all():
        raise ArithmeticError(out.message)
    return out


def evaluate_second(parameters,cfg,diagnostics=False):
    cfg.validate()
    if cfg.beta<=0:
        raise ValueError('finite positive beta required; auxiliary limit is analytic')
    s,w1r,w1i,w2r,w2i=map(float,parameters)
    W=np.array([complex(w1r,w1i),complex(w2r,w2i)])
    beta,R,e,Phi=cfg.beta,cfg.radius,cfg.coupling,cfg.amplitude
    def radial(y,z):
        _,gp=pulses(y)
        return (z[1],-beta**2*abs(W@gp)**2*z[0])
    back=integrate(radial,(1.,0.),[1.,0.],cfg)
    fb,fyb=back.y[:,-1].real
    base=prepare_radius(s,fb,beta/(1-beta)*fyb,cfg)
    v1,v2,rate=base['v1'],base['v2'],base['lam']
    ph1,ph2=cmath.exp(-1j*rate*math.log(v1)),cmath.exp(-1j*rate*math.log(v2))

    # State uses actual H,T,P,K. Per-piece coordinates resolve the early C0
    # joints; no delta terms arise since phi is continuous and phi' is bounded.
    def jet_rhs(r,lam,Q,field,V,state):
        H,T,P,K=state
        nu=-H/(4*r)
        a,b,c=nu/r,lam/r,1j*e*Q/(4*r*r)
        ruv=-nu*lam/r-(1-Q*Q/(r*r))/(4*r)
        au=(T*nu-r*abs(P)**2)/r-nu*nu/(r*r)
        bu=ruv/r-nu*lam/(r*r)
        Qu=-e*r*r*(field*np.conj(P)).imag
        cu=1j*e*(Qu+Q*(T-2*nu/r))/(4*r*r)
        return np.array([1-Q*Q/(r*r),
            -2*(P*np.conj(V)).real+1/(2*r*r)+2*nu*lam/(r*r)-Q*Q/r**4,
            -a*V-b*P-c*field,
            -b*K+(a*b-bu-3*c)*P+(a*a-au)*V-(a*c+cu)*field])

    def early(rf,fx,q,field,field_z,dx_dz,state):
        dv=beta*dx_dz
        return dv*jet_rhs(R*rf,R*fx/beta,R*q,field,field_z/dv,state)
    def on(z,state):
        f,fx=harmonic_transfer(base['f0'],base['p0'],Phi/v1,v1*z)
        return early(f,fx,0.,Phi*ph1*z,Phi*ph1,v1,state)
    def charging(z,state):
        x=v1*math.exp(z)
        f=base['C']*x**s+base['D']*x**(1-s)
        fx=s*base['C']*x**(s-1)+(1-s)*base['D']*x**(-s)
        field=Phi*cmath.exp(-1j*rate*math.log(x))
        return early(f,fx,base['charge'](x),field,-1j*rate*field,x,state)
    def off(z,state):
        x=v2+(1-v2)*z
        f,fx=harmonic_transfer(fb,beta/(1-beta)*fyb,Phi/(1-v2),x-1)
        return early(f,fx,base['qf'],Phi*ph2*(1-z),-Phi*ph2,1-v2,state)
    pieces=[]
    state=np.array([beta*base['f0']/base['p0'],0,0,0],dtype=complex)
    for fun,end in ((on,1.),(charging,math.log(v2/v1)),(off,1.)):
        sol=integrate(fun,(0.,end),state,cfg)
        pieces.append(sol)
        state=sol.y[:,-1]
    early_end=state.copy()
    def late(y,state):
        f,fy=back.sol(y).real
        g,gp=pulses(y)
        return (1-beta)*jet_rhs(R*f,R*fy/(1-beta),R*base['qf'],
                                beta*(W@g),beta*(W@gp)/(1-beta),state)
    sol=integrate(late,(0.,1.),state,cfg)
    pieces.append(sol)
    H,T,P,K=sol.y[:,-1]
    residual=np.array([base['qf']-1,(P/beta).real,(P/beta).imag,
                       (K/beta).real,(K/beta).imag])
    if not diagnostics:
        return residual
    minimum=min(float(np.min(p.sol(np.linspace(p.t[0],p.t[-1],401))[0].real)) for p in pieces)
    return dict(parameters=list(parameters),beta=beta,scaled_residual=residual.tolist(),
                P_over_beta=[(P/beta).real,(P/beta).imag],
                K_over_beta=[(K/beta).real,(K/beta).imag],
                early_K_over_beta_squared=[(early_end[3]/beta**2).real,
                                           (early_end[3]/beta**2).imag],
                T_final=T.real,min_sampled_H=minimum,r_initial=R*base['f0'],
                evidence='E0_C0_early_piecewise_ODE',smooth_layer_resolved=False,
                rigorous_root_box=False,goal_A_proved=False)


def initial_second(cfg):
    s,wr,wi=limit_start(cfg)
    return np.array([s,15*wr/4,15*wi/4,-3*wr/4,-3*wi/4])


def solve_second(cfg,initial=None):
    start=initial_second(cfg) if initial is None else initial
    sol=root(lambda p:evaluate_second(p,cfg),start,method='hybr',options={'xtol':2e-9})
    report=evaluate_second(sol.x,cfg,True)
    report['solver_success']=bool(sol.success)
    report['solver_message']=str(sol.message)
    return sol.x,report
