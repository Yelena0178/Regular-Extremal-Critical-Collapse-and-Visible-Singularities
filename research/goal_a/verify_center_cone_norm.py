"""Check finite-cone identities and rational budgets; not a future evolution test."""
from fractions import Fraction as F
import sympy as s


def main():
    a,b,x,y,r=s.symbols('a b x y r',real=True,nonzero=True)
    h=a+s.I*b
    avg=x+s.I*y
    # (r |avg|^2)' = 2 Re(h conjugate(avg)) - |avg|^2.
    derivative=2*s.re(h*s.conjugate(avg))-avg*s.conjugate(avg)
    residual=(h-avg)*s.conjugate(h-avg)-(h*s.conjugate(h)-derivative)
    if s.simplify(s.expand_complex(residual))!=0:
        raise RuntimeError('mean-subtraction identity')
    print('mean_subtraction_identity: EXACT_ZERO')
    z,t=s.symbols('z t',positive=True)
    if s.simplify(s.integrate((t/z)**2/z,(z,t,s.oo))-s.Rational(1,2))!=0:
        raise RuntimeError('BV kernel norm')
    print('BV_kernel_norm_squared: EXACT_ONE_HALF')
    e,R,L,A=F(3,5),F(65536),F(1),F(1)
    M,q=F(314953,150),F(126,5)
    l,G=F(3,16),F(8,3)
    C=2*M/R**2+F(4,3)*q*q/R**3+2*e*q/R
    S=A/(1-L*C)
    eta=L*C*S
    eps=L*G*S/l*(M/(2*R**3)+q*q/(2*R**4)+e*q/(4*R**2))
    delta=4*eps**2+e**2*eps**2*eta**2/4
    mass=eps*eta/2+2*e**2*eps*eta**3
    for name,value,bound in (
        ('amplitude',eps,F(126,10**10)),
        ('compactness',delta,F(64,10**17)),
        ('hawking_mass',mass,F(3,10**12)),
    ):
        if not 0<value<bound:
            raise RuntimeError(name)
        print(f'{name}: EXACT_LESS_THAN {bound}; approximate_bound={float(value):.12g}')
    print('Scope: one cone only; propagation to all future cones unproved.')


if __name__=='__main__':
    main()
