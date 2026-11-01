"""Independent backgrounds and Cauchy gauge/constraint checks, all numerical E0."""
from pathlib import Path
from hashlib import sha256
import json
import numpy as np
from scipy.integrate import solve_ivp
from charged_lobatto import rhs
from charged_cauchy_diamond import evolve
from canonical_cauchy_data import CanonicalCauchyData
from verify_neutral_transport import flrw_state


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def known_backgrounds():
    M, Q, R = 2., 1., 5.
    flow = solve_ivp(lambda t, r: [(1-2*M/r[0]+Q*Q/r[0]**2)/2],
                     (0., 8.), [R], method='DOP853', rtol=5e-14, atol=5e-15, dense_output=True)
    def rn(t, x):
        r = float(flow.sol(2*x)[0])
        f = 1-2*M/r+Q*Q/r**2
        return np.array([r, .5, 0., 0., -f/2, 0., 0., M-Q*Q/(2*r), 0., 0., Q, Q/r])
    def flrw(t, x):
        u, v = t-x, t+x
        r, k, theta, nu, z, m = flrw_state(u, v)
        phi = np.sqrt(3)/2*np.log(1-(u+v)/8)
        return np.array([r, k, theta, 0., nu, z, 0., m, phi, 0., 0., 0.])
    def minkowski(t, x):
        alpha = 1.4
        r = (alpha*(t+x)-(t-x)/alpha)/2
        return np.array([r, alpha/2, 0., 0., -1/(2*alpha), 0., 0., 0., 0., 0., 0., 0.])
    groups = {}
    for label, exact in [('RN', rn), ('FLRW', flrw), ('tilted_Minkowski', minkowski)]:
        runs = []
        for steps in (16, 32, 64):
            data = evolve(lambda x: exact(0., x), .5, 3.5, .25, steps)
            require(data['completed'], label+' stopped')
            target = np.array([exact(.25, x) for x in data['x']])
            error = float(np.max(abs(data['state']-target)))
            runs.append(dict(steps=steps, maximum_state_error=error,
                             constraints=data['final_row_constraints']))
        if label == 'tilted_Minkowski':
            require(max(row['maximum_state_error'] for row in runs) < 1e-11, label+' exactness')
        else:
            for old, new in zip(runs, runs[1:]):
                require(new['maximum_state_error'] < old['maximum_state_error']/3.5,
                        label+' second-order convergence')
        groups[label] = runs
    return groups


def initial_constraints(data):
    records = []
    for x in (3., 3.5, 4., 4.5, 5., 5.5, 6., 8., 15., 25.):
        y = data.state_at_proper(x)
        r, Q, f = data.radial_at_proper(x)
        phi, gradient, chi, ell, ellp = data.free(r)
        D = f+(r*ell)**2
        root = np.sqrt(D)
        kr = ell+r*ellp-r*root*np.real(chi*np.conj(gradient))
        h = 2e-5
        dx = (data.state_at_proper(x-2*h)-8*data.state_at_proper(x-h)
              +8*data.state_at_proper(x+h)-data.state_at_proper(x+2*h))/(12*h)
        flow = rhs(y)
        nu, k = y[4], y[1]
        z, ph = complex(*y[5:7]), complex(*y[8:10])
        rho = dict(radius=float(abs(dx[0]+nu-k*f)),
            scalar=float(abs(complex(*flow[8:10])-complex(*dx[8:10])-nu*z/r)),
            charge=float(abs(flow[10]-dx[10]+.6*r*nu*np.imag(ph*np.conj(z)))),
            mass=float(abs(flow[7]-dx[7]-Q*Q*nu/(2*r*r)-f*nu*abs(z)**2/2)),
            initial_k=float(abs(2*flow[1]/k+dx[1]/k+2*flow[4]/nu-dx[4]/nu+2*kr)),
            omega_normalization=float(abs(-4*k*nu-1)),
            scalar_normal=float(abs(nu*z/r+complex(*y[2:4])/r-root*chi)),
            scalar_tangent=float(abs(complex(*y[2:4])/r-nu*z/r-root*gradient)))
        records.append(dict(x=x, r=r, residuals=rho))
    maxima = {key: max(row['residuals'][key] for row in records) for key in records[0]['residuals']}
    require(max(maxima.values()) < 2e-6, 'canonical Cauchy constraints/gauge')
    return dict(maximum_residuals=maxima, sampled_points=records)


def core_checks(data):
    errors = []
    for x in (.2, .7, .8*data.vacuum_proper_end):
        errors.append(float(max(abs(data.vacuum_state(0., x)-data.state_at_proper(x)))))
    require(max(errors) < 2e-10, 'analytic vacuum boundary does not match initial data')
    residuals = []
    for u, v in [(-.5, 1.), (.3, 1.2), (.5, .85*data.vacuum_proper_end)]:
        t, x = (u+v)/2, (v-u)/2
        h = 1e-5
        y = data.vacuum_state(t, x)
        du = (data.vacuum_state(t+h/2, x-h/2)-data.vacuum_state(t-h/2, x+h/2))/(2*h)
        dv = (data.vacuum_state(t+h/2, x+h/2)-data.vacuum_state(t-h/2, x-h/2))/(2*h)
        residuals.append(float(max(abs(np.r_[du[:4], dv[4:]]-rhs(y)))))
    require(max(residuals) < 2e-7, 'flat-boundary characteristic equations')
    try:
        data.vacuum_state(data.vacuum_proper_end, .1)
    except ValueError:
        pass
    else:
        raise ArithmeticError('vacuum boundary accepted beyond incoming matter ray')
    return dict(initial_match=max(errors), maximum_characteristic_residual=max(residuals),
                out_of_domain_boundary_rejected=True)


def main():
    folder = Path(__file__).resolve().parent
    result = dict(status='PASS', backgrounds=known_backgrounds(), initial_constraints={}, core_checks={})
    names = ['verify_charged_cauchy_diamond.py', 'charged_cauchy_diamond.py', 'canonical_cauchy_data.py',
             'charged_lobatto.py', 'verify_neutral_transport.py']
    for label in ('A020_W8', 'A030_W4'):
        name = 'ROTATING_CANONICAL_'+label+'_2026-10-21.npz'
        data = CanonicalCauchyData(folder/name)
        result['initial_constraints'][label] = initial_constraints(data)
        result['core_checks'][label] = core_checks(data)
        names.append(name)
    result.update(finite_PDE_error_certified=False, full_future_classified=False, goal_A_proved=False,
                  source_sha256={name: sha256((folder/name).read_bytes()).hexdigest() for name in names})
    (folder/'CHARGED_CAUCHY_DIAMOND_CHECKS_2026-10-22.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'],
        background_errors={key: [row['maximum_state_error'] for row in rows] for key, rows in result['backgrounds'].items()},
        initial_residuals={key: val['maximum_residuals'] for key, val in result['initial_constraints'].items()},
        core_checks=result['core_checks'],
        finite_PDE_error_certified=False), indent=2))


if __name__ == '__main__':
    main()
