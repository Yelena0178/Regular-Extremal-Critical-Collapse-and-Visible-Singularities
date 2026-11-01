"""Independent envelope and phase directions in the existing charged shell.

Exact initial-family argument: CORE_CANDIDATE_REVIEW_2026-11-01.md.
The evaluator uses floating ODEs; no future or initialization error certificate.
"""
import numpy as np
from charge_preserving_shell import ChargePreservingShell


class SplitDirectionShell(ChargePreservingShell):
    def __init__(self, parameters, phase_direction, **kwargs):
        if not np.isfinite(phase_direction) or not -1 <= phase_direction <= 1:
            raise ValueError('phase direction must lie in [-1, 1]')
        self.phase_direction = float(phase_direction)
        super().__init__(parameters, **kwargs)

    def free(self, r):
        a, ap = self.envelope(r)
        if a == 0 and ap == 0:
            return 0j, 0j, 0j
        p = self.parameters
        dq = self.phase_direction
        phase = np.exp(1j*dq*p.frequency*(r-p.radius))
        return (phase*a, phase*(ap+1j*dq*p.frequency*a),
                phase*(-p.direction*(ap+a/r)-1j*p.frequency*a))

    def constraint_rhs(self, r, y):
        Q, f, _ = y
        if f <= 0 or not np.isfinite(y).all():
            raise ArithmeticError('constraint solve lost f>0')
        a, ap = self.envelope(r)
        p = self.parameters
        S = (ap*ap+p.direction**2*(ap+a/r)**2
             +(1+self.phase_direction**2)*p.frequency**2*a*a)
        return [.6*p.frequency*r*r*a*a,
                (1-f)/r-Q*Q/r**3-r*f*S, 1/np.sqrt(f)]

    def summary(self):
        result = super().summary()
        result.update(envelope_direction=self.parameters.direction,
                      phase_direction=self.phase_direction,
                      analytic_initial_scope='A=2/5, omega=3/20, R=10, W=4; both directions in [-1,1]; no radial bias',
                      analytic_initial_claim='SPLIT01.1; see CORE_CANDIDATE_REVIEW_2026-11-01.md',
                      floating_evaluator_error_certified=False)
        return result
