"""Exact identities/integrals for the conditional far-field strip estimate."""
import sympy as s


def check(name, expr):
    if s.simplify(expr) != 0:
        raise RuntimeError(name + ': nonzero residual')
    print(name + ': EXACT_ZERO')


def main():
    r, O, Q, M, e, nu, lam = s.symbols('r O Q M e nu lam', nonzero=True)
    phi, pu, pv = s.symbols('phi pu pv')
    F = O*Q/(2*r**2)
    ruv = -nu*lam/r - O*(1-Q**2/r**2)/(4*r)
    mixed = -nu*pv/r-lam*pu/r+s.I*e*F*phi/2
    expanded = ruv*phi+nu*pv+lam*pu+r*mixed
    check('covariant_product_rule', expanded-(ruv/r+s.I*e*F/2)*r*phi)
    nlam = -O*(1-2*M/r+Q**2/r**2)/4
    potential = O*(-M/(2*r**3)+Q**2/(2*r**4)+s.I*e*Q/(4*r**2))
    check('renormalized_mass_potential', (ruv/r+s.I*e*F/2).subs(nu*lam,nlam)-potential)
    if s.simplify(potential-s.conjugate(potential).subs({s.conjugate(z):z for z in (r,O,Q,M,e)})) == 0:
        raise RuntimeError('imaginary-sign negative control failed')
    print('commutator_sign_change: REJECTED')
    x, R, l = s.symbols('x R l', positive=True)
    for n in (2,3,4,6,8):
        check(f'radial_integral_{n}', s.integrate(x**(-n),(x,R,s.oo))-R**(1-n)/(n-1))
    for n in (4,6,8):
        check(f'null_integral_{n}', s.integrate((R+l*x)**(-n),(x,0,s.oo))-R**(1-n)/(l*(n-1)))
    print('Scope: algebra/integrals only; geometric bootstrap and center remain open.')


if __name__ == '__main__':
    main()
