# C3 leading-order threshold: nonlinear endpoint-factored repair record

Date: 2026-09-26

## New certified record

Within the same leading-order C3 Fourier model,

- N = 50
- w = 0.051300 = 513/10000
- lambda = eM = 0.5064104188660820369212190741897402181...

Hence

    eM < 0.506411.

This improves the previous certified moving-manifold record

    0.5064726376107769558...

by approximately 6.22e-5.

## What changed methodologically

The previous branch varied w and orthogonally projected the old solution onto the nine exact linear constraints. That branch hit K(0)=0 near w≈0.05189328.

The present search instead works in endpoint-factored coordinates

    X(theta) = (1-cos theta)^2 P(cos theta),
    Y(theta) = sin(theta)(1-cos theta)^2 Q(cos theta),

so that

    C = w(1-cos theta)^4 R(cos theta).

At each fixed w, the three small front-end current minima are used to define a local tangent space. The scale direction and these active-current gradients are removed to first order. A normalized nonlinear trust-region/SLSQP repair is then performed in the remaining tangent space, with the weighted K(0) margin explicitly rescaled to its natural critical scale.

This produces a branch transverse to the old moving-projection branch and crosses its K(0)=0 barrier.

The successful certified continuation sequence included approximately

    w=0.051890  -> eM=0.506468330086800...
    w=0.051885  -> eM=0.506467432088708...
    w=0.051880  -> eM=0.506466665208088...
    w=0.051870  -> eM=0.506465284593967...
    w=0.051850  -> eM=0.506463254042536...
    w=0.051800  -> eM=0.506461319541459...
    w=0.051700  -> eM=0.506455416326314...
    w=0.051500  -> eM=0.506441840803620...
    w=0.051300  -> eM=0.506410418866082...

A local w scan around 0.051300 did not find a lower neighboring repaired point. Thus w≈0.05130 is the current local minimum along this nonlinear-repair branch, not a claim of a global optimum over all N=50 profiles.

## Exact / high-precision audit

For the saved rationalized candidate:

- E0 = 1.0000000000000031298172457664471...
- C0 = 0.20260246665093284893073849791836...
- lambda = eM = 0.50641041886608203692121907418974...
- EL = 4.80496113144584308746e-17
- CL = 4.74413743701262819122e-17
- weighted ratio EL/(2 CL) = 0.50641040602646573290...
- K(0) = 1.21825808769496305e-24 > 0
- all nine C3 / leading-order transverse linear equalities hold exactly after rationalization.

## Rigorous positivity certificate

- Current positivity: exact integer Bernstein/de Casteljau certificate on u in [-1,1].
- Certified R lower bound: approximately 5.0831339865e-11.
- K(x) on the compact region: 200-bit fixed-point interval Taylor certificate.
- Certified compact K lower bound: approximately 7.0725395263e-25.
- Analytic tail closure begins at x = 76.
- Primary replay: PASS.

## Interpretation

The old w≈0.05189328 obstruction was not the true C3 leading-order threshold; it was an obstruction of the one-dimensional moving-projection path. A nonlinear coefficient repair transverse to that path lowers the certified sufficient construction substantially further.

At the present record, current positivity is still not the active bottleneck: its certified lower bound is around 5e-11. The dominant active constraint is the weighted K(0) condition. Further progress should therefore target the local K(0)=0 manifold directly, preferably by a second-order KKT/Newton continuation or by jointly optimizing w and the transverse coefficient coordinates rather than scanning w externally.

## Scope

This is a rigorous certificate only within the same leading-order C3 admissible Fourier model. It is not by itself the finite-amplitude exact nonlinear C3 characteristic gluing theorem, and it is not a proof that 0.5064104188... is the sharp C3 threshold.

## Replay

From this directory run

    python replay.py

Do not use `python -O`; assertions are part of the verification path.

`build_certificate.py` reconstructs the rationalized input, audit, and certificate from `floating_candidate.json`.
