"""Exact constraint propagation algebra and E0 independent charged benchmarks."""

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from charged_characteristic_screen import rhs,evolve
from verify_null_infinity_algebra import sym,imag
from verify_neutral_transport import evaluate as polynomial_value,flrw_state


def require(condition,message):
    if not condition:raise ArithmeticError(message)


def real(p):return (p+p.conjugate())/2


def algebra():
    names=('r','k','tr','ti','n','zr','zi','m','pr','pi','Q','A')
    r,k,tr,ti,n,zr,zi,m,pr,pi,Q,A=map(sym,names)
    e,ii=sym('e'),sym('i')
    t,z,p=tr+ii*ti,zr+ii*zi,pr+ii*pi
    f=1-2*m/r; a=k*(2*m-Q*Q/r)/r**2
    tu=-k*n*f*z/r-ii*e*k*n*Q*p/r-ii*e*A*t
    zv=-t/r-a*z+ii*e*k*Q*p/r
    pv=t/r; qv=e*r*imag(p*t.conjugate()); av=2*k*n*Q/r**2
    field=(n,k*n*z*z.conjugate()/r,real(tu),imag(tu),a*n,real(zv),imag(zv),
           Q*Q*k*f/(2*r**2)+t*t.conjugate()/(2*k),real(pv),imag(pv),qv,av)
    E,G,C,Sr,Si=map(sym,('E','G','C','Sr','Si'))
    S=Sr+ii*Si
    H=Q*Q*n/(2*r**2)+f*n*z*z.conjugate()/2
    q_u=C-e*r*n*imag(p*z.conjugate())
    p_u=n*z/r-ii*e*A*p+S
    du=dict(zip(names,(n,field[1],field[2],field[3],sym('nuu'),sym('zru'),sym('ziu'),
                       H+G,real(p_u),imag(p_u),q_u,sym('Auu'))))
    dv=dict(zip(names,(k*f+E,sym('kv'),sym('trv'),sym('tiv'),field[4],field[5],field[6],
                       field[7],field[8],field[9],field[10],field[11])))
    Eu=field[4]-(k*f).total(du)
    Gv=field[7].total(du)-H.total(dv)
    Cv=qv.total(du)+(e*r*n*imag(p*z.conjugate())).total(dv)
    Sv=pv.total(du)+ii*e*(av*p+A*pv)-(n*z/r).total(dv)
    claims={
        'E_u':Eu-2*k*G/r,
        'G_v':Gv-(-k*Q*Q*G/r**3+(Q*Q*n/r**3-m*n*z*z.conjugate()/r**2)*E+Q*k*f*C/r**2),
        'charge_constraint_v':Cv-(e*n*imag(p*z.conjugate())*E+e*r*imag(S*t.conjugate())),
        'scalar_constraint_v':Sv-n*z*E/r**2,
    }
    physical_du=dict(du,m=H,Q=-e*r*n*imag(p*z.conjugate()),
                     pr=real(n*z/r-ii*e*A*p),pi=imag(n*z/r-ii*e*A*p))
    physical_dv=dict(dv,r=k*f)
    claims['conformal_Einstein']=(n*z*z.conjugate()/r).total(physical_dv)+a.total(physical_du)-(
        -2*n*real(z*t.conjugate())/r**2-4*k*m*n/r**3+4*k*n*Q*Q/r**4)
    for name,expression in claims.items():
        require(not expression.terms,'charged identity '+name+': '+str(expression.terms)[:500])
    # Reverse just one imaginary charged term: both real and imaginary scalar
    # constraint identities must fail, rather than passing a neutral-only test.
    wrong_tu=-k*n*f*z/r+ii*e*k*n*Q*p/r-ii*e*A*t
    bad_du=dict(du,tr=real(wrong_tu),ti=imag(wrong_tu))
    bad=pv.total(bad_du)+ii*e*(av*p+A*pv)-(n*z/r).total(dv)-n*z*E/r**2
    require(bool(bad.terms),'wrong charged wave sign accepted')
    for sample in range(1,8):
        point=dict(zip(names,(F(7+sample,3),F(2,5),F(sample,13),-F(sample,17),-F(3,7),
                              F(2,11),-F(sample,19),F(2,3),F(sample,23),F(3,29),F(4,5),F(2,7))))
        point['e']=F(3,5)
        expected=np.array([complex(polynomial_value(q,dict(point,i=1j))).real for q in field])
        observed=rhs(np.array([float(point[name]) for name in names]))
        require(np.max(abs(expected-observed))<2e-14,'charged numerical rhs disagrees with exact polynomial')
    return dict(status='PASS',exact_identities=list(claims),wrong_charged_wave_sign_rejected=True,
                nonzero_charged_rhs_comparisons=7,
                arithmetic='exact rational complex Laurent polynomials')


def rn_benchmark(graded=False):
    M,Q,R=2.,1.,8.
    def flow(s,r):return [(1-2*M/r[0]+Q*Q/r[0]**2)/2]
    forward=solve_ivp(flow,(0.,.8),[R],method='DOP853',rtol=2e-13,atol=2e-14,dense_output=True)
    backward=solve_ivp(flow,(0.,-.5),[R],method='DOP853',rtol=2e-13,atol=2e-14,dense_output=True)
    def exact(u,v):
        s=v-u;r=float((forward if s>=0 else backward).sol(s)[0])
        f=1-2*M/r+Q*Q/r**2
        return np.array([r,.5,0.,0.,-f/2,0.,0.,M-Q*Q/(2*r),0.,0.,Q,Q/r])
    runs=[]
    for n in (16,32,64):
        if graded:
            v=np.array([0.]+[.025*2**(j-6) for j in range(7)]+
                       list(np.linspace(.025,.8,n+1)[1:]))
        else:
            v=np.linspace(0.,.8,n+1)
        data=evolve(lambda v:exact(0,v),lambda u:exact(u,0),.5,v,n)
        error=np.max(abs(data['state'][-1,-1]-exact(.5,.8)))
        runs.append(dict(n=n,endpoint_max_error=float(error)))
    for a,b in zip(runs,runs[1:]):require(b['endpoint_max_error']<a['endpoint_max_error']/3.5,'RN convergence')
    return runs


def flrw_benchmark():
    def exact(u,v):
        r,k,t,n,z,m=flrw_state(u,v)
        phi=np.sqrt(3)/2*np.log(1-(u+v)/8)
        return np.array([r,k,t,0.,n,z,0.,m,phi,0.,0.,0.])
    runs=[]
    for n in (16,32,64):
        v=np.linspace(2.6,4.7,n+1)
        data=evolve(lambda v:exact(0,v),lambda u:exact(u,2.6),2.2,v,n)
        error=np.max(abs(data['state'][-1,-1]-exact(2.2,4.7)))
        runs.append(dict(n=n,endpoint_max_error=float(error)))
    for a,b in zip(runs,runs[1:]):require(b['endpoint_max_error']<a['endpoint_max_error']/3.,'FLRW convergence')
    return runs


def main():
    result=dict(status='PASS',algebra=algebra(),RN=rn_benchmark(),RN_graded=rn_benchmark(True),FLRW=flrw_benchmark(),
                scope='finite exact algebra and E0 known-solution comparisons',
                actual_candidate_PDE_certified=False,goal_A_proved=False)
    folder=Path(__file__).resolve().parent
    names=['verify_charged_characteristic.py','charged_characteristic_screen.py',
           'verify_null_infinity_algebra.py','verify_neutral_transport.py']
    result['source_sha256']={name:sha256((folder/name).read_bytes()).hexdigest() for name in names}
    (folder/'CHARGED_CHARACTERISTIC_CHECKS_2026-10-17.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2))


if __name__=='__main__':main()
