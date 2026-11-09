"""Constraint propagation for the integral formulation, without assuming kappa_u."""
import sympy as s


def main():
    r,g,m,Q,e,D2,W2,X,I,J,G=s.symbols('r g m Q e D2 W2 X I J G',nonzero=True, real=True)
    f=1-2*m/r
    V=g*f/2
    Vr=g*(m-Q**2/(2*r))/r**2
    mr=f*D2/2+Q**2/(2*r**2)
    Dm=G-V*Q**2/(2*r**2)-W2/g
    Df=-2*Dm/r-2*V*m/r**2
    Dmr=(Df*D2/2+f*(Vr*D2-e*g*Q*I/(2*r)-X/r)
         -e*Q*J/r+V*Q**2/r**3)
    Gr=(Dmr-Vr*mr+Vr*Q**2/(2*r**2)+V*Q*(e*r*I)/r**2
        -V*Q**2/r**3+2*V*X/(g*r)+e*Q*J/r-D2*W2/(g*r))
    assert s.factor(Gr+D2*G/r)==0
    assert s.factor((-Vr-Df/f+W2/(V*r)).subs(G,0))==0
    print('mass_defect_and_recovered_kappa_transport: EXACT_ZERO')
    pr,pi,hr,hi,kr,ki,c,v=s.symbols('pr pi hr hi kr ki c v',real=True)
    P=pr+s.I*pi
    h=hr+s.I*hi
    k=kr+s.I*ki
    Dh=v*(h-P/r)+s.I*c*P
    k_r=-v*P/r-s.I*c*P
    first=e*s.im(k*s.conjugate(h)+P*s.conjugate(Dh))-v*e*s.im(P*s.conjugate(h))
    second=e*s.im(h*s.conjugate(k)+P*s.conjugate(k_r))
    assert s.simplify(s.expand_complex(first+second))==0
    wrong=e*s.im(h*s.conjugate(k)+P*s.conjugate(-v*P/r))
    assert s.simplify(s.expand_complex(first+wrong))!=0
    print('Maxwell_time_constraint_and_omitted_charge_control: PASS')
    print('Scope: algebra and conditional propagation; local/global existence not certified.')


if __name__=='__main__':
    main()
