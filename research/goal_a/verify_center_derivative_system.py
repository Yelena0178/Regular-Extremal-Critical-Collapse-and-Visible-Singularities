"""Check covariant radial differentiation, including the charged commutator."""
import sympy as s


def main():
    B,Br,C,Cr,r,h,j,Psi=s.symbols('B Br C Cr r h j Psi')
    beta=B/r+s.I*C
    beta_r=Br/r-B/r**2+s.I*Cr
    # D_u((D_v h)/lambda), with lambda_u/lambda=B,
    # and i e F_uv/lambda=2 i C.
    derived=-Br*h-B*j+beta_r*Psi+beta*h+2*s.I*C*h-B*j
    expected=-2*B*j+(-Br+B/r+3*s.I*C)*h+(Br/r-B/r**2+s.I*Cr)*Psi
    if s.simplify(derived-expected)!=0:
        raise RuntimeError('radial derivative transport failed')
    print('charged_radial_transport: EXACT_ZERO')
    wrong=expected-2*s.I*C*h
    if s.simplify(derived-wrong)==0:
        raise RuntimeError('missing commutator was not rejected')
    print('omitted_commutator: REJECTED')
    eps,e,Q,P,M=s.symbols('eps e Q P M', nonzero=True)
    # Exact initial N=1/2, r=1/eps; fixed initial M and Q suffice
    # for the leading term. Uniformly bounded varying M has the same limit.
    f=1-2*M*eps+Q**2*eps**2
    B0=-(M-Q**2*eps)*eps**2/f
    C0=e*Q*eps**2/(2*f)
    j0=2*(B0*eps+s.I*C0)*P
    if s.simplify(s.limit(j0/eps**2,eps,0)-s.I*e*Q*P)!=0:
        raise RuntimeError('initial leading coefficient failed')
    print('initial_R_squared_limit: EXACT_ZERO')
    print('Scope: identities only; finite-region estimates and center theorem require analysis.')


if __name__=='__main__':
    main()
