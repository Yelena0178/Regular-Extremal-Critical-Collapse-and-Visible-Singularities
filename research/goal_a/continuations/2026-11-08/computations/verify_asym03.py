"""Exact commutator identities and finite second-jet ODE controls; no PDE certificate."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]

# Independent operator calculation in radial electromagnetic gauge A_r=0.
v,r,e=sp.symbols('v r e',real=True,nonzero=True)
ph=sp.Function('phi')(v,r);av=sp.Function('av')(v,r)
la=sp.Function('lam')(v,r);E=sp.Function('E')(v,r)
c=-e*sp.diff(av,r)/2  # F_vr=-partial_r av, hence 2c=eF_vr.
Dv=lambda x:sp.diff(x,v)+sp.I*e*av*x
DL=lambda x:Dv(x)+la*sp.diff(x,r)
U=sp.diff(ph,r);H=sp.diff(ph,r,2);W=DL(ph)
res1=DL(U)+W/r+E*U-sp.I*c*ph
rhs2=-(sp.diff(la,r)+E)*H+2*W/r**2+((E-sp.diff(la,r))/r-sp.diff(E,r)+3*sp.I*c)*U+sp.I*(sp.diff(c,r)+c/r)*ph
res2=DL(H)-rhs2
assert sp.simplify(res2-(sp.diff(res1,r)-res1/r))==0
# A divergence-form charged wave equation gives the first transport law.
wave=Dv(r*r*U)+sp.diff(r*r*Dv(ph)+2*la*r*r*U,r)
assert sp.simplify(wave/(2*r*r)-res1.subs(E,sp.diff(la,r)+la/r))==0
# Negative control: delete electromagnetic contribution to the moving commutator.
wrong=rhs2-2*sp.I*c*U-2*sp.I*c*ph/r
assert sp.simplify((DL(H)-wrong)-(sp.diff(res1,r)-res1/r))!=0
u1=-sp.Rational(3,400)*(1+sp.I)
f1=(-sp.Rational(1,4)+sp.Rational(9,20)*sp.I)*u1
assert sp.simplify(sp.I*f1-(sp.Rational(3,2000)+sp.Rational(21,4000)*sp.I))==0

# Reuse only the existing coefficient/functions prefix; never execute old verification/output.
old=ROOT/'computations/verify_asym01.py'
source=old.read_text(encoding='utf-8')
assert source.count('\nrecords=[]')==1
ns={'__file__':str(old)}
exec(compile(source.split('\nrecords=[]')[0],str(old),'exec'),ns)
radial=ns['radial'];field=ns['field'];field_prime=ns['field_prime'];D=ns['D']
receipt=json.loads((ROOT/'results/ASYM01_RAY_CHECKS.json').read_text())
assert receipt['source_sha256']['computations\\verify_asym01.py']==hashlib.sha256(old.read_bytes()).hexdigest()
initial=receipt['finite_controls'][0]
y0=[initial['nu'],initial['P_real'],initial['P_imag'],0.,0.,1.]

def coefficients(t,y):
    rad,lam,_,q,_,_,_=radial(t);n=y[0];p=complex(y[1],y[2]);h=complex(y[3],y[4])
    phi=field(t);w=field_prime(t);b=-1/(2*n);u=p/n
    br=b*rad*abs(u)**2;qr=-.6*rad*rad*np.imag(phi*np.conj(u))
    dd=D(t);ee=b*dd/(2*rad);cc=.3*b*q/rad**2;lr=ee-lam/rad
    er=br*dd/(2*rad)+b*(-2*q*qr/rad**2+2*q*q/rad**3)/(2*rad)-b*dd/(2*rad**2)
    cr=.3*(br*q/rad**2+b*qr/rad**2-2*b*q/rad**3)
    hp=-(lr+ee)*h+2*w/rad**2+((ee-lr)/rad-er+3j*cc)*u+1j*(cr+cc/rad)*phi
    np_=-n*lam/rad-dd/(4*rad)
    pp=-n*w/rad-lam*p/rad-.15j*q*phi/rad**2
    brr=b*rad**2*abs(u)**4+b*abs(u)**2+2*b*rad*np.real(h*np.conj(u))
    lrr=er-lr/rad+lam/rad**2
    arr=2*lam*brr+4*br*lr+2*b*lrr
    return np_,pp,hp,-(lr+ee)*y[5],dict(B=b,B_r=br,B_rr=brr,A_rr=arr,U_abs=abs(u),H_real=h.real,H_imag=h.imag,H_abs=abs(h),a=lr+ee)

def ode(t,y):
    n,p,h,g,_=coefficients(t,y)
    return [n,p.real,p.imag,h.real,h.imag,g]

times=[1.,2.,4.,16.,64.,256.,1024.]
sols=[]
for tol in [2e-10,2e-12]:
    sol=solve_ivp(ode,(1.,1024.),y0,method='DOP853',rtol=tol,atol=tol/100,max_step=4.,t_eval=times)
    assert sol.success
    sols.append(sol)
error=float(np.max(abs(sols[0].y-sols[1].y)))
assert error<1e-7
records=[];h1=.0015+.00525j
for t,y in zip(times,sols[-1].y.T):
    data=coefficients(t,y)[-1]
    h=complex(y[3],y[4]);comp=h-h1*t**(-1j)
    data.update(t=t,H_compensated_real=comp.real,H_compensated_imag=comp.imag,homogeneous_multiplier=float(y[5]))
    records.append(data)
out=dict(passed=True,scope='symbolic transport and finite along-ray jet ODE; no fixed-width neighborhood or actual PDE certificate',symbolic_checks=['charged wave divergence to U transport','moving electromagnetic commutator to H transport','wrong commutator rejected','oscillatory leading coefficient'],initial_H=[0,0],other_finite_H0='add homogeneous_multiplier*H0; analytic bounds proved separately',times=times,max_tolerance_comparison_difference=error,records=records,goal_A_proved=False,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),old,ROOT/'results/ASYM01_RAY_CHECKS.json',ROOT/'proofs/ASYM03_REGULAR_SECOND_DERIVATIVES.md']})
dest=ROOT/'results/ASYM03_SECOND_JET_CHECKS.json'
if dest.exists():raise FileExistsError(dest)
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
