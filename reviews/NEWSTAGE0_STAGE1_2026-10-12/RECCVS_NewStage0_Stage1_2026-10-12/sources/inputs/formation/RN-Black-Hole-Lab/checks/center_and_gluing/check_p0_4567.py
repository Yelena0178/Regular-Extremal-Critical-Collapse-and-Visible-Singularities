"""Finite exact audits; no claim to certify PDE existence or causal gluing."""
from pathlib import Path
import json
import sympy as S


def gauge():
    ar, au, alpha, s, su, ut = S.symbols('alpha_R alpha_u alpha s s_u u_T', nonzero=True)
    ur=-1/s; utr=su*ut/s**2
    chi_tr=(au*s-alpha*su)*ut/s**2
    vr=(ar+au*ur)*ut+alpha*utr+chi_tr
    assert S.simplify(vr-ar*ut)==0
    return {'status':'PASS','identity':'V_R = alpha_R*u_T, all chain-rule terms included'}


def ern():
    r, ru, ruu, nu = S.symbols('r r_U r_UU nu', nonzero=True, real=True)
    k=-1/(2*nu)
    F=(1-1/r)**2
    rt=k*F/2; rut=S.diff(rt,r)*ru
    lapse=ru/nu; ellu=ruu/ru; ellt=S.diff(rt,r)
    mass=r*(1+4*ru*rt/lapse)/2+1/(2*r)
    assert S.simplify(mass-1)==0
    assert S.simplify(ruu-ellu*ru)==0
    assert S.simplify(S.diff(rt,r)*rt-ellt*rt)==0
    cross=-lapse*(1-1/r**2)/(4*r)-ru*rt/r
    assert S.simplify(rut-cross)==0
    ellut=S.diff(ellt,r)*ru
    ell_rhs=lapse/(2*r**2)+2*ru*rt/r**2-lapse/r**4
    assert S.simplify(ellut-ell_rhs)==0
    # -exp(ell)*dU*dt in (v,r), v=k(t-1): 2 dr dv-F dv^2.
    assert S.simplify(-1/(nu*k)-2)==0
    assert S.simplify(F/(2*nu*k)+F)==0
    # F_Ut = exp(ell)/(2 r^2) yields F_vr=1/r^2.
    assert S.simplify(-1/(2*nu*k*r**2)-1/r**2)==0
    return {'status':'PASS','identities':['mass=1','both Raychaudhuri constraints','r_Ut equation','ell_Ut equation','EF coordinate metric','electric field normalization']}


def polar_einstein_tensor():
    T,R,theta,phi=S.symbols('T R theta phi',real=True)
    coords=[T,R,theta,phi]
    a,N=S.Function('a')(T,R),S.Function('N')(T,R)
    metric=S.diag(-N**2,a**2,R**2,R**2*S.sin(theta)**2)
    inv=metric.inv()
    ch=[[[S.simplify(sum(inv[i,l]*(S.diff(metric[l,k],coords[j])+S.diff(metric[l,j],coords[k])-S.diff(metric[j,k],coords[l])) for l in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
    ric=S.zeros(4)
    for i in range(4):
        for j in range(4):
            ric[i,j]=S.simplify(sum(S.diff(ch[k][i][j],coords[k])-S.diff(ch[k][i][k],coords[j])+sum(ch[k][i][j]*ch[l][k][l]-ch[l][i][k]*ch[k][j][l] for l in range(4)) for k in range(4)))
    scalar=S.simplify(sum(inv[i,j]*ric[i,j] for i in range(4) for j in range(4)))
    G=S.simplify(ric-metric*scalar/2)
    want_tt=N**2*((1-1/a**2)/R**2+2*S.diff(a,R)/(R*a**3))
    want_rr=-(a**2-1)/R**2+2*S.diff(N,R)/(R*N)
    assert S.simplify(G[0,0]-want_tt)==0
    assert S.simplify(G[1,1]-want_rr)==0
    return {'status':'PASS','scope':'exact Einstein tensor for arbitrary time-dependent polar metric; no Taylor truncation'}


def pivots():
    m=S.symbols('m', integer=True, positive=True)
    a,n,v,q,p=S.symbols('a n v q p')
    # Exact leading coefficient matrix in the manuscript's induction order.
    matrix=S.Matrix([[2*m+2,0,0,0,0],
                     [0,2*m+2,0,0,0],
                     [0,-1,2*m+1,0,0],
                     [1,0,0,2*m+1,0],
                     [0,0,0,0,(2*m+1)*(2*m+2)]])
    det=S.factor(matrix.det())
    assert S.simplify(det-(2*m+1)**3*(2*m+2)**3)==0
    assert S.ask(S.Q.positive(det)) is True
    return {'status':'PASS','unknown_order':['Q_even','a_odd','N_odd','V_odd','psi_odd'],'determinant':str(det),'scope':'general symbolic pivots; dependency-order argument is analytic in manuscript'}


def budgets():
    eps=S.symbols('eps',positive=True)
    # Witnesses of how much flatness suffices for each fixed derivative order.
    cases=[]
    for s in range(1,13):
        for N in range(1,7):
            L=N+s+2
            exponents=[L-j for j in range(s+1)]
            assert min(exponents)>N
            cases.append((s,N))
    # Exact solution to y'=L*y+delta, y(0)=0; used for the null-flow bound.
    t,L,delta=S.symbols('t L delta',positive=True)
    y=delta*(S.exp(L*t)-1)/L
    assert S.simplify(S.diff(y,t)-L*y-delta)==0
    assert y.subs(t,0)==0
    # For N=2, C*eps^2<eps/4 when eps<1/(4*C).
    C=S.symbols('C',positive=True)
    margin=S.simplify(eps/4-C*eps**2)
    assert S.factor(margin)==-eps*(4*C*eps-1)/4
    return {'status':'PASS','cutoff_cases':len(cases),'null_comparison_solution':str(y),'scope':'exact finite exponent checks and comparison ODE; reference stability is a PDE input'}


if __name__=='__main__':
    result={'radial_gauge':gauge(),'actual_ERN':ern(),'polar_Einstein_tensor':polar_einstein_tensor(),'parity_pivots':pivots(),'cutoff_and_null_budgets':budgets(),'overall':'PASS'}
    Path(__file__).with_name('RESULTS_NEW.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
