"""Uniform exact boundary bounds for every 0 < physical ramp width <= 2^-40."""

from fractions import Fraction as Q
from hashlib import sha256
import json
import math
import numpy as np
from verify_horizon_seed import I,up
from certify_onset_boundary import add,mul,scale,bounds,hermite,exp_bound


def trig(argument):
    x=Q(argument)
    if not 0<=x<=1:raise ArithmeticError('trig range')
    cosine,ct=I(1),I(1);sine,st=I(x),I(x)
    for k in range(1,21):
        ct=-ct*x*x/((2*k-1)*(2*k));cosine=cosine+ct
        st=-st*x*x/((2*k)*(2*k+1));sine=sine+st
    return (cosine+I(-Q(1,math.factorial(42)),Q(1,math.factorial(42))),
            sine+I(-Q(1,math.factorial(43)),Q(1,math.factorial(43))))


def certify(values,slopes,v_exact,base):
    cert=json.loads((base/'ONSET_BOUNDARY_CERTIFICATE_2026-10-16.json').read_text(encoding='utf-8'))
    for name,want in cert['source_sha256'].items():
        if sha256((base/name).read_bytes()).hexdigest()!=want:raise ArithmeticError('stale shape bound')
    constants={k:Q(v) for k,v in cert['exact_constants'].items()}
    cap,r0,L,amplitude=map(constants.get,('cap','r0','length','amplitude'))
    if v_exact[0]!=cap or v_exact[-1]!=constants['end']:raise ArithmeticError('endpoint mismatch')
    q=amplitude/L;qmax=Q(cert['rational_bounds']['q_absolute']);width=Q(1,2**40)
    if width>=v_exact[1]-cap or qmax>1:raise ArithmeticError('thin width or shape bound')
    T=v_exact[-1]-cap;Rmax=r0+T/2
    # Difference equation r_w'' + q_w^2 r_w = 0 against the C0 harmonic
    # radius. Its forcing is supported on length <= width; |q_w| <= qmax <=1.
    energy=up(exp_bound(T).hi*Rmax*(qmax*qmax+q*q)*width)
    if r0*(1-(q*T)**2/2)<=energy:raise ArithmeticError('uniform radius positivity')
    result=np.zeros((len(v_exact),6));local=[]
    for j,(left,right) in enumerate(zip(v_exact,v_exact[1:])):
        h=right-left;mid=(left+right)/2-cap
        c,s=trig(q*mid);r= r0*c+s/(2*q);rp=-r0*q*s+c/2
        t=[-Q(1,2),Q(1)];t2=mul(t,t);t3=mul(t2,t)
        model=add(add([r],scale(t,rp*h)),add(scale(t2,-q*q*r*h*h/2),scale(t3,-q*q*rp*h**3/6)))
        remainder=q**4*Rmax*h**4/384
        polys=[hermite(values[j,k],values[j+1,k],slopes[j,k],slopes[j+1,k],h) for k in range(3)]
        er=max(abs(bounds(add(model,scale(polys[0],-1))).lo),abs(bounds(add(model,scale(polys[0],-1))).hi))+remainder+energy
        dk=bounds(add(model,scale(mul([left,h],polys[1]),-1)))
        ek=(max(abs(dk.lo),abs(dk.hi))+remainder+energy)/left
        if j==0:
            theta=bounds(polys[2]);theta_max=qmax*(r0+h/2+energy)
            et=max(abs(theta.lo),abs(theta.hi),abs(theta_max-theta.lo),abs(theta_max-theta.hi))
        else:
            dt=bounds(add(scale(model,q),scale(polys[2],-1)))
            et=max(abs(dt.lo),abs(dt.hi))+q*(remainder+energy)
        errors=[up(er),up(ek),up(et)]
        result[j+1,:3]=[math.nextafter(float(e),math.inf) for e in errors]
        local.append([str(e) for e in errors])
    signature=sha256(json.dumps(dict(v=[str(v) for v in v_exact],
        values=[[float(a).hex() for a in row[:3]] for row in values],
        slopes=[[float(a).hex() for a in row[:3]] for row in slopes]),sort_keys=True).encode()).hexdigest()
    return result,dict(uniform_physical_width_upper=str(width),uniform_width_range='0 < w <= 2^-40',
        radial_C1_difference_from_C0_bound=str(energy),shape_q_upper=str(qmax),
        maximum_boundary_errors=np.max(result,axis=0).tolist(),boundary_sha256=signature,
        actual_thin_family_boundary_certified=True,original_parameter_transfer=False)
