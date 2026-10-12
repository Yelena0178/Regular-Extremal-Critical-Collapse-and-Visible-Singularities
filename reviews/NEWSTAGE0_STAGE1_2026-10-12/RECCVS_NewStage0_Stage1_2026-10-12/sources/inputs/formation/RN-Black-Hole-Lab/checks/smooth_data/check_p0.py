"""Exact finite checks for P0_123_proof.md; not a PDE or convergence proof."""
from pathlib import Path
import json
import sympy as S


def maxwell():
    R, e, s, sr, alpha, ar = S.symbols('R e s sr alpha ar', real=True, nonzero=True)
    x, y, xr, yr, xrr, yrr, xu, yu = S.symbols('x y xr yr xrr yrr xu yu', real=True)
    f, fr, frr, fu = x+S.I*y, xr+S.I*yr, xrr+S.I*yrr, xu+S.I*yu
    fur = -fu/R+s*fr/R+sr*fr/2+s*frr/2-S.I*e*alpha*f/R-S.I*e*alpha*fr-S.I*e*ar*f/2
    im = lambda z: S.expand(S.im(S.expand(z)))
    qr = e*R**2*im(f*S.conjugate(fr))
    qrr = e*(2*R*im(f*S.conjugate(fr))+R**2*im(f*S.conjugate(frr)))
    qur = e*R**2*im(fu*S.conjugate(fr)+f*S.conjugate(fur))
    current_r = 2*R*im(f*S.conjugate(fu))+R**2*im(fr*S.conjugate(fu)+f*S.conjugate(fur))
    potential_r = (2*R*alpha+R**2*ar)*(x*x+y*y)+2*R**2*alpha*(x*xr+y*yr)
    residual = S.expand(qur-sr*qr-s*qrr+e*current_r-e**2*potential_r)
    assert residual == 0, residual
    return {'status':'PASS', 'identity':'d_R Maxwell residual = 0, arbitrary local complex field'}


def einstein_residual():
    u, R, theta, phi = S.symbols('u R theta phi', real=True)
    coords = [u,R,theta,phi]
    g, s, X, Y = [S.Function(z)(u,R) for z in ['g','s','X','Y']]
    metric = S.Matrix([[-g*s,-g,0,0],[-g,0,0,0],[0,0,R**2,0],[0,0,0,R**2*S.sin(theta)**2]])
    inv = metric.inv()
    christ = [[[S.simplify(sum(inv[a,d]*(S.diff(metric[d,c],coords[b])+S.diff(metric[d,b],coords[c])-S.diff(metric[b,c],coords[d])) for d in range(4))/2) for c in range(4)] for b in range(4)] for a in range(4)]
    E = S.zeros(4); E[0,0]=X; E[0,1]=E[1,0]=Y
    trace = sum(inv[a,b]*E[a,b] for a in range(4) for b in range(4))
    mixed = S.simplify(inv*(E-metric*trace/2))
    def divergence(b):
        result = sum(S.diff(mixed[a,b],coords[a]) for a in range(4))
        result += sum(christ[a][a][c]*mixed[c,b]-christ[c][a][b]*mixed[a,c] for a in range(4) for c in range(4))
        return S.simplify(result)
    radial = divergence(1)
    assert S.simplify(radial+2*Y/(g*R)) == 0, radial
    temporal = S.simplify(divergence(0).subs(Y,0).doit())
    assert S.simplify(temporal+S.diff(R**2*X,R)/(g*R**2)) == 0, temporal
    return {'status':'PASS','radial':str(radial),'temporal_after_Y_zero':str(temporal)}


def jacobians():
    beta, p, q, mu = S.symbols('beta p q mu', nonzero=True, real=True)
    G = S.Matrix([[q,beta*(p-q)],[0,-beta/q]])
    assert S.simplify(G.det()+beta)==0
    kr, ki = S.symbols('kr ki', real=True)
    complex_mult = S.Matrix([[kr,-ki],[ki,kr]])
    assert S.expand(complex_mult.det()-kr**2-ki**2)==0
    fixed_row, E_e, de = S.symbols('fixed_row E_e de')
    dQ = -de/mu
    assert S.expand(fixed_row-mu*E_e*dQ-(fixed_row+E_e*de))==0
    return {'status':'PASS','geometric_determinant':str(G.det()),'complex_response_determinant':str(complex_mult.det()),'charge_row_operation':'PASS'}


def division_ibp():
    R, theta = S.symbols('R theta', real=True)
    tested=[]
    for k in range(1,9):
        # Exact polynomial witnesses for the integration-by-parts formula.
        v=sum(S.Rational((-1)**i,i+1)*R**i for i in range(1,k+4))
        w=sum(S.Rational(i+2,i+3)*R**i for i in range(1,k+3))
        vk,wk=S.diff(v,R,k),S.diff(w,R,k)
        def at(expr): return expr.subs(R,theta*R)
        interior=sum(S.binomial(k+1,i)*at(S.diff(v,R,i))*at(S.diff(w,R,k+1-i)) for i in range(1,k+1))
        extreme_boundary=(vk*w+v*wk)/R
        correction=k*theta**(k-1)*(at(vk)*at(w)+at(v)*at(wk))/R+theta**k*(at(vk)*at(S.diff(w,R))+at(S.diff(v,R))*at(wk))
        rhs=extreme_boundary+S.integrate(S.expand(theta**k*interior-correction),(theta,0,1))
        assert S.expand(S.diff(S.cancel(v*w/R),R,k)-rhs)==0, k
        tested.append(k)
    return {'status':'PASS','orders':tested,'scope':'finite exact polynomial checks of IBP; analytic tame bound is proved in manuscript'}


if __name__ == '__main__':
    results={'maxwell':maxwell(),'einstein_residual':einstein_residual(),'jacobians':jacobians(),'division_ibp':division_ibp()}
    results['overall']='PASS'
    path=Path(__file__).with_name('RESULTS.json')
    path.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))
