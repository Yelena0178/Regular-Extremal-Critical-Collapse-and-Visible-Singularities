"""Exact leading-order charged regular-axis identities; not PDE existence."""
from pathlib import Path
from hashlib import sha256
import json
import sympy as s


def main():
    x, k = s.symbols('x k', positive=True)
    pr, pi, vr, vi, e = s.symbols('pr pi vr vi e', real=True)
    phi, V = pr+s.I*pi, vr+s.I*vi
    norm = vr**2+vi**2
    current = pi*vr-pr*vi
    a = 2*k
    r, nu = a*x, -k
    m3, q3 = 2*a*norm/3, 2*e*a*a*current/3
    m, Q, Au = m3*x**3, q3*x**3, -q3*x*x/2
    theta, z = r*V, -r*V/k
    f = 1-2*m/r
    transport = k*(2*m-Q*Q/r)/r**2
    values = [nu, k*nu*s.expand_complex(z*s.conjugate(z))/r,
              -k*nu*f*z/r-s.I*e*k*nu*Q*phi/r-s.I*e*Au*theta,
              transport*nu, -theta/r-transport*z+s.I*e*k*Q*phi/r,
              Q*Q*k*f/(2*r*r)+r*r*norm/(2*k), theta/r,
              e*r*r*current, 2*k*nu*Q/r**2]
    targets = [-k, 0, -k*V, 0, -V, 0, V, 0, 0]
    for value, target in zip(values, targets):
        if s.simplify(s.limit(value,x,0,dir='+')-target) != 0:
            raise ArithmeticError('axis limit mismatch')
    identities = {
        'mass_cubic_coefficient':s.limit(values[5]/x**2,x,0)-3*m3/2,
        'charge_cubic_coefficient':s.limit(values[7]/x**2,x,0)-3*q3/2,
        'potential_quadratic_coefficient':s.limit(values[8]/x,x,0)+q3/2,
    }
    if any(s.simplify(value) != 0 for value in identities.values()):
        raise ArithmeticError('charged leading coefficient mismatch')
    h = s.symbols('h', positive=True)
    exact = s.integrate(x*x,(x,0,h))
    if s.simplify(h*h*h/3-exact) != 0 or s.simplify((h*h*h/2)/exact) != s.Rational(3,2):
        raise ArithmeticError('axis quadrature coefficients')
    folder = Path(__file__).resolve().parent
    names = ['verify_regular_axis_limits.py', 'centered_cauchy_diamond.py', 'charged_lobatto.py']
    report = dict(status='PASS', exact_axis_limits=len(targets), exact_charged_coefficients=list(identities),
                  naive_quadrature_leading_factor='3/2', corrected_quadrature_leading_factor='1',
                  source_sha256={name:sha256((folder/name).read_bytes()).hexdigest() for name in names},
                  assumption='a smooth regular-axis solution exists in the stated gauge',
                  axis_existence_proved=False, numerical_stability_proved=False, goal_A_proved=False)
    (folder/'REGULAR_AXIS_LIMITS_CHECKS_2026-10-22.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:val for key,val in report.items() if key != 'source_sha256'},indent=2))


if __name__ == '__main__':
    main()
