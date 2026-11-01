"""FAR03 finite exact identities and countercontrols; no global PDE certificate."""
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def zero(expr, label):
    if s.simplify(s.expand(expr)) != 0:
        raise ArithmeticError(label)


def main():
    r, p, e = s.symbols('r p e', positive=True)
    b, m, Q, a = s.symbols('b m Q a', real=True)
    pr, pi, zr, zi, vr, vi = s.symbols('pr pi zr zi vr vi', real=True)
    psi, Z, Zr = pr+s.I*pi, zr+s.I*zi, vr+s.I*vi
    norm = lambda z: s.expand(z*s.conjugate(z))
    re = lambda z: s.expand(s.re(z))
    h = Z-psi/r
    phir = h/r
    f = 1-2*m/r
    c = b*f
    br = b*r*norm(phir)
    mr = Q**2/(2*r**2)+r**2*f*norm(phir)/2
    Qr = e*s.im(psi*s.conjugate(Z))
    ar = -b*Q/r**2
    # Independent jet derivative, including all radial Einstein/Maxwell constraints.
    def radial(expr):
        return (s.diff(expr, r)+s.diff(expr, b)*br+s.diff(expr, m)*mr
                +s.diff(expr, Q)*Qr+s.diff(expr, pr)*zr+s.diff(expr, pi)*zi
                +s.diff(expr, zr)*vr+s.diff(expr, zi)*vi)
    cr = b*(2*m/r**2-Q**2/r**3)
    zero(radial(c)-cr, 'radial metric cancellation')
    Zt = c*Zr/2+cr*Z/2-s.I*e*a*Z-(s.I*e*ar/2+cr/(2*r))*psi
    Et = 2*r**p*re(Zt*s.conjugate(Z))
    A = r**(p-1)*(p*c-r*cr)*norm(Z)/2
    scalar_rhs = -r**p*re((s.I*e*ar+cr/r)*psi*s.conjugate(Z))
    zero(Et-radial(c*r**p*norm(Z)/2)+A-scalar_rhs, 'uncompleted actual rp wave')
    J = -c*r**p*norm(Z)/2+b*r**(p-2)*Q**2/2+r**(p-1)*cr*norm(psi)/2
    bulk = A-radial(b*r**(p-2))*Q**2/2-radial(r**(p-1)*cr)*norm(psi)/2
    zero(Et+radial(J)+bulk, 'Maxwell-completed current including electromagnetic boundary')
    y = psi/r
    x, q = m/r, Q/r
    dimensionless = ((p-2*(p+1)*x)*norm(Z)+2*(3-p)*x*norm(y)-norm(h)*norm(y)
                     +q*q*((2-p)+2*re(Z*s.conjugate(y))-(6-p)*norm(y)+norm(h)*norm(y))
                     +2*q*Qr*norm(y))
    zero(2*bulk/(b*r**(p-1))-dimensionless, 'complete nonlinear dimensionless bulk F6')
    if s.simplify(Et+radial(J-b*r**(p-2)*Q**2/2)+bulk) == 0:
        raise ArithmeticError('missing electromagnetic boundary was not rejected')
    # Radial Hardy identity before Cauchy--Schwarz; the inner endpoint is nonzero.
    zero(radial(r**(p-2)*norm(psi))-(p-2)*r**(p-3)*norm(psi)
         -2*r**(p-2)*re(psi*s.conjugate(Z)), 'Hardy differential identity')
    eta, M = s.symbols('eta M', positive=True)
    K2 = 4+64*e**2*M**2
    Lambda2 = 16*e**2*M**2*eta
    zero((8*K2/p+6)*eta+8*Lambda2/p
         -eta*(6+(32+640*e**2*M**2)/p), 'explicit far-radius threshold')
    zero(p/s.Integer(12)-4*(p*(2-p)**2/96)/(2-p)**2-p/24,
         'Hardy absorption constant with b>=1/3')
    # Actual stationary RN balances: finite spacetime Coulomb energy persists.
    R0, T, charge = s.symbols('R0 T charge', positive=True)
    coulomb_bulk_integral = (2-p)*charge**2/2*R0**(p-2)/(2-p)
    inner = charge**2*R0**(p-2)/2
    zero(coulomb_bulk_integral-inner, 'static RN rp boundary pays entire bulk')
    if s.simplify(coulomb_bulk_integral) == 0:
        raise ArithmeticError('RN negative control lost stationary Coulomb field')
    t = s.symbols('t', real=True, nonnegative=True)
    weight = (1+t)**2
    EC = charge**2/(2*R0)
    zero(weight.subs(t,T)*EC-EC-s.integrate(s.diff(weight,t)*EC,(t,0,T)),
         'weighted Kodama static terminal and reservoir cancellation')
    # Generic weighted energy splitting, without assuming a sign for Coulomb work.
    Es = s.Function('Es')(t); Ec = s.Function('Ec')(t)
    w = s.Function('w')(t)
    zero(s.diff(w*(Es+Ec),t)-s.diff(w,t)*(Es+Ec)
         -(s.diff(w*Es,t)-s.diff(w,t)*Es+w*s.diff(Ec,t)),
         'Coulomb work remains after energy split')
    # Finite polynomial control; the C-infinity delayed family is proved in the note.
    z, L = s.symbols('z L', nonnegative=True)
    pulse = z**3*(1-z)**3
    E0 = s.integrate(s.diff(pulse,z)**2,(z,0,1))
    weighted = s.integrate((1+L+z)**2*s.diff(pulse,z)**2,(z,0,1))
    zero(s.diff(weighted,L,2)-2*E0, 'delayed outgoing reference weighted energy grows quadratically')
    if E0 <= 0 or s.limit(weighted,L,s.oo) != s.oo:
        raise ArithmeticError('delay countercontrol')
    root = Path(__file__).resolve().parent
    names = ['verify_far_zone_rp.py', 'FAR_ZONE_RP_AND_COULOMB_BALANCE.md',
             'ACTUAL_BONDI_COMPLETENESS_BRIDGE.md', 'GLOBAL_COVARIANT_MORAWETZ.md',
             '../../definitions/MODEL.md', 'ACCEPTANCE.md']
    report = dict(claim_ids=[f'FAR03.{i}' for i in range(1,6)],
                  logic='PROVED for exact identities and scoped controls; global inequalities are analytic arguments',
                  evidence=['EXACT_ALGEBRA','EXACT_RN_CONTROL','LINEAR_REFERENCE_FINITE_CONTROL'],
                  audit='INTERNAL_AUDIT',
                  checks=['independent radial metric and actual wave jet',
                          'Maxwell-completed rp current with all radial constraints',
                          'full nonlinear dimensionless bulk including b_r and Q_r',
                          'Hardy derivative, explicit threshold and absorption constants',
                          'stationary RN electromagnetic boundary and bulk balance',
                          'weighted Kodama terminal Coulomb balance',
                          'generic scalar/Coulomb energy split with nonzero work',
                          'finite delayed outgoing linear pulse energy moments'],
                  negative_controls=['omitting electromagnetic radial flux fails exact current identity',
                                     'positive static RN Coulomb bulk cannot have zero inner flux',
                                     'bounded unweighted exterior boundary energy does not pay weighted radiation'],
                  pulse_control=dict(unweighted_energy=str(E0),weighted_energy=str(weighted),
                                     is_actual_EMCSF_solution=False),
                  analytic_source='FAR_ZONE_RP_AND_COULOMB_BALANCE.md FAR03.1-FAR03.5',
                  actual_far_zone_global_inequality_computer_certified=False,
                  actual_weighted_radiation_flux_verified=False,late_charge_limit_verified=False,
                  horizon_parameter_agreement_verified=False,RN_convergence_verified=False,goal_A_proved=False,
                  source_sha256={n:sha256((root/n).read_bytes()).hexdigest() for n in names})
    (root/'FAR_ZONE_RP_CHECKS_2026-10-23.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: FAR03 exact constrained rp identities, Hardy constants, RN and delayed reference controls; actual weighted radiation/Goal A OPEN')


if __name__ == '__main__':
    main()
