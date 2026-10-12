"""Independent exact L2 input check; this is not a finite endpoint solver."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
import sys

def multiply(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def main(source,destination):
    data=json.loads(source.read_text())
    re=[F(x) for x in data['polynomial_real']]
    im=[F(x) for x in data['polynomial_imag']]
    rr=multiply(re,re);ii=multiply(im,im)
    length=max(len(rr),len(ii));rr += [F(0)]*(length-len(rr));ii += [F(0)]*(length-len(ii))
    squared_norm=sum(((rr[j]+ii[j])*factorial(j)*10**(j+1) for j in range(length)),F(0))/F(data['E_total'])
    assert 0<squared_norm<16
    result=dict(status='EXACT_UNTRUNCATED_PROFILE_L2_BOUND_PASS',squared_L2_norm=str(squared_norm),L2_norm_upper='4',scope='Leading normalized w only; not a finite-amplitude root.')
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],squared_L2_display=float(squared_norm))))

if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
