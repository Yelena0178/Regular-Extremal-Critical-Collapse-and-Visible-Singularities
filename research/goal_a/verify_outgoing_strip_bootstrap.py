"""Exact transport identities and a rational consistency witness for S3."""
from fractions import Fraction as F
import sympy as s


def main():
    r,k,n,Q,m,e=s.symbols('r k n Q m e', real=True, nonzero=True)
    a,b,x,y=s.symbols('a b x y', real=True)
    psi=a+s.I*b
    zeta=x+s.I*y
    phi=psi/r
    z=zeta/n-psi/r
    W=zeta-n*psi/r
    f=1-2*m/r
    Qu=-e*r*n*s.im(phi*s.conjugate(z))
    mu=Q**2*n/(2*r**2)+f*n*z*s.conjugate(z)/2
    identities={
        'scalar_conversion': n*z-W,
        'charge_u': Qu+e*s.im(psi*s.conjugate(zeta)),
        'mass_u': mu+Q*Qu/r-Q**2*n/(2*r**2)
            -(f*W*s.conjugate(W)/(2*n)+Q*Qu/r),
        'kappa_u': n*z*s.conjugate(z)/r-W*s.conjugate(W)/(r*n),
        'nu_v': k*(2*m-Q**2/r)/r**2
            -2*k*((m+Q**2/(2*r))-Q**2/r)/r**2,
    }
    for name,expr in identities.items():
        if s.simplify(s.expand_complex(expr)) != 0:
            raise RuntimeError(name)
        print(name+': EXACT_ZERO')
    coupling,A,Z0,L,M0,Q0,R=F(3,5),F(1),F(1),F(1),F(5),F(1),F(4096)
    Z=Z0+1
    K=Z+2*A
    q=abs(Q0)+2*abs(coupling)*A*L*Z+1
    M=abs(M0)+4*L*K*K+1
    C=2*M/R**2+F(4,3)*q*q/R**3+2*abs(coupling)*q/R
    checks={
        'metric':(2*M/R+q*q/R**2,F(1,2)),
        'nu_exponent':(4*M/R+2*q*q/R**2,F(1,4)),
        'kappa_exponent':(4*L*K*K/R,F(1,4)),
        'volterra':(L*C,F(1,4)),
        'zeta':(2*A*C,F(1,2)),
        'charge_mass':(2*abs(coupling)*q*A*L*Z/R,F(1,2)),
    }
    for name,(lhs,rhs) in checks.items():
        if not lhs<rhs:
            raise RuntimeError(name+': insufficient margin')
        print(name+': rational_margin='+str(rhs-lhs))
    print('Scope: identities and constant feasibility; no global existence certification.')


if __name__=='__main__':
    main()
