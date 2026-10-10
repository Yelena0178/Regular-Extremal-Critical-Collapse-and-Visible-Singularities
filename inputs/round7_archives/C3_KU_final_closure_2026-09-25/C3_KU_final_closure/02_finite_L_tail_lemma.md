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
