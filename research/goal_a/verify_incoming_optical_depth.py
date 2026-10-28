"""Exact identities/negative controls for A-OPT01; no PDE certificate."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def check(expr, label):
    if s.simplify(expr) != 0:
        raise ArithmeticError(label)


def main():
    r, O, nu, lam, q, P2, k, w, f = s.symbols('r O nu lam q P2 k w f', nonzero=True, real=True)
    mixed = -nu*lam/r-O*(1-q*q/r**2)/(4*r)
    check((nu*lam+r*mixed)/nu-(-O/(4*nu))*(1-q*q/r**2), 'radial transport')
    # Raychaudhuri: (nu/O)_u=-r P2/O, log(k)_u=r P2/nu.
    check(-(-r*P2/O)/(nu/O)/nu-r*P2/nu**2, 'log k derivative')
    # k'=wk, (r k f)'=k(1-Q^2/r^2).
    fprime = (1-f)/r-q*q/r**3-w*f
    check(k*f+r*w*k*f+r*k*fprime-k*(1-q*q/r**2), 'integrating factor ODE')
    check((1-f-r*fprime)/2-(q*q/(2*r*r)+r*f*w/2), 'weighted Hawking mass budget')
    z2, cross, imag, alpha, coupling = s.symbols('z2 cross imag alpha coupling',real=True)
    # d_v[-nu |z|^2/r] at fixed u, before the moving-endpoint terms.
    z2_v=-2*cross-2*alpha*z2-2*coupling*k*q*imag/r
    integrand_v=-alpha*nu*z2/r-nu*z2_v/r+nu*lam*z2/r**2
    claimed=nu*((alpha+lam/r)*z2/r+2*cross/r+2*coupling*k*q*imag/r**2)
    check(integrand_v-claimed,'moving optical layer interior')
    check((alpha+lam/r-k*(1-q*q/r**2)/r).subs(
        {alpha:k*(1-f-q*q/r**2)/r,lam:k*f}),'moving layer damping cancellation')
    qr=s.symbols('qr',real=True)
    check((-2*coupling*k*q*imag/r**2).subs(imag,-qr/(coupling*r))-2*k*q*qr/r**3,
          'Maxwell charge work sign')
    A,C=s.symbols('A C',real=True)
    check(A*A/4+4*C*C-2*A*C-(A/2-2*C)**2,'Young absorption')
    M, Q, rr = s.symbols('M Q rr', positive=True)
    rn = 1-2*M/rr+Q*Q/rr**2
    check(s.diff(rr*rn, rr)-(1-Q*Q/rr**2), 'vacuum RN')
    # Exact constant-depth radial model: w=c/r, Q=0.
    c, a, b, fa, x = s.symbols('c a b fa x', positive=True)
    fb = a/b*(a/b)**c*fa+(1-(a/b)**(c+1))/(c+1)
    particular = (1-(a/b)**(c+1))/(c+1)
    check(s.diff(b*fb, b)+c*fb-1, 'nonzero depth exact radial model')
    check(fb.subs(b,a)-fa, 'radial model inner value')
    N=s.symbols('N',positive=True)
    model=1/(N+1)+(a/b)**(N+1)*N/(N+1)
    check(s.diff(b*model,b)+N*model-1,'mass-only countermodel ODE')
    if s.limit(model.subs({a:1,b:2}),N,s.oo)!=0:
        raise ArithmeticError('mass-only countermodel endpoint')
    # Reject reversed optical exponent by a concrete exact substitution.
    wrong = a/b*(b/a)**c*fa+((b/a)**c-a/b)/(1+c)
    if s.simplify((s.diff(b*wrong,b)+c*wrong-1).subs({a:1,b:2,c:1,fa:1})) == 0:
        raise ArithmeticError('reversed optical exponent accepted')
    # Omitting a negative inner term is invalid even for positive source.
    if (a/b*fa+(b-a)/b).subs({a:1,b:2,fa:-2}) >= 0:
        raise ArithmeticError('negative-inner-end control')
    # ERN illustrates that the low-charge premise is essential inside r=M.
    if not (Q*Q/rr**2).subs({Q:1,rr:s.Rational(1,2)}) > 1:
        raise ArithmeticError('ERN charge-ratio control')
    root=Path(__file__).resolve().parent
    names=['verify_incoming_optical_depth.py','INCOMING_OPTICAL_DEPTH_GATE.md','../../definitions/MODEL.md']
    report=dict(claim_ids=['O01.1','O01.2','O01.3','O01.4','O01.5','O01.6'],
                logic='PROVED (checked finite identities only)',evidence=['EXACT_ALGEBRA','EXPERIMENTAL (trace controls)'],audit='INTERNAL_AUDIT',
                sympy_version=s.__version__,
                checks=['mixed-equation radial transport','Raychaudhuri log-k derivative',
                        'integrating-factor ODE','weighted Hawking mass budget','vacuum RN',
                        'nonzero-depth radial model and inner endpoint','bounded-mass unbounded-depth countermodel',
                        'moving layer interior, damping cancellation, charge work sign and Young absorption'],
                negative_controls=['reversed optical exponent','negative inner endpoint','ERN inside exceeds Q/r=1'],
                limitations=['radial model is not an EMCSF construction','no continuous PDE bounds or global theorem'],
                goal_A_proved=False,
                source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    # Exercise the actual read-only observer on exact traces, with nonzero scalar flux.
    import numpy as np
    from screen_incoming_optical_depth import IncomingDiagnostics
    from verify_centered_cauchy_diamond import flrw, curved_flat
    controls={}
    for name,exact in [('FLRW',flrw),('curved_Minkowski',curved_flat)]:
        groups=[]
        for n in (64,128):
            observer=IncomingDiagnostics(rays=(1.5,))
            for t0 in np.linspace(0,1,n+1):
                x0=1.5-t0
                y=exact(t0,x0)[None,:]
                before=y.copy()
                observer(float(t0),np.array([x0]),y)
                if not np.array_equal(y,before):
                    raise ArithmeticError('observer mutated input')
            ray=observer.report()['rays'][0]
            groups.append(dict(steps=n,log_k_defect=ray['maximum_log_k_defect'],
                               mixed_defect=ray['maximum_mixed_transport_defect']))
        if name=='FLRW' and not (groups[1]['log_k_defect']<groups[0]['log_k_defect']/3.8 and groups[1]['mixed_defect']<1e-12):
            raise ArithmeticError('nonzero-flux exact trace integration did not refine')
        if name=='curved_Minkowski' and not (groups[-1]['log_k_defect']<1e-12 and groups[1]['mixed_defect']<groups[0]['mixed_defect']/3.8):
            raise ArithmeticError('curved flat trace control failed')
        controls[name]=groups
    report.update(exact_trace_observer_controls=controls,observer_input_unchanged=True,
                  exact_trace_controls_are_floating=True)
    from scipy.integrate import quad
    from scipy.optimize import brentq
    def trace(radius,label):
        t0=brentq(lambda t0:np.sqrt(1-t0/4)*(label-t0)-radius,0,label)
        y=flrw(t0,label-t0)
        k0,z0=y[1],y[5]
        return k0,z0*z0/radius,y[2]/radius,z0,k0*(1-2*y[7]/radius)
    def depth(label):
        return quad(lambda r0:trace(r0,label)[1],.5,1.,epsabs=1e-11)[0]
    ka,wa,va,za,la=trace(.5,1.5)
    kb,wb,vb,zb,lb=trace(1.,1.5)
    def interior(r0):
        k0,w0,V0,z0,_=trace(r0,1.5)
        return k0*w0/r0+2*z0*V0/r0
    integral=quad(interior,.5,1.,epsabs=1e-11)[0]
    lhs=(depth(1.5+1e-5)-depth(1.5-1e-5))/2e-5
    full=la*wa-lb*wb-integral
    if abs(lhs-full)>1e-8 or abs(lhs+integral)<1e-4:
        raise ArithmeticError('moving fixed-area layer endpoint control')
    report['moving_layer_FLRW_control']=dict(derivative=lhs,full_rhs=full,
                                            discrepancy=abs(lhs-full),
                                            omission_of_endpoint_terms_rejected=True)
    report['negative_controls'].append('moving-area endpoint terms cannot be omitted')
    for name in ['screen_incoming_optical_depth.py','verify_centered_cauchy_diamond.py',
                 'centered_cauchy_diamond.py','charged_cauchy_diamond.py','charged_lobatto.py',
                 'charge_preserving_shell.py']:
        report['source_sha256'][name]=sha256((root/name).read_bytes()).hexdigest()
    (root/'INCOMING_OPTICAL_DEPTH_CHECKS_2026-10-23.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS: exact optical identities, nonzero-depth model and trace negative controls; no PDE certificate')


if __name__ == '__main__':
    main()
