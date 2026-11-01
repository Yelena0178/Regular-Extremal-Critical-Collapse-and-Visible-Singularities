"""A posteriori continuous-radius barrier for canonical smooth AF profiles.

No numerical ODE error estimate is trusted: proposed cubic barriers are checked
by outward interval inequalities. Arithmetic assumptions: IEEE binary64 basic
operations and sqrt with gradual underflow, CPython Decimal correctly rounded
exp. No future spacetime or original-seed transfer is certified here.
"""
import json
import math
import time
from decimal import Decimal, localcontext
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
import numpy as np
from interval_transport_grid import V, down, up


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


def exp_point(x):
    # Decimal.exp is correctly rounded to nearest; adjacent Decimal numbers
    # enclose its exact value. Float conversion is checked against that bound.
    if x < -800:
        return 0., float(np.nextafter(0., np.inf))
    with localcontext() as ctx:
        ctx.prec = 60
        y = Decimal.from_float(float(x)).exp()
        lo, hi = y.next_minus(), y.next_plus()
        a, b = float(lo), float(hi)
        if Decimal.from_float(a) > lo:
            a = math.nextafter(a, -math.inf)
        if Decimal.from_float(b) < hi:
            b = math.nextafter(b, math.inf)
    return max(0., a), b


def exp_interval(x):
    return V(exp_point(float(x.lo))[0], exp_point(float(x.hi))[1])


def step_box(a, b):
    """Enclose H and dH/dt, including the flat endpoints, 0<=a<b<=1."""
    require(0 <= a < b <= 1, 'invalid normalized interval')
    if a >= .5:
        H, Hp = step_box(1-b, 1-a)
        return 1-H, Hp
    require(b <= .5, 'split at t=1/2')
    if a == 0:
        t = V(b)
        E = exp_interval(-1/t+1/(1-t))
        # For b<=1/2, t^-2 exp(-1/t) increases on (0,b].
        hp = E*(1/(t*t)+1/((1-t)*(1-t)))
        return V(0., float((E/(1+E)).hi)), V(0., float(hp.hi))
    t = V(a, b)
    E = exp_interval(-1/t+1/(1-t))
    H = E/(1+E)
    Hp = E/((1+E)*(1+E))*(1/(t*t)+1/((1-t)*(1-t)))
    return H, Hp


def step_grid(n):
    require(n >= 2 and n & (n-1) == 0, 'dyadic subdivision required')
    boxes = [step_box(j/n, (j+1)/n) for j in range(n)]
    return (V(np.array([float(a.lo) for a, b in boxes]), np.array([float(a.hi) for a, b in boxes])),
            V(np.array([float(b.lo) for a, b in boxes]), np.array([float(b.hi) for a, b in boxes])))


def square(x):
    lo = np.minimum(x.lo*x.lo, x.hi*x.hi)
    hi = np.maximum(x.lo*x.lo, x.hi*x.hi)
    lo = np.where((x.lo <= 0) & (x.hi >= 0), 0., np.maximum(0., down(lo)))
    return V(lo, up(hi))


def sqrt(x):
    require(np.all(x.lo > 0), 'sqrt domain')
    return V(down(np.sqrt(x.lo)), up(np.sqrt(x.hi)))


def translate(jet, center, left, length):
    """Exact-input polynomial in normalized segment t, with interval coefficients."""
    a, b, c, d = [V(row) for row in jet]
    z = V(left)-V(center)
    return [a+z*(b+z*(c+z*d)), length*(b+z*(2*c+3*z*d)),
            length*length*(c+3*z*d), length*length*length*d]


def polynomial(coefficients, t):
    value = coefficients[-1]
    for c in coefficients[-2::-1]:
        value = c+t*value
    return value


def fields(segment, t, H, Hp):
    left, right, ca, cb, ja, jb = segment
    length = V(right)-V(left)
    a = translate(ja, ca, left, length)
    b = translate(jb, cb, left, length)
    diff = [bb-aa for aa, bb in zip(a, b)]
    # Keep b-a as a polynomial; evaluating two nearly equal functions separately
    # would destroy the cancellation that makes the blend derivatives small.
    tt = V(t.lo[:, None], t.hi[:, None])
    hh, hp = V(H.lo[:, None], H.hi[:, None]), V(Hp.lo[:, None], Hp.hi[:, None])
    value = polynomial(a, tt)+hh*polynomial(diff, tt)
    deriv = (polynomial([a[1], 2*a[2], 3*a[3]], tt)
             +hh*polynomial([diff[1], 2*diff[2], 3*diff[3]], tt)
             +hp*polynomial(diff, tt))/length
    return value, deriv


def segments(data):
    r, jets = data['r'], data['jets']
    require(r.ndim == 1 and len(r) >= 2 and np.all(np.isfinite(r))
            and np.all(np.diff(r) > 0), 'profile knots')
    require(jets.shape == (len(r), 4, 5) and np.all(np.isfinite(jets)), 'profile jets')
    z = np.zeros_like(jets[0])
    cfirst, clast = z.copy(), z.copy()
    cfirst[0], clast[0] = jets[0, 0], jets[-1, 0]
    inner, left, right, outer = data['bounds']
    require(np.all(np.isfinite(data['bounds'])) and 0 < inner < left < r[0]
            and r[-1] < right < outer, 'profile cap/tail bounds')
    result = [(inner, left, inner, r[0], z, cfirst),
              (left, r[0], r[0], r[0], cfirst, jets[0])]
    result.extend((a, b, a, b, ja, jb) for a, b, ja, jb in zip(r[:-1], r[1:], jets[:-1], jets[1:]))
    result.extend([(r[-1], right, r[-1], r[-1], jets[-1], clast),
                   (right, outer, r[-1], outer, clast, z)])
    return result


def prepare(source, output, pieces=32, parameter=Fraction(1)):
    from scipy.integrate import solve_ivp
    from rotating_af_numeric import SmoothFreeProfile
    from constraint_contraction import rhs
    report = json.loads(source.read_text(encoding='utf-8'))
    with np.load(source.with_suffix('.npz')) as data:
        smooth = SmoothFreeProfile(dict(data), report['depth'])
    jets = np.stack([smooth.jets[..., 0].real, smooth.jets[..., 0].imag,
                     smooth.jets[..., 1].real, smooth.jets[..., 1].imag,
                     smooth.jets[..., 2].real], axis=-1)
    data = dict(r=smooth.r, jets=jets, bounds=np.array([smooth.inner,
        smooth.r[0]-smooth.hleft, smooth.r[-1]+smooth.hright, smooth.outer]))
    fs, dfs = [], []
    state = np.array([0., 1.])
    for left, right, *_ in segments(data):
        sol = solve_ivp(lambda r, y: rhs(r, y, smooth.profile, float(parameter)), (left, right), state,
                        method='DOP853', rtol=2e-12, atol=2e-14,
                        max_step=(right-left)/pieces, dense_output=True)
        require(sol.success, 'proposal integration')
        radii = np.linspace(left, right, pieces+1)
        states = sol.sol(radii).T
        fs.append(states[:, 1])
        dfs.append([rhs(r, y, smooth.profile, float(parameter))[1] for r, y in zip(radii, states)])
        state = states[-1]
    # Shared values and slopes are forced identical, so the canonical real
    # Hermite function is C1 even if dense-output endpoint rounding differs.
    fs, dfs = np.array(fs), np.array(dfs)
    fs[1:, 0] = fs[:-1, -1]
    dfs[1:, 0] = dfs[:-1, -1]
    np.savez_compressed(output, **data, f=fs, df=dfs)


def charge_cells(qprime, length, Qlo, Qhi):
    increments = qprime*length
    lows, highs = np.empty_like(increments.lo), np.empty_like(increments.hi)
    for j, (a, b) in enumerate(zip(increments.lo, increments.hi)):
        # At an intermediate radius, displacement ranges over [0,h].
        lows[j] = math.nextafter(Qlo+min(0., float(a)), -math.inf)
        highs[j] = math.nextafter(Qhi+max(0., float(b)), math.inf)
        Qlo = math.nextafter(Qlo+float(a), -math.inf)
        Qhi = math.nextafter(Qhi+float(b), math.inf)
    return V(lows, highs), Qlo, Qhi


def barrier(coeff_f, coeff_df, length, n, epsilon):
    pieces = len(coeff_f)-1
    require(n % pieces == 0, 'subdivision must resolve Hermite pieces')
    sub = n//pieces
    t = V(np.arange(sub)/sub, np.arange(1, sub+1)/sub)
    h = length/pieces
    low, high, dlo, dhi = [], [], [], []
    for a, b, da, db in zip(coeff_f[:-1], coeff_f[1:], coeff_df[:-1], coeff_df[1:]):
        c = [V(a)-epsilon, h*da, 3*(V(b)-V(a))-h*(2*V(da)+V(db)),
             2*(V(a)-V(b))+h*(V(da)+V(db))]
        val = polynomial(c, t)
        der = polynomial([c[1], 2*c[2], 3*c[3]], t)/h
        low.extend(val.lo); high.extend(val.hi); dlo.extend(der.lo); dhi.extend(der.hi)
    return V(np.array(low), np.array(high)), V(np.array(dlo), np.array(dhi))


def certify(input_path, output, n=4096, epsilon=1/4096, parameter=Fraction(1)):
    start = time.monotonic()
    with np.load(input_path) as raw:
        data = dict(raw)
    segs = segments(data)
    parameter = Fraction(parameter)
    require(parameter >= 0, 'negative profile parameter')
    scale = V.rational(parameter)
    require(data['f'].shape == data['df'].shape and data['f'].shape[0] == len(segs)
            and data['f'].shape[1] >= 2 and np.all(np.isfinite(data['f']))
            and np.all(np.isfinite(data['df'])), 'nonfinite/malformed barrier')
    require(data['f'][0, 0]-epsilon <= 1 and epsilon > 0, 'initial lower barrier')
    require(np.array_equal(data['f'][1:, 0], data['f'][:-1, -1]), 'barrier continuity')
    H, Hp = step_grid(n)
    t = V(np.arange(n)/n, np.arange(1, n+1)/n)
    Qlo = Qhi = 0.
    min_f, min_gap = math.inf, math.inf
    records = []
    status = 'PASS'
    for i, segment in enumerate(segs):
        left, right, *_ = segment
        length = V(right)-V(left)
        r = V(left)+length*t
        val, der = fields(segment, t, H, Hp)
        if parameter != 1:
            val, der = scale*val, scale*der
        pr, pi, cr, ci, ell = [val[:, j] for j in range(5)]
        gr, gi = der[:, 0], der[:, 1]
        qprime = V.rational('3/5')*r*r*(pi*cr-pr*ci)
        charge, Qlo, Qhi = charge_cells(qprime, length/n, Qlo, Qhi)
        lower, lower_prime = barrier(data['f'][i], data['df'][i], length, n, V(epsilon))
        require(np.all(np.isfinite(val.lo)) and np.all(np.isfinite(val.hi))
                and np.all(np.isfinite(der.lo)) and np.all(np.isfinite(der.hi))
                and np.all(np.isfinite(lower.lo)) and np.all(np.isfinite(lower.hi))
                and np.all(np.isfinite(lower_prime.lo)) and np.all(np.isfinite(lower_prime.hi))
                and math.isfinite(Qlo) and math.isfinite(Qhi), 'nonfinite field or barrier enclosure')
        if np.any(lower.lo <= 0):
            status = 'FAIL: proposed lower barrier is not positive'
            records.append(dict(segment=i, lower_f=float(min(lower.lo))))
            break
        b = r*ell
        D = lower+square(b)
        root = sqrt(D)
        S = square(cr)+square(ci)+square(gr)+square(gi)
        J = cr*gr+ci*gi
        # Signed form is exact; interval evaluation handles all signs of ell.
        energy = r*r*(D*S+2*b*root*J)/2
        F = (1-lower)/r-square(charge)/(r*r*r)-2*energy/r
        gap = F-lower_prime
        require(np.all(np.isfinite(gap.lo)) and np.all(np.isfinite(gap.hi)), 'nonfinite comparison')
        here_f, here_gap = float(min(lower.lo)), float(min(gap.lo))
        min_f, min_gap = min(min_f, here_f), min(min_gap, here_gap)
        records.append(dict(segment=i, r_left=float(left), r_right=float(right),
            lower_f=here_f, comparison_gap=here_gap, Q_lower=Qlo, Q_upper=Qhi))
        if here_gap <= 0:
            status = 'FAIL: comparison inequality not certified'
            break
    tail = None
    if status == 'PASS':
        outer = V(data['bounds'][-1])
        fend = V(data['f'][-1, -1])-V(epsilon)
        require(0 < float(fend.lo) and float(fend.hi) < 1, 'terminal barrier range')
        qmax = V(max(abs(Qlo), abs(Qhi)))
        # Worst RN continuation for f(out)>=fend and |Q|<=qmax. Its derivative
        # is positive on [out,infinity) if the following numerator is positive.
        numerator = square(outer)*(1-fend)-square(qmax)
        require(float(numerator.lo) > 0, 'RN lower continuation monotonicity')
        tail = dict(lower_f=float(fend.lo), derivative_numerator_lower=float(numerator.lo))
    report = dict(status=status, input=input_path.name,
        profile_parameter=dict(numerator=parameter.numerator, denominator=parameter.denominator),
        input_sha256=sha256(input_path.read_bytes()).hexdigest(), subdivisions_per_segment=n,
        epsilon=epsilon, segments_total=len(segs), segments_checked=len(records),
        minimum_certified_lower_f=min_f, minimum_comparison_gap=min_gap,
        final_charge_enclosure=[Qlo, Qhi], tail=tail, records=records,
        continuous_initial_positivity_certified=status == 'PASS',
        arithmetic_assumptions=['IEEE754 binary64 correctly rounded basic operations and sqrt',
                                'gradual underflow', 'CPython Decimal correctly rounded exp'],
        original_seed_preserved=False, early_future_screen_certified=False,
        critical_three_branch_theorem=False, elapsed_seconds=time.monotonic()-start)
    folder = Path(__file__).resolve().parent
    report['source_sha256'] = {name: sha256((folder/name).read_bytes()).hexdigest()
        for name in ['certify_rotating_af_barrier.py', 'interval_transport_grid.py']}
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('records', 'source_sha256')}, indent=2), flush=True)
    if status != 'PASS':
        print(json.dumps(records[-1]), flush=True)
    return report


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--subdivisions', type=int, default=4096)
    parser.add_argument('--parameter', type=Fraction, default=Fraction(1))
    args = parser.parse_args()
    if args.prepare:
        prepare(args.input, args.output, parameter=args.parameter)
    else:
        result = certify(args.input, args.output, args.subdivisions, parameter=args.parameter)
        if result['status'] != 'PASS':
            raise SystemExit(1)
