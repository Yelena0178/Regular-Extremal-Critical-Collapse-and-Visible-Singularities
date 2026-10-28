"""Exact finite algebra for A-JET02; no candidate or global PDE certification."""

from hashlib import sha256
import json
from pathlib import Path
from verify_null_infinity_algebra import sym


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def main():
    a,b,c,au,bu,cu,phi,V,P,K = map(sym,
        ('a','b','c','au','bu','cu','phi','V','P','K'))
    pv = -a*V-b*P-c*phi
    # Differentiate the original equation using D_u V = D_v P + 2c phi,
    # then commute D_v D_u P = D_u D_v P - 2c P.
    du = dict(a=au,b=bu,c=cu,phi=P,V=pv+2*c*phi,P=K)
    derived = pv.total(du)-2*c*P
    claimed = -b*K+(a*b-bu-3*c)*P+(a*a-au)*V-(a*c+cu)*phi
    require(not (derived-claimed).terms, 'second jet transport')
    for wrong in (pv.total(du), pv.total(du)+2*c*P):
        require(bool((wrong-claimed).terms), 'wrong commutator accepted')
    r,nu,lam,T,Q,Qu,e,i,PP,ruv = map(sym,
        ('r','nu','lam','T','Q','Qu','e','i','PP','ruv'))
    # Omega^2 has value 1 on the cone, but u derivative T there.
    O=sym('O')
    cu_direct=(i*e*O*Q/(4*r**2)).total(dict(O=O*T,Q=Qu,r=nu))
    cu_formula=i*e*(Qu+Q*(T-2*nu/r))/(4*r**2)
    require(not (cu_direct.substitute(dict(O=1))-cu_formula).terms,'c_u')
    au_formula=(T*nu-r*PP)/r-nu**2/r**2
    bu_formula=ruv/r-nu*lam/r**2
    require(not ((nu/r).total(dict(nu=T*nu-r*PP,r=nu))-au_formula).terms,'a_u')
    require(not ((lam/r).total(dict(lam=ruv,r=nu))-bu_formula).terms,'b_u')
    source=claimed+b*K
    require(not (lam*K+r*claimed.substitute(dict(b=lam/r))
                 -r*source.substitute(dict(b=lam/r))).terms,'integrating factor')
    require(not source.substitute(dict(phi=0,V=0,P=0)).terms,'zero lower jets')
    # Corner data are not a PDE solution certificate. They independently test
    # the covariant jet and show why the arbitrary gauge value cancels there.
    u,h,A,Au=map(sym,('u','h','A','Au'))
    data=h*u**2/2
    first=data.partial('u')+i*e*A*data
    second=first.total(dict(u=1,A=Au))+i*e*A*first
    require(not first.substitute(dict(u=0)).terms,'first corner jet')
    require(not (second.substitute(dict(u=0))-h).terms,'second corner jet')
    base=Path(__file__).resolve().parent
    files=['SECOND_TRANSVERSE_JET.md','verify_second_jet.py',
           'verify_null_infinity_algebra.py','../../definitions/MODEL.md']
    report=dict(status='PASS',arithmetic='exact rational Laurent polynomials',
        identities=['second_jet','c_u','a_u','b_u','integrating_factor',
                    'zero_lower_jets','first_corner_jet','second_corner_jet'],
        rejected_commutator_variants=2, candidate_second_jet_certified=False,
        nonlinear_counterexample_constructed=False, full_goal_A_proved=False,
        source_sha256={name:sha256((base/name).read_bytes()).hexdigest() for name in files})
    (base/'SECOND_JET_CHECKS_2026-10-16.json').write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':
    main()
