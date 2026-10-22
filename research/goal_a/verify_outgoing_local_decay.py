"""Exact finite-derivative identities in EXIT22; not a global PDE certificate."""
import sympy as s


def check(expression, label):
    if s.simplify(expression) != 0:
        raise RuntimeError(label)


def main():
    r = s.symbols('r', positive=True)
    V, C, h, psi = (s.Function(name)(r) for name in ('V', 'C', 'h', 'psi'))
    j, w = s.diff(h, r), s.diff(h, r, 2)
    d = h-psi/r
    vr, vrr, vrrr = (s.diff(V, r, i) for i in (1, 2, 3))
    cr, crr = s.diff(C, r), s.diff(C, r, 2)
    rhs_j = 2*vr*j+(vrr-vr/r)*d+3*s.I*C*h+s.I*cr*psi
    # partial_r(Dj)=D(j_r)-V_r*j_r+i e a_r*j, e a_r=-2C.
    rhs_w = s.diff(rhs_j, r)+vr*w+2*s.I*C*j
    rhs_w = rhs_w.subs(s.diff(psi, r), h)
    expected = (3*vr*w+(3*vrr-vr/r+5*s.I*C)*j
                +(vrrr-2*vrr/r+2*vr/r**2)*d
                +4*s.I*cr*h+s.I*crr*psi)
    check(rhs_w-expected, 'second radial charged transport')
    if s.simplify(rhs_w-(expected-2*s.I*C*j)) == 0:
        raise RuntimeError('commutator negative control did not reject')
    dvj, duj, tangent, initial_w = s.symbols('dvj duj tangent initial_w')
    # tangent=d_v-d_u and d_v j=lambda*w on the initial curve.
    check((2*(tangent+duj)).subs(tangent, initial_w/2-duj)-initial_w,
          'slanted Cauchy second derivative')
    print('second_transport_commutator_and_slanted_initial_trace: EXACT_ZERO')

    m, Q, P, J, Jr, Qt = s.symbols('m Q P J Jr Qt', real=True)
    f = 1-2*m/r
    Pr = P*(2*m/(f*r**2)-Q**2/(f*r**3))
    mt = r**2*f*P*J
    St = 2*P*Jr+4*(Pr+P/r)*J-2*Q*Qt/(f*r**4)
    # Time derivative of r*S/2+m/(f*r^2)-Q^2/(2*f*r^3).
    lapse_rt = (r*St/2+mt/(f**2*r**2)-Q*Qt/(f*r**3)
                -Q**2*mt/(f**2*r**4))
    candidate_rt = (P*J+r*Pr*J+r*P*Jr
                    +2*(P/f*(1-Q**2/r**2)*J-Q*Qt/(f*r**3)))
    check(lapse_rt-candidate_rt, 'lapse time flux identity')
    wrong_St = St+4*Q*Qt/(f*r**4)
    if s.simplify(lapse_rt+r*(wrong_St-St)/2-candidate_rt) == 0:
        raise RuntimeError('electric sign negative control did not reject')

    # Derive S_t from the covariant wave system using real components.
    xr, xi, yr, yi, zr, zi, pxr, pxi, fxr, fxi, er, Ar = s.symbols(
        'xr xi yr yi zr zi pxr pxi fxr fxi er Ar', real=True)
    Pi, Phi, scalar = xr+s.I*xi, yr+s.I*yi, zr+s.I*zi
    Pir, Phir = pxr+s.I*pxi, fxr+s.I*fxi
    DtPi = P*Phir+(Pr+2*P/r)*Phi
    DtPhi = P*Pir+Pr*Pi-s.I*er*Ar*scalar
    energy_t = s.expand(2*s.re(DtPi*s.conjugate(Pi)
                               +DtPhi*s.conjugate(Phi)))
    Jvalue = s.re(Pi*s.conjugate(Phi))
    Jrvalue = s.re(Pir*s.conjugate(Phi)+Pi*s.conjugate(Phir))
    Ivalue = s.im(scalar*s.conjugate(Phi))
    check(energy_t-(2*P*Jrvalue+4*(Pr+P/r)*Jvalue+2*er*Ar*Ivalue),
          'energy time derivative from covariant waves')
    check((2*er*Ar*Ivalue).subs(Ar, -P*Q/(f*r**2))
          +2*Q*(er*r**2*P*Ivalue)/(f*r**4), 'charge work conversion')
    print('polar_wave_energy_lapse_flux_and_wrong_charge_rejection: PASS')

    # Match polar mass and charge flux directly to the established null flux.
    g, v, ut, dr, di, wr, wi, hr, hi = s.symbols(
        'g v ut dr di wr wi hr hi', real=True, nonzero=True)
    dn, W, H = dr+s.I*di, wr+s.I*wi, hr+s.I*hi
    polar_pi, polar_phi = (dn+W/v)/(2*r), (dn-W/v)/(2*r)
    polar_mt = r**2*f*(2*v*ut)*s.re(polar_pi*s.conjugate(polar_phi))
    null_mt = ut*(-s.expand_complex(W*s.conjugate(W))/g
                  +v*f*s.expand_complex(dn*s.conjugate(dn))/2)
    check((polar_mt-null_mt).subs(v, g*f/2), 'null to polar mass flux')
    polar_qt = er*r**2*(2*v*ut)*s.im(H*s.conjugate(polar_phi))
    null_qt = er*r*ut*s.im(H*s.conjugate(v*dn-W))
    check(polar_qt-null_qt, 'null to polar charge flux')
    print('null_to_polar_mass_and_charge: EXACT_ZERO')
    print('Scope: identities and negative controls only; no PDE estimate certification.')


if __name__ == '__main__':
    main()
