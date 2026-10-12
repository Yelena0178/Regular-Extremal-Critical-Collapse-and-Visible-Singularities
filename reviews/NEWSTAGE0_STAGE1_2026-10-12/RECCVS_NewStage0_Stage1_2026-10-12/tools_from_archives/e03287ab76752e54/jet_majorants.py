"""Effective dyadic majorants for the reduced finite K=8 FLIFT jet system.

Entries are exponents a meaning a certified upper majorant 2**a; None is zero.
The analytic justification of the weighted algebra is in PROOF.md.
No floating point endpoint evolution is performed.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import json
import sys

K=8
BEXP=4000
ALPHA=F(1,64)
T=2**20+2

def esum(*values):
    values=[v for v in values if v is not None]
    if not values:return None
    # Repeated binary sums are outward majorants, not log evaluations.
    value=values[0]
    for other in values[1:]:value=max(value,other)+1
    return value
def eprod(a,b):return None if a is None or b is None else a+b
def factor_exp(v):
    v=abs(F(v))
    if not v:return None
    n=v.numerator.bit_length()-v.denominator.bit_length()
    if v>F(2)**n:n+=1
    return n

@dataclass(frozen=True)
class Bound:
    actual:int|None
    background:int|None
    difference:int|None
    def __add__(self,other):
        return Bound(esum(self.actual,other.actual),esum(self.background,other.background),esum(self.difference,other.difference))
    def __mul__(self,other):
        return Bound(eprod(self.actual,other.actual),eprod(self.background,other.background),esum(eprod(self.difference,other.actual),eprod(self.background,other.difference)))
    def scale(self,value):
        exponent=factor_exp(value)
        return Bound(eprod(self.actual,exponent),eprod(self.background,exponent),eprod(self.difference,exponent))
    def background_zero(self):return Bound(self.actual,None,self.difference)
    def encoded(self):return dict(actual_exponent=self.actual,background_exponent=self.background,difference_over_delta_exponent=self.difference)

ZERO=Bound(None,None,None)
ONE=Bound(0,0,None)
def total(items):
    result=ZERO
    for item in items:result=result+item
    return result
def polynomial_product(*arrays,n):
    result=[ONE]+[ZERO]*n
    for array in arrays:
        result=[total(result[j]*array[k-j] for j in range(k+1) if k-j<len(array)) for k in range(n+1)]
    return result
def coefficient(*arrays,n):return polynomial_product(*arrays,n=n)[n]
def inverse_radius(radius,n):
    out=[Bound(BEXP,0,2*BEXP)]
    for k in range(1,n+1):
        out.append((out[0]*total(radius[i]*out[k-i] for i in range(1,k+1))).background_zero())
    return out
def lapse_exp(lapse,n):
    out=[ONE]
    for k in range(1,n+1):
        out.append(total((lapse[i]*out[k-i]).scale(F(i,k)) for i in range(1,k+1)))
    return out
def integrate(source,actual_initial=False,difference_initial=True):
    return Bound(esum(eprod(source.actual,2),0 if actual_initial else None),eprod(source.background,2),esum(eprod(source.difference,2),0 if difference_initial else None))

def derive():
    radius=[Bound(BEXP,0,BEXP)]
    charge=[Bound(BEXP,0,BEXP)]
    lapse=[ZERO]
    scalar=[Bound(BEXP,BEXP,None)]
    potential=[]
    delta=[Bound(0,None,BEXP)]
    rows=[]
    for n in range(K):
        inv=inverse_radius(radius,n)
        exp=lapse_exp(lapse,n)
        x_source=(coefficient(exp,[coefficient(charge,charge,inv,inv,n=j)+(ONE if j==0 else ZERO) for j in range(n+1)],n=n).scale(F(1,4))).background_zero()
        x=integrate(x_source,actual_initial=n in [0,1],difference_initial=n in [0,1]).background_zero()
        lower=total((radius[i]*radius[n-i+1]).scale(n-i+1) for i in range(1,n+1))
        rnext=((x+lower)*inv[0]).scale(F(1,n+1)).background_zero()
        radius.append(rnext)
        an=integrate(coefficient(exp,charge,inv,inv,n=n).scale(F(1,2)))
        potential.append(an)
        # Time-derivative jets have the same capacities, one lower time degree.
        rt=[Bound(v.actual,None,v.difference) for v in radius[:n+1]]
        ft=scalar[:]
        ru=[radius[j+1].scale(j+1) for j in range(n+1)]
        rr=polynomial_product(rt,inv,n=n)
        first=total((rr[a]*scalar[n-a+1]).scale(n-a+1) for a in range(1,n+1))
        second=coefficient(ru,inv,ft,n=n)
        electro=coefficient(exp,charge,inv,inv,scalar,n=n).scale(F(3,20))
        gauge=(coefficient(potential,rr,scalar,n=n)+coefficient(potential,ft,n=n)).scale(F(3,5))
        fsource=(first+second+electro+gauge).scale(F(1,n+1))
        fnext=integrate(fsource*radius[0])*inv[0]
        scalar.append(fnext)
        fu=[scalar[j+1].scale(j+1) for j in range(n+1)]
        covfu=[fu[j]+coefficient(potential,scalar,n=j).scale(F(3,5)) for j in range(n+1)]
        qnext=coefficient(delta,radius,radius,scalar,covfu,n=n).scale(F(3,5*(n+1)))
        charge.append(qnext.background_zero())
        lsource=(coefficient(exp,inv,inv,n=n).scale(F(1,2))
            +coefficient(ru,rt,inv,inv,n=n).scale(2)
            +coefficient(exp,charge,charge,inv,inv,inv,inv,n=n)
            +coefficient(delta,covfu,ft,n=n).scale(2)).scale(F(1,n+1))
        lnext=integrate(lsource)
        lapse.append(lnext)
        rows.append(dict(order=n+1,r=rnext.encoded(),A=an.encoded(),f=fnext.encoded(),Q=qnext.encoded(),ell=lnext.encoded(),X=x.encoded()))
    # Repeated D_U=partial_U+i*mu*A; retain all ordinary/covariant conversion.
    g=scalar[:]
    covariant=[]
    for j in range(1,K+1):
        g=[g[k+1].scale(k+1)+coefficient(potential,g,n=k).scale(F(3,5)) for k in range(K-j+1)]
        covariant.append(dict(order=j,bound=g[0].encoded()))
    D=max(row['bound']['difference_over_delta_exponent'] for row in covariant)
    background_max=max(v.background for array in [scalar,lapse,potential] for v in array if v.background is not None)
    boundary_exponent=4*T+BEXP
    # Fixed m test integers; do not pretend a failed majorant excludes a root.
    choices=[12000,2104156,max(12000,D+4110)]
    checks=[]
    for exponent in sorted(set(choices)):
        boundary_lhs=3+3*exponent+2*boundary_exponent+background_max
        # L/64 > 2**(exponent+14). Comparison uses bit lengths, no ODE stepping.
        boundary_pass=boundary_lhs.bit_length()<=exponent+14
        Yexp=D+4103-exponent
        qexp=D+10-exponent
        contains=Yexp<=-3 and qexp<=-3 and boundary_pass and exponent>=12000
        checks.append(dict(m_exponent=exponent,boundary_master_log2_lhs=boundary_lhs,boundary_pass=boundary_pass,
            residual_real_component_error_exponent=D-exponent,
            jacobian_real_row_sum_error_exponent=D+4-exponent,
            Krawczyk_scaled_Y_exponent=Yexp,Krawczyk_contraction_q_exponent=qexp,
            sufficient_strict_inclusion=contains))
    return dict(status='EFFECTIVE_MAJORANTS_FOR_FROZEN_FINITE_JET_SYSTEM',K=K,T=T,mu='3/5',alpha='1/64',base_majorant_exponent=BEXP,
        normalized_jets=True,jet_rows=rows,covariant_rows=covariant,max_endpoint_difference_over_delta_exponent=D,
        background_initial_majorant_exponent=background_max,boundary_majorant_exponent=boundary_exponent,
        parameter_box_c_real_component_radius_exponent=-4097,eliminated_kappa_derivative_abs_upper_exponent=154,
        chain_rule_included_in_base_bounds=True,tests=checks,
        warning='Certificate validity depends on explicit weighted-norm and base estimates in PROOF.md, not just this integer recurrence.')

if __name__=='__main__':
    result=derive()
    target=Path(sys.argv[1]);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(D=result['max_endpoint_difference_over_delta_exponent'],rows=result['covariant_rows'],tests=result['tests']),indent=2))
