"""Independent symbolic identities, constraint residuals, and vacuum regression."""
from dataclasses import replace
import json
from pathlib import Path
import numpy as np
import sympy as s
import mpmath as mp
from fractions import Fraction
from hashlib import sha256
from certify_charge_shell_initial import certificate
from charge_preserving_shell import ChargePreservingShell, ShellParameters
from centered_cauchy_diamond import axis_state, evolve_centered
from screen_charge_preserving_shell import Diagnostics


def verify():
    r, a, ap, d, w, f = s.symbols('r a ap d w f', real=True, positive=True)
    chi = -d*(ap+a/r)-s.I*w*a
    gradient = ap+s.I*d*w*a
    current = s.simplify(s.im(a*s.conjugate(chi))-w*a*a)
    energy = s.simplify(s.expand_complex(abs(chi)**2+abs(gradient)**2)
                        -(ap*ap+d*d*(ap+a/r)**2+(1+d*d)*w*w*a*a))
    incoming = s.simplify(a+r*(chi+gradient)-(1-d)*(a+r*ap-s.I*r*w*a))
    outgoing = s.simplify(-a+r*(chi-gradient)+(1+d)*(a+r*ap+s.I*r*w*a))
    assert (current, energy, incoming, outgoing) == (0, 0, 0, 0)
    # Removing the normal imaginary component must destroy the prescribed charge.
    wrong_current = s.simplify(s.im(a*s.conjugate(-d*(ap+a/r)))-w*a*a)
    assert wrong_current != 0
    p = ShellParameters(amplitude=.3, frequency=.3, direction=.65)
    plus = ChargePreservingShell(p)
    minus = ChargePreservingShell(replace(p, direction=-p.direction))
    center = ChargePreservingShell(replace(p, direction=0.))
    grid = np.linspace(plus.inner, plus.outer, 1001)
    symmetry_error = float(np.max(abs(plus.sol.sol(grid)-minus.sol.sol(grid))))
    charge_error = float(np.max(abs(plus.sol.sol(grid)[0]-center.sol.sol(grid)[0])))
    assert symmetry_error < 1e-12 and charge_error < 1e-9
    # Held-out finite-difference check of Gauss and Hamiltonian equations.
    residuals = []
    for n in [512, 1024, 2048]:
        radii = np.linspace(plus.inner, plus.outer, n+1)
        Q, fvalues, _ = plus.sol.sol(radii)
        h = radii[1]-radii[0]
        m = radii*(1-fvalues)/2
        dq = (Q[:-4]-8*Q[1:-3]+8*Q[3:-1]-Q[4:])/(12*h)
        dm = (m[:-4]-8*m[1:-3]+8*m[3:-1]-m[4:])/(12*h)
        gauss, hamiltonian = [], []
        for j, at in enumerate(radii[2:-2]):
            phi, g, chi = plus.free(at)
            q, fv = Q[j+2], fvalues[j+2]
            gauss.append(dq[j]-.6*at*at*(phi*chi.conjugate()).imag)
            hamiltonian.append(dm[j]-q*q/(2*at*at)-at*at*fv*(abs(chi)**2+abs(g)**2)/2)
        residuals.append(dict(intervals=n, gauss=float(max(abs(np.array(gauss)))),
                              hamiltonian=float(max(abs(np.array(hamiltonian))))))
    assert residuals[-1]['gauss'] < 1e-7 and residuals[-1]['hamiltonian'] < 1e-7
    vacuum = ChargePreservingShell(replace(p, amplitude=0.))
    observer = Diagnostics(vacuum, 2.)
    result = evolve_centered(vacuum.state_at_proper, axis_state(.5, 0j), 0j,
                             vacuum.proper_max, 2., 32, observer=observer)
    reference = evolve_centered(vacuum.state_at_proper, axis_state(.5, 0j), 0j,
                                vacuum.proper_max, 2., 32)
    assert result['completed'] and np.array_equal(result['state'], reference['state'])
    vacuum_mass_error = float(np.max(abs(result['state'][:, 7])))
    assert vacuum_mass_error < 1e-12 and abs(observer.axis_proper_time-2.) < 1e-12
    coarse, fine = certificate(128), certificate(1024)
    clo, chi = Fraction(coarse['charge_lower']), Fraction(coarse['charge_upper'])
    flo, fhi = Fraction(fine['charge_lower']), Fraction(fine['charge_upper'])
    assert clo <= flo <= fhi <= chi
    with mp.workdps(60):
        charge = mp.mpf('0.6')*mp.mpf('0.15')*mp.mpf('0.4')**2*4*mp.quad(
            lambda z: (10+4*z)**2*mp.exp(-2*z*z/(1-z*z)) if abs(z)<1 else 0,
            [-1, 0, 1])
        assert mp.mpf(flo.numerator)/flo.denominator < charge < mp.mpf(fhi.numerator)/fhi.denominator
        charge_display = mp.nstr(charge, 35)
    return dict(symbolic_current_energy_and_null_decomposition=True, negative_control_rejected=True,
                opposite_direction_geometry_error=symmetry_error,
                direction_independent_charge_error=charge_error, initial_constraint_residuals=residuals,
                observer_preserves_vacuum_evolution=True, vacuum_mass_error=vacuum_mass_error,
                nested_charge_enclosures=True, independent_60_digit_charge=charge_display,
                high_precision_check_is_not_certificate=True,
                finite_PDE_error_certified=False, goal_A_proved=False)


if __name__ == '__main__':
    result = verify()
    result['source_sha256'] = {name: sha256(Path(name).read_bytes()).hexdigest() for name in
        ['verify_charge_preserving_shell.py', 'charge_preserving_shell.py',
         'certify_charge_shell_initial.py', 'screen_charge_preserving_shell.py',
         'centered_cauchy_diamond.py']}
    Path('CHARGE_PRESERVING_SHELL_CHECKS_2026-10-22.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
