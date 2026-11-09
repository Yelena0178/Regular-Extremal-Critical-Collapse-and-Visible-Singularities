"""Independent pointwise audits of the uniform parameter boundary proof."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from thin_onset_reference import boundaries
from graded_transport import mesh,v_derivative
from thin_parameter_boundary import certify,geometry_box
from thin_boundary_certificate import trig
from certify_onset_boundary import hermite


def require(ok,message):
    if not ok:raise ArithmeticError(message)


def polynomial(poly,t):
    return sum((a*t**i for i,a in enumerate(poly)),Q(0))


def main():
    base=Path(__file__).resolve().parent
    old,fixed,ar,length,box=geometry_box(base)
    out,_,p,_=boundaries();v=mesh(p['v_cap'],31*p['v_end']/32)
    values=np.array([out(float(w)) for w in v]);slopes=v_derivative(values[None],v)[0]
    b,report=certify(values,slopes,v,base)
    count=0
    for a,L in [(ar.lo,length.lo),(ar.lo,length.hi),(ar.hi,length.lo),(ar.hi,length.hi),
                (fixed['r0'],fixed['length'])]:
        q=fixed['amplitude']/L
        for j in [0,1,12,100,len(v)-2]:
            h=v[j+1]-v[j]
            polys=[hermite(values[j,k],values[j+1,k],slopes[j,k],slopes[j+1,k],h) for k in range(3)]
            for tau in [Q(1,3),Q(1,2),Q(1)]:
                at=v[j]+h*tau;t=at-fixed['cap'];c,s=trig(q*t)
                r=a*c+s/(2*q);physical_v=at+2*(a-fixed['r0'])
                for k,true in enumerate([r,r/physical_v,r*q]):
                    diff=true-polynomial(polys[k],tau)
                    require(max(abs(diff.lo),abs(diff.hi))<=Q(float(b[j+1,k])),
                            'C0 state outside uniform bound')
                    count+=1
        require(a/(fixed['cap']+2*(a-fixed['r0']))==Q(1,2),'translated vacuum kappa')
    require(ar.lo/fixed['cap']!=Q(1,2),'untranslated denominator negative control')
    sources=['verify_thin_parameter_transfer.py','thin_parameter_boundary.py','thin_boundary_certificate.py',
             'graded_transport.py','thin_onset_reference.py','ONSET_BOUNDARY_CERTIFICATE_2026-10-16.json']
    result=dict(status='PASS',independent_interval_point_comparisons=count,
                auxiliary_limit_strictly_in_box=box['auxiliary_limit_strictly_inside'],
                translated_vacuum_identity=True,negative_controls=1,
                note='Finite audit; continuum coverage comes from the analytic interval construction.',
                source_sha256={name:sha256((base/name).read_bytes()).hexdigest() for name in sources})
    (base/'THIN_PARAMETER_AUDIT_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
