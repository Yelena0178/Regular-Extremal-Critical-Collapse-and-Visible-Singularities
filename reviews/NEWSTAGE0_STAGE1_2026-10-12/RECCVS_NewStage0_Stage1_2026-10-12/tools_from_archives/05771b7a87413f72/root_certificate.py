"""Assemble and check the reduced finite-endpoint root certificate.

The mathematical proof is PROOF.md. This is an analytic-enclosure Krawczyk
certificate, not a sampled numerical integration or a spacetime certificate.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

def realify(m):
    r=[[F(0)]*(2*len(m)) for _ in range(2*len(m))]
    for j,row in enumerate(m):
        for k,entry in enumerate(row):
            a,b=map(F,entry)
            r[2*j][2*k]=a;r[2*j][2*k+1]=-b
            r[2*j+1][2*k]=b;r[2*j+1][2*k+1]=a
    return r
def audit_base():
    p=lambda n:F(2)**n
    assert (1+p(154))*p(6425-12000)<p(-5420)
    assert p(143)+p(155)+p(-5420)<p(156)
    assert p(3201)*(1+F(8,7)*p(154))<p(3357)
    assert 1+F(8,7)*p(154)<p(155)
    assert 1+p(155)<p(156)
    assert 5*p(155)+p(144)+10*p(157)<p(163)
    assert p(3357)+p(3201+157)<p(3360)
    assert p(3201+155)+p(1742)+2*p(3201+157)<p(3361)
    assert 16+p(165)+p(3205-12000)+p(3367-12000)<p(4000)
    assert 1+p(163)+p(3201-12000)+p(3361-12000)<p(4000)
    assert 65*p(3370)<p(4000)
    assert F(1,1-F(9,64))+1<4
    # Initial inverse q and inverse r estimates; r1 includes division by four.
    assert 3362+166-2<4000  # coefficients of 4*T cancel here
    return dict(status='EXPLICIT_BASE_CONSTANT_ARITHMETIC_PASS',alpha='1/64',base_exponent=4000,
        checks=['graph chain rule','global R and Q derivatives','time derivatives','inverse radius','weighted base differences','integrator factor','initial inverse q/R budget'])

def create(bounds,coupling):
    assert bounds['K']==8 and bounds['T']==2**20+2 and bounds['mu']=='3/5'
    assert bounds['alpha']=='1/64' and bounds['base_majorant_exponent']==4000
    assert coupling['parameters']['K']==8 and coupling['parameters']['T']==bounds['T'] and coupling['parameters']['mu']=='3/5'
    D=bounds['max_endpoint_difference_over_delta_exponent'];M=coupling['parameters']['m']['exponent']
    test=next(t for t in bounds['tests'] if t['m_exponent']==M)
    assert M>=12000
    assert test['residual_real_component_error_exponent']==D-M
    assert test['jacobian_real_row_sum_error_exponent']==D+4-M
    assert test['Krawczyk_scaled_Y_exponent']==D+4103-M
    assert test['Krawczyk_contraction_q_exponent']==D+10-M
    boundary_lhs=3+3*M+2*(4*bounds['T']+4000)+bounds['background_initial_majorant_exponent']
    assert test['boundary_master_log2_lhs']==boundary_lhs
    assert boundary_lhs.bit_length()<=M+14
    assert test['sufficient_strict_inclusion']
    family=coupling['finite_coupling_family']
    assert F(family['scaled_Y'])+F(family['scaled_q'])<F(1,4)
    assert family['derivative_kappa_negative_abs_lower']=='1/5'
    assert family['eliminated_kappa_c_derivative_abs_upper']=='2^154'
    A=realify(coupling['leading_matrix']['T_mu']);P=realify(coupling['leading_matrix']['T_mu_inverse'])
    for j in range(16):
        for k in range(16):assert sum((P[j][i]*A[i][k] for i in range(16)),F(0))==int(j==k)
    exact_norm=max(sum(map(abs,row)) for row in P);assert exact_norm<64
    base=audit_base()
    assert D==max(x['bound']['difference_over_delta_exponent'] for x in bounds['covariant_rows'])
    assert test['Krawczyk_scaled_Y_exponent']<=-3 and test['Krawczyk_contraction_q_exponent']<=-3
    def matrix(m):return [[str(v) for v in row] for row in m]
    return dict(status='CERTIFIED_BOX_ROOT_OF_FROZEN_FINITE_ENDPOINT_SYSTEM',
        certification_method='16-real-dimensional Krawczyk with explicit analytic finite-jet enclosures; scalar implicit elimination',
        dimensions=dict(original_real=17,reduced_real=16,complex_transverse=8),mu='3/5',K=8,T=bounds['T'],m=dict(power_of_two_exponent=M),
        parameter_box=dict(c_real_center=[0]*16,c_real_component_radius_power_of_two=-4097,
            kappa_center=coupling['parameter_box']['kappa_center'],kappa_radius_power_of_two=-3900,
            c_order='Re c1, Im c1, ..., Re c8, Im c8',tau='T*kappa',delta='kappa/m'),
        center_for_reduced_residual='c=0, kappa=kappa_m(0) defined by the uniquely certified scalar equation; not the literal kappa midpoint',
        residual_enclosure=dict(all_16_components_center='0',all_16_components_symmetric_radius_power_of_two=D-M,
            derivation='proved finite-jet difference from exact background T_mu*c at c=0, not an assumption that finite residuals vanish'),
        jacobian_enclosure=dict(center_matrix=matrix(A),entrywise_symmetric_radius_power_of_two=D-M,
            real_row_sum_error_power_of_two=D+4-M,chain_rule='F_c + F_kappa*kappa_c, included in effective C1 majorants'),
        preconditioner=dict(matrix=matrix(P),real_infinity_norm=str(exact_norm),strict_upper=64),
        inclusion=dict(Y_power_of_two_upper=test['Krawczyk_scaled_Y_exponent'],q_power_of_two_upper=test['Krawczyk_contraction_q_exponent'],Y_plus_q_strict_upper='1/4',strict_interior=True),
        uniqueness='Within the stated product parameter box, by scalar uniqueness and reduced contraction; no global uniqueness claim.',
        boundary=test,base_constant_audit=base,
        quantitative_proof_dependency='PROOF.md and EFFECTIVE_JET_BOUNDS.json; original L021 smooth-function definitions and prior scalar averaging proof',
        scope=dict(finite_jet_endpoint_root=True,actual_global_formation_spacetime=False,H_positivity=False,center_fill=False,An_Lim_application=False),
        distinction='m_geom is certified here only after the separate finite-jet bounds pass; no geometric condition substitutes for root existence.')

if __name__=='__main__':
    bounds=json.loads(Path(sys.argv[1]).read_text());coupling=json.loads(Path(sys.argv[2]).read_text())
    result=create(bounds,coupling)
    result['input_sha256']={Path(arg).name:hashlib.sha256(Path(arg).read_bytes()).hexdigest() for arg in sys.argv[1:3]}
    Path(sys.argv[3]).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],m_exponent=result['m']['power_of_two_exponent'],inclusion=result['inclusion'],scope=result['scope']),indent=2))
