from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'data/profile.json').read_text());a=list(map(F,r['a']));b=list(map(F,r['b']));w=F(r['w']);N=len(a)
z={0:-sum(a)}
for j in range(1,N+1):z[j]=(a[j-1]+b[j-1])/2;z[-j]=(a[j-1]-b[j-1])/2
v={j:j*w*x for j,x in z.items()}
E=[sum((v[j]*v.get(j-k,F(0)) for j in v),F(0))*(1 if k==0 else 2) for k in range(2*N+1)]
C=[sum((z[j]*(v.get(j+k,F(0))+v.get(j-k,F(0))) for j in z),F(0))/(2 if k==0 else 1) for k in range(2*N+1)]
lam=2*E[0]/C[0]
D=sum(E[k]/(1+(k*w)**2) for k in range(2*N+1))
S=[2*(lam*C[k]-E[k])/(k*w*(1+(k*w)**2)) for k in range(1,2*N+1)]
T=[2*lam*C[k]/(1+(k*w)**2) for k in range(1,2*N+1)]
def trim(p):
 while len(p)>1 and p[-1]==0:p.pop()
 return p
def add(p,q):
 out=[F(0)]*max(len(p),len(q))
 for i,x in enumerate(p):out[i]+=x
 for i,x in enumerate(q):out[i]+=x
 return trim(out)
def scale(p,s):return trim([s*x for x in p])
def mul(p,q):
 out=[F(0)]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q):out[i+j]+=x*y
 return trim(out)
def diff(p):return [i*x for i,x in enumerate(p)][1:] or [F(0)]
def div(p,q):
 p=p[:];out=[F(0)]*max(1,len(p)-len(q)+1)
 while len(p)>=len(q) and any(p):
  n=len(p)-len(q);c=p[-1]/q[-1];out[n]=c
  for j,x in enumerate(q):p[n+j]-=c*x
  trim(p)
 assert not any(p)
 return trim(out)
def bern(p,l=F(-1),h=F(1)):
 n=len(p)-1
 pp=[sum((p[j]*comb(j,k)*l**(j-k)*(h-l)**k for j in range(k,n+1)),F(0)) for k in range(n+1)]
 return [sum((pp[k]*F(comb(i,k),comb(n,k)) for k in range(i+1)),F(0)) for i in range(n+1)]
def split(bb):
 rows=[bb];left=[bb[0]];right=[bb[-1]]
 while len(rows[-1])>1:
  row=[(x+y)/2 for x,y in zip(rows[-1],rows[-1][1:])];rows.append(row);left.append(row[0]);right.append(row[-1])
 return left,right[::-1]
def inverse(A):
 n=len(A);B=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
 for i in range(n):
  k=next(k for k in range(i,n) if B[k][i]);B[i],B[k]=B[k],B[i];s=B[i][i];B[i]=[x/s for x in B[i]]
  for j in range(n):
   if j!=i:
    s=B[j][i];B[j]=[x-s*y for x,y in zip(B[j],B[i])]
 return [row[n:] for row in B]
if __name__=='__main__':
 print('lambda',float(lam),'K0',float(4*E[0]-D+sum(T)))
 print('tail L1 bound at20',float(44*E[0]-abs(D)-sum(map(abs,S))-sum(map(abs,T))))
