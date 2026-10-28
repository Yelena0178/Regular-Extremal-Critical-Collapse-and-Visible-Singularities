"""Rational bounds on the inner null trace, conditional on A-EXIT04."""
from fractions import Fraction as F
import sympy as s


def main():
    a,b,x,y,lam,r=s.symbols('a b x y lam r',real=True,nonzero=True)
    psi=a+s.I*b
    chi=x+s.I*y
    theta=chi-lam*psi/r
    if s.simplify(s.im(psi*s.conjugate(theta))-s.im(psi*s.conjugate(chi)))!=0:
        raise RuntimeError('charge cancellation failed')
    print('charge_cancellation: EXACT_ZERO')
    # |X-Y|^2 <= 2|X|^2+2|Y|^2: its difference equals |X+Y|^2.
    Y=lam*psi/r
    gap=2*chi*s.conjugate(chi)+2*Y*s.conjugate(Y)-theta*s.conjugate(theta)
    if s.simplify(gap-(chi+Y)*s.conjugate(chi+Y))!=0:
        raise RuntimeError('energy bound identity failed')
    print('energy_bound_identity: EXACT_ZERO')
    e,R,L,A=F(3,5),F(65536),F(1),F(1)
    M,q=F(314953,150),F(126,5)
    C=2*M/R**2+F(4,3)*q*q/R**3+2*e*q/R
    delta=L*C
    if not 0<delta<F(1,4):
        raise RuntimeError('bootstrap condition failed')
    S=A/(1-delta)
    J=delta*S
    G,l=F(8,3),F(3,16)
    E=3*L**2*G**2*S**2*(
        M**2/4*(L/R**6+1/(5*l*R**5))
        +q**4/4*(L/R**8+1/(7*l*R**7))
        +e**2*q**2/16*(L/R**4+1/(3*l*R**3)))
    qc=e*J**2/2
    mc=F(8,3)*E+F(3,2)*J**2/R+qc**2/(2*R)
    vc=mc+qc**2/(2*R)
    for name,value,limit in (
        ('Psi_and_chi_L1',J,F(1,2000)),
        ('charge_total_variation',qc,F(1,10**7)),
        ('chi_L2_squared',E,F(2,10**12)),
        ('renormalized_mass',vc,F(11,10**12)),
    ):
        if not 0<value<limit:
            raise RuntimeError(name+': bound failed')
        print(f'{name}: EXACT_LESS_THAN {limit}; approximate_bound={float(value):.12g}')
    print('Scope: conditional trace budgets; center concentration and global existence unproved.')


if __name__=='__main__':
    main()
