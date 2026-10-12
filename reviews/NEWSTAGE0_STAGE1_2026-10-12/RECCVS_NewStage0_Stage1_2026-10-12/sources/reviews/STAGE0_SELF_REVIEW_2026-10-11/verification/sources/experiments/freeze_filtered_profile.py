"""Exact rational leading-profile discovery. This is NOT a finite-amplitude seed.

Uses the imported fixed-K filtered exponential construction. Prints exact
leading integral checks and Descartes information. No numerical PDE is run.
"""
from fractions import Fraction as F
from math import factorial, comb
from pathlib import Path
import argparse
import json


def add(p, q):
    out = [F(0)] * max(len(p), len(q))
    for i, v in enumerate(p): out[i] += v
    for i, v in enumerate(q): out[i] += v
    while len(out) > 1 and not out[-1]: out.pop()
    return out


def scale(p, a): return [a*x for x in p]


def mul(p, q):
    out = [F(0)] * (len(p)+len(q)-1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                if b: out[i+j] += a*b
    return out


def deriv(p): return [F(i)*p[i] for i in range(1,len(p))] or [F(0)]


def cadd(p,q): return (add(p[0],q[0]),add(p[1],q[1]))


def cscale(p,a,b=F(0)):
    return (add(scale(p[0],a),scale(p[1],-b)),
            add(scale(p[0],b),scale(p[1],a)))


def cderiv(p): return (deriv(p[0]),deriv(p[1]))


def integral_exp(p, a):
    return sum((v*F(factorial(j),1)/a**(j+1) for j,v in enumerate(p)),F(0))


def variations(p):
    signs = [1 if a>0 else -1 for a in p if a]
    return sum(a != b for a,b in zip(signs,signs[1:]))


def make(n, sigma, K):
    if not (n%2 == 0 and n >= 4*K+4 and sigma>0 and K>=1):
        raise ValueError('invalid fixed-K filtered profile parameters')
    re=[F(0)]*(3*n//2+1); im=re.copy()
    for j in range(n+1):
        k=n-j
        v=F(comb(n,j)*(-2*n)**k)
        if k%4==0: re[n//2+j]=v
        elif k%4==1: im[n//2+j]=v
        elif k%4==2: re[n//2+j]=-v
        else: im[n//2+j]=-v
    p=(re,im)
    for k in range(1,K+1):
        p=cadd(cderiv(p),cscale(p,-sigma-k,F(1,4)))
    y=cadd(cderiv(p),cscale(p,-sigma,F(1,4)))
    D=add(mul(p[0],p[0]),mul(p[1],p[1]))
    E=add(mul(y[0],y[0]),mul(y[1],y[1]))
    C=add(mul(p[0],y[1]),scale(mul(p[1],y[0]),-1))
    A=add(mul(p[0],y[0]),mul(p[1],y[1]))
    et=integral_exp(E,2*sigma); ct=integral_exp(C,2*sigma)
    el=integral_exp(E,1+2*sigma); cl=integral_exp(C,1+2*sigma)
    lam=2*et/ct
    k0=2*lam*cl-el
    # Numerator of J = lambda*((1+2l)k+k')-l*l-k*k.
    N=add(scale(add(mul(add(D,scale(A,2)),C),
                    add(mul(deriv(C),D),scale(mul(C,deriv(D)),-1))),lam),
          scale(mul(E,D),-1))
    moments=[]
    for s in range(1,K+1):
        # exp(-s*x) z = exp(-(s+sigma-i/4)*x) p.
        ar=F(s)+sigma; ai=F(-1,4)
        den=ar*ar+ai*ai
        inv=(ar/den,-ai/den)
        powr,powi=F(1),F(0)
        zr,zi=F(0),F(0)
        for j in range(max(len(p[0]),len(p[1]))):
            powr,powi=powr*inv[0]-powi*inv[1],powr*inv[1]+powi*inv[0]
            a=p[0][j] if j<len(p[0]) else F(0)
            b=p[1][j] if j<len(p[1]) else F(0)
            fac=factorial(j)
            zr+=fac*(a*powr-b*powi); zi+=fac*(a*powi+b*powr)
        moments.append([str(zr),str(zi)])
    return dict(K=K,n=n,sigma=str(sigma),gamma_real=str(-sigma),gamma_imag='1/4',
                polynomial_real=[str(a) for a in p[0]],polynomial_imag=[str(a) for a in p[1]],
                E_total=str(et),C_total=str(ct),lambda_exact=str(lam),lambda_float=float(lam),
                K0_exact=str(k0),K0_positive=k0>0,
                K0_normalized_exact=str(k0/et),
                moments_exact=moments,
                J_numerator_degree=len(N)-1,J_numerator_sign_variations=variations(N),
                J_numerator=[str(v) for v in N],
                status='LEADING_PROFILE_ONLY_NOT_FINITE_AMPLITUDE_NOT_CAUCHY_DATA')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--K',type=int,default=8)
    parser.add_argument('--n',type=int,default=44)
    parser.add_argument('--sigma',default='1/20')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    data=make(args.n,F(args.sigma),args.K)
    if not all(v==['0','0'] for v in data['moments_exact']):
        raise ValueError('exact moment check failed')
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:data[k] for k in ['K','n','sigma','lambda_float','K0_positive',
                                       'J_numerator_degree','J_numerator_sign_variations','status']}))
