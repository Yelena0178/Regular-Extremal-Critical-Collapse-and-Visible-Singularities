"""Independent 80-digit boundary/jet audit; not an interval PDE proof."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

import mpmath as mp

from frozen_charged_boundary import (PARAMETERS,SPEC,I,boundary_jets,proposal,exact_mesh)
from certify_onset_boundary import hermite


mp.mp.dps=80


def number(x):
    x=Q(x);return mp.mpf(x.numerator)/x.denominator


R,e,Phi,S,cap,s,v1,v2=[number(PARAMETERS[k]) for k in ('R','e','Phi','S','cap','s','v1','v2')]
c=mp.cos(Phi);rate=mp.sqrt(s*(1-s))/Phi;t=v1/v2
f1=c*t**s;p1=s*f1/v1
f0=f1*mp.cos(Phi)-p1*v1*mp.sin(Phi)/Phi
p0=f1*Phi*mp.sin(Phi)/v1+p1*mp.cos(Phi)
B=e*R*Phi*mp.sqrt(s*(1-s))*c*c/(2*s);a=t**(2*s)


def integral(x):
    y=x/v2
    return v2*B*B/(c*c)*((y**(1+2*s)-t**(1+2*s))/(1+2*s)-2*a*(y-t)
                          +a*a*(y**(1-2*s)-t**(1-2*s))/(1-2*s))


def profile(piece,V):
    x=(V-cap)/S
    if piece==0:
        w=Phi/v1;f=f0*mp.cos(w*x)+p0*mp.sin(w*x)/w
        H=f0/p0+x;q=mp.mpf(0)
        phi=Phi*mp.exp(-1j*rate*mp.log(v1))*x/v1
        pv=Phi*mp.exp(-1j*rate*mp.log(v1))/(S*v1)
    elif piece==1:
        f=c*(x/v2)**s;q=B*((x/v2)**(2*s)-a);H=f0/p0+x-integral(x)
        phi=Phi*mp.exp(-1j*rate*mp.log(x));pv=-1j*rate*phi/(S*x)
    else:
        w=Phi/(1-v2);y=x-v2;p2=s*c/v2
        f=c*mp.cos(w*y)+p2*mp.sin(w*y)/w;q=B*(1-a)
        H=f0/p0+v2-integral(v2)+y-q*q*mp.sin(w*y)/(c*w*f)
        phi=Phi*mp.exp(-1j*rate*mp.log(v2))*(1-x)/(1-v2)
        pv=-Phi*mp.exp(-1j*rate*mp.log(v2))/(S*(1-v2))
    r=R*f;k=r/(S*H);theta=r*pv
    return (r,k,theta.real,theta.imag),R*q,phi


def require(ok,message):
    if not ok:raise ArithmeticError(message)


def main():
    folder=Path(__file__).resolve().parent
    source='FROZEN_CHARGED_BOUNDARY_CERTIFICATE_2026-10-17.json'
    cert=json.loads((folder/source).read_text());comparisons=0;identities=0
    for piece in range(3):
        mesh=exact_mesh(96,piece);error=[Q(x) for x in cert['pieces'][piece]['errors']]
        for j in (0,48,95):
            left,right=mesh[j],mesh[j+1];h=right-left
            val0,slope0=proposal(float(left),piece);val1,slope1=proposal(float(right),piece)
            polynomials=[hermite(val0[k],val1[k],slope0[k],slope1[k],h) for k in range(4)]
            for tau in (Q(1,7),Q(1,2),Q(1)):
                V=left+h*tau;jet=boundary_jets(piece,I(V));Vmp=number(V)
                for k in range(4):
                    for order in range(5):
                        actual=mp.diff(lambda at:profile(piece,at)[0][k],Vmp,order)/mp.factorial(order)
                        require(number(jet[k].c[order].lo)<=actual<=number(jet[k].c[order].hi),
                                f'high-precision jet enclosure {piece},{j},{k},{order}')
                        comparisons+=1
                    actual=profile(piece,Vmp)[0][k]
                    polynomial=sum((number(coefficient)*number(tau)**p for p,coefficient in enumerate(polynomials[k])),mp.mpf(0))
                    require(abs(actual-polynomial)<=number(error[k]),'certified full-edge error missed a point')
                rr,kk,_,_=profile(piece,Vmp)[0];qq=profile(piece,Vmp)[1]
                rp=mp.diff(lambda at:profile(piece,at)[0][0],Vmp)
                rpp=mp.diff(lambda at:profile(piece,at)[0][0],Vmp,2)
                kp=mp.diff(lambda at:profile(piece,at)[0][1],Vmp)
                theta=profile(piece,Vmp)[0][2]+1j*profile(piece,Vmp)[0][3]
                require(abs(rpp+abs(theta)**2/rr)<mp.mpf('1e-60'),'Raychaudhuri normalization')
                require(abs(rr*kp-kk*rp+kk*kk*(1-qq*qq/(rr*rr)))<mp.mpf('1e-60'),'kappa normalization')
                qp=mp.diff(lambda at:profile(piece,at)[1],Vmp)
                phi=profile(piece,Vmp)[2]
                require(abs(qp-e*rr*mp.im(phi*mp.conj(theta)))<mp.mpf('1e-60'),'Gauss sign and scale')
                identities+=3
    for piece,knot in [(0,v1),(1,v2)]:
        V=cap+S*knot
        for k in (0,1):
            for order in (0,1):
                l=mp.diff(lambda at:profile(piece,at)[0][k],V,order)
                r=mp.diff(lambda at:profile(piece+1,at)[0][k],V,order)
                require(abs(l-r)<mp.mpf('1e-60'),'geometric junction mismatch')
        require(abs(profile(piece,V)[1]-profile(piece+1,V)[1])<mp.mpf('1e-60'),'charge junction mismatch')
        require(abs(profile(piece,V)[2]-profile(piece+1,V)[2])<mp.mpf('1e-60'),'scalar junction mismatch')
    result=dict(status='PASS',high_precision_jet_comparisons=comparisons,
                defining_constraint_comparisons=identities,precision_digits=80,
                junctions_checked=2,complete_rectangle_certified=False,
                scope='independent finite high-precision audit; continuum coverage is the rational Taylor proof',
                actual_smooth_seed_certified=False,goal_A_proved=False)
    names=['verify_frozen_charged_boundary.py','frozen_charged_boundary.py',SPEC,source]
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'FROZEN_CHARGED_BOUNDARY_AUDIT_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
