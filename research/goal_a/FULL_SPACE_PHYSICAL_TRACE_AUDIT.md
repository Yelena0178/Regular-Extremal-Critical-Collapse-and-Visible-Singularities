# A-TRACE17：全空间W传递、必要反控制与载频兼容输入

2026-10-24，R25。D001、e=3/5、GA-2026-10-16-v1不变。复用[ROBIN13](PHYSICAL_TRACE_LOW_FREQUENCY.md)、[UPPER16](UNIFORM_UPPER_KERNEL_AND_FUTURE_LOCALIZATION.md)。本轮只研究低频纯边界传递，真实体源不被省略。新结论均INTERNAL_AUDIT；实际新增迹输入尚未兑现，Goal A仍OPEN。

## TRACE17.1：有限r的乘子并非辐射乘子

固定正q紧集、R=R_*≥1及ROBIN13的χ=χ₀(ωR)。纯外向边界解W₀=w给

    widehat(Ψ_b)(r,ω)=m_r(ω)widehat(w),
    m_r=−2Y(r,ω)/d_+(ω).                                (T1)

辐射极限的m_W阶数为−1/2，但固定r时m_r的零频阶数为0。设s_±=1/2±iβ、β=sqrt(q²−1/4)、A/B为ROBIN13的Whittaker系数，

    c_±=s_±−iq, b=A/B, a=b c_+/c_-,
    z=−2iωR, y=z^(2iβ), ℓ=r/R,
    κ_q=|a|e^(πβ)<1.

在|ω|r足够小时，一致有

    m_r=M_r^0+O(sqrt(Rr)|ω|r),
    M_r^0=−2sqrt(Rr) ℓ^(iq)/c_-
                         ·[ℓ^(−iβ)+b y ℓ^(iβ)]/(1+a y). (T2)

所有固定阶D_ω导数满足同样余项阶数。分母几何级数在闭上半平面的小频域一致收敛，因为|ay|≤κ_q。其非恒定系数按|a|ⁿ衰减，ℓ上的相位模为1。q紧集上κ_q远离1。

## TRACE17.2：核有两种尺度，但原函数统一有界

**逻辑PROVED（辅助低频边界核）；证据ANALYTIC；审计INTERNAL_AUDIT。** K_r=F⁻¹(χm_r)满足r≥R、t∈R上一致的

    |K_r(t)|≤C sqrtR (R+|t|)⁻¹ᐟ² sqrt[r/(r+|t|)],
    sup_{a<b}|∫_a^b K_r(t)dt|≤C sqrt(Rr).                (T3)

第一式由λ≤1/r处的阶0界C sqrt(Rr)与λ≥1/r处的阶−1/2界C sqrtR λ⁻¹ᐟ²，分别二进制分部求和。这里只是双侧核界。

原函数不能靠绝对值求和。对低频几何级数，用Γ–Laplace式得到

    L⁻¹[s^(iα)] = d/dt{1_{t>0}t^(−iα)/Γ(1−iα)}.

其原函数有界；α=0项对应有界Heaviside原函数。依据[NIST 5.4.3](https://dlmf.nist.gov/5.4#E3)及[5.5.1](https://dlmf.nist.gov/5.5#E1)，

    |Γ(1−iα)|⁻¹=[sinh(πα)/(πα)]¹ᐟ².

α=2nβ时增长至多C e^(πnβ)/sqrt(n)，与|a|ⁿ组成可和的κ_qⁿ序列。低频切片在1/r尺度上的逆核L¹范数统一；T2余项除ω后直接L¹_ω可积。高于1/r的原函数也可由∫sqrtR λ⁻³ᐟ²dλ≤C sqrt(Rr)控制。由此得到T3第二式，不加入q的额外共振排除。

## TRACE17.3：仅有H_η不足——精确的世界管反控制

**逻辑REFUTED（所述输入到输出的有界性）；证据ANALYTIC；审计INTERNAL_AUDIT。** 取r=R，T2的非恒定部分给正时间核渐近

    K_R(t)=R t⁻¹ P_q(log(t/(2R)))+O(R²t⁻²), t≫R,
    P_q(x)=−2(b−a)/c_-
           ·Σ_{n≥1}(-a)^(n−1)e^(−2inβx)/Γ(−2inβ).       (T4)

χ的常量部分为快速尾。低频余项是阶1，给O(t⁻²)。Γ倒数的增长与κ_q<1使级数及任意固定阶导数一致可和。P_q的首个系数非零，所以它是非零、均值0、周期π/β的光滑函数。因此∫_R^L|K_R(t)|dt按正系数log(L/R)增长，而有符号原函数仍满足T3。

令ν=1−η、0<η<1/4。对每个大T，构造光滑紧支撑输入w_T，支撑在s∈[2T/3,T−CR]，令τ=T−s、

    w_T(s)=(1+s)⁻ᵛ ρ_T(τ)
      ·conjugate(P_q(log(τ/(2R))))
           /sqrt(|P_q(log(τ/(2R)))|²+ε²).

其中ε>0固定，ρ_T在2CR≤τ≤T/4为1，并在CR与T/3之外为0。故H_η(w_T)=sup U^ν|w_T|≤1，且输入具有零早期尾。周期平均|P_q|²/sqrt(|P_q|²+ε²)>0，T4的余项径向可积，给

    |Ψ_b(R,T)|≥c R T⁻ᵛ log(T/R)−C R T⁻ᵛ.              (T5)

于是全空间A_η在r=R的权重已产生至少c sqrtR log(T/R)的增长。不存在仅依赖H_η的统一T全空间A界。这是合法辅助波边界输入族的反控制，不是实际D001演化、不反驳Goal A；实际W受到尚待证明的内区/散射结构约束。ROBIN13辐射界与T5不冲突，其输出空间不同。

## TRACE17.4：低频通道的时间正则性足够

**逻辑PROVED（辅助纯边界映射）；证据ANALYTIC；审计INTERNAL_AUDIT。** 对零早期尾的w₀，设

    L₀=sup_{u≥0}U^ν[|w₀(u)|+U|w₀′(u)|]<∞.

则

    sup_{r≥R,u≥0} U^(1/2−η)sqrt(1+U/r)
                       |(K_r*w₀)(u)|≤C_η sqrtR L₀.      (T6)

证明若u≤2r，直接用T3的半积分核和U⁻ν输入。若u>2r，将源时间分为[0,u/2]、[u/2,3u/2]与[3u/2,∞]：两尾由sqrt(Rr)/|u−s|和η>0控制为C sqrt(Rr)U⁻ν；中段写w₀(s)=w₀(u)+差值。常值部分用T3有符号原函数，差值用|w₀(s)−w₀(u)|≤C L₀U⁻ν⁻¹|s−u|，以及

    ∫_{|τ|≤u/2}|τ| |K_r(τ)|dτ≤C sqrt(Rr)u.

全部得到C sqrt(Rr)U⁻ν，正好支付内锥的A权重。不需要假装K_r绝对L¹。T5反控制的逐点H虽有界，其时间正则性L₀不保持统一，因此不与T6矛盾。

## TRACE17.5：保留非零载频，不回到R14的过强平方预算

对有限个通道令

    w=w₀+Σ_j e^(−iθ_j(u))a_j(u),
    |θ_j′|≥Ω_min>2ω₀, |θ_j′|≤Ω_max,
    U^k|∂u^kθ_j′|≤C_k (1≤k≤4),
    L_j=sup U^ν Σ_{k=0}^4 U^k|a_j^(k)|<∞.

所有通道取光滑零早期尾，θ_j实值。其低频纯边界输出满足

    A_η(Ψ_b)≤C sqrtR [L₀+Σ_j L_j].                     (T7)

Ω范围与相位常数进入C。证明在χ支持附近，ω−θ_j′远离0。对∫exp(iωu−iθ_j)a_j作四次非驻相分部，新的幅度为O(U⁻ν⁻⁴)，其ω导数到三阶可积。乘一个等于1于χ支持的平滑切片，得到C_c³频率函数；其逆核v_j满足∫(1+|t|)|v_j|dt≤C L_j。与T3的双尺度包络卷积给

    |Ψ_{b,j}(r,t)|≤C L_j sqrtR (R+|t|)⁻¹ᐟ²
                                             sqrt[r/(r+|t|)],

从而T7成立。相位可以慢变，不预设最终常载频、Q_f或极端等式。普通固定载频及u⁻¹对数相位振荡包络属于该类型；并未将[CARRIER07](TAIL_CURRENT_AND_CARRIER_AUDIT.md)的一般极端载频重新排除。

## TRACE17.6：实际依赖裁决

T6/T7是新迹输入的充分条件，**没有证明实际W满足这些通道/相位/时间正则性界**。T5表明不能只拿现有H_η逐点界就声称全A已闭合。实际有效边界还含GREEN14的势/度量校正；本轮没有把它们当自由零输入，也没有支付全部有限r体源。

| 声明 | 逻辑 | 证据 | 审计/范围 |
|---|---|---|---|
| T1–4 有限r符号/原函数/振荡尾 | PROVED（辅助低频） | ANALYTIC/EXACT_ALGEBRA/PRIMARY_IDENTITIES | INTERNAL_AUDIT；Γ因子及几何级数优势保留 |
| H_η单独给统一全空间A | REFUTED（辅助输入映射） | ANALYTIC | INTERNAL_AUDIT；反控制非D001/非Goal A反例 |
| T6/T7 带低频时间正则/载频分解的全A映射 | PROVED（纯边界/新输入） | ANALYTIC | INTERNAL_AUDIT；兼容载频不等于实际通道已证 |
| 实际W迹通道、有限r体源/高频/强终态/Goal A | OPEN | 真实PDE与同曲线证据缺失 | 原A1–A6不变 |

下一轮先研究实际W的低频时间正则性或物理内区可提供的载频分解；不得把T7输入写成已完成的实际前提。也可寻找无需该分解的实际波式能量/散射控制，但必须避开T5反控制。有限r体源、实际高频、强视界、Bondi/视界参数相认、Mf=|Qf|及同一X⁶三分支继续单列。

[代码](verify_full_space_trace.py)、[报告](FULL_SPACE_TRACE_CHECKS_2026-10-24.json)及[Gamma来源收据](DLMF_MELLIN_GAMMA_RECEIPT_2026-10-24_R25.json)分开精确式、有限控制和实际未验证输入；不机器认证解析算子范数或Goal A。
