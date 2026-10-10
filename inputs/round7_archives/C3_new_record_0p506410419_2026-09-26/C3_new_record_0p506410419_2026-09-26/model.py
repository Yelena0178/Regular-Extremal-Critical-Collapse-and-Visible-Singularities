"""Independent leading-order Fourier model; all floating diagnostics are [N]."""
import numpy as np
from scipy.linalg import null_space
from numpy.polynomial import chebyshev as ch

def rows(N,w,mode='full'):
 j=np.arange(1,N+1.)
 a=[];b=[]
 if mode not in ['no_endpoint','c0']:
  a.append(j);b.extend([np.ones(N),j*j]) # u=j*a,v=j*b
 if mode not in ['no_moments','c0']:
  for s in [1,2,3]:
   a.append(-j*w*w/(s*(s*s+(j*w)**2)))
   b.append(w/(s*s+(j*w)**2))
 A=np.array(a).reshape(-1,N);B=np.array(b).reshape(-1,N)
 return A,B

def basis(N,w,mode='full'):
 A,B=rows(N,w,mode)
 def ns(M):return np.eye(N) if not len(M) else null_space(M/np.linalg.norm(M,axis=1)[:,None],rcond=1e-12)
 U,V=ns(A),ns(B)
 P=np.zeros((2*N,U.shape[1]+V.shape[1]));P[:N,:U.shape[1]]=U;P[N:,U.shape[1]:]=V
 return P

def eval_z(a,b,t):
 j=np.arange(1,len(a)+1.);co=np.cos(np.outer(t,j));si=np.sin(np.outer(t,j))
 return (co-1)@a,si@b,-si@(j*a),co@(j*b)

def fourier(a,b):
 N=len(a);nt=1<<int(np.ceil(np.log2(4*N+1)));t=2*np.pi*np.arange(nt)/nt
 X,Y,Xp,Yp=eval_z(a,b,t)
 E=np.fft.rfft(Xp*Xp+Yp*Yp).real[:2*N+1]*2/nt
 C=np.fft.rfft(X*Yp-Y*Xp).real[:2*N+1]*2/nt
 E[0]/=2;C[0]/=2
 return E,C

def kval(a,b,w,x,deriv=0):
 E,C=fourier(a,b);L=2*E[0]/C[0];j=np.arange(1,len(E));nu=w*j
 D=w*w*np.sum(E/(1+(w*np.arange(len(E)))**2))
 S=2*w*(L*C[1:]-E[1:])/(j*(1+nu*nu));T=2*L*w*w*C[1:]/(1+nu*nu)
 xx=np.asarray(x);ss=np.sin(np.outer(xx,nu));cc=np.cos(np.outer(xx,nu))
 if deriv==1:return 2*w*w*E[0]+D*np.exp(-xx)+cc@(nu*S)-ss@(nu*T)
 if deriv==2:return -D*np.exp(-xx)-ss@(nu*nu*S)-cc@(nu*nu*T)
 return 2*w*w*E[0]*(xx+2)-D*np.exp(-xx)+ss@S+cc@T

def factor_maps(N):
 h2=np.array([1.5,-2.,.5]);pa=[];qb=[]
 U0=np.array([1.]);U1=np.array([0.,2.]);us=[U0,U1]
 for n in range(2,N):us.append(ch.chebsub(ch.chebmul([0,2],us[-1]),us[-2]))
 for j in range(1,N+1):
  f=np.zeros(j+1);f[0]=-1/j;f[j]=1/j
  p,_=ch.chebdiv(f,h2);q,_=ch.chebdiv(us[j-1]/j,h2)
  pa.append(np.pad(p,(0,N-len(p))));qb.append(np.pad(q,(0,N-len(q))))
 return np.array(pa).T,np.array(qb).T

def factor(a,b,t):
 N=len(a);j=np.arange(1,N+1);P,Q=factor_maps(N);p=P@(j*a);q=Q@(j*b);u=np.cos(t)
 pv=ch.chebval(u,p);qv=ch.chebval(u,q)
 return u*pv*qv+(1-u*u)*(qv*ch.chebval(u,ch.chebder(p))-pv*ch.chebval(u,ch.chebder(q)))

class Problem:
 def __init__(self,N,w,mode='full',drop_k=False,drop_current=False,ngrid=500,thgrid=None,k_margin=1e-9,c_margin=1e-8):
  self.N=N;self.w=w;self.mode=mode;self.k_margin=k_margin;self.c_margin=c_margin;self.P=basis(N,w,mode);self.j=np.arange(1,N+1.)
  self.nt=1<<int(np.ceil(np.log2(4*N+1)));t=2*np.pi*np.arange(self.nt)/self.nt
  co=np.cos(np.outer(t,self.j));si=np.sin(np.outer(t,self.j));Z=np.zeros_like(co)
  self.X=np.c_[(co-1)/self.j,Z]@self.P;self.Y=np.c_[Z,si/self.j]@self.P
  self.Xp=np.c_[-si,Z]@self.P;self.Yp=np.c_[Z,co]@self.P
  x=np.unique(np.r_[np.linspace(0,4,90),np.linspace(4,25,180),np.linspace(25,130,180)])
  self.x=x;nu=w*np.arange(1,2*N+1);jj=np.arange(1,2*N+1)
  self.KE=np.c_[w*w*(2*(x+2)-np.exp(-x)), -w*w*np.exp(-x[:,None])/(1+nu**2)-2*w*np.sin(np.outer(x,nu))/(jj*(1+nu**2))]
  self.KC=np.c_[np.zeros(len(x)),2*w*np.sin(np.outer(x,nu))/(jj*(1+nu**2))+2*w*w*np.cos(np.outer(x,nu))/(1+nu**2)]
  self.drop_k=drop_k;self.drop_current=drop_current
  ts=np.linspace(0,np.pi,ngrid) if thgrid is None else thgrid
  self.factored=mode not in ['no_endpoint','c0']
  if self.factored:
   p,q=factor_maps(N);u=np.cos(ts);V=ch.chebvander(u,N-1)
   pd=np.column_stack([ch.chebval(u,ch.chebder(p[:,i])) for i in range(N)])
   qd=np.column_stack([ch.chebval(u,ch.chebder(q[:,i])) for i in range(N)])
   self.p=np.c_[V@p,np.zeros((len(ts),N))]@self.P
   self.q=np.c_[np.zeros((len(ts),N)),V@q]@self.P
   self.pd=np.c_[pd,np.zeros((len(ts),N))]@self.P
   self.qd=np.c_[np.zeros((len(ts),N)),qd]@self.P
   self.u=u
  else:
   pp=[];qq=[];us=[np.array([1.]),np.array([0.,2.])]
   for n in range(2,N):us.append(ch.chebsub(ch.chebmul([0,2],us[-1]),us[-2]))
   for j in range(1,N+1):
    f=np.zeros(j+1);f[0]=-1/j;f[j]=1/j
    p,_=ch.chebdiv(f,[1.,-1.]);q=us[j-1]/j
    pp.append(np.pad(p,(0,N-len(p))));qq.append(np.pad(q,(0,N-len(q))))
   p,q=np.array(pp).T,np.array(qq).T;u=np.cos(ts);V=ch.chebvander(u,N-1)
   pd=np.column_stack([ch.chebval(u,ch.chebder(p[:,i])) for i in range(N)])
   qd=np.column_stack([ch.chebval(u,ch.chebder(q[:,i])) for i in range(N)])
   self.p=np.c_[V@p,np.zeros((len(ts),N))]@self.P
   self.q=np.c_[np.zeros((len(ts),N)),V@q]@self.P
   self.pd=np.c_[pd,np.zeros((len(ts),N))]@self.P
   self.qd=np.c_[np.zeros((len(ts),N)),qd]@self.P
   self.u=u
  self.cache=None
 def calc(self,p):
  if self.cache is not None and np.array_equal(p,self.cache[0]):return self.cache[1]
  X,Y,Xp,Yp=[M@p for M in [self.X,self.Y,self.Xp,self.Yp]]
  Earr=Xp*Xp+Yp*Yp;Carr=X*Yp-Y*Xp
  dEarr=2*(Xp[:,None]*self.Xp+Yp[:,None]*self.Yp)
  dCarr=Yp[:,None]*self.X+X[:,None]*self.Yp-Xp[:,None]*self.Y-Y[:,None]*self.Xp
  def fft(v):
   r=np.fft.rfft(v,axis=0).real[:2*self.N+1]*2/self.nt;r[0]/=2;return r
  E,C,dE,dC=map(fft,[Earr,Carr,dEarr,dCarr]);L=2*E[0]/C[0];dL=2*dE[0]/C[0]-L*dC[0]/C[0]
  K=self.KE@E+L*(self.KC@C);dK=self.KE@dE+L*(self.KC@dC)+np.outer(self.KC@C,dL)
  pv,qv,pd,qd=[M@p for M in [self.p,self.q,self.pd,self.qd]];u=self.u;v=1-u*u
  hh=u if self.factored else -np.ones_like(u)
  cf=hh*pv*qv+v*(qv*pd-pv*qd)
  dcf=(hh*qv-v*qd)[:,None]*self.p+(hh*pv+v*pd)[:,None]*self.q+(v*qv)[:,None]*self.pd-(v*pv)[:,None]*self.qd
  # scale to avoid enormous endpoint factor derivatives
  cs=np.maximum(1.,np.linalg.norm(dcf,axis=1)); # variable scaling NOT used for derivatives: use fixed initialization below
  if not hasattr(self,'cscale'):self.cscale=cs
  cons=[np.array([C[0]-1e-4])];jac=[dC[0][None,:]]
  if not hasattr(self,'kscale'):self.kscale=np.maximum(1e-9,np.linalg.norm(dK,axis=1))
  if not self.drop_k:cons.append((K-self.k_margin)/self.kscale);jac.append(dK/self.kscale[:,None])
  if not self.drop_current:cons.append((cf-self.c_margin)/self.cscale);jac.append(dcf/self.cscale[:,None])
  out=(self.w*L,self.w*dL,np.concatenate(cons),np.vstack(jac),E,C)
  self.cache=(p.copy(),out);return out
 def unpack(self,p):
  v=self.P@p;v=v*np.sqrt(2/np.dot(v,v));return v[:self.N]/self.j,v[self.N:]/self.j
