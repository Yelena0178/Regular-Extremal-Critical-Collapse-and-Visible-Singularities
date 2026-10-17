"""Cross-check variable-width cell bounds against exact rational arithmetic."""

from fractions import Fraction as Q
import json
import numpy as np
from thin_onset_reference import boundaries
from thin_boundary_certificate import trig
from graded_transport import mesh,evolve,derivatives
from interval_transport_grid import V,coefficients,cell_bounds
from rational_transport_cell import hermite_cell,cell_quantities
from verify_horizon_seed import trig_half
from verify_interval_transport_grid import require,contains,arithmetic_checks


def main():
    arithmetic=arithmetic_checks();oldc,olds=trig_half();c,s=trig(Q(1,2))
    require(c.lo<=oldc.lo and c.hi>=oldc.hi and s.lo<=olds.lo and s.hi>=olds.hi,'independent trig enclosure')
    out,inc,p,_=boundaries();v=mesh(p['v_cap'],31*p['v_end']/32,16)
    data=evolve(out,inc,p['v_end']/2,v,16);x=data['state'];xu,xv,xuv=derivatives(data,v)
    hu=Q(p['v_end']/2)/16;records=[]
    for i,j in [(3,0),(8,12),(15,len(v)-2)]:
        sl=(slice(i,i+2),slice(j,j+2));hv=v[j+1]-v[j]
        exact=hermite_cell(x[sl].tolist(),xu[sl].tolist(),xv[sl].tolist(),xuv[sl].tolist(),hu,hv)
        pol=coefficients(x[sl],xu[sl],xv[sl],xuv[sl],V.rational(hu),V.rational(hv))
        for k,ep in enumerate(exact):
            terms={}
            for monomial,value in ep.terms.items():
                d=dict(monomial);terms[d.get('u',0),d.get('v',0)]=value
            for a in range(4):
                for b in range(4):require(contains(pol[0,0,k,a,b],terms.get((a,b),Q(0))),'graded coefficient')
        B,delta=cell_bounds(pol,V.rational(hu),V.rational(hv))
        Br,dr,_=cell_quantities(exact,hu,hv,[Q(1,1000)]*6)
        for k in range(6):
            require(Q(float(B.lo[0,0,k]))<=Br[k][0] and Q(float(B.hi[0,0,k]))>=Br[k][1],'graded Bernstein')
            require(Q(float(delta[0,0,k]))>=dr[k],'graded residual')
        records.append(dict(cell=[i,j],width=str(hv),exact_coefficients=96))
    require(all(b>a for a,b in zip(v,v[1:])),'strict mesh')
    require(np.all(x[:,0,3:]==[-.5,0,0]) and np.all(xu[:,0,3:]==0),'exact incoming edge')
    print(json.dumps(dict(status='PASS',arithmetic=arithmetic,cells=records),indent=2))


if __name__=='__main__':main()
