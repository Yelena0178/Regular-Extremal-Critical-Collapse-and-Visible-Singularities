# A-JET18：实际世界管电荷流、加强冻结与一阶系数交换

2026-10-24，R26。冻结 D001、e=3/5、GA-2026-10-16-v1，不改模型、X⁶或A1–A6。接续 [TRACE17](FULL_SPACE_PHYSICAL_TRACE_AUDIT.md) 的实际迹缺口；复用 [MOD08](MODULATED_BONDI_RADIAL_IMPROVEMENT.md) 的径向改进和 [COUL04.2](COULOMB_RENORMALIZATION_AND_MELLIN_GATE.md) 的无损光学表示。以下实际估计依赖明确的A/D/K输入，均为 INTERNAL_AUDIT；没有证明这些输入全未来有界。

## JET18.1：约定、依赖与实际固定半径电荷式

在BOND02已实现的实际Bondi图中，r≥R≥max{4M,1}，U=1+u，0<η<1/4，设

    ν=1−η，g=1−2η，h=1/2−2η，
    A=A_η(S)，D=D_η(S)，|Q|≤K，0≤u≤S。

所有常数允许依赖R,M,K,η；S不进入常数。沿用MOD08的Λ、C_Z、C_φ=1+C_Z、C_Q=|e|C_Z。实际场为Ψ=rφ、Z=Ψ_r、p=φ_r、W=D_nΨ，n=∂u−c∂r/2、c=b(1−2m/r)、D_u=∂u+iea。径向改进和波式给

    |Ψ|≤A sqrt(r) U^(−ν)，
    |p|≤C_φ A r^(−3/2)U^(−ν)，
    |W|≤[D+2ΛA/sqrt(r)]U^(−ν)，
    |Q_r|≤C_Q A² U^(2η)/(r+U)²≤C_Q A²U^(−2ν)。 (J1)

这是把已有双尺度包络放宽后的全r界，并非将大r渐近常数当共同时间常数。Maxwell取向务必保留为D001的

    Q_r=e Im(Ψ conjugate(Z))，
    nQ=−e Im(Ψ conjugate(W))，
    Q_u=(c/2)Q_r−e Im(Ψ conjugate(W))
       =cQ_r−e Im(Ψ conjugate(D_uΨ))。             (J2)

最后一项的c不是c/2；W与D_uΨ相差cZ/2。复共轭位置整体翻转会改电荷取向，不能在其中一行单独改号。

定义非负常数

    B_Q=2|e|Λ+C_Q/2，
    L_R=|e|AD sqrt(R)+B_Q A²。

由c≤1和J1/J2，在真实世界管上

    |Q_u(u,R)|≤L_R U^(−1−g)，
    |Q(v,R)−Q(u,R)|≤(L_R/g)[U^(−g)−(1+v)^(−g)]
                 ≤(L_R/g)U^(−g)， u≤v≤S。       (J3)

这是实际方程上的有限窗推论，没有以任意边界电荷函数代替Maxwell演化，也没有假定终电荷。

## JET18.2：不用先有Q_f的加强末端冻结

令Q_S=Q_B(S)，只作该有限窗的固定参考。MOD08给

    |Q(u,r)−Q(u,R)|≤C_Q A² U^(2η)/(R+U)，
    |Q_B(S)−Q(S,R)|≤C_Q A² (1+S)^(2η)/(R+1+S)。

两项各≤C_Q A²U^(−g)。结合J3，设

    E_R=2C_Q A²+L_R/g，

得到全r、全有限窗的实际估计

    |Q(u,r)−Q_S|≤E_R U^(−g)，
    |Q_B(u)−Q_S|≤E_R U^(−g)。                  (J4)

先在每个有限u取r→∞是BOND02已有操作；不交换u→∞。若同一实际解的A,D,K有共同全时间界，J3使Q(u,R)成为Cauchy族；MOD08的|Q−Q_B|≤C_Q A²U^(−g)再给共同极限Q_f及

    sup_{r≥R}|Q(u,r)−Q_f|+|Q_B(u)−Q_f|
                         ≤2E_R U^(−g)。        (J5)

比单独积分Bondi电流得到的U^(−h)更强。原因是固定半径的Ψ多一个内锥衰减因子；不是给Bondi电流绝对值强行加快衰减。J5只认同远区的电荷极限，没有认同视界电荷、没有Mf=|Qf|，也没有支付A/D/K本身。

反驳测试：仅在Bondi边界ODE取α=1/2−η、Ω>0、F=U^(−α)exp(2iΩsqrt(U))，则U^α|F|=1、U^ν|F′|≤sqrt(α²+Ω²)，能量可积，但Q_B′=eΩU^(−1−h)，终电荷尾为eΩU^(−h)/h，不能升级到U^(−g)。可在初段光滑开启，不改变尾率。这不是实际D001解；它验证新证明必须同时使用实际固定半径Maxwell式及MOD08径向电荷改进，不能声称仅由辐射A/D或Bondi平衡得到J5。

实际a=∫_r^∞bQ/s²ds，MOD08的光学余项给

    r|e(a−Q_S/r)|≤d_R U^(−g)，
    d_R=|e|[E_R+K C_φ² A²/(6R²)]。             (J6)

这里∫_r^∞(1−b)/s²≤C_φ² A²U^(−g)/(6r³)，直接由M4的J_b≤1/(2s²)得到。对S→∞的Green功能极限仍须先固定参考Q₀；不能把Q_B(S)随着切断参数移动后使用UPPER16的同一核极限。J4/J6只加强每窗估计，不授权那种交换。

## JET18.3：更强时间幂次的径向转换会饱和

**逻辑PROVED（指定实际源范数的条件估计）；证据ANALYTIC；审计INTERNAL_AUDIT。** 设|δc|≤G/r、r|eδa|≤d_R U^(−g)。仅估计非截断误差

    F₁=−δc(Z−Ψ/r)+ieδaΨ，
    F₀=−δc Z/r+δcΨ/r²+ieδa Z。

沿用BODY11的N_η=∫[r^(−1/2)sup U^ν|F₁|+sqrt(r)sup U^ν|F₀|]dr。令x=U/(r+U)。由于g>1/2，不能沿用x^(1/2)≤(U/r)^g；当U/r→0该式为假。正确的是

    sup_{U≥1} U^(−g)x^(1/2)=(r+1)^(−1/2)，
    sup_{U≥1} U^(−g)x^(3/2)≤C_g r^(−g)，
    C_g=(1−2g/3)^(3/2−g)(2g/3)^g。

第二式通过在y=U/r>0上求y^(3/2−g)/(1+y)^(3/2)的最大值得到。故

    N_η≤(1+C_Z)2GA/R
                +d_R A[2R^(−1/2)+(C_Z C_g/g)R^(−g)]。 (J7)

时间幂从h改善到g，但F₁的绝对值时间确界只给R^(−1/2)；把两项都写成R^(−g)会错。d_R还含AD sqrt(R)，所以不能由J7宣称扩大世界管免费闭合非线性小性。旧BODY11的h估计保持有效；J7是另一有界估计，不声称逐参数总比旧界小。没有处理完整有限r体源、高频或实际迹。

## JET18.4：一阶系数时间变化由已有低阶输入支付

**逻辑PROVED（实际有限窗、明确A/D/K）；证据ANALYTIC/EXACT_ALGEBRA；审计INTERNAL_AUDIT。** 为研究迹交换，使用COUL04.2已证明而非重新假设的表示。记γ=b_u/b、v=D_nφ；则

    v=(W+cΨ/(2r))/r，
    γ=c r|p|²/2
      +∫_r^∞[2Re(v conjugate(p))−(s c_s+c)|p|²/2
                                      −a_s Q_s/s]ds。 (J8)

这里p、v、c在积分项均于(u,s)评价。AF端使n log b在无穷远为0；静态RN的p=v=Q_s=0给γ=0。设

    L_c=1+2M/R+K²/R²，B_v=2Λ+1/2，
    B_γ=(4/3)C_φ AD，
    C_γ=C_φ²/2+C_φ B_v+L_c C_φ²/4+K C_Q/2。

J1给|v|≤[D/r+B_v A/r^(3/2)]U^(−ν)。J8逐项径向积分得到

    |γ|≤[B_γ r^(−3/2)+C_γ A²r^(−2)]U^(−2ν)。  (J9)

保留电磁项a_sQ_s，使用|a_s|≤K/s²；它不被设零。令

    b_* =exp[−2M/(R(1−2M/R))]>0，
    C_m=2B_v²+C_φ²/4。

实际质量式在固定r上精确为

    m_u=−r²|v|²/b+c²r²|p|²/(4b)，
    |m_u|≤b_*^(−1)[2D²+C_m A²/r]U^(−2ν)，
    c_u=cγ−2b m_u/r。                          (J10)

电磁库仑项在n m+c m_r/2中精确抵消；m_u本身未获符号。Maxwell还给

    a_u=∫_r^∞ b[Q_u+γQ]/s² ds，
    |a_u|≤[2|e|AD/sqrt(r)+B_Q A²/r
          +K(2B_γ/(5r^(5/2))+C_γ A²/(3r³))]U^(−2ν)。 (J11)

所有固定r的系数一阶时间变差可积，∫_u^S U_s^(−2ν)ds≤U^(−g)/g。推导只用了实际一阶场，不引入F″、W_u或高阶时间范数。仍是A/D/K条件结论；质量预算单独没有给这些右侧共同常数。

## JET18.5：实际迹第一次交换的精确边界缺口

写B=iea_r/2−c_r/(2r)，实际W_r=BΨ。由[∂r,D_u]=iea_r直接得

    ∂r(D_u W)=B_u Ψ+B D_uΨ+iea_r W，
    a_{ru}=−b(γQ+Q_u)/r²，
    c_{ru}=γc_r+b(2m_u/r²−2QQ_u/r³)。          (J12)

右侧系数全由J2/J9–11的低阶量表示。有限窗AF紧化允许径向积分且DuW(∞)=F″，所以

    D_uW(u,r)=F″(u)
       −∫_r^∞[B_u Ψ+B D_uΨ+iea_r W]ds。      (J13)

J12修复的是系数交换中的潜在损失；J13仍保留真实边界F″。普通时间导数还要减ieaW。不能由J9–13把F″删除，不能从已知F′∈L²推出加权F″；即使估计F″，一般载频的普通导数也不自动每次额外衰减一阶。规范相位Θ′=ea(u,R)仅给∂u(e^(iΘ)Ψ)=e^(iΘ)(W+cZ/2)，并不自动把实际W分成TRACE17的四阶慢变载频包络。

结构审计：在单个已知光滑AF截面u=u₀，Ψ、Z、m、Q、b、a及F′决定W的径向解；对J12另选F″会给另一个DuW径向解而不改变该截面上的低阶约束。这只说明上述径向等式没有提供F″估计，不是两个满足同一全Cauchy初值的实际解，更不是Goal A反例；实际历史、内区和散射仍可能提供所需限制。X∞逐成员光滑只给有限窗F″存在，不给目标的统一加权衰减。

## 审计账、失败路线与下一动作

| 声明 | 逻辑状态 | 证据类型 | 审计状态与范围 |
|---|---|---|---|
| J2/J8/J10/J12–13实际恒等式 | PROVED | ANALYTIC/EXACT_ALGEBRA | INTERNAL_AUDIT；复共轭取向、固定r与n区分、AF边界均保留 |
| J3–6加强冻结及条件终电荷 | PROVED（A/D/K输入下） | ANALYTIC | INTERNAL_AUDIT；有限窗先证，Q_f只在共同全时间界后定义 |
| J7及径向增益饱和 | PROVED（指定源范数） | ANALYTIC/EXACT_OPTIMIZATION | INTERNAL_AUDIT；非完整有限rGreen估计，不宣称总常数较小 |
| J9–11系数一阶时间变差 | PROVED（A/D/K输入下） | ANALYTIC/EXACT_ALGEBRA | INTERNAL_AUDIT；电磁功未删除，不支付迹高阶包络 |
| 系数光滑/一阶变差自动支付TRACE17的实际迹条件 | NOT_ESTABLISHED | 有限窗存在不够 | 径向交换仍含F″；非完整PDE不可能性证明 |
| 实际统一A/D/H、有限r体源、高频、强视界、同一X⁶三分支和Goal A | OPEN | 尚缺真实全局PDE证据 | 原A1–A6保持冻结 |

本轮没有重算COUL04已有的无损光学表示作为新成果。新进展是固定世界管Maxwell积分提升终电荷率、正确重做g>1/2的源范数转换，以及对实际系数给一阶可积时间界。失败路线记录：仅由Bondi电流绝对值积分看不到J4的改进；直接把h换成g会破坏x^(1/2)的径向比较；把系数变差当成迹包络则遗漏J13的F″。

下一轮应对实际内区/远区的时间交换建立可传递的辐射或世界管频率通道估计，显式保留F″/载频；先检查是否能通过协变交换与真实内边界的联合能量支付，而不把径向约束当时间演化。优先考察有限r Green体源与J12的配对，保留返回相位和世界管内端项；不能继续把加强冻结本身当完整A闭合。强视界与同曲线三分支仍独立列账。

[核验脚本](verify_timelike_charge_jets.py)及[报告](TIMELIKE_CHARGE_JETS_CHECKS_2026-10-24.json)区分精确代数、有限积分对照与实际未证输入；没有新外部定理或数值PDE认证。
