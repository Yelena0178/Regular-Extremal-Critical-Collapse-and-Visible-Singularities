"""Eight analytic inflow components for the equivalent u-constrained system.

Uses the same frozen rational cone, without changing old certificates.
"""

from fractions import Fraction as Q
from hashlib import sha256
import cmath
import json
from pathlib import Path
import numpy as np

import frozen_charged_boundary as old
from frozen_charged_boundary import (I,J,R,E,PHI,S,START,S0,V1,V2,COS,RATE,B,A0,
    QFINAL,IntervalWidthError,exact_mesh,power,trigonometric,logarithm)
from certify_onset_boundary import add,mul,scale,bounds,hermite
from verify_horizon_seed import up


def boundary_jets(piece,V,strict=False,details=False):
    original,H,rbound=old.boundary_jets(piece,V,strict,True)
    r,k,tr,ti=original;x=(I.lift(V)-START)/S
    if piece==1:
        rv4=r.c[4]*(S0-4)/(S*x)
        q=J(B*power(x/V2,2*S0))
        for j in range(1,5):q.c[j]=q.c[j-1]*(2*S0-j+1)/(j*S*x)
        q.c[0]=q.c[0]-B*A0
        pc,ps=trigonometric(RATE*logarithm(x));pr0,pi0=PHI*pc,-PHI*ps
    else:
        w=PHI/(V1 if piece==0 else 1-V2)
        rv4=w**4*r.c[1]/(24*S**4)
        q=J(0 if piece==0 else QFINAL)
        pc,ps=trigonometric(RATE*logarithm(I(V1 if piece==0 else V2)))
        weight=x/V1 if piece==0 else (1-x)/(1-V2)
        pr0,pi0=PHI*pc*weight,-PHI*ps*weight
    rv=J(coefficients=[(j+1)*r.c[j+1] for j in range(4)]+[rv4])
    vr,vi=tr/r,ti/r
    pr=J(coefficients=[pr0]+[vr.c[j-1]/j for j in range(1,5)])
    pi=J(coefficients=[pi0]+[vi.c[j-1]/j for j in range(1,5)])
    m=r*(1-rv/k)/2
    result=original+(m,pr,pi,R*q)
    return (result,H,rbound) if details else result


def proposal(V,piece):
    values,slopes=old.proposal(V,piece)
    r,k,tr,ti=values;rp=slopes[0];theta=tr+1j*ti
    s,phi,v1,v2,c,rate,f0,p0,Bf,a,integral=old.FLOAT
    x=(V-float(START))/float(S)
    if piece==0:
        field=phi*cmath.exp(-1j*rate*np.log(v1))*x/v1;q=0.
    elif piece==1:
        field=phi*cmath.exp(-1j*rate*np.log(x));q=float(R)*Bf*((x/v2)**(2*s)-a)
    else:
        field=phi*cmath.exp(-1j*rate*np.log(v2))*(1-x)/(1-v2);q=float(R)*Bf*(1-a)
    m=r*(1-rp/k)/2
    mv=q*q*k*(1-2*m/r)/(2*r*r)+abs(theta)**2/(2*k)
    pv=theta/r;qv=float(E)*r*(field*theta.conjugate()).imag
    return (np.r_[values,m,field.real,field.imag,q],
            np.r_[slopes,mv,pv.real,pv.imag,qv])


def fourth_bounds(piece,a,b,depth=0):
    try:
        jets,H,r=boundary_jets(piece,I(a,b),True,True)
        return [max(abs(j.c[4].lo),abs(j.c[4].hi)) for j in jets],H.lo,r.lo,depth
    except IntervalWidthError:
        if depth>=24:raise ArithmeticError('u-boundary subdivision exhausted')
        mid=(a+b)/2
        left=fourth_bounds(piece,a,mid,depth+1);right=fourth_bounds(piece,mid,b,depth+1)
        return ([max(a,b) for a,b in zip(left[0],right[0])],min(left[1],right[1]),
                min(left[2],right[2]),max(left[3],right[3]))


def certify(n=96):
    reports=[]
    for piece in range(3):
        mesh=exact_mesh(n,piece);data=[proposal(float(v),piece) for v in mesh]
        errors=[Q(0)]*8;least_H=None;least_r=None;max_depth=0
        for j,(a,b) in enumerate(zip(mesh,mesh[1:])):
            h=b-a;jets=boundary_jets(piece,I((a+b)/2))
            fourth,lh,lr,depth=fourth_bounds(piece,a,b)
            least_H=lh if least_H is None else min(least_H,lh)
            least_r=lr if least_r is None else min(least_r,lr);max_depth=max(max_depth,depth)
            z=[-Q(1,2),Q(1)];powers=[[I(1)]]
            for p in range(1,4):powers.append(mul(powers[-1],z))
            for k in range(8):
                model=[I(0)]
                for p in range(4):model=add(model,scale(powers[p],jets[k].c[p]*h**p))
                poly=hermite(data[j][0][k],data[j+1][0][k],data[j][1][k],data[j+1][1][k],h)
                difference=bounds(add(model,scale(poly,-1)))
                errors[k]=max(errors[k],up(max(abs(difference.lo),abs(difference.hi))+fourth[k]*h**4/16))
        reports.append(dict(piece=piece,cells=n,errors=[str(e) for e in errors],
            display_errors=[float(e) for e in errors],minimum_H_lower=str(least_H),
            minimum_r_lower=str(least_r),maximum_derivative_subdivision=max_depth))
        print(json.dumps(dict(stage='u_boundary',**reports[-1])),flush=True)
    return reports


def main():
    folder=Path(__file__).resolve().parent
    result=dict(status='PASS',scope='eight inflow fields of the same frozen C0 cone',
        components=['r','k','tr','ti','m','pr','pi','Q'],pieces=certify(),
        complete_rectangle_certified=False,actual_smooth_seed_certified=False,goal_A_proved=False)
    names=['frozen_charged_u_boundary.py','frozen_charged_boundary.py',old.SPEC,
        'verify_horizon_seed.py','certify_onset_boundary.py','thin_boundary_certificate.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'FROZEN_CHARGED_U_BOUNDARY_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],goal_A_proved=False)),flush=True)


if __name__=='__main__':main()
