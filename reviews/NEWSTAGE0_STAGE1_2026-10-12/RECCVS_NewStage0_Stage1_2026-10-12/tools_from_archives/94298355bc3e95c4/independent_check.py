"""Independent integer/rational and exact kernel-identity check.

Does not import check_stage3. Does not assume existence of a PDE rectangle.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
import hashlib
import sys

def dy(n):
    return Q(2)**n

def lin_add(*vs):
    out={}
    for v in vs:
        for k,a in v.items():out[k]=out.get(k,Q(0))+a
    return {k:a for k,a in out.items() if a}

def scale(v,a):return {k:a*x for k,x in v.items() if a*x}

def derivative(v):
    # State functions: F'=C, P_E'=E, p'=E-p,
    # T_C'=T_C-C, T_E'=T_E-E. A lambda degree is a constant label.
    rule={'F':{'C':1},'PE':{'E':1},'p':{'E':1,'p':-1},
          'TC':{'TC':1,'C':-1},'TE':{'TE':1,'E':-1},
          'C':{'Cp':1},'E':{'Ep':1}}
    out={}
    for (symbol,lam_degree),a in v.items():
        for child,b in rule[symbol].items():
            key=(child,lam_degree);out[key]=out.get(key,Q(0))+a*b
    return {k:a for k,a in out.items() if a}

def audit(directory):
    directory=Path(directory)
    inp=json.loads((directory/'certificates/FIRST_PERIOD_INPUTS.json').read_text())
    hc=json.loads((directory/'certificates/H_CERTIFICATE.json').read_text())
    hand=json.loads((directory/'certificates/ROOT_HANDOFF.json').read_text())
    root_path=directory/'baseline/certificates/ROOT_CERTIFICATE_mgeom.json'
    root=json.loads(root_path.read_text())
    for obj in [inp,hc,hand]:
        assert obj['identity']['root_sha256']==hashlib.sha256(root_path.read_bytes()).hexdigest()
        assert obj['identity']['m_power_of_two_exponent']==2104156
    assert root['scope']['finite_jet_endpoint_root']
    assert not inp['common_single_ended_Cauchy_identification_certified']
    assert not inp['AL_target_domain_and_strict_trapping_certified']
    assert not hc['actual_PDE_global_certificate']
    assert not inp['smooth_repair_certified']

    M=root['m']['power_of_two_exponent'];T=root['T']
    env=inp['envelopes']
    expected={
      'q_L_lower_power':-M-2*T-2,'q_L_upper_power':3201-M,
      'd0_strict_lower_power':-M-2*T-2,'d0_strict_upper_power':3223-M,
      'charge_ratio_upper_power':4-M,'epsilon_strict_upper_power':8-2*M,
      'Delta_v_strict_upper_power':3201+2*T-M,
      'mu_Delta_v_strict_upper_power':3201+2*T-M,
      'physical_radius_width_strict_lower_power':-M-2*T-4,
      'conditional_bootstrap_radius_lower_power':-M-2*T-3,
      'conditional_quotient_volume_upper_power':3203+2*T-M,
      'H_pulse_over_delta_t_lower_power':-856}
    for key,value in expected.items():assert env[key]==value
    assert env['eta0_lower']=='1-2^('+str(1-T)+')'
    assert env['rho_lower']=='1/4' and env['rho_upper']=='1/2'

    # Integer exponent audit separate from the generating arithmetic.
    assert 20100-22000 <= -856
    assert 3203+4025-22000 < -1
    assert 3203-22000 < -1
    assert 3206-22000 < -3
    assert 12006+8052 < 20100
    assert 2*(1+2**4002*T)**2+8*(1+2**4002*T)+16 < 32*(1+2**4002*T)**2
    assert 15*2**3201+50 < 2**3206
    assert 2**3207 < 2**4000
    assert 2**4001-4 >= 2**4000+1
    assert 2**7205+2**6405+4*2**6402 < 2**12000
    assert Q(1,2) > Q(26,1024)+Q(9,32768)
    assert Q(1,2) > Q(14,32768)
    assert Q(1024,116281) < Q(1,8)
    assert Q(20480,116281) < 2

    # Exact functional identity, not evaluation at chosen E or C.
    # K=2 lambda(F+TC)-2 PE+p-TE.
    K={('F',1):Q(2),('TC',1):Q(2),('PE',0):Q(-2),
       ('p',0):Q(1),('TE',0):Q(-1)}
    rhs={('F',1):Q(-2),('C',1):Q(-2),('PE',0):Q(2)}
    assert lin_add(derivative(derivative(K)),scale(K,-1))==rhs
    Kp=derivative(K)
    assert Kp=={('TC',1):Q(2),('p',0):Q(-1),('TE',0):Q(-1)}
    assert {k:v for k,v in Kp.items() if k[0]!='p'} == {('TC',1):Q(2),('TE',0):Q(-1)}
    # This also checks K'(0)=K(0) because F(0)=PE(0)=p(0)=0.

    answer=dict(status='INDEPENDENT_STAGE3_CONSTANTS_AND_KERNEL_IDENTITIES_PASS',
       generator_not_imported=True, exact_functional_kernel_identity=True,
       identity_and_scope_consistency=True, first_period_envelope_consistency=True,
       note='Supports the written analytic proof. No numerical ODE or global spacetime existence test.')
    target=directory/'verification/INDEPENDENT_STAGE3_CHECK.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(answer,indent=2)+'\n')
    print(json.dumps(answer,indent=2))

if __name__=='__main__':
    if not __debug__:raise SystemExit('Do not disable assertions.')
    audit(sys.argv[1])
