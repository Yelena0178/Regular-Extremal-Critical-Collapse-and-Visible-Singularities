"""Independent implementation of VAR01 tangent; finite algebra controls only."""
from shape_probe import ROOT,SRC
from charged_lobatto import rhs
import numpy as np
import json,hashlib

def product(*pairs):
    return sum(d*np.prod([v for j,(v,_) in enumerate(pairs) if j!=i]) for i,(_,d) in enumerate(pairs))

def tangent(y,w):
    r,k,tr,ti,n,zr,zi,m,pr,pi,q,b=y
    R,K,Tr,Ti,N,Zr,Zi,H,Pr,Pi,Cq,B=w
    th,z,ph=complex(tr,ti),complex(zr,zi),complex(pr,pi)
    T,Z,P=complex(Tr,Ti),complex(Zr,Zi),complex(Pr,Pi)
    f=1-2*m/r;F=-2*H/r+2*m*R/r**2
    a=k*(2*m-q*q/r)/r**2
    C=K*(2*m-q*q/r)/r**2+k*(2*H-2*q*Cq/r+q*q*R/r**2)/r**2-2*a*R/r
    inv=(1/r,-R/r**2)
    Tu=-product((k,K),(n,N),(f,F),(z,Z),inv)-.6j*product((k,K),(n,N),(q,Cq),(ph,P),inv)-.6j*(B*th+b*T)
    Zv=-T/r+th*R/r**2-C*z-a*Z+.6j*product((k,K),(q,Cq),(ph,P),inv)
    Hv=product((q*q,2*q*Cq),(k,K),(f,F),(.5/r**2,-R/r**3))+np.real(T*np.conj(th))/k-abs(th)**2*K/(2*k*k)
    Pv=T/r-th*R/r**2
    return np.array([N,(K*n+k*N)*abs(z)**2/r+2*k*n*np.real(Z*np.conj(z))/r-k*n*abs(z)**2*R/r**2,Tu.real,Tu.imag,C*n+a*N,Zv.real,Zv.imag,Hv,Pv.real,Pv.imag,.6*R*np.imag(ph*np.conj(th))+.6*r*np.imag(P*np.conj(th)+ph*np.conj(T)),2*product((k,K),(n,N),(q,Cq),(1/r**2,-2*R/r**3))])

rng=np.random.default_rng(20261108)
errors=[];negative=[]
for i in range(24):
    y=rng.normal(size=12);y[0]=rng.uniform(1,5);y[1]=rng.uniform(.3,2);y[4]=-rng.uniform(.2,1)
    w=rng.normal(size=12);h=2e-5
    exact=tangent(y,w);difference=(rhs(y+h*w)-rhs(y-h*w))/(2*h)
    error=np.max(abs(difference-exact))/(1+np.max(abs(exact)))
    errors.append(float(error));assert error<2e-8
    wrong=exact.copy();wrong[10]=-wrong[10]
    negative.append(float(abs(wrong[10]-difference[10])))
assert max(negative)>1
paths=[__file__,str(SRC/'charged_lobatto.py'),str(ROOT/'proofs/VAR01_CONSTRAINT_AND_TRANSPORT.md')]
out=dict(passed=True,states=24,max_scaled_derivative_error=max(errors),wrong_Maxwell_sign_rejected=True,source_sha256={str(p):hashlib.sha256(open(p,'rb').read()).hexdigest() for p in paths},scope='finite rational-RHS derivative checks, no actual PDE solution or interval certificate',goal_A_proved=False)
dest=ROOT/'results/VAR01_TRANSPORT_CHECKS.json'
if dest.exists():raise FileExistsError(dest)
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
