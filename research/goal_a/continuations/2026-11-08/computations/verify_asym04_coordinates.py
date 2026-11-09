import sympy as s,json,hashlib
from pathlib import Path
x,y,R=s.symbols('x y R',positive=True)
T=2*(y-x)+4*R*s.log(y/x)+2*R**2*(1/x-1/y)
assert s.simplify(s.diff(T,y)-2*(R+y)**2/y**2)==0
assert s.simplify(T.subs(y,x))==0
assert s.limit(T*x,x,0,dir='+')==2*R**2
p=Path('reviews/ASYM04_EXTERIOR_REALIZATION_GATE.md')
out=dict(passed=True,scope='exact extremal RN comparison only, not ASYM exterior existence',checks=['travel-time primitive','zero interval','shrinking-label asymptotic'],source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest()},goal_A_proved=False)
Path('results/ASYM04_COORDINATE_CHECKS.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
