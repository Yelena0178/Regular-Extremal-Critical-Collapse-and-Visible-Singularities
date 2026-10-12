"""Exact rational identities, integer Bernstein positivity, fixed-point K proof."""
from fractions import Fraction as F
from math import lcm,comb,factorial,ceil
from pathlib import Path
import json,time,sys
from interval_core import I,B,scpoint,exppoint
from high_precision import rationalize,audit
ROOT=Path(__file__).resolve().parents[1]
def add(a,b):
 c=[0]*max(len(a),len(b))
 for i,v in enumerate(a):c[i]+=v
 for i,v in enumerate(b):c[i]+=v
 return c

def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,v in enumerate(a):
  for j,u in enumerate(b):c[i+j]+=v*u
 return c

def der(a):return [i*v for i,v in enumerate(a)][1:]
def scale(a,k):return [v*k for v in a]
def divh2(a):
 a=a.copy();q=[0]*(max(0,len(a)-2))
 for j in range(len(a)-1,1,-1):
  v=a[j];q[j-2]=v;a[j]-=v;a[j-1]+=2*v;a[j-2]-=v
 assert all(v==0 for v in a)
 return q

def prepare(r):
 N=r['N'];w=F(r['w']);a,b=[[F(q) for q in r[k]] for k in ['a','b']];den=lcm(*(q.denominator for q in a+b));aa=[int(q*den) for q in a];bb=[int(q*den) for q in b]
 Ts=[[1],[0,1]];Us=[[1],[0,2]]
 for j in range(2,N+1):
  Ts.append(add([0]+scale(Ts[-1],2),scale(Ts[-2],-1)));Us.append(add([0]+scale(Us[-1],2),scale(Us[-2],-1)))
 X=[-sum(aa)];Y=[0]
 for j in range(1,N+1):X=add(X,scale(Ts[j],aa[j-1]));Y=add(Y,scale(Us[j-1],bb[j-1]))
 p,q=divh2(X),divh2(Y)
 poly=add([0]+mul(p,q),mul([1,0,-1],add(mul(q,der(p)),scale(mul(p,der(q)),-1))))
 while poly[-1]==0:poly.pop()
 # Laurent coefficients 2*den*c_n are integers; coefficients of z have real values.
 cc={0:-2*sum(aa)}
 for j in range(1,N+1):cc[j]=aa[j-1]+bb[j-1];cc[-j]=aa[j-1]-bb[j-1]
 e=[0]*(2*N+1);c=e.copy()
 for n,u in cc.items():
  for m,v in cc.items():e[abs(n-m)]+=n*m*u*v;c[abs(n-m)]+=n*u*v
 e=[F(v,4*den*den) for v in e];c=[F(v,4*den*den) for v in c];L=2*e[0]/c[0];lam=L*w
 D=w*w*sum(e[j]/(1+j*j*w*w) for j in range(2*N+1));S=[2*w*(L*c[j]-e[j])/(j*(1+j*j*w*w)) for j in range(1,2*N+1)];T=[2*L*w*w*c[j]/(1+j*j*w*w) for j in range(1,2*N+1)]
 K0=4*w*w*e[0]-D+sum(T);CL=w*sum(c[j]/(1+j*j*w*w) for j in range(2*N+1))
 return dict(poly=poly,den=den,e=e,c=c,L=L,lam=lam,D=D,S=S,T=T,K0=K0,CL=CL,w=w)

def bernstein(poly,den):
 n=len(poly)-1;coef=[sum(poly[k]*comb(k,i)*(-1)**(k-i)*2**i for k in range(i,n+1)) for i in range(n+1)]
 unit=lcm(*(comb(n,i) for i in range(n+1)));b=[sum(coef[i]*comb(j,i)*(unit//comb(n,i)) for i in range(j+1)) for j in range(n+1)]
 todo=[('',b)];leaves=[];st=time.time()
 while todo:
  path,b=todo.pop()
  if min(b)>0:
   lower=F(min(b),den*den*unit*2**(n*len(path)));leaves.append(dict(path=path,lower=str(lower)));continue
  if max(b)<=0:raise RuntimeError(('negative current cell',path))
  if len(path)>65:raise RuntimeError(('unresolved current cell',path))
  row=b.copy();left=[row[0]*2**n];right=[row[-1]*2**n]
  for level in range(1,n+1):
   row=[row[j]+row[j+1] for j in range(len(row)-1)];left.append(row[0]*2**(n-level));right.append(row[-1]*2**(n-level))
  todo.extend([(path+'1',right[::-1]),(path+'0',left)])
 low=min(F(v['lower']) for v in leaves)
 print('CURRENT PASS',len(leaves),'lower',float(low),'seconds',time.time()-st,flush=True)
 return dict(degree=n,leaves=leaves,lower=str(low),method='exact integer Bernstein/de Casteljau on u in [-1,1]')

def kcert(d):
 w=d['w'];slope=2*w*w*d['e'][0];D=I(d['D']);S=list(map(I,d['S']));T=list(map(I,d['T']));order=16;J=len(S)
 nus=[w*j for j in range(1,J+1)];powers=[[I(nu**k) for nu in nus] for k in range(order+2)]
 globalsup=abs(d['D'])+sum((abs(ss)+abs(tt))*nu**(order+1) for ss,tt,nu in zip(d['S'],d['T'],nus))
 tailX=F(max(1,ceil((abs(d['D'])+sum(map(abs,d['S']))+sum(map(abs,d['T'])))/slope-2)))+1
 tail_lower=slope*(tailX+2)-abs(d['D'])-sum(map(abs,d['S']))-sum(map(abs,d['T']))
 assert tail_lower>0 and d['K0']>0
 def jets(x):
  sn,cs=scpoint((w*x).numerator,(w*x).denominator);slist=[];clist=[];s0=I(0);c0=I(1)
  for j in range(J):s0,c0=s0*cs+c0*sn,c0*cs-s0*sn;slist.append(s0);clist.append(c0)
  ex=exppoint(x.numerator,x.denominator);arr=[]
  for k in range(order+1):
   val=I(slope*(x+2)) if k==0 else (I(slope) if k==1 else I(0))
   val-=(-1)**k*D*ex
   for j in range(J):
    ss,cc=slist[j],clist[j]
    if k%4==1:ss,cc=cc,-ss
    elif k%4==2:ss,cc=-ss,-cc
    elif k%4==3:ss,cc=-cc,ss
    val+=powers[k][j]*(S[j]*ss+T[j]*cc)
   arr.append(val)
  return arr
 todo=[(F(0),tailX,0)];leaves=[];st=time.time();count=0
 while todo:
  lo,hi,dep=todo.pop();mid=(lo+hi)/2;rad=(hi-lo)/2;v=jets(mid);bound=I(0)
  for k in range(1,order+1):bound+=v[k].abs()*I(rad**k/F(factorial(k)))
  bound+=I(globalsup*rad**(order+1)/factorial(order+1));lower=F(v[0].l-bound.h,B)
  if lower>0:leaves.append([str(lo),str(hi),str(lower)])
  else:
   if v[0].h<0:raise RuntimeError(('K negative',str(mid),str(F(v[0].h,B))))
   if dep>65:raise RuntimeError(('unresolved K',str(lo),str(hi)))
   todo.extend([(mid,hi,dep+1),(lo,mid,dep+1)])
  count+=1
  if count%200==0:print('K cells',count,'leaves',len(leaves),'elapsed',round(time.time()-st,2),flush=True)
 print('K PASS',len(leaves),'tail',float(tailX),'seconds',time.time()-st,flush=True)
 return dict(scale_bits=200,taylor_order=order,tail_start=str(tailX),tail_lower=str(tail_lower),K0_exact=str(d['K0']),compact_lower=str(min(F(l[2]) for l in leaves)),cells=leaves)
if __name__=='__main__':
 source=json.load(open(ROOT/('data/continuation.json' if '--best' in sys.argv else 'data/search.json')));ww=float(sys.argv[1]) if len(sys.argv)>1 else .06;d=next(v for v in source if v['w']==ww);r=rationalize(d);name=('best_' if '--best' in sys.argv else '')+'w'+str(ww).replace('.','_');(ROOT/f'data/{name}_rational.json').write_text(json.dumps(r,indent=2));prep=prepare(r)
 print('CANDIDATE',ww,float(prep['lam']),'K0 exact sign',prep['K0']>0,'K0',float(prep['K0']),flush=True)
 out=dict(input=name+'_rational.json',objective_exact=str(prep['lam']),objective=float(prep['lam']),linear_conditions='exact via rationalize plus divh2',current=bernstein(prep['poly'],prep['den']))
 (ROOT/f'data/{name}_partial_certificate.json').write_text(json.dumps(out,indent=2));out['K']=kcert(prep);(ROOT/f'data/{name}_certificate.json').write_text(json.dumps(out,indent=2));print('ALL LEADING ORDER CHECKS PASS',flush=True)
