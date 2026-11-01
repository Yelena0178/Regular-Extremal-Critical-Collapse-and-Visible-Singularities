"""Geometric identities used in EXIT18, not a geodesic-completeness test."""
import sympy as s


def main():
    u,r=s.symbols('u r',positive=True)
    g=s.Function('g')(u,r)
    b=s.Function('b')(u,r)
    G=s.Function('G')(u)
    metric=s.Matrix([[-g*b,-g],[-g,0]])
    time=s.Matrix([1,1])
    assert s.simplify((time.T*metric.inv()*time)[0]-(b-2)/g)==0
    omega=1/G
    luu=omega*s.diff(-g*b,u)+2*(-g*b)*s.diff(omega,u)
    lur=omega*s.diff(-g,u)+(-g)*s.diff(omega,u)
    assert s.simplify(luu+G*s.diff(g*b/G**2,u))==0
    assert s.simplify(lur+s.diff(g/G,u))==0
    wrong=omega*s.diff(-g*b,u)
    assert s.simplify(wrong+G*s.diff(g*b/G**2,u))!=0
    print('time_gradient_and_normalized_deformation_negative_control: PASS')
    V,f,Q,W2,d2=s.symbols('V f Q W2 d2')
    Dm=-V*Q**2/(2*r**2)-W2/g
    mr=f*d2/2+Q**2/(2*r**2)
    assert s.simplify(Dm+V*mr-(-W2/g+V*f*d2/2))==0
    print('fixed_radius_mass_time_derivative: EXACT_ZERO')
    print('Scope: exact identities only; completeness relies on the analytical bounds.')


if __name__=='__main__':
    main()
