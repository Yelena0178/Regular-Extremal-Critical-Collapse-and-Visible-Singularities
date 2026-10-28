# A-COM19：实际普通时间交换、可积体强迫与能量门槛

2026-10-24，R27。冻结D001、e=3/5、GA-2026-10-16-v1及A1–A6。接续[JET18](TIMELIKE_CHARGE_AND_COEFFICIENT_JETS.md)实际迹中保留F″的缺口，不重复电荷冻结。复用其A/D/K条件估计、[SOURCE01](GLOBAL_RN_SOURCE_NORM_AUDIT.md)的协变交换与[GREEN14](PHYSICAL_TRACE_GREEN_AND_DELAY.md)的真实内边界原则。新结论均INTERNAL_AUDIT；本轮没有支付统一A/D/K，也没有完成Goal A。

## COM19.1：固定规范中的普通时间交换不产生静态电场源

在实际Bondi图r≥R≥max{4M,1}、A=a du、a_∞=0中，令P=∂uΨ、Z=Ψ_r。固定规范后普通∂u合法；不声称它在任意时间依赖规范变换下协变。保留c≥c_*>0，这是远区估计，不能延伸到c退化的视界。

实际算子为

    LΨ=−2Ψ_{ur}+∂r(cΨ_r)−2ieaΨ_r−(iea_r+c_r/r)Ψ=0。

直接时间交换，先保留完整最高阶项：

    LP=−c_u Z_r+(2iea_u−c_{ru})Z
                           +(iea_{ru}+c_{ru}/r)Ψ。       (C1)

也可写成LOW05同型散度源，内端项必须保留：

    LP=∂rS₁+S₀，
    S₁=−c_u(Z−Ψ/r)+iea_uΨ，
    S₀=−c_uZ/r+c_uΨ/r²+iea_uZ。                       (C2)

若把C2直接当普通L²强迫，就会遇到∂rS₁；不能因为S₁本身小就删去这个径向导数。实际原波式恰好给

    cZ_r=2P_r+(2iea−c_r)Z+(iea_r+c_r/r)Ψ。

因此设ρ=c_u/c，改把顶阶项留在左侧，有精确的无二阶低层场强迫式

    (L+2ρ∂r)P=T_Z Z+T_Ψ Ψ=:S，
    T_Z=ρ(c_r−2iea)−c_{ru}+2iea_u，
    T_Ψ=iea_{ru}+c_{ru}/r−ρ(iea_r+c_r/r)。             (C3)

C1–3不引入F″或P_u的体强迫。与D_u交换不同，时间静态的a,c使ρ=T_Z=T_Ψ=0；大而静态的库仑项仍在L左侧，不能假装它已消失。消去Z_r用了c>0，必须列出共同下界。

## COM19.2：真实低阶输入支付加权L¹时间、L²径向强迫

**逻辑PROVED（实际有限窗A/D/K输入下）；证据ANALYTIC/EXACT_ALGEBRA；审计INTERNAL_AUDIT。** 在[0,T]采用JET18的ν=1−η、g=1−2η及B_γ、C_γ、B_Q、C_m、b_*、C_Z。所有这些常数与T无关，实际A=A_η(T)、D=D_η(T)仍待统一控制。设E_c=2M+K²/R，定义非负径向主控函数

    G_γ=B_γ r^(−3/2)+C_γ A²r^(−2)，
    G_m=b_*^(−1)[2D²+C_m A²/r]，
    G_Q=|e|AD sqrt(r)+B_Q A²，
    G_c=G_γ+2G_m/r，
    G_{cr}=E_c G_γ/r²+2G_m/r²+2K G_Q/r³，
    G_{ar}=(K G_γ+G_Q)/r²，
    G_a=2|e|AD/sqrt(r)+B_Q A²/r
                    +K[2B_γ/(5r^(5/2))+C_γ A²/(3r³)]。

JET18及其a_{ru},c_{ru}精确式逐项给

    |c_u|≤G_c U^(−2ν)， |c_{ru}|≤G_{cr}U^(−2ν)，
    |a_u|≤G_a U^(−2ν)， |a_{ru}|≤G_{ar}U^(−2ν)。     (C4)

不对JET18的包络直接微分；特别是c_{ru}要用实际Einstein/Maxwell式计算。为给简明共同常数，取

    C_c=B_γ/sqrt(R)+C_γ A²/R+2b_*^(−1)[2D²+C_m A²/R]，
    C_{cr}=E_c[B_γ/R^(3/2)+C_γ A²/R²]
              +2b_*^(−1)[2D²+C_m A²/R]
              +2K[|e|AD/sqrt(R)+B_Q A²/R]，
    C_{ar}=|e|AD+B_Q A²/sqrt(R)
                         +K[B_γ/R²+C_γ A²/R^(5/2)]，
    C_a=2|e|AD+B_Q A²/sqrt(R)
                       +K[2B_γ/(5R²)+C_γ A²/(3R^(5/2))]。

则G_c≤C_c/r、G_{cr}≤C_{cr}/r²、G_{ar}≤C_{ar}/r^(3/2)、G_a≤C_a/sqrt(r)。令

    C_TZ=(C_c/c_*)[E_c/R^(5/2)+2|e|K/R^(3/2)]
                                      +C_{cr}/R^(3/2)+2|e|C_a，
    C_TΨ=|e|C_{ar}+C_{cr}/R^(3/2)
                         +(C_c/c_*)[|e|K/R^(3/2)+E_c/R^(5/2)]。

由|a|≤K/r、|a_r|≤K/r²、|c_r|≤E_c/r²得

    |T_Z|≤C_TZ r^(−1/2)U^(−2ν)，
    |T_Ψ|≤C_TΨ r^(−3/2)U^(−2ν)。

MOD08的全r放宽界|Z|≤C_Z A r^(−1/2)U^(−ν)、|Ψ|≤A sqrt(r)U^(−ν)于是给

    |S(u,r)|≤A(C_Z C_TZ+C_TΨ)r^(−1)U^(−3ν)，
    ||S(u,·)||_{L²(dr)}≤A(C_Z C_TZ+C_TΨ)R^(−1/2)U^(−3ν)。 (C5)

对任意σ<3ν−1（特别可取σ=ν），直接积分得

    ∫₀^T U^σ||S||₂du
       ≤A(C_Z C_TZ+C_TΨ)/[sqrt(R)(3ν−σ−1)]。

同时V=2ρ满足

    ∫₀^T ||V||_∞du≤2C_c/(c_* Rg)，
    |V_r|≤2[C_{cr}/(c_*r²)+C_c E_c/(c_*²r³)]U^(−2ν)。 (C6)

C5是实际低层输入对普通交换体强迫的可积估计，非新的自由边界假设。右侧关于A,D至少三次（固定M,K,R等常数）；但没有给未知P的传播估计，更没有用有界源自动推出所需迹尾。

径向积分另须谨慎：C5的r^(−1)放宽界不是L¹(dr)，不能用它去积分到I⁺。保留MOD08双尺度包络则可补足这一点。置α=1/2−η、C_S=C_Z C_TZ+C_TΨ、L_R(U)=2 asinh(sqrt(U/R))，精确原函数给

    ∫_R^∞dr/[r sqrt(r+U)]=U^(−1/2)L_R(U)，
    ∫_R^∞dr/[r(r+U)^(3/2)]
             =U^(−3/2)[L_R(U)−2sqrt(U/(R+U))]。

用未放宽的Ψ,Z界逐项估计，得到

    ||S(u,·)||_{L¹(dr)}≤A C_S U^(−3ν)L_R(U)。          (C6a)

晚时仅多一个log；它不破坏加权时间可积性。特别L_R≤2sqrt(U/R)，故sup U^(−2ν)L_R≤2/sqrt(R)。这里没有将发散的粗r^(−1)主控当可积函数。

## COM19.3：保留真实内边界，不能由零早期外尾推出P受控

在u=0的早期外尾P=0，但r=R处由完整内部供能。其真实物理迹W[P]=(D_u−c∂r/2)P精确为

    W[P]=∂uW−iea_uΨ+(c_u/2)Z。                        (C7)

后两项由C4/已有包络支付，∂uW没有被C5支付。若与固定(f₀,a₀)比较并作完整散度分部，GREEN14有效输入还含

    w_eff[P]=W[P]−(ie/2)(a−a₀)P+(c−f₀)P/(2R)。         (C8)

C8只表示原比较误差的内端组合；C3新增V∂rP及强迫另按体源记账，不删除、不设零，也不把它们擅合成已知边界小误差。系数有界和低层A/D给P的点态幅度不等于给∂uW、P_r或载频包络。普通时间交换没有自动提供TRACE17要求的U∂u慢变正则性；C6的无权可积界也不自动支付多一个U的时间矩。

还能把剩余缺口收紧到真实交换迹。由P=W+cZ/2−ieaΨ及CARRIER07的精确W−F′核，实际普通导数字段满足

    A_η[P]≤D sqrt(1+1/R)+(2Λ+C_Z/2+|e|K)A/R=:A_P。   (C8a)

例如W−F′项乘回A权重为2ΛA[1+U/r−sqrt(1+U/r)]/U≤2ΛA/r，未假定P多一阶时间衰减。对B=iea_r/2−c_r/(2r)，原波结构与C3给

    ∂r W[P]=BP−S/2+ρP_r。

ρP在无穷端消失，故分部得到不含未知P_r的精确实际桥

    F″=W[P](R)−ρ(R)P(R)
                        +∫_R^∞[(B−ρ_r)P−S/2]dr。     (C8b)

这一步需要C6a；单用C5不能合法完成。设C_ρ=C_{cr}/c_*+C_c E_c/(c_*²R)，则|ρ_r|≤C_ρr^(−2)U^(−2ν)。记D_P(T)=sup U^ν|F″|、H_P(T)=sup U^ν|W[P](R)|，沿用精确径向半积分核并用C6a得

    D_P(T)≤H_P(T)+R^(−1/2)
               ·{2ΛA_P+(C_c/c_*+2C_ρ)A_P+A C_S}。    (C8c)

C8a–c在实际有限窗成立，没有额外P_r或F″体源预算。但H_P仍是新的真实内边界义务，不能将C8c当其闭合；给定低层A/D并不自动给高层D_P。也没有从普通导数的幅度界推断TRACE17的慢变载频分解。

## COM19.4：交换场不自动拥有原Maxwell的正能量抵消

SOURCE01对实际φ的电场功抵消用了它与实际Q的Maxwell配对。对P=∂uΨ，不能把Q_u直接当成“P的电荷”。径向Maxwell连续微分给

    Q_{ru}=e Im(P conjugate(Z)+Ψ conjugate(P_r))，
    Q_{ruu}=e Im(P_u conjugate(Z)+2P conjugate(P_r)
                                        +Ψ conjugate(P_{ur}))。 (C9)

P自身的径向电流为e Im(P conjugate(P_r))；它不是Q_{ru}。例如单点形式jet Ψ=Z=0、P=1、P_r=i时前者为−e，Q_{ru}=0。原波式要求Z_r=2i/c，可同时满足该jet条件；这只反驳代数配对，未构造完整Cauchy发展或Goal A反例。C9的二次时间层含2P电流，但同时含P_u和Ψ的项，不能删后者取得正Maxwell余额。

另一个直接能量审计：固定参考RN远区中改用静态t=u+x、x_r=f₀^(−1)，作时间无关规范变换把A_x置零，A_t=Q₀/r仍在。此规范只用于参考测试能量，不用作Goal A强AF比较或改动实际Bondi规范。普通时间导数P不受该时间无关变换的额外导数影响。测试波满足

    (∂t+iea₀)²P−P_{xx}+V₀P=0， V₀=f₀ f₀′/r。

静态规范下标准时间能量是

    E_can[P]=(1/2)∫[|P_t|²+|P_x|²+(V₀−e²a₀²)|P|²]dx， (C10)

其平衡保留两端通量Re(P_x conjugate(P_t))；仅在端通量为零时守恒。2iea₀P_t的实功为0。它不是自动非负。取P_t=0、P=sqrt(r)g(log(r/S))、g实、支撑在(0,L)，则远区平直主型为

    E_flat=(1/2)∫[|g_s|²+(1/4−q²)|g|²]ds， q=eQ₀。

当q>1/2，取g=sin(πs/L)于[0,L]、区间外零，属于H¹₀；

    E_flat=π²/(4L)+(1/4−q²)L/4<0
                       若L>π/sqrt(q²−1/4)。          (C11)

先选L使严格负，再取S充分大，RN误差趋零，H¹₀的光滑紧支撑逼近保持严格负。具体固定e=3/5、M₀=Q₀=1、L=12、S=10000，用π²<10，有E_flat<−73/600。RN误差绝对值不超过

    (1/2){(3/S)(23/12)+(4/S)6
                             +(9/25)[(3/S)/(1−3/S)]6}<1/500，

故该指定能量确实非正定。误差界分别由|f₀−1|≤3/S、|rf₀′|≤4/S和|f₀^(−1)−1|≤(3/S)/(1−3/S)支付；无需有限计算推断全频稳定性。

C10–11仅否定指定测试场能量的自动强制性，不是参考不稳定性结论，也不声称该测试数据是某个目标实际交换场。特别不能因C5/C6可积就直接使用未经证明的正能量Gronwall；仍需真实内边界、适当稳定传播/频率结构，以及原耦合系统高阶估计。

## 三轴裁决、失败尝试与下一动作

| 声明 | 逻辑状态 | 证据类型 | 审计状态/范围 |
|---|---|---|---|
| C1–3普通交换及消去二阶低层场 | PROVED | ANALYTIC/EXACT_ALGEBRA | INTERNAL_AUDIT；固定规范、远区c_*下界；静态场不作小强迫 |
| C4–6实际体强迫的加权可积控制 | PROVED（明确A/D/K输入） | ANALYTIC | INTERNAL_AUDIT；不微分包络，不证明P传播或实际输入 |
| C7–9真实迹/Maxwell电流关系 | PROVED | ANALYTIC/EXACT_ALGEBRA | INTERNAL_AUDIT；内边界∂uW保留，Q_u不是P的Maxwell配对 |
| C6a/C8a–c交换场幅度与二阶辐射桥 | PROVED（低层A/D/K及未知H_P输入） | ANALYTIC/EXACT_ALGEBRA | INTERNAL_AUDIT；补足径向L¹而非误用r⁻¹粗界；不声称H_P已证 |
| C10标准静态时间能量自动非负 | REFUTED（指定功能） | ANALYTIC/EXACT_INEQUALITY | INTERNAL_AUDIT；负测试功能非D001或Goal A反例，非模不稳定 |
| 实际交换能量、F″/载频迹、全A/高频/强视界/同曲线三分支 | OPEN | 缺真实全局传播/内边界证据 | A1–A6不变 |

本轮关闭的是普通时间交换体强迫中的顶阶低层损失及其明确范数；没有把能量门槛或边界门槛改名为已证。失败路线保留：直接对散度源套L²会漏导数；把D_u的静态电场交换源当时间短程不成立；把原φ/Q功抵消照搬到P/Q_u不成立；仅凭可积系数/强迫自动获得正能量传播不成立。

下一轮不再强化C5右侧。应在完整内部供能与固定参考散射之间寻找能控制C7的真实传播估计，或者转向有限r Green公式保留原始低层场，从而绕开未证的高阶边界。可先检验把实际晚时度量静态主部纳入参考是否消除当前不衰减几何误差；任何RN参考Robin逆的零频/上半平面性质须另证，不能沿用仅平直Coulomb的ROBIN13结论。目标仍为实际全时间尾及同一X⁶三分支。

[核验脚本](verify_ordinary_time_commutation.py)、[报告](ORDINARY_TIME_COMMUTATION_CHECKS_2026-10-24.json)只认证列明精确式和有限主控积分，不认证解析统一传播、实际迹输入或Goal A。
