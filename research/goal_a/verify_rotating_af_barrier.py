"""Independent algebra and high-precision containment checks for A-AF05."""
from fractions import Fraction
from pathlib import Path
from hashlib import sha256
import json
import math
import numpy as np
import mpmath as mp
import sympy as sy
from certify_rotating_af_barrier import (require, exp_point, step_box, fields,
                                         segments, charge_cells, barrier, V)


def contain(box, value, label):
    require(mp.mpf(float(box.lo)) <= value <= mp.mpf(float(box.hi)), label)


def real_step(t):
    if t == 0:
        return mp.mpf(0), mp.mpf(0)
    if t == 1:
        return mp.mpf(1), mp.mpf(0)
    a, b = mp.exp(-1/t), mp.exp(-1/(1-t))
    h = a/(a+b)
    hp = a*b/(a+b)**2*(1/t**2+1/(1-t)**2)
    return h, hp


def real_poly(jet, center, r):
    z = r-mp.mpf(float(center))
    coefficients = [[mp.mpf(float(x)) for x in row] for row in jet]
    value, derivative = [], []
    for j in range(5):
        a, b, c, d = [row[j] for row in coefficients]
        value.append(a+z*b+z*z*c+z*z*z*d)
        derivative.append(b+2*z*c+3*z*z*d)
    return value, derivative


def exact_algebra():
    f, b, r, q, R, B, U = sy.symbols('f b r q R B U', real=True, positive=True)
    a, c, d, e = sy.symbols('a c d e', real=True)
    S, J = a*a+c*c+d*d+e*e, a*d+c*e
    D = f+b*b
    signed = r*r*(D*S+2*b*sy.sqrt(D)*J)/2
    squares = r*r*((D+b*sy.sqrt(D))*((a+d)**2+(c+e)**2)
                    +(D-b*sy.sqrt(D))*((a-d)**2+(c-e)**2))/4
    require(sy.simplify(signed-squares) == 0, 'positive energy decomposition')
    require(sy.simplify(sy.diff(signed, f)-r*r*(S+b*J/sy.sqrt(D))/2) == 0,
            'monotone scalar equation derivative')
    tail = 1-R*(1-B)/r-U**2/(R*r)+U**2/r**2
    require(sy.simplify(tail.subs(r, R)-B) == 0, 'tail endpoint')
    require(sy.simplify(sy.diff(tail, r).subs(r, R)-(R*R*(1-B)-U*U)/R**3) == 0,
            'tail derivative numerator')
    require(Fraction(3, 8)**800 < Fraction(1, 2)**1074, 'underflow shortcut rational proof')
    return 5


def main():
    mp.mp.dps = 150
    count = exact_algebra()
    # Test exact dyadic points, including the normal/subnormal transition.
    for x in [-1000., -800., -799., -745., -744., -100., -1., 0., .25, 1.]:
        lo, hi = exp_point(x)
        contain(V(lo, hi), mp.exp(mp.mpf(x)), 'exponential enclosure')
    checked_steps = 0
    for n in (32, 4096):
        bins = [0, 1, 2, n//4, n//2-1, n//2, n-3, n-2, n-1]
        for j in bins:
            H, Hp = step_box(j/n, (j+1)/n)
            for theta in (0, Fraction(1, 3), Fraction(2, 3), 1):
                t = (mp.mpf(j)+mp.mpf(theta.numerator)/theta.denominator)/n if isinstance(theta, Fraction) else mp.mpf(j+theta)/n
                h, hp = real_step(t)
                contain(H, h, 'flat step value')
                contain(Hp, hp, 'flat step derivative')
                checked_steps += 1
    folder = Path(__file__).resolve().parent
    checked_fields, negative_controls = 0, 0
    source_files = ['verify_rotating_af_barrier.py', 'certify_rotating_af_barrier.py', 'interval_transport_grid.py']
    for label in ('A020_W8', 'A030_W4'):
        name = 'ROTATING_CANONICAL_'+label+'_2026-10-21.npz'
        source_files.append(name)
        with np.load(folder/name) as raw:
            data = dict(raw)
        segs = segments(data)
        for index in [0, 1, 7, 100, 400, 600, 700, len(segs)-2, len(segs)-1]:
            segment = segs[index]
            left, right, ca, cb, ja, jb = segment
            for bin_index in (0, 256, 2047, 2048, 4095):
                tlo, thi = bin_index/4096, (bin_index+1)/4096
                H, Hp = step_box(tlo, thi)
                val, der = fields(segment, V(np.array([tlo]), np.array([thi])),
                                  V(np.array([float(H.lo)]), np.array([float(H.hi)])),
                                  V(np.array([float(Hp.lo)]), np.array([float(Hp.hi)])))
                t = (mp.mpf(bin_index)+mp.mpf(1)/3)/4096
                length = mp.mpf(float(right))-mp.mpf(float(left))
                rr = mp.mpf(float(left))+length*t
                a, ap = real_poly(ja, ca, rr)
                b, bp = real_poly(jb, cb, rr)
                h, hp = real_step(t)
                for j in range(5):
                    contain(val[0, j], (1-h)*a[j]+h*b[j], 'canonical field')
                    contain(der[0, j], (1-h)*ap[j]+h*bp[j]+hp*(b[j]-a[j])/length,
                            'canonical radial derivative')
                    checked_fields += 2
        bad = dict(data)
        bad['r'] = data['r'][::-1]
        try:
            segments(bad)
        except ArithmeticError:
            negative_controls += 1
        else:
            raise ArithmeticError('reversed knots accepted')
        cert_name = 'ROTATING_AF_BARRIER_'+label+'_N4096_2026-10-21.json'
        source_files.append(cert_name)
        cert = json.loads((folder/cert_name).read_text(encoding='utf-8'))
        require(cert['status'] == 'PASS' and cert['continuous_initial_positivity_certified'], 'incomplete certificate')
        require(cert['segments_checked'] == len(segs), 'missing segment')
        require(Fraction(cert['minimum_certified_lower_f']) > Fraction(3, 10000)
                and Fraction(cert['tail']['lower_f']) > Fraction(3, 10000), 'common rational f lower bound')
        require(cert['input_sha256'] == sha256((folder/name).read_bytes()).hexdigest(), 'input hash drift')
        for source, digest in cert['source_sha256'].items():
            require(digest == sha256((folder/source).read_bytes()).hexdigest(), 'certificate source drift')
        require(not cert['early_future_screen_certified'] and not cert['critical_three_branch_theorem'],
                'scope upgrade rejected')
    # Signed current: upper/lower endpoints alone must not miss an interior extremum.
    cells, lo, hi = charge_cells(V(np.array([-2., 3.]), np.array([-1., 4.])), V(.25), 1., 1.)
    require(float(cells.lo[0]) <= .5 and float(cells.hi[0]) >= 1., 'negative-current cell range')
    require(float(cells.lo[1]) <= .5 and float(cells.hi[1]) >= 1.75, 'positive-current cell range')
    require(lo <= 1.25 and hi >= 1.75, 'signed current endpoint propagation')
    # A plainly invalid positive shift of the comparison curve is detectable
    # even in exact vacuum: B>1 gives F(B)<0 while B'=0.
    badB, badBp = barrier(np.array([1.01, 1.01]), np.array([0., 0.]), V(1.), 32, V(0.))
    badgap = (1-badB)/V(2., 3.)-badBp
    require(np.all(badgap.hi < 0), 'invalid vacuum barrier negative control')
    negative_controls += 1
    report = dict(status='PASS', exact_algebra_checks=count, exponential_points=10,
        high_precision_step_checks=checked_steps, high_precision_field_checks=checked_fields,
        negative_controls=negative_controls, precision_digits=mp.mp.dps,
        certificate_replay_scope='hashes, coverage and stated signs; full interval replay is a separate command',
        future_spacetime_certified=False, goal_A_proved=False,
        source_sha256={name: sha256((folder/name).read_bytes()).hexdigest() for name in source_files})
    (folder/'ROTATING_AF_BARRIER_CHECKS_2026-10-21.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'source_sha256'}, indent=2))


if __name__ == '__main__':
    main()
