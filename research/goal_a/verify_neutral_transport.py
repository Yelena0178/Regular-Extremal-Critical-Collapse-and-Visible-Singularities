"""Exact finite transport algebra and E0 numerical checks; no PDE certificate."""

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import numpy as np
from verify_null_infinity_algebra import P, sym
from neutral_transport import (TransportConfiguration, evolve, rhs, jacobian,
                               geometry, onset_boundaries)
from transport_defect import exact_cell_margins


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def evaluate(poly, point):
    value = Q(0)
    for powers, coefficient in poly.terms.items():
        term = coefficient
        for name, power in powers:
            term *= point[name]**power
        value += term
    return value


def algebra_checks():
    names = ("r","k","t","n","z","m")
    r,k,t,n,z,m = [sym(s) for s in names]
    E,G,nuu,zu,kv,tv = [sym(s) for s in ("E","G","nuu","zu","kv","tv")]
    f = 1-2*m/r
    field = (n,k*n*z*z/r,-k*f*n*z/r,2*k*m*n/r**2,-t/r-2*k*m*z/r**2,t*t/(2*k))
    H = f*n*z*z/2
    du = dict(zip(names,(n,field[1],field[2],nuu,zu,H+G)))
    dv = dict(zip(names,(k*f+E,kv,tv,field[3],field[4],field[5])))
    identities = {
        "E_u": field[3]-(k*f).total(du)-2*k*G/r,
        "G_v": field[5].total(du)-H.total(dv)+m*n*z*z*E/r**2,
        "scalar_integrability": (n*z).total(dv)+n*t/r,
        "mass_identity": r*(1+4*n*k*f/(-4*k*n))/2-m,
        "r_mixed": field[3]-2*k*m*n/r**2,
    }
    du_physical = dict(du,m=H)
    dv_physical = dict(dv,r=k*f)
    identities["S_mixed"] = ((n*z*z/r).total(dv_physical)
                              +(field[3]/n).total(du_physical)
                              +2*n*z*t/r**2+4*k*m*n/r**3)
    for name, expression in identities.items():
        require(not expression.terms,"exact identity: "+name)
    # Nonzero negative controls: wrong sign in the scalar transport and the
    # omitted mass term do not satisfy the defining integrability equation.
    for bad_zv in (t/r-2*k*m*z/r**2,-t/r):
        bad_dv = dict(dv,z=bad_zv)
        require(bool(((n*z).total(bad_dv)+n*t/r).terms),"wrong wave variant accepted")
    for sample in range(1,8):
        point = dict(zip(names,(Q(3+sample,4),Q(2,5),Q(sample,11),
                               -Q(4,7),-Q(sample,9),Q(sample,13))))
        array = np.array([float(point[name]) for name in names])
        values = np.array([float(evaluate(poly,point)) for poly in field])
        J = np.array([[float(evaluate(poly.partial(name),point)) for name in names]
                      for poly in field])
        require(np.max(abs(values-rhs(array))) < 5e-14,"numerical RHS expression")
        require(np.max(abs(J-jacobian(array))) < 5e-13,"numerical Jacobian expression")
    return {"identities":list(identities),"arithmetic":"exact rational Laurent polynomials",
            "rejected_wave_variants":2,"RHS_Jacobian_sample_checks":7}


def flrw_state(u,v):
    b = 1-(u+v)/8
    a = np.sqrt(b)
    x = (v-u)/2
    r = a*x
    adot = -1/(8*a)
    nu,lam = (-a+adot*x)/2,(a+adot*x)/2
    scalar_derivative = -np.sqrt(3)/(16*b)
    k = -b/(4*nu)
    return np.array((r,k,r*scalar_derivative,nu,r*scalar_derivative/nu,
                     r*(1+4*nu*lam/b)/2))


def main():
    algebra = algebra_checks()
    radius,edge,h,d = [Q(1,10)]*6,[Q(1,100)]*6,[Q(1,20)]*6,[Q(1,50)]*6
    L = [[Q(int(i==j),2) for j in range(6)] for i in range(6)]
    margin = exact_cell_margins(radius,edge,h,d,L)
    rejected = False
    try:
        exact_cell_margins(radius,edge,h,[Q(10)]*6,L)
    except ArithmeticError:
        rejected = True
    require(rejected,"invalid cell inequality accepted")
    runs = []
    for n in (32,64,128):
        cfg = TransportConfiguration(steps_u=n,steps_v=n,final_u=2.2,initial_v=2.6,final_v=4.7)
        data = evolve(lambda v:flrw_state(0,v),lambda u:flrw_state(u,2.6),cfg)
        exact = flrw_state(data['u'][:,None],data['v'][None,:]).transpose(1,2,0)
        errors = np.max(abs(data['state']-exact),axis=(0,1)).tolist()
        runs.append({"configuration":data['report']['configuration'],"max_errors":errors,
                     "fixed_point":geometry(data['state'][-1,-1]),
                     "exact_fixed_point":geometry(flrw_state(2.2,4.7)),
                     "maximum_last_iteration_change":data['report']['maximum_last_iteration_change']})
    for coarse,fine in zip(runs,runs[1:]):
        require(all(b<a/2.5 for a,b in zip(coarse['max_errors'],fine['max_errors'])),
                "FLRW transport convergence")
    folder = Path(__file__).resolve().parent
    result = {"evidence":"exact_finite_algebra_and_E0_transport_benchmarks",
              "goal_A_proved":False,"rigorous_PDE_error":False,
              "actual_strict_trapping_certified":False,"algebra":algebra,"FLRW_runs":runs,
              "cell_kernel":{"exact_positive_margins":[str(v) for v in margin],
                             "bad_inequality_rejected":rejected,
                             "scope":"finite inequality only; supplied bounds not certified"}}
    sources = ("neutral_transport.py","transport_defect.py","verify_neutral_transport.py",
               "verify_null_infinity_algebra.py","RATIONAL_GOURSAT_CERTIFICATION.md")
    result['source_sha256'] = {s:hashlib.sha256((folder/s).read_bytes()).hexdigest() for s in sources}
    output = folder/"NEUTRAL_TRANSPORT_CHECKS_2026-10-16.json"
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"consistency":"pass","scope":result['evidence'],
                      "FLRW_errors":[r['max_errors'] for r in runs],"report":output.name}),flush=True)


if __name__ == '__main__':
    main()
