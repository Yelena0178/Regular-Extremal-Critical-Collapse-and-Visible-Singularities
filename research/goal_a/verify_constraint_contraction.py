"""Exact constraint-homotopy algebra, not an evolution certificate."""
from pathlib import Path
from hashlib import sha256
import json
import sympy as z


def check(expr, label):
    if z.simplify(expr) != 0:
        raise ArithmeticError(label)


def main():
    r = z.symbols('r', positive=True)
    m, mp, ell, ellp, current = z.symbols('m mp ell ellp current', real=True)
    f = 1-2*m/r
    D = f+r*r*ell*ell
    Dr = z.diff(D,r)+z.diff(D,m)*mp+z.diff(D,ell)*ellp
    scalar_curvature = 2*(1-D-r*Dr)/r**2
    kr = ell+r*ellp+r*current
    check(2*((kr-ell)/r-ellp)-2*current, 'momentum constraint')
    check(scalar_curvature+4*kr*ell+2*ell**2
          -4*(mp/r**2+r*ell*current), 'Hamiltonian reduction')
    if z.simplify(scalar_curvature+4*kr*ell+2*ell**2-4*mp/r**2) == 0:
        raise ArithmeticError('missing momentum work negative control')

    s, ff = z.symbols('s ff', positive=True)
    k, J, S = z.symbols('k J S', real=True)
    Ds = ff+s*s*k*k
    gp = s*s*Ds+s**3*k*z.sqrt(Ds)
    gm = s*s*Ds-s**3*k*z.sqrt(Ds)
    energy = r*r*s*s*Ds*S/2+r*r*s**3*k*z.sqrt(Ds)*J
    check(energy-r*r*(gp*(S+2*J)+gm*(S-2*J))/4,
          'positive square decomposition')
    y = s*k/z.sqrt(Ds)
    for sign in (-1,1):
        G = s*s*Ds+sign*s**3*k*z.sqrt(Ds)
        check(z.diff(G,s)-s*Ds*(1+sign*y)*(y*y+sign*y+2),
              'monotone coefficient derivative')
    yy = z.symbols('y',real=True)
    for sign in (-1,1):
        check(yy*yy+sign*yy+2-((yy+z.Rational(sign,2))**2+z.Rational(7,4)),
              'strictly positive quadratic factor')
    check(1-y*y-ff/Ds, 'absolute normalized tilt below one')
    check(Ds-s*s*k*k-ff, 'initial expansion product')
    check(energy.subs(k,0)-r*r*s*s*ff*S/2, 'polar constraint limit')

    alpha, R, integral = z.symbols('alpha R integral',positive=True)
    check(z.diff(-alpha**2*R*integral,alpha,2)+2*R*integral,
          'terminal pulse quadratic focusing')
    folder=Path(__file__).resolve().parent
    names=['verify_constraint_contraction.py',
           'CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md','../../definitions/MODEL.md']
    report=dict(status='PASS',
                scope='exact constraint, scaling, and leading focusing identities only',
                actual_AF_seed_implemented_numerically=False,
                full_evolution_certified=False,
                small_data_analysis_independently_verified=False,
                boundary_parameter_computed=False,
                extremal_endpoint_proved=False,
                three_branch_goal_proved=False,
                source_sha256={name:sha256((folder/name).read_bytes()).hexdigest()
                               for name in names})
    (folder/'CONSTRAINT_CONTRACTION_CHECKS_2026-10-20.json').write_text(
        json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: constraints, signed tilt monotonicity, expansion identity, '
          'polar limit, and terminal-pulse quadratic focusing.')
    print('Scope: exact algebra only; no evolution or three-branch certification.')


if __name__=='__main__':
    main()
