"""Exact pullback identities and independent numerical AF-interface checks."""
import json
from pathlib import Path
from hashlib import sha256
import numpy as np
import sympy as sy
from scipy.integrate import solve_ivp
from rotating_af_numeric import SmoothFreeProfile
from charged_lobatto import evolve


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


def exact_checks():
    r, N, L, O, b = sy.symbols('r N L O b', positive=True)
    ar, ai, br, bi = sy.symbols('ar ai br bi', real=True)
    p, nu = -b*b, -N
    w = L+p*nu
    f = -4*nu*L/O**2
    D = w*w/(O*O*b*b)
    ell = -(L-p*nu)/(r*O*b)
    P, pv = ar+sy.I*ai, br+sy.I*bi
    gradient, chi = (p*P+pv)/w, (-p*P+pv)/w
    abs2 = lambda z: sy.expand(z*sy.conjugate(z))
    J = sy.re(sy.expand(chi*sy.conjugate(gradient)))
    energy = r*r*D*(abs2(chi)+abs2(gradient))/2+r**3*ell*w/(O*b)*J
    transported = -2*r*r*(p*L*abs2(P)+nu*abs2(pv))/(O*O*w)
    require(sy.simplify(D-f-r*r*ell*ell) == 0, 'induced metric identity')
    require(sy.simplify(energy-transported) == 0, 'independent null mass flux pullback')
    require(sy.simplify(chi-(pv-p*P)/w) == 0, 'charge current pullback')
    # Independent second fundamental form of an arbitrary flat spacelike graph.
    pp = sy.symbols('pp', real=True)
    pvar = sy.symbols('pvar', negative=True)
    flatell = -(1+pvar)/(2*r*sy.sqrt(-pvar))
    ellr = sy.diff(flatell, r)+sy.diff(flatell, pvar)*pp/((1-pvar)/2)
    require(sy.simplify(flatell+r*ellr+pp/(2*(-pvar)**sy.Rational(3, 2))) == 0,
            'geometric radial K sign')
    return ['induced_metric', 'null_mass_flux', 'charge_current', 'geometric_radial_K']


def backwards_rn():
    M, Q, R = 2., 1., 5.
    flow = solve_ivp(lambda t, r: [(1-2*M/r[0]+Q*Q/r[0]**2)/2],
                     (0., 5.), [R], method='DOP853', rtol=5e-14, atol=5e-15,
                     dense_output=True)
    def exact(u, v):
        r = float(flow.sol(v-u)[0])
        f = 1-2*M/r+Q*Q/r**2
        return np.array([r, .5, 0., 0., -f/2, 0., 0., M-Q*Q/(2*r), 0., 0., Q, Q/r])
    runs = []
    for n in (8, 16, 32):
        data = evolve(lambda v: exact(0., v), lambda u: exact(u, 0.), -1.,
                      np.linspace(0., 4., n+1), n)
        error = float(max(abs(data['state'][-1, -1]-exact(-1., 4.))))
        runs.append(dict(n=n, endpoint_error=error))
    for old, new in zip(runs, runs[1:]):
        require(new['endpoint_error'] < old['endpoint_error']/10, 'backwards RN convergence')
    return runs


def independent_mass_solve(smooth, stored):
    state = np.array([0., 0.])  # Q,m instead of Q,f; original signed source.
    max_f, max_Q = 0., 0.
    def fun(r, y):
        Q, m = y
        phi, gradient, chi, ell, _ = smooth.free(r)
        f = 1-2*m/r
        D = f+(r*ell)**2
        require(f > 0, 'independent mass solve lost untrapped condition')
        energy = .5*r*r*D*(abs(chi)**2+abs(gradient)**2)
        energy += r**3*ell*np.sqrt(D)*np.real(chi*np.conj(gradient))
        return [.6*r*r*np.imag(phi*np.conj(chi)), Q*Q/(2*r*r)+energy]
    for left, right in zip(smooth.breaks[:-1], smooth.breaks[1:]):
        sol = solve_ivp(fun, (left, right), state, method='DOP853',
                        rtol=2e-12, atol=2e-14, max_step=(right-left)/4)
        require(sol.success, 'independent mass integration failed')
        state = sol.y[:, -1]
        j = int(np.argmin(abs(stored['r']-right)))
        require(abs(stored['r'][j]-right) < 1e-12, 'stored blend endpoint absent')
        max_f = max(max_f, abs(1-2*state[1]/right-stored['f'][j]))
        max_Q = max(max_Q, abs(state[0]-stored['Q'][j]))
    require(max_f < 2e-8 and max_Q < 2e-8, 'independent Q,m comparison')
    # Non-node free-function derivative check; avoids a check identical to RHS.
    discrepancy = 0.
    for i in np.linspace(2, len(smooth.r)-4, 30).astype(int):
        left, right = smooth.r[i:i+2]
        at = left+.41*(right-left)
        h = (right-left)*1e-3
        derivative = (smooth.free(at-2*h)[0]-8*smooth.free(at-h)[0]
                      +8*smooth.free(at+h)[0]-smooth.free(at+2*h)[0])/(12*h)
        discrepancy = max(discrepancy, abs(derivative-smooth.free(at)[1]))
    require(discrepancy < 1e-7, 'smooth profile analytic derivative')
    return dict(maximum_f_difference=float(max_f), maximum_Q_difference=float(max_Q),
                profile_derivative_difference=float(discrepancy))


def main():
    folder = Path(__file__).resolve().parent
    algebra = exact_checks()
    rn = backwards_rn()
    records = {}
    source_files = ['verify_rotating_af_interface.py', 'rotating_af_numeric.py',
                    'rotating_past_slice.py', 'constraint_contraction.py', 'charged_lobatto.py']
    for label in ('A020_W8', 'A030_W4'):
        reports = []
        for n in (48, 96, 192):
            name = f'ROTATING_PAST_SLICE_{label}_N{n}_2026-10-21.json'
            reports.append(json.loads((folder/name).read_text(encoding='utf-8')))
            source_files.append(name)
        for old, new in zip(reports, reports[1:]):
            for key, residual in old['bulk_residuals'].items():
                require(new['bulk_residuals'][key] < residual/2, label+' '+key+' refinement')
        finest = reports[-1]
        require(finest['omitted_gauge_bulk_residual'] > 10*finest['bulk_residuals']['scalar_radial_gauge'],
                'omitting radial gauge must be detected')
        name = f'ROTATING_PAST_SLICE_{label}_N192_2026-10-21.npz'
        source_files.append(name)
        with np.load(folder/name) as a:
            smooth = SmoothFreeProfile(dict(a), finest['depth'])
        name = f'ROTATING_AF_{label}_N192_2026-10-21_S1.npz'
        source_files.append(name)
        with np.load(folder/name) as stored:
            comparison = independent_mass_solve(smooth, stored)
        records[label] = comparison
    report = dict(status='PASS', exact_identities=algebra, backwards_RN=rn,
        independent_constraint_comparisons=records,
        source_sha256={name: sha256((folder/name).read_bytes()).hexdigest() for name in source_files},
        scope='algebra, known-solution convergence, independent numerical constraint formulation',
        all_radius_error_certified=False, actual_seed_transfer_certified=False,
        early_future_screen_certified=False, goal_A_proved=False)
    (folder/'ROTATING_AF_INTERFACE_CHECKS_2026-10-21.json').write_text(
        json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'source_sha256'}, indent=2))


if __name__ == '__main__':
    main()
