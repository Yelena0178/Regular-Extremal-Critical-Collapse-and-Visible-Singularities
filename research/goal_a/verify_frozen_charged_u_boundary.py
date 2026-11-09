"""Independent 80-digit audit of the four additional u-inflow fields."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import mpmath as mp

from frozen_charged_u_boundary import boundary_jets,proposal,exact_mesh,I
from verify_frozen_charged_boundary import number,profile,e
from certify_onset_boundary import hermite


def target(piece,V):
    fields,q,phi=profile(piece,V);r,k,tr,ti=fields
    rv=mp.diff(lambda at:profile(piece,at)[0][0],V)
    return (*fields,r*(1-rv/k)/2,phi.real,phi.imag,q)


def require(ok,message):
    if not ok:raise ArithmeticError(message)


def main():
    folder=Path(__file__).resolve().parent;source='FROZEN_CHARGED_U_BOUNDARY_2026-10-17.json'
    cert=json.loads((folder/source).read_text());count=0;identities=0
    for piece in range(3):
        mesh=exact_mesh(96,piece);errors=[Q(a) for a in cert['pieces'][piece]['errors']]
        for j in (0,48,95):
            left,right=mesh[j],mesh[j+1];h=right-left
            va,da=proposal(float(left),piece);vb,db=proposal(float(right),piece)
            polys=[hermite(va[k],vb[k],da[k],db[k],h) for k in range(8)]
            for tau in (Q(1,7),Q(1,2),Q(1)):
                at=left+h*tau;V=number(at);jets=boundary_jets(piece,I(at))
                for k in range(4,8):
                    for order in range(5):
                        actual=mp.diff(lambda x:target(piece,x)[k],V,order)/mp.factorial(order)
                        require(number(jets[k].c[order].lo)<=actual<=number(jets[k].c[order].hi),
                            f'u-boundary jet {piece},{j},{k},{order}');count+=1
                for k in range(8):
                    poly=sum((number(c)*number(tau)**p for p,c in enumerate(polys[k])),mp.mpf(0))
                    require(abs(target(piece,V)[k]-poly)<=number(errors[k]),'u-boundary Hermite error')
                rr,kk,tr,ti,m,pr,pi,q=target(piece,V);theta=tr+1j*ti;phi=pr+1j*pi
                mv=mp.diff(lambda x:target(piece,x)[4],V)
                require(abs(mv-q*q*kk*(1-2*m/rr)/(2*rr*rr)-abs(theta)**2/(2*kk))<mp.mpf('1e-58'),
                    'outgoing mass constraint');identities+=1
                require(abs(mp.diff(lambda x:target(piece,x)[7],V)-e*rr*mp.im(phi*mp.conj(theta)))<mp.mpf('1e-58'),
                    'outgoing charge constraint');identities+=1
    result=dict(status='PASS',extra_jet_enclosures=count,outgoing_constraint_checks=identities,
        precision_digits=mp.mp.dps,scope='independent finite audit; rational Taylor supplies continuum coverage',
        complete_rectangle_certified=False,goal_A_proved=False)
    names=['verify_frozen_charged_u_boundary.py','frozen_charged_u_boundary.py',
        'verify_frozen_charged_boundary.py','frozen_charged_boundary.py',source]
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'FROZEN_CHARGED_U_BOUNDARY_AUDIT_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
