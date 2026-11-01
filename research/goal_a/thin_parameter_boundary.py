"""Uniform thin-layer bounds with cap-radius and onset-length intervals."""

from fractions import Fraction as Q
from hashlib import sha256
import json
import math
import numpy as np
from verify_horizon_seed import I,up,trig_half
from certify_onset_boundary import add,mul,scale,bounds,hermite,exp_bound
from thin_boundary_certificate import trig


def trig_box(x):
    if not 0<=x.lo<=x.hi<=1:raise ArithmeticError('parameter trig range')
    ca,sa=trig(x.lo);cb,sb=trig(x.hi)
    return I(cb.lo,ca.hi),I(sa.lo,sb.hi)


def geometry_box(base):
    old=json.loads((base/'ONSET_BOUNDARY_CERTIFICATE_2026-10-16.json').read_text(encoding='utf-8'))
    fixed={k:Q(v) for k,v in old['exact_constants'].items()}
    ar=I(fixed['r0']-Q(1,65536),fixed['r0']+Q(1,65536))
    length=I(fixed['length']-Q(1,8192),fixed['length']+Q(1,8192))
    c,s=trig_half();phi=Q(1,2);K=phi*c*c*(1-phi*phi)/2
    root=9*K*K/(1+9*K*K)
    limit_a=5*(phi*c*c-root*s*c)
    limit_L=10*(phi*phi*s*c+phi*root*c*c)
    if not ar.lo<limit_a.lo<=limit_a.hi<ar.hi:raise ArithmeticError('limit cap outside box')
    if not length.lo<limit_L.lo<=limit_L.hi<length.hi:raise ArithmeticError('limit width outside box')
    return old,fixed,ar,length,dict(
        cap_radius_interval=[str(ar.lo),str(ar.hi)],onset_length_interval=[str(length.lo),str(length.hi)],
        auxiliary_limit_cap_interval=[str(limit_a.lo),str(limit_a.hi)],
        auxiliary_limit_length_interval=[str(limit_L.lo),str(limit_L.hi)],
        auxiliary_limit_strictly_inside=True,
        auxiliary_zero_parameters_are_physical_data=False)


def certify(values,slopes,v_exact,base):
    old,fixed,ar,length,box=geometry_box(base)
    for name,want in old['source_sha256'].items():
        if sha256((base/name).read_bytes()).hexdigest()!=want:raise ArithmeticError('stale shape source')
    cap,r0=fixed['cap'],fixed['r0'];q=fixed['amplitude']/length
    if v_exact[0]!=cap or v_exact[-1]!=fixed['end']:raise ArithmeticError('parameter endpoints')
    qmax=up(Q(old['rational_bounds']['q_absolute'])*fixed['length']/length.lo)
    width=Q(1,2**40);T=v_exact[-1]-cap;Rmax=ar.hi+T/2
    if width>=v_exact[1]-cap or qmax>1 or T>=length.lo-width:raise ArithmeticError('parameter domain')
    energy=up(exp_bound(T).hi*Rmax*(qmax*qmax+q.hi*q.hi)*width)
    if ar.lo*(1-(q.hi*T)**2/2)<=energy:raise ArithmeticError('parameter radius')
    shift=2*(ar-r0)
    result=np.zeros((len(v_exact),6))
    for j,(left,right) in enumerate(zip(v_exact,v_exact[1:])):
        h=right-left;mid=(left+right)/2-cap
        c,s=trig_box(q*mid);r=ar*c+s/(2*q);rp=-ar*q*s+c/2
        t=[-Q(1,2),Q(1)];t2=mul(t,t);t3=mul(t2,t)
        model=add(add([r],scale(t,rp*h)),add(scale(t2,-q*q*r*h*h/2),scale(t3,-q*q*rp*h**3/6)))
        rem=q.hi**4*Rmax*h**4/384
        polys=[hermite(values[j,k],values[j+1,k],slopes[j,k],slopes[j+1,k],h) for k in range(3)]
        dr=bounds(add(model,scale(polys[0],-1)))
        er=max(abs(dr.lo),abs(dr.hi))+rem+energy
        dk=bounds(add(model,scale(mul([I(left)+shift,h],polys[1]),-1)))
        ek=(max(abs(dk.lo),abs(dk.hi))+rem+energy)/(left+shift.lo)
        if j==0:
            bt=bounds(polys[2]);maximum=qmax*(ar.hi+h/2+energy)
            et=max(abs(bt.lo),abs(bt.hi),abs(maximum-bt.lo),abs(maximum-bt.hi))
        else:
            dt=bounds(add(scale(model,q),scale(polys[2],-1)))
            et=max(abs(dt.lo),abs(dt.hi))+q.hi*(rem+energy)
        result[j+1,:3]=[math.nextafter(float(up(a)),math.inf) for a in (er,ek,et)]
    signature=sha256(json.dumps(dict(v=[str(v) for v in v_exact],
        values=[[float(a).hex() for a in row[:3]] for row in values],
        slopes=[[float(a).hex() for a in row[:3]] for row in slopes]),sort_keys=True).encode()).hexdigest()
    return result,dict(**box,uniform_physical_width_upper=str(width),
        radial_C1_difference_from_own_C0_bound=str(energy),shape_q_upper=str(qmax),
        maximum_boundary_errors=np.max(result,axis=0).tolist(),boundary_sha256=signature,
        coordinate_identification='v_physical = v_reference + 2*(r_cap-r_cap_reference)',
        actual_thin_parameter_boundary_certified=True)
