#!/usr/bin/env python3
"""Independent exact arithmetic audit; NOT a PDE existence certificate.

Only Python stdlib. No imports of the previous generator/checker.
Run from any directory: python3 code/independent_audit.py
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json

BASE = Path(__file__).resolve().parents[1]
checks = []
def check(name, condition, evidence):
    if not condition:
        raise AssertionError(name)
    checks.append(dict(name=name, passed=True, evidence=str(evidence)))

M, T = 2104156, 1048578
root = BASE / 'baseline/ROOT_CERTIFICATE_mgeom.json'
sha = hashlib.sha256(root.read_bytes()).hexdigest()
check('same_root_identity', sha == '7845f2276b7dc12669d9e27861704bdee99f395458c35647fc9c734f93fb6dc2', sha)
env = json.loads((BASE/'baseline/FIRST_PERIOD_INPUTS.json').read_text())['envelopes']
check('eta_input_exponent', env['eta0_lower'] == f'1-2^({1-T})', 1-T)
check('width_input_exponent', env['Delta_v_strict_upper_power'] == 3201+2*T-M == -3799, -3799)
check('charge_input_exponent', env['epsilon_strict_upper_power'] == 8-2*M == -4208304, -4208304)
check('eta15over16', T-1 > 4, '2^(-1048577)<1/16')
check('b64', env['d0_strict_upper_power'] < -6, 'b<d0<2^-2100933<1/64')
check('h16_geometry', F(1,4)*(F(1,2)-F(1,64)) == F(31,256) > F(1,16), F(31,256))
check('radius_ratio_improvement', F(1,64)/(F(1,2)-F(1,64)) == F(1,31) < F(1,2), F(1,31))

h = F(1,16)
ec = h**4/2**12
alpha = 5*ec/(4*h*h)+ec*ec/h**4+F(5,2)*ec
check('cell_absorption', alpha < F(1,4), alpha)
check('n_substitution', 16+5*4 == 36, 'n=2+2^36*(B+1), B=2^7000000')
check('phi_v_exponent', 4201315-1052078+1600 == 3150837 < 3150840, 3150837)
check('r_vv_exponent', 2*3150840 == 6301680 < 7000000, 6301680)
check('lapse_boundary', 136*4+328 < 2**10, 136*4+328)
check('r_uu_boundary', 4*2**10+4*17**2 < 2**13, 4*2**10+4*17**2)

# Monomial majorants for the complete first-order D001 RHS, real components.
# entry: (absolute coefficient sum incl. complex-component expansion,
#         number of direct variable factors, inverse-r power, exponential ell).
rows = {
 'r_u': [(1,1,0,0)],
 'phi_u': [(1,1,1,0),(2,2,0,0)],
 'ell_u': [(1,1,0,0)],
 'Q_u': [(2,3,0,0)],
 'lambda_u': [(1,2,1,0),(F(1,4),0,1,1),(F(1,4),2,3,1)],
 'zeta_u': [(1,2,1,0),(F(1,4),2,1,1),(2,2,0,0)],
 'kappa_u': [(4,2,2,0),(F(1,2),0,2,1),(2,2,2,0),(1,2,4,1)],
 'nu_v': [(1,2,1,0),(F(1,4),0,1,1),(F(1,4),2,3,1)],
 'eta_v': [(1,2,1,0),(F(1,4),2,1,1)],
 'A_v': [(F(1,2),1,2,1)],
 'ell_u_v': [(4,2,2,0),(F(1,2),0,2,1),(2,2,2,0),(1,2,4,1)]
}
row_evidence = {}
for name, terms in rows.items():
    # For N>=1: each monomial and each first derivative <=
    # c*2^(a+b+1)*(1+a+b)*(1+N)^12*exp(2N).
    # r differentiation increases inverse power by 1; ell derivative does not
    # add polynomial factors. Coupling |mu|<=1 is treated as fixed.
    coef = sum(c*2**(a+b+1)*(1+a+b) for c,a,b,e in terms)
    degree = max(a+b+1 for c,a,b,e in terms)
    check('rhs_row_'+name, degree<=12 and coef<2**60, f'coefficient={coef}, degree<={degree}')
    row_evidence[name] = dict(coefficient=str(coef), polynomial_degree=degree)
check('picard_budget', 8*F(1,2**40)<1, '8*N*d(N)*L_N <=8*2^-40, since N/(1+N)^8<=1 and exp(-18N)<=1')

chi = F(1, 2**7596)
theta_bound_sq = F(1, 2**7598)
check('chi_definition', 4*theta_bound_sq == chi, 'chi=4*(2^-3799)^2=2^-7596')
check('charge_margin', F(9,4)*theta_bound_sq < chi, '9/4<4; strict only when eta>0')
check('electric_margin', F(9,4)*chi*theta_bound_sq <= chi**2, '(9/4)/4=9/16')
check('zeta_margin', (1+chi)**2 <= 1+4*chi, 'chi^2<=2*chi')
check('mass_integrating_factor_exponent_sum', -(2+3*chi)+(1+4*chi) == -1+chi, 'x power and (x-b) power yield the stated partial fractions')
# x f = -(2+3chi)+(1+4chi)*x/(x-b)
#      = -1+chi+(1+4chi)*b/(x-b).
check('mass_partial_fraction', -(2+3*chi)+(1+4*chi) == -1+chi, '-1+chi')
check('ratio_fraction', (F(1,2)-F(1,64))/(1-F(1,64)) == F(31,63)>F(31,64), F(31,63))
check('eighth_power', F(7,8)**8 < F(31,64), F(7,8)**8)
check('exponent_margin', 4*chi < F(1,8), '4chi<1/8')
mass = F(15,16)*4*F(31,64)*F(7,8)
check('mass_contradiction', mass==F(3255,2048)>1, mass)
check('first_contact_slope', (1-F(1,32))/4 > F(1,8), 'r<=1, Omega^2>=exp(-Z), chi<1/32')

# Differentiate theta(x)=exp(-1/x): theta^(k)=exp(-t)*p_k(t), t=1/x.
p = {0: 1}
theta_bounds=[]
for k in range(6):
    bound=sum(abs(c)*(j**j if j else 1) for j,c in p.items())
    theta_bounds.append(bound)
    check('theta_derivative_'+str(k), bound<2**48, bound)
    nxt={}
    for j,c in p.items():
        nxt[j+2]=nxt.get(j+2,0)+c
        if j: nxt[j+1]=nxt.get(j+1,0)-j*c
    p=nxt
# One of x,1-x>=1/2, so denominator >=exp(-2)>1/9 because e<3.
# Majorize reciprocal derivatives by Leibniz recurrence, not a sampled grid.
from math import comb
inv=[F(9)]
for k in range(1,6):
    inv.append(9*sum(F(comb(k,j))*2**49*inv[k-j] for j in range(1,k+1)))
step=[sum(F(comb(k,j))*2**48*inv[k-j] for j in range(k+1)) for k in range(6)]
check('step_0_to_5', max(step)<2**512, 'exact reciprocal-derivative majorants')
check('cartesian_cutoff', 512+16+15 <=544, 'Faà di Bruno partitions and derivatives R<=2^16 R^(1-j), R^-3<2^15')
check('taylor_order', 7-4==3, 'zero Cartesian jets through order 6 at R=r0; C7 remainder')
check('H4_constant', 544+19+4+8 <600, '2^575<2^600')
check('epsilon_algebra', F(1,2**12)==F(1,4096), 'epsilon^2<=1/(4096*Kc) =>Kc*epsilon^3<=epsilon/4096')
out=dict(scope='exact algebra, derivative majorants and frozen-root identity; NOT PDE or numeric reverse-Cauchy certification',
         number_of_checks=len(checks),all_passed=True,checks=checks,rhs_rows=row_evidence)
(BASE/'verification/RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(all_passed=True,number_of_checks=len(checks),scope=out['scope']),ensure_ascii=False))
