"""Small exact Laurent-polynomial differentiator, no CAS dependency."""
from fractions import Fraction as F
class P:
 def __init__(self,x=0):self.d=x if isinstance(x,dict) else ({():F(x)} if x else {})
 def __add__(self,o):
  if not isinstance(o,P):o=P(o)
  d=self.d.copy()
  for k,v in o.d.items():d[k]=d.get(k,F(0))+v
  return P({k:v for k,v in d.items() if v})
 __radd__=__add__
 def __neg__(self):return P({k:-v for k,v in self.d.items()})
 def __sub__(self,o):return self+-co(o)
 def __rsub__(self,o):return co(o)+-self
 def __mul__(self,o):
  o=co(o);d={}
  for k,v in self.d.items():
   for l,w in o.d.items():
    a=dict(k)
    for j,n in l:a[j]=a.get(j,0)+n
    z=tuple(sorted((j,n) for j,n in a.items() if n));d[z]=d.get(z,F(0))+v*w
  return P({k:v for k,v in d.items() if v})
 __rmul__=__mul__
 def __pow__(self,n):
  if n<0:
   assert len(self.d)==1
   (k,v),=self.d.items();return P({tuple((j,n*m) for j,m in k):v**n})
  r=P(1)
  for _ in range(n):r=r*self
  return r
 def __truediv__(self,o):return self*co(o)**-1
 def __eq__(self,o):return self.d==co(o).d
 def derivative(self,rules):
  out=P()
  for k,v in self.d.items():
   for name,n in k:
    if name not in rules:continue
    a=dict(k);a[name]-=1;a=tuple(sorted((j,m) for j,m in a.items() if m))
    out=out+P({a:v*n})*rules[name]
  return out
def co(o):return o if isinstance(o,P) else P(o)
def var(s):return P({((s,1),):F(1)})
r,al,r2,Q,Q1,Q2,O,ell,ell2,be,av,p1,P1,p2,P2,z,Z,v,V,w,W=map(var,'r al r2 Q Q1 Q2 O ell ell2 be av p1 P1 p2 P2 z Z v V w W'.split())
rules={'r':al,'al':r2,'Q':Q1,'Q1':Q2,'O':O*ell,'ell':ell2,'be':av,'p1':p2,'P1':P2,'z':p1,'Z':P1,'v':w,'V':W}
def du(p):return p.derivative(rules)
for n in (1,2):
 H=Q/r**n
 expected=Q2/r**n-2*n*Q1*al/r**(n+1)-n*Q*r2/r**(n+1)+n*(n+1)*Q*al**2/r**(n+2)
 assert du(du(H))==expected
 assert du(du(O*H))==O*((ell**2+ell2)*H+2*ell*du(H)+expected)
LV=O/(2*r**2)+2*al*be/r**2-O*Q**2/r**4-(p1*V+P1*v)
expected=O*ell/(2*r**2)-O*al/r**3+(2*r2*be+2*al*av)/r**2-4*al**2*be/r**3-O*(Q**2*ell+2*Q*Q1)/r**4+4*O*Q**2*al/r**5-(p2*V+P2*v+p1*W+P1*w)
assert du(LV)==expected
assert du(r**2*(z*P1-Z*p1))==2*r*al*(z*P1-Z*p1)+r**2*(z*P2-Z*p2)
print('PASS exact symbolic quotient, lapse, and second Maxwell derivatives.')
# Moment kernels: polynomial in lambda, with formal i satisfying i^2=-1.
# Check complex coefficients using exact rational pairs at 4 distinct lambda values.
# All identities have degree <=3, so these evaluations prove the polynomial identities.
def cmul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
for e in map(F,(1,2,3,4)):
 d3=cmul((0,e/128),cmul((3*e,2),(5*e,6)))
 assert d3==(-7*e*e/32,15*e**3/128-3*e/32)
 c31=cmul((0,e*e/128),(15*e,-8))
 assert c31==(e*e/16,15*e**3/128)
 c32=cmul((0,-5*e*e/64),(3*e,2))
 assert c32==(5*e*e/32,-15*e**3/64)
print('PASS third throat kernel coefficients by exact polynomial identity checks.')
