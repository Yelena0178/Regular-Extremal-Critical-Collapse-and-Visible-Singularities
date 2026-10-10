"""Fixed-point directed interval proof of K>=kappa on a whole rectangle.
Every acceptance is integer arithmetic. Point sin/cos/exp use Taylor
with explicit uniform remainder and range reduction; no math transcendental.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial
from pathlib import Path
import json,time
B=1<<200
class I:
 __slots__=('l','h')
 def __init__(self,a=0,b=None,raw=False):
  if raw:self.l,self.h=a,b;return
  a=F(a);b=a if b is None else F(b)
  self.l=(a.numerator*B)//a.denominator;self.h=-((-b.numerator*B)//b.denominator)
 def __add__(self,o):
  if not isinstance(o,I):o=I(o)
  return I(self.l+o.l,self.h+o.h,raw=True)
 __radd__=__add__
 def __neg__(self):return I(-self.h,-self.l,raw=True)
 def __sub__(self,o):return self+-o if isinstance(o,I) else self+(-I(o))
 def __rsub__(self,o):return -self+o
 def __mul__(self,o):
  if not isinstance(o,I):o=I(o)
  v=[self.l*o.l,self.l*o.h,self.h*o.l,self.h*o.h]
  return I(min(v)//B,-((-max(v))//B),raw=True)
 __rmul__=__mul__
 def __truediv__(self,o):
  if not isinstance(o,I):o=I(o)
  assert not o.l<=0<=o.h
  pairs=[(a*B,b) for a in (self.l,self.h) for b in (o.l,o.h)]
  return I(min(a//b for a,b in pairs),max(-((-a)//b) for a,b in pairs),raw=True)
 def __pow__(self,n):
  q=I(1)
  for _ in range(n):q=q*self
  return q
 def absmax(self):return max(abs(self.l),abs(self.h))
 def abs(self):return I(0 if self.l<=0<=self.h else min(abs(self.l),abs(self.h)),self.absmax(),raw=True)

@lru_cache(maxsize=500000)
def scpoint(n,d):
 a=F(n,d);m=0
 while abs(a)>F(1,2):a/=2;m+=1
 z=I(a);z2=z*z;ss=z;cc=I(1);ts=z;tc=I(1)
 for k in range(1,25):
  ts=-ts*z2/((2*k)*(2*k+1));tc=-tc*z2/((2*k-1)*(2*k));ss+=ts;cc+=tc
 # Taylor through degree 49 (cos degree48); degree49 remainders <= .5^50/50!.
 err=F(1,2**50*factorial(50));ss+=I(-err,err);cc+=I(-err,err)
 for _ in range(m):ss,cc=2*ss*cc,cc*cc-ss*ss
 return ss,cc

def scbox(a):
 mid=F(a.l+a.h,2*B);rad=F(a.h-a.l,2*B)
 s,c=scpoint(mid.numerator,mid.denominator)
 s=s+I(-rad,rad);c=c+I(-rad,rad)
 return I(max(-B,s.l),min(B,s.h),raw=True),I(max(-B,c.l),min(B,c.h),raw=True)
@lru_cache(maxsize=100000)
def exppoint(n,d):
 a=F(n,d);assert a>=0;m=0
 while a>F(1,2):a/=2;m+=1
 z=I(-a);p=I(1);term=I(1)
 for k in range(1,50):term=term*z/k;p+=term
 err=F(1,2**50*factorial(50));p+=I(-err,err)
 for _ in range(m):p=p*p
 return p

def expbox(a):
 assert a.l>=0
 l=exppoint(a.h,B).l;h=exppoint(a.l,B).h
 return I(l,h,raw=True)
