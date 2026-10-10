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
