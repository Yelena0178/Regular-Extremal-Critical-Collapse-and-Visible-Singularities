# A-FAR03：实际远区 r^p 正性、库仑库与带权通量缺口

2026-10-23，R11。固定 D001、e=3/5、GA-2026-10-16-v1；承接 [BOND02](ACTUAL_BONDI_COMPLETENESS_BRIDGE.md) 的新完整形成种子。以下解析结论均为 INTERNAL_AUDIT，没有独立外部数学复核。此稿不选择极端端点，也不把远区估计当完整 Goal A。

## FAR03.1：实际区域与全时间一致的低阶界

**逻辑 PROVED（实际外区引理）；证据 ANALYTIC；审计 INTERNAL_AUDIT。** 取 R₀>4M，M=M_ADM；整个 r≥R₀ 外区有 0≤m≤M，f=1−2m/r≥1−2M/r，单位 Bondi 规范

    g₂=−b²f dt²−2b dt dr， c=bf， A=a dt， a_r=−bQ/r²， a(t,∞)=0。
    Ψ=rφ， Z=Ψ_r， n=∂t−(c/2)∂r。

BOND02 已逐个有限时间证明光滑 I⁺、φ(t,∞)=0、Q_B/M_B 存在。现在才可对每个 t 使用 AF 锚定的径向 Hardy；不是以尚未证明的共同迟时 AF 余项为输入。由

    m_r=Q²/(2r²)+r²f|φ_r|²/2， (log b)_r=r|φ_r|²

得到全时间一致（各 r≥R₀）

    |φ(t,r)|²≤2M/[r(1−2M/r)]≤4M/r，
    exp[−2M/(r(1−2M/r))]≤b≤1，
    |a(t,r)|≤sqrt(2M/r)。                         (F1)

第一个界用 |∫_r^∞φ_s ds|²≤r⁻¹∫s²|φ_s|²；第三个由 Q 的径向质量预算 Cauchy–Schwarz。F1 不给 |Ψ| 的 r 一致界，也不声称其时间可积。

**无需预设 Q_B 一致有界的点电荷界。** 在 [r,2r]，质量约束与 F1 给

    ∫ Q² ds≤8Mr²， ∫|Q_s|² ds≤32e²M²r，
    |Q(t,r)|≤sqrt(8Mr)+sqrt(32)|e|Mr，
    Q²/r²≤16M/r+64e²M²≤K²:=4+64e²M²。           (F2)

确切地说，第二式使用 Q_s=e s² Im(φ conjugate(φ_s))，max s²|φ|²≤8Mr 和 ∫s²|φ_s|²≤4M；第一式保证存在一点 y∈[r,2r] 满足 |Q(y)|≤sqrt(8Mr)，再沿区间积分 Q_s。F2 允许 |Q| 随 r 线性增长，不给最终电荷极限；但固定 r 世界管的电荷全时间有界。

## FAR03.2：Maxwell 完成的精确 r^p 恒等式

**逻辑 PROVED（实际微分恒等式）；证据 ANALYTIC/EXACT_ALGEBRA；审计 INTERNAL_AUDIT。** BOND02 的实际波式为

    D_n Z=(c_r/2)Z−(iea_r/2+c_r/(2r))Ψ，
    c_r=b(2m/r²−Q²/r³)， Q_r=e Im(Ψ conjugate(Z))。

对任意实 p，先不改写电荷交叉项，得

    ∂t(r^p|Z|²)−∂r(c r^p|Z|²/2)
      +r^(p−1)(pc−r c_r)|Z|²/2
      =−r^p Re[(iea_r+c_r/r)Ψ conjugate(Z)]。      (F3)

其电场项正好是 r^p a_r Q_r=−b r^(p−2)Q Q_r；幅度项是 −r^(p−1)c_r (|Ψ|²)_r/2。因此

    ∂t E_p^dens+∂r J_p+K_p=0，
    E_p^dens=r^p|Z|²，
    J_p=−c r^p|Z|²/2+b r^(p−2)Q²/2
                         +r^(p−1)c_r|Ψ|²/2，
    K_p=r^(p−1)(pc−r c_r)|Z|²/2
        −(b r^(p−2))_r Q²/2−(r^(p−1)c_r)_r|Ψ|²/2。 (F4)

没有冻结电场，没有取绝对值丢掉 Maxwell 抵消。eQ 交叉项换成了真实电磁边界和体项；不能直接删除它们。

## FAR03.3：任意固定 eM 的足够远区积分正性

**逻辑 PROVED（实际全时间远区估计）；证据 ANALYTIC；审计 INTERNAL_AUDIT。** 固定 0<p<2，设

    η=4M/R₀， K²=4+64e²M²，
    η≤min{1, p/16, p(2−p)²/96,
                   (2−p)/[2(6+(32+640e²M²)/p)]}。 (F5)

R₀ 还大于初始标量支撑；总可增大 R₀ 满足 F5，不要求 eM 或 eQ 小。

**完整代数与估计。** 写 x=m/r、q=Q/r、y=φ=Ψ/r、U=Z、h=U−y=rφ_r。对 F4 的 K_p 同时代入径向 Einstein/Maxwell 约束，精确得到

    2K_p/(b r^(p−1))
      =[p−2(p+1)x]|U|²+2(3−p)x|y|²−|h|²|y|²
       +q²[(2−p)+2Re(U conjugate(y))−(6−p)|y|²
                                      +|h|²|y|²]
       +2q Q_r |y|²，
    Q_r=e r Im(y conjugate(U))。                 (F6)

这里 q²|U|² 与 b_r 产生的 −q²|h|² 的主部已抵消；若分别粗估它们，会错误地要求 eM 小。用 x≤M/R₀、|y|²≤η、q²≤K²，并令

    Λ=8|e|M^(3/2)/sqrt(R₀)， Λ²=16e²M²η，

则 e r|y|³≤Λ，且

    −|h|²|y|²≥−2η|U|²−2η|y|²，
    2q²Re(U conjugate(y))≥−(p/8)|U|²−(8K²η/p)q²，
    2q Q_r |y|²≥−(p/8)|U|²−(8Λ²/p)q²。

丢弃非负的 2(3−p)x|y|² 和 q²|h|²|y|²，F5 支付全部损失，故 F6≥(p/2)|U|²+((2−p)/2)q²−2η|y|²。由 F1、R₀≥4M 有 b≥exp(−1)>1/3。最后一个负项用真正有内端项的 Hardy：

    ∫_R₀^∞r^(p−1)|y|²dr
      ≤4/(2−p)²∫_R₀^∞r^(p−1)|U|²dr
                      +2R₀^(p−2)|Ψ(t,R₀)|²/(2−p)。 (F7)

F7 的无穷端项先对每个有限 t 使用 BOND02 的 Ψ 有界及 Z=O_t(r⁻²)，再取 r→∞；内端不能省。于是

    ∫K_p dr≥(p/24)∫r^(p−1)|Z|²dr
       +(2−p)/12∫Q²r^(p−3)dr
       −2η R₀^(p−2)|Ψ(t,R₀)|²/(2−p)。           (F8)

F4 的无穷端 J_p 对任意有限 T 一致趋零（p<2）；不能从这里推时间无穷的极限。令 E_p(t)=∫_R₀^∞r^p|Z|²dr，积分 F8，保留 r=R₀ 的真实 J_p，再只丢弃其负的 Z² 项并用 c_r≤2M/R₀²，得所有有限 T 的统一常数估计

    E_p(T)+(p/24)∫₀^T∫_R₀^∞r^(p−1)|Z|²drdt
      +(2−p)/12∫₀^T∫_R₀^∞Q²r^(p−3)drdt
    ≤E_p(0)+(R₀^(p−2)/2)∫₀^TQ(t,R₀)²dt
      +M[1+8/(2−p)]R₀^(p−3)∫₀^T|Ψ(t,R₀)|²dt。 (F9)

这是实际非线性带电外区估计，常数不随 T 变，也不预设最终 Q 或 RN。F1/F2 只保证右侧至多 O(T)；这不足以得到全时间衰减或 BOND02.8 的 E_ε。这里 Z 是径向导数，F4 的无穷端通量为零，不是 |F′|²。若再乘非减时间权 w(t)，积分右端还增加 ∫w′E_p；空间 r^p 本身不支付时间权，也没有自动产生辐射能量控制。

## FAR03.4：静态库仑库的反驳审计与质量带权平衡

**逻辑 PROVED（精确平衡/路线限制）；证据 ANALYTIC/EXACT_ALGEBRA；审计 INTERNAL_AUDIT。** 用完整系统的精确 RN、φ=0、b=1、Q=Q_*≠0 作反驳控制：F4 给

    J_p(R₀)=Q_*²R₀^(p−2)/2，
    ∫_R₀^∞K_p dr=Q_*²R₀^(p−2)/2。

两者随时间同样累积，E_p 和所有标量通量均为零。若把电磁内边界删除后仍主张 F8 的正体积分，就在这个实际精确外区上矛盾。RN 仅用于恒等式审计，不充当新种子的未来演化。

同样，对真实质量流 J^r=−m_t，有

    m_t=−r²b⁻¹|D_tφ|²+r²f Re(D_tφ conjugate(φ_r))，
    ∂t m_r+∂r J^r=0， lim_r→∞J^r=|F′|²。

定义 E_ext=M_B−m(t,R₀)≥0、j₀(t)=−m_t(t,R₀)。对任意正 C¹ 时间权 w，在有限时间窗严格有

    ∫₀^T w|F′|²dt+w(T)E_ext(T)
      =w(0)E_ext(0)+∫₀^T w j₀dt+∫₀^T w′E_ext dt。 (F10)

无权质量只控制 j₀ 的有符号原函数，不给其带权绝对通量。E_ext 含静态库仑库：

    E_C=∫Q²/(2r²)dr， E_s=∫r²f|φ_r|²/2 dr， E_ext=E_C+E_s。

对精确 RN，E_C=Q_*²/(2R₀)>0，j₀=0；F10 的增长终端项恰好与 ∫w′E_C 抵消。既不能把这个静态库当辐射，也不能在绝对估计中同时扔掉终端项与它的补偿。

有限时间的 BOND02 光滑紧化足以微分 E_C（尾 Q_t 有界），故合法扣除后为

    E_C′=∫Q Q_t/r² dr， Q_t=cQ_r−e Im(Ψ conjugate(D_tΨ))，
    ∫₀^T w|F′|²dt+w(T)E_s(T)
      =w(0)E_s(0)+∫₀^T w j₀dt+∫₀^T w′E_sdt
                                                    −∫₀^T w E_C′dt。 (F11)

F11 的库仑功没有符号。不能省略它，也不能把 a_r=−bQ/r² 当成 −Q/r²；进一步对势分部必须连同 b 的导数一起处理。本轮未取得该项的全未来可积界。

## FAR03.5：审计范围、失败记账与下一关键义务

| 声明 | 逻辑 | 证据类型 | 审计及范围 |
|---|---|---|---|
| F1/F2 实际世界管幅度/电荷一致界 | PROVED | ANALYTIC | INTERNAL_AUDIT；AF 锚定来自已经证明的有限时间实际 I⁺；不含晚时极限 |
| F3/F4/F6 精确抵消 | PROVED | ANALYTIC / EXACT_ALGEBRA | INTERNAL_AUDIT；全约束代入，含 b_r、Q_r |
| F5–F9 远区积分正性 | PROVED | ANALYTIC | INTERNAL_AUDIT；大 R₀，无小 eM；真实边界未关闭 |
| F10/F11 带权质量/标量能平衡 | PROVED | ANALYTIC / EXACT_ALGEBRA | INTERNAL_AUDIT；有限时间等式，不给一致 T→∞ 上界 |
| 删除静态电磁内边界仍得正时空库 | REFUTED | EXACT_RN_CONTROL | 精确实际电真空外区已反驳；不反驳 Goal A |
| 仅以无权内边界能量控制带权辐射 | REFUTED（外区黑箱主张） | ANALYTIC_LINEAR_REFERENCE_CONTROL | 任意延迟的自由出射紧支撑脉冲能量相同，带权能量无界；不是实际带电塌缩反例 |
| 实际 E_ε、Q_f、视界参数一致和 RN | OPEN | 缺少所需全未来证据 | 不能从 F9 的 O(T) 界或 F11 的恒等式升级 |

最后一个外区反控制可取 Minkowski r≥R₀ 的 Ψ=H(t−L)，H∈C_c^∞((0,1))、H′非零。无权内/外辐射能量都是 ∫|H′|²，与 L 无关；对 w=(1+t)^(1+ε)，带权辐射至少 (1+L)^(1+ε)∫|H′|²。任意延迟也保持世界管幅度的一致界。这严格排除缺少时间矩/内部演化信息的外区输入主张；不能排除从完整 Cauchy 数据或内部 PDE 获取这些信息。脚本中的多项式脉冲只是精确积分对照；C∞ 主张依靠上述解析构造。

研究结果改变下一步：远区 r^p 主部正性不再要求未知的最终电荷或小 eQ；**首要缺口转为库仑库扣除后的实际全时间内区供能/幅度控制**。下一轮先从 F11 与 Maxwell 时间式推导带完整 b 导数的库仑功分解，并尝试以实际全域动量流 MOR01 的边界/体项支付。若保留不可闭合的时刻权或世界管迹，要明确登记，不能重复使用 F9 的 O(T) 预算。该步骤仍须服务于原端点与同一三分支，不接受只证明任意形成解有有限窗外区。

[核验代码](verify_far_zone_rp.py)及[报告](FAR_ZONE_RP_CHECKS_2026-10-23.json)检查独立波式、Maxwell 完成、完整约束体密度、Hardy 常数、RN 静态余额、时间权库仑余额与延迟脉冲对照。程序不认证全局解析估计、实际 PDE 演化或 A1–A6。
