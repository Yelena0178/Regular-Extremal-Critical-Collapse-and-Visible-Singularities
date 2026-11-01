"""E0 fixed-support constraint contraction (A-PATH01).

The callback returns (phi, radial derivative of phi, chi, ell, ell').
It must be C-infinity and flat at both support endpoints; this regularity
is a mathematical input, not something finite sampling can certify.
No spacetime evolution or interval-arithmetic guarantee is provided.
"""
from dataclasses import dataclass
import math
import numpy as np
from incoming_family import exterior_minimum


@dataclass
class Profile:
    inner: float
    outer: float
    free: object

    def validate(self):
        if not (math.isfinite(self.inner) and math.isfinite(self.outer)
                and 0 < self.inner < self.outer):
            raise ValueError('finite positive support bounds required')
        for radius in (self.inner,self.outer):
            if any(abs(value)>1e-14 for value in self.free(radius)):
                raise ValueError('profile endpoint values must vanish')


def scalar_mass_source(r,f,gradient,chi,ell):
    """Positive square form; avoids subtraction of near-null large terms."""
    b=r*ell
    D=f+b*b
    root=math.sqrt(D)
    small=f/(1+abs(b)/root)
    large=D+abs(b)*root
    plus,minus=(large,small) if b>=0 else (small,large)
    return r*r*(plus*abs(chi+gradient)**2+minus*abs(chi-gradient)**2)/4


def reconstruct(r,f,Q,profile,s):
    if r < 0 or not math.isfinite(r) or not math.isfinite(f) or f<=0:
        raise ValueError('invalid radius or nonpositive f')
    if r<=profile.inner or r>=profile.outer:
        phi,gradient,chi,ell,ellprime=0j,0j,0j,0.,0.
    else:
        phi,gradient,chi,ell,ellprime=(s*x for x in profile.free(r))
    D=f+(r*ell)**2
    root=math.sqrt(D)
    Pi=root*chi
    J=(chi*gradient.conjugate()).real
    kr=ell+r*ellprime-r*root*J
    electric=Q*root/r**2 if r else 0.
    rho=((Q/r**2)**2+D*(abs(chi)**2+abs(gradient)**2))/2 if r else 0.
    b=r*ell
    out=f/(root+b) if b>=0 else root-b
    ingoing=-f/(root-b) if b<=0 else -root-b
    return dict(r=r,f=f,Q=Q,D=D,phi=phi,gradient=gradient,chi=chi,
                Pi=Pi,ell=ell,kr=kr,electric_r=electric,
                jr=-root*J,rho=rho,
                expansion_out=2*out/r if r else None,
                expansion_in=2*ingoing/r if r else None)


def rhs(r,state,profile,s):
    Q,f=state
    x=reconstruct(r,f,Q,profile,s)
    phi,gradient,chi,ell=x['phi'],x['gradient'],x['chi'],x['ell']
    energy=scalar_mass_source(r,f,gradient,chi,ell)
    return np.array([.6*r*r*(phi*chi.conjugate()).imag,
                     (1-f)/r-Q*Q/r**3-2*energy/r])


def integrate(profile,s,steps=1024):
    profile.validate()
    if not math.isfinite(s) or not 0<=s<=1:
        raise ValueError('contraction parameter must be in [0,1]')
    if not isinstance(steps,int) or steps<16:
        raise ValueError('steps must be an integer >=16')
    radii=np.linspace(profile.inner,profile.outer,steps+1)
    h=(profile.outer-profile.inner)/steps
    state=np.array([0.,1.])
    rows=[reconstruct(radii[0],state[1],state[0],profile,s)]
    for r in radii[:-1]:
        k1=rhs(r,state,profile,s)
        k2=rhs(r+h/2,state+h*k1/2,profile,s)
        k3=rhs(r+h/2,state+h*k2/2,profile,s)
        k4=rhs(r+h,state+h*k3,profile,s)
        state=state+h*(k1+2*k2+2*k3+k4)/6
        if not np.isfinite(state).all():
            raise ArithmeticError('nonfinite constraint state')
        rows.append(reconstruct(r+h,state[1],state[0],profile,s))
    charge=float(state[0])
    mass=float(profile.outer*(1-state[1])/2+charge**2/(2*profile.outer))
    tail_min=exterior_minimum(mass,charge,profile.outer)
    if tail_min<=0:
        raise ArithmeticError('nonpositive RN exterior minimum')
    return dict(profile=profile,s=s,rows=rows,ADM_mass=mass,ADM_charge=charge,
                minimum_sampled_f=min(x['f'] for x in rows),
                analytic_tail_minimum_binary64=tail_min,
                evidence='E0 constraint ODE and analytic tail formula in binary64',
                all_radius_positivity_certified=False,
                actual_spacetime_evolved=False)


def tail_or_cap(result,r):
    profile=result['profile']
    if profile.inner<r<profile.outer:
        raise ValueError('interior evaluation requires the integrated data')
    if r<=profile.inner:
        return reconstruct(r,1.,0.,profile,result['s'])
    Q,M=result['ADM_charge'],result['ADM_mass']
    f=1-2*M/r+Q*Q/r**2
    return reconstruct(r,f,Q,profile,result['s'])
