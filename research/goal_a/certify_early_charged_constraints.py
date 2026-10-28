"""Rational interval proof of the new smooth charged pulse constraints.

Backward Raychaudhuri enclosure, forward charge quadrature, and a complete
H budget. This certifies null data, not their two-dimensional future.
"""

from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import time

from verify_horizon_seed import I,down,up
from certify_onset_boundary import exp_bound


def square(x):
    x=I.lift(x)
    return I(0 if x.lo<=0<=x.hi else down(min(x.lo*x.lo,x.hi*x.hi)),
             up(max(x.lo*x.lo,x.hi*x.hi)))


@lru_cache(None)
def bump_bounds(j,n):
    # Both b^2 and (b')^2 are invariant under v -> 1-v.
    j=min(j,n-1-j);left,right=Q(j,n),Q(j+1,n)
    if j==0:
        z=Q(n,4)
        if z<2:raise ValueError('tail bound requires n>=8')
        b2=exp_bound(2-2*z)
        return I(0,b2.hi),I(0,up(16*z**4*b2.hi))
    dlow,dhigh=4*left*(1-left),4*right*(1-right)
    # Monotonicity of exp(2-2/d) for positive d supplies exact endpoint bounds.
    b2=I(max(0,exp_bound(2-2/dlow).lo),min(1,exp_bound(2-2/dhigh).hi))
    factor=I(4*(1-2*right)/dhigh**2,4*(1-2*left)/dlow**2)
    return b2,square(factor)*b2


def display(x):return [float(x.lo),float(x.hi)]
def exact(x):return [str(x.lo),str(x.hi)]


def certify(amplitude,frequency,n=2048):
    a,w=Q(amplitude),Q(frequency);h=Q(1,n)
    if n%2:raise ValueError('even mesh required')
    cells=[None]*n;f,p=I(1),I(0);least_f=Q(1)
    # In reversed time s, f_s=-p and p_s=W f. Positivity and these two
    # elementary integral bounds give a continuation enclosure on each cell.
    for j in range(n-1,-1,-1):
        b2,bp2=bump_bounds(j,n);W=a*a*(bp2+w*w*b2)
        pmax=up(p.hi+h*W.hi*f.hi)
        fmin=down(f.lo-h*pmax)
        if fmin<=0:raise ArithmeticError(f'positive Raychaudhuri tube failed at {j}')
        F,P=I(fmin,f.hi),I(max(0,p.lo),pmax)
        cells[j]=(F,b2)
        f,p=f-h*P,p+h*W*F
        p=I(max(0,p.lo),p.hi)
        least_f=min(least_f,F.lo)
    if p.lo<=0:raise ArithmeticError('initial slope not positive')
    initial_f,initial_p=f,p
    charge=[I(0)]
    for F,b2 in cells:charge.append(charge[-1]+h*w*a*a*square(F)*b2)
    total=charge[-1]
    if total.lo<=0:raise ArithmeticError('charge integral not positive')
    radius=1/(Q(3,5)*total);H=initial_f/initial_p;least_H=H.lo
    for j,(F,b2) in enumerate(cells):
        C=I(max(0,charge[j].lo),charge[j+1].hi)
        q=C/total
        # q is a cumulative nonnegative integral divided by its own total.
        q=I(max(0,q.lo),min(1,q.hi))
        rate=1-square(q/F)
        least_H=min(least_H,down(H.lo+h*min(0,rate.lo)))
        H=H+h*rate
        if least_H<=0:raise ArithmeticError(f'positive H budget failed at {j}')
    cap=2*radius*initial_f;scale=2*radius*initial_p
    return dict(amplitude=str(a),frequency=str(w),cells=n,
        initial_f=exact(initial_f),initial_p=exact(initial_p),charge_integral=exact(total),
        radius=exact(radius),cap=exact(cap),scale=exact(scale),terminal_H=exact(H),
        minimum_dimensionless_radius_lower=str(least_f),minimum_H_lower=str(least_H),
        display=dict(radius=display(radius),initial_f=display(initial_f),initial_p=display(initial_p),
            H_terminal=display(H),minimum_H=float(least_H),minimum_f=float(least_f)))


def main(n=2048):
    start=time.monotonic();records=[]
    for a,w in [(Q(1,5),8),(Q(3,10),4)]:
        try:record=dict(status='PASS',**certify(a,w,n))
        except ArithmeticError as error:record=dict(status='FAIL',amplitude=str(a),frequency=str(w),failure=str(error))
        records.append(record)
        print(json.dumps({k:v for k,v in record.items() if k in ('status','amplitude','frequency','display','failure')}),flush=True)
    folder=Path(__file__).resolve().parent
    names=['certify_early_charged_constraints.py','verify_horizon_seed.py','certify_onset_boundary.py']
    result=dict(status='PASS' if all(r['status']=='PASS' for r in records) else 'FAIL',
        scope='smooth rotating-bump null constraints only',runs=records,elapsed_seconds=time.monotonic()-start,
        fixed_coupling='3/5',terminal_charge_equals_radius_by_definition=True,
        complete_PDE_rectangle_certified=False,full_AF_Cauchy_realization=False,goal_A_proved=False,
        source_sha256={name:sha256((folder/name).read_bytes()).hexdigest() for name in names})
    (folder/f'EARLY_CHARGED_CONSTRAINT_CERTIFICATE_N{n}_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    if result['status']!='PASS':raise SystemExit(1)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,default=2048)
    main(parser.parse_args().n)
