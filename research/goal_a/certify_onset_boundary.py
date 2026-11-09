"""Rational posteriori bounds for the resolved neutral onset boundary.

The exact data are defined by frozen binary64 constants read from the existing
experiment. This does NOT certify their agreement with the original eta seed.
"""

from fractions import Fraction as F
from hashlib import sha256
import json
import math
from pathlib import Path
import numpy as np
from neutral_transport import onset_boundaries, fourth_derivative
from verify_horizon_seed import I, up


def absolute(x):
    x=I.lift(x)
    return max(abs(x.lo),abs(x.hi))


def exp_bound(x):
    x=F(x)
    if x<0:
        return exp_bound(-x).reciprocal()
    squares=0
    while x>1:
        x/=2; squares+=1
    term,total=I(1),I(1)
    for k in range(1,25):
        term=term*x/k;total=total+term
    remainder=F(1,math.factorial(25))/(1-F(1,26))
    total=I(total.lo,up(total.hi+remainder))
    for _ in range(squares):
        total=total*total
    return total


def chi_point(y):
    if not 0<y<1:
        raise ValueError('interior point required')
    if y>F(1,2):
        return 1-chi_point(1-y)
    return 1/(1+exp_bound(1/y-1/(1-y)))


def q_jets(y,amplitude_over_length,width):
    """Enclose q, q_v, q_vv away from the analytically bounded tails."""
    if not F(1,64)<=y.lo<=y.hi<=F(63,64):
        raise ValueError('interior interval required')
    chi=I(chi_point(y.lo).lo,chi_point(y.hi).hi)
    B=1/y**2+1/(1-y)**2
    B1=-2/y**3+2/(1-y)**3
    B2=6/y**4+6/(1-y)**4
    first=chi*(1-chi)*B
    second=chi*(1-chi)*((1-2*chi)*B**2+B1)
    third=chi*(1-chi)*((1-6*chi+6*chi**2)*B**3+3*(1-2*chi)*B*B1+B2)
    scale=amplitude_over_length
    return (scale*(chi+y*first),scale*(2*first+y*second)/width,
            scale*(3*second+y*third)/width**2)


def add(a,b):
    out=[I(0) for _ in range(max(len(a),len(b)))]
    for i,x in enumerate(a):out[i]=out[i]+x
    for i,x in enumerate(b):out[i]=out[i]+x
    return out


def mul(a,b):
    out=[I(0) for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=out[i+j]+I.lift(x)*y
    return out


def scale(a,s):
    return [I.lift(x)*s for x in a]


def bounds(a):
    n=len(a)-1
    coefficients=[sum((I.lift(a[j])*F(math.comb(k,j),math.comb(n,j))
                       for j in range(k+1)),I(0)) for k in range(n+1)]
    return I(min(x.lo for x in coefficients),max(x.hi for x in coefficients))


def compose(a,offset,slope):
    out=[I(0)]
    for coefficient in reversed(a):
        out=add(mul(out,[offset,slope]),[coefficient])
    return out


def hermite(a,b,da,db,h):
    a,b,da,db=map(F,(a,b,da,db))
    return [a,h*da,3*(b-a)-h*(2*da+db),2*(a-b)+h*(da+db)]


def coarse_boundary_signature(values,slopes,cap,end):
    payload=dict(cap=str(F(cap)),end=str(F(end)),
        values=[[float(x).hex() for x in row[:3]] for row in values],
        v_derivatives=[[float(x).hex() for x in row[:3]] for row in slopes])
    return sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def field_model(left,right,cap,width,qscale):
    """Affine Taylor models of q and q² in local t in [0,1]."""
    h=right-left
    yl,yr=(left-cap)/width,(right-cap)/width
    if yr<=F(1,64):
        qref=F(0);err=qscale*F(387,2**64)
    elif yl>=F(63,64) and yr<=1:
        qref=qscale;err=qscale*F(24579,2**64)
    elif yl>=1:
        qref=qscale;err=F(0)
    else:
        whole=q_jets(I(yl,yr),qscale,width)
        q,qp,_=q_jets(I((yl+yr)/2),qscale,width)
        second_square=2*(whole[1]**2+whole[0]*whole[2])
        return ([q-qp*h/2,qp*h],absolute(whole[2])*h*h/8,
                [q*q-q*qp*h,2*q*qp*h],absolute(second_square)*h*h/8,
                whole[0])
    return ([I(qref)],err,[I(qref*qref)],2*abs(qref)*err+err*err,I(qref-err,qref+err))


def certificate(n=384,refinement=16):
    outgoing,_,params=onset_boundaries(.05)
    cap=F(params['v_cap']);r0=F(params['r_cap'])
    length=F(params['v_onset_width']);amplitude=F(params['field_amplitude'])
    # Freeze all input constants explicitly. The endpoint is the same binary64
    # operation used by the existing rectangle experiment.
    end=F(31*params['v_end']/32);epsilon=F(.05)
    width=epsilon*length;qscale=amplitude/length
    hcoarse=(end-cap)/n
    vfloat=np.linspace(float(cap),float(end),n+1)
    values=np.array([outgoing(v) for v in vfloat])
    slopes=fourth_derivative(values,0,vfloat[1]-vfloat[0])
    coarse=[[hermite(values[j,k],values[j+1,k],slopes[j,k],slopes[j+1,k],hcoarse)
             for k in range(3)] for j in range(n)]
    knots=sorted(set([cap+(end-cap)*F(j,n*refinement) for j in range(n*refinement+1)]
                     +[cap+width/64,cap+63*width/64,cap+width]))
    nodes=np.array([outgoing(float(v)) for v in knots])
    # An arbitrary numerical reference is admissible: its error is proved by
    # the differential residual, never by the DOP853 tolerance.
    radial_slopes=(nodes[:,0]-2*nodes[:,5])/np.array([float(v) for v in knots])
    residual_integral=F(0);rmin=None;qmax=F(0)
    approximation_errors=[F(0)]*3
    for j,(left,right) in enumerate(zip(knots,knots[1:])):
        h=right-left
        radius=hermite(nodes[j,0],nodes[j+1,0],radial_slopes[j],radial_slopes[j+1],h)
        rb=bounds(radius);rabs=absolute(rb)
        rmin=rb.lo if rmin is None else min(rmin,rb.lo)
        qm,qe,q2m,q2e,qb=field_model(left,right,cap,width,qscale)
        qmax=max(qmax,absolute(qb))
        residual=add([2*radius[2]/h**2,6*radius[3]/h**2],mul(radius,q2m))
        residual_bound=up(absolute(bounds(residual))+rabs*q2e)
        residual_integral=up(residual_integral+h*residual_bound)
        cell=min(n-1,int((left-cap)/hcoarse))
        origin=cap+cell*hcoarse
        approximation=[compose(poly,(left-origin)/hcoarse,h/hcoarse) for poly in coarse[cell]]
        errors=[absolute(bounds(add(radius,scale(approximation[0],-1)))),
                absolute(bounds(add(radius,scale(mul([left,h],approximation[1]),-1))))/left,
                absolute(bounds(add(mul(radius,qm),scale(approximation[2],-1))))+rabs*qe]
        approximation_errors=[max(a,up(b)) for a,b in zip(approximation_errors,errors)]
    if qmax>1:
        raise ArithmeticError('the energy estimate requires |q| <= 1')
    initial_error=abs(F(nodes[0,0])-r0)+abs(F(radial_slopes[0])-F(1,2))
    energy=up(exp_bound(end-cap).hi*(initial_error+residual_integral))
    if rmin<=energy:
        raise ArithmeticError('radius positivity not certified')
    errors=[up(approximation_errors[0]+energy),
            up(approximation_errors[1]+energy/cap),
            up(approximation_errors[2]+energy*qmax)]
    return dict(n=n,refinement=refinement,verified_subintervals=len(knots)-1,
        coarse_boundary_sha256=coarse_boundary_signature(values,slopes,cap,end),
        exact_constants={k:str(v) for k,v in dict(cap=cap,r0=r0,length=length,
                        amplitude=amplitude,epsilon=epsilon,end=end).items()},
        rational_bounds={k:str(v) for k,v in dict(q_absolute=qmax,
            radius_reference_lower=rmin,initial_error=initial_error,
            radial_residual_L1=residual_integral,radial_C1_error=energy).items()},
        outgoing_errors_r_k_theta=[str(x) for x in errors],
        outgoing_errors_display=[float(x) for x in errors],
        reference_comparison_errors_display=[float(x) for x in approximation_errors],
        actual_radius_lower_display=float(rmin-energy),
        certificate_scope='entire outgoing inflow edge: r,kappa,theta against exact dyadic Hermite',
        frozen_resolved_neutral_data=True,original_eta_seed_transfer=False,
        full_grid_PDE_certified=False,actual_trapping_certified=False)


def main():
    result=certificate()
    base=Path(__file__).resolve().parent
    files=['ONSET_BOUNDARY_CERTIFICATION.md','certify_onset_boundary.py','neutral_transport.py','neutral_onset_input.py',
           'verify_horizon_seed.py','FIRST_JET_CHECKS_2026-10-16.json']
    result['source_sha256']={name:sha256((base/name).read_bytes()).hexdigest() for name in files}
    (base/'ONSET_BOUNDARY_CERTIFICATE_2026-10-16.json').write_text(
        json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['verified_subintervals','outgoing_errors_display',
        'reference_comparison_errors_display','actual_radius_lower_display',
        'full_grid_PDE_certified','actual_trapping_certified']},indent=2))


if __name__=='__main__':
    main()
