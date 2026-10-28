"""Exact checks of the general-l spherical constraints; no AF realization."""

from hashlib import sha256
import json
from pathlib import Path

from verify_null_infinity_algebra import sym,imag


def checks():
    r,m,Q,l,lp,w,e,cr,ci,br,bi,pr,pi=map(sym,
        ('r','m','Q','l','lp','w','e','cr','ci','br','bi','pr','pi'))
    ii=sym('i');chi=cr+ii*ci;gradient=br+ii*bi;phi=pr+ii*pi
    chi2=chi*chi.conjugate();grad2=gradient*gradient.conjugate()
    cross=(chi*gradient.conjugate()+chi.conjugate()*gradient)/2
    D=1-2*m/r+r*r*l*l
    jr=-w*cross
    kr=l+r*lp+r*jr
    qp=e*r*r*imag(phi*chi.conjugate())
    mp=Q*Q/(2*r*r)+r*r*D*(chi2+grad2)/2+r**3*l*w*cross
    Dp=D.total(dict(r=1,m=mp,l=lp))
    scalar_curvature=2*(1-D-r*Dp)/r**2
    combination=4*kr*l+2*l*l
    matter=2*(D*(chi2+grad2)+Q*Q/r**4)
    varpi=m+Q*Q/(2*r)
    claims=dict(
        Hamiltonian=scalar_curvature+combination-matter,
        momentum=(kr-l)/r-lp-jr,
        Gauss=w*qp/r**2-e*w*imag(phi*chi.conjugate()),
        renormalized_mass=varpi.total(dict(r=1,m=mp,Q=qp))-
            (r*r*D*(chi2+grad2)/2+r**3*l*w*cross+Q*qp/r),
        expansion_product=(-r*l+w)*(-r*l-w)+(w*w-r*r*l*l))
    for name,value in claims.items():
        if value.terms:raise ArithmeticError('exact constraint identity '+name)
    # Omitting the cross term is only legitimate at l=0 or in special data.
    wrong_mp=mp-r**3*l*w*cross
    wrong_Dp=D.total(dict(r=1,m=wrong_mp,l=lp))
    wrong=2*(1-D-r*wrong_Dp)/r**2+combination-matter
    if not wrong.terms:raise ArithmeticError('missing cross term not rejected')
    R,n,lam,Om,T,nuu,Qu=map(sym,('R','n','lam','Om','T','nuu','Qu'))
    ruv=-n*lam/r-Om*(1-Q*Q/r**2)/(4*r)
    derivative=ruv.total(dict(r=n,n=nuu,lam=ruv,Om=T*Om,Q=Qu))
    at=derivative.substitute(dict(r=R,Q=R,lam=0,Qu=0,Om=1))
    if (at+n/(2*R**2)).terms:raise ArithmeticError('endpoint lambda second derivative')
    ss,xx,hh,AA=map(sym,('s','x','h','AA'))
    young=(hh*xx/2-AA*ss**3)**2-(hh*hh*xx*xx/4+AA*AA*ss**6-hh*AA*ss**3*xx)
    if young.terms:raise ArithmeticError('past-collar Young identity')
    from fractions import Fraction as F
    widths=[]
    for AA,hh,LL,nn,rmin,rmax in [
        (F(1),F(1,8),F(2),F(1,4),F(1,8),F(16)),
        (F(16),F(1,1024),F(128),F(1,128),F(1,128),F(32)),
        (F(1024),F(1,2**20),F(2**14),F(1,2**15),F(1,2**15),F(2**10))]:
        CC=AA+AA*AA/hh;KK=max(F(1),4*CC/hh);BB=LL*KK+AA*(2*KK+1)
        width=F(1,2)
        while not (AA*width<hh/4 and BB*width**4<nn/2 and
                   2*CC*width**3/rmin<nn*nn/(8*rmax*rmax)):
            width/=2
        widths.append(str(width))
    return dict(status='PASS',exact_constraint_identities=list(claims),
                omitted_cross_term_rejected=True,endpoint_lambda_second_derivative=True,
                past_collar_Young_identity=True,past_collar_abstract_test_widths=widths,
                actual_seed_past_collar_constants_effective=False,
                arithmetic='exact rational complex Laurent polynomials',
                actual_Cauchy_ball_constructed=False,full_AF_Cauchy_realization=False,
                global_terminal_state_proved=False,goal_A_proved=False)


def main():
    result=checks();folder=Path(__file__).resolve().parent
    names=['verify_af_outer_extension.py','AF_OUTER_EXTENSION.md','PAST_COLLAR_AND_AF_REALIZATION.md','verify_null_infinity_algebra.py',
           '../../definitions/MODEL.md']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'AF_OUTER_EXTENSION_CHECKS_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
