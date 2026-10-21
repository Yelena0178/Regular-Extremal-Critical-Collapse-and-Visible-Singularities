"""Exact constraint reconstruction and lowest charged center coefficients."""
import sympy as s


def main():
    r,g,b,Q,d2=s.symbols('r g b Q d2',nonzero=True,real=True)
    gr=g*d2/r
    br=(g*(1-Q**2/r**2)-b)/r
    mr=(1-b/g)/2+r*(-br/g+b*gr/g**2)/2
    assert s.simplify(mr-(b*d2/(2*g)+Q**2/(2*r**2)))==0
    print('mass_constraint_from_integral_reconstruction: EXACT_ZERO')
    x0,y0,x1,y1,e=s.symbols('x0 y0 x1 y1 e',real=True)
    h0=x0+s.I*y0
    h1=x1+s.I*y1
    h=h0+h1*r
    H=h0+h1*r/2
    current=s.expand(e*r*s.im(H*s.conjugate(h)))
    charge=s.integrate(current,(r,0,r))
    I=s.im(h0*s.conjugate(h1)).expand()
    assert s.simplify(charge-e*I*r**3/6)==0
    norm=x1**2+y1**2
    g2=norm/8
    b2=g2/3
    m3=(g2-b2)/2
    assert s.simplify(m3-norm/24)==0
    a2=-e*I/12
    covariant=s.expand(b2*h1/2+s.I*e**2*I*h0/12)
    ordinary=s.expand(covariant-s.I*e*a2*h0)
    expected=norm*h1/48+s.I*e**2*I*h0/6
    assert s.simplify(ordinary-expected)==0
    assert s.simplify(covariant-expected)!=0
    print('charged_center_coefficients_and_gauge_negative_control: PASS')
    print('Scope: exact algebra only; local well-posedness and global continuation unproved.')


if __name__=='__main__':
    main()
