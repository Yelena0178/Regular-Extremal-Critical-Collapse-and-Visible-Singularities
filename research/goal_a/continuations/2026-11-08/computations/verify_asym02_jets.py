import sympy as s,json,hashlib
from pathlib import Path
r,n,l,q,o,L,nuu,qu,lu=s.symbols('r n l q o L nuu qu lu', real=True, nonzero=True)
D=1-q*q/r**2
f=-n*l/r-o*D/(4*r)
partials={r:n,n:nuu,l:lu,q:qu,o:o*L}
du=lambda expr:s.expand(sum(s.diff(expr,x)*v for x,v in partials.items()))
expected=-nuu*l/r-n*lu/r+n*n*l/r**2-o*L*D/(4*r)+o*n*D/(4*r*r)+o*q*qu/(2*r**3)-o*q*q*n/(2*r**4)
assert s.simplify(du(f)-expected)==0
p2=s.symbols('p2',nonnegative=True)
B=-o/(2*n)
assert s.simplify((du(B)/n).subs(nuu,L*n-r*p2)-B*r*p2/n**2)==0
h,j=s.symbols('h j',real=True)
m=r/2+2*r*n*l
M=m+q*q/(2*r)
Mprime=sum(s.diff(M,x)*v for x,v in {r:l,n:-n*l/r-D/(4*r),l:-r*h,q:j}.items())
assert s.simplify(Mprime-(-2*r*r*n*h+q*j/r))==0
assert s.Rational(1,8000)**2/(2*s.Rational(1,50)*s.Rational(1,16))==s.Rational(1,160000)
paths=[Path('proofs/ASYM01_AFFINE_RAY_AND_TRANSVERSE_TAIL.md'),Path('proofs/ASYM02_TRANSVERSE_SECOND_JET.md')]
out=dict(passed=True,checks=['full transverse second lambda derivative including conformal derivative','regular EF B radial derivative cancellation','renormalized mass null flux identity','Taylor polynomial relative loss coefficient'],source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},scope='exact symbolic identities, not transverse neighborhood existence',goal_A_proved=False)
Path('results/ASYM02_JET_CHECKS.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
