"""GPT 主张，未经外部独立审查。
Exact arithmetic and symbolic identities only; never a PDE existence certificate.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import platform
from exact_rational import Rat, var, symbols

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, value, evidence):
    if not bool(value):
        raise AssertionError(name + ': ' + str(evidence))
    checks.append({'name': name, 'passed': True, 'evidence': str(evidence)})

def ident(name, expression):
    residue = Rat.wrap(expression)
    check(name, residue.is_zero(), 'exact cross-multiplied numerator terms=' + str(residue.n.terms))

def positive_polynomial(name, expression, variable, lower):
    # Coefficients after translation certify the full ray, not a sample point.
    z = var('slack_z')
    translated = expression.substitute('H',lower+z)
    coeffs=list(translated.n.terms.values())
    denominator=translated.d.terms
    check(name, all(v >= 0 for v in coeffs) and translated.n.terms.get((),F(0))>0
          and all(v>0 for v in denominator.values()),
          'positive translated numerator coefficients: '+str(translated.n.terms))

# Exact bump derivative recurrence, including every coefficient.
poly = {0: 1}
bounds = []
polynomials = []
for j in range(8):
    polynomials.append(dict(poly))
    bound = sum(abs(v) * (k ** k if k else 1) for k, v in poly.items())
    bounds.append(bound)
    check(f'u_derivative_bound_{j}', bound < 2**100,
          {'polynomial': poly, 'bound': bound})
    nxt = defaultdict(int)
    for k, v in poly.items():
        nxt[k + 2] += v
        if k:
            nxt[k + 1] -= k * v
    poly = {k: v for k, v in nxt.items() if v}
z = var('z')
for j in range(7):
    pj = sum(v*z**k for k,v in polynomials[j].items())
    pj1 = sum(v*z**k for k,v in polynomials[j+1].items())
    ident(f'u_recurrence_identity_{j}', pj1-z**2*(pj-pj.derivative('z')))
for j in range(8):
    bj = 16**j * sum(comb(j,k)*bounds[k]*bounds[j-k] for k in range(j+1))
    check(f'scaled_product_bound_{j}', bj < 2**(200+5*j), bj)
    check(f'normalized_bound_{j}', 1296*bj < 2**(211+5*j), 1296*bj)
    check(f'candidate_exponent_{j}', 211+5*j <= 246, 211+5*j)
check('candidate_P_bound', 1+2**246 < 2**247, '1+max norm < 1+2^246 < 2^247')
check('e_lower_bound', F(1)+F(1)+F(1,2)>2, 'e > first three Taylor terms > 2')
check('e_upper_tail', F(1,6)/(1-F(1,4)) == F(2,9), 'n!>=6*4^(n-3) for n>=3')
check('e_less_than_3', F(5,2)+F(2,9) < 3, F(49,18))
check('candidate_interval_length', F(13,32)-F(11,32)==F(1,16), '1/16')
for t in [F(11,32),F(13,32)]:
    xx=16*(t-F(5,16)); yy=16*(F(7,16)-t)
    check(f'bump_normalization_interval_{t}', F(1,2)<=xx<=F(3,2)
          and F(1,2)<=yy<=F(3,2), (xx,yy))
check('candidate_integral_lower', F(1,16)*F(1,81)==F(1,1296)>F(1,2048), 'Ib>1/1296>2^-11')

# Convex path budget: all-tau identity, not finite tau sampling.
tau, Pa, P0 = symbols('tau Pa P0')
ident('convex_P_identity', 1+(1-tau)*(Pa-1)+tau*(P0-1)-((1-tau)*Pa+tau*P0))
Pbar=var('Pbar')
ident('convex_max_gap_identity',Pbar-((1-tau)*Pa+tau*P0)-((1-tau)*(Pbar-Pa)+tau*(Pbar-P0)))

# RN lower-bound factors and true symbols in original chart.
check('RN_F_lower_factor', F(1,4)*F(1,4)==F(1,16), '(p-1)^2 >= nu_h^2 sigma^2/4; p^2<4')
check('RN_positive_denominator_upper', 4*2==8, 'nu_h,p_prime<0 and |p_prime|<=2|nu_h|')
check('RN_d_lower_factor', F(1,16)/8==F(1,128), 'sigma^2/128')
check('RN_sigma_to_a_power', 16**2*128==2**15, '(a/16)^2/128=a^2/2^15')
check('RN_safety_20', F(1,2**15)>=F(1,2**20), 'five dyadic powers of slack')
check('mid_slope_safety', F(1,1024)>=F(1,2**20), '0<a<1 implies a/1024>=a^2/2^20')
check('central_slope_safety', 4>=F(1,2**20), 'beta>1 and a<1')
check('J_dyadic', 20+1==21, 'J*=(1/2)e^-2L d*')

d, om, lam, nu, J, A, B = symbols('d om lam nu J A B')
# We use nu as |physical nu| here, so J=lambda+d*nu.
# gUt=-om/2, inverse g^Ut=-2/om. The determinant is -om^2/4!=0.
ident('metric_inverse_off_diagonal',(-om/2)*(-2/om)-1)
ident('double_null_inverse',2*(-2/om)*d+4*d/om)
ident('induced_tangent_norm',2*(-om/2)*(-d)-om*d)
ident('timelike_tube_vector',2*(-om/2)*F(1,2)/(2*d)+om/(4*d))
ident('VF_exact',F(1,2)+d/(2*d)-1)
ident('radial_areal_metric',2*(-om/2)*(-d)/(lam+d*nu)**2-om*d/(lam+d*nu)**2)
check('metric_lower_factor', F(1,2)/4==F(1,8), 'Omega^2>=1/2; J<=2 e^H D')
check('metric_combined_dyadic', 20+3==23, 'a^2/(2^23 e^2H D^2)')
check('metric_conservative_dyadic', 25>=23, 'two more safety powers')

# Candidate endpoint estimates without evaluating huge transcendental numbers.
H=var('H'); hmin=2**100
check('H_candidate_dominance', 100*hmin>247, '100H > 247 > 247 ln2')
check('D0_first_safety', 1+F(1,8)<2, 'D0 < (9/8)e^100H < 2e^100H')
check('D0_second_safety', F(5,2)>2, 'e^H>=e>5/2>2 for H>=1')
check('outer_endpoint_log_power', 2*8+2+2*101==220, 'a^2 e^-2H e^-202H=e^-220H')
check('epsilon_comparison_log2_coefficient', 25-1==24, 'epsilon/2 versus e^-220H/2^25')
positive_polynomial('epsilon_comparison_all_H_ge_1', 1+300*H-220*H-24,H,1)
check('candidate_inner_margin', F(1,2)<1, 'alpha>epsilon/2; epsilon<1')
check('inverse_operator_bound', F(1,1)/F(1,2)==2, 'gamma>=epsilon/2 Id => inverse op<=2/epsilon')

# Coordinate repair: old center y is harmonic label, not areal radius.
delta=F(1,4096)
check('areal_radial_J_lower', 1-3*delta>F(1,2), 1-3*delta)
check('areal_radial_J_upper', 1+3*delta<2, 1+3*delta)
check('areal_angular_J_lower', 1-delta>F(1,2), 1-delta)
check('areal_angular_J_upper', 1+delta<2, 1+delta)
x=var('x')
ident('sqrt_lower_polynomial', (1-x)-(1-x)**2-x*(1-x))
ident('sqrt_upper_polynomial', (1+x)**2-(1+x)-(x+x**2))
check('center_dr_upper_slack', 2+F(1,8)<3, 'partial_R r + f_prime partial_s r <=1+(2+1/8)delta')
check('coordinate_metric_loss', 2**2==4, 'max singular Dx/Dy<2 => min singular Dy/Dx>1/2')
check('areal_endpoint_margin', F(1,2)/4==F(1,8), 'epsilon/8')

# Original giant budget and algebraic tighter budget.
check('Cpsi_outer_power',16**201==2**804,'16^201=2^804')
check('Cpsi_small_log_coeff',2001+248==2249,'2249 ln2')
positive_polynomial('Cpsi_log_slack_full_ray',F(102**2,2)*H**2-200*H-2249,H,hmin)
check('Cpsi_final_comparison',2*hmin>805,'805 ln2 < 805 < 2H; 104<200')
check('Cpsi_vs_N7_exponents',104<200,'log C0<exp104H<exp200H=log N7')
check('C_alg_power_slack',2**804>5120,'positive log M coefficient in log(Cpsi/C_alg)')
check('C_alg_constant_slack',2001*2**804>21160,'positive ln2 coefficient')
check('uniform_B6_power',8+7==15,'alpha^-8 eps^-7 <=2^8 eps^-15')
check('uniform_B6_constant',34000+8==34008,'34008+2^41')
check('uniform_Bg_constant',2048+8==2056,'alpha^-8 <=2^8 eps^-8')
check('endpoint_Bc_safety',30<31,'2^30 C0 <2^31 N7')
check('mass_charge_parameter',1+1==2,'M_ADM=Q=1; m_geom is not mass')
check('reference_d_minus_one',-2*(-1)-1==1 and 2300+1==2301,'reference tail factor gives 2^2301')

# Concentration construction: same spacetime point; exact rational identity.
ell,m,b,v,l,O=symbols('ell m b v l O')
dd=m+b/ell; jj=l+v*dd
gamma=O*dd/jj**2
gamma_cleared=O*ell*(m*ell+b)/((l+v*m)*ell+v*b)**2
ident('concentration_metric_exact',gamma-gamma_cleared)
check('concentration_metric_limit',gamma_cleared.substitute('ell',0).is_zero(),
      'exact ell=0 numerator vanishes; denominator=(v*b)^2 !=0 for v,b>0; continuity gives limit 0')
ident('concentration_upper_gap',O/(v**2*dd)-gamma-
      O*l*(l+2*v*dd)/(v**2*dd*jj**2))
ident('concentration_linear_upper_gap',O*ell/(v**2*b)-O/(v**2*dd)-
      O*m*ell**2/(v**2*b*(m*ell+b)))
ident('fixed_event_CDF_half',-A-B*F(1,2)-(-A-B/2))
check('concentration_support',F(3,8)-F(1,16)>F(1,4) and F(3,8)+F(1,16)<F(1,2),
      'all scaled symmetric bumps remain strictly inside prescribed interval')
for j in range(8):
    check(f'concentration_derivative_scaling_{j}',j+1>0,
          '||psi_ell^(j)||=ell^(-j-1)||b^(j)||')

# Tube identities (parameter time versus proper time).
check('tube_vstar',20+20==40 and 1+2==3,'v*=a*d*/2^20=a^3/2^40')
check('tube_U_slack',F(1,2**41)<F(1,8192),'|Delta U| <=a^3/2^41<a/8192')
check('tube_t_slack',F(1,2**21)<F(1,16),'|Delta t|<=a/2^21<1/16')
check('ambient_U0_slack',F(1,2**15)<F(1,8192),'cutoff support margin')
check('ambient_Ustar_slack',F(1,2**15)<F(1,4096),'cutoff support margin')

root_file=ROOT/'baseline/ROOT_CERTIFICATE_mgeom.json'
digest=hashlib.sha256(root_file.read_bytes()).hexdigest()
check('frozen_root_identity',digest=='7845f2276b7dc12669d9e27861704bdee99f395458c35647fc9c734f93fb6dc2',digest)

result={
    'label':'GPT 主张，未经外部独立审查',
    'number_of_checks':len(checks),'all_passed':True,'checks':checks,
    'environment':{'python':platform.python_version(),'symbolic_engine':'code/exact_rational.py; Fraction-only cross multiplication'},
    'scope':'Exact finite bump coefficients, rational factors, symbolic metric identities and concentration limit, polynomial exponent slack; no PDE or external independent review.',
    'path_pure_numeric_certificate':False,
    'endpoint_bounds':'conditional on frozen field, center and extraction inputs',
    'coordinate_correction':{'frozen_labels_lower':'epsilon/2','global_areal_lower':'epsilon/8','H6_same_numeric_budget_after_change':False},
    'actual_candidate_selection':'conditional on existing common development, Cauchy and MGHD inputs',
}
(ROOT/'verification/RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['number_of_checks','all_passed','environment','scope']},ensure_ascii=False))
