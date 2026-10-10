"""Exact normalized endpoint identities; not a substitute for cone existence."""
from symbolic_checks import *
def ev(p,values):
 return sum((v*__import__('functools').reduce(lambda a,b:a*b,(values[n]**j for n,j in k),F(1)) for k,v in p.d.items()),F(0))
vals={n:F(0) for n in rules};vals.update(r=F(1),al=F(-1,2),Q=F(1),O=F(1))
for name in ['p2','P2','v','V','w','W','r2','Q2','ell2','av']:vals[name]=F(0)
assert ev(LV,vals)==F(-1,2)
assert ev(du(LV),vals)==F(-3,2)
aV=-O*Q/(2*r**2)
assert ev(aV,vals)==F(-1,2)
assert ev(du(aV),vals)==F(-1,2)
assert ev(du(du(aV)),vals)==F(-3,4)
# Raychaudhuri at zero scalar and pure lapse-normalized endpoint.
rUUV=ev(LV,vals)*F(-1,2);rUUUV=ev(du(LV),vals)*F(-1,2)
assert rUUV==F(1,4) and rUUUV==F(3,4)
aUVV=-ev(LV,vals)/2
assert aUVV==F(1,4)
# Minkowski all mixed entries in this table vanish for every R>0.
for R in map(F,(1,2,3)):
 vv=vals.copy();vv.update(r=R,Q=F(0),be=F(1,2))
 assert ev(LV,vv)==0 and ev(du(LV),vv)==0
 assert ev(aV,vv)==0 and ev(du(aV),vv)==0
print('PASS nonzero RN mixed jets, and Minkowski zero mixed jets.')
