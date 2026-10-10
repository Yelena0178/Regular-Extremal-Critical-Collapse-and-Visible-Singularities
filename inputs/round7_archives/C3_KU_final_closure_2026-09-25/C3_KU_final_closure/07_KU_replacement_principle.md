# KU replacement principle [C: conditional input implication]

## Proposition

For a nonzero scalar coupling, suppose an order-(k+1) EMCSF cone-data path joins a Minkowski sphere to RN horizon sphere data, with positive radius and strictly negative outgoing-cone transverse radius derivative throughout the compact gluing segment. Then the spacetime construction used in Kehle–Unger §5.2 applies with this path as its characteristic-gluing input. It yields the corresponding regular one-ended asymptotically flat collapse development, with the regularity guarantee reduced by one at the center. A large-coupling or large-mass assumption is not additionally required of the supplied path.

## Proof audit / exact locations

Use arXiv:2211.15742v2 (15 February 2024), https://arxiv.org/pdf/2211.15742 . The statement is an implication extracted from the proof, not a claim that the published mass-restricted Corollary 1 directly applies outside its hypotheses.

- Definition 3.1, printed p.21, specifies the required gauge-equivalent endpoint sphere data. File 05 checks this input.
- Proposition 3.1, pp.22–23, converts that cone gluing into a local spacetime gluing. It has no large-mass requirement on an independently supplied cone path.
- In §5.2, printed p.37, the proof of Corollary 1 starts by invoking Theorem 2B at index k+1 together with Proposition 3.1. The role of Theorem 2B at this point is to supply the cone path and sign. Replace exactly that invocation by the path proved here.
- The rest of the construction in §5.2, p.38, uses local characteristic evolution, the Minkowski region, an RN exterior, regular center extension, and the strict sign on a neighbourhood of the compact gluing segment. It contains no further estimate involving the large parameter used to prove Theorem 2B.
- The Cauchy hypersurface is chosen in the domain of outer communication, with an RN asymptotic end. Completeness of future null infinity is inherited from the exact RN exterior. Uniqueness embeds the constructed domain into its maximal development. Raychaudhuri propagates the absence of antitrapped symmetry spheres; Appendix B, Proposition B.2 supplies the statement for general closed surfaces.

The initial Minkowski radius of the present cone may be very small. It is nevertheless strictly positive for each finite δ,L. The local neighbourhoods and chosen Cauchy slice may depend on this radius; the replacement argument needs no uniform lower radius bound along the limiting sequence. In the picture in §5.2 replace the particular displayed Minkowski wedge by a wedge through this actual positive-radius sphere. The same local and center extension steps apply.

This establishes the conditional replacement proposition. Its hypotheses are supplied by 01–06 for k=2; the regularity issue is separated in 08. This argument does not reproduce the different Schwarzschild-to-extremal construction in §5.3, nor assert that the present model contains an earlier Schwarzschild apparent horizon.
