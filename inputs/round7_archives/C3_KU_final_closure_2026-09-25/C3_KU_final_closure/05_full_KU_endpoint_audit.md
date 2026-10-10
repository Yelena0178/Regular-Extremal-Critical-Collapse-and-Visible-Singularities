# Full endpoint sphere-data audit [C]

Reference: Kehle–Unger, arXiv:2211.15742v2, Definition 2.3 (pp.19–20), Definitions 2.4–2.6, Propositions 2.3–2.4, Definition 3.1 (p.21), and RN sphere data in §3.3. URL: https://arxiv.org/pdf/2211.15742 . Page numbers here are printed pages.

The exact list at index k=3 contains r with pure U,V derivatives through order FOUR; Ω²,Φ,Q through order three; and a=A_U with pure U derivatives through three and pure V derivatives through FOUR. The differential constraints link many of these entries. Mixed derivatives are fixed by the wave/Maxwell equations, rather than additional free entries of the sphere data list.

## 1. Gauge normalization is performed separately at each endpoint

Definition 3.1 requires gauge equivalence at each end. It does not require a single lapse-normalized gauge all along the cone.

At the Minkowski endpoint β>0, α=-1/(4β). Positive linear rescalings U=f(u),V=g(v) with f'=2β and g'=1/(2β) produce α_new=-1/2,β_new=1/2,Ω²_new=1. At the RN endpoint α<0 and β=0; choose f'=-1/(2α)>0, g'=1/f'. Then α_new=-1/2,β_new=0,Ω²_new=1. Positivity of α's negative sign is indispensable here.

The higher jets of f and g can set all pure lapse derivatives through order three to zero. This follows constructively by making the lapse constant on each of the two coordinate axes through the sphere: solve the two one-dimensional reparametrization equations, with the prescribed positive first derivatives. Only finite jets are required, and increasing smooth extensions exist. Independently choose χ(U) with χ'=-a on the incoming axis, setting a and its first three pure U derivatives to zero. This gauge preserves A_V=0. Covariant scalar zero jets remain zero under both transformations. Such normalizations do not assert that mixed lapse or mixed potential derivatives vanish.

## 2. Pure sphere-data entries after normalization

Let R_i=R(L)>0. The entries below are exhaustive for k=3. Category labels: A=ansatz, F=exact residual, C=constraint, G=gauge, I=initial Minkowski data.

|Quantity|Minkowski end|Extremal RN end M=Q=1|Reason|
|---|---|---|---|
|r|R_i|1|radius construction A|
|r_U|−1/2|−1/2|G after α<0|
|r_V|1/2|0|G; q(0)=0 at RN end|
|Ω²|1|1|A then G|
|pure ∂U^jΩ²,∂V^jΩ², 1≤j≤3|0|0|G|
|Q|0|1|I; exact e=1/J_L|
|pure ∂U^jQ,∂V^jQ, 1≤j≤3|0|0|C, Maxwell current derivatives|
|Φ|0|0|A|
|∂V^jΦ,1≤j≤3|0|0|A: integer number of periods and preserved endpoint constraints|
|∂U^jΦ,1≤j≤3|0|0|I; F and ordinary/covariant triangular identities|
|pure ∂U^jr,∂V^jr,2≤j≤4|0|0|C, Raychaudhuri differentiated at most twice|
|a,∂U^ja,1≤j≤3|0|0|G|
|a_V|0|−1/2|C, a_V=−Ω²Q/(2r²)|
|∂V^ja,2≤j≤4|0|0|C: all pure V jets of r,Q,Ω² needed here vanish|

For example r_UU=ℓα-r|DΦ|². Differentiating twice requires at most ∂U³Ω² and D³Φ, all of which have the requisite normalized endpoint values. Thus r_UUUU=0 is checked, not omitted. Maxwell differentiated twice similarly determines Q_UUU,Q_VVV. The scalar pure jets imply all source products vanish at both endpoints.

In particular a_V at the RN endpoint is NOT zero. The independent sphere-data prescription must always be read together with the constraint relations; setting every dependent potential derivative to zero would give false matching.

## 3. All mixed jets needed at this regularity

In the same normalized gauge, the following table gives every mixed jet through total order three, and the additional mixed r jets of total order four. Minkowski entries are all zero.

|Jet|Minkowski|eRN at r=Q=1,α=−1/2,β=0|
|---|---|---|
|Φ_UV,Φ_UUV,Φ_UVV|0|0|
|Q_UV,Q_UUV,Q_UVV|0|0|
|r_UV|0|0|
|r_UUV,r_UVV|0,0|1/4,0|
|r_UUUV,r_UUVV,r_UVVV|0,0,0|3/4,0,0|
|(Ω²)_UV|0|−1/2|
|(Ω²)_UUV,(Ω²)_UVV|0,0|−3/2,0|
|a_UV|0|−1/2|
|a_UUV,a_UVV|0,0|−3/4,1/4|

These are equal on the glued and RN sides because the same equations with the matched pure jets compute them. To verify the nonzero entries directly, use

    r_UV=(-1+Q²/r²)/(4r)-αβ/r,
    L_UV=Ω²/(2r²)+2αβ/r²-Ω²Q²/r⁴,
    a_V=-Ω²Q/(2r²),

and retain lapse derivatives before evaluating. For instance r_UUV=L_UV α=1/4 by the differentiated Raychaudhuri equation, and r_UUUV=L_UUV α=3/4. For a_UVV, differentiating a_V twice produces -(Ω²)_UV/2=1/4, a term that would be missed by setting Ω²=1 before differentiation.

The scalar wave equation and its first derivatives give all three mixed scalar jets as zero. Differentiating the Maxwell currents then gives all listed mixed Q jets as zero. The additional radial jets follow by a second derivative of the radial equation or differentiated Raychaudhuri; r_UUVV=r_UVVV=0 because β and its pure V derivatives vanish.

No fourth-order scalar residual is required by k=3 sphere data. The pure fourth radial derivative is already constrained by third scalar/lapse jets. No extra independent residual or correction parameter was found in this audit.

## 4. Construction as cone data, not just a terminal jet list

For each finite δ,L, the seed is smooth on [0,1], r>0, and satisfies the tangential constraints. Its V jet at the initial sphere is the Minkowski jet after the positive affine rescaling. KU Proposition 2.3 constructs the full continuous sphere-data path, including the pure lapse/potential jets not needed for the residual proof. The explicit transports in 01 are its first three scalar covariant jets, by uniqueness of these triangular transports. Therefore the terminal matching above proves Definition 3.1 at order three.
