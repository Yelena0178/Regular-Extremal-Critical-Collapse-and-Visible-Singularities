"""Algebra checks for EXIT09; not a global evolution certificate."""
import sympy as s


def main():
    r, g, m, Q, e, d2, Qr = s.symbols('r g m Q e d2 Qr', nonzero=True, real=True)
    f = 1-2*m/r
    mr = f*d2/2+Q**2/(2*r**2)
    gr = g*d2/r
    br = gr*f+g*(-2*mr/r+2*m/r**2)
    expected = 2*g*(m-Q**2/(2*r))/r**2
    assert s.simplify(br-expected) == 0
    print('Bondi_radial_coefficient: EXACT_ZERO')
    # Original B=-b_r/2, C=e*g*Q/(2*r**2).
    h, P = s.symbols('h P')
    B = -expected/2
    old = -B*h+(B/r+s.I*e*g*Q/(2*r**2))*P
    new = expected/2*(h-P/r)+s.I*e*g*Q*P/(2*r**2)
    assert s.simplify(old-new) == 0
    print('Bondi_transport: EXACT_ZERO')
    vr, rho, projection, electric = s.symbols('vr rho projection electric', real=True)
    source = vr*(rho-projection)+electric-vr*rho
    assert s.expand(source-(-vr*projection+electric)) == 0
    assert s.expand(source-(vr*(rho-projection)+electric)) != 0
    print('L1_flux_and_missing_divergence_control: PASS')
    x = s.symbols('x', positive=True)
    F = s.Function('F')(x)
    assert s.simplify(s.diff(F**3/x,x)-(3*F**2*s.diff(F,x)/x-F**3/x**2)) == 0
    assert s.simplify(s.diff(F**4/(2*x**2),x)-(2*F**3*s.diff(F,x)/x**2-F**4/x**3)) == 0
    print('Hardy_integration_coefficients: EXACT_ZERO')
    # Exact flat transport h0(r)=exp(-r), including central flux.
    u = s.symbols('u', nonnegative=True)
    eta = s.exp(-u/2)
    assert s.simplify(s.diff(eta,u)+s.exp(-u/2)/2) == 0
    print('flat_center_flux: EXACT_ZERO')
    print('Scope: algebra only; future norm propagation and global existence unproved.')


if __name__ == '__main__':
    main()
