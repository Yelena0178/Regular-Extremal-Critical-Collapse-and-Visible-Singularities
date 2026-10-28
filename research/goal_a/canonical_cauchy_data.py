"""E0 evaluation of the exact A-AF05 input, in initial proper-distance gauge.

The frozen dyadic coefficients define the target Cauchy data. This evaluator
uses floating ODE integration and inversion; it does not certify those errors.
"""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from certify_rotating_af_barrier import segments
from constraint_contraction import scalar_mass_source
from rotating_af_numeric import step


class CanonicalCauchyData:
    def __init__(self, path, parameter=1., exterior_width=2., tolerance=2e-12):
        if not np.isfinite(parameter) or parameter < 0 or exterior_width <= 0:
            raise ValueError('invalid contraction parameter or exterior width')
        self.path = Path(path)
        self.digest = sha256(self.path.read_bytes()).hexdigest()
        with np.load(self.path) as raw:
            self.data = dict(raw)
        self.segments = segments(self.data)
        self.edges = np.array([self.segments[0][0]]+[part[1] for part in self.segments])
        self.parameter = parameter
        self.inner, self.outer = self.edges[0], self.edges[-1]
        self.radius_max = self.outer+exterior_width
        self.tolerance = tolerance
        self.solutions = []
        self.proper_ends = []
        state = np.array([0., 1., self.inner, self.inner])  # Q, f, x, flat-cap V(x)
        radial_edges = np.r_[self.edges, self.radius_max]
        for left, right in zip(radial_edges[:-1], radial_edges[1:]):
            sol = solve_ivp(self.constraint_rhs, (left, right), state,
                            method='DOP853', rtol=tolerance, atol=tolerance/100,
                            max_step=(right-left)/8, dense_output=True)
            if not sol.success:
                raise ArithmeticError(sol.message)
            state = sol.y[:, -1]
            self.solutions.append((left, right, sol.sol))
            self.proper_ends.append(state[2])
        self.proper_ends = np.array(self.proper_ends)
        self.proper_max = float(state[2])
        self.vacuum_proper_end = float(self.proper_ends[1])
        # ADM data evaluated at the actual support endpoint, before exterior.
        Q, f, self.proper_support, _ = self.solutions[-2][2](self.outer)
        self.ADM_charge = float(Q)
        self.ADM_mass = float(self.outer*(1-f)/2+Q*Q/(2*self.outer))

    @staticmethod
    def poly(jet, center, radius):
        x = radius-center
        a, b, c, d = jet
        return a+x*(b+x*(c+x*d)), b+x*(2*c+3*x*d)

    def free(self, radius):
        if radius <= self.inner or radius >= self.outer:
            return 0j, 0j, 0j, 0., 0.
        i = min(np.searchsorted(self.edges, radius, side='right')-1, len(self.segments)-1)
        left, right, ca, cb, ja, jb = self.segments[i]
        length = right-left
        h, hp = step((radius-left)/length)
        a, ap = self.poly(ja, ca, radius)
        b, bp = self.poly(jb, cb, radius)
        value = a+h*(b-a)
        derivative = ap+h*(bp-ap)+(hp/length)*(b-a)
        s = self.parameter
        return (s*complex(value[0], value[1]), s*complex(derivative[0], derivative[1]),
                s*complex(value[2], value[3]), s*float(value[4]), s*float(derivative[4]))

    def constraint_rhs(self, r, y):
        Q, f, x, flat_V = y
        if f <= 0 or not np.isfinite(y).all():
            raise ArithmeticError('numeric constraint initialization lost positivity')
        phi, gradient, chi, ell, _ = self.free(r)
        source = scalar_mass_source(r, f, gradient, chi, ell)
        D = f+(r*ell)**2
        return [.6*r*r*(phi*chi.conjugate()).imag,
                (1-f)/r-Q*Q/r**3-2*source/r, 1/np.sqrt(D), 1-r*ell/np.sqrt(D)]

    def radial_at_proper(self, x):
        if not 0 <= x <= self.proper_max:
            raise ValueError('proper coordinate outside initialized interval')
        if x <= self.inner:
            return x, 0., 1.
        i = min(np.searchsorted(self.proper_ends, x, side='left'), len(self.solutions)-1)
        left, right, sol = self.solutions[i]
        r = brentq(lambda radius: sol(radius)[2]-x, left, right, xtol=3e-14, rtol=1e-14)
        Q, f = sol(r)[:2]
        return r, float(Q), float(f)

    @lru_cache(maxsize=65536)
    def flat_coordinate(self, x):
        if not 0 <= x <= self.vacuum_proper_end:
            raise ValueError('flat coordinate outside matter-free initial core')
        r, Q, f = self.radial_at_proper(x)
        if x <= self.inner:
            return x, 1., r, 1.
        i = min(np.searchsorted(self.proper_ends, x, side='left'), len(self.solutions)-1)
        value = float(self.solutions[i][2](r)[3])
        _, _, _, ell, _ = self.free(r)
        b = r*ell
        root = np.sqrt(1+b*b)
        return value, root-b, r, root+b

    def vacuum_state(self, t, x):
        """Analytic Minkowski core in the Cauchy gauge, numerically evaluated.

        Center continuation U(u)=V(u) for u>=0 makes the future regular axis
        x=0. Valid only before the first incoming matter ray v=x_vac.
        """
        if x <= 0 or t < 0 or t+x > self.vacuum_proper_end:
            raise ValueError('point outside proven flat-core domain')
        u, v = t-x, t+x
        V, Vprime, _, _ = self.flat_coordinate(v)
        U, Up, r0, other = self.flat_coordinate(abs(u))
        if u < 0:
            U, Up = U-2*r0, other
        radius = (V-U)/2
        if radius <= 0:
            raise ArithmeticError('flat core radius not positive')
        return np.array([radius, Vprime/2, 0., 0., -Up/2, 0., 0., 0., 0., 0., 0., 0.])

    def state_at_proper(self, x):
        r, Q, f = self.radial_at_proper(float(x))
        if r <= 0:
            raise ValueError('positive-radius characteristic state required')
        phi, gradient, chi, ell, _ = self.free(r)
        b = r*ell
        root = np.sqrt(f+b*b)
        plus = f/(root-b) if b < 0 else root+b
        nu = -plus/2
        kappa = 1/(2*plus)
        P = root*(chi-gradient)/2
        V = root*(chi+gradient)/2
        theta, z = r*V, r*P/nu
        # A_v=0 in the evolution gauge; radial and normal potentials vanish
        # initially. The electric field is encoded in the subsequent A_u flux.
        return np.array([r, kappa, theta.real, theta.imag, nu, z.real, z.imag,
                         r*(1-f)/2, phi.real, phi.imag, Q, 0.])

    def summary(self):
        return dict(canonical_input=self.path.name, canonical_sha256=self.digest,
                    parameter=self.parameter, inner_radius=float(self.inner),
                    original_certified_parameter_interval=[0., 1.],
                    outer_support_radius=float(self.outer),
                    outer_support_proper_distance=float(self.proper_support),
                    vacuum_proper_end=self.vacuum_proper_end,
                    radius_max=float(self.radius_max), proper_distance_max=self.proper_max,
                    ADM_mass=self.ADM_mass, ADM_charge=self.ADM_charge,
                    initialization_tolerance=self.tolerance,
                    initial_gauge='u=t-x, v=t+x; x initial proper distance; Omega^2=1; A_u=A_v=0',
                    initialization_error_certified=False)
