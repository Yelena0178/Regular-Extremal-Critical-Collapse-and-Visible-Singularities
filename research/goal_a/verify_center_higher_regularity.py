"""Finite algebra checks for the quotient and averaged coefficient formulas."""
import sympy as s


def main():
    r,t=s.symbols('r t',positive=True)
    F=r+2*r**3-r**5+r**8
    G=3*r-r**2+2*r**6
    for k in range(1,7):
        dk=s.diff(G,r,k)
        bracket=dk-k*s.integrate(t**(k-1)*dk.subs(r,t*r),(t,0,1))
        rhs=F/r*bracket
        for j in range(1,k+1):
            rhs+=s.binomial(k,j)*s.diff(F,r,j)*s.integrate(
                t**(k-j)*s.diff(G,r,k-j+1).subs(r,t*r),(t,0,1))
        assert s.expand(rhs-s.diff(F*G/r,r,k))==0
        assert s.expand(rhs-F/r*dk-s.diff(F*G/r,r,k))!=0
    print('quotient_formula_orders_1_to_6_and_boundary_negative_control: PASS')
    g=1+r+r**2
    d=r+r**2
    Z=r+2*r**2
    mass=s.integrate(g*(d**2+r**2*Z**2),(r,0,r))/(2*g)
    direct=g*mass/r**2-g*r*Z**2/2
    avg=s.integrate(t*(g*(d**2/r+r*Z**2)).subs(r,t*r),(t,0,1))/2-g*r*Z**2/2
    assert s.simplify(avg-direct)==0
    print('averaged_velocity_derivative: EXACT_ZERO')
    print('Scope: polynomial identity checks; regularity theorem requires analytic proof.')


if __name__=='__main__':
    main()
