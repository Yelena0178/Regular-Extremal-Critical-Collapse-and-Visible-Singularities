"""Checks for EXIT10, restricted to identities and decay integrals."""
import sympy as s


def main():
    vr, vrr, C, Cr, r, h, j, P = s.symbols('vr vrr C Cr r h j P')
    B, Br = -vr, -vrr
    old = -2*B*j+(-Br+B/r+3*s.I*C)*h+(Br/r-B/r**2+s.I*Cr)*P
    new = 2*vr*j+(vrr-vr/r)*(h-P/r)+3*s.I*C*h+s.I*Cr*P
    assert s.simplify(old-new) == 0
    assert s.simplify(old-(new-2*s.I*C*h)) != 0
    print('derivative_equation_and_commutator_control: PASS')
    u = s.symbols('u', nonnegative=True)
    integral = s.integrate((1+u)**(-s.Rational(3,2)), (u,0,s.oo))
    assert integral == 2
    assert 16*integral == 32
    print('characteristic_kernel_integral: EXACT_2')
    assert 8*s.Rational(1,32)+32*s.Rational(1,128) == s.Rational(1,2)
    print('bootstrap_improvement_factor: EXACT_1_OVER_2')
    e = s.Rational(3,5)
    K = s.Rational(1,8)
    assert 4*K**2+e**2*K**4 < s.Rational(1,2)
    # exp(x)<=1/(1-x), 0<=x<1, supplies an exact upper bound <2.
    assert 1/(1-2*K**2) < 2
    print('geometric_bootstrap_margins: PASS')
    for exponent in (s.Rational(5,2), s.Rational(11,2)):
        assert s.integrate((1+u)**(-exponent),(u,0,s.oo)) == 1/(exponent-1)
    print('L1_time_error_integrability: PASS')
    print('Scope: symbolic checks; local existence, continuation, completeness remain unproved.')


if __name__ == '__main__':
    main()
