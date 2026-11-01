"""Constraint and compactified-trace algebra for EXIT23, not PDE stability."""
import sympy as s


def check(expression, label):
    if s.simplify(expression) != 0:
        raise RuntimeError(label)


def main():
    r, m, Q, e = s.symbols('r m Q e', positive=True)
    ar, ai, pr, pi, dr, di = s.symbols('ar ai pr pi dr di', real=True)
    phi, P, derivative = ar+s.I*ai, pr+s.I*pi, dr+s.I*di
    f = 1-2*m/r
    H = r**2*(s.expand_complex(P*s.conjugate(P))
              +s.expand_complex(derivative*s.conjugate(derivative)))/2
    Qr = e*r**2*s.im(phi*s.conjugate(P))
    # Keep f represented by a positive independent variable for conjugation.
    fp = s.symbols('fp', positive=True)
    Pi_pos = s.sqrt(fp)*P
    gauss = s.sqrt(fp)*Qr/r**2-e*s.im(phi*s.conjugate(Pi_pos))
    check(gauss, 'Gauss with Pi=sqrt(f) P')
    if s.simplify(gauss-2*s.sqrt(fp)*Qr/r**2) == 0:
        raise RuntimeError('wrong Gauss sign not rejected')
    mr = f*H+Q**2/(2*r**2)
    rho4 = 2*(Q**2/r**4+f*s.expand_complex(P*s.conjugate(P))
              +f*s.expand_complex(derivative*s.conjugate(derivative)))
    check(4*mr/r**2-rho4, 'Hamiltonian constraint')
    k = -r*s.sqrt(fp)*s.re(P*s.conjugate(derivative))
    check(k/r+s.re(Pi_pos*s.conjugate(derivative)), 'momentum constraint')
    check(mr+2*H*m/r-H-Q**2/(2*r**2), 'linear mass ODE')
    kr, kt = s.symbols('kr kt', real=True)
    curvature = (kr+2*kt)**2-(kr**2+2*kt**2)
    check(curvature.subs(kt, 0), 'radial extrinsic curvature cancellation')
    if s.simplify(curvature) == 0:
        raise RuntimeError('nonzero angular K contribution incorrectly discarded')
    print('complete_constraint_parameterization: EXACT_ZERO')

    x = s.symbols('x', positive=True)
    wave = s.Function('k')(x)
    hh = x**2*wave
    jr = -x**2*s.diff(hh, x)
    wr = -x**2*s.diff(jr, x)
    check(jr-(-2*x**3*wave-x**4*s.diff(wave, x)), 'first trace derivative')
    check(wr-(6*x**4*wave+6*x**5*s.diff(wave, x)
              +x**6*s.diff(wave, x, 2)), 'second trace derivative')
    check((1+1/x)**s.Rational(3, 2)*x**2
          -(1+x)**s.Rational(3, 2)*s.sqrt(x), 'weighted trace factor')
    if s.simplify(wr-(6*x**4*wave+x**6*s.diff(wave, x, 2))) == 0:
        raise RuntimeError('mixed derivative omission not rejected')
    print('compactified_C2_to_weighted_trace_and_negative_control: PASS')
    print('Scope: algebra only; no Cauchy/PDE stability or critical-curve proof.')


if __name__ == '__main__':
    main()
