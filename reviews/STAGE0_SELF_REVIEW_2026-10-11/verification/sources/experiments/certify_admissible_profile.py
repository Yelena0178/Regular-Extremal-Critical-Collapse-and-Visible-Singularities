"""Exact bounds for an explicitly defined smooth periodic K=8 profile family.

This checks the rational parts of L021. The cutoff and bumps are defined
analytically in that proof; their integrals need not be rounded to create
the exact family. This is NOT a finite-amplitude formation root or a PDE.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from math import comb, gcd, lcm
from pathlib import Path

from freeze_filtered_profile import add, mul, cadd, cderiv, cscale, integral_exp, make
from certify_filtered_J import primitive, split, certify as certify_J


def require(condition, message):
    if not condition: raise ValueError(message+'; NOT CERTIFIED')


def bernstein(p, left, right):
    """Power polynomial on [left,right] -> integer Bernstein coefficients."""
    d = len(p)-1
    width = right-left
    power = [sum((p[j]*comb(j,k)*left**(j-k)*width**k
                  for j in range(k,d+1)), F(0)) for k in range(d+1)]
    b = [sum((power[j]*F(comb(k,j),comb(d,j)) for j in range(k+1)),F(0))
         for k in range(d+1)]
    den = 1
    for v in b: den = lcm(den,v.denominator)
    return primitive([int(v*den) for v in b])


def positive_certificate(p, left, right, max_depth=30):
    todo = [(0,0,bernstein(p,left,right))]
    leaves=[]; nodes=0
    while todo:
        index,depth,b=todo.pop(); nodes+=1
        if min(b)>0:
            leaves.append(dict(index=index,depth=depth,
                               all_bernstein_coefficients_positive=True))
            continue
        if depth>=max_depth or nodes>20000:
            raise RuntimeError('positive polynomial bound NOT CERTIFIED')
        lb,rb=split(b)
        todo.append((2*index+1,depth+1,rb))
        todo.append((2*index,depth+1,lb))
    return dict(left=str(left),right=str(right),node_count=nodes,
                leaf_count=len(leaves),leaves=leaves)


def abs_eval(p,x): return sum((abs(v)*x**j for j,v in enumerate(p)),F(0))


def certify(path):
    raw=path.read_bytes(); data=json.loads(raw)
    require((data['K'],data['n'],data['sigma']) == (8,88,'1/20'),
            'incorrect frozen profile parameters')
    regenerated=make(88,F(1,20),8)
    require(data==regenerated,'stored profile differs from exact defining expression')
    j_cert=certify_J(regenerated)
    require(j_cert['single_negative_to_positive'],'global J sign structure failed')
    p=([F(x) for x in data['polynomial_real']],
       [F(x) for x in data['polynomial_imag']])
    y=cadd(cderiv(p),cscale(p,F(-1,20),F(1,4)))
    D=add(mul(p[0],p[0]),mul(p[1],p[1]))
    E=add(mul(y[0],y[0]),mul(y[1],y[1]))
    C=add(mul(p[0],y[1]),[-x for x in mul(p[1],y[0])])
    et=integral_exp(E,F(1,10)); ct=integral_exp(C,F(1,10))
    lam=2*et/ct
    k0=(2*lam*integral_exp(C,F(11,10))
        -integral_exp(E,F(11,10)))/et
    require(et == F(data['E_total']) and ct == F(data['C_total']),'total integrals mismatch')
    require(F(1,2) < lam < F(51,100),'coupling interval failed')
    require(k0 > F(1,2**854),'endpoint kernel lower bound failed')
    require(3 < ct/et < 4,'current interval failed')
    p_order=min(next(i for i,v in enumerate(a) if v) for a in p)
    y_order=min(next(i for i,v in enumerate(a) if v) for a in y)
    require(p_order == 36 and y_order == 35,'origin vanishing orders failed')
    h0=sum((abs(v) for a in p for v in a),F(0))
    h1=sum((abs(v) for a in y for v in a),F(0))
    require(h0*h0 < et and h1*h1 < et,'normalized coefficient bound failed')
    core_h0=sum((abs_eval(a,F(9)) for a in p),F(0))
    core_h1=sum((abs_eval(a,F(9)) for a in y),F(0))
    require(core_h0*core_h0 < et and core_h1*core_h1 < et,'core pointwise upper bounds failed')
    bound=D.copy(); bound[0]-=et*F(1,2**1998)
    core_cert=positive_certificate(bound,F(3,4),F(33,4))
    return dict(
        status='EXPLICIT_SMOOTH_PERIODIC_LEADING_FAMILY_NOT_FINITE_AMPLITUDE_SEED',
        profile_sha256=hashlib.sha256(raw).hexdigest(),
        global_J_certificate=dict(root_count=j_cert['positive_root_count'],
                                  single_negative_to_positive=True,
                                  node_count=j_cert['node_count']),
        exact_checks=dict(lambda_interval=['1/2','51/100'],
                          normalized_K0_lower='2^-854',
                          normalized_total_current_interval=['3','4'],
                          origin_orders=dict(field=p_order,field_derivative=y_order),
                          normalized_coefficient_l1_bounds=dict(field='<1',derivative='<1'),
                          normalized_core_pointwise_upper=dict(field='<1',derivative='<1'),
                          core_polynomial_lower='D/E_total > 2^-1998'),
        core_positive_certificate=core_cert,
        analytically_verified_constants=dict(
            left_cutoff_a='2^-1000',right_cutoff_B=2**20,period_T=2**20+2,
            cutoff_H1_error_upper='2^-20000',
            bump_centers=list(range(1,9)),bump_halfwidth='1/4',
            moment_inverse_infinity_norm_upper='2^128',
            repaired_base_H1_error_upper='2^-19000',
            parameter_ball_max_complex_modulus='2^-4096',
            family_H1_error_upper='2^-3950',
            family_core_C1_error_upper='2^-3950',
            family_lambda_upper='3/5',
            family_single_block_K_lower='2^-855',
            family_periodic_K_lower='2^-855'),
        analytic_dependency='RECCVS_L020.md + RECCVS_L021.md; not an interval PDE solver')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('profile');parser.add_argument('output')
    args=parser.parse_args();cert=certify(Path(args.profile))
    Path(args.output).write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({k:v for k,v in cert.items() if k!='core_positive_certificate'}))
    print('core polynomial positivity nodes:',cert['core_positive_certificate']['node_count'])
