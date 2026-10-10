# Remaining work and status boundaries

## Main analytic existence theorem

[C] The proof chain A–I is supplied in files 01–09. This includes an explicit C1 majorant for every scalar integrand, parameter derivatives, finite-end boundary effects, exact zero stability, uniform admissibility, full sphere-data matching, coupling dependence, the KU proof replacement, and regularity bookkeeping.

[C] Rational profile constraints, right inverse, Jacobian nondegeneracy, current factor positivity, K positivity, and stability on a fixed correction cube are checked by executable scripts included in this package. These checks were reconstructed from the original profile, not from a new optimized profile.

There is no unresolved analytic assumption imported from the positivity summary: the underlying profile positivity is now independently rechecked. The use of the published KU local/global existence construction is explicitly identified; this project does not reprove that general PDE theorem.

## Second-stage explicit finite member

[O] A concrete δ*, L*, corrected coefficient enclosure, and interval-Newton/Krawczyk certificate for the EXACT finite residual have NOT been produced.

The current rigorous interval calculations concern the leading profile and the correction neighbourhood. They do not certify a numerical finite-amplitude root. The analytic root is obtained from qualitative C1 convergence; the proof does not provide a computable printed cutoff δ0. Claiming that an arbitrary small decimal δ lies below that cutoff would be unjustified.

A direct numerical trial was not substituted for a certificate. With the deliberately tiny correction cube and conservative averaged-energy lower bound, brute-force integration over the chosen diagonal length is not an appropriate certified algorithm. An explicit member will require quantitative bounds for the residual at zero and the derivative variation, plus a periodic-block or analytic-tail enclosure of the long interval. Then one can choose δ* and certify the root by interval Newton. The existing majorant table is an input to that task, not its completion.

[P] Practical numerical implementation plan: integrate a weighted triangular jet system on a compact x interval; represent the remaining periodic radius/charge evolution by rigorously enclosed period maps; enclose the scalar tail analytically; propagate interval sensitivities in the six correction directions; certify a root and its coupling/admissibility margins. No claimed result depends on this unimplemented plan.

## Claims specifically not made

- No new lower threshold or profile optimization.
- No generic stability of extremal collapse.
- No stellar matter simulation.
- No global C3 regularity guarantee from order-three gluing alone.
- No claim that the cited center construction necessarily loses a derivative for every solution.
- No claim that all |e|M<0.57 are attainable.
- No finite numerical witness disguised as an exact certificate.
