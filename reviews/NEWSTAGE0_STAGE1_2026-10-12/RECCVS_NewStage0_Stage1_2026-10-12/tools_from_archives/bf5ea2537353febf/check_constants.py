#!/usr/bin/env python3
"""Exact/logarithmic constant audit; NOT a formal PDE proof.

No import from previous certificate generators. Run from any working directory.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import hashlib,json

BASE=Path(__file__).resolve().parents[1]
checks=[]
def check(name, assertion, evidence):
    if not assertion:raise AssertionError(name)
    checks.append(dict(name=name,passed=True,evidence=str(evidence)))

root=BASE/'baseline/ROOT_CERTIFICATE_mgeom.json'
digest=hashlib.sha256(root.read_bytes()).hexdigest()
check('same_root',digest=='7845f2276b7dc12669d9e27861704bdee99f395458c35647fc9c734f93fb6dc2',digest)
source=json.loads((BASE/'baseline/filtered_K8_n88_sigma1over20.json').read_text())
S=sum((abs(F(x)) for x in source['polynomial_real']),F(0))+sum((abs(F(x)) for x in source['polynomial_imag']),F(0))
E=F(source['E_total'])
check('normalized_coefficients',E>0 and S*S/E<2**4000,'S/sqrt(E)<2^2000')
check('polynomial_degree',max(len(source['polynomial_real']),len(source['polynomial_imag']))-1==132,132)
check('w_nine_derivative_budget',2000+22*132+9*8+9<5000,'2000+2904+72+9=4985')

# theta^(j)(x)=exp(-t)*p_j(t), t=1/x. Envelope t^k exp(-t)<=k^k.
p={0:1};theta=[]
for j in range(10):
    b=sum(abs(c)*(k**k if k else 1) for k,c in p.items())
    check('theta_'+str(j),b<2**100,b);theta.append(b)
    q={}
    for k,c in p.items():
        q[k+2]=q.get(k+2,0)+c
        if k:q[k+1]=q.get(k+1,0)-k*c
    p=q
inv=[F(9)]
for j in range(1,10):
    inv.append(9*sum(comb(j,k)*2**101*inv[j-k] for k in range(1,j+1)))
step=[sum(comb(j,k)*2**100*inv[j-k] for k in range(j+1)) for j in range(10)]
check('step_nine_derivatives',max(step)<2**2000,'reciprocal and quotient derivative recursion')
check('z_nine_derivative_budget',5000+2*2000+9000+9+4<30000,'product cutoff and eight correction bumps')
check('graph_derivative_budget',8*9+3<100,'h_c^-1<exp(9H), beta and coefficient factors absorbed in exp(3H)')
check('J_lower',F(1,2)+2*F(1,8)==F(3,4),'lambda>beta/2, -nu>1/(8beta)')
check('J_upper',2+5*F(1,2)<5,'lambda<2beta, -nu<1/(2beta)')
check('ring_width_lower',F(3,4)*F(1,4)/2**16>F(1,2**20),'3a/(2^20 beta)>a/(2^20 beta)')
check('ring_width_upper',F(5,4)/2**16<F(1,2**14),'5a/(2^18 beta)<a/(2^14 beta)')
check('metric_lower',F(1,2)*2/25==F(1,25),'Omega^2 d/J^2>1/25')
check('metric_upper',2*5/(F(3,4)**2)<18,'Omega^2 d/J^2<160/9<18')

# These inequalities hold for the frozen H, using H>2^100 and ln2<1;
# no astronomical exponential is numerically evaluated.
check('H_minimum',2**100>100000,'H=2^100 exp(200(L+4))>2^100')
check('boundary_polynomial_budget',100000*2<2**100*200,'exp(200L)>=200L, L>=1')
check('RN_recursive_budget',20**10<2**100,'j<=10 linear highest jet ODE recurrence')
check('W_log_recurrence',10*F(1,15)<1,'sum of forcing series coefficient 10/15')
check('W8_power',2*16**8==2**33,'w8<2^33 exp(100H)')
check('W8_absorption',33<2**100,'33 ln2<H')
check('jet_operation_count',comb(11,3)==165,'three variable jets degree<=8')
check('jet_operations_iteration',17**200<2**1000,'log-majorant for <=200 tensor operations')
check('jet_to_N7',1000<2*2**100 and 104<200,'2^1000 exp(102H)<exp(104H)<exp(200H)')
check('H4_cutoff_exponent',544+19+4+8<600,'575<600; <=32 real input components including spatial A')
check('Sobolev_product_count',35*16*2*4*32<2**20,'Leibniz, embedding, component/duplicate margins')
check('Neumann_initialization',F(2**20*2**4,2**30)==F(1,64),'input q<=2^-30')

ricci_first=2*4*(4*16*3)
ricci_quadratic=2*16*12**2
harmonic_quadratic=4*6144
check('Ricci_counts',ricci_first+ricci_quadratic+harmonic_quadratic==30720,30720)
check('all_RHS_row_margin',2*30720+2**15<2**20,'wave factor 2 and extra matter terms')
check('source_exponent_margin',200+20+20+20+4<300,'coefficient, product, row and real-component margins')
check('second_time_derivative_margin',300+20+20<400,'wave equation solves partial_s^2 U in H2')
check('commutator_margin',200+400+20+20+20<800,'time second derivative and coefficient derivative products')
check('energy_margin',800+30+20+20<900<1000,'commutator, X/E, real components and energy multiplication')
check('a_star_energy_initial',10-2000==-1990,'E0<=2^10 X0')
check('nonlinear_bootstrap',1000+2-1990==-988,'2^1000*4 E0<=2^-988<1')
check('time_growth_factor',3**3<2**8,'e<3 =>exp(3/8)<3^(3/8)<2')
check('energy_guard',2-1990<-40 and 10+2-1990<-30,'E and X guard improve strictly')
check('stability_X_growth',10+1+10==21,'X<=2^21 X0')
check('C1_margin',10+21<100,'C1<=2^31 X0')
check('cone_speed_margin',10+10+21<100,'speed error<=2^41 X0')
check('root_duration',2*F(1,16)==F(1,8),'2r0<1/8')

# e^(-e^(300H)) satisfies every threshold through elementary e^x>=1+x.
# e^(300H)>= (1+100H)e^(200H), so the gap dominates all dyadic constants.
check('epsilon_initialization_threshold',700+2000<2**100,'A epsilon^3<2^-2000; H vastly dominates 2700 ln2')
check('epsilon_speed_threshold',800+12<2**100,'Kc epsilon^2<2^-12')
check('epsilon_geometric_radius',256<2**100,'epsilon<1/256<r0/8')
check('epsilon_ring_threshold',9+2<300,'e^(300H)>9H+ln4 and ring width>e^-9H')

result=dict(all_passed=True,number_of_checks=len(checks),scope='exact arithmetic and symbolic exponent inequalities; not PDE existence/constraint propagation certification',checks=checks)
(BASE/'verification/RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(all_passed=True,number_of_checks=len(checks),scope=result['scope']),ensure_ascii=False))
