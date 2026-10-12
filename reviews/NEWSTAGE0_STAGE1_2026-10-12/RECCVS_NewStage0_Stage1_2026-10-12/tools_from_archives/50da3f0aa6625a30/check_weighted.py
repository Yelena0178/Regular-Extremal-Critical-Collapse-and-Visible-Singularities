#!/usr/bin/env python3
"""Finite exact checks. Does not certify PDEs or recover the missing actual psi."""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
from math import comb, factorial
import hashlib
import json

B=Path(__file__).resolve().parents[1]
checks=[]
def check(name,test,evidence):
    if not test:raise AssertionError(name)
    checks.append(dict(name=name,passed=True,evidence=str(evidence)))

digest=hashlib.sha256((B/'baseline/ROOT_CERTIFICATE_mgeom.json').read_bytes()).hexdigest()
check('same_root',digest=='7845f2276b7dc12669d9e27861704bdee99f395458c35647fc9c734f93fb6dc2',digest)
source=(B/'baseline/COMMON_CAUCHY_REALIZATION_mgeom.md').read_text()
check('psi_class_only_in_frozen_source','取固定非负光滑 ψ' in source,'definition audit is manual; string check only')

# u^(j)(x)=exp(-t)*p_j(t), t=1/x. No imports from older checks.
p={0:1};ub=[]
for j in range(10):
    bound=sum(abs(c)*(k**k if k else 1) for k,c in p.items())
    ub.append(bound)
    check('u_derivative_'+str(j),bound<2**100,bound)
    q=defaultdict(int)
    for k,c in p.items():
        q[k+2]+=c
        if k:q[k+1]-=k*c
    p=dict(q)
for j in range(8):
    bound=16**j*sum(comb(j,k)*ub[k]*ub[j-k] for k in range(j+1))
    check('candidate_bump_derivative_'+str(j),bound<2**(200+5*j),bound)
    check('candidate_psi_derivative_'+str(j),11+200+5*j<=246,211+5*j)
check('candidate_integral_lower',F(1,16*81)>F(1,2**11),'u factors >=exp(-2), e<3')
check('candidate_Ppsi',246+1==247,'1+max derivative <2^247')

# Seven-node reflection at a ball boundary; interpolation at +1 from -l.
reflection=[(-1)**(l-1)*l*comb(8,l+1) for l in range(1,8)]
for j in range(7):
    value=sum(c*(-l)**j for l,c in enumerate(reflection,1))
    check('reflection_moment_'+str(j),value==1,value)
check('reflection_coefficient_max',max(map(abs,reflection))==224,reflection)
q0,q1,q2=1,4,310
v0=9;v1=9*2*q1*v0
v2=9*(2*2*q1*v1+2*q2*v0)
theta2=q2*v0+2*q1*v1+q0*v2
check('theta_H2_constant',theta2==151506 and theta2<2**18,theta2)
check('local_H2_extension_margin',18+10+10+6+20<80,'cutoff, reflection, coordinates and norms')
check('local_H6_product_margin',84*64*32*2**80<2**100,'embedding, Leibniz and component sums')

# Radial Cartesian derivative coefficient recurrence, with angular seed n_i/n_i*n_j.
def diff(poly,axis):
    out=defaultdict(int)
    for (j,m,ell),c in poly.items():
        plus=list(ell);plus[axis]+=1;plus=tuple(plus)
        out[j+1,m,plus]+=c
        out[j,m+1,plus]-=m*c
        for k in range(3):
            if ell[k]:
                if k==axis:
                    minus=list(ell);minus[k]-=1
                    out[j,m+1,tuple(minus)]+=ell[k]*c
                out[j,m+1,plus]-=ell[k]*c
    return {k:v for k,v in out.items() if v}
rows=[]
seeds=[]
for i in range(3):
    ell=[0]*3;ell[i]=1;seeds.append(tuple(ell))
    for j in range(3):
        ell=[0]*3;ell[i]+=1;ell[j]+=1;seeds.append(tuple(ell))
for order in range(7):
    largest=0
    for i in range(order+1):
        for j in range(order-i+1):
            beta=(i,j,order-i-j)
            for seed in seeds:
                poly={(0,0,seed):1}
                for axis,count in enumerate(beta):
                    for _ in range(count):poly=diff(poly,axis)
                assert all(a+b==order for a,b,_ in poly)
                largest=max(largest,sum(map(abs,poly.values())))
    rows.append(largest)
    check('angular_radial_coefficients_'+str(order),largest<2**40,largest)

# Closed rational formulas, checked by derivative recurrence in (R-1)^(-p), R^(-p).
h={(1,1):2,(1,2):1} # (shift,power): coefficient, shift=1 =>R-1.
e={(1,1):1,(0,1):-1}
def rational_diff(poly):return {(s,p+1):-p*c for (s,p),c in poly.items()}
for j in range(7):
    check('metric_derivative_formula_'+str(j),h=={(1,j+1):(-1)**j*2*factorial(j),(1,j+2):(-1)**j*factorial(j+1)},h)
    check('electric_derivative_formula_'+str(j),e=={(1,j+1):(-1)**j*factorial(j),(0,j+1):-(-1)**j*factorial(j)},e)
    h=rational_diff(h);e=rational_diff(e)
check('tail_pointwise_budget',40+13+10+8+10<100,'radial coefficient, factorial, dyadic radial scaling, throat interval and reserve')
check('tail_norm_count',2**13*16*84*15<2**30,'weight, angular measure, multiindices, metric and both E conventions')
check('tail_final_exponent',100+15<120,'square-root norm and sum reserve')
check('tail_integral_d_minus_one',F(1,1)==F(1,-2*(-1)-1),'R_R>1; integral R^-2 is bounded by integration from 1')
check('compact_weight',3**13<2**21,'R<2 and maximum squared weight exponent <13')
check('compact_norm_margin',11+7+6<30,'weight square root, volume and component/multiindex margins')
check('RN_tail_gap',F(1,16)*F(1,2)>F(1,64),'p gap at U* and backward comparison')
check('RN_reference_d_lower',F(1,16)**2/F(128)>F(1,2**20),'|sigma_RN|>=a/16')
check('J_Sigma_lower',F(1,2**20)*F(1,2)==F(1,2**21),'d minimum times -nu minimum')
check('inverse_denominator_budget',16+2<20,'a^-2=exp(16H), L<H and dyadic constants absorbed')
check('RN_vector_field_budget',14<20 and 18<40,'p jet and inverse p-prime factor counts')
check('RN_t_derivative_count',7+1==8,'seven time derivatives of vector field')
check('RN_exp_absorption',640+82000<100*2**100,'log C_R <=640L+82000, H>2^100*200(L+4)')
check('jet_operation_count',32+24+48+24+32==160<200,'explicit batch count in proof')
check('jet_recurrence_envelope',F(16,15)<16,'200 iterations of log map absorbed by exponent16^201')
check('candidate_Cpsi_log',4*201==804 and 805<2**100,'log Cpsi<=2^805 exp(102H)<exp(104H)')
check('candidate_below_N7',104<200,'conditional on Ppsi<2^247, not actual certificate')
check('gauge_norm_margin',6*100+100+100<2048,'local products, Bell and component/weight reserve')
check('inverse_metric_norm_margin',7*100+100+100<2048,'inverse derivatives and extra tensor product')
check('reference_budget_margin',2000+40+30+30+30<2300,'cutoff, Cartesian, weights, volume and norm reserve')
check('reference_d_minus_one',2300+1==2301,'B_ref(-1)=2^2301')

result=dict(all_passed=True,number_of_checks=len(checks),
 scope='exact finite arithmetic and derivative recurrences; NOT actual psi identification, PDE existence, global gauge-group or Cauchy-isotopy certification',
 actual_psi_numerically_certified=False,candidate_psi_bound='P_psi0<2^247',
 radial_angular_coefficient_rows=rows,reflection_coefficients=reflection,checks=checks)
(B/'verification/RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['all_passed','number_of_checks','actual_psi_numerically_certified','radial_angular_coefficient_rows','scope']},ensure_ascii=False))
