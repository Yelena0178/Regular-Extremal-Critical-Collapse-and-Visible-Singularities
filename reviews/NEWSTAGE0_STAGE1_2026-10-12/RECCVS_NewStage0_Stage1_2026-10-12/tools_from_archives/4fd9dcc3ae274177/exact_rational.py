"""Small exact multivariate polynomial/rational engine using Fraction only.

No symbolic assumptions or floating-point evaluations are used. Identity
checks are zero numerator checks after exact denominator cross-multiplication.
GPT 主张，未经外部独立审查。
"""
from fractions import Fraction as F


class Poly:
    def __init__(self, terms=None):
        self.terms = {m:F(c) for m,c in (terms or {}).items() if c}

    @classmethod
    def constant(cls, c):
        return cls({():F(c)})

    @classmethod
    def variable(cls, name):
        return cls({((name,1),):F(1)})

    def __add__(self, other):
        out=dict(self.terms)
        for m,c in other.terms.items():
            out[m]=out.get(m,F(0))+c
        return Poly(out)

    def __neg__(self):
        return Poly({m:-c for m,c in self.terms.items()})

    def __sub__(self, other):
        return self+-other

    def __mul__(self, other):
        out={}
        for m,c in self.terms.items():
            for mm,cc in other.terms.items():
                pp=dict(m)
                for name,power in mm:
                    pp[name]=pp.get(name,0)+power
                key=tuple(sorted(pp.items()))
                out[key]=out.get(key,F(0))+c*cc
        return Poly(out)

    def derivative(self, name):
        out={}
        for m,c in self.terms.items():
            pp=dict(m); power=pp.get(name,0)
            if power:
                if power==1: del pp[name]
                else: pp[name]=power-1
                out[tuple(sorted(pp.items()))]=c*power
        return Poly(out)

    def substitute(self, name, replacement):
        total=Rat(0)
        for m,c in self.terms.items():
            term=Rat(c)
            for symbol,power in m:
                term *= (replacement if symbol==name else var(symbol))**power
            total += term
        return total


class Rat:
    def __init__(self, numerator=0, denominator=None):
        self.n=numerator if isinstance(numerator,Poly) else Poly.constant(numerator)
        self.d=denominator if denominator is not None else Poly.constant(1)
        if not self.d.terms:
            raise ZeroDivisionError('zero polynomial denominator')

    @staticmethod
    def wrap(value):
        return value if isinstance(value,Rat) else Rat(value)

    def __add__(self, other):
        other=self.wrap(other)
        return Rat(self.n*other.d+other.n*self.d,self.d*other.d)

    __radd__=__add__

    def __neg__(self):
        return Rat(-self.n,self.d)

    def __sub__(self, other):
        return self+-self.wrap(other)

    def __rsub__(self, other):
        return self.wrap(other)+-self

    def __mul__(self, other):
        other=self.wrap(other)
        return Rat(self.n*other.n,self.d*other.d)

    __rmul__=__mul__

    def __truediv__(self, other):
        other=self.wrap(other)
        return Rat(self.n*other.d,self.d*other.n)

    def __rtruediv__(self, other):
        return self.wrap(other)/self

    def __pow__(self, power):
        if not isinstance(power,int):
            raise TypeError('integer powers only')
        if power<0:
            return Rat(self.d,self.n)**(-power)
        result=Rat(1)
        for _ in range(power):
            result *= self
        return result

    def derivative(self, name):
        return Rat(self.n.derivative(name)*self.d-self.n*self.d.derivative(name),self.d*self.d)

    def substitute(self, name, value):
        value=self.wrap(value)
        return self.n.substitute(name,value)/self.d.substitute(name,value)

    def is_zero(self):
        return not self.n.terms


def var(name):
    return Rat(Poly.variable(name))


def symbols(names):
    return tuple(var(name) for name in names.split())
