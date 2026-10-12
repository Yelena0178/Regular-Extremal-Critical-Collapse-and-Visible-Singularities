"""Independent positive-rational majorant arithmetic, without importing generator.

The analytic weighted-norm proof remains necessary; this checker verifies the
coefficient arithmetic and uses independent Taylor/geometric series formulae.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import factorial
import json
import sys

Z=(Q(0),Q(0),Q(0));U=(Q(1),Q(1),Q(0))
def plus(x,y):return tuple(a+b for a,b in zip(x,y))
def times(x,y):return (x[0]*y[0],x[1]*y[1],x[2]*y[0]+x[1]*y[2])
def scaled(x,s):return tuple(a*abs(Q(s)) for a in x)
def sigma(xs):
    result=Z
    for x in xs:result=plus(result,x)
    return result
def conv(x,y,N):return [sigma(times(x[i],y[k-i]) for i in range(k+1) if i<len(x) and k-i<len(y)) for k in range(N+1)]
def chain(arrays,N):
    result=[U]+[Z]*N
    for array in arrays:result=conv(result,array,N)
    return result
def get(arrays,N):return chain(arrays,N)[N]
def fixed_zero_background(x):return (x[0],Q(0),x[2])
def primitive(x,actual_boundary=False,error_boundary=True):return (4*x[0]+int(actual_boundary),4*x[1],4*x[2]+int(error_boundary))
def exponential(ell,N):
    # exp(ell)=sum_{p=0}^N ell_positive**p/p!, since ell_0=0.
    power=[U]+[Z]*N
    result=[U]+[Z]*N
    for p in range(1,N+1):
        power=conv(power,ell,N)
        result=[plus(a,scaled(b,Q(1,factorial(p)))) for a,b in zip(result,power)]
    return result
def reciprocal(r,N,B):
    base=(B,Q(1),B*B)
    positive=[Z]+[times(r[j],base) for j in range(1,N+1)]
    power=[U]+[Z]*N
    result=[U]+[Z]*N
    for p in range(1,N+1):
        power=conv(power,positive,N)
        result=[plus(a,b) for a,b in zip(result,power)]
    return [times(base,result[j]) if j==0 else fixed_zero_background(times(base,result[j])) for j in range(N+1)]

def run(certificate):
    assert certificate['K']==8 and certificate['T']==2**20+2
    assert certificate['mu']=='3/5' and certificate['alpha']=='1/64'
    assert certificate['base_majorant_exponent']==4000
    N=certificate['K'];B=Q(2)**certificate['base_majorant_exponent']
    r=[(B,Q(1),B)];q=[(B,Q(1),B)];ell=[Z];a=[];f=[(B,B,Q(0))];delta=[(Q(1),Q(0),B)]
    calculated=[]
    for n in range(N):
        inv=reciprocal(r,n,B);ex=exponential(ell,n)
        h=chain([q,q,inv,inv],n);h[0]=plus(h[0],U)
        x=primitive(fixed_zero_background(scaled(get([ex,h],n),Q(1,4))),n<2,n<2)
        low=sigma(scaled(times(r[j],r[n-j+1]),n-j+1) for j in range(1,n+1))
        rn=fixed_zero_background(scaled(times(plus(x,low),inv[0]),Q(1,n+1)));r.append(rn)
        an=primitive(scaled(get([ex,q,inv,inv],n),Q(1,2)));a.append(an)
        rt=[fixed_zero_background(v) for v in r[:n+1]];ft=f[:]
        ru=[scaled(r[j+1],j+1) for j in range(n+1)]
        rho=chain([rt,inv],n)
        src=sigma([sigma(scaled(times(rho[j],f[n-j+1]),n-j+1) for j in range(1,n+1)),get([ru,inv,ft],n),scaled(get([ex,q,inv,inv,f],n),Q(3,20)),scaled(plus(get([a,rho,f],n),get([a,ft],n)),Q(3,5))])
        fn=times(primitive(times(scaled(src,Q(1,n+1)),r[0])),inv[0]);f.append(fn)
        fu=[scaled(f[j+1],j+1) for j in range(n+1)]
        cov=[plus(fu[j],scaled(get([a,f],j),Q(3,5))) for j in range(n+1)]
        qn=fixed_zero_background(scaled(get([delta,r,r,f,cov],n),Q(3,5*(n+1))));q.append(qn)
        ls=sigma([scaled(get([ex,inv,inv],n),Q(1,2)),scaled(get([ru,rt,inv,inv],n),2),get([ex,q,q,inv,inv,inv,inv],n),scaled(get([delta,cov,ft],n),2)])
        ln=primitive(scaled(ls,Q(1,n+1)));ell.append(ln)
        calculated.append(dict(r=rn,A=an,f=fn,Q=qn,ell=ln,X=x))
    errors=[]
    labels=['actual_exponent','background_exponent','difference_over_delta_exponent']
    for j,row in enumerate(calculated):
        for field,triple in row.items():
            bounds=certificate['jet_rows'][j][field]
            for i,key in enumerate(labels):
                exponent=bounds[key]
                if (triple[i]!=0 if exponent is None else triple[i]>Q(2)**exponent):errors.append([j+1,field,key])
    g=f[:];endpoints=[]
    for j in range(1,N+1):
        g=[plus(scaled(g[k+1],k+1),scaled(get([a,g],k),Q(3,5))) for k in range(N-j+1)]
        endpoints.append(g[0])
        for i,key in enumerate(labels):
            exponent=certificate['covariant_rows'][j-1]['bound'][key]
            if (g[0][i]!=0 if exponent is None else g[0][i]>Q(2)**exponent):errors.append([j,'covariant',key])
    if errors:raise AssertionError('Independent upper arithmetic exceeds saved bounds: '+repr(errors))
    for test in certificate['tests']:
        exponent=test['m_exponent'];D=certificate['max_endpoint_difference_over_delta_exponent']
        assert test['Krawczyk_scaled_Y_exponent']==D+4103-exponent
        assert test['Krawczyk_contraction_q_exponent']==D+10-exponent
        if test['sufficient_strict_inclusion']:
            assert test['boundary_pass']
            assert Q(2)**test['Krawczyk_scaled_Y_exponent']+Q(2)**test['Krawczyk_contraction_q_exponent']<Q(1,4)
    return dict(status='INDEPENDENT_POSITIVE_RATIONAL_MAJORANTS_PASS',
        generator_not_imported=True,independent_exp_Taylor_and_inverse_geometric_series=True,
        all_saved_jet_and_covariant_bounds_dominate=True,
        mathematical_proof_dependency='PROOF.md weighted algebra, base estimates, boundary suppression',
        full_spacetime_or_H_positivity_certified=False)

if __name__=='__main__':
    if sys.get_int_max_str_digits():sys.set_int_max_str_digits(0)
    data=json.loads(Path(sys.argv[1]).read_text());result=run(data)
    Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
