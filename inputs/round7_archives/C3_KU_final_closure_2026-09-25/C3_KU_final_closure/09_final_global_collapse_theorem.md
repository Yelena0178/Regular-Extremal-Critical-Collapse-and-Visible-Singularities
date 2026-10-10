# Low-coupling formation of an extremal Reissner–Nordström black hole [C]

Within the spherically symmetric Einstein–Maxwell–massless charged scalar field system there exist a nonzero scalar coupling e and regular one-ended asymptotically flat Cauchy data on Σ≃R3 whose maximal future globally hyperbolic development has the following properties:

1. A regular center and at least classical C2 spacetime regularity.
2. The initial hypersurface contains no trapped surfaces and lies in the domain of outer communication.
3. The development contains no antitrapped surfaces.
4. Future null infinity is complete.
5. The black-hole region is nonempty and has an event horizon.
6. For all sufficiently late advanced times the domain of outer communication, including the event horizon, is exactly RN with |Q|=M.
7. |e|M<0.57.

The input characteristic gluing has order three in KU's sphere-data sense. It is a finite-amplitude, finite-length gluing, not a limiting weak solution.

## Proof

Keep the supplied rational N=50 profile. The exact endpoint and moment checks and the rational right inverse are in `jacobian_check.py`. The finite-pulse residual theorem 01, using the diagonal from 02, gives C1 convergence to a map with invertible six-real Jacobian. The contraction argument 03 therefore gives cδ→0 with the three complex exact transverse residuals zero. Independent current and K certificates and the correction stability check supply the hypotheses of the uniform admissibility proof 04. This yields r>0 and r_U<0 on each sufficiently small finite member.

The complete endpoint and mixed-jet verification 05 proves order-three characteristic gluing, including the dependent fourth radial and potential V jets. File 06 gives exact charge matching and the limiting coupling λ0<0.57, hence the strict finite-member inequality for sufficiently small δ. Apply the replacement proposition 07 and center bookkeeping 08. Their conclusions give all the global assertions above.

The δ smallness restrictions in these steps are finitely many positive thresholds for fixed constants and a fixed correction ball. Their minimum is positive. L=T ceil[Aδ^-1log(1/δ)/T] is finite for every chosen δ>0. Hence this is a genuine existential theorem about at least one finite member, even though this proof does not print a numerical δ* or the corrected coefficients of such a member.

## Scope

“Collapse model” here means the stated rigorous spherical EMCSF gravitational-collapse spacetime. It is not a stellar-fluid simulation, a stability theorem under generic perturbations, a sharp-threshold theorem, or an explicit computable finite-amplitude certificate. No claim is made that all couplings below 0.57 admit such gluing.
