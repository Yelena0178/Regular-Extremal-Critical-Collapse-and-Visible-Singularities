"""Algebraic bounds for EXIT11; does not test the continuation proof."""
from fractions import Fraction as F
import sympy as s


def main():
    r, nu, lam, P, chi, zeta = s.symbols('r nu lam P chi zeta', nonzero=True)
    phi=P/r
    theta=chi-lam*P/r
    z=zeta/nu-P/r
    assert s.simplify(theta+lam*phi-chi)==0
    assert s.simplify(nu*z+nu*phi-zeta)==0
    print('transport_state_conversion: EXACT_ZERO')
    lower=4*F(3,8)*F(3,8)
    upper=4*F(1)*F(2,3)
    assert lower==F(9,16) and upper==F(8,3)
    assert upper/2/F(3,16)==F(64,9)
    print('affine_factor_and_potential_bounds: PASS')
    # r<=R+3L/2+3t/2; rho=R+3t/16, R>=L.
    R,L,t=s.symbols('R L t',nonnegative=True)
    gap=s.expand(10*(R+3*t/16)-(R+3*L/2+3*t/2))
    assert s.expand(gap.subs(R,L+s.Symbol('x',nonnegative=True))) == 15*L/2+9*s.Symbol('x',nonnegative=True)+3*t/8
    print('radius_comparison: PASS')
    print('Scope: coefficient checks only; analytic continuation requires the written argument.')


if __name__=='__main__':
    main()
