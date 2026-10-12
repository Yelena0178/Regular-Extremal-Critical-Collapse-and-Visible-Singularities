#!/usr/bin/env python3
"""Exact finite audit. This program does not solve or formally verify a PDE."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
checks = {}

def check(name, condition):
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)

root_file = ROOT/'baseline/baseline/certificates/ROOT_CERTIFICATE_mgeom.json'
root_hash = hashlib.sha256(root_file.read_bytes()).hexdigest()
status = json.loads((ROOT/'STATUS.json').read_text())
check('same_certified_root_sha256', root_hash == status['root_sha256'])
check('parameter_identity', (status['M'],status['T'],status['mu']) == (2104156,1048578,'3/5'))
j = json.loads((ROOT/'baseline/baseline/certificates/EFFECTIVE_JET_BOUNDS.json').read_text())
exponents = [v['actual_exponent'] for row in j['jet_rows'] for v in row.values()
             if isinstance(v,dict) and 'actual_exponent' in v]
check('ordinary_jet_budget_including_factorial',max(exponents)+16+10<500000)
check('restored_jet_finite_product_budget',64+10*500000+128<10000000)
# L is kept as an exponent expression. Never allocate its real exponential.
check('L_dominates_log_budgets',status['M']>100 and 2**100>10000000+status['M']+2*status['T']+10000)
check('ln2_upper_bound_by_positive_Taylor',sum(F(7,10)**k/F([1,1,2,6][k]) for k in range(4))>2)
check('beta_log_upper_budget',3201*F(7,10)<3000)
check('beta_log_lower_budget',2**100>status['M']+2*status['T']+4)
check('Sigma_integral_budget',F(1,2**14)+F(1,256)+F(1,8192)<F(1,64))
check('Sigma_bump_coefficient',F(1,8)-F(1,64)==F(7,64))
check('thin_strip_left_margin',F(-1,8)-F(1,16)>-1)
check('charge_absorption_coefficient',4-2*3799 == -7594 and -7594 < -3)
# Exact linear coefficients in (T_flat,R_flat,r0):
# U/(2 beta)=T-R; sigma/(2 beta)=2r0-T-R.
U_coeff=(F(1),F(-1),F(0)); sigma_coeff=(F(-1),F(-1),F(2))
check('G_center_is_smooth_time_function',tuple(a-b for a,b in zip(U_coeff,sigma_coeff))==(F(2),F(0),F(-2)))

# Small exact Laurent algebra for the first-order subsystem.
names=['r','pr','pi','ell','Q','lam','zr','zi','kap','nu','hr','hi','A','chi','s']
N=len(names); ix={n:i for i,n in enumerate(names)}
zero=(0,)*N
def const(c): return {zero:F(c)} if c else {}
def var(n):
    k=list(zero);k[ix[n]]=1;return {tuple(k):F(1)}
def add(*ps):
    out={}
    for p in ps:
        for k,c in p.items():out[k]=out.get(k,F(0))+c
    return {k:c for k,c in out.items() if c}
def scale(p,c):return {k:v*F(c) for k,v in p.items() if v*c}
def mul(*ps):
    out=const(1)
    for p in ps:
        new={}
        for a,c in out.items():
            for b,d in p.items():
                k=tuple(x+y for x,y in zip(a,b));new[k]=new.get(k,F(0))+c*d
        out=new
    return {k:c for k,c in out.items() if c}
def rp(n):
    k=list(zero);k[ix['r']]=n;return {tuple(k):F(1)}
def diff(p,n):
    i=ix[n];out={}
    for k,c in p.items():
        if k[i]:
            b=list(k);b[i]-=1;b=tuple(b);out[b]=out.get(b,F(0))+c*k[i]
        if n=='ell' and k[ix['s']]:
            out[k]=out.get(k,F(0))+c*k[ix['s']]
    return {k:c for k,c in out.items() if c}
r,pr,pi,Q,lam,zr,zi,nu,hr,hi,A,s=[var(n) for n in ['r','pr','pi','Q','lam','zr','zi','nu','hr','hi','A','s']]
mu=F(3,5)
Fr=add(scale(mul(nu,lam,rp(-1)),-1),scale(mul(s,rp(-1)),F(-1,4)),scale(mul(s,Q,Q,rp(-3)),F(1,4)))
Fhr=add(scale(mul(nu,zr,rp(-1)),-1),scale(mul(s,Q,pi,rp(-1)),mu/4))
Fhi=add(scale(mul(nu,zi,rp(-1)),-1),scale(mul(s,Q,pr,rp(-1)),-mu/4))
FA=scale(mul(s,Q,rp(-2)),F(-1,2))
Fchi=add(scale(mul(add(mul(hr,zr),mul(hi,zi)),rp(-2)),-2),scale(mul(s,rp(-2)),F(1,2)),scale(mul(nu,lam,rp(-2)),2),scale(mul(s,Q,Q,rp(-4)),-1))
z_names=['nu','hr','hi','A','chi'];y_names=names[:9]
# Use positive polynomial majorants and B >= 1; every term is at most linear in B.
values={n:F(1) for n in names};values.update(r=F(1,128),Q=F(2),s=F(2),lam=F(2),zr=F(2),zi=F(2))
def bound(p):
    total=F(0)
    for k,c in p.items():
        # lam,zr,zi each have bound 2B. Affine coefficient/forcing polynomials
        # have total degree <=1 in these three variables.
        check('at_most_linear_B_'+str(len(checks)),sum(k[ix[n]] for n in ['lam','zr','zi'])<=1)
        value=abs(c)
        for n,power in zip(names,k):value*=values[n]**power
        total+=value
    return total
row_bounds=[]
for eq in [Fr,Fhr,Fhi,FA,Fchi]:
    coeffs=[diff(eq,n) for n in z_names]
    forcing={k:c for k,c in eq.items() if all(k[ix[n]]==0 for n in z_names)}
    check('affine_Z_'+str(len(row_bounds)),all(sum(k[ix[n]] for n in z_names)<=1 for k in eq))
    base=sum(bound(p) for p in coeffs+[forcing])
    deriv=sum(bound(diff(p,n)) for p in coeffs+[forcing] for n in y_names)
    check('ODE_coefficient_row_'+str(len(row_bounds)),base<2**60 and deriv<2**60)
    row_bounds.append({'coefficient_and_source_over_B':str(base),'Y_derivative_row_over_B':str(deriv)})
# Scalar compatibility exactly: phi_t=zeta/r, phi_U=eta/r-i mu A phi,
# A_t=-sQ/(2r^2). Real/imag components tested separately.
phiU=[add(mul(hr,rp(-1)),scale(mul(A,pi),mu)),add(mul(hi,rp(-1)),scale(mul(A,pr),-mu))]
phiT=[mul(zr,rp(-1)),mul(zi,rp(-1))]
zetaU=[add(scale(mul(lam,hr,rp(-1)),-1),scale(mul(s,Q,pi,rp(-1)),-mu/4),scale(mul(A,zi),mu)),
        add(scale(mul(lam,hi,rp(-1)),-1),scale(mul(s,Q,pr,rp(-1)),mu/4),scale(mul(A,zr),-mu))]
t_derivs={'r':lam,'pr':phiT[0],'pi':phiT[1],'hr':Fhr,'hi':Fhi,'A':FA}
for k in range(2):
    d_t=add(*(mul(diff(phiU[k],n),p) for n,p in t_derivs.items()))
    d_u=add(mul(zetaU[k],rp(-1)),scale(mul([zr,zi][k],nu,rp(-2)),-1))
    check('scalar_compatibility_component_'+str(k),not add(d_t,scale(d_u,-1)))
check('status_does_not_claim_full_closure',not status['claims']['original_outgoing_vertex_in_future'] and not status['claims']['full_An_Lim_target_domain'] and not status['claims']['strict_trapped_sphere_certified'])
manifest_file=ROOT/'MANIFEST.json'
if manifest_file.exists():
    for name,sha in json.loads(manifest_file.read_text())['sha256'].items():
        check('manifest:'+name,hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha)
out={'result':'PASS','scope':status['verification_scope'],'checks':checks,
     'ODE_rows':row_bounds,'max_normalized_actual_jet_exponent':max(exponents),
     'explicit_width':'a_S=exp(-8*2^100*exp(200*(L+S+2)))',
     'unclosed':status['open'],'separate_stage4':status['separate_stage4']}
(ROOT/'verification').mkdir(exist_ok=True)
(ROOT/'verification/CHECK_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result':out['result'],'checks':len(checks),'max_jet_exponent':max(exponents),'scope':out['scope']},ensure_ascii=False))
