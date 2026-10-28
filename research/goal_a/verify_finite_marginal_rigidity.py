"""Exact algebra for A-MARG02, not a PDE or global Goal A certificate."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as sp


def main():
    r, O, nu, lam, q, e = sp.symbols('r O nu lam q e', nonzero=True, real=True)
    uv = -nu*lam/r-O*(1-q*q/r**2)/(4*r)
    at = sp.factor(uv.subs(lam, 0))
    if sp.simplify(at-O*(q*q-r*r)/(4*r**3)) != 0:
        raise ArithmeticError('mixed equation at marginal sphere')
    # Solve symmetric wave equation and commutator together, independently.
    X, Y, P, V, phi = sp.symbols('X Y P V phi')
    solved = sp.solve([X+Y+2*nu*V/r+2*lam*P/r,
                       X-Y-sp.I*e*O*q*phi/(2*r**2)], (X, Y))
    desired = -nu*V/r-lam*P/r-sp.I*e*O*q*phi/(4*r**2)
    if sp.simplify(solved[Y]-desired) != 0:
        raise ArithmeticError('D_v D_u phi sign')
    wrong = desired+sp.I*e*O*q*phi/(2*r**2)
    if sp.simplify(solved[Y]-wrong) == 0:
        raise ArithmeticError('wrong commutator accepted')
    s, A, B, pr, pi, cr, ci = sp.symbols('s A B pr pi cr ci', real=True)
    # P=P0-i A c s, A=e q Omega^2(S)/(4R^2).
    squared = sp.expand((pr+A*ci*s)**2+(pi-A*cr*s)**2)
    if sp.simplify(squared.coeff(s, 2)-A*A*(cr*cr+ci*ci)) != 0:
        raise ArithmeticError('complex cancellation')
    M, rr = sp.symbols('M rr', positive=True)
    f = (1-M/rr)**2
    if sp.diff(f, rr).subs(rr, M) != 0:
        raise ArithmeticError('ERN control')
    rp, rm = sp.Rational(2), sp.Rational(1)
    frn = (1-rp/rr)*(1-rm/rr)
    if not (frn.subs(rr, sp.Rational(3, 2)) < 0 and sp.diff(frn, rr).subs(rr, rp) > 0):
        raise ArithmeticError('subextremal interior negative control')
    v = sp.symbols('v', nonnegative=True)
    if sp.integrate((1+v)**-2, (v, 0, sp.oo)) != 1:
        raise ArithmeticError('infinite-coordinate finite-affine negative control')
    eps, a, K, t = sp.symbols('eps a K t', positive=True)
    quadratic = eps+a*t+K*t*t/2
    if sp.simplify(quadratic.subs(t, -a/K)-(eps-a*a/(2*K))) != 0:
        raise ArithmeticError('sharp nonnegative Taylor bound')
    root = Path(__file__).resolve().parent
    names = ['verify_finite_marginal_rigidity.py', 'FINITE_MARGINAL_RIGIDITY.md',
             'ACCEPTANCE.md', '../../definitions/MODEL.md']
    report = dict(claim_ids=['M02.1', 'M02.2', 'M02.3', 'M02.5'],
                  logic='PROVED (finite identities only)', evidence='EXACT_ALGEBRA',
                  audit='INTERNAL_AUDIT', sympy_version=sp.__version__,
                  checks=['marginal mixed derivative', 'wave plus commutator sign',
                          'quadratic affine curvature coefficient', 'ERN control',
                          'sharp quadratic Taylor gradient bound'],
                  negative_controls=['wrong commutator rejected', 'subextremal RN interior trapped',
                                     'unbounded coordinate with finite affine integral'],
                  pde_existence_certified=False, horizon_identity_certified=False,
                  affine_completeness_certified=False, goal_A_proved=False,
                  source_sha256={name: sha256((root/name).read_bytes()).hexdigest() for name in names})
    (root/'FINITE_MARGINAL_RIGIDITY_CHECKS_2026-10-23.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: five finite algebra controls and three negative controls; no global certification')


if __name__ == '__main__':
    main()
