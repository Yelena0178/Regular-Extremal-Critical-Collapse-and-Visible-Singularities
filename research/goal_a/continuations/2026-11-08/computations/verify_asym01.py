"""Exact rational ray certificate plus finite transverse quadrature controls."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,sys,platform
import numpy as np
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1]
N=8; R=F(2);C=F(1,20);coupling=F(3,5);amp=F(1,10)
c=[F(1)]
for n in range(1,N+2):c.append(-C*c[-1]/(4*n*(4*n+1)))
assert abs(c[1])==F(1,400)
assert F(3,500)*F(399,400)**2>F(1,200)
assert F(997,500)>0
assert F(9,40000)==coupling**2*amp**2/(8*R**2*F(1,4)*2)
# Q polynomial is the exact integral of the squared truncated radius.
d=[sum((c[i]*c[n-i] for i in range(max(0,n-N),min(N,n)+1)),F(0)) for n in range(2*N+1)]
qdef=[coupling*amp**2*R**2*d[n]/(4*(n+1)) for n in range(2*N+1)]
r_error=R*abs(c[N+1])
q_error=coupling*amp**2*2*R**2*abs(c[N+1])/(4*(N+2))
certificate=dict(scope='all t>=1 exact rational series remainder bounds for ray r and Q only',radius_error_bound_at_t1=str(r_error),radius_error_power=4*(N+1),charge_error_bound_at_t1=str(q_error),charge_error_power=4*(N+2),positive_radius_lower='399/200',positive_charge_lower='997/500',Q_less_than_r_margin_coefficient=str(F(3,500)*F(399,400)**2-F(1,200)),arithmetic='Python Fraction exact rational arithmetic; analytic alternating-series and integral bounds in ASYM01',actual_spacetime_certified=False)

def radial(t):
    deficit=-sum(2*float(c[n])*t**(-4*n) for n in range(1,N+1))
    rp=sum(-8*n*float(c[n])*t**(-4*n-1) for n in range(1,N+1))
    rpp=sum(8*n*(4*n+1)*float(c[n])*t**(-4*n-2) for n in range(1,N+1))
    dq=sum(float(a)*t**(-4*(n+1)) for n,a in enumerate(qdef))
    qp=sum(4*(n+1)*float(a)*t**(-4*(n+1)-1) for n,a in enumerate(qdef))
    return 2-deficit,rp,rpp,2-dq,qp,deficit,dq

def D(t):
    r,_,_,q,_,dr,dq=radial(t)
    return (dq-dr)*(4-dr-dq)/(r*r)

def nu(t):
    r=radial(t)[0]
    return (-1+.25*quad(D,t,np.inf,epsabs=1e-13,epsrel=1e-11)[0])/r

def field(t): return .1*t**complex(-2,-1)
def field_prime(t):return complex(-2,-1)*field(t)/t
def P(t):
    def remainder(x):
        r,_,_,q,_,dr,dq=radial(x)
        return (nu(x)+.5)*field_prime(x)+.15j*(dr-dq)/r*field(x)
    integ=quad(lambda x:remainder(x).real,t,np.inf,epsabs=1e-13)[0]+1j*quad(lambda x:remainder(x).imag,t,np.inf,epsabs=1e-13)[0]
    return (.015j/(1+1j)*t**complex(-1,-1)+.5*field(t)+integ)/radial(t)[0]

records=[]
for t in [1.,2.,4.,8.,16.,64.]:
    r,rp,rpp,q,qp,dr,dq=radial(t);n=nu(t);p=P(t)
    rayerr=abs(rpp+.05*t**-6*r)
    qerr=abs(qp-.006*r*r*t**-5)
    h=1e-3*t
    pd=(P(t+h)-P(t-h))/(2*h)
    nd=(nu(t+h)-nu(t-h))/(2*h)
    wave=abs(r*pd+rp*p+n*field_prime(t)+.15j*q*field(t)/r)
    mixed=abs(r*nd+rp*n+D(t)/4)
    # Finite differences are only controls; tolerance scales with tail size.
    assert rayerr<1e-15 and qerr<1e-16
    assert wave<3e-7*t**-2 and mixed<2e-7*t**-4
    ric=2*abs(p/n)**2
    gap=(r-q)**2/(2*r)+2*r*n*rp
    records.append(dict(t=t,r=r,Q=q,lambda_affine=rp,nu=n,P_real=p.real,P_imag=p.imag,ric_nn=ric,scaled_ric=ric*t*t,scaled_local_mass_gap=gap*t**5,ray_residual=rayerr,maxwell_residual=qerr,transverse_wave_finite_difference_residual=wave,mixed_radius_finite_difference_residual=mixed))
out=dict(passed=True,exact_ray_certificate=certificate,finite_controls=records,limits=dict(scaled_ric=9/40000,scaled_local_mass_gap=-1/25),scope='constraint-series certificate and finite quadrature checks; no neighborhood, center, event horizon, Bondi or PDE error certificate',goal_A_proved=False,environment=dict(python=sys.version,numpy=np.__version__,platform=platform.platform()),source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'proofs/ASYM01_AFFINE_RAY_AND_TRANSVERSE_TAIL.md']})
dest=ROOT/'results/ASYM01_RAY_CHECKS.json'
if dest.exists():raise FileExistsError(dest)
dest.write_text(json.dumps(out,indent=2)+'\n')
cert=ROOT/'certificates/ASYM01_RATIONAL_RAY.json'
if cert.exists():raise FileExistsError(cert)
cert.write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps(dict(certificate=certificate,finite_controls=records),indent=2))
