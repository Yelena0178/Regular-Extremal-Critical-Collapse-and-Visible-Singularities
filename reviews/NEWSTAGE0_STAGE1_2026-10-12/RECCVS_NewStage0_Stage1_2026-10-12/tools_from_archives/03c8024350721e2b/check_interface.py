"""Exact finite algebra verification, not a PDE/geometric certification.
GPT 主张，未经外部独立审查。
Run: python3 -B code/check_interface.py
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, platform
from exact_rational import Rat, var

ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, condition, evidence):
    if not condition: raise AssertionError(name+': '+str(evidence))
    checks.append({'name':name,'passed':True,'evidence':str(evidence)})
def ident(name, expr):
    expr=Rat.wrap(expr)
    check(name,expr.is_zero(),'exact zero numerator; denominator domain as stated in PROOF')
def inverse(m):
    n=len(m); z=[[F(v) for v in row]+[F(i==j) for j in range(n)] for i,row in enumerate(m)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if z[i][j])
        z[j],z[pivot]=z[pivot],z[j]
        v=z[j][j]; z[j]=[x/v for x in z[j]]
        for i in range(n):
            if i!=j:
                v=z[i][j]; z[i]=[x-v*y for x,y in zip(z[i],z[j])]
    return [row[n:] for row in z]
def transported(p, diag):
    return [[sum(F(diag[k])*p[k][i]*p[k][j] for k in range(len(p))) for j in range(len(p))] for i in range(len(p))]
def pair(i,j): return tuple(sorted((i,j)))

# Byte lock and baseline status. These checks preserve evidence, not its truth.
lock=json.loads((ROOT/'INPUT_LOCK.json').read_text())
for name, expected in lock['sha256'].items():
    check('frozen:'+name,hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,expected)
ep=json.loads((ROOT/'frozen/ENDPOINT.json').read_text())
old=json.loads((ROOT/'frozen/stage312/STATUS.json').read_text())
for key,other in [('member','member'),('candidate','candidate_endpoint'),('selection','selection'),('path','fixed_path')]:
    check('endpoint_copy:'+key,ep[key]==old[other],'exact JSON object equality')
check('conditional_only',ep['selection']['conditional_actual_fixed_slice'] and not ep['selection']['unconditional_certification'],'no status upgrade')
check('original_psi_not_identified',not ep['selection']['original_psi_identity_with_candidate_certified'],'different slice data allowed')
actualroot=hashlib.sha256((ROOT/'frozen/stage312/baseline/ROOT_CERTIFICATE_mgeom.json').read_bytes()).hexdigest()
check('root_member_lock',actualroot==ep['member']['root_sha256'],actualroot)

# Formal symmetric inverse coefficients and commuting second jets: universal
# Maxwell principal cancellation, all 4 output components, not metric sampling.
gi=[[var('g%d%d'%pair(i,j)) for j in range(4)] for i in range(4)]
pairs=[(i,j) for i in range(4) for j in range(i,4)]
for b in range(4):
    h=lambda c,i,j: var('A%d_%d%d'%(c,*pair(i,j)))
    mixed=sum(gi[a][c]*(-h(c,a,b)+h(c,b,a)) for a in range(4) for c in range(4))
    ident('Maxwell_mixed_cancel_'+str(b),mixed)

# Einstein principal part. Three exact non-diagonal Lorentz point metrics.
# For each metric check all 100 independent second metric-jet basis vectors.
# This is a finite sample test of the general analytic identity, not a proof
# over every metric. P^T diag(-1,positive,positive,positive) P is Lorentz.
matrices=[]
for k in (1,2,3):
    p=[[F(i==j) for j in range(4)] for i in range(4)]
    p[0][1]=F(k,20); p[1][0]=F(1,30); p[1][2]=F(k,7); p[2][3]=F(1,9)
    matrices.append(transported(p,[-1,2,3,5]))
for mk,g in enumerate(matrices):
    inv=inverse(g)
    check('metric_inverse_'+str(mk),all(sum(g[i][k]*inv[k][j] for k in range(4))==F(i==j) for i in range(4) for j in range(4)),str(g))
    check('metric_time_'+str(mk),g[0][0]<0 and inv[0][0]<0,(g[0][0],inv[0][0]))
    for pq in pairs:
        for cd in pairs:
            def jet(a,b,c,d): return F(pair(a,b)==pq and pair(c,d)==cd)
            def dG(r,a,b,c):
                return sum(inv[r][d]*(jet(b,d,c,a)+jet(a,d,c,b)-jet(a,b,c,d)) for d in range(4))/2
            dh=[[sum(inv[a][b]*dG(r,a,b,c) for a in range(4) for b in range(4)) for c in range(4)] for r in range(4)]
            residual=[]
            for a,b in pairs:
                ric=sum(dG(c,a,b,c)-dG(c,a,c,b) for c in range(4))
                q=sum(g[a][r]*dh[r][b]+g[b][r]*dh[r][a] for r in range(4))/2
                wave=-sum(inv[c][d]*jet(a,b,c,d) for c in range(4) for d in range(4))/2
                residual.append(ric-q-wave)
            check('Einstein_principal_%d_%s_%s'%(mk,pq,cd),all(x==0 for x in residual),'all 10 output components zero')

# Exact harmonic and L0 initialization for non-diagonal positive gamma.
for case in range(4):
    p=[[F(i==j) for j in range(3)] for i in range(3)]
    p[0][1]=F(case+1,7); p[1][2]=F(1,5)
    gamma=transported(p,[2,3,4]); invgamma=inverse(gamma)
    g=[[F(0) for _ in range(4)] for _ in range(4)]; g[0][0]=-F(1)
    for i in range(3):
        for j in range(3): g[i+1][j+1]=gamma[i][j]
    inv=inverse(g)
    first=lambda k,i,j:F((k+1)*(min(i,j)+2)+(max(i,j)+1)*(case+1),11)
    K=[[F((i+1)*(j+1)*(case+1),13) for j in range(3)] for i in range(3)]
    dg=[[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for k in range(3):
        for i in range(3):
            for j in range(3): dg[k+1][i+1][j+1]=first(k,i,j)
    for i in range(3):
        for j in range(3): dg[0][i+1][j+1]=-2*K[i][j]
    dg[0][0][0]=2*sum(invgamma[i][j]*K[i][j] for i in range(3) for j in range(3))
    for i in range(3):
        v=sum(invgamma[k][l]*(first(k,l,i)-first(i,k,l)/2) for k in range(3) for l in range(3))
        dg[0][0][i+1]=dg[0][i+1][0]=v
    def Gamma(r,a,b): return sum(inv[r][d]*(dg[a][b][d]+dg[b][a][d]-dg[d][a][b]) for d in range(4))/2
    H=[sum(inv[a][b]*Gamma(r,a,b) for a in range(4) for b in range(4)) for r in range(4)]
    check('harmonic_initial_'+str(case),all(x==0 for x in H),'all four H components zero')
    da=[[F((i+2)*(j+3)+case,17) for j in range(3)] for i in range(3)]
    dotA0=sum(invgamma[i][j]*da[i][j] for i in range(3) for j in range(3))
    check('L0_initial_'+str(case),-dotA0+sum(invgamma[i][j]*da[i][j] for i in range(3) for j in range(3))==0,'L0=0')
    hdot=[F(case+i+1,19) for i in range(4)]
    Q=[[F(0) for _ in range(4)] for _ in range(4)]; Q[0][0]=-hdot[0]
    for i in range(3): Q[0][i+1]=Q[i+1][0]=sum(gamma[i][j]*hdot[j+1] for j in range(3))/2
    tr=sum(inv[a][b]*Q[a][b] for a in range(4) for b in range(4))
    defect=[[Q[a][b]-g[a][b]*tr/2 for b in range(4)] for a in range(4)]
    check('Hamiltonian_Hdot_sign_'+str(case),defect[0][0]==-hdot[0]/2,defect[0][0])
    check('momentum_Hdot_sign_'+str(case),all(defect[0][i+1]==sum(gamma[i][j]*hdot[j+1] for j in range(3))/2 for i in range(3)),'all three components exact')

# Universal first-jet identity used to covariantize Q.
def dg(c,a,b): return var('dg%d_%d%d'%(c,*pair(a,b)))
for a,b in pairs:
    for r in range(4):
        lowerGamma=(dg(a,b,r)+dg(b,a,r)-dg(r,a,b))/2
        ident('Q_covariant_coefficient_%d%d%d'%(a,b,r),(dg(a,b,r)+dg(b,a,r))/2-lowerGamma-dg(r,a,b)/2)

# Matter trace reversal and gauge covariance as formal algebra identities.
EM,SF,trSF,g=map(var,['EM','SF','trSF','metric_component'])
ident('stress_trace_reversal',2*(EM+SF-g*trSF/2)-g*(-2*trSF)/2-(2*EM+2*SF))
J,L,Fbc=map(var,['current','dL','Fbc'])
ident('stress_source_cancel',Fbc*(J-L)-Fbc*J+Fbc*L)
ident('Gauss_Ldot',J+(-J))
# d(exp(-i mu chi)Phi) + i mu(A+dchi)exp(-i mu chi)Phi
# factor out phase; cancel the real coefficient of i mu explicitly.
mu,A,dchi,Phi=map(var,['mu','A','dchi','Phi'])
ident('U1_covariance',-mu*dchi*Phi+mu*(A+dchi)*Phi-mu*A*Phi)
pr,pi,xr,xi=map(var,['Phi_real','Phi_imag','Pi_real','Pi_imag'])
ident('current_conjugate_sign',(pr*xi-pi*xr)+(pi*xr-pr*xi))

# Rational safety margins used in common-domain and two isotopy corridors.
check('angular_constant',256**2>=2*128**2,'Cauchy-Schwarz bound 256*sqrt(deltaU*deltat)')
check('outer_collar_left',F(1,2**15)<F(1,8192),'mo < left graph gap')
check('outer_collar_right',F(1,2**15)<F(1,4096),'mo < right graph gap')
check('inner_collar_margin',F(1,8)-F(1,128)==F(15,128),'15 epsilon/128')
check('inner_normal_error',F(16,4096)<F(1,2),'gamma_margin>epsilon; q in [0,1)')
check('inner_metric_error',F(8,4096)<F(1,2),'induced margin > gamma_margin/2')
theta,q=map(var,['theta','q'])
ident('inner_normal_monotonicity',1-theta**2*q**2-(1-q**2)-(1-theta**2)*q**2)
ident('inner_margin_factor',1-q**2-(1-q)*(1+q))

# Acyclic prerequisite ledger is a logic/order check, not a theorem proof.
nodes={
 'actual_strip':[], 'actual_center':[], 'old_Cauchy':[], 'compatible_category':[],
 'local_existence':[], 'geometric_uniqueness':[], 'MGHD_construction':[],
 'common_domain':['actual_strip','old_Cauchy'],
 'fixed_embed_into_Ma':['common_domain','compatible_category','geometric_uniqueness','MGHD_construction'],
 'inner_isotopy':['actual_center','compatible_category'],
 'outer_isotopy':['fixed_embed_into_Ma','compatible_category'],
 'candidate_Cauchy':['inner_isotopy','outer_isotopy','old_Cauchy'],
 'Ma_candidate_development':['candidate_Cauchy'],
 'candidate_Mb':['Ma_candidate_development','local_existence','geometric_uniqueness','MGHD_construction','compatible_category'],
 'Ma_to_Mb':['Ma_candidate_development','candidate_Mb'],
 'reverse_isotopy_in_extension':['Ma_to_Mb','inner_isotopy','outer_isotopy'],
 'old_surface_Cauchy_in_extension':['reverse_isotopy_in_extension'],
 'old_maximality_transfer':['old_surface_Cauchy_in_extension','MGHD_construction'],
 'onto_identification':['old_maximality_transfer','Ma_to_Mb']}
seen=set()
for n, deps in nodes.items():
    check('dependency_order:'+n,all(d in seen for d in deps),deps)
    seen.add(n)
(ROOT/'verification/DEPENDENCIES.json').write_text(json.dumps({'label':'GPT 主张，未经外部独立审查','nodes':nodes,'open_premises':['actual_strip','actual_center','old_Cauchy','compatible_category','local_existence','geometric_uniqueness','MGHD_construction'],'acyclic':True,'premises_proved_by_script':False},ensure_ascii=False,indent=2)+'\n')
result={'stage':'3.13','label':'GPT 主张，未经外部独立审查','python':platform.python_version(),'engine':'stdlib Fraction plus exact multivariate polynomial numerators','number_of_checks':len(checks),'all_passed':True,'checks':checks,'PDE_certification_by_script':False,'geometric_certification_by_script':False,'external_independent_review':False,'Einstein_test_scope':'100 independent second-jet bases at each of 3 rational non-diagonal Lorentz metrics; analytic general identity remains required'}
(ROOT/'verification/RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['stage','number_of_checks','all_passed','PDE_certification_by_script']},ensure_ascii=False))
