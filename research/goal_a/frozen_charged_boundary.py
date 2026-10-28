"""Exact-input C0 cone: rational knots and outward Taylor boundary jets.

Unlike an endpoint root, this reference has no imposed exact terminal charge
or terminal radius. All affine-coordinate constants are frozen rationals.
"""

from fractions import Fraction as Q
from functools import lru_cache
import cmath
import json
import math
from pathlib import Path

import numpy as np

from verify_horizon_seed import I,down,up,log_two
from certify_onset_boundary import exp_bound,add,mul,scale,bounds,hermite
from thin_boundary_certificate import trig


SPEC='FROZEN_CHARGED_CONE_2026-10-17.json'
PARAMETERS=json.loads((Path(__file__).resolve().parent/SPEC).read_text())
R,E,PHI,S,START,S0,V1,V2=[Q(PARAMETERS[k]) for k in ('R','e','Phi','S','cap','s','v1','v2')]


@lru_cache(None)
def logarithm_point(x):
    x=Q(x)
    if x<=0:raise ArithmeticError('logarithm domain')
    shift=0
    while x<1:x*=2;shift-=1
    while x>=2:x/=2;shift+=1
    z=(x-1)/(x+1);n=96
    value=2*sum((z**(2*j+1)/(2*j+1) for j in range(n)),Q(0))
    tail=2*z**(2*n+1)/((2*n+1)*(1-z*z))
    return I(down(value),up(value+tail))+shift*log_two()


def logarithm(x):return I(logarithm_point(x.lo).lo,logarithm_point(x.hi).hi)


def exponential(x):return I(exp_bound(x.lo).lo,exp_bound(x.hi).hi)


def power(x,a):return exponential(I.lift(a)*logarithm(I.lift(x)))


@lru_cache(None)
def trig_point(x):
    x=Q(x);sign=1 if x>=0 else -1;x=abs(x);count=0
    while x>1:x/=2;count+=1
    c,s=trig(x)
    for _ in range(count):c,s=c*c-s*s,2*c*s
    return c,sign*s


def trigonometric(x):
    x=I.lift(x);mid=(x.lo+x.hi)/2;radius=(x.hi-x.lo)/2
    c,s=trig_point(mid)
    return I(max(-1,c.lo-radius),min(1,c.hi+radius)),I(max(-1,s.lo-radius),min(1,s.hi+radius))


def square_root(x):
    x=I.lift(x)
    if x.lo<0:raise ArithmeticError('square root domain')
    den=2**192
    def floor(value):
        z=value*den*den
        return math.isqrt(z.numerator//z.denominator)
    return I(Q(floor(x.lo),den),Q(floor(x.hi)+1,den))


COS,SIN=trig_point(PHI)
RATE=square_root(I(S0*(1-S0)))/PHI
T=Q(V1/V2);A0=power(I(T),2*S0)
F1=COS*power(I(T),S0);P1=S0*F1/V1
F0=F1*COS-P1*V1*SIN/PHI
P0=F1*PHI*SIN/V1+P1*COS
H0=F0/P0
B=E*R*PHI*square_root(I(S0*(1-S0)))*COS*COS/(2*S0)
QFINAL=B*(1-A0)


class IntervalWidthError(ArithmeticError):
    pass


def middle_integral(x):
    y=I.lift(x)/V2
    primitive=((power(y,1+2*S0)-power(I(T),1+2*S0))/(1+2*S0)
               -2*A0*(y-T)+A0*A0*(power(y,1-2*S0)-power(I(T),1-2*S0))/(1-2*S0))
    return V2*B*B*primitive/(COS*COS)


H2=H0+V2-middle_integral(I(V2))


class J:
    def __init__(self,value=0,coefficients=None):
        self.c=[I(0) for _ in range(5)] if coefficients is None else list(coefficients)
        if coefficients is None:self.c[0]=I.lift(value)
    @staticmethod
    def lift(x):return x if isinstance(x,J) else J(x)
    def __add__(self,x):
        x=self.lift(x);return J(coefficients=[a+b for a,b in zip(self.c,x.c)])
    __radd__=__add__
    def __neg__(self):return J(coefficients=[-a for a in self.c])
    def __sub__(self,x):return self+-self.lift(x)
    def __rsub__(self,x):return self.lift(x)+-self
    def __mul__(self,x):
        x=self.lift(x)
        return J(coefficients=[sum((self.c[j]*x.c[n-j] for j in range(n+1)),I(0)) for n in range(5)])
    __rmul__=__mul__
    def reciprocal(self):
        c=[1/self.c[0]]
        for n in range(1,5):c.append(-sum((self.c[j]*c[n-j] for j in range(1,n+1)),I(0))/self.c[0])
        return J(coefficients=c)
    def __truediv__(self,x):return self*self.lift(x).reciprocal()
    def __rtruediv__(self,x):return self.lift(x)*self.reciprocal()


def harmonic(f,fx,omega):
    return J(coefficients=[f,fx/S,-omega*omega*f/(2*S*S),
                           -omega*omega*fx/(6*S**3),omega**4*f/(24*S**4)])


def phi_derivative_jets(x):
    c,s=trigonometric(RATE*logarithm(x))
    rr,ii=PHI*c,-PHI*s
    real,imag=[rr],[ii]
    for j in range(1,6):
        a,b=1-j,-RATE
        rr,ii=(a*rr-b*ii)/(j*S*x),(b*rr+a*ii)/(j*S*x)
        real.append(rr);imag.append(ii)
    return (J(coefficients=[(j+1)*real[j+1] for j in range(5)]),
            J(coefficients=[(j+1)*imag[j+1] for j in range(5)]))


def boundary_jets(piece,V,strict=False,details=False):
    x=(I.lift(V)-START)/S
    if piece==0:
        c,s=trigonometric(PHI*x/V1)
        f=F0*c+P0*V1*s/PHI;fx=-F0*PHI*s/V1+P0*c
        fj=harmonic(f,fx,PHI/V1);qj=J(0);hvalue=H0+x
        pc,ps=trigonometric(RATE*logarithm(I(V1)))
        vr,vi=J(PHI*pc/(S*V1)),J(-PHI*ps/(S*V1))
    elif piece==1:
        fj=J(coefficients=[COS*power(x/V2,S0)] +
             [I(0) for _ in range(4)])
        for j in range(1,5):fj.c[j]=fj.c[j-1]*(S0-j+1)/(j*S*x)
        qj=J(B*power(x/V2,2*S0))
        for j in range(1,5):qj.c[j]=qj.c[j-1]*(2*S0-j+1)/(j*S*x)
        qj.c[0]=qj.c[0]-B*A0
        hvalue=H0+x-middle_integral(x);vr,vi=phi_derivative_jets(x)
    elif piece==2:
        omega=PHI/(1-V2);y=x-V2;c,s=trigonometric(omega*y)
        p2=S0*COS/V2;f=COS*c+p2*s/omega;fx=-COS*omega*s+p2*c
        fj=harmonic(f,fx,omega);qj=J(QFINAL)
        hvalue=H2+y-QFINAL*QFINAL*s/(COS*omega*f)
        pc,ps=trigonometric(RATE*logarithm(I(V2)))
        vr,vi=J(-PHI*pc/(S*(1-V2))),J(PHI*ps/(S*(1-V2)))
    else:raise ValueError('piece must be 0,1,2')
    if strict and (hvalue.lo<=0 or hvalue.hi-hvalue.lo>hvalue.lo/4 or fj.c[0].lo<=0):
        raise IntervalWidthError('subdivide derivative enclosure')
    rhs=(1-(qj/fj)*(qj/fj))/S
    hj=J(coefficients=[hvalue]+[rhs.c[j-1]/j for j in range(1,5)])
    rj=R*fj;kj=rj/(S*hj)
    result=(rj,kj,rj*vr,rj*vi)
    return (result,hvalue,rj.c[0]) if details else result


def float_constants():
    s,phi,v1,v2,e,Rf=map(float,(S0,PHI,V1,V2,E,R))
    c=math.cos(phi);t=v1/v2;rate=math.sqrt(s*(1-s))/phi
    f1=c*t**s;p1=s*f1/v1
    f0=f1*math.cos(phi)-p1*v1*math.sin(phi)/phi
    p0=f1*phi*math.sin(phi)/v1+p1*math.cos(phi)
    Bf=e*Rf*phi*math.sqrt(s*(1-s))*c*c/(2*s);a=t**(2*s)
    def integral(x):
        y=x/v2
        return v2*Bf*Bf/(c*c)*((y**(1+2*s)-t**(1+2*s))/(1+2*s)-2*a*(y-t)
                    +a*a*(y**(1-2*s)-t**(1-2*s))/(1-2*s))
    return s,phi,v1,v2,c,rate,f0,p0,Bf,a,integral


FLOAT=float_constants()


def proposal(V,piece):
    s,phi,v1,v2,c,rate,f0,p0,Bf,a,integral=FLOAT
    scale,cap=float(S),float(START);x=(V-cap)/scale
    if piece==0:
        w=phi/v1;f=f0*math.cos(w*x)+p0*math.sin(w*x)/w
        fx=-f0*w*math.sin(w*x)+p0*math.cos(w*x);q=0.;H=f0/p0+x
        pv=phi*cmath.exp(-1j*rate*math.log(v1))/(scale*v1);pvv=0j
    elif piece==1:
        f=c*(x/v2)**s;fx=s*f/x;q=Bf*((x/v2)**(2*s)-a);H=f0/p0+x-integral(x)
        field=phi*cmath.exp(-1j*rate*math.log(x));z=-1j*rate
        pv=z*field/(scale*x);pvv=z*(z-1)*field/(scale*scale*x*x)
    else:
        w=phi/(1-v2);y=x-v2;p2=s*c/v2
        f=c*math.cos(w*y)+p2*math.sin(w*y)/w
        fx=-c*w*math.sin(w*y)+p2*math.cos(w*y);q=Bf*(1-a)
        H=f0/p0+v2-integral(v2)+y-q*q*math.sin(w*y)/(c*w*f)
        pv=-phi*cmath.exp(-1j*rate*math.log(v2))/(scale*(1-v2));pvv=0j
    r=float(R)*f;rp=float(R)*fx/scale;k=r/(scale*H);Hp=(1-q*q/(f*f))/scale
    kp=rp/(scale*H)-r*Hp/(scale*H*H);theta=r*pv;tp=rp*pv+r*pvv
    return np.array([r,k,theta.real,theta.imag]),np.array([rp,kp,tp.real,tp.imag])


def exact_mesh(n,piece):
    if piece==0:xs=[V1*Q(j,n) for j in range(n+1)]
    elif piece==1:
        # Dyadic interior proposals, exact rational physical endpoints.
        xs=[V1]+[Q(float(V1)*math.exp(math.log(float(V2/V1))*j/n)) for j in range(1,n)]+[V2]
    else:xs=[V2+(1-V2)*Q(j,n) for j in range(n+1)]
    return [START+S*x for x in xs]


def fourth_bounds(piece,a,b,depth=0):
    try:
        jets,H,r=boundary_jets(piece,I(a,b),strict=True,details=True)
        return [max(abs(j.c[4].lo),abs(j.c[4].hi)) for j in jets],H.lo,r.lo,depth
    except IntervalWidthError:
        if depth>=24:raise ArithmeticError('boundary derivative subdivision exhausted')
        mid=(a+b)/2
        left=fourth_bounds(piece,a,mid,depth+1);right=fourth_bounds(piece,mid,b,depth+1)
        return [max(x,y) for x,y in zip(left[0],right[0])],min(left[1],right[1]),min(left[2],right[2]),max(left[3],right[3])


def certify(n=96):
    reports=[]
    for piece in range(3):
        mesh=exact_mesh(n,piece);values=[];slopes=[]
        for V in mesh:
            value,slope=proposal(float(V),piece);values.append(value);slopes.append(slope)
        error=[Q(0)]*4;least_H=None;least_r=None;max_depth=0
        for j,(a,b) in enumerate(zip(mesh,mesh[1:])):
            h=b-a;middle=boundary_jets(piece,I((a+b)/2));fourth,lh,lr,depth=fourth_bounds(piece,a,b)
            least_H=lh if least_H is None else min(least_H,lh)
            least_r=lr if least_r is None else min(least_r,lr);max_depth=max(max_depth,depth)
            z=[-Q(1,2),Q(1)];powers=[[I(1)]]
            for k in range(1,4):powers.append(mul(powers[-1],z))
            for k in range(4):
                model=[I(0)]
                for power_index in range(4):model=add(model,scale(powers[power_index],middle[k].c[power_index]*h**power_index))
                poly=hermite(values[j][k],values[j+1][k],slopes[j][k],slopes[j+1][k],h)
                difference=bounds(add(model,scale(poly,-1)))
                rem=fourth[k]*h**4/16
                error[k]=max(error[k],up(max(abs(difference.lo),abs(difference.hi))+rem))
        reports.append(dict(piece=piece,cells=n,errors=[str(e) for e in error],
                            display_errors=[float(e) for e in error],minimum_H_lower=str(least_H),
                            minimum_r_lower=str(least_r),maximum_derivative_subdivision=max_depth))
        print(json.dumps(dict(stage='exact_boundary',**reports[-1])),flush=True)
    return reports


def main():
    from hashlib import sha256
    reports=certify(96)
    nu=-S/(4*R*P0);proposal_nu=Q(-float(S)/(4*float(R)*FLOAT[7]))
    error=nu-proposal_nu
    result=dict(status='PASS',scope='four inflow components of a frozen C0 cone; all three analytic pieces',
                pieces=reports,incoming_nu_interval=[str(nu.lo),str(nu.hi)],
                incoming_nu_proposal=str(proposal_nu),incoming_nu_error=str(max(abs(error.lo),abs(error.hi))),
                reference_is_exact_endpoint_root=False,actual_smooth_seed_certified=False,
                complete_PDE_rectangle_certified=False,goal_A_proved=False)
    folder=Path(__file__).resolve().parent
    names=['frozen_charged_boundary.py',SPEC,'verify_horizon_seed.py','certify_onset_boundary.py',
           'thin_boundary_certificate.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'FROZEN_CHARGED_BOUNDARY_CERTIFICATE_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',scope=result['scope'],goal_A_proved=False)),flush=True)


if __name__=='__main__':main()
