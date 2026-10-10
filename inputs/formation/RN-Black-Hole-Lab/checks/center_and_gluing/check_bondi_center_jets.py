"""Exact rational formal-series checks; not a proof of analytic estimates."""
from fractions import Fraction as F
from math import factorial

class C:
    def __init__(self, r=0, i=0):
        if isinstance(r, C): self.r, self.i = r.r, r.i
        else: self.r, self.i = F(r), F(i)
    def __add__(self, v):
        v=C(v); return C(self.r+v.r,self.i+v.i)
    __radd__=__add__
    def __neg__(self): return C(-self.r,-self.i)
    def __sub__(self,v): return self+-C(v)
    def __mul__(self,v):
        v=C(v); return C(self.r*v.r-self.i*v.i,self.r*v.i+self.i*v.r)
    __rmul__=__mul__
    def __truediv__(self,v): return C(self.r/F(v),self.i/F(v))
    def __bool__(self): return bool(self.r or self.i)
    def conj(self): return C(self.r,-self.i)
    def __eq__(self,v):
        v=C(v); return self.r==v.r and self.i==v.i
    def __repr__(self): return f'({self.r})+i({self.i})'

class S:
    nt=0; nr=0
    def __init__(self,d=0):
        if not isinstance(d,dict): d={(0,0):C(d)}
        self.d={k:C(v) for k,v in d.items() if v and k[0]<=S.nt and 0<=k[1]<=S.nr}
    def __add__(self,x):
        x=x if isinstance(x,S) else S(x); d=self.d.copy()
        for k,v in x.d.items(): d[k]=d.get(k,C())+v
        return S(d)
    __radd__=__add__
    def __neg__(self): return S({k:-v for k,v in self.d.items()})
    def __sub__(self,x): return self+-as_s(x)
    def __mul__(self,x):
        x=as_s(x); d={}
        for (j,k),v in self.d.items():
            for (l,m),w in x.d.items():
                key=(j+l,k+m)
                if key[0]<=S.nt and key[1]<=S.nr: d[key]=d.get(key,C())+v*w
        return S(d)
    __rmul__=__mul__
    def scale(self,x): return S({k:v*x for k,v in self.d.items()})
    def shift(self,k):
        assert all(r+k>=0 for j,r in self.d), 'nonregular division at center'
        return S({(j,r+k):v for (j,r),v in self.d.items()})
    def dr(self): return S({(j,r-1):v*r for (j,r),v in self.d.items() if r})
    def du(self): return S({(j-1,r):v*j for (j,r),v in self.d.items() if j})
    def integral(self): return S({(j,r+1):v/(r+1) for (j,r),v in self.d.items()})
    def avg(self): return S({(j,r):v/(r+1) for (j,r),v in self.d.items()})
    def conj(self): return S({k:v.conj() for k,v in self.d.items()})
    def imag(self): return S({k:C(v.i) for k,v in self.d.items()})
    def exp_zero(self):
        assert all(r>=2 for j,r in self.d)
        out=S(1); term=S(1)
        for m in range(1,S.nr//2+1):
            term=(term*self).scale(F(1,m)); out=out+term
        return out

def as_s(x): return x if isinstance(x,S) else S(x)

def fields(h, charge=F(3,2)):
    f=h.avg(); q=h-f
    L=(q*q.conj()).shift(-1).integral()
    g=L.exp_zero()
    Q=(f*h.conj()).imag().shift(1).integral().scale(charge)
    alpha=-(g*Q).shift(-2).integral()
    speed=(g-(g*Q*Q).shift(-2)).avg()
    B=(speed.dr()*q).scale(F(1,2))-(alpha*h).scale(C(0,charge)) \
      +(g*Q*f).shift(-1).scale(C(0,charge/2))
    assert B.d.get((0,0),C())==0
    return f,g,Q,alpha,speed,B

def rhs(h, charge=F(3,2)):
    f,g,Q,alpha,speed,B=fields(h,charge)
    return (speed*h.dr()).scale(F(1,2))+B

def evolve(seed,n):
    h=S({(0,k):v for k,v in seed.items()})
    for j in range(n):
        old=S.nt; S.nt=j
        r=rhs(h)
        S.nt=old
        for (jj,k),v in r.d.items():
            if jj==j: h.d[(j+1,k)]=v/(j+1)
    return h

for n in range(2,7):
    S.nt=n; S.nr=n+4
    base={0:C(1,1),1:C(2,-1),2:C(F(1,3),F(2,5))}
    a=C(1,2)
    changed=base.copy(); changed[n]=changed.get(n,C())+a*((n+1)*F(1,factorial(n)))
    hb=evolve(base,n); hc=evolve(changed,n)
    for j in range(n):
        assert hc.d.get((j,0),C())==hb.d.get((j,0),C())
    delta=(hc.d.get((n,0),C())-hb.d.get((n,0),C()))*factorial(n)
    expect=a*F(n+1,2**n)
    assert delta==expect,(n,delta,expect)
    print(f'PASS n={n}: exact nonlinear center jet difference = {delta}',flush=True)
print('Checks use nonzero complex background and nonzero charge coupling.')

S.nt=3; S.nr=10
hh=evolve({0:C(1,1),1:C(2,-1),2:C(F(1,3),F(2,5))},3)
f,g,Q,alpha,speed,B=fields(hh)
e=F(3,2)
residual=Q.du()-speed*Q.dr()+(f*f.du().conj()).imag().shift(2).scale(e) \
         -(alpha*f*f.conj()).shift(2).scale(e*e)
bad={key:v for key,v in residual.d.items() if key[0]<=1 and key[1]<=5 and v}
assert not bad,bad
print('PASS: Bondi Maxwell supplementary equation through u^1 R^5, exact rationals')
print('These checks do not verify uniform remainder bounds or global existence.')
