"""Exact identities/abstract budgets for AF03; no actual PDE certificate."""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import sympy as s


def check(expression, label):
    if s.simplify(expression) != 0:
        raise RuntimeError(label)


def main(replay_candidates=False):
    r, R, nu, lam, Om, nuu, Omu, Qu = s.symbols(
        'r R nu lam Om nuu Omu Qu', real=True, nonzero=True)
    Q = s.symbols('Q', real=True)
    mixed = -nu*lam/r-Om*(1-Q**2/r**2)/(4*r)
    total = (s.diff(mixed, r)*nu+s.diff(mixed, nu)*nuu
             +s.diff(mixed, lam)*mixed+s.diff(mixed, Om)*Omu
             +s.diff(mixed, Q)*Qu)
    terminal = total.subs({r:R, Q:R, lam:0, Qu:0})
    check(terminal+Om*nu/(2*R**2), 'terminal lambda curvature')
    if s.simplify(total.subs({r:R, Q:R, lam:0})-terminal) == 0:
        raise RuntimeError('omitted terminal charge derivative not rejected')

    u, ar, ai, br, bi, e = s.symbols('u ar ai br bi e', real=True)
    P0, P1 = ar+s.I*ai, br+s.I*bi
    phi, P = u*P0+u**2*P1/2, P0+u*P1
    current = s.expand(s.im(phi*s.conjugate(P)))
    check(current.coeff(u, 1), 'linear charge current cancellation')
    check(current.coeff(u, 2)-s.im(P0*s.conjugate(P1))/2,
          'quadratic charge current')
    leading_lam = -Om*nu*u**2/(4*R**2)
    du_difference = -2*R**2*leading_lam*(ar**2+ai**2)/Om
    check(s.integrate(du_difference, (u, 0, u))
          -nu*(ar**2+ai**2)*u**3/6, 'cubic mass charge difference')
    print('terminal_curvature_current_cancellation_and_cubic_difference: EXACT_ZERO')

    # Positive symbols implement nu=-N and p=lambda/nu.
    N, la, om = s.symbols('N la om', positive=True)
    slope = -la/N
    norm = om*s.sqrt(-slope)
    nr = (-slope*(-N)+la)/norm
    sr = (slope*(-N)+la)/norm
    ff = 4*N*la/om**2
    check(nr, 'zero angular extrinsic curvature')
    check(sr**2-ff, 'D=f on l=0 slice')
    Pu, pv = s.symbols('Pu pv')
    gradient = (slope*Pu+pv)/(2*la)
    chi = (-slope*Pu+pv)/(norm*s.sqrt(ff))
    check(gradient-(-Pu/(2*N)+pv/(2*la)), 'spatial scalar gradient')
    check(chi-(Pu/(2*N)+pv/(2*la)), 'normalized scalar momentum')

    m, ch2, grad2, qp = s.symbols('m ch2 grad2 qp', real=True)
    f = 1-2*m/r
    mp = Q**2/(2*r**2)+r**2*f*(ch2+grad2)/2
    difference_r = mp+Q*qp/r-Q**2/(2*r**2)-qp
    expected = r**2*f*(ch2+grad2)/2+(Q/r-1)*qp
    check(difference_r-expected, 'exact mass charge difference constraint')
    if s.simplify(difference_r-r**2*f*(ch2+grad2)/2) == 0:
        raise RuntimeError('electric work term omission not rejected')
    print('zero_angular_slice_and_difference_constraint: EXACT_ZERO')

    # Abstract constants, not bounds for either physical seed.
    # Assume r in [R/2,2R], |phi|<=A*delta, |phi'|,|chi|<=B,
    # r0-R in [c*delta,C*delta], |Q0-R|,|d0|<=D*delta^3.
    results = []
    for RR, c, C, A, B, D in [(F(5),F(1,4),F(2),F(3),F(4),F(8)),
                                (F(15),F(1,32),F(8),F(16),F(64),F(128))]:
        ee = F(3,5)
        qprime_coefficient = 4*ee*RR**2*A*B
        qerror_coefficient = D+qprime_coefficient
        distance_coefficient = C+1+qerror_coefficient
        # With |d|<=L*delta^3 and delta<=1, f <= C_f*delta^2.
        fbase = 4*distance_coefficient**2/RR**2
        # d' <= 4R^2 B^2 f + (2*distance/R)*qprime*delta^2.
        forcing_base = 4*RR**2*B**2*fbase+2*distance_coefficient*qprime_coefficient/RR
        LL = 2*(D+forcing_base+1)
        delta = F(1,2)
        while not (qerror_coefficient*delta<c/2
                   and 4*RR**2*B**2*4*LL*delta/RR<LL/2
                   and 4*LL*delta/RR<c**2/(32*RR**2)
                   and (C+1)*delta<RR/2):
            delta /= 2
        # A direct scalar f upper bound retains the d part in the budget.
        fupper_coefficient = fbase+4*LL*delta/RR
        forcing = 4*RR**2*B**2*fupper_coefficient+2*distance_coefficient*qprime_coefficient/RR
        if not D+forcing<LL:
            raise RuntimeError('abstract difference bootstrap not improved')
        flower_coefficient = c**2/(16*RR**2)-4*LL*delta/RR
        if flower_coefficient <= 0:
            raise RuntimeError('abstract untrapped margin not positive')
        results.append(str(delta))
    print('abstract_delta2_vs_delta3_budgets: PASS', ', '.join(results))
    if replay_candidates:
        from certify_early_charged_constraints import certify
        folder = Path(__file__).resolve().parent
        certificate_name = 'EARLY_CHARGED_CONSTRAINT_CERTIFICATE_N2048_2026-10-17.json'
        certificate = json.loads((folder/certificate_name).read_text())
        if certificate['status'] != 'PASS' or certificate['fixed_coupling'] != '3/5':
            raise RuntimeError('wrong source certificate or coupling')
        for name, wanted in certificate['source_sha256'].items():
            if sha256((folder/name).read_bytes()).hexdigest() != wanted:
                raise RuntimeError('stale null constraint source: '+name)
        replayed = []
        for record in certificate['runs']:
            if record['status'] != 'PASS':
                raise RuntimeError('failed source seed')
            fresh = certify(F(record['amplitude']), F(record['frequency']), record['cells'])
            for key in ('initial_f', 'initial_p', 'charge_integral', 'radius',
                        'cap', 'scale', 'terminal_H', 'minimum_dimensionless_radius_lower',
                        'minimum_H_lower'):
                if fresh[key] != record[key]:
                    raise RuntimeError('constraint replay mismatch: '+key)
            replayed.append({'amplitude':record['amplitude'],
                             'frequency':record['frequency'], 'cells':record['cells']})
        if {(row['amplitude'], row['frequency']) for row in replayed} != {('1/5','8'),('3/10','4')}:
            raise RuntimeError('unexpected candidate inventory')
        names = ['verify_af_transverse_flux.py', 'AF_REALIZATION_WITH_TRANSVERSE_FLUX.md',
                 certificate_name, '../../definitions/MODEL.md']
        result = dict(status='PASS', replayed_constraint_seeds=replayed,
                      exact_endpoint_slice_and_constraint_identities=True,
                      abstract_budget_widths=results,
                      actual_AF_collar_constants_certified=False,
                      numerical_full_AF_data_constructed=False,
                      two_dimensional_early_screen_certified=False,
                      analytical_AF_realization_independently_reviewed=False,
                      critical_curve_and_three_branches_proved=False,
                      source_sha256={name:sha256((folder/name).read_bytes()).hexdigest()
                                     for name in names})
        (folder/'AF_TRANSVERSE_FLUX_VALIDATION_2026-10-18.json').write_text(
            json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print('candidate_null_constraint_replay: PASS', len(replayed), 'seeds')
    print('Scope: exact identities and abstract budgets; actual seed constants not certified.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay-candidates', action='store_true')
    main(parser.parse_args().replay_candidates)
