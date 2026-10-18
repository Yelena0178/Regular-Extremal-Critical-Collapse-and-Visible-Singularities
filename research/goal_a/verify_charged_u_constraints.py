"""Exact equivalent formulation: propagate mass, scalar and charge in u.

This is algebra only; no new interval rectangle is certified here.
"""

from hashlib import sha256
import json
from pathlib import Path

from verify_null_infinity_algebra import sym,imag


def real(x):return (x+x.conjugate())/2


def main():
    names=('r','k','tr','ti','n','zr','zi','m','pr','pi','Q','A')
    r,k,tr,ti,n,zr,zi,m,pr,pi,Q,A=map(sym,names);ii,e=sym('i'),sym('e')
    theta,z,phi=tr+ii*ti,zr+ii*zi,pr+ii*pi
    f=1-2*m/r;rate=k*(2*m-Q*Q/r)/r**2
    tu=-k*n*f*z/r-ii*e*k*n*Q*phi/r-ii*e*A*theta
    zv=-theta/r-rate*z+ii*e*k*Q*phi/r
    mu=Q*Q*n/(2*r*r)+f*n*z*z.conjugate()/2
    pu=n*z/r-ii*e*A*phi;qu=-e*r*n*imag(phi*z.conjugate())
    mv=Q*Q*k*f/(2*r*r)+theta*theta.conjugate()/(2*k)
    qv=e*r*imag(phi*theta.conjugate())
    E,H,J,Tre,Tim=map(sym,('E','H','J','Tre','Tim'));T=Tre+ii*Tim
    du=dict(zip(names,(n,k*n*z*z.conjugate()/r,real(tu),imag(tu),sym('nuu'),sym('zru'),sym('ziu'),
                       mu,real(pu),imag(pu),qu,sym('Auu'))))
    dv=dict(zip(names,(k*f+E,sym('kv'),sym('trv'),sym('tiv'),rate*n,real(zv),imag(zv),
                       mv+H,real(theta/r+T),imag(theta/r+T),qv+J,2*k*n*Q/r**2)))
    claims=dict(
        radius_v_constraint_u=rate*n-(k*f).total(du),
        scalar_v_constraint_u=pu.total(dv)-(theta/r).total(du)-(-n*z*E/r**2-ii*e*A*T),
        charge_v_constraint_u=qu.total(dv)-qv.total(du)-(-e*n*imag(phi*z.conjugate())*E-e*r*n*imag(T*z.conjugate())),
        mass_v_constraint_u=mu.total(dv)-mv.total(du)-(
            -n*z*z.conjugate()*H/r-(Q*Q*n/r**3-m*n*z*z.conjugate()/r**2)*E+Q*n*J/r**2))
    for name,p in claims.items():
        if p.terms:raise ArithmeticError('u-constraint propagation '+name+': '+str(p.terms)[:500])
    bad=mu-Q*Q*n/(2*r*r)
    if not (bad.total(dv)-mv.total(du)).terms:raise ArithmeticError('omitted electromagnetic term not rejected')
    result=dict(status='PASS',exact_homogeneous_identities=list(claims),
                u_direction_components=['r','kappa','theta_real','theta_imag','m','phi_real','phi_imag','Q'],
                v_direction_components=['nu','z_real','z_imag','A_u'],
                omitted_electromagnetic_mass_term_rejected=True,
                complete_rectangle_certified=False,strict_trapping_certified=False,goal_A_proved=False)
    folder=Path(__file__).resolve().parent
    names=['verify_charged_u_constraints.py','verify_null_infinity_algebra.py','../../definitions/MODEL.md']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'CHARGED_U_CONSTRAINT_CHECKS_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
