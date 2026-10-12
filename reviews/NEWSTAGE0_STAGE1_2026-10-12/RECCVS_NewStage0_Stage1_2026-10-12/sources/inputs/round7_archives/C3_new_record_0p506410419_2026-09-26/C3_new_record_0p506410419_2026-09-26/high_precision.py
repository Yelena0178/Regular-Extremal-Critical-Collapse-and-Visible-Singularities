import numpy as np,json
from decimal import Decimal,getcontext
getcontext().prec=90
class mp:
 mpf=Decimal
 @staticmethod
 def nstr(v,n):return format(v,".50g")
from pathlib import Path
from fractions import Fraction as F
from scipy.linalg import qr

ROOT=Path(__file__).resolve().parents[1]

def rationalize(d):
 N=d['N'];w=F(str(d['w']));j=np.arange(1,N+1.)
 a=[F(round(x*10**16),10**16) for x in d['a']];b=[F(round(x*10**16),10**16) for x in d['b']]
 A=[[F(k*k) for k in range(1,N+1)]]+[[(-k*k*w*w/(s*(s*s+k*k*w*w))) for k in range(1,N+1)] for s in [1,2,3]]
 B=[[F(k) for k in range(1,N+1)],[F(k**3) for k in range(1,N+1)]]+[[k*w/(s*s+k*k*w*w) for k in range(1,N+1)] for s in [1,2,3]]
 deps=[]
 for M,c in [(A,a),(B,b)]:
  Mm=np.array([[float(v) for v in row] for row in M])/j;Mm/=np.linalg.norm(Mm,axis=1)[:,None]
  _,_,piv=qr(Mm,pivoting=True);dep=sorted(piv[:len(M)].tolist());deps.append(dep)
  right=[-sum(row[k]*c[k] for k in range(N) if k not in dep) for row in M]
  aug=[[row[k] for k in dep]+[rhs] for row,rhs in zip(M,right)]
  for i in range(len(M)):
   q=next(j for j in range(i,len(M)) if aug[j][i]);aug[i],aug[q]=aug[q],aug[i]
   fac=aug[i][i];aug[i]=[v/fac for v in aug[i]]
   for j in range(len(M)):
    if j!=i:
     fac=aug[j][i];aug[j]=[v-fac*u for v,u in zip(aug[j],aug[i])]
  for k,row in zip(dep,aug):c[k]=row[-1]
  assert all(sum(x*y for x,y in zip(row,c))==0 for row in M)
 return dict(N=N,w=str(w),a=list(map(str,a)),b=list(map(str,b)),dependent_columns=deps,source_label=d['label'],normalization='E0 near 1, exact value recoverable from coefficients',nine_linear_equalities_exact=True)

def mpnum(q):
 q=F(str(q));return mp.mpf(q.numerator)/q.denominator

def audit(d):
 N=d['N'];a=list(map(mpnum,d['a']));b=list(map(mpnum,d['b']));w=mpnum(d['w']);
 lap=[1/(1+(w*k)**2) for k in range(2*N+1)];EL=mp.mpf(0);CL=mp.mpf(0)
 for i in range(1,N+1):
  for j in range(1,N+1):
   cc=(lap[abs(i-j)]+lap[i+j])/2;ss=(lap[abs(i-j)]-lap[i+j])/2
   EL+=w*w*i*j*(a[i-1]*a[j-1]*ss+b[i-1]*b[j-1]*cc)
   CL+=w*a[i-1]*b[j-1]*(j*(cc-lap[j])+i*ss)
 E0=sum(j*j*(a[j-1]**2+b[j-1]**2) for j in range(1,N+1))/2;C0=sum(j*a[j-1]*b[j-1] for j in range(1,N+1));lam=2*w*E0/C0;K0=2*lam*CL-EL
 # Independent direct evaluation of endpoint factor for exact jets
 ep=16*sum(a[j-1]*j**4/24 for j in range(1,N+1))*sum(b[j-1]*j**5/120 for j in range(1,N+1))
 return {k:mp.nstr(v,50) for k,v in dict(E0=E0,C0=C0,e=lam,EL=EL,CL=CL,K0=K0,weighted_ratio=EL/(2*CL),defect=EL-CL,endpoint_cf=ep).items()}
if __name__=='__main__':
 repaired=json.load(open(ROOT/'data/positive_repaired.json'));(ROOT/'data/rational').mkdir(exist_ok=True)
 rats=[];aud=[]
 for d in repaired:
  rr=rationalize(d);rats.append(rr);(ROOT/f"data/rational/N{d['N']}.json").write_text(json.dumps(rr,indent=2));z=audit(rr);z.update(N=d['N'],w=d['w'],label='positive_repaired_rational');aud.append(z);print(d['N'],z['e'],z['K0'],flush=True)
 for d in json.load(open(ROOT/'data/zero_margin.json')):
  if d['label']=='zero_margin_frequency':
   z=audit(d);z.update(N=d['N'],w=d['w'],label=d['label']);aud.append(z);print('freq',d['w'],z['e'],z['K0'],z['weighted_ratio'],flush=True)
 (ROOT/'data/high_precision_audit.json').write_text(json.dumps(aud,indent=2))
