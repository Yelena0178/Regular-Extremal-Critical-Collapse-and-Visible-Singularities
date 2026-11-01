"""Exact checks for the Cauchy-to-strip interface; no full-future claim."""
from fractions import Fraction as F
import sympy as s


def main():
    h,r,a,w,p,d,Q,e=s.symbols('h r a w p d Q e', real=True, nonzero=True)
    phase=s.symbols('phase', real=True)
    derivative=a*(d+s.I*w*p)*s.exp(s.I*phase)
    rpi=-h*derivative
    scalar_source=a*a*h*h*(d*d+(d-p/r)**2+2*w*w*p*p)/2
    Qr=e*w*a*a*p*p
    mr=Q*Q/(2*r*r)+scalar_source
    residuals={
        'null_norm': -h**(-2)*h*h+1,
        'initial_kappa': (h**(-2))/(4*F(1,2))-1/(2*h*h),
        'initial_chi': (rpi+h*derivative)/(2*h),
        'initial_zeta': (rpi-h*derivative)/(2*h)+derivative,
        'initial_mass_derivative': mr+Q*Qr/r-Q*Q/(2*r*r)-scalar_source-Q*Qr/r,
    }
    for name,value in residuals.items():
        if s.simplify(value)!=0:
            raise RuntimeError(name)
        print(name+': EXACT_ZERO')
    e,A,Z0,L,R=F(3,5),F(1),F(19),F(1),F(65536)
    I0,I1=F(1,3),F(108)
    qb=e*I0
    Mb=(3*I1+4*I0)/2+qb*qb/2
    Z=Z0+1
    K=Z+2*A
    q=qb+2*e*A*L*Z+1
    M=Mb+4*L*K*K+1
    C=2*M/R**2+F(4,3)*q*q/R**3+2*e*q/R
    checks={
        'initial_constraint':(4*Mb,R),
        'metric':(2*M/R+q*q/R**2,F(1,2)),
        'nu':(4*M/R+2*q*q/R**2,F(1,4)),
        'kappa':(4*L*K*K/R,F(1,4)),
        'wave':(L*C,F(1,4)),
        'derivative':(2*A*C,F(1,2)),
        'mass_charge':(2*e*q*A*L*Z/R,F(1,2)),
    }
    for name,(lhs,rhs) in checks.items():
        if not lhs<rhs:
            raise RuntimeError(name)
        print(name+': rational_margin='+str(rhs-lhs))
    print('budgets: Mb='+str(Mb)+', M='+str(M)+', q='+str(q))
    print('Scope: explicit initial-data budgets and strip estimates; center/global dispersion open.')


if __name__=='__main__':
    main()
