"""Exact single-cell demonstration on a strong E0 approximate field.

The specified inflow errors remain hypotheses, not proven input bounds.
This is neither a full rectangle certificate nor a certified trapped sphere.
"""

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import numpy as np
from neutral_transport import (TransportConfiguration,evolve,onset_boundaries,
                               fourth_derivative,jacobian)
from rational_transport_cell import hermite_cell,verify_cell


def require(condition,message):
    if not condition:
        raise ArithmeticError(message)


def evaluate(poly,u,v):
    value = Q(0)
    for monomial,c in poly.terms.items():
        for name,power in monomial:
            c *= {'u':u,'v':v}[name]**power
        value += c
    return value


def strings(value):
    if isinstance(value,Q):
        return str(value)
    if isinstance(value,(tuple,list)):
        return [strings(v) for v in value]
    if isinstance(value,dict):
        return {k:strings(v) for k,v in value.items()}
    return value


def main():
    outgoing,incoming,p = onset_boundaries(.05)
    cfg = TransportConfiguration(steps_u=192,steps_v=192,final_u=p['v_end']/2,
                                 initial_v=p['v_cap'],final_v=31*p['v_end']/32)
    data = evolve(outgoing,incoming,cfg)
    x,F = data['state'],data['rhs']
    du,dv = data['u'][1],data['v'][1]-data['v'][0]
    xu,xv = fourth_derivative(x,0,du),fourth_derivative(x,1,dv)
    xu[...,:3],xv[...,3:] = F[...,:3],F[...,3:]
    J = jacobian(x)
    xuv = np.empty_like(x)
    xuv[...,:3] = np.einsum('...ij,...j->...i',J[...,:3,:],xv)
    xuv[...,3:] = np.einsum('...ij,...j->...i',J[...,3:,:],xu)
    hu = Q(cfg.final_u)/cfg.steps_u
    hv = (Q(cfg.final_v)-Q(cfg.initial_v))/cfg.steps_v
    polys = hermite_cell(x[-2:,-2:].tolist(),xu[-2:,-2:].tolist(),
                         xv[-2:,-2:].tolist(),xuv[-2:,-2:].tolist(),hu,hv)
    for i in (0,1):
        for j in (0,1):
            for k in range(6):
                require(evaluate(polys[k],i,j)==Q(float(x[-2+i,-2+j,k])),
                        'exact nodal value')
                require(evaluate(polys[k].partial('u'),i,j)/hu
                        ==Q(float(xu[-2+i,-2+j,k])),'exact u derivative')
                require(evaluate(polys[k].partial('v'),i,j)/hv
                        ==Q(float(xv[-2+i,-2+j,k])),'exact v derivative')
    neighbor = hermite_cell(x[-3:-1,-2:].tolist(),xu[-3:-1,-2:].tolist(),
                            xv[-3:-1,-2:].tolist(),xuv[-3:-1,-2:].tolist(),hu,hv)
    for left,right in zip(neighbor,polys):
        require(not (left.substitute({'u':1})-right.substitute({'u':0})).terms,
                'exact shared edge values')
        require(not (left.partial('u').substitute({'u':1})
                     -right.partial('u').substitute({'u':0})).terms,'exact shared edge derivative')
    M,b = [Q(1,50)]*6,[Q(1,100)]*6
    certificate = verify_cell(polys,hu,hv,M,b)
    rejected = False
    try:
        verify_cell(polys,hu,hv,M,[Q(1)]*6)
    except ArithmeticError:
        rejected = True
    require(rejected,'large unproven inflow error accepted')
    B = certificate['field_ranges']
    conditional_margin = 2*(B[5][0]-M[5])-(B[0][1]+M[0])
    folder = Path(__file__).resolve().parent
    sources = ['rational_transport_cell.py','verify_rational_transport_cell.py',
               'neutral_transport.py','neutral_onset_input.py','verify_horizon_seed.py',
               'verify_null_infinity_algebra.py','FIRST_JET_CHECKS_2026-10-16.json',
               'RATIONAL_GOURSAT_CERTIFICATION.md']
    result = {'evidence':'exact_single_cell_conditional_on_unproved_inflow_errors',
              'goal_A_proved':False,'full_candidate_PDE_certified':False,
              'actual_strict_trapping_certified':False,
              'cell_index':[191,191],'rational_hu':str(hu),'rational_hv':str(hv),
              'radius':list(map(str,M)),'assumed_entire_inflow_edge_errors':list(map(str,b)),
              'certificate':strings(certificate),'conditional_2m_minus_r_lower':str(conditional_margin),
              'bad_inflow_error_rejected':rejected,'exact_shared_C1_edge_checked':True,
              'source_sha256':{s:hashlib.sha256((folder/s).read_bytes()).hexdigest() for s in sources}}
    output = folder/'RATIONAL_TRANSPORT_CELL_CHECKS_2026-10-16.json'
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'consistency':'pass','scope':result['evidence'],
                      'residual_bounds':[float(v) for v in certificate['residual_bounds']],
                      'strict_margins':[float(v) for v in certificate['strict_margins']],
                      'report':output.name}),flush=True)


if __name__ == '__main__':
    main()
