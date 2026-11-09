"""Exact EXIT20 compactification identities; no PDE existence certification."""
import sympy as s


def require_zero(expression, label):
    if s.simplify(expression) != 0:
        raise RuntimeError(label)


def main():
    x, g, m, Q, e, a, V = s.symbols('x g m Q e a V', real=True)
    pr, pi, kr, ki = s.symbols('pr pi kr ki', real=True)
    psi, k = pr+s.I*pi, kr+s.I*ki
    h, d = x**2*k, x*(x*k-psi)
    f = 1-2*m*x
    # Each x derivative equals -r^2 times its physical r derivative.
    require_zero(-h/x**2+k, 'radiation constraint')
    require_zero(-e*s.im(psi*s.conjugate(h))/x**2
                 +e*s.im(psi*s.conjugate(k)), 'charge constraint')
    require_zero(-(g*s.conjugate(d)*d*x)/x**2
                 +g*x*s.conjugate(x*k-psi)*(x*k-psi), 'metric constraint')
    require_zero(-(f*s.conjugate(d)*d/2+Q**2*x**2/2)/x**2
                 +(f*s.conjugate(x*k-psi)*(x*k-psi)+Q**2)/2,
                 'mass constraint')
    require_zero(-(-g*Q*x**2)/x**2-g*Q, 'potential constraint')
    kx, ku = s.symbols('kx ku')
    vr = g*(m-Q**2*x/2)*x**2
    # Substitute h=x^2 k in (partial_u - V partial_r + i e a)h.
    original = (x**2*ku+V*x**2*(2*x*k+x**2*kx)
                +s.I*e*a*x**2*k-vr*d-s.I*e*g*Q*psi*x**2/2)
    compact_rhs = (-2*V*x*k+g*x*(m-x*Q**2/2)*(x*k-psi)
                   +s.I*e*g*Q*psi/2-s.I*e*a*k)
    require_zero(original/x**2-(ku+V*x**2*kx-compact_rhs),
                 'compactified charged wave equation')
    if s.simplify(compact_rhs.subs(x, 0)+s.I*e*a*k) == 0:
        raise RuntimeError('negative control failed: charged boundary term lost')
    wx_from_r = -(V*d*x-s.I*e*g*Q*psi*x**2/2)/x**2
    require_zero(wx_from_r-(-V*(x*k-psi)+s.I*e*g*Q*psi/2),
                 'transverse constraint')
    print('compactified_constraints_wave_transverse: EXACT_ZERO')

    u = s.symbols('u', real=True)
    gg, mm = s.Function('g')(u, x), s.Function('m')(u, x)
    ff = 1-2*mm*x
    metric = s.Matrix([[-gg**2*ff*x**2, gg], [gg, 0]])
    inverse = metric.inv()
    require_zero(metric.det()+gg**2, 'conformal nondegeneracy')
    require_zero(inverse[1, 1]-ff*x**2, 'null conformal boundary')
    coordinates = [u, x]
    gamma_uuu = sum(inverse[0, j]*(2*s.diff(metric[j, 0], u)
                                 -s.diff(metric[0, 0], coordinates[j]))/2
                    for j in range(2))
    at_boundary = gamma_uuu.subs(x, 0).doit()
    G = gg.subs(x, 0)
    require_zero(at_boundary-s.diff(G, u)/G, 'boundary connection')
    require_zero(s.diff(1/G, u)/G+at_boundary/G**2,
                 'affine null boundary generator')
    # Bondi-normalized physical g_uu = -(g/G)^2 f; g/G=1+O(x^2).
    c2 = s.symbols('c2')
    coefficient = s.diff(-(1+c2*x**2)**2*(1-2*m*x), x).subs(x, 0)
    require_zero(coefficient-2*m, 'Bondi mass coefficient')
    print('conformal_boundary_generator_and_Bondi_coefficient: EXACT_ZERO')

    W2, d2 = s.symbols('W2 d2', real=True)
    Dm = -V*Q**2*x**2/2-W2/g
    mr = f*d2/2+Q**2*x**2/2
    require_zero(Dm+V*mr-(-W2/g+V*f*d2/2), 'mass flux cancellation')
    psi_u, W = s.symbols('psi_u W')
    psi_u_expression = W+V*x**2*k-V*x*psi-s.I*e*a*psi
    require_zero(psi_u_expression.subs(x, 0)+s.I*e*a*psi-W,
                 'covariant radiation derivative')
    print('Bondi_flux_and_gauge_negative_control: PASS')
    print('Scope: exact algebra only; finite-u regularity and global claims need analysis.')


if __name__ == '__main__':
    main()
