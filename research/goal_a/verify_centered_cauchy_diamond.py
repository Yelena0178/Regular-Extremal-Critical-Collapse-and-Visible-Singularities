"""Known regular-axis solutions, including nonzero scalar flux; E0 only."""
import json
from pathlib import Path
from hashlib import sha256
import numpy as np
from centered_cauchy_diamond import axis_state, axis_flow, reconstruct_axis, evolve_centered
from charged_lobatto import rhs


def flrw(t, x):
    a = np.sqrt(1-t/4)
    adot = -1/(8*a)
    r = a*x
    nu = (adot*x-a)/2
    k = -a*a/(4*nu)
    V = -np.sqrt(3)/(16*a*a)
    phi = np.sqrt(3)*np.log(a)
    return np.array([r, k, r*V, 0., nu, r*V/nu, 0., adot*adot*x**3/(2*a), phi, 0., 0., 0.])


def curved_flat(t, x):
    u, v = t-x, t+x
    F = lambda y: y+.03*y**3
    dF = lambda y: 1+.09*y*y
    return np.array([(F(v)-F(u))/2, dF(v)/2, 0., 0., -dF(u)/2, 0., 0., 0., 0., 0., 0., 0.])


def complex_flrw(t, x):
    y = flrw(t, x)
    for j in (2, 5, 8):
        value = y[j]*np.exp(.7j)
        y[j], y[j+1] = value.real, value.imag
    return y


def main():
    groups = {}
    for name, exact, V0 in [('FLRW', flrw, -np.sqrt(3)/16),
                           ('complex_FLRW', complex_flrw, -np.sqrt(3)*np.exp(.7j)/16),
                           ('curved_Minkowski', curved_flat, 0j)]:
        runs = []
        for n in (32, 64, 128, 256):
            result = evolve_centered(lambda x: exact(0., x), exact(0., 0.), V0, 3., 1., n)
            if not result['completed']:
                raise ArithmeticError(name+' evolution stopped')
            target = np.array([exact(1., x) for x in result['x']])
            error = np.max(abs(result['state']-target), axis=0)
            axis_error = np.max(abs(result['state'][0]-target[0]))
            runs.append(dict(steps=n, maximum_state_error=float(max(error)), axis_state_error=float(axis_error),
                             axis_radial_defect=result['maximum_axis_radial_defect'],
                             axis_kappa_defect=result['maximum_axis_kappa_defect'],
                             minimum_lambda=result['worst']['lambda_value'],
                             final_constraints=result['final_row_constraints']))
        ratios = [a['maximum_state_error']/b['maximum_state_error'] for a,b in zip(runs, runs[1:])]
        if not all(3.2 < q < 5. for q in ratios):
            raise ArithmeticError(name+' failed second-order check: '+str(ratios))
        groups[name] = dict(runs=runs, error_ratios=ratios)
    # The axis RHS is a genuine limit of the positive-radius FLRW equations.
    endpoint = flrw(.5, 0.)
    target = axis_flow(endpoint[1], -np.sqrt(3)/(16*(1-.5/4)))
    defects = [float(np.max(abs(rhs(flrw(.5, h))-target))) for h in (1e-3, 1e-4, 1e-5)]
    if not defects[-1] < defects[0]/90:
        raise ArithmeticError('axis RHS limit failed')
    folder = Path(__file__).resolve().parent
    names = ['centered_cauchy_diamond.py','verify_centered_cauchy_diamond.py',
             'charged_cauchy_diamond.py','charged_lobatto.py']
    report = dict(status='PASS', backgrounds=groups, axis_RHS_limit_errors=defects,
                  source_sha256={name: sha256((folder/name).read_bytes()).hexdigest() for name in names},
                  finite_PDE_error_certified=False, full_future_classified=False, goal_A_proved=False)
    (folder/'CENTERED_CAUCHY_DIAMOND_CHECKS_2026-10-22.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status='PASS',
        errors={name:[row['maximum_state_error'] for row in group['runs']] for name,group in groups.items()},
        ratios={name:group['error_ratios'] for name,group in groups.items()},
        axis_RHS_limit_errors=defects), indent=2))


if __name__ == '__main__':
    main()
