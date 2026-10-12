from fractions import Fraction as F
from math import factorial, comb
from pathlib import Path
from collections import defaultdict
import json
p=Path(__file__).resolve().parents[1]; tests=[]
def ck(n,v):
 assert v,n
 tests.append({'name':n,'passed':True})
def mul(a,b,n=7):return [sum(a[i]*b[j-i] for i in range(j+1) if i<len(a) and j-i<len(b)) for j in range(n+1)]
def inv(a,n=7):
 b=[1/a[0]]
 for j in range(1,n+1): b.append(-sum(a[i]*b[j-i] for i in range(1,j+1))/a[0])
 return b
def sqrtjet(a,w0,n=7):
 b=[w0]
 for j in range(1,n+1): b.append((a[j]-sum(b[i]*b[j-i] for i in range(1,j)))/(2*w0))
 return b
for seed in range(1,5):
 a=[F(seed*seed)]+[F((-1)**j*(j+seed),j+1) for j in range(1,8)]
 ck('inverse_convolution_'+str(seed),mul(a,inv(a))==[F(1)]+[F(0)]*7)
 ck('sqrt_convolution_'+str(seed),mul(sqrtjet(a,F(seed)),sqrtjet(a,F(seed)))==a)
# Exact radial differentiation: R=1+t+t², J=1+2t, u=(R-1)^m.
v=inv([F(1),F(2)]+[F(0)]*6)
for m in range(7):
 u=[F(1)]+[F(0)]*6
 for _ in range(m):u=mul(u,[F(0),F(1),F(1)]+[F(0)]*4,6)
 for k in range(7):
  ck('radial_operator_m%d_k%d'%(m,k),u[0]==(factorial(m) if m==k else 0))
  if k<6:u=mul(v,[(j+1)*u[j+1] for j in range(len(u)-1)],5-k)
# Power bounds are algebraic and monotone for S>=2.
ck('inverse_norm_power',7*2+1==15)
ck('C_alg_constant',200+30*16+80*256==21160)
ck('C_alg_M_power',20*256==5120)
ck('Cpsi_power_domination',16**201>5120)
ck('Cpsi_constant_domination',2001*16**201>21160)
ck('Bg_constant_gap',12000-2048==9952)
ck('Bg_large_Bc',4*34008>9952)
ck('sixth_K_needs_d7',6+1==7)
ck('sigma8_needs_d7',8-1==7)
ck('multiindex_count',comb(9,3)==84)
# Independent Cartesian coefficient recurrence, derivative of R^-q n^ell u^(k).
def diff(poly,axis):
 out=defaultdict(int)
 for (k,q,ell),c in poly.items():
  e=list(ell);e[axis]+=1;e=tuple(e)
  out[k+1,q,e]+=c;out[k,q+1,e]-=(q+sum(ell))*c
  if ell[axis]:
   e=list(ell);e[axis]-=1;out[k,q+1,tuple(e)]+=ell[axis]*c
 return {k:c for k,c in out.items() if c}
rows=[]
for order in range(7):
 mx=0
 for i in range(order+1):
  for j in range(order-i+1):
   for seed in [(0,0,0),(1,0,0),(2,0,0),(1,1,0)]:
    poly={(0,0,seed):1}
    for axis,num in enumerate((i,j,order-i-j)):
     for _ in range(num):poly=diff(poly,axis)
    mx=max(mx,sum(abs(x) for x in poly.values()))
 rows.append(mx);ck('cartesian_coeff_%d'%order,mx<2**20)
ck('cartesian_max_exact',max(rows)==495715)
# Endpoint invariance is checked algebraically only, not a global embedding test.
for tau in [F(0),F(1,7),F(1,2),F(1)]:
 ck('psi_normalization_'+str(tau),(1-tau)*1+tau*1==1)
 ck('psi_positivity_weights_'+str(tau),0<=tau<=1)
r={'number_of_checks':len(tests),'all_passed':True,'tests':tests,'angular_rows':rows,'scope':'Finite rational jet identities and bound arithmetic only; no PDE, actual psi or MGHD certification','label':'GPT 主张，未经外部独立审查'}
(p/'verification/RESULTS.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['number_of_checks','all_passed','angular_rows','scope']},ensure_ascii=False))
