"""Independent boundary audits and exact analytic-budget checks for R=10."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

import numpy as np

from new_shape_constraints import rational_certificate, PHI, RHO, RADIUS, COUPLING
from new_shape_screen import geometry, reference, boundary_envelope
from graded_transport import mesh, v_derivative, evolve, derivatives
from thin_boundary_certificate import trig
from certify_onset_boundary import hermite
from rational_transport_cell import hermite_cell, cell_quantities
from interval_transport_grid import V, coefficients, cell_bounds
from verify_interval_transport_grid import require, contains
from verify_null_infinity_algebra import sym


def analytic_checks():
    s, a, t = sym('s'), sym('a'), sym('t')
    D = (1+2*s)*(1-2*s)
    direct = (1-a*t)*(1-2*s)-2*a*(1-t)*D+(a*a-a*t)*(1+2*s)
    simplified = (1-2*s)-2*a*D+a*a*(1+2*s)-8*a*s*s*t
    require(not (direct-simplified).terms, 'general rho charge-energy primitive')
    # Powers of two deliberately leave ample room for all rational roundings.
    df, dp, dc, dq = Q(1, 2**62), Q(1, 2**54), Q(1, 2**50), Q(1, 2**45)
    require(128*df+Q(1, 2**62) < dp, 'derivative perturbation budget')
    require(3*512*df+Q(1, 2**84) < dc, 'charge-integral perturbation budget')
    require(32*dc <= dq, 'normalized charge perturbation')
    dh0 = 4*df+8*dp
    dh_integral = 3*dq*2**14+2*df*2**26
    require(dh0+dh_integral < Q(1, 2**26), 'uniform H perturbation')
    require(Q(1, 512)-Q(1, 2**26) > Q(1, 1024), 'smoothed H margin')
    ds = 4*dc  # |k'|>1/4 on the complete s interval.
    da = 2*ds+RADIUS*df
    dL = Q(5, 2)*ds+2*RADIUS*dp
    require(da < Q(1, 2**46) and dL < Q(1, 2**45), 'root geometry displacement')
    af, lf, ar, length, box = geometry()
    # geometry() has already checked the C0 root, here also leave room for
    # explicit smoothing and the finite arithmetic used by its enclosure.
    from new_shape_constraints import trigonometric_bounds
    c, sn = trigonometric_bounds(PHI)
    K = PHI*c*c*(1-RHO**2)/2
    root = (COUPLING*RADIUS*K)**2/(1+(COUPLING*RADIUS*K)**2)
    a0 = RADIUS*RHO*c*(c-root*sn/PHI)
    L0 = 2*RADIUS*RHO*c*(PHI*sn+root*c)
    require(ar.lo < a0.lo-da and a0.hi+da < ar.hi, 'smoothed cap inside screen box')
    require(length.lo < L0.lo-dL and L0.hi+dL < length.hi, 'smoothed length inside screen box')
    physical_width = 2*RADIUS*129*Q(1, 2**200)
    require(physical_width < Q(1, 2**100), 'physical ramp width covered')
    # Coefficient of I_g^4 in the four-dimensional real transverse block.
    cabs2 = COUPLING**2/(16*RADIUS**2)
    Aabs2 = (3*COUPLING**2/(16*RADIUS**2))**2+(COUPLING/(8*RADIUS**3))**2
    block = cabs2*Aabs2*Q(4, 729)
    require(block > 0, 'new radius transverse block nondegenerate')
    return dict(general_rho_primitive_exact=True,
                smooth_H_perturbation_upper='1/2^26', smoothed_H_lower='1/1024',
                smoothed_geometry_inside_screen_box=True,
                physical_ramp_width_upper=str(physical_width),
                two_jet_real_block_I_to_four_coefficient=str(block),
                nonlinear_IFT_thresholds_effective=False)


def main():
    base = Path(__file__).resolve().parent
    constraints = rational_certificate()
    analytic = analytic_checks()
    af, L, ar, length, _ = geometry()
    cap, end = 2*af, 2*af+Q(31, 32)*L
    v = mesh(cap, end, 32)
    out, inc = reference(af, L)
    values = np.array([out(float(w)) for w in v])
    slopes = v_derivative(values[None], v)[0]
    errors, _ = boundary_envelope(values, slopes, v, af, ar, length)
    count = 0
    for a0, L0 in [(ar.lo,length.lo),(ar.lo,length.hi),(ar.hi,length.lo),
                    (ar.hi,length.hi),(af,L)]:
        q = PHI/L0
        for j in [0, 1, 12, 20, len(v)-2]:
            h = v[j+1]-v[j]
            polys = [hermite(values[j,k],values[j+1,k],slopes[j,k],slopes[j+1,k],h)
                     for k in range(3)]
            for tau in (Q(1,3),Q(1,2),Q(1)):
                at = v[j]+h*tau
                c, s = trig(q*(at-cap))
                r = a0*c+s/(2*q)
                for k, true in enumerate((r,r/(at+2*(a0-af)),r*q)):
                    poly = sum((coefficient*tau**p for p,coefficient in enumerate(polys[k])),0)
                    diff = true-poly
                    require(max(abs(diff.lo),abs(diff.hi)) <= Q(float(errors[j+1,k])),
                            'new shape boundary envelope')
                    count += 1
        require(a0/(cap+2*(a0-af)) == Q(1,2), 'physical corner kappa')
    require(ar.lo/cap != Q(1,2), 'wrong coordinate denominator negative control')
    # Check variable-width polynomial construction at the smallest, transition,
    # and far cells, on data from this candidate rather than the rejected R=5.
    u_end = Q(19,20)*cap
    data = evolve(out,inc,float(u_end),v,32)
    x = data['state']; xu,xv,xuv = derivatives(data,v)
    hu = u_end/32
    cell_records = []
    for i,j in [(3,0),(16,12),(31,len(v)-2)]:
        sl = (slice(i,i+2),slice(j,j+2)); hv = v[j+1]-v[j]
        exact = hermite_cell(x[sl].tolist(),xu[sl].tolist(),xv[sl].tolist(),xuv[sl].tolist(),hu,hv)
        pol = coefficients(x[sl],xu[sl],xv[sl],xuv[sl],V.rational(hu),V.rational(hv))
        for k, ep in enumerate(exact):
            terms = {}
            for monomial,value in ep.terms.items():
                powers = dict(monomial)
                terms[powers.get('u',0),powers.get('v',0)] = value
            for aa in range(4):
                for bb in range(4):
                    require(contains(pol[0,0,k,aa,bb],terms.get((aa,bb),Q(0))), 'new shape exact coefficient')
        B,delta = cell_bounds(pol,V.rational(hu),V.rational(hv))
        Br,dr,_ = cell_quantities(exact,hu,hv,[Q(1,1000)]*6)
        for k in range(6):
            require(Q(float(B.lo[0,0,k])) <= Br[k][0] and Q(float(B.hi[0,0,k])) >= Br[k][1],
                    'new shape exact Bernstein enclosure')
            require(Q(float(delta[0,0,k])) >= dr[k], 'new shape exact residual bound')
        cell_records.append([i,j])
    result = dict(status='PASS', analytic=analytic, independent_boundary_point_comparisons=count,
                  independent_exact_cells=cell_records, exact_coefficient_comparisons=288,
                  wrong_denominator_rejected=True, continuous_s_partition_cells=constraints['partition_cells'],
                  goal_A_proved=False)
    names = ['verify_new_shape.py','new_shape_constraints.py','new_shape_screen.py',
             'verify_horizon_seed.py','rational_transport_cell.py','interval_transport_grid.py',
             'graded_transport.py','thin_boundary_certificate.py','thin_parameter_boundary.py',
             'certify_onset_boundary.py','verify_null_infinity_algebra.py','NEW_SHAPE_CONSTRAINTS.md']
    result['source_sha256'] = {name:sha256((base/name).read_bytes()).hexdigest() for name in names}
    (base/'NEW_SHAPE_AUDIT_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k != 'source_sha256'},indent=2))


if __name__ == '__main__':
    main()
