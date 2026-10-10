# C3 → KU final analytic closure — 2026-09-25

## Result

[C] An analytic existence proof is supplied for exact finite-amplitude order-three characteristic gluing using the original rational N=50 profile, with |e|M<0.57, r>0 and r_U<0. Applying the audited KU replacement argument gives a regular one-ended asymptotically flat classical C2 collapse spacetime with late exact extremal RN exterior and event horizon.

[O] No explicit numerical finite-amplitude member has yet received an interval-Newton/Krawczyk certificate. The analytic existence result and this separate computational task must not be conflated.

|Task|Status|Evidence|
|---|---|---|
|A: uniform finite-amplitude C1 residual|[C]|01: exact grouped integral formulas; complete termwise C1 weight table|
|B: finite-L tails|[C]|02: geometric exp(-2ηδL), moving-end boundary, rounded diagonal|
|C: exact zero|[C]|03: contraction proof from C1 stability; cδ→0|
|D: admissibility|[C]|04 and independent exact/interval profile and correction certificates|
|E: all endpoint data|[C]|05: pure and mixed jets, including r order four and potential V order four|
|F: e and charge|[C]|06: e=1/J_L, C1 dependence and exact Q(1)=1|
|G: KU replacement|[C]|07: proof-level hypothesis audit of Definition 3.1, Proposition 3.1 and §5.2|
|H: center regularity|[C]|08: guaranteed C2; no unjustified necessity assertion|
|I: global theorem|[C]|09 and FINAL_PROOF.md|
|Explicit δ*,L*, interval finite root|[O]|10: not supplied; not needed for the existential theorem|

## New work beyond the previous handoff

1. Retained the finite-amplitude boundary products in second and third scalar integral identities.
2. Used exact Raychaudhuri constraints for r_UU,r_UUU to shorten, rather than omit, the hierarchy.
3. Gave a C1 Banach-algebra envelope table with h=e^(x/1000), maximum propagated exponent h^16, and integrable envelope Ce^(-0.98x).
4. Proved normalization convergence in C1 over the growing interval by a periodic-primitive identity.
5. Independently rebuilt the rational moment right inverse and positivity checks. The original coefficients were copied unchanged.
6. Supplied an explicitly certified, conservative correction cube ||c||∞≤10^-200 with K≥5×10^-9 and positive factored current.
7. Recomputed the compact H coefficient directly, including the constant term in the integrated radius expansion.
8. Checked the nonzero mixed RN lapse/potential jets and the dependent fourth-order radial data.

[C] denotes a proof supplied in this package, with its stated scope; it is not a claim of journal peer review. [P] means a strategy, [N] numerical evidence, and [O] uncompleted work. The runnable certificates are not a machine formalization of the analytic PDE proof.

## Read order

Read 01 first, then 02–09. FINAL_PROOF combines these in order. AUDIT_CERTIFICATE records the executable checks and their limits. Reproduce with `python proof_checks/run_checks.py` using standard-library Python 3 only.
