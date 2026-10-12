"""Finite algebra supporting the analytic proof, not its certification."""
import json
from pathlib import Path
import sympy as s

results=[]
def identity(name, expr):
    assert s.simplify(expr)==0, (name,s.simplify(expr))
    results.append({'name':name,'status':'PASS'})
def positive(name, expr):
    assert s.simplify(expr).is_positive is True, (name,expr)
    results.append({'name':name,'status':'PASS'})

O, p, delta, G, margin, du, dw=s.symbols('O p delta G margin du dw',positive=True)
inv=s.Matrix([[0,-2/O],[-2/O,0]])
cov=s.Matrix([1,p])  # sigma'=-p
identity('timelike graph barrier norm',(cov.T*inv*cov)[0]+4*p/O)
positive('lower boundary margin',G+delta)
positive('upper boundary past margin',margin+du+dw)
zprime=s.symbols('zprime',positive=True)
positive('unique center crossing derivative',zprime+p)

r=s.symbols('r',positive=True)
F=(1-1/r)**2
rs=r+2*s.log(r-1)-1/(r-1)
identity('static tail tortoise',s.diff(rs,r)-1/F)
identity('static tail induced metric',-F/F**2+2/F-1/F)
rho, rho_prime, k=s.symbols('rho rho_prime k',positive=True)
Fr=(1-1/rho)**2
# Here rho'= -rho_prime; b'= -2 rho'/F(rho).
bprime=2*rho_prime/Fr
identity('RN graph derivative',-k/bprime+k*Fr/(2*rho_prime))

# Project phi=sqrt(4pi) times Kommemi psi; constant scaling
# commutes with every covariant derivative.
psi2,current,re_cross=s.symbols('psi2 current re_cross')
norm=1/(4*s.pi)
identity('Kommemi Raychaudhuri normalization',4*s.pi*norm*psi2-psi2)
identity('Kommemi Maxwell normalization',4*s.pi*norm*current-current)
identity('Kommemi log lapse normalization',8*s.pi*norm*re_cross-2*re_cross)

U,v,ub,T=s.symbols('U v ub T')
# ub=b(U)=v-2rstar; b(sigma)=2T-v. Since b is increasing,
# U>=sigma is equivalent to ub>=2T-v, i.e. static time>=T.
identity('future of static tail condition',(v+ub)/2-T-(v+ub-2*T)/2)
identity('extremal surface gravity',s.diff(F,r).subs(r,1)/2)

report={'scope':'finite identities and sign bookkeeping only; analytic G-A/G-B proved in prose',
        'sympy':s.__version__,'results':results}
Path(__file__).with_name('RESULTS_GA_GB.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
