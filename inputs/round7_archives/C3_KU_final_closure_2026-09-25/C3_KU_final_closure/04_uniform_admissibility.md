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
