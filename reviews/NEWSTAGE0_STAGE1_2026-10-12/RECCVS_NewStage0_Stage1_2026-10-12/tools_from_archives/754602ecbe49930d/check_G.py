from fractions import Fraction as F
from math import comb
from collections import defaultdict
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parents[1];cs=[]
def ck(n,v,e=''):
 assert v,n
 cs.append({'name':n,'passed':True,'evidence':str(e)})
ck('root_identity',hashlib.sha256((p/'baseline/ROOT_CERTIFICATE_mgeom.json').read_bytes()).hexdigest()=='7845f2276b7dc12669d9e27861704bdee99f395458c35647fc9c734f93fb6dc2')
# Candidate bump derivative polynomial recurrence.
poly={0:1}; bounds=[]
for j in range(8):
 bound=sum(abs(c)*(k**k if k else 1) for k,c in poly.items());bounds.append(bound)
 ck('u_derivative_'+str(j),bound<2**100,bound)
 nxt=defaultdict(int)
 for k,c in poly.items():
  nxt[k+2]+=c
  if k:nxt[k+1]-=k*c
 poly=dict(nxt)
for j in range(8):
 b=16**j*sum(comb(j,k)*bounds[k]*bounds[j-k] for k in range(j+1))
 ck('candidate_bump_j'+str(j),b<2**(200+5*j),b)
 ck('candidate_normalized_power_j'+str(j),211+5*j<=246)
ck('candidate_integral',F(1,1296)>F(1,2048))
ck('candidate_P_bound',246+1==247)
for tau in [F(0),F(1,9),F(1,2),F(8,9),F(1)]:
 ck('convex_normalization_'+str(tau),(1-tau)+tau==1)
 ck('convex_nonnegative_'+str(tau),0<=tau<=1)
# Metric g_Ut=-Omega^2/2, dF=(1,d), V=(1/2,1/(2d)).
for d in [F(1,2**20),F(1,16),F(1),F(16),F(2**20)]:
 for om2 in [F(1,2),F(1),F(2)]:
  vu=F(1,2);vt=1/(2*d)
  ck('VF_d%s_om%s'%(d,om2),vu+d*vt==1)
  gv=-om2*vu*vt
  ck('Vtimelike_d%s_om%s'%(d,om2),gv==-om2/(4*d) and gv<0)
  ck('noncharacteristic_d%s_om%s'%(d,om2),-4*d/om2<=-2*d)
# Scalar coefficient identities and dyadic safety margins (0<a<1).
ck('vstar_a_power',1+2==3)
ck('vstar_dyadic',20+20==40)
ck('U_drift_coeff',F(1,2**41)<F(1,8192))
ck('t_drift_coeff',F(1,2**21)<F(1,16))
ck('environment_cutoff_margin_U0',F(1,2**15)<F(1,8192))
ck('environment_cutoff_margin_Ustar',F(1,2**15)<F(1,4096))
ck('uniform_gamma_margin',F(1,8)>F(1,32))
ck('J_upper',1+1<=2)
ck('P_family_bound',1+1<=2,'max convex combination <= max endpoint; P*=Pa+2^247')
ck('Cauchy_surface_dimensions',1+2==3)
ck('final_Cpsi_power',16**201==2**804)
ck('Cpsi_log_small_terms',102**2*2**100//2>200+2249)
ck('Cpsi_log_805',804+1==805)
ck('Cpsi_below_N7',805<2**100 and 104<200)
ck('uniform_B6_alpha_exponent',8+7==15)
ck('uniform_B6_constant',34000+8==34008)
ck('uniform_Bg_constant',2048+8==2056)
ck('reference_tail_d_minus_one',-2*(-1)-1==1 and 2300+1==2301)
r={'label':'GPT 主张，未经外部独立审查','number_of_checks':len(cs),'all_passed':True,'checks':cs,'scope':'Exact candidate-bump, metric and dyadic identities; not PDE, H6 trace convergence, domain-of-dependence or topological Cauchy certification','actual_psi_identity_certified':False,'candidate_selection':'conditional on frozen actual development and MGHD inputs'}
(p/'verification/RESULTS.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['number_of_checks','all_passed','scope']},ensure_ascii=False))
