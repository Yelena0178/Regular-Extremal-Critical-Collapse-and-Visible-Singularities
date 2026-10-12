#!/usr/bin/env python3
"""Finite exact audits; no numerical spacetime evolution or formal PDE proof."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib,json

BASE=Path(__file__).resolve().parents[1]
checks={}
def require(name,value):
    checks[name]=bool(value)
    if not value:raise AssertionError(name)

status=json.loads((BASE/'STATUS.json').read_text())
require('same_root',hashlib.sha256((BASE/status['root_path']).read_bytes()).hexdigest()==status['root_sha256'])
require('parameter_identity',(status['mu'],status['M'])==('3/5',2104156))
require('normalized_phi_v_bound',4201315+1600-1052078<3150840)
require('edge_norm_B_dominates_rvv_and_other_low_orders',2*3150840+100<7000000)
require('charge_coefficient_without_Omega_upper_assumption',F(9,16)/F(1,2)**2==F(9,4)<4)
require('chi_exponent',2-2*3799==-7596)
require('radius_bootstrap_strict_improvement',F(1,64)/(F(1,2)-F(1,64))==F(1,31)<F(1,2))
require('positive_radius_target',F(1,4)*(F(1,2)-F(1,64))==F(31,256)>F(1,16))
require('force_over_A_squared_coefficient',F(9,4)<4)
require('Theta_squared_budget',(1+F(1,32))**2<1+4*F(1,32))
require('half_radius_exponent_margin',(F(7,8))**8<F(31,64))
eta=F(15,16)*4*F(31,64)*F(7,8)
require('eta_half_contradiction',eta==F(3255,2048)>1)
require('cell_absorption',F(5,4)/2**12+F(1,2**24)+F(5,2)/2**12<F(1,4))
require('partition_count_instantiation_exponent',16+5*4==36)
require('partition_marginal_budget',F(2)+F(6)+F(4,1)/F(1,16)<=8*F(2)/F(1,16))

# log lower comparison: x(x-b)*dlog[g]/dx has coefficients
# (-1+chi)*x + (2+3chi)*b. Independently differentiate the
# x^[-(2+3chi)]*(x-b)^[1+4chi] comparison expression.
for chi in [F(0),F(1,32),F(1,10**6)]:
    from_differential=(F(-1)+chi,F(2)+3*chi)
    from_integrating_factor=(-(2+3*chi)+(1+4*chi),2+3*chi)
    require('integrating_factor_coefficients_'+str(chi),from_differential==from_integrating_factor)

# Small polynomial algebra, in covariant real components.
vars=['p','q','a','b','c','d','lam','nu','ri','s','Q']
ix={s:i for i,s in enumerate(vars)};dim=len(vars);zero=(0,)*dim
def val(c):return {zero:F(c)} if c else {}
def v(s):
    k=list(zero);k[ix[s]]=1;return {tuple(k):F(1)}
def plus(*ps):
    out={}
    for p in ps:
        for k,c in p.items():out[k]=out.get(k,F(0))+c
    return {k:c for k,c in out.items() if c}
def times(*ps):
    out=val(1)
    for p in ps:
        nxt={}
        for a,c in out.items():
            for b,d in p.items():
                k=tuple(x+y for x,y in zip(a,b));nxt[k]=nxt.get(k,F(0))+c*d
        out=nxt
    return out
def scale(p,c):return {k:v*F(c) for k,v in p.items() if v*c}
p,q,a,b,c,d,lam,nu,ri,s,Q=[v(n) for n in vars]
mu=F(3,5)
# a+ib=Du Phi; c+id=Phi_v; ri=1/r; s=Omega^2.
av=plus(scale(times(lam,ri,a),-1),scale(times(nu,ri,c),-1),scale(times(s,Q,q,ri,ri),mu/4))
bv=plus(scale(times(lam,ri,b),-1),scale(times(nu,ri,d),-1),scale(times(s,Q,p,ri,ri),-mu/4))
fu=scale(plus(times(p,a),times(q,b)),2)
fv=scale(plus(times(p,c),times(q,d)),2)
fuv=scale(plus(times(c,a),times(d,b),times(p,av),times(q,bv)),2)
mixed=scale(plus(times(a,c),times(b,d)),2)
require('signed_mixed_scalar_null_identity',not plus(fuv,times(lam,ri,fu),times(nu,ri,fv),scale(mixed,-1)))

# theta^(j)=exp(-1/u)*sum coeff[k] u^-k. Differentiate directly.
pol={0:1};theta_bounds=[]
for j in range(6):
    bound=sum(abs(a)*max(1,k**k) for k,a in pol.items())
    theta_bounds.append(bound)
    require('theta_derivative_'+str(j),bound<2**48)
    nxt={}
    for k,a in pol.items():
        nxt[k+2]=nxt.get(k+2,0)+a
        if k:nxt[k+1]=nxt.get(k+1,0)-k*a
    pol={k:a for k,a in nxt.items() if a}
# Reciprocal derivatives from D R=1, with D>=1/9.
inv=[9];rho_bounds=[]
for n in range(1,6):
    inv.append(9*sum(comb(n,k)*2*theta_bounds[k]*inv[n-k] for k in range(1,n+1)))
for n in range(6):
    bnd=sum(comb(n,k)*theta_bounds[k]*inv[n-k] for k in range(n+1))
    rho_bounds.append(bnd)
    require('cutoff_step_derivative_'+str(n),bnd<2**512)
require('radial_cartesian_cutoff_constant',512+15+16<=544)
require('C7_to_H4_epsilon_cubic',7-4==3)
require('H4_component_and_volume_budget',544+19+4+8<600)
require('conditional_Cauchy_cone_speed_budget',F(1,2**12)<F(1,2))
require('local_Picard_constants_slack',60-100<-4 and 12-20<=-1 and 2-20<0)
require('status_keeps_effective_common_surface_open',not status['common_cauchy']['effective_before_p_Sigma_frozen'])
require('status_does_not_claim_A_to_D_or_coordinate_box',not status['A_to_D_proved'] and not status['first_period']['concrete_trapped_sphere_coordinate_box_certified'])
manifest=BASE/'MANIFEST.json'
if manifest.exists():
    for name,sha in json.loads(manifest.read_text())['sha256'].items():
        require('manifest:'+name,hashlib.sha256((BASE/name).read_bytes()).hexdigest()==sha)
answer={'result':'PASS','scope':'Exact finite arithmetic and polynomial identities supporting written analytic proofs; not formal PDE or causal verification',
        'checks':checks,'eta_half_lower_bound':str(eta),'theta_derivative_majorants':theta_bounds,
        'cutoff_step_derivative_majorants':rho_bounds,'uninstantiated_Cauchy_constants':['N7','C_red','C_stab']}
(BASE/'verification').mkdir(exist_ok=True)
(BASE/'verification/CHECK_RESULTS.json').write_text(json.dumps(answer,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result':'PASS','checks':len(checks),'eta_half_lower_bound':str(eta),'scope':answer['scope']},ensure_ascii=False))
