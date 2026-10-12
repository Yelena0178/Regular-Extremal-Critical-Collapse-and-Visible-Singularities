"""Exact arithmetic audit of Stage 3. Python stdlib only; do not use -O.

PROOF_H.md supplies the analytic inequalities. This program checks their
constants and the inherited box-root handoff; it does not solve a PDE.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

def p(n):
    return F(1 << n) if n >= 0 else F(1, 1 << -n)

def audit(root_path, output_dir):
    root_path = Path(root_path)
    d = json.loads(root_path.read_text())
    M = d['m']['power_of_two_exponent']; T = d['T']
    assert (M, T, d['K'], d['mu']) == (2104156, 1048578, 8, '3/5')
    assert d['status'] == 'CERTIFIED_BOX_ROOT_OF_FROZEN_FINITE_ENDPOINT_SYSTEM'
    assert d['scope']['finite_jet_endpoint_root']
    box = d['parameter_box']; kap = box['kappa_center']
    kh = F(int(kap['numerator_hex'], 16), 1 << kap['denominator_power'])
    assert F(7, 8) < kh-p(-3900) < kh+p(-3900) < 1
    assert box['c_real_component_radius_power_of_two'] == -4097
    assert 2*p(-4097)**2 < p(-4096)**2
    assert d['inclusion']['Y_power_of_two_upper'] == 348174+4103-M
    assert d['inclusion']['q_power_of_two_upper'] == 348174+10-M
    A = [[F(v) for v in row] for row in d['jacobian_enclosure']['center_matrix']]
    P = [[F(v) for v in row] for row in d['preconditioner']['matrix']]
    for i in range(16):
        for j in range(16):
            assert sum(P[i][k]*A[k][j] for k in range(16)) == (i == j)
    assert max(sum(abs(v) for v in row) for row in P) < 64
    eps = p(348174-M); contraction = p(348174+10-M)
    assert 64*eps/(1-contraction) < p(348181-M)

    # Uniform analytic H constants, valid already for M >= 22000.
    b, J, C0 = p(3201), p(3206), p(4000)
    assert 15*b+50 < J
    assert 2*J < C0
    assert 4*C0/2-4 >= C0+1
    assert T < p(21)
    X = (1 << 4002)*T
    assert X < p(4025)
    eta = p(-3950)
    assert F(7,8)*(1-3*eta)-p(6424-M) > F(3,4)
    assert 1+3*eta+p(6424-M) < F(5,4)
    # e^(3/4)>2, e^(5/4)<4, via exact rational Taylor and e<3.
    assert 1+F(3,4)+F(3,4)**2/2+F(3,4)**3/6 > 2
    assert 3**5 < 4**4
    # The second-order ratio remainder budgets used in PROOF_H.md.
    assert C0*b+b*b < p(7202)
    assert 2*p(7202)+b*b < p(7205)
    assert 2*b*b < p(6405)
    assert p(7205)+p(6405)+4*b*b < p(12000)
    assert 2+8+16 < 32
    assert 12006+2*4026 < 20100
    for m_exp in [22000, M]:
        assert b*p(-m_exp) < F(1,4)
        assert J*p(-m_exp) < F(1,6)
        assert 4*b*p(-m_exp) < F(1,2)
        assert 4*b*p(-m_exp)*X < F(1,2)
        assert p(20100-m_exp) <= p(-856)

    # First PHYSICAL period, x runs from L to L-T, not from 0 to T.
    q_upper_exp = 3201-M
    q_lower_exp = -M-2*T-2
    d_upper_exp = 3202+21-M
    d_lower_exp = -M-2*T-2
    charge_ratio_exp = 4-M  # 12 delta < 16 delta
    epsilon_exp = 8-2*M
    width_exp = 3201+2*T-M  # uses rho < 1/2 and exp(T) < 2^(2T)
    eta_loss_exp = 1-T
    assert 3201-M < -T
    assert d_upper_exp < -20
    assert epsilon_exp < -10
    assert width_exp < -4
    assert 3201+21-M < -22
    assert 12*p(-M) < F(1,32)
    assert 144 < 256
    assert eta_loss_exp <= -2
    # An--Lim sufficient inequalities from the accepted Stage 1 matrix.
    threshold1 = F(26,1024)+F(9,32768)
    threshold2 = F(14,32768)
    width1 = F(1024,116281)
    width2 = F(20480,116281)
    assert threshold1 < F(1,16) and threshold2 < F(1,16)
    assert width1 < F(1,8) and width2 < 2
    assert F(65,512) < 1
    # Positivity of every (finite member) scale; logarithmic storage avoids
    # expanding exp(-mT). No decimal evaluation of t1 or beta is used.
    radius_width_lower_exp = d_lower_exp-2
    before_target_radius_lower_exp = radius_width_lower_exp+1
    volume_upper_exp = width_exp+2

    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    identity = dict(mu='3/5', K=8, T=T, m_power_of_two_exponent=M,
                    root_sha256=hashlib.sha256(root_path.read_bytes()).hexdigest(),
                    root_file='baseline/certificates/ROOT_CERTIFICATE_mgeom.json')
    h = dict(status='ANALYTIC_WHOLE_CONE_H_BOUND_WITH_EXACT_CONSTANT_AUDIT',
             identity=identity, constants=dict(b_power=3201, tail_integral_error_power=3206,
             C0_power=4000, N0_power=4002, X='2^4002*T',
             ratio_remainder_power=12000, compact_integrated_remainder_power=20100,
             sufficient_m_power=22000, kernel_lower_power=-855),
             bound='H_L(t) >= delta*2^(-856)*t for exp(-m*T)<=t<=1',
             scope='Whole finite pulse, plus exact Minkowski continuation. H=0 at the regular axis; H/r>0 there.',
             source='PROOF_H.md; inherited L020/L021 profile inequalities',
             actual_PDE_global_certificate=False)
    inputs = dict(status='CERTIFIED_SPECIFIED_CHARACTERISTIC_INPUTS_NOT_GLOBAL_PDE_DOMAIN',
        identity=identity, parameter_box=box,
        definitions=dict(delta='kappa_star/2^M', L='2^M*T', t1='exp(-L)',
          t2='exp(-(L-T))', rho='R(L)', beta='q(L)*R(L)/t1',
          tc='t1-rho/beta',
          u='U/(2*beta)-2*rho', v='2*beta*(t-tc)',
          u0='-2*rho', v1='2*rho',
          center_line_in_flat_region='v=u+2*rho',
          v2='v1+2*q(L)*rho*(exp(T)-1)',
          first_period='t1 <= t <= t2; x=L down to L-T'),
        envelopes=dict(rho_lower='1/4',rho_upper='1/2',
          q_L_lower_power=q_lower_exp,q_L_upper_power=q_upper_exp,
          eta0_lower='1-2^('+str(eta_loss_exp)+')',eta0_upper='1',
          d0_strict_lower_power=d_lower_exp,d0_strict_upper_power=d_upper_exp,
          charge_ratio_upper_power=charge_ratio_exp,epsilon_strict_upper_power=epsilon_exp,
          Delta_v_strict_upper_power=width_exp,mu_Delta_v_strict_upper_power=width_exp,
          omega='1/2',AL_L='0',AL_psi1='0',H_pulse_over_delta_t_lower_power=-856,
          physical_radius_width_strict_lower_power=radius_width_lower_exp,
          conditional_bootstrap_radius_lower_power=before_target_radius_lower_exp,
          conditional_quotient_volume_upper_power=volume_upper_exp),
        epsilon_domain='outgoing prefix from its center to v2, and complete incoming v=v1; NOT the entire formation cone',
        mass_definition='m_H=r*(1+4*r_u*r_v/Omega^2)/2; eta0=2*(m2-m1)/r2; m1=0',
        incoming_data='r=-u/2, Omega^2=1, phi=Q=A_u=0, -2*rho<=u<=0',
        full_smooth_initial_edges=True,
        local_positive_radius_characteristic_realization='external KU Proposition 2.1, with exact flat cap',
        common_single_ended_Cauchy_identification_certified=False,
        AL_target_domain_and_strict_trapping_certified=False,
        smooth_repair_certified=False)
    handoff = dict(status='FORMAL_ROOT_HANDED_TO_H_AND_CHARACTERISTIC_INPUT_CERTIFICATES',
        identity=identity, inherited_root_scope=d['scope'],
        same_member_fixed_by='unique joint root (c_star,kappa_star) in the inherited product box',
        root_component_strict_upper_power=348181-M,
        completed=['same-box identity and exact inverse audit','whole-pulse H positivity',
          'exact complete Minkowski incoming data and flat center cap',
          'finite D8 endpoint ERN sphere identification interface',
          'first physical period characteristic inputs'],
        unresolved=['quantitatively fixed common Cauchy hypersurface and inclusion domain',
          'quantitatively specified actual two-sided gluing domain',
          'D001 version of the complete An-Lim proof and actual target domain continuation',
          'finite regularity versus smooth continuation and strong repair budget'],
        forbidden_inferences=['auxiliary e_infinity equals mu','global epsilon small on entire formation cone',
          'H positivity gives full PDE development','box root implies complete Cauchy realization',
          'input inequalities alone certify strict trapped sphere'])
    for name,obj in [('H_CERTIFICATE.json',h),('FIRST_PERIOD_INPUTS.json',inputs),('ROOT_HANDOFF.json',handoff)]:
        (output_dir/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
    result=dict(status='ALL_STAGE3_EXACT_CONSTANT_CHECKS_PASS', identity=identity,
        key_bounds=inputs['envelopes'],
        scope='Arithmetic audit of analytic proof constants, root identity, and initial cone data; no global PDE claim')
    (output_dir/'ARITHMETIC_CHECK.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(status=result['status'],root_component_power=handoff['root_component_strict_upper_power'],
        first_period=inputs['envelopes']),ensure_ascii=False,indent=2))

if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Do not disable assertions.')
    audit(sys.argv[1],sys.argv[2])
