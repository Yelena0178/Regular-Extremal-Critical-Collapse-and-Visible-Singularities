"""Exact integer Bernstein root isolation for the filtered leading profile.

The only approximate values printed are display values. Certificates use
integers and dyadic intervals. This certifies J's root structure, not a PDE.
"""
import argparse
import json
from fractions import Fraction as F
from math import comb, gcd, lcm
from pathlib import Path


def signs_variations(a):
    signs=[1 if x>0 else -1 for x in a if x]
    return sum(x!=y for x,y in zip(signs,signs[1:]))


def primitive(a):
    g=0
    for x in a: g=gcd(g,abs(x))
    return [x//g for x in a] if g>1 else a


def split(a):
    d=len(a)-1; row=a[:]
    left=[row[0]*(1<<d)]; right=[row[-1]*(1<<d)]
    for j in range(1,d+1):
        row=[row[k]+row[k+1] for k in range(len(row)-1)]
        left.append(row[0]*(1<<(d-j)))
        right.append(row[-1]*(1<<(d-j)))
    return primitive(left),primitive(right[::-1])


def certify(data,max_depth=50,max_nodes=20000):
    N=[F(x) for x in data['J_numerator']]
    order=0
    while N and N[0]==0:
        N.pop(0);order+=1
    while N and N[-1]==0: N.pop()
    if not N: raise ValueError('zero J polynomial: root structure NOT CERTIFIED')
    B=2*data['n']; d=len(N)-1
    # F(u)=(1-u)^d N(B*u/(1-u)).
    coefficients=[N[j]*B**j/F(comb(d,j)) for j in range(d+1)]
    denom=1
    for c in coefficients: denom=lcm(denom,c.denominator)
    a=primitive([int(c*denom) for c in coefficients])
    todo=[(0,0,a)]; leaves=[];nodes=0
    while todo:
        index,depth,b=todo.pop();nodes+=1
        if nodes>max_nodes: raise RuntimeError('node limit reached: NOT CERTIFIED')
        v=signs_variations(b)
        if v<=1 and b[0] and b[-1]:
            leaves.append(dict(index=index,depth=depth,variations=v,
                               left_sign=1 if b[0]>0 else -1,
                               right_sign=1 if b[-1]>0 else -1))
            continue
        if depth>=max_depth: raise RuntimeError('depth limit reached: NOT CERTIFIED')
        l,r=split(b)
        todo.append((2*index+1,depth+1,r));todo.append((2*index,depth+1,l))
    leaves.sort(key=lambda x:F(x['index'],2**x['depth']))
    roots=sum(x['variations'] for x in leaves)
    return dict(removed_origin_order=order,compact_degree=d,x_scale=B,
                node_count=nodes,leaf_count=len(leaves),positive_root_count=roots,
                first_sign=leaves[0]['left_sign'],last_sign=leaves[-1]['right_sign'],
                leaves=leaves,
                single_negative_to_positive=(roots==1 and leaves[0]['left_sign']==-1
                                             and leaves[-1]['right_sign']==1),
                method='exact integer Bernstein subdivision + Descartes rule',
                scope='LEADING_PROFILE_J_ROOTS_ONLY')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('profile');p.add_argument('output')
    args=p.parse_args();data=json.loads(Path(args.profile).read_text())
    cert=certify(data);Path(args.output).write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({k:v for k,v in cert.items() if k!='leaves'}))
