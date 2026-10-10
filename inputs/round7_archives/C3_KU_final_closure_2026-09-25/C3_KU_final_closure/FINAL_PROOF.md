# Complete analytic proof — C3 low-coupling collapse

This is the combined version of files 01–09. The separate explicit finite-member computer-assisted certificate remains open; see 10_remaining_gaps.md.

# Uniform finite-amplitude C1 residual theorem [C]

Date: 2026-09-25. This is an analytic existence argument; it does not specify a numerical finite amplitude. The exact rational profile is `data/profile.json`. Correction directions are reproducible by `proof_checks/jacobian_check.py`. No optimization is used.

## 1. Conventions and statement

Use ds²=-Ω² dU dV+r²dω², D=D_U=∂U+iea, a=A_U, A_V=0, ℓ=(log Ω²)_U. On the cone Ω²=1. Differentiation in U is performed BEFORE restriction to the cone. The coupling e is constant in spacetime, though it varies with the construction parameters. Put

    z=z_c=z_0+Σ c_j h_j, E=|z_x|², C=Im(conj(z)z_x),
    λ(c)=2 Ebar/Cbar, T=2π/w, w=149/1250,
    q'=q²-q+δE, q(0)=0, R=exp(-∫_0^x q),
    L=T ceil(A δ^(-1)log(1/δ)/T), ε=e^(-L), a0=1-ε,
    t=ε+a0 V=e^(-x), Φ=√δ z(x), r=R(x),
    J_L=δ∫_0^L C R² dx, e=1/J_L,
    Q(x)=e δ∫_x^L C R² dy.

The symbol a0 is the affine coordinate factor, and is NOT the potential a.

There is a fixed parameter ball about zero, and positive δ0,A, for which

    δ^(-1/2)(DΦ,D²Φ,D³Φ)(V=1) → T_{λ(c)}(M1,M2,M3)

uniformly with one c derivative. Mi=∫_0^∞e^(-ix)z_c(x)dx. In particular, this theorem concerns the EXACT finite pulse and its Minkowski initial transverse data. The limiting geometry is not used in place of a finite solution.

For this result it suffices that Ebar,Cbar stay strictly positive and the family is bounded in the finitely many smooth profile norms. Current positivity and K positivity are not needed to prove residual convergence. They are imposed later for admissibility.

## 2. Exact scalar formulas, including product boundary terms

Write α=r_U, β=r_V, r2=r_UU, r3=r_UUU, Ψ_j=D^jΦ,

    K=ie Ω² Q/r, b=ie a_V=-ie Ω² Q/(2r²),
    W1=D(Φ_V)=∂V Ψ1-bΦ,
    W2=D²(Φ_V)=∂V Ψ2-2bΨ1-b_UΦ.

Commutators are [D,∂V]=-b and [∂V,D]=b. All three incoming scalar transverse jets vanish at V=0. The following exact identities hold:

    r Ψ1(V)=∫_0^V [-α Φ_V-KΦ/4] dv.                     (S1)

    r Ψ2(V)=∫_0^V [-r2 Φ_V-α W1
                  -(K_U Φ+KΨ1)/4+rbΨ1] dv -αΨ1(V).     (S2)

    r Ψ3(V)=∫_0^V [-r3 Φ_V-2r2 W1-α W2
                  -(K_UU Φ+2K_U Ψ1+KΨ2)/4
                  +2rbΨ2+(2αb+rb_U)Ψ1] dv
                  -2αΨ2(V)-r2Ψ1(V).                    (S3)

Derivation: S1 is the charged wave equation. Applying D to S1 in differential form gives

    ∂V(rΨ2+αΨ1)=-r2Φ_V-αW1-(K_UΦ+KΨ1)/4+rbΨ1.

A second differentiation, retaining [D,∂V], gives S3. Boundary products at V=0 vanish because Ψ1=Ψ2=0 there. These grouped identities are equivalent to the expanded third-order transport, but require neither r_UUV nor b_UU as separate estimates. S2's boundary product was absent from the old summary of the integrand; it must not be discarded at finite δ.

## 3. Exact geometric hierarchy

The following equations determine all coefficients in S1–S3. The constraints provide simpler exact formulas for r2 and r3 than an additional radial Volterra integral:

    ∂V(rα)=(-1+Q²/r²)/4,
    α(L)=-ε/[4a0 q(L)R(L)], β=a0 qR/t,
    Q1:=Q_U=-e r² Im(Φ conj(Ψ1)),
    a_V=-Q/(2r²),
    ℓ_V=1/(2r²)+2αβ/r²-Q²/r⁴-2 Re(Ψ1 conj(Φ_V)),
    r2=ℓα-r|Ψ1|²,
    Q2:=Q_UU=-e[2rα Im(Φ conj(Ψ1))+r² Im(Φ conj(Ψ2))],
    (a_U)_V=-1/2[Q1/r²+Qℓ/r²-2Qα/r³],
    (ℓ2)_V=ℓ/(2r²)-α/r³+(2r2β+2αα_V)/r²-4α²β/r³
             -(Q²ℓ+2QQ1)/r⁴+4Q²α/r⁵
             -2 Re(Ψ2 conj(Φ_V)+Ψ1 conj(W1)),
    ℓ2=L_UU,
    r3=ℓ2α+ℓr2-α|Ψ1|²-2r Re(Ψ2 conj(Ψ1)).

Initial values a=ℓ=a_U=ℓ2=0 are exact Minkowski values. r2=r3=0 initially follow from the constraints. Also

    α_V=(-1+Q²/r²)/(4r)-αβ/r,
    H1=Q/r, H1_U=Q1/r-Qα/r²,
    H1_UU=Q2/r-2Q1α/r²-Qr2/r²+2Qα²/r³,
    K_U=ie(ℓH1+H1_U),
    K_UU=ie[(ℓ²+ℓ2)H1+2ℓH1_U+H1_UU],
    b_U=-ie/2[ℓ Q/r²+Q1/r²-2Qα/r³].

If desired the expanded third-order formula also uses

    b_UU=-ie/2[(ℓ²+ℓ2)Q/r²
             +2ℓ(Q1/r²-2Qα/r³)
             +Q2/r²-4Q1α/r³-2Qr2/r³+6Qα²/r⁴].

No equation above introduces an uncontrolled jet. The occurrence of r2 inside ℓ2 comes after r2 has been determined, and r3 is determined after ℓ2 and Ψ2.

## 4. Tangential bounds and parameter differentiability

Fix a closed small parameter ball. Set E*=sup E and choose C0=2E*. If δ<1/(4E*), comparison at 0 and C0δ gives 0≤q≤C0δ. If p'+p=E, p(0)=0, then (q-δp)'+(q-δp)=q². Thus q≥δp. With Ebar≥E_*>0,

    q≥ηδ for x≥T, η=e^(-T)T E_*.

For a parameter derivative denoted by a dot,

    dot q'=(2q-1)dot q+δ dot E, dot q(0)=0.

After shrinking δ0 so 2q-1≤-1/2, |dot q|≤2δ sup|dot E| and |dot R/R|≤Cδx. Consequently all solutions and their first c derivatives exist for every x≥0. In particular each finite truncation has positive radius.

Here is a C1 averaging proof for the coupling, not just an appeal to smooth ODE dependence over an expanding interval. Put f=C-(Cbar/Ebar)E and let P be a bounded periodic primitive of f. Integration by parts with (R²)'=-2qR² gives

    δ∫_0^∞ fR² = -δP(0)+2δ∫_0^∞ PqR² = O_C1(δ).

For the differentiated integral, dot q=O(δ), dot R/R=O(δx), R²≤C exp(-2ηδx) imply its magnitude is O(δ): the worst integral is δ³∫x exp(-2ηδx)dx=O(δ). There is no hidden factor δ^-1 left over.

An exact identity is

    δ∫_0^∞ ER² = 1/2+∫_0^∞ q²R² = 1/2+O_C1(δ).

It follows that J∞=1/λ+O_C1(δ). The finite tail is O_C1((1+δL)e^(-2ηδL)); hence e→λ in C1. J_L is bounded away from zero.

At a fixed bounded x, the exact representation Q(x)=1-eδ∫_0^x CR² shows Q→1 and dot Q→0 uniformly in c. Globally Q and dot Q are bounded: differentiate the unnormalized integral and use δ∫(1+δy)e^(-2ηδy)dy≤C. This argument does not assume a sign of C. At fixed x, R→1, dot R→0 and β→0 with its c derivative.

## 5. A single explicit majorant calculus

For functions depending on c use the norm

    |f(x)|_1=sup_c |f(x,c)|+Σ_j sup_c |∂_{c_j}f(x,c)|.

It is a Banach algebra norm: |fg|_1≤|f|_1|g|_1. All estimates in this section therefore ALREADY include one parameter derivative. Fix s=1/1000 and h(x)=exp(sx). By shrinking δ0, the previous estimates imply

    |R|_1+|R^-1|_1≤C h,
    |Q|_1+|e|_1+|z|_1+|z_x|_1≤C,
    |β|_1≤C t^-1 h.

For R^-1, choose C0δ0≤s/2 and absorb (1+Cδx) into the remaining exp(sx/2). This explains explicitly the polynomial factors generated by parameter differentiation. All inverse-radius powers below are controlled by products of this bound.

In x variables |dv|=t dx/a0. A Volterra integral from 0 to V becomes an integral from x to L. For k>ms,

    ∫_x^L t(y)^k h(y)^m dy ≤ t(x)^k h(x)^m/(k-ms).   (W)

The only nonzero incoming radial boundary constant is

    R(L)α(L)=-ε/[4a0 q(L)],
    |R(L)α(L)|_1≤C ε/δ.

On the chosen diagonal δ^-1≤exp(sL) for small δ, so ε/δ≤t(x)h(x) for every 0≤x≤L. The same bound holds for its c derivative since dot q/q is bounded. This controls the early endpoint without falsely replacing its scale by exp(-σL).

The following exponents are deliberately generous. Define ψj=Ψj/√δ and wj=Wj/√δ. Each row is valid in |.|_1.

|Quantity|Bound|Derivation|
|---|---|---|
|α|C t h³|radial integral: t(1+Q²/r²), plus boundary, then r^-1|
|ψ1|C t h⁴|S1: α z_x and tKz, then r^-1|
|∂Vψ1, w1|C h⁶|differentiate S1, subtract bz; βψ1/r is the largest term|
|Q1|C δ t h⁶|Maxwell formula|
|a|C t h²|a_V integral|
|ℓ|C t h⁶|largest geometric term tαβ/r²; scalar term δψ1 z_x|
|α_V|C h⁵|radial wave equation|
|r2|C t² h⁹|ℓα-rδ|ψ1|²|
|K_U|C t h⁷|explicit quotient derivatives|
|ψ2|C t² h¹⁰|S2 including -αψ1|
|∂Vψ2, w2|C t h¹²|differentiate S2; βψ2/r is the largest term|
|Q2|C δ t² h¹²|second Maxwell formula|
|a_U|C t² h⁸|three terms in its exact transport|
|ℓ2|C t² h¹²|term-by-term list below|
|r3|C t³ h¹⁵|four terms in the Raychaudhuri derivative|
|K_UU|C t² h¹³|explicit quotient formula|
|b, b_U, b_UU|C h², C t h⁸, C t² h¹⁴|explicit quotient formulas|
|ψ3|C t³ h¹⁶|S3 including both boundary products|

### Every scalar integrand

The next table includes the factor t/a0 converting dv to dx and division by √δ. It lists each separate term, so no high-order term is concealed in an induction assertion.

|Formula|Term|Bound in x measure|
|---|---|---|
|S1|αΦ_V|C t h³|
|S1|KΦ/4|C t h|
|S2|r2Φ_V|C t² h⁹|
|S2|αW1|C t² h⁹|
|S2|K_UΦ/4|C t² h⁷|
|S2|KΨ1/4|C t² h⁵|
|S2|rbΨ1|C t² h⁷|
|S3|r3Φ_V|C t³ h¹⁵|
|S3|2r2W1|C t³ h¹⁵|
|S3|αW2|C t³ h¹⁵|
|S3|K_UUΦ/4|C t³ h¹³|
|S3|K_UΨ1/2|C t³ h¹¹|
|S3|KΨ2/4|C t³ h¹¹|
|S3|2rbΨ2|C t³ h¹³|
|S3|2αbΨ1|C t³ h⁹|
|S3|rb_UΨ1|C t³ h¹³|

The unintegrated boundary products obey |αψ1|_1≤Ct²h⁷, |2αψ2|_1+|r2ψ1|_1≤Ct³h¹³. Their division by r accounts for the final extra h, not an extra loss of t.

### Every second-lapse integrand

The individual terms in t(ℓ2)_V have bounds, in the order written in Section 3:

    tℓ/(2r²): Ct²h⁸;
    tα/r³: Ct²h⁶;
    2tr2β/r²: Ct²h¹²;
    2tαα_V/r²: Ct²h¹⁰;
    4tα²β/r³: Ct²h¹⁰;
    tQ²ℓ/r⁴ and 2tQQ1/r⁴: Ct²h¹⁰;
    4tQ²α/r⁵: Ct²h⁸;
    2tδψ2 conj(z_V): Cδt²h¹⁰;
    2tδψ1 conj(w1): Cδt²h¹⁰.

The three terms of t(a_U)_V are bounded by Ct²h⁸. The four terms defining r3 are bounded by Ct³h¹⁵, Ct³h¹⁵, Cδt³h¹¹, Cδt³h¹⁵ respectively. Thus the only explicit inverse radius in the original lapse transport reaches r^-5; repeated products/divisions are already covered by the table's exponent h¹⁶.

For ∂Vψ2, differentiation of S2 gives, exactly,

    r∂Vψ2=-βψ2-r2 z_V-αw1-(K_Uz+Kψ1)/4
           +rbψ1-α_Vψ1-α∂Vψ1.

This proves the claimed bound for w2 without estimating a derivative of an uncontrolled function. Parameter derivatives obey this same algebraic estimate, including the terms involving ∂c e, ∂c b and ∂c K.

In particular EVERY scalar/geometric integration kernel in this proof is bounded in C1 by C exp(-0.98x), or by a faster exponential. This is of the requested form C(1+x)^N exp(-ax), with N=0,a=0.98, after absorbing polynomial factors. The constants do not depend on δ,L,c. Setting the integrands to zero for x>L gives domination on the common half-line.

## 6. Uniform dominated convergence, one layer at a time

All statements below include first parameter derivatives and are uniform on the fixed ball. Uniform convergence on a compact x interval plus the common exponential tail proves convergence in L1_x: split the integral at a fixed X, use uniform convergence on [0,X], and then let X→∞. This is the parameter-uniform form of dominated convergence actually used here.

1. R,R^-1→1 and Q→1 on compact x intervals by Section 4. Their parameter derivatives tend to zero.
2. In the radial integral, 1-Q²/r²→0, and the boundary constant→0. Therefore α→0.
3. Apply S1: ψ1→ψ1⁰, where ∂tψ1⁰=-iλ z/4 and ψ1⁰(0)=0. The term α z_x vanishes in L1. Also ∂Vψ1 and w1 converge by their explicit expressions.
4. Q1→0 because it has a factor δ. Integrating a_V and ℓ_V gives a→-t/2 and ℓ→-t/2. The scalar product in ℓ_V tends to zero with its derivative, since it has a factor δ.
5. The exact constraint r2=ℓα-δr|ψ1|² gives r2→0.
6. Apply S2. Its boundary product vanishes locally, and every integral kernel has the table's majorant. The result is ∂tψ2⁰=(iλ/8)t z-(3iλ/4)ψ1⁰, ψ2⁰(0)=0. ∂Vψ2 and w2 converge by the displayed algebraic formula.
7. Q2→0 by its explicit factor δ.
8. In (a_U)_V only -Qℓ/(2r²) survives. In (ℓ2)_V only ℓ/(2r²)-Q²ℓ/r⁴ survives. Both tend to t/4, so a_U,ℓ2→t²/8.
9. The four-term formula for r3 gives r3→0.
10. The quotient formulas give K_U→-iλt/2, K_UU→3iλt²/8, b→-iλ/2, b_U→iλt/4. Apply S3, whose two boundary products again vanish. Thus

    ∂tψ3⁰=-(3iλ/32)t²z+(iλ/2)tψ1⁰-(5iλ/4)ψ2⁰,
    ψ3⁰(0)=0.

The lower boundary in t moves to zero. The envelope estimates prove that no boundary layer leaves a finite scalar jet behind. This addresses the finite-L issue for each layer rather than assuming an infinite cone at the outset.

The limiting datum z(−log t) need not extend continuously to t=0. The limiting scalar recursions are bounded-data improper Volterra integrals, justified by the majorants above; no smooth limiting scalar field at t=0 is assumed.

## 7. Limiting matrix

Integrating these elementary recursions yields

    Tλ = [[-iλ/4, 0, 0],
          [-3λ²/16, λ(3λ+2i)/16, 0],
          [iλ²(15λ-8i)/128, -5iλ²(3λ+2i)/64,
           iλ(3λ+2i)(5λ+6i)/128]].

The convergence is C1 in c, not merely at c=0. All diagonal entries are nonzero for real λ≠0. At zero, differentiation of λ contributes (∂λT)M=0 because M(0)=0. This completes Task A.

## Audit scope

The proof is original algebra/estimation starting from the EMCSF equations, with conventions cross-checked against Lee, arXiv:2609.22518v1, §2.2 and Appendix A. It does not infer exact nonlinear cancellation from the leading moments. That cancellation is obtained only by the zero-stability argument in file 03.


---

# Finite-L tail and diagonal [C]

Use the constants C0,η>0 fixed on the correction ball in file 01. L is independent of c. Dot denotes one correction derivative. It is not a δ derivative.

1. Scalar moments satisfy |∫_L^∞e^(-sx)z_c dx|_C1≤C e^(-sL), s=1,2,3. For a polynomial weight x^n the bound is C(1+L)^n e^(-sL).
2. R(y)≤R(L)e^(-ηδ(y-L)) for y≥L≥T. Therefore

       T_L=δ∫_L^∞CR²,
       |T_L|≤C R(L)²,
       |dot T_L|≤C(1+δL)R(L)²,
       ||T_L||_C1≤C(1+δL)e^(-2ηδL).

   The last estimate follows by inserting |dot C|≤C and |dot R/R|≤Cδy. The moment of y in an exponential integral costs δ^-2, multiplied by δ² in the integrand. This leaves only 1+δL. The estimate also controls J_L-J∞ and hence their reciprocals when J is bounded away from zero.
3. The exact incoming Minkowski value is α(L)=-e^(-L)/[4(1-e^(-L))q(L)R(L)]. Since q(L)≥ηδ and R^-1≤exp(C0δL),

       ||α(L)||_C1≤C(1+δL)δ^-1 exp(-L+C0δL).

   Differentiating produces -dot q/q-dot R/R; the first is bounded and the second is O(δL). No derivative of L occurs.
4. Fix, for example, A=2/η and

       L=T ceil[A δ^-1 log(1/δ)/T].

   Then δL=A log(1/δ)+O(δ), and the geometric tail is O((1+|logδ|)δ^(2ηA))=O((1+|logδ|)δ^4)=o(δ). More generally A>1/(2η) is sufficient for this o(δ) requirement; A>0 is enough merely to make this geometric tail tend to zero. If a weakened exponent σ is used, require A>1/σ for o(δ).

   The incoming boundary term and any fixed negative power of δ times exp(-L+C0δL) are smaller than every power of δ. The same remains true after a first c derivative.

5. A claim valid for any L above a lower bound must not substitute an upper bound for 1+δL. The exact ceiling choice above gives both bounds. Alternatively monotonicity of (1+δL)e^(-σδL) for large δL justifies an upper bound on the whole allowed range.

The proof in 01 controls all further boundary products explicitly by the common envelope. This lemma does not claim every propagated error has a universal exp(-σL) scale, nor does it need an O(δ) residual rate.


---

# Exact finite-amplitude zero [C]

Let Gδ(c) be the realification of the exact residual divided by √δ. File 01 proves Gδ→G0 in C1 on a fixed ball, where G0=Realify(Tλ(c)M(c)). The rational check verifies M(0)=0 and D_c Realify(M)=I6. Set A=D G0(0)=Realify(Tλ0). Its determinant is |d1 d2 d3|²>0.

Choose a closed Euclidean ball B_r contained in the certified correction cube, small enough that sup_Br ||I-A^-1 DG0||≤1/4. For sufficiently small δ, uniform C1 convergence gives sup_Br ||I-A^-1 DGδ||≤1/2 and |A^-1Gδ(0)|≤r/2.

The map Pδ(c)=c-A^-1Gδ(c) maps B_r into itself and has Lipschitz constant ≤1/2. Banach's fixed-point theorem gives a unique cδ in B_r with Gδ(cδ)=0. Moreover

    |cδ|≤2|A^-1Gδ(0)|→0.

Thus the unscaled residual vanishes EXACTLY:

    (D_UΦ,D_U²Φ,D_U³Φ)(1;δ,L(δ),cδ)=0.

This conclusion holds for every sufficiently small δ along the specified length choice. L may jump by periods as δ varies; a differentiable dependence on δ is unnecessary. No O(δ) claim for cδ is made. The cube chosen for the certificate is intentionally extremely small; this changes the unspecified smallness threshold for δ, not the logic of existence.

The result is an analytic existential root. It is not an interval-Newton certificate of an explicitly selected numerical δ.


---

# Uniform admissibility, including independent positivity verification [C]

## 1. What was actually recomputed

The inherited archive contained a positivity summary, but not the full executable certificates behind that summary. This run therefore reconstructed certificates from the supplied rational N=50 coefficients, without changing the profile.

`current_check.py` uses exact Fraction polynomial arithmetic. With y=cosθ,

    X=Σa_j(T_j(y)-1), B=Σb_j U_{j-1}(y), Y=sinθ B(y),
    Cθ=X[yB-(1-y²)B']+(1-y²)BX'.

It exactly divides Cθ by (1-y)^4 and proves the degree-95 quotient ≥1/100 on [-1,1] by rational Bernstein subdivision (7 leaves, maximum depth 5). Thus the x-current is w times this nonnegative factored expression. No sampled positivity test is used.

`interval_checks.py` reconstructs the exact cosine coefficients E_j,C_j of E(x),C(x). Define ν_j=jw and

    D=E0+Σ_{j≥1}E_j/(1+ν_j²),
    S_j=2(λC_j-E_j)/(ν_j(1+ν_j²)),
    T_j=2λC_j/(1+ν_j²),
    K(x)=2E0(x+2)-D e^(-x)+Σ[S_j sinν_jx+T_j cosν_jx].   (K)

On [0,20] it encloses a Taylor polynomial of degree 20 on each half-unit interval, converts that polynomial to Bernstein form, and subtracts a rigorous order-21 derivative remainder. Every arithmetic operation uses directed Decimal rounding at precision 100. Sine, cosine and the exponential are themselves enclosed by Taylor remainders; no floating-point transcendental evaluation is trusted. Forty covered intervals suffice. The smallest enclosed lower bound exceeds 1.09517133513e-7.

On x≥20 the exact rational lower bound is

    K(x)≥2E0(x+2)-|D|-Σ(|S_j|+|T_j|)
        ≥0.17966134138645...>1/10.

Consequently K0(x)≥κ0=10^-8 everywhere. Here K0 means the base PROFILE functional, not K evaluated at zero.

## 2. A concrete fixed correction neighbourhood

Take ||c||∞≤ρ=10^-200. This deliberately conservative value avoids any need to optimize the neighbourhood. `stability_check.py` verifies coefficient-norm bounds with exact rationals, not a c-grid.

For full complex Fourier coefficients z_j and derivative coefficients v_j=jwz_j let Z=Σ|z_j|, V=Σ|v_j|, and let H_z,H_v be the sums of these norms over the six correction directions. Then Δz≤ρH_z, Δv≤ρH_v, and

    ΔE_l1≤2VΔv+(Δv)²,
    ΔC_l1≤ZΔv+VΔz+ΔzΔv.

Cbar≥Cbar0/2, Ebar≥Ebar0/2, and

    Δλ≤2ΔE/(Cbar0/2)+2Ebar0ΔC/[Cbar0(Cbar0/2)].

Using (K), a uniform bound on |K_c-K_0| on [0,20], and on the change of the tail lower-envelope intercept at x=20, is

    B_K=45ΔE+(2/w+2)[(|λ0|+Δλ)ΔC+Δλ||C_0||_l1+ΔE].

The script proves B_K<5×10^-9 and that the tail slope stays positive. Thus

    K_c(x)≥κ*=5×10^-9 for all x≥0.

For the current factor, polynomial l1 norms X0,B0,H_X,H_B give a variation bounded by

    binom(2N+4,4)(4N-1)
      [ρH_X||B0||_1+ρH_B||X0||_1+ρ²H_XH_B].

The binomial factor bounds division by (1-y)^4 using its power series; divisibility is preserved by the exact endpoint conditions. The bound is <1/200, so the factored current is ≥1/200 throughout the same cube. The resulting current is nonnegative, with only the forced endpoint zeros. The cube contains a Euclidean ball, which is sufficient for the IFT.

## 3. Radius

The bounds in 01 give 0≤q≤C0δ, and q≥ηδ for x≥T. Hence R>0 for every finite x, R→0 as x→∞, and R(y)≤R(x)e^(-ηδ(y-x)) for y≥x≥T. Define ρ_r(t)=R(-log t); this symbol is the radius function, not the correction-ball radius. It satisfies ρ_r,tt=-δρ_r |z_x|²/t²≤0 and ρ_r,t=qR/t>0 for t<1. The strict inequality follows because a nonzero trigonometric E cannot vanish on an interval. Also ρ_r(0)=0.

## 4. Uniform charge-radius asymptotics

Let I(x)=δ∫_x^∞CR². The exact energy identity is

    δ∫_x^∞ ER²=(1/2-q(x))R(x)²+∫_x^∞q²R².

Since q²≤C0δ q and ∫_x^∞qR²=R(x)²/2, the final term is O(δR(x)²). Integrating the bounded periodic primitive of C-(Cbar/Ebar)E gives its contribution O(δR(x)²), uniformly in x,c. Therefore

    I(x)=λ(c)^-1 R(x)²[1+O(δ)],
    J∞=I(0)=λ^-1[1+O(δ)],
    Q∞(x)=I(x)/I(0), Q∞(x)/R(x)=R(x)[1+O(δ)].

The constant is uniform on the correction cube. No pointwise lower bound on E is used.

## 5. The compact H expansion, with its actual coefficient

Define

    H∞(t)=t-∫_0^t (Q∞/ρ_r)² du.

Let p'+p=E,p(0)=0, A(x)=∫_0^x p and F(x)=∫_0^x C. Variation of constants in q-δp gives |q-δp|≤Cδ² globally, whence

    R=1-δA+O(δ²(x+x²)),
    R^-1=1+δA+O(δ²(x+x²)e^(C0δx)),
    Q∞=1-δλF+O(δ²(x+x²)).

For the third estimate use exactly Q∞=1-J∞^-1δ∫_0^xCR², J∞^-1=λ+O(δ), and |1-R²|≤Cδx. For the first two estimates use |A|≤Cx and Taylor's theorem for the exponential; the stated errors remain upper bounds even for large x. Products give an error ≤Cδ²(1+x)^4 e^(2C0δx) in (Q∞/R)². Its y-integral against e^-y is finite uniformly for small δ.

Consequently for each fixed X,

    H∞(e^-x)/e^-x=δK_c(x)+O_X(δ²), 0≤x≤X,
    K_c(x)=2∫_0^∞e^-y[λF(x+y)-A(x+y)]dy.          (H)

The coefficient in (H) is precisely (K). Indeed

    p=E0+Σ E_j(cosν_jx+ν_j sinν_jx)/(1+ν_j²)-D e^-x,
    A=E0(x-1)+D e^-x
       +Σ E_j[sinν_jx/ν_j-cosν_jx]/(1+ν_j²).

In particular the constant in A is -E0, not -D. Integrating (H) gives 2E0(x+2) in (K). This explicit computation resolves the possible constant-term ambiguity. A separate exact check is K(0)=2λ∫e^-x C dx-∫e^-x E dx, yielding 1.0951713352112...×10^-7 for the given profile.

For δ small enough the compact error is ≤δκ*/2, giving H∞>0 on [0,X].

## 6. Infinite tail H positivity

Choose B with Q∞/R≤(1+Bδ)R. Fix X≥T+(B+1)/η, independent of δ and c. For x≥X,y≥0,

    (Q∞/R)(x+y)≤(1+Bδ)e^[-ηδ(x+y-T)]≤e^(-ηδy).

Here log(1+Bδ)≤Bδ justifies the fixed X. Thus

    H∞(e^-x)/e^-x
       ≥1-∫_0^∞e^[-(1+2ηδ)y]dy
       =2ηδ/(1+2ηδ)>0.

Even if X is very large, it is fixed before δ is taken small, so the compact and tail arguments are compatible. No claim of a useful numerical amplitude follows from these coarse constants.

## 7. Exact finite truncation

By nonnegative current, 0≤Q∞≤1 and Q∞(ε)<1, and

    Qε(t)=[Q∞(t)-Q∞(ε)]/[1-Q∞(ε)]≤Q∞(t), ε≤t≤1.

The inequality follows algebraically from 0≤Q∞(ε)≤Q∞(t)≤1. Concavity and ρ_r(0)=0 imply ρ_r(ε)/ρ_r,t(ε)≥ε. Integrating the exact radial equation with the exact Minkowski initial value gives

    4r r_U=-Hε(V),
    a0 Hε(V)=ρ_r(ε)/ρ_r,t(ε)+t-ε
                 -∫_ε^t (Qε/ρ_r)²du
             ≥H∞(t)>0.

Thus r_U<0 throughout the closed finite cone. r≥R(L)>0. The positive minima are for each fixed finite construction; they are not asserted uniform as δ→0.

Finally cδ→0 from 03 enters the certified cube for small δ. All conclusions apply to the exact nonlinear root, not just the uncorrected profile.


---

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


---

# Exact charge normalization and low coupling [C]

For the conventions of 01, Φ_V=−√δ(1−ε)z_x/t, so

    Im(Φ conj(Φ_V))=δ(1−ε)C/t.

The Maxwell equation Q_V=e r² Im(Φ conj(Φ_V)) therefore integrates to Q(1)=eJ_L with J_L=δ∫_0^L CR². It has positive sign. No extra affine factor survives the change of variables. Set e=J_L^-1. Then Q(0)=0 and Q(1)=1 exactly.

The radius seed is independent of e, so this definition is not circular. J_L>0 on the certified correction cube; its C1 dependence follows by differentiation under a finite integral. The uniform estimates in 01–02 strengthen this to

    J_L→1/λ(c), e→λ(c) in C1_c.

There is no need to add e as a seventh unknown. One could equivalently impose the seventh equation eJ_L−1=0, whose partial derivative in e is J_L≠0, and eliminate e by the implicit function theorem. The residuals in 01 already use the eliminated e(c,δ,L); their parameter derivatives include its derivative.

At c=0 the limiting Jacobian is exactly Tλ0 DM, because

    D_c[Tλ(c)M(c)]=(∂λTλ)(D_cλ)M(c)+Tλ(c)D_cM(c)

and M(0)=0. The discarded term is zero only at that base point, not on the whole parameter ball.

The exact rational Fourier means verify

    0.56129762150689 < λ0 < 0.56129762150691 < 0.57.

For the exact root cδ→0,

    e(δ,L(δ),cδ)→λ0.

Thus e<0.57 for all sufficiently small δ. With r(1)=Q(1)=1 and r_V(1)=0 the renormalized Hawking mass is

    varpi=r/2[1+4r_U r_V/Ω²]+Q²/(2r)=1.

Consequently the matched RN parameters are M=Q=1, and eM=e<0.57. The theorem asserts existence of such a coupling; it is not a theorem for every prescribed eM<0.57. Standard length scaling can equivalently fix a nonzero dimensional scalar coupling and choose the corresponding mass, while preserving the product |e|M. Charge conjugation gives the opposite charge sign if desired.


---

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


---

# Regularity and center extension [C]

KU §5.2, printed p.38, footnote 7 explicitly uses characteristic regularity k+1 to guarantee global regularity k because of the spherical wave equation at the center. For the present input, k+1=3 and the guaranteed global regularity is C2. The characteristic construction and local gluing away from r=0 retain order three. The loss in the stated guarantee occurs when extending to the regular center.

One can see the derivative bookkeeping already for a radial linear wave: the regular solution contains a divided difference (f(t+r)−f(t−r))/r. Controlling its k derivatives through r=0 calls for k+1 derivatives of f. This is an explanation of the regularity count, not a substitute for KU's nonlinear center-extension argument.

C2 regularity of the metric and scalar field, with the compatible Maxwell regularity in the construction, suffices to evaluate the classical second-order Einstein and scalar equations. The center is regular in Cartesian coordinates under the cited spherical center construction; the degenerate polar coordinate description at r=0 is not a curvature singularity.

It would be incorrect to say the model necessarily loses exactly one derivative or cannot be better than C2. The cited method guarantees C2 from this input. To guarantee a global C3 solution by the same regularity bookkeeping, order-four characteristic gluing is sufficient and is what that method asks for. This is not a proof that C4 gluing is a mathematically necessary condition for every possible globally C3 collapse construction.

No nonspherical low-regularity existence theorem or high-regularity Cauchy-stability alternative is substituted for the spherical argument here. The applicable branch is the spherical center-extension route in §5.2 preceding Lemma 5.1.


---

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
