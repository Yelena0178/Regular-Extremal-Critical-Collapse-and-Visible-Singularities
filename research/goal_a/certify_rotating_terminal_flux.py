"""Rational enclosure of terminal transverse scalar flux, not a global solution.

Uses the same certified Raychaudhuri/Gauss tubes as the rotating seeds, adds
rigorous phase and first-transverse-transport integrals. No float acceptance.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import factorial, isqrt
from pathlib import Path
import json
import time

from certify_early_charged_constraints import bump_bounds, square, exact, display
from verify_horizon_seed import I, down, up, DEN


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def sqrt_box(value):
    require(value.lo >= 0, 'negative square root input')
    def integer_floor(x):
        return isqrt((x.numerator*DEN*DEN)//x.denominator)
    low, high = integer_floor(value.lo), integer_floor(value.hi)
    if F(high*high, DEN*DEN) < value.hi:
        high += 1
    return I(F(low, DEN), F(high, DEN))


def trig_point(angle):
    """Taylor polynomials with global derivative<=1 remainder, exact rationals."""
    angle = F(angle)
    order = 24
    cosine = sum(((-1)**j*angle**(2*j)/factorial(2*j)
                  for j in range(order+1)), F(0))
    sine = sum(((-1)**j*angle**(2*j+1)/factorial(2*j+1)
                for j in range(order+1)), F(0))
    # Derivatives of real sin/cos are bounded by one, for every real angle.
    cr = abs(angle)**(2*order+1)/factorial(2*order+1)
    sr = abs(angle)**(2*order+2)/factorial(2*order+2)
    return I(down(cosine-cr), up(cosine+cr)), I(down(sine-sr), up(sine+sr))


def phase_boxes(frequency, cells):
    step = F(frequency, cells)
    cosine, sine = trig_point(step/2)
    cd, sd = trig_point(step)
    radius = abs(step)/2
    for _ in range(cells):
        # The centers have enclosed phases; Lipschitz-1 extends over the cell.
        cb = I(max(F(-1), cosine.lo-radius), min(F(1), cosine.hi+radius))
        sb = I(max(F(-1), sine.lo-radius), min(F(1), sine.hi+radius))
        yield cb, sb
        cosine, sine = cosine*cd-sine*sd, sine*cd+cosine*sd


def distance_from_zero(box):
    return min(abs(box.lo), abs(box.hi)) if box.lo*box.hi > 0 else F(0)


def certify(amplitude, frequency, cells=2048):
    a, w, e, dt = F(amplitude), F(frequency), F(3,5), F(1,cells)
    require(cells >= 8 and cells % 2 == 0 and a > 0 and w > 0, 'input box')
    # No dependence on the printed floating radius: R=1/(e*C_total) exactly.
    tube = [None]*cells
    f, p = I(1), I(0)
    for j in range(cells-1, -1, -1):
        b2, bp2 = bump_bounds(j, cells)
        W = a*a*(bp2+w*w*b2)
        pmax = up(p.hi+dt*W.hi*f.hi)
        fmin = down(f.lo-dt*pmax)
        require(fmin > 0, 'radial positivity at cell '+str(j))
        ff, pp = I(fmin, f.hi), I(max(F(0),p.lo),pmax)
        tube[j] = (ff, pp, b2)
        f, p = f-dt*pp, p+dt*W*ff
        p = I(max(F(0),p.lo),p.hi)
    f0, p0 = f, p
    require(p0.lo > 0, 'initial slope')
    charge = [I(0)]
    for ff, _, b2 in tube:
        charge.append(charge[-1]+dt*w*a*a*square(ff)*b2)
    total = charge[-1]
    require(total.lo > 0, 'charge integral')
    H = f0/p0
    akre, akim, azre, azim = I(0), I(0), I(0), I(0)
    for j, ((ff, pp, b2), (cosine, sine)) in enumerate(zip(tube, phase_boxes(w,cells))):
        cumulative = I(max(F(0),charge[j].lo), charge[j+1].hi)
        q = cumulative/total
        q = I(max(F(0),q.lo), min(F(1),q.hi))
        rate = 1-square(q/ff)
        HH = I(down(H.lo+dt*min(F(0),rate.lo)),
               up(H.hi+dt*max(F(0),rate.hi)))
        require(HH.lo > 0, 'ingoing expansion at cell '+str(j))
        br = sqrt_box(b2)
        real_phi, imag_phi = a*br*cosine, -a*br*sine
        kernel = rate/ff-HH*pp/square(ff)
        electric = q/ff
        akre, akim = akre+dt*kernel*real_phi, akim+dt*kernel*imag_phi
        azre, azim = azre+dt*electric*real_phi, azim+dt*electric*imag_phi
        H = H+dt*rate
    # RP = integral (nu_t - i e S q/(4f))*phi dt, nu=-p0 H/(2f), S=2R p0.
    coefficient = -e*p0/2
    pre = coefficient*(total*akre-azim)
    pim = coefficient*(total*akim+azre)
    nu_end = -p0*H/2
    norm_lower = distance_from_zero(pre)**2+distance_from_zero(pim)**2
    require(norm_lower > 0, 'terminal P enclosure does not exclude zero')
    require(nu_end.hi < 0, 'terminal negative nu')
    curvature_lower = 2*norm_lower/max(abs(nu_end.lo),abs(nu_end.hi))**2
    return dict(amplitude=str(a), frequency=str(w), cells=cells,
                initial_f=exact(f0), initial_p=exact(p0),
                charge_integral=exact(total), terminal_H=exact(H),
                terminal_P_real=exact(pre), terminal_P_imag=exact(pim),
                terminal_nu=exact(nu_end), norm_squared_lower=str(norm_lower),
                areal_normal_Ricci_lower=str(curvature_lower),
                display=dict(P_real=display(pre),P_imag=display(pim),
                             nu=display(nu_end),Ricci_lower=float(curvature_lower)))


def algebra():
    import sympy as s
    rr, R, S, p0, C, e = s.symbols('rr R S p0 C e', real=True, nonzero=True)
    H, f, hp, fp, q = s.symbols('H f hp fp q', real=True)
    nut = -p0*(hp/f-H*fp/f**2)/2
    lhs = nut/R-s.I*e*S*q/(4*R*f)
    rhs = -e*p0*(C*(hp/f-H*fp/f**2)+s.I*q/f)/2
    residual = s.simplify((lhs-rhs).subs(S,2*R*p0).subs(R,1/(e*C)))
    require(residual == 0, 'terminal integral change of normalization')
    wrong = s.simplify((lhs+e*p0*C*(hp/f-H*fp/f**2)/2).subs(S,2*R*p0).subs(R,1/(e*C)))
    require(wrong != 0, 'omitted charged commutator not rejected')
    # Canonical areal transverse null normal, N(r)=-1.
    nu, Pr, Pi = s.symbols('nu Pr Pi', real=True, nonzero=True)
    require(s.simplify(2*(Pr**2+Pi**2)/nu**2-2*((Pr/nu)**2+(Pi/nu)**2)) == 0,
            'areal-normal Ricci identity')
    print('terminal_integral_normalization_and_electric_negative_control: PASS',flush=True)


def main(cells=2048):
    started = time.monotonic()
    algebra()
    records = []
    for a,w in ((F(1,5),8),(F(3,10),4)):
        record = certify(a,w,cells)
        records.append(record)
        print(json.dumps({k:record[k] for k in ('amplitude','frequency','display')}),flush=True)
    folder = Path(__file__).resolve().parent
    sources = ['certify_rotating_terminal_flux.py','certify_early_charged_constraints.py',
               'verify_horizon_seed.py','certify_onset_boundary.py',
               '../../definitions/MODEL.md']
    result = dict(status='PASS', fixed_coupling='3/5',
                  scope='rational null-cone and terminal transverse flux only',
                  runs=records, elapsed_seconds=time.monotonic()-started,
                  actual_future_zero_tail_is_event_horizon_proved=False,
                  full_two_dimensional_early_screen_certified=False,
                  candidates_globally_excluded=False, critical_curve_proved=False,
                  source_sha256={name:sha256((folder/name).read_bytes()).hexdigest()
                                 for name in sources})
    (folder/f'ROTATING_TERMINAL_FLUX_N{cells}_2026-10-20.json').write_text(
        json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Scope: exact first-jet enclosure; no event-horizon identification or global exclusion.',flush=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--cells',type=int,default=2048)
    main(parser.parse_args().cells)
