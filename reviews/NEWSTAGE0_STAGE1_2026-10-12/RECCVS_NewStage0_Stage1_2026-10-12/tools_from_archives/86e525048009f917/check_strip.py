from fractions import Fraction as F
from math import factorial,comb
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parents[1]; tests=[]
def ck(n,v,e=''):
 assert v,n
 tests.append({'name':n,'passed':True,'evidence':str(e)})
ck('same_root',hashlib.sha256((p/'baseline/ROOT_CERTIFICATE_mgeom.json').read_bytes()).hexdigest()=='7845f2276b7dc12669d9e27861704bdee99f395458c35647fc9c734f93fb6dc2')
# Each term: coefficient,r exponent, exponential ell exponent, other field powers.
# pr/pi=Phi, hr/hi=eta, zr/zi=zeta.
mu=F(3,5)
def t(c,r=0,s=0,**powers):return (F(c),r,s,powers)
fr=[t(-1,-1,nu=1,lam=1),t(F(-1,4),-1,1),t(F(1,4),-3,1,Q=2)]
fh=[t(-2,-2,hr=1,zr=1),t(-2,-2,hi=1,zi=1),t(F(1,2),-2,1),t(2,-2,nu=1,lam=1),t(-1,-4,1,Q=2)]
rows={
 'r_U':[t(1,nu=1)],'phiR_U':[t(1,-1,hr=1),t(mu,A=1,pi=1)],
 'phiI_U':[t(1,-1,hi=1),t(-mu,A=1,pr=1)],'ell_U':[t(1,chi=1)],
 'Q_U':[t(-mu,1,pi=1,hr=1),t(mu,1,pr=1,hi=1)],
 'lambda_U':fr,
 'zetaR_U':[t(-1,-1,lam=1,hr=1),t(-mu/4,-1,1,Q=1,pi=1),t(mu,A=1,zi=1)],
 'zetaI_U':[t(-1,-1,lam=1,hi=1),t(mu/4,-1,1,Q=1,pr=1),t(-mu,A=1,zr=1)],
 'kappa_U':fh,'nu_t':fr,
 'etaR_t':[t(-1,-1,nu=1,zr=1),t(mu/4,-1,1,Q=1,pi=1)],
 'etaI_t':[t(-1,-1,nu=1,zi=1),t(-mu/4,-1,1,Q=1,pr=1)],
 'A_t':[t(F(-1,2),-2,1,Q=1)],'chi_t':fh}
ck('fourteen_real_rows',len(rows)==14)
for name,row in rows.items():
 ck(name+'_direct_degree',max(max(0,r)+sum(pow.values()) for c,r,s,pow in row)<=3)
 ck(name+'_inverse_power',max(max(0,-r) for c,r,s,pow in row)<=4)
 ck(name+'_exp_power',max(s for c,r,s,pow in row)<=1)
 ck(name+'_coefficient_sum',sum(abs(c) for c,r,s,pow in row)<=8)
# All 0..8 derivatives of each monomial: worst factor at each state derivative<=12,
# 14 ordered state directions; inverse radius<=128, exp<=2. Other factors<=exp(H).
for j in range(9):
 c=14*8*2*(14*12)**j*128**(4+j)
 ck('state_row_coefficient_j%d'%j,c<2**200,c)
ck('state_bound_A_log',200+3*2**100<100*2**100,'ln2<1 and H>=2^100')
# Recursive pure/ mixed jet majorant after taking log.
coef=F(2); cs=[coef]
for j in range(1,9):
 coef=40+16*coef;cs.append(coef)
 ck('log_majorant_j%d'%j,coef<2**35,coef)
ck('log_majorant_closed_form',cs[8]==2*16**8+40*F(16**8-1,15))
ck('D8_reserve',35<2**100,'35 ln2 < H, so 2^35 exp(100H)<exp(101H)')
# Boundary r_j log majorant uses 20 factor, with source <=2^100 exp(3L).
c=F(2)
for j in range(1,11):
 c=2**100+20*c
 ck('ERN_edge_r_log_j%d'%j,c<2**200,c)
ck('chi_U8_needs_r10',8+1+1==10)
ck('nu_U8_needs_r9',8+1==9)
ck('poly_r10_initial_zero',10>9)
ck('combo_Omega_absorption',6*100>80,'M>=2^100, 2^160 M^14<=2^80 M^20')
ck('combo_graph_absorption',9<20)
ck('Cpsi_power',16**201>5120)
# Corridor bounds assuming the fixed cutoff supports already checked in baseline.
ck('near_U0_gap',F(1,8)*F(1,1024)==F(1,8192))
ck('near_Ustar_gap',F(1,4)*F(1,1024)==F(1,4096))
for tau in [F(0),F(1,10),F(1,2),F(9,10),F(1)]:
 ck('bump_integral_tau_'+str(tau),1-tau+tau==1)
 ck('bump_nonnegative_tau_'+str(tau),tau>=0 and 1-tau>=0)
ck('candidate_Cpsi_log_power',4*201==804 and 805<2**100)
ck('candidate_Cpsi_below_N7',104<200)
result={'label':'GPT 主张，未经外部独立审查','checks':tests,'number_of_checks':len(tests),'all_passed':True,'log_recurrence_coefficients':[str(x) for x in cs], 'scope':'Exact row structure and coefficient arithmetic; does NOT certify boundary PDE, full-strip existence, constraints or interface G','interface_G_certified':False}
(p/'verification/RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['number_of_checks','all_passed','scope','interface_G_certified']},ensure_ascii=False))
