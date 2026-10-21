"""Low-order polar-coordinate and gauge parity checks; not all-order proof."""
import sympy as s


def main():
    e,I,J,N,P=s.symbols('e I J N P',real=True)
    h0,h1,h3=s.symbols('h0 h1 h3')
    b2=N/24
    h2dot=3*h3/2+N*h1/24+s.I*e**2*I*h0/6
    bare=h1*b2/6-h2dot/6+h3/4
    assert s.simplify(bare+s.I*e**2*I*h0/36)==0
    gauged=bare+s.I*e**2*I*h0/36
    assert s.simplify(gauged)==0
    assert s.simplify(bare)!=0
    print('scalar_cubic_gauge_cancellation_and_negative_control: PASS')
    # P=Re(h1*conj(h2)), so Ndot=2P and b2dot=P/12.
    assert s.simplify(5*P/18-2*P/6+2*(P/12)/3)==0
    assert s.simplify(P/6-2*P/12)==0
    print('lapse_and_radial_metric_cubic_parity: PASS')
    # J=Im(h0*conj(h2))=Idot.
    a3=-e*J/18
    a2dot=-e*J/12
    assert s.simplify(a3-a2dot+a2dot/3)==0
    assert s.simplify(e*J/6-e*J/6)==0
    print('temporal_potential_cubic_and_charge_quartic_parity: PASS')
    print('Scope: low-order algebra; all-order parity and spacetime completeness need analysis.')


if __name__=='__main__':
    main()
