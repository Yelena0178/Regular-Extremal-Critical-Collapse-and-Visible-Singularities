"""Smooth charge-preserving direction family; floating constraint reconstruction.

Fixed coupling e=3/5. phi=a exp(i*d*w*(r-R)),
chi=exp(i*d*w*(r-R))*(-d*(a'+a/r)-i*w*a), ell=0.
The entire charge profile is independent of d; f is even in d.
No continuous-radius or future PDE error certificate is supplied.
"""
from dataclasses import dataclass, asdict
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


@dataclass(frozen=True)
class ShellParameters:
    amplitude: float = .2
    frequency: float = .3
    direction: float = 0.
    radius: float = 10.
    width: float = 4.

    def __post_init__(self):
        if not all(np.isfinite(v) for v in asdict(self).values()):
            raise ValueError('finite parameters required')
        if self.amplitude < 0 or self.frequency <= 0 or not -1 <= self.direction <= 1:
            raise ValueError('invalid amplitude, frequency or direction')
        if not 0 < self.width < self.radius:
            raise ValueError('a nonempty flat central cap is required')


class ChargePreservingShell:
    def __init__(self, parameters, exterior_width=50., tolerance=2e-11):
        self.parameters = parameters
        self.inner = parameters.radius-parameters.width
        self.outer = parameters.radius+parameters.width
        self.radius_max = self.outer+exterior_width
        self.tolerance = tolerance
        if exterior_width <= 0:
            raise ValueError('positive exterior width required')
        initial = np.array([0., 1., self.inner])  # Q, f, proper distance
        self.sol = solve_ivp(self.constraint_rhs, (self.inner, self.outer), initial,
                             method='DOP853', rtol=tolerance, atol=tolerance/100,
                             max_step=parameters.width/64, dense_output=True)
        if not self.sol.success:
            raise ArithmeticError(self.sol.message)
        Q, f, self.proper_support = self.sol.y[:, -1]
        self.ADM_charge = float(Q)
        self.ADM_mass = float(self.outer*(1-f)/2+Q*Q/(2*self.outer))
        # The vacuum tail is explicit. A positive support endpoint alone does
        # not exclude a zero farther out; inspect its possible interior minimum.
        if self.ADM_mass > 0 and Q*Q/self.ADM_mass > self.outer:
            tail_min = 1-self.ADM_mass**2/(Q*Q)
        else:
            tail_min = min(float(f), 1.)
        if tail_min <= 0:
            raise ArithmeticError('vacuum exterior is not everywhere untrapped')
        self.tail = solve_ivp(lambda r, y: [1/np.sqrt(self.tail_f(r))],
                             (self.outer, self.radius_max), [self.proper_support],
                             method='DOP853', rtol=tolerance, atol=tolerance/100,
                             max_step=exterior_width/100, dense_output=True)
        if not self.tail.success:
            raise ArithmeticError(self.tail.message)
        self.proper_max = float(self.tail.y[0, -1])

    def envelope(self, r):
        p = self.parameters
        z = (r-p.radius)/p.width
        if abs(z) >= 1:
            return 0., 0.
        a = p.amplitude*np.exp(1-1/(1-z*z))
        return a, -2*z*a/(p.width*(1-z*z)**2)

    def free(self, r):
        a, ap = self.envelope(r)
        p = self.parameters
        phase = np.exp(1j*p.direction*p.frequency*(r-p.radius))
        phi = phase*a
        gradient = phase*(ap+1j*p.direction*p.frequency*a)
        chi = phase*(-p.direction*(ap+a/r)-1j*p.frequency*a)
        return phi, gradient, chi

    def constraint_rhs(self, r, y):
        Q, f, _ = y
        if f <= 0 or not np.isfinite(y).all():
            raise ArithmeticError('constraint solve lost f>0')
        a, ap = self.envelope(r)
        p = self.parameters
        S = ap*ap+p.direction**2*(ap+a/r)**2+(1+p.direction**2)*p.frequency**2*a*a
        return [.6*p.frequency*r*r*a*a, (1-f)/r-Q*Q/r**3-r*f*S, 1/np.sqrt(f)]

    def tail_f(self, r):
        return 1-2*self.ADM_mass/r+self.ADM_charge**2/r**2

    def radial_at_proper(self, x):
        if not 0 <= x <= self.proper_max:
            raise ValueError('outside initialized proper-distance interval')
        if x <= self.inner:
            return float(x), 0., 1.
        if x <= self.proper_support:
            r = brentq(lambda r: self.sol.sol(r)[2]-x, self.inner, self.outer,
                       xtol=2e-13, rtol=2e-14)
            Q, f = self.sol.sol(r)[:2]
            return r, float(Q), float(f)
        r = brentq(lambda r: self.tail.sol(r)[0]-x, self.outer, self.radius_max,
                   xtol=2e-13, rtol=2e-14)
        return r, self.ADM_charge, self.tail_f(r)

    def state_at_proper(self, x):
        r, Q, f = self.radial_at_proper(float(x))
        if r <= 0:
            raise ValueError('axis is supplied separately')
        phi, gradient, chi = self.free(r)
        root = np.sqrt(f)
        nu, kappa = -root/2, 1/(2*root)
        V, P = root*(chi+gradient)/2, root*(chi-gradient)/2
        theta, z = r*V, r*P/nu
        return np.array([r, kappa, theta.real, theta.imag, nu, z.real, z.imag,
                         r*(1-f)/2, phi.real, phi.imag, Q, 0.])

    def summary(self):
        radii = np.linspace(self.inner, self.outer, 4097)
        return dict(parameters=asdict(self.parameters), coupling=.6,
                    initial_gauge='initial proper distance; Omega^2=1; A_u=A_v=0; ell=0',
                    ADM_mass=self.ADM_mass, ADM_charge=self.ADM_charge,
                    minimum_sampled_initial_f=float(self.sol.sol(radii)[1].min()),
                    proper_support=float(self.proper_support), proper_max=self.proper_max,
                    initialization_tolerance=self.tolerance,
                    initialization_error_certified=False,
                    all_radius_initial_positivity_certified=False)
