"""Finite pre-axis screen for the new R=10 shape; never a global certificate.

The approximate reference may be C0 at the vacuum corner. The proved
boundary envelope covers actual positive-width smooth onsets instead.
"""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
import math
from pathlib import Path
import time
import platform

import numpy as np
from scipy.integrate import solve_ivp

from new_shape_constraints import PHI, RHO, RADIUS, COUPLING, trigonometric_bounds
from verify_horizon_seed import I, up as rational_up
from thin_parameter_boundary import trig_box
from certify_onset_boundary import add, mul, scale, bounds, hermite, exp_bound
from graded_transport import mesh, evolve, derivatives, propagate
from interval_transport_grid import V, coefficients, cell_bounds
from verify_interval_transport_grid import arithmetic_checks


def geometry():
    c, s = trigonometric_bounds(PHI)
    K = PHI*c*c*(1-RHO**2)/2
    root = (COUPLING*RADIUS*K)**2/(1+(COUPLING*RADIUS*K)**2)
    a = RADIUS*RHO*c*(c-root*s/PHI)
    L = 2*RADIUS*RHO*c*(PHI*s+root*c)
    af, lf = Q(float((a.lo+a.hi)/2)), Q(float((L.lo+L.hi)/2))
    ar, length = I(af-Q(1, 2**42), af+Q(1, 2**42)), I(lf-Q(1, 2**42), lf+Q(1, 2**42))
    if not (ar.lo < a.lo <= a.hi < ar.hi and length.lo < L.lo <= L.hi < length.hi):
        raise ArithmeticError('auxiliary root outside geometry box')
    return af, lf, ar, length, dict(
        auxiliary_s_interval=[str(root.lo), str(root.hi)],
        cap_radius_interval=[str(ar.lo), str(ar.hi)],
        onset_length_interval=[str(length.lo), str(length.hi)],
        auxiliary_geometry_strictly_inside=True)


def reference(af, length):
    a, cap, L, q = float(af), float(2*af), float(length), float(PHI/length)
    def radius(v):
        t = v-cap
        return (a*np.cos(q*t)+np.sin(q*t)/(2*q),
                -a*q*np.sin(q*t)+np.cos(q*t)/2)
    def z_rhs(v, z):
        r, lam = radius(v)
        return -q-(1/v-lam/r)*z
    zsol = solve_ivp(z_rhs, (cap, cap+L), [0.], method='DOP853',
                     rtol=2e-12, atol=2e-14, max_step=L/384, dense_output=True)
    if not zsol.success:
        raise ArithmeticError(zsol.message)
    def outgoing(v):
        r, lam = radius(v)
        return np.array([r, r/v, 0. if v == cap else r*q,
                         -v/(4*r), float(zsol.sol(v)[0]), (r-v*lam)/2])
    def incoming(u):
        return np.array([a-u/2, .5, 0., -.5, 0., 0.])
    return outgoing, incoming


def boundary_envelope(values, slopes, v, af, ar, length):
    cap, width = 2*af, Q(1, 2**100)
    T = v[-1]-cap
    q = PHI/length
    # chi + y chi' <= 9 follows from 0<=chi<=1 and |chi'|<=8.
    qmax = 9*q.hi
    Rmax = ar.hi+T/2
    energy = rational_up(exp_bound(max(Q(1), qmax*qmax)*T).hi
                         *Rmax*(qmax*qmax+q.hi*q.hi)*width)
    if not (width < v[1]-cap and T < length.lo-width):
        raise ArithmeticError('thin layer or charging endpoint enters wrong cell')
    if ar.lo*(1-(q.hi*T)**2/2) <= energy:
        raise ArithmeticError('boundary radius not positive')
    shift = 2*(ar-af)
    result = np.zeros((len(v), 6))
    for j, (left, right) in enumerate(zip(v, v[1:])):
        h, mid = right-left, (left+right)/2-cap
        c, s = trig_box(q*mid)
        rr, rp = ar*c+s/(2*q), -ar*q*s+c/2
        t = [-Q(1, 2), Q(1)]
        t2, t3 = mul(t, t), mul(mul(t, t), t)
        model = add(add([rr], scale(t, rp*h)),
                    add(scale(t2, -q*q*rr*h*h/2), scale(t3, -q*q*rp*h**3/6)))
        remainder = q.hi**4*Rmax*h**4/384
        polynomials = [hermite(values[j, k], values[j+1, k], slopes[j, k], slopes[j+1, k], h)
                       for k in range(3)]
        dr = bounds(add(model, scale(polynomials[0], -1)))
        er = max(abs(dr.lo), abs(dr.hi))+remainder+energy
        dk = bounds(add(model, scale(mul([I(left)+shift, h], polynomials[1]), -1)))
        ek = (max(abs(dk.lo), abs(dk.hi))+remainder+energy)/(left+shift.lo)
        if j == 0:
            bt = bounds(polynomials[2])
            maximum = qmax*(ar.hi+h/2+energy)
            et = max(abs(bt.lo), abs(bt.hi), abs(maximum-bt.lo), abs(maximum-bt.hi))
        else:
            dt = bounds(add(scale(model, q), scale(polynomials[2], -1)))
            et = max(abs(dt.lo), abs(dt.hi))+q.hi*(remainder+energy)
        result[j+1, :3] = [math.nextafter(float(rational_up(e)), math.inf) for e in (er, ek, et)]
    return result, dict(smooth_width_upper=str(width), q_upper=str(qmax),
                        radial_C1_perturbation_upper=str(energy),
                        parameter_coordinate='V=v_reference+2*(a-a_reference)',
                        maximum_boundary_errors=result.max(axis=0).tolist())


def main(steps=128):
    if steps < 16:
        raise ValueError('at least 16 cells per regular coordinate are required')
    started = time.monotonic()
    folder = Path(__file__).resolve().parent
    result = dict(status='FAIL', evidence='finite_pre_axis_outward_interval_screen',
                  target_radius='10', coupling='3/5', steps_u=steps,
                  finite_domain_nontrapping_certified=False,
                  whole_future_nontrapping_certified=False,
                  full_AF_Cauchy_realization=False, goal_A_proved=False)
    try:
        with np.errstate(over='raise', invalid='raise', divide='raise', under='ignore'):
            result['arithmetic_checks'] = arithmetic_checks()
            af, L, ar, length, box = geometry()
            cap, u_end, v_end = 2*af, Q(19, 20)*(2*af), 2*af+Q(31, 32)*L
            if u_end >= 2*ar.lo:
                raise ArithmeticError('parameter axis enters rectangle')
            v = mesh(cap, v_end, steps)
            nv = len(v)-1
            result.update(steps_v=nv, geometry=box, exact_rectangle={
                'u_max': str(u_end), 'v_min': str(cap), 'v_max': str(v_end)})
            print(json.dumps(dict(stage='new_shape_reference',steps_u=steps,steps_v=nv)), flush=True)
            out, inc = reference(af, L)
            data = evolve(out, inc, float(u_end), v, steps)
            x = data['state']
            xu, xv, xuv = derivatives(data, v)
            if not all(np.isfinite(a).all() for a in (x, xu, xv, xuv)):
                raise ArithmeticError('nonfinite reference')
            if not np.all(x[:, 0, 3:] == [-.5, 0., 0.]) or not np.all(xu[:, 0, 3:] == 0):
                raise ArithmeticError('incoming vacuum trace mismatch')
            boundary, edge = boundary_envelope(x[0], xv[0], v, af, ar, length)
            result['boundary'] = edge
            hu = V.rational(u_end/steps)
            widths = [V.rational(b-a) for a, b in zip(v, v[1:])]
            hv = V(np.array([float(h.lo) for h in widths]), np.array([float(h.hi) for h in widths]))
            low = np.empty((steps, nv, 6)); high = np.empty_like(low); delta = np.empty_like(low)
            for first in range(0, steps, 8):
                last = min(steps, first+8); sl = slice(first, last+1)
                c = coefficients(x[sl], xu[sl], xv[sl], xuv[sl], hu, hv[:, None])
                B, d = cell_bounds(c, hu, hv[:, None, None])
                low[first:last], high[first:last], delta[first:last] = B.lo, B.hi, d
                if first % 32 == 0:
                    print(json.dumps(dict(stage='new_shape_cell_bounds', rows_complete=last)), flush=True)
            radii, report = propagate(low, high, delta, hu, hv, boundary,
                lambda diagonal, margin: print(json.dumps(dict(stage='new_shape_propagation',
                    diagonal=diagonal, margin=margin)), flush=True))
            M = V(radii[1:, 1:])
            actual = V((V(low)-M).lo, (V(high)+M).hi)
            gap = actual[..., 0]-2*actual[..., 5]
            lam = actual[..., 1]*(1-2*actual[..., 5]/actual[..., 0])
            if np.min(gap.lo) <= 0 or np.min(lam.lo) <= 0:
                raise ArithmeticError('full-cell nontrapping signs not certified')
            result.update(status='PASS', **report, finite_domain_nontrapping_certified=True,
                          entire_rectangle_r_minus_2m_lower=float(np.min(gap.lo)),
                          entire_rectangle_lambda_lower=float(np.min(lam.lo)),
                          maximum_error_radii=np.max(radii, axis=(0, 1)).tolist(),
                          original_smooth_charge_root_transferred=False,
                          arithmetic_assumptions=['IEEE-754 binary64 correctly rounded basic arithmetic',
                                                  'gradual underflow', 'correct nextafter',
                                                  'exact Python integer and Fraction arithmetic'],
                          array_sha256={name: sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
                              for name, a in [('nodes', x), ('du', xu), ('dv', xv), ('duv', xuv),
                                              ('low', low), ('high', high), ('residual', delta), ('radii', radii)]})
    except (ArithmeticError, ValueError, FloatingPointError) as error:
        result['failure'] = str(error)
    result['elapsed_seconds'] = time.monotonic()-started
    result['runtime'] = dict(python=platform.python_version(), numpy=np.__version__)
    sources = ['new_shape_screen.py', 'new_shape_constraints.py', 'verify_horizon_seed.py',
               'thin_parameter_boundary.py', 'thin_boundary_certificate.py', 'certify_onset_boundary.py',
               'graded_transport.py', 'interval_transport_grid.py', 'verify_interval_transport_grid.py',
               'neutral_transport.py', 'RATIONAL_GOURSAT_CERTIFICATION.md', 'NEW_SHAPE_CONSTRAINTS.md']
    result['source_sha256'] = {name: sha256((folder/name).read_bytes()).hexdigest() for name in sources}
    target = folder/f'NEW_SHAPE_SCREEN_N{steps}_2026-10-17.json'
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('source_sha256', 'array_sha256')}, indent=2), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--steps', type=int, default=128)
    outcome = main(parser.parse_args().steps)
    if outcome['status'] != 'PASS':
        raise SystemExit(1)
