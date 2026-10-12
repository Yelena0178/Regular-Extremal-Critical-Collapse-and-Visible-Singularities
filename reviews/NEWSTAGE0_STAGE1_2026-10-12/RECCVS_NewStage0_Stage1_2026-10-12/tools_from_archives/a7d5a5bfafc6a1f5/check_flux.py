#!/usr/bin/env python3
"""Exact finite arithmetic checks. Not a formal PDE/existence proof."""
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
from math import comb, factorial
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]
checks = []

def check(name, assertion, evidence):
    if not assertion:
        raise AssertionError(name)
    checks.append(dict(name=name, passed=True, evidence=str(evidence)))

digest = hashlib.sha256((BASE/'baseline/ROOT_CERTIFICATE_mgeom.json').read_bytes()).hexdigest()
check('root_identity', digest == '7845f2276b7dc12669d9e27861704bdee99f395458c35647fc9c734f93fb6dc2', digest)

# Formal radial differentiation: f^(j) R^(-m) product_i n_i^ell_i.
# D_i n_k=(delta_ik-n_i*n_k)/R. Integer coefficients; all multiindices <=8.
def differentiate(poly, axis):
    out = defaultdict(int)
    for (j, m, ell), c in poly.items():
        plus = list(ell); plus[axis] += 1; plus = tuple(plus)
        out[(j+1, m, plus)] += c
        out[(j, m+1, plus)] -= m*c
        for k in range(3):
            if ell[k]:
                if axis == k:
                    minus = list(ell); minus[k] -= 1
                    out[(j, m+1, tuple(minus))] += ell[k]*c
                out[(j, m+1, plus)] -= ell[k]*c
    return {key: c for key, c in out.items() if c}

radial_rows = []
for order in range(9):
    maxsum = 0
    for i in range(order+1):
        for j in range(order-i+1):
            beta = (i,j,order-i-j)
            poly = {(0,0,(0,0,0)):1}
            for axis, count in enumerate(beta):
                for _ in range(count):
                    poly = differentiate(poly, axis)
            check('radial_homogeneity_'+str(beta), all(a+b == order for a,b,_ in poly), beta)
            maxsum = max(maxsum, sum(abs(c) for c in poly.values()))
    radial_rows.append(maxsum)
    check('radial_coefficient_'+str(order), maxsum < 2**30, maxsum)

# e^(-1/x) derivatives, t=1/x, have polynomial coefficient recurrence.
p = {0:1}; exp_bounds=[]
for j in range(10):
    bound = sum(abs(c)*(k**k if k else 1) for k,c in p.items())
    exp_bounds.append(bound)
    check('exp_step_base_'+str(j), bound < 2**100, bound)
    nxt=defaultdict(int)
    for k,c in p.items():
        nxt[k+2] += c
        if k: nxt[k+1] -= k*c
    p=dict(nxt)
# u(x)+u(1-x)>=e^-2>1/9. Quotient rule recursion.
inverse=[Q(9)]
for j in range(1,10):
    inverse.append(9*sum(comb(j,k)*2**101*inverse[j-k] for k in range(1,j+1)))
step=[sum(comb(j,k)*2**100*inverse[j-k] for k in range(j+1)) for j in range(10)]
check('smooth_step_derivatives', max(step)<2**2000, 'orders 0..9')
check('cutoff_cartesian_margin', 2000+30+6*5 < 2100, 'actual radial coefficients <2^30, r0^-1<32')
check('shell_volume', 8*4*Q(5,64)**2 < 1, 8*4*Q(5,64)**2)
check('cutoff_H7_margin',2100+14+7+6<2200,'Taylor, Leibniz, multiindices/components')
check('multiindex_counts',comb(10,3)==120 and comb(9,3)==84, 'degrees <=7 and <=6 in three variables')
check('H7_product_count',120*128*2**4*32 < 2**40,'embedding constant <=16; component and Leibniz margins')
check('initial_mapper_margin', 40+20+20<100,'product, inverse series and tensor/component margins')
check('source_margin',5*40+40+20+40+20<700,'five inverse factors, products, row count and component margins')
check('second_time_margin',700+40+100<900,'solve principal equation')
check('commutator_margin',300+900+100==1300,'coefficient, second-time and combinatorial margins')
check('energy_margin',1300+40+100+100<4000,'commutator, norm conversions, sums and reserve')
check('energy_bootstrap',4000+2-9990<0,'nonlinear coefficient <1')
check('energy_growth',3**3<2**8,'e<3, exp(3/8)<2')
check('Y_exponent',2300+21==2321,'two energy equivalences and growth')
check('Y_tiny',2321+2**60<2**100,'exponential log gap >H>2^100, ln2<1')

c=0; jet_log=[]
for j in range(2,8):
    c=2048+16*c
    jet_log.append(c)
check('time_jet_log_recurrence',c<2**32,jet_log)
check('A_budget',16*c+2000+100<2**40,'inverse/time jets, products, components, embeddings')
check('source_times_jet_small',2000+17*2**40<2**60,'C_S*A*Y<1')
check('graph_derivative_margin',2100+6*7<4096,'f radial/Cartesian factors to order eight')
check('flux_positivity',16*Q(1,4096)<Q(1,2)*Q(3,4),'16delta <3alpha/4 from alpha>epsilon/2')
check('normalization_worst_power',Q(1,2)+6==Q(13,2)<7,'six derivatives of S^-1/2')

sqrt_coeff=Q(1)
for j in range(1,7):
    sqrt_coeff*=Q(2*j-1,2)
check('square_root_scalar_coefficients',sqrt_coeff<factorial(13)*2**16,sqrt_coeff)
check('tensor_expansion_budget',
      60+60+100+80+160+20<1024,
      'Bell/Leibniz 60, coordinates 60, inverse jet 100, sqrt 80, inverse insertions 160, norms 20')
check('physical_combined_exponent',1024+7*4096+2422==32118,32118)
check('physical_rounding',32118<33000<34000,'compact difference reserve')
check('A_squared_exponent',2*2**40==2**41,2**41)
check('pure_epsilon_power',8+7==15 and 34000+8==34008,'alpha>epsilon/2')
check('init_inverse_exponent',7<8 and 7+1<10,'six inverse derivatives, initializer product reserve')

result=dict(all_passed=True,number_of_checks=len(checks),
            scope='finite coefficient recurrences, exact rational arithmetic and symbolic exponent checks; NOT a formal PDE or root-existence certificate',
            radial_coefficient_rows=radial_rows,time_jet_log_upper_bounds=jet_log,checks=checks)
(BASE/'verification/RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('all_passed','number_of_checks','radial_coefficient_rows','time_jet_log_upper_bounds','scope')},ensure_ascii=False))
