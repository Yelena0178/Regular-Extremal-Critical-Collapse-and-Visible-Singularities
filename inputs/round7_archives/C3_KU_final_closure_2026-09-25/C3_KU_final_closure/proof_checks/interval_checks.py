"""Independent outward-rounded Decimal interval + Taylor/Bernstein K proof.
No mesh positivity inference; every interval is covered by a polynomial enclosure.
"""
from exact_core import *
from decimal import Decimal as Dec, Context, ROUND_FLOOR, ROUND_CEILING
from math import factorial
loctx=Context(prec=100,rounding=ROUND_FLOOR);hictx=Context(prec=100,rounding=ROUND_CEILING)
class I:
 def __init__(self,a,b=None):
  if isinstance(a,I):self.l,self.h=a.l,a.h;return
  if isinstance(a,F):self.l=loctx.divide(Dec(a.numerator),Dec(a.denominator));self.h=hictx.divide(Dec(a.numerator),Dec(a.denominator));return
  self.l=Dec(a);self.h=Dec(a if b is None else b)
 def __add__(self,o):
  o=I(o);return I(loctx.add(self.l,o.l),hictx.add(self.h,o.h))
 __radd__=__add__
 def __neg__(self):return I(self.h.copy_negate(),self.l.copy_negate())
 def __sub__(self,o):return self+-I(o)
 def __rsub__(self,o):return I(o)+-self
 def __mul__(self,o):
  o=I(o);pairs=[(x,y) for x in (self.l,self.h) for y in (o.l,o.h)]
  return I(min(loctx.multiply(x,y) for x,y in pairs),max(hictx.multiply(x,y) for x,y in pairs))
 __rmul__=__mul__
 def __truediv__(self,o):
  o=I(o);assert o.l*o.h>0
  return self*I(loctx.divide(Dec(1),o.h),hictx.divide(Dec(1),o.l))
 def __pow__(self,n):
  assert n>=0;r=I(1);p=self
  while n:
   if n%2:r=r*p
   p=p*p;n//=2
  return r
 def inflate(self,b):b=I(b);return self+I(b.h.copy_negate(),b.h)
def trig(x):
 x=I(x);ss=I(0);cc=I(0)
 for k in range(61):
  cc=cc+((-1)**k)*(x**(2*k))/factorial(2*k)
  ss=ss+((-1)**k)*(x**(2*k+1))/factorial(2*k+1)
 return ss.inflate(x**123/factorial(123)),cc.inflate(x**122/factorial(122))
def expminus(x):
 y=I(x);v=I(0)
 for k in range(241):v=v+((-1)**k)*y**k/factorial(k)
 return v.inflate(y**241/factorial(241))
DE=I(E[0]);DD=I(D);SI=list(map(I,S));TI=list(map(I,T));nu=[I(k*w) for k in range(1,2*N+1)]
order=20
# A uniform derivative bound for order21 on x>=0.
B=I(abs(D))
for j in range(2*N):B=B+I(abs(S[j])+abs(T[j]))*nu[j]**(order+1)
leaves=[]
def certify(l,h,depth=0):
 m=(l+h)/2;radius=(h-l)/2;sn,cs=trig(w*m);sns=[I(0),sn];css=[I(1),cs]
 for j in range(2,2*N+1):sns.append(2*cs*sns[-1]-sns[-2]);css.append(2*cs*css[-1]-css[-2])
 ex=expminus(m);pc=[]
 for n in range(order+1):
  d=-DD*((-1)**n)*ex
  if n==0:d=d+2*DE*(m+2)
  if n==1:d=d+2*DE
  for j in range(2*N):
   sinphase=[sns[j+1],css[j+1],-sns[j+1],-css[j+1]][n%4]
   cosphase=[css[j+1],-sns[j+1],-css[j+1],sns[j+1]][n%4]
   d=d+(SI[j]*sinphase+TI[j]*cosphase)*nu[j]**n
  pc.append(d/factorial(n))
 # Taylor polynomial in u=(x-l)/(h-l), y=radius*(2u-1).
 pp=[sum((pc[j]*comb(j,k)*I(radius)**j*(2**k)*((-1)**(j-k)) for j in range(k,order+1)),I(0)) for k in range(order+1)]
 bb=[sum((pp[k]*F(comb(i,k),comb(order,k)) for k in range(i+1)),I(0)) for i in range(order+1)]
 rem=B*I(radius)**(order+1)/factorial(order+1)
 low=loctx.subtract(min(v.l for v in bb),rem.h)
 if low>Dec('1e-8'):
  leaves.append({'l':str(l),'h':str(h),'lower':str(low),'remainder_upper':str(rem.h)});return
 assert depth<15,('unresolved',l,h,str(low))
 certify(l,m,depth+1);certify(m,h,depth+1)
for j in range(40):certify(F(j,2),F(j+1,2))
# x>=20: monotone affine lower envelope, using exp(-x)<=1.
tail=44*E[0]-abs(D)-sum(map(abs,S))-sum(map(abs,T))
assert tail>F(1,10)
(ROOT/'data/K_certificate.json').write_text(json.dumps({'method':'Decimal100 directed interval Taylor20 Bernstein, plus exact rational tail','kappa':'1/100000000','leaves':leaves,'tail_start':20,'tail_lower_exact':str(tail)},indent=2))
print('PASS K>=1e-8 on all x>=0; compact leaves',len(leaves),'min certified',min(Dec(v['lower']) for v in leaves),'tail lower',float(tail))
