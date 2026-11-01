"""Independent high-precision checks of the smooth-pulse constraint proof."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import mpmath as mp

from certify_early_charged_constraints import bump_bounds


mp.mp.dps=50


def number(x):
    x=Q(x);return mp.mpf(x.numerator)/x.denominator


def bump(v):
    if v<=0 or v>=1:return mp.mpf(0),mp.mpf(0)
    d=4*v*(1-v);b=mp.exp(1-1/d)
    return b,4*(1-2*v)*b/(d*d)


def rk4(amplitude,frequency,n=1024):
    a,w=number(amplitude),number(frequency);h=-mp.mpf(1)/n
    state=mp.matrix([1,0,0])
    def rhs(v,y):
        b,bp=bump(v);f,p,C=y
        return mp.matrix([p,-a*a*(bp*bp+w*w*b*b)*f,w*a*a*f*f*b*b])
    for j in range(n):
        v=1-mp.mpf(j)/n;k1=rhs(v,state)
        k2=rhs(v+h/2,state+h*k1/2);k3=rhs(v+h/2,state+h*k2/2)
        k4=rhs(v+h,state+h*k3);state+=h*(k1+2*k2+2*k3+k4)/6
    return state[0],state[1],-state[2]


def require(ok,message):
    if not ok:raise ArithmeticError(message)


def main():
    folder=Path(__file__).resolve().parent
    source='EARLY_CHARGED_CONSTRAINT_CERTIFICATE_N2048_2026-10-17.json'
    report=json.loads((folder/source).read_text());comparisons=0;flow=[]
    require(report['status']=='PASS','constraint source failed')
    for name,want in report['source_sha256'].items():
        require(sha256((folder/name).read_bytes()).hexdigest()==want,'stale constraint proof '+name)
    n=2048
    for j in (0,1,32,256,511,1023,1536,2046,2047):
        b2,bp2=bump_bounds(j,n)
        for tau in (Q(0),Q(1,7),Q(1,2),Q(1)):
            v=number((j+tau)/n);b,bp=bump(v)
            for interval,actual in ((b2,b*b),(bp2,bp*bp)):
                require(number(interval.lo)<=actual<=number(interval.hi),'bump interval enclosure')
                comparisons+=1
    for record in report['runs']:
        a,w=Q(record['amplitude']),Q(record['frequency']);coarse=rk4(a,w,512);fine=rk4(a,w,1024)
        for value,key in zip(fine,('initial_f','initial_p','charge_integral')):
            low,high=map(number,record[key]);require(low<value<high,'independent flow enclosure '+key)
        R=1/(mp.mpf(3)/5*fine[2]);lo,hi=map(number,record['radius'])
        require(lo<R<hi,'independent radius enclosure')
        flow.append(dict(amplitude=str(a),frequency=str(w),
            independent_flow_values=[mp.nstr(x,24) for x in fine],
            refinement_differences=[float(abs(a-b)) for a,b in zip(fine,coarse)]))
    result=dict(status='PASS',precision_digits=mp.mp.dps,bump_point_comparisons=comparisons,
        independent_RK4_checks=flow,scope='finite independent audit; rational enclosure supplies the proof',
        complete_PDE_rectangle_certified=False,goal_A_proved=False)
    names=['verify_early_charged_constraints.py','certify_early_charged_constraints.py',source]
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'EARLY_CHARGED_CONSTRAINT_AUDIT_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
