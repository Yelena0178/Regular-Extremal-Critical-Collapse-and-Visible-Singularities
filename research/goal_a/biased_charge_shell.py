"""Exact-integral-normalized charge location, independent of propagation direction.

The mathematical normalization is a ratio of smooth positive integrals.
quad approximates that ratio here; its estimated error is not a certificate.
The original direction-family implementation is preserved for reproducibility.
"""
import numpy as np
from scipy.integrate import quad
from charge_preserving_shell import ChargePreservingShell


class BiasedChargeShell(ChargePreservingShell):
    def __init__(self, parameters, bias=0., **kwargs):
        if not np.isfinite(bias) or abs(bias) > 2:
            raise ValueError('this implementation restricts charge bias to [-2,2]')
        self.bias = float(bias)
        R, W = parameters.radius, parameters.width

        def integrand(z, beta):
            if abs(z) >= 1:
                return 0.
            return (R+W*z)**2*np.exp(-2*z*z/(1-z*z)-beta*z)

        base, base_error = quad(integrand, -1., 1., args=(0.,),
                                epsabs=2e-12, epsrel=2e-13, limit=200)
        tilted, tilted_error = quad(integrand, -1., 1., args=(self.bias,),
                                    epsabs=2e-12, epsrel=2e-13, limit=200)
        self.normalization = base/tilted
        self.quadrature_diagnostics = dict(base_integral=base, tilted_integral=tilted,
                                           base_error_estimate=base_error,
                                           tilted_error_estimate=tilted_error,
                                           errors_certified=False)
        super().__init__(parameters, **kwargs)

    def frequency_and_phase(self, r):
        p = self.parameters
        z = (r-p.radius)/p.width
        omega = p.frequency*self.normalization*np.exp(-self.bias*z)
        integrated = z if self.bias == 0 else -np.expm1(-self.bias*z)/self.bias
        phase = p.direction*p.frequency*self.normalization*p.width*integrated
        return omega, phase

    def free(self, r):
        a, ap = self.envelope(r)
        if a == 0 and ap == 0:
            return 0j, 0j, 0j
        omega, theta = self.frequency_and_phase(r)
        d = self.parameters.direction
        phase = np.exp(1j*theta)
        return (phase*a, phase*(ap+1j*d*omega*a),
                phase*(-d*(ap+a/r)-1j*omega*a))

    def constraint_rhs(self, r, y):
        Q, f, _ = y
        if f <= 0 or not np.isfinite(y).all():
            raise ArithmeticError('constraint solve lost f>0')
        a, ap = self.envelope(r)
        omega, _ = self.frequency_and_phase(r)
        d = self.parameters.direction
        S = ap*ap+d*d*(ap+a/r)**2+(1+d*d)*omega*omega*a*a
        return [.6*omega*r*r*a*a, (1-f)/r-Q*Q/r**3-r*f*S, 1/np.sqrt(f)]

    def summary(self):
        result = super().summary()
        result.update(charge_bias=self.bias, normalization=self.normalization,
                      quadrature=self.quadrature_diagnostics,
                      mathematical_normalization='C_beta=integral(r^2*a^2)/integral(r^2*a^2*exp(-beta*z))',
                      charge_fraction_inside_R=float(self.sol.sol(self.parameters.radius)[0]/self.ADM_charge)
                          if self.ADM_charge != 0 else None,
                      analytic_initial_certificate_scope='A=2/5, omega=3/20, R=10, W=4, |d|<=1, |beta|<=2; exact integral normalization',
                      floating_evaluator_error_certified=False)
        return result
