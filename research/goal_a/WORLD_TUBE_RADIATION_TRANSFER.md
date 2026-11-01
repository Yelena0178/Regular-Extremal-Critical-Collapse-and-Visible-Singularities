# A-TRACE09：真实世界管、散度源辐射公式与反射替代障碍

2026-10-23，R17。固定 D001、e=3/5、GA-2026-10-16-v1。复用 [CARRIER07](TAIL_CURRENT_AND_CARRIER_AUDIT.md)、[LOW05](LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md) 与 [INNER06](MELLIN_INNER_TRANSFER_AND_CHARGE_BOOTSTRAP.md)。新证明为 INTERNAL_AUDIT；实际尾估计与完整 Goal A 仍 OPEN。下面的外加 Coulomb 反例不属于完整 Einstein–Maxwell–标量模型。

## TRACE09.1：实际辐射导数由真实世界管迹支付

**逻辑 PROVED（实际有限窗估计，A/K输入）；证据 ANALYTIC/EXACT_ALGEBRA；审计 INTERNAL_AUDIT。** 沿用 CARRIER07 的 U=1+u、0≤η<1/4、R_*≥max{4M,1}、暂定 |Q|≤K，令

    H_η(T)=sup_{0≤u≤T}U^(1−η)|W(u,R_*)|，
    ε_R=2Λ_K/sqrt(R_*)， W=D_nΨ。

由 CARRIER07 的实际精确径向核，在相同 u 上

    U^(1−η)|W(u,R_*)−F′(u)|
      ≤2Λ_K A_η(T)U⁻¹ᐟ²[sqrt(1+U/R_*)−1]
      ≤ε_R A_η(T)，
    |D_η(T)−H_η(T)|≤ε_R A_η(T)。                (T1)

所以 D 不再是独立的远区主未知量。若 A=A_η(T)、H=H_η(T)，CARRIER07 的电荷预算变为

    J_η(A,D,K)≤AH/h+A²[ε_R/h+2Λ_K/g]，
    h=1/2−2η， g=1−2η。                         (T2)

这是一个实际幅度加真实边界输入的二次映射；H 的全未来衰减尚未证明。增大 R_* 只减小径向修正，不使 H 免费变小；若 A 统一有界，T1 反而显示该迹的加权范数趋近真实辐射导数范数。不能把初始外尾零场当作未来 H=0。

## TRACE09.2：固定参考的外向核与自然散度源

**逻辑 PROVED（固定参考 ODE）；证据 ANALYTIC；审计 INTERNAL_AUDIT。** 取合法静态参考 M₀≥|Q₀|>0，q=eQ₀，r≥R_*>4M₀。参考不认成实际终态；令 f₀=1−2M₀/r+Q₀²/r²，x_r=1/f₀、x(R_*)=0、k=ω−q/r、θ_x=k、θ(R_*)=0。对实 ω≠0，取归一外向解 R₊，满足

    R_{+,xx}+[k²−f₀f₀′/r]R₊=0，
    Y_ω:=exp(−iθ)R₊→1，
    R₋=conjugate(R₊)，
    W(R₊,R₋):=R₊R_{-,x}−R_{+,x}R₋=−2iω。      (T3)

外向解由 LOW05 的无穷端 Volterra 构造延至 R_*；在有限正半径段不要求额外视界条件。R₋ 是同一实系数 ODE 的另一解；此共轭关系只用于实 ω。

将 Ψ 的参考源写成 ∂rF₁+F₀，时间 Fourier 约定为 exp(iωu)，R=exp(iθ)Ψ̂。则静态模式方程的源为 ∂xG₁+G₀，其中

    G₁=exp(iθ)F̂₁， G₀=f₀exp(iθ)F̂₀−ikG₁。      (T4)

不能分别粗估 G₀ 中的 −ikG₁。它正好与辐射核的主要振荡导数抵消：

    R_{-,x}G₁−R₋G₀
        =∂x(conjugate(Y_ω))F̂₁−f₀conjugate(Y_ω)F̂₀。 (T5)

这是源结构的精确恒等式，不使用小电荷、最终参数或带保持假设。

## TRACE09.3：外向区域的核导数与低频源界

**逻辑 PROVED（参考径向估计）；证据 ANALYTIC；审计 INTERNAL_AUDIT。** 置 λ=|ω|，b₀=2|q|+1；限制 λ 足够小，使 r_b=b₀/λ≥R_*。在 r≥r_b，|k|≥λ/2，LOW05 的振幅能量给 |Y_ω|≤C。Y 满足

    f₀Y_{rr}+(f₀′+2ik)Y_r+B Y=0，
    B=iq/r²−f₀′/r。

令 V=f₀Y_r。外向终端条件给

    V(r)=exp(−2iθ(r))∫_r^∞exp(2iθ(s))B(s)Y(s)ds。 (T6)

先绝对积分得到 V=O(1/r)，再用 θ_r=k/f₀ 非零作一次分部，得到

    |V(r)|≤C/(λr²)+∫_r^∞C/(λs²)|V(s)|ds。

端点 BY/θ_r 在无穷远为零，剩余系数导数可积；|k|≥λ/2、r≥b₀/λ 使常数不依赖 λ。用从无穷端的 Volterra Gronwall，结论为

    |Y_r|≤C/(λr²)， |Y−1|≤C/(λr)。             (T7)

负频率同样适用，估计只用 |k| 的下界。T7 不提供频率导数的尾符号估计。

若在此外区 |F̂₁|≤C₁(ω)/r、|F̂₀|≤C₀(ω)/r²，T5 给

    (2λ)⁻¹|∫_{r_b}^∞[∂r(conjugate(Y))F̂₁
                                      −conjugate(Y)F̂₀]dr|
                  ≤C[C₁(ω)/b₀²+C₀(ω)/b₀]。     (T8)

没有额外的低频 λ 损失，也没有未经抵消的 log∞。这里 C_j 仍依赖实际源及时间截断，不能把 T8 当作全未来 A 估计。若分别估 R_{-,x}G₁ 与 R₋G₀，F₁∼1/r 时会制造不应出现的对数发散。

## TRACE09.4：实际有限时间场的完整辐射公式

**逻辑 PROVED（实际截断场/参考核恒等式）；证据 ANALYTIC/EXACT_ALGEBRA；审计 INTERNAL_AUDIT。** 对实际 Φ=ζ(u)Ψ，ζ∈C_c^∞，使用 LOW05 精确误差源 F₁[Φ]、F₀[Φ]，并将 −2ζ′Ψ_r 留在 F₀。BOND02 的有限窗 AF 光滑性给 F₁=O_T(r⁻¹)、F₀=O_T(r⁻²)，且 Φ 的无穷端为 ζF。对每个实 ω≠0，令

    h₀=Φ̂(R_*)， p₀=R_x(R_*)−G₁(R_*)。

对流 J=R R_{-,x}−(R_x−G₁)R₋ 精确微分，有 J_x=R_{-,x}G₁−R₋G₀。T3/T5 给

    −2iω·widehat(ζF)
       =h₀R_{-,x}(R_*)−p₀R₋(R_*)
         +∫_{R_*}^∞[∂r(conjugate(Y_ω))F̂₁
                                      −conjugate(Y_ω)F̂₀]dr。 (T9)

积分的无穷端按 T7 和有限窗源界绝对收敛。公式无需先假定实际解全未来可积。p₀ 也没有引入可自由选择的径向导数：在真实世界管上

    p₀=Fourier[cΦ_r−D_uΦ−(c−f₀)Φ/R_*]
       =Fourier[D_uΦ−2ζW−2ζ′Ψ−(c−f₀)Φ/R_*]。  (T10)

整个时间变化系数乘积都取 Fourier；不能将它与频率投影交换。

q>1/2 时，INNER06 的参考长内侧界给 R₋(R_*)、R_{-,x}(R_*)=O(sqrt(λ))，负频率由同一 Mellin 扰动绝对值界处理。因此 T9 的边界贡献至多 Cλ⁻¹ᐟ²(|h₀|+|p₀|)。分母来自同一外向核的自流，不是未知实际视界与无穷远两模式的交叉 Wronskian。

晚时间截断可获得一项有限改进。MOD08 的实际 Z 包络给

    ∫_{R_*}^∞|Z(u,r)|dr≤2C_Z A_η(2T)U^(−1/2+η)。

若 ζ_T 的晚截断导数支持于 [T,2T]、总变差一致有界，q>1/2 的参考核还满足低频全外区 |Y_ω|≤C（由 LOW05 与 INNER06 接合），于是仅晚截断源的贡献满足

    |widehat(F_late)(ω)|≤C A_η(2T)(1+T)^(−1/2+η)/|ω|。

乘 ω 后的界对一个固定低频带一致，但不支付完整加权时域 D 范数或低频 F 幅度。只有统一 A 真正兑现时，才可用它移除相应局部频率的晚截断项；不能据此先假定全未来可积。

这没有消除全局稳定性问题：保留完整真实 Cauchy 迹对才可使用该传递；不能把它说成仅给一个 Dirichlet 数据就存在衰减解的定理。将 T9 逆变换为点态 A 界，还需频率导数/源范数和剩余截断控制。全局实际视界匹配仍在独立义务中。

## TRACE09.5：反射世界管的外加 Coulomb 模型有增长模

**逻辑 PROVED（限定参考模型）；证据 ANALYTIC/SPECIAL_FUNCTION，有限根值仅作对照；审计 INTERNAL_AUDIT。** 此节采用 Minkowski 度规和外加静态 A=Q₀dt/r，不解 Einstein 反馈，故不是 D001 的完整解。研究 r≥R_* 上带电波，内界为反射 R(R_*)=0。模态 exp(−iωt)R(r)/r 满足

    R_{rr}+(ω−q/r)²R=0， q=eQ₀>1/2。

令 β=sqrt(q²−1/4)、z=−2iωr。根据 [DLMF 13.14](https://dlmf.nist.gov/13.14#E33) 的微分式、连接式与无穷端定义，外向解为 W_{−iq,iβ}(z)。标准恒等式的定位见 [读取收据](DLMF_WHITTAKER_RECEIPT_2026-10-23_R17.json)。小 z 展开为

    W_{−iq,iβ}(z)=z^(1/2)[A z^(iβ)(1+O(z))
                                      +B z^(−iβ)(1+O(z))]，
    A=Γ(−2iβ)/Γ(1/2−iβ+iq)，
    B=Γ(2iβ)/Γ(1/2+iβ+iq)。                     (T11)

由 [DLMF 5.4.4](https://dlmf.nist.gov/5.4#E4)，

    ρ:=|B/A|=sqrt(cosh(π(q+β))/cosh(π(q−β)))，
    1<ρ<exp(πβ)。                               (T12)

上界由 log cosh 的导数 tanh<1 给出。取主支 log，首项零点满足

    log z_n=[arg(−B/A)+2πn]/(2β)−i logρ/(2β)， n→−∞。

其固定辐角 θ_*=−logρ/(2β)∈(−π/2,0)，模趋零。在固定小相对圆周 |z−z_n|=ε|z_n| 上，首项有与 n 无关的正下界，余项 O(|z_n|)→0；Rouché 给一个精确简单零点 z̃_n=z_n(1+O(z_n))。于是

    ω_n=i z̃_n/(2R_*)， Im ω_n>0， Re ω_n>0。    (T13)

该模态在空间无穷端指数衰减、时间上指数增长，而 Dirichlet 迹恒为零；其法向/入射导数不为零。因此仅由反射 Dirichlet 迹和有限初始范数推出无条件衰减的外区替代命题是假的。该反例的初始场不是实际研究种子的零早期外尾；不声称它反驳该特定完整 Cauchy 演化。

这也说明实轴 T3 的自流不自动排除上半平面不稳定性。增长模若先乘有限时间截断，T9 中 ζ′ 源会保留它，不能无证明删去未来截断项。本文没有证明完整 RN 黑洞或实际 EMCSF 有这些模态；真实内部不能换成这个反射模型。

## TRACE09.6：三轴审计与下一义务

| 声明 | 逻辑 | 证据类型 | 审计/范围 |
|---|---|---|---|
| T1/T2 实际 D→真实迹H与A | PROVED（A/K输入下） | ANALYTIC | INTERNAL_AUDIT；H未来界仍OPEN，扩大外区不使迹免费小 |
| T3–8 参考核、散度抵消与外向源界 | PROVED（固定参考） | ANALYTIC/EXACT_ALGEBRA | INTERNAL_AUDIT；未给全部频率导数/时间尾估计 |
| T9/T10 实际截断辐射公式 | PROVED | ANALYTIC/EXACT_ALGEBRA | INTERNAL_AUDIT；保留完整迹对和未来截断，不假定全未来可积 |
| T11–13 反射Coulomb增长模 | PROVED（外加场模型） | ANALYTIC/SPECIAL_FUNCTION | INTERNAL_AUDIT；Rouché证明与有限求根分列，非完整D001反例 |
| 实际A/H尾界、强终态与A1–A6 | OPEN | 所需全未来/内区/同曲线证据缺失 | 契约不变，不以反射模型替换真实内部 |

本轮将远区 D 化为真实 H 加径向小修正，并给出可直接追踪边界和散度误差的辐射方程；同时排除一个会偷偷丢掉稳定性条件的反射替代。下一轮应主攻 A 与同一实际发展的 Ψ/W 世界管迹：对 T9 的核和源建立所需低频参数导数/时间卷积界，或与 MOD08 的锥内调制接合。必须保留真实内区供能、上半平面/边界条件审计及未来截断；不能把已知实轴分母当成全未来稳定性。

[核验代码](verify_world_tube_radiation.py)与[报告](WORLD_TUBE_RADIATION_CHECKS_2026-10-23.json)检查流/源/边界恒等式、Whittaker变量及三个有限复杂根；不认证实际 A/H 或 Goal A。
