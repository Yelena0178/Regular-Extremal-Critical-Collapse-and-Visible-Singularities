# 目标 A 持续研究

**2026-10-18 同步快照**：[本轮结果及验证范围](SYNC_PROGRESS_2026-10-18.md)。全局阈值路线已推进至 A-EXIT08：外向 AF 初值、有限外条带及内侧迹预算、加权导数障碍、BV 迹与单锥约束控制。完整未来传播、同一条临界曲线及三分支终态仍未证明。

最终目标：[ACCEPTANCE.md](ACCEPTANCE.md)。本目录从 2026-10-16 开始；基础仓库 main 的起点提交为 3d5bf6bc40d4c3f1d66f2a7d5eaf3fd1a2e57643。既有 23 份证明和历史快照不改写。

**当前主线已变更（2026-10-17）**：按用户要求转为 [全局阈值优先](GLOBAL_THRESHOLD_ROUTE.md)，先研究迟时色散出口、形成侧估计及其分界，再选择能实现这些条件的初值族。脉冲扫描、末端匹配和局部证书不再作为默认推进方向。新记录给出质量电荷差的精确输运预算及外部定理适用范围；尚无新的全局存在性结论。下述候选材料保留为既有成果。

最新的不同构造见 [从开启段充电与无限尾两条路线](ALTERNATIVE_CHARGED_CANDIDATES.md)：两个 C∞ 旋转脉冲 (a,ω)=(1/5,8)、(3/10,4) 已有 2048 格整锥有理约束证书，固定 e=3/5 且由确切电荷积分定义 R。完整脉冲矩形的 48/96/192 网格 E0 筛选在 u>0 采样点均有正出射膨胀，终点稳定在约 0.05189084、0.06175235。二维实际解尚无严格误差；横向 jets 非零，旧 AF 实现稿不能直接套用。另有显式 Bessel 指数尾约束方案及其数值失败记录，没有将它当成实际事件视界或全局终态。

**目标 A 仍未证明。** 2026-10-17 更新：原 R=5 固定早期形状的小参数路线已有条件性陷俘排除，见 [A-TRANSFER01](THIN_ONSET_PARAMETER_TRANSFER.md)。新的固定 e=3/5、R=10、Φ=7/10、ρ=1/8 候选已有连续参数约束预算、精确光滑电荷根与预穿轴有限矩形的全域无陷俘证书；前两阶横向匹配给局部隐函数定理延伸，见 [A-NEW01/02](NEW_SHAPE_CONSTRAINTS.md)。穿轴后仅有 E0 探索。没有外部独立数学审查，完整 AF Cauchy 实现、全未来估计、真正临界曲线与三分支终态仍未完成。以下较早条目的限制按其当轮日期阅读。

后续推进：[A-CHG01](CHARGED_CHARACTERISTIC_METHOD.md) 给带电十二实变量系统、五个精确约束/Einstein 恒等式和有限充电区域的 E0 比较；有限 β 的两个较大根因采样 H 失正被拒绝，较小根仍无光滑根盒。分段单侧迹恢复固定内点的近二阶残差下降，但充电端点有尚未认证的负膨胀信号。[A-AF01](AF_OUTER_EXTENSION.md) 给外环带的 AF 尾延拓；[A-AF02](PAST_COLLAR_AND_AF_REALIZATION.md) 再用过去薄带的两情形估计给出实际光滑匹配种子到完整 AF 初值的非有效内部构造。该证明稿未经独立复核，尚无指定成员和共同常数的有效认证，更未证明极端终态或临界性。

进一步筛选见 [充电高阶比较](CHARGED_SCREEN_REFINEMENT.md)：R=10 的负膨胀 E0 信号在 Lobatto 方法中再次出现，R=11/12/14 的正值尚未得到稳定余量。十二变量向外舍入核已通过精确有理交叉检查，实际全域证书仍缺。[A-CHG02](CHARGED_FINITE_DOMAIN_STABILITY.md) 给出 r、κ 一致范数与 θ 的 L² 范数下的有限域转移接口，用于将未来经认证的 C0 参考结论转给光滑根；它不补出缺失的参考解证书。

[冻结锥证书推进](FROZEN_CHARGED_CERTIFICATION.md)：四分量入流边界的完整有理误差已通过；修正误差半径提议器后，开启和充电两段共 18432 单元的实际区间压缩通过，关断段预算仍失败。该参考不是光滑端点根，尚不能认证其完整未来或严格陷俘。[A-CHG03](CHARGED_U_CONSTRAINED_FORMULATION.md) 的八实分量沿 u 输运改写已通过四个精确约束传播恒等式，尚未运行新布局的全域证书。

## 本轮成果与作用域

| 材料 | 本轮取得的内容 | 尚未取得 |
|---|---|---|
| [A-AF02](PAST_COLLAR_AND_AF_REALIZATION.md) | 退化端点的未陷俘过去薄带估计；规则中心空间球与外侧环带连接；实际光滑匹配种子存在时的非有效 AF 实现及有限锥嵌入证明稿 | 独立数学复核、指定成员有效常数、临界曲线和三分支全局终态；不是数值 AF 认证 |
| [A-CHG01](CHARGED_CHARACTERISTIC_METHOD.md) | 带电约束传播和共形 Einstein 方程的精确代数；RN/FLRW 比较；新形状有限 β 两阶求根与充电域 E0 筛选 | 正平滑根盒、带电全域严格误差、修复脉冲及中心的实际未来、三分支全局终态 |
| [A-AF01](AF_OUTER_EXTENSION.md) | 一般角向外曲率下的精确约束 ODE；具有明示小量级的外环带可延拓为完整 AF 尾；两阶端点 jets 提供局部外侧量级 | 相容实际内侧 Cauchy 球、整体未陷俘与未来依赖域嵌入；不是完整 AF 实现 |
| [A-NEW01/02](NEW_SHAPE_CONSTRAINTS.md) | 新 R=10 形状的有理约束预算、光滑电荷根与同一早段的 18048 单元无陷俘证书；两阶横向匹配的局部解析延伸 | 显式修复参数阈值、中心穿越及充电未来的严格误差、完整 AF Cauchy 实现与 A1–A6 |
| [A-INC01](INCOMING_CONSTRAINT_FAMILY.md) | 非零径向动量、径向相位产生电荷、rφ 入射准备的 Cauchy 约束构造；小幅度全局正则与固定 X⁶ 光滑依赖的直接证明；最优小幅度相位频率及固定壳宽的电荷效率界 | 候选的实际未来、色散或形成、真正临界端点 |
| [A-INC01-B](EXACT_INITIAL_BUDGET.md) | 固定 bump 的线性屏障给全体 \|a\|≤2、\|ω\|≤1/4 的全半径 Δ≥32/851；小幅度 \|a\|≤1/8 另有更强界及明确正电荷成员 | \|a\|>2 样本的全半径认证、任何未来结论 |
| [A-TAIL01](BONDI_TAIL_OBSTRUCTION.md) | 在明确额外 Bondi 连续性假设下，正质量端点迫使迟发辐射质量缺失 m*、尾族不紧、耗散时间趋无穷；给有限半径到 Bondi 连续性的充分接口 | 本系统实际候选的 Bondi 提取连续性、非一致全局色散估计 |
| [生成器](incoming_family.py) / [复算入口](verify_research.py) | 固定 e=3/5、固定平坦中心和 AF 外尾；原始 Hamiltonian/Gauss/动量约束交叉检查；四档网格；Gauss 反号与漏掉 K 的拒绝检查；共轭和零幅度基准 | 该初值入口的严格浮点误差包络及任何未来结论 |
| [A-EVOL01](POLAR_EVOLUTION.md) / [有限时间演化](polar_evolution.py) | 同归一化的极坐标面积半径约化；平直解析波穿轴、RN 电真空环、全耦合四档网格与独立质量/电荷传播检查；中心 Taylor 迹和错误电势符号拒绝 | 严格 PDE 误差、穿越视界、完整 I⁺、全未来与终态 |
| [A-EVOL02](AREAL_SHIFT_EVOLUTION.md) / [径向 shift 演化](areal_shift_evolution.py) | 保留同一 Cauchy 数据；动态 lapse 和正则中心交错网格；RN 穿视界环、两种切片弱场的中心固有时比较；谐切片带电样本的数值双负膨胀 | 实际陷俘认证、完整适定性、误差包络、真正形成与临界性 |
| [A-HYP01](HARMONIC_PRINCIPAL_SYMBOL.md) | 谐切片正半径约化的显式特征变换与正定对称化；变换在 W=z 的视界处不退化；27 组 Fraction 代数复算 | 原点、非局部约束强范数、边界、完整 PDE 适定性与长期控制 |
| [A-GEO01](CAUSAL_COMPLETENESS.md) | 球对称全部未来因果测地线完备的几何判据及 L006 小数据适用接口；有限参数下的有界、反复折返和逃向无穷三种情形逐一排除；最大未来发展识别 | 完整 I⁺、全部点逃逸到该 I⁺、未知临界端点附近的控制 |
| [A-RET01](RETARDED_CAUCHY_BOUNDS.md) | Gauss 与有限区间 Hardy 给全时间电荷界；迟时 Cauchy 内部质量/电荷衰减；明确的零 Bondi 终态充分接口 | 实际光学函数与坐标延迟标签的比较、Bondi 极限存在及完整 I⁺ |
| [A-KL01](KL_INTERFACE_AUDIT.md) / [精确复算](verify_causal_algebra.py) | 更正原 L006 的 (12.3)–(12.4) 引用；依赖无循环核对；双零 Hessian 与独立 RN 有效势的 Fraction 多项式恒等式及错误变体拒绝 | 外部独立数学复核；代数检查不认证分析证明 |
| [A-NULL01](SMALL_DATA_NULL_INFINITY.md) | 实际零线的截止带退出和迟时比较；非退化光学流；带电输运改进使电荷可积；有限切片的 C² 共形边界、完整 I⁺及零 Bondi 终态 | 独立数学复核；这些小数据估计不能无证明地跨越到正质量端点 |
| [A-SD01](SMALL_DATA_DISPERSION.md) | 对 L002/L006 的充分小幅度族逐项连接全部完整色散条款；共同标签中中心时间为固有时 | 该安全区与真正极端临界族的连接；不是任意 X⁶ 小数据定理 |
| [A-HOR01](SMOOTH_HORIZON_CONSTRAINT_SEED.md) | 固定 e=3/5、终端面积半径5的光滑零锥约束种子；256格有理区间认证连续参数余量；解析平滑化及中值定理保留精确终端电荷 | 横向标量 jets、完整 RN 匹配、实际未来中心、Cauchy 三分支 |
| [A-SCH01](SCHNEIDER_2026_INTERFACE_AUDIT.md) | 纳入 Schneider 2608.23355v1 的剖面；按 D001 独立重推约束及带电横向复残差，区分其 C0 结果和目标 A | 不以其有限时间拼接界限制所有渐近极端解；不直接采用未匹配的协变式或一阶修复条件 |
| [A-JET01](FIRST_TRANSVERSE_JET.md) | 后置固定相位弱脉冲不添纵向电荷，带电交换子给可逆的横向复方向；C1 参数平滑化与隐函数定理给充分小辅助参数下的精确三实根及 H>β/8192 | 显式 β0/η0 与指定根盒、高阶横向 jets、完整 RN、全中心发展及真正临界族 |
| [A-JET02](SECOND_TRANSVERSE_JET.md) | 从 D001 推出二阶横向复残差及闭合系数；证明零标量延续段保留首个未消去的横向 jet；线性化 RN 特征检验显示一阶条件不自动控制二阶条件 | 实际光滑候选的二阶残差、增广求根及高阶匹配；不是非线性反例或目标 A 禁止定理 |
| [A-JET03](TWO_PULSE_SECOND_JET.md) | 两个分离的固定相位脉冲保持末段零直接电流；独立的零阶/一阶矩给五实残差 Jacobian 非零，IFT 消去前两阶横向标量残差；E0 五维求根及有限 β 正性失败均保留 | 显式光滑根盒、三阶及更高阶匹配、全中心/AF 实现和三分支全局终态 |
| [A-EVOL03](NEUTRAL_CHARACTERISTIC_METHOD.md) | 同模型中性双零方程；解析平直波穿轴与全耦合收缩 FLRW 比较；独立约束、中心质量系数及失败轴线版本对照 | 非线性稳定性、连续 PDE 误差及实际候选未来；FLRW 不渐近平坦 |
| [A-SCREEN01](NEUTRAL_CAUSAL_SCREEN.md) | 精确真空帽将早期筛选化为正半径特征矩形；冻结 β=0.003 C0 输入及已分辨平滑开启实验的三档同点双负膨胀；另一固定 e 的 R=10 形状在有限预穿轴窗口未见同类信号 | 原 η 平滑层、严格陷俘、原光滑族排除、新形状光滑电荷根及横向匹配、全局无陷俘和临界性 |
| [A-GOUR01](RATIONAL_GOURSAT_CERTIFICATION.md) | 不在出射零膨胀处退化的六变量有理输运；精确约束缺陷传播；逐单元 Banach误差管道命题；独立强场数值及条件性有理单元核；完整有限域应用见 A-GRID01 | 中心、AF 端及矩形外的未来；条件性单元核不能单独给出实际陷俘 |
| [A-BOUND01](ONSET_BOUNDARY_CERTIFICATION.md) | 冻结平滑开启数据的 6147 个子区间有理包络；整条出射边 r、κ、θ 对指定 Hermite 多项式的严格误差界及实际半径正下界；已供 A-GRID01 使用 | 原 η 种子转移、完整 Cauchy 实现；整边证书本身不提供二维结论 |
| [A-GRID01](FULL_TRANSPORT_GRID_CERTIFICATION.md) | 在明确 IEEE-754 算术假设下核验全部147456个单元，得到冻结 ε=0.05 数据的有限矩形实际解及局部严格陷俘球；终点2m−r>0.21144 | 原 η 光滑根转移、完整 AF Cauchy 实现、原候选正式排除、事件视界及三分支全局终态 |

不将本轮命题编号混入原 L001–L023；新的命题和方法仅在本目录编号。

## 实际复算

Python 3.11+，仅标准库：

    python research/goal_a/verify_research.py
    python -O research/goal_a/verify_research.py

输出为 [RESULTS_2026-10-16.json](RESULTS_2026-10-16.json)，记录源文件 SHA-256、参数、观测收敛阶、原方程残差和拒绝检查。它不是 PDE 或目标 A 证书。

本次实际环境：Windows，Python 3.13。默认壳 [1,21]、幅度 0.5、频率 0.2；四档步数 256/512/1024/2048。RK4 观测阶约 4.0006、3.9989；最细网格 Hamiltonian/Gauss/动量残差约 4.56×10⁻¹³、2.23×10⁻¹⁴、2.17×10⁻¹⁹，入射准备有限差分残差约 2.52×10⁻¹¹。误差为浮点实验观测，未提供严格区间上界。

固定 bump 的相位最优频率估计约 0.2375643，小幅度 ADM 比上确界估计约 1.262816。扫描得到的比值是**初始 ADM 比**，不能据此分类终态或声称发现极端黑洞。

## 有限时间演化的实际复算

安装 [固定 NumPy 版本](requirements-evolution.txt)，运行：

    python research/goal_a/verify_evolution.py
    python -O research/goal_a/verify_evolution.py
    python research/goal_a/explore_polar_family.py

这些入口分别生成 [演化基准报告](EVOLUTION_RESULTS_2026-10-16.json) 和 [有限参数探索](FINITE_TIME_SCAN_2026-10-16.json)。初值标准库复算入口不变。

实际基准：128/256/512/1024 四档网格；解析平直波比较到 t=12，包含中心穿越；全耦合弱场比较到 t=8。全耦合观测收敛阶约 2.005、2.002；最细网格独立质量/电荷传播残差约 1.25×10⁻⁷、1.34×10⁻⁷。固定 dr 扩大外半径的场差约 3.29×10⁻¹⁴，时间步减半差约 4.97×10⁻¹²。这些都是经验数值，不能当作严格边界无影响或 PDE 误差证书。

新增中心检查发现并修正了普通中点求积的缺陷：首格 Q/r³、m/r³ 的领先系数会低估 25%，即使 Q、m 本身看似收敛。现在精确积分 r² 权重，并对独立制造数据的中心 Taylor 迹验收二阶收敛；电势梯度残差也恢复二阶。

探索入口保留整个有限振幅样本和计算停止，不给“色散/黑洞”标签。有限半径质量、电荷不写成 Bondi 终态。极切片 Δ>0 图中初始及后续坐标球未陷俘的事实，不能用于排除该图未来之外的黑洞或陷俘区。

实际探索包含七个单网格样本：ω=0.2、a=0.25/0.5/1/2 的 t=24 演化；以及 a=2、ω=0/0.1/0.2 的 t=40 尝试。后两项 ω=0、0.1 分别在最后完成时间约 37.92、38.92 触及 Δ<0.05 的人为极坐标停止条件；ω=0.2 到 t=40 的最小观测 Δ 约 0.0791。这些没有强场网格误差包络，不构成真正色散/黑洞 bracket，更不认证阈值或终态。它们具体说明：下一步必须解决规则视界规范中的继续演化，不能在当前图中无限延长积分来替代。

## 径向 shift 与主符号：新增结果

实际复算入口：

    python research/goal_a/verify_areal_shift.py
    python -O research/goal_a/verify_areal_shift.py
    python research/goal_a/verify_harmonic_symbol.py
    python research/goal_a/explore_shifted_strong.py

最后一个为较长的三档强场试算。输出分别为 [规范基准](AREAL_SHIFT_RESULTS_2026-10-16.json)、[主符号精确代数](HARMONIC_SYMBOL_RESULTS_2026-10-16.json)、[带电强场探索](SHIFT_STRONG_SCAN_2026-10-16.json)。

首次同点规范离散在线性 Minkowski 子系统上产生随 1/h 增长的模，已经拒绝；其强场负号和停止不作为物理证据。现在 W 在半格，lapse 在节点，球对称散度与梯度满足体积加权伴随关系。对应平直半离散规范子系统有能量恒等式；谱检查实部约为舍入量。这不证明完整非线性数值稳定。

穿越 RN 外视界的正半径环检查呈二阶收敛；两种切片都与原极切片按中心固有时比较 |φ|。原 1+log 非线性控制样本仍发生计算停止，保留其具体时间和状态，不将其直接归因为规范激波或时空奇点。谐切片样本则可继续到数值双负膨胀。

具体强场探索固定 e=3/5、a=2、ω=0.2、外半径 80、t=37.4、面积半径 r=0.9375。512/1024/2048 格上 θ₊ 约为 −0.06346/−0.03920/−0.02369，θ₋ 均严格负，空间度量仍正定。独立质量传播残差约 0.0142/0.00428/0.00115；最细总质量漂移约 0.000716。强场数据仍属 E0：负号随加密变化明显，没有连续解的严格误差，不能升级为实际陷俘证书，也不能据 L001 正式淘汰候选。不能将同一球面的局部质量/电荷当作最终黑洞参数。

分析引理 A-HYP01 给出谐切片正半径主符号的完整实特征分解。重合的规范/物质特征之间，同速度耦合为零，显式变换仅含 z² 分母，在 1−2m/r=0、z=W>0 处有限。它提供下一步正半径能量估计的入口；未覆盖原点、边界和非局部约束积分的强范数估计。

## 小数据几何接口：新增结果

    python research/goal_a/verify_causal_algebra.py
    python -O research/goal_a/verify_causal_algebra.py

结果记录在 [CAUSAL_ALGEBRA_RESULTS_2026-10-16.json](CAUSAL_ALGEBRA_RESULTS_2026-10-16.json)。复算比较双零 Hessian/角动量给出的精确面积半径加速度与 RN 独立有效势，保留 Hawking 质量与 RN 参数的区别；通过只支持有限代数。

A-GEO01 用全局规则图、统一未陷俘余量、内区可积 Christoffel 和全时间电荷界补上 L006 的非径向因果线缺口。证明覆盖有任意固定角动量的类时线和零线。A-RET01 的电荷界先由 Gauss 积分得到，不依赖测地完备，故两份证明没有互相假定结论。

固定 s=2/3 时，迟时内部电荷界为 O((1+q)^(-1/3))，质量界为 O((1+q)^(-4/3)) 加电磁 O((1+q)^(-5/3)) 项。A-RET01 本身仍是 Cauchy 片估计；后续 A-NULL01 用实际零线证明 q 的迟时下界，并另证每个 Bondi 极限存在，才推出 Mf=Qf=0。不得省去这些中间步骤或交换极限。

## 实际零无穷远与小数据完整色散：新增证明链

    python research/goal_a/verify_null_infinity_algebra.py
    python -O research/goal_a/verify_null_infinity_algebra.py

精确结果见 [NULL_INFINITY_ALGEBRA_RESULTS_2026-10-16.json](NULL_INFINITY_ALGEBRA_RESULTS_2026-10-16.json)。检查独立展开带电波算子，验证 Maxwell 的径向/时间约束兼容、径向 Einstein 标量项抵消、RN 电真空专门化和 Bondi 通量的时间归一化；错误交换子、电势号数与漏掉 Maxwell 输运项均须被拒绝。脚本不认证分析证明。

A-NULL01 首先处理 R* 的时间依赖截止：实际迟发零线在 t≥8(1+u) 后永久离开过渡带，不能把全时间的 log(t)/t 项直接积掉。随后利用真正的早期外侧电真空出射面，将 h=∂r(rφ) 改进为 O(r^(-2))，才使 Qr 可积。有限 u 切片上有 C² 共形度量和 C¹ 电磁场延拓；无界单位 Bondi 时间及每点出射逃逸给完整 I⁺和空黑洞区。

A-SD01 将此结果与 A-GEO01 的全部因果完备及规则紧域衰减合并，提出 L002/L006 小幅度族的完整色散内部定理；未宣称该曲线区间是 X⁶ 中的开集。它以 Minkowski 为幅度零点，不能当作目标 A 的正质量临界端点。当前最重要的剩余任务已转向把合法候选真正连接到非零质量极端终态。

## 固定有限耦合的零锥种子：新增结果

    python research/goal_a/verify_horizon_seed.py
    python -O research/goal_a/verify_horizon_seed.py

[报告](HORIZON_SEED_RESULTS_2026-10-16.json) 将有理区间证书与 C0 基准的浮点横向诊断分开。固定 Phi=1/2，s∈[3/20,17/100]；连续区间上的初末入射预算 H 均严格大于1/1024。固定宽度平滑化的 H1 误差由解析估计控制，中值定理给 e=3/5、r=Q=5 的精确终端零锥约束根，平滑后 H>1/2048。它不需要随参数更换长度单位。

该新种子有 Minkowski 顶点相容帽，但并非已构造的完整正则中心发展或 RN 时空拼接。D001 的实际波输运还要求一个复残差 J=0；纵向全阶平坦不能代替这个横向条件。三档浮点诊断提示 C0 基准的终端 |Duφ| 约0.009496，未给其严格误差，也未数值分辨平滑层。后续 A-JET01 在更小的辅助参数范围给出该三实残差的局部可解证明，而非直接将原种子判作 RN。

## 一阶横向匹配：新增解析机制

    python research/goal_a/explore_first_jet.py
    python research/goal_a/verify_first_jet.py
    python -O research/goal_a/verify_first_jet.py

探索另需 [固定 SciPy/NumPy 版本](requirements-shooting.txt)。[E0 探索](FIRST_JET_EXPLORATION_2026-10-16.json) 和 [一致性检查](FIRST_JET_CHECKS_2026-10-16.json) 保留原始残差、约束采样最小值、独立 Gauss/波输运积分、容差加密及 Jacobian 差分。它们不认证正平滑宽度的实际根盒。

A-JET01 将早期充电段放在 [0,β]，后段加入 βWg 的固定相位光滑脉冲。后段电荷电流精确为零，半径反馈为 O(β²)，横向复残差则有非零的 O(β) 电磁响应。缩放后极限 Jacobian 行列式为
3k'(s0)·(e∫g/4)²≠0；还用移动接点的固定域拉回，证明平滑化后端点映射的 C1 收敛，补足直接套隐函数定理会缺的参数接口。

内部存在论证给充分小正 β、η 下 Q(1)=5、Duφ(1)=0 的光滑零锥数据，并保留 H>β/8192。β=0 是辅助退化映射，不是实际时空或 X⁶ 中的临界端点。尚无显式 β0、η0 或任一指定数值点的区间认证；报告中的 β=0.01/0.003/0.001/0.0003 仅为 C0 早段浮点实现。高阶横向匹配、中心未来及目标 A 仍未完成。

## 下一步与不得绕开的验收

[A-JET03](TWO_PULSE_SECOND_JET.md) 以两个脉冲替换原末段，给出充分小 β、η 下同时消去 Q/R−1、D_uφ、D_u²φ 的内部解析存在论证。这个新族尚未完成三阶匹配或完整 RN；早期陷俘风险也仍需筛查。`verify_two_pulse_second_jet.py` 记录精确有限代数及 E0 五维求根：β=0.003 虽残差小，但 H 采样失正；较小 β 的正采样值仍不是连续区间证书。

路线审查 [A-JET02](SECOND_TRANSVERSE_JET.md) 明确了另一项独立缺口：一阶匹配不自动兑现二阶横向匹配，后者有 (J22) 的可计算复积分条件；精确 RN 拼接需要高阶机制。该条件尚未在原光滑根上认证，不能据此宣布其失败。精确有限时拼接也不是最终验收的额外要求；若改走渐近 RN 路线，须直接兑现其全未来收敛范数。有限域筛选的作用仍是淘汰候选，不能替代构造三分支。

本轮新增必要筛选见 [A-SCREEN01](NEUTRAL_CAUSAL_SCREEN.md)。实际入口：

    python research/goal_a/verify_neutral_characteristic.py
    python -O research/goal_a/verify_neutral_characteristic.py
    python research/goal_a/explore_neutral_onset.py
    python research/goal_a/explore_neutral_shapes.py
    python research/goal_a/check_neutral_screen.py

原 R=5 形状在固定点的 θout 随 N=192/384/768 约为 −0.872772/−0.872789/−0.872793，θin约−5.5924。中心仍精确真空，轴线近似次数为零。结果仅 E0，局部残差下降不能代替全域误差，也未将原极薄 η 层数值分辨。优先把该正半径矩形做成连续解认证，再决定是否值得继续此形状的高阶 jets。R=10、Φ=0.7、ρ=1/8 的另一固定耦合形状只通过了有限预穿轴窗口的数值筛选，尚无光滑约束根或 RN匹配证书。[一致性报告](NEUTRAL_SCREEN_CHECKS_2026-10-16.json) 保留未认证标签及源文件哈希。

后续 [A-GOUR01](RATIONAL_GOURSAT_CERTIFICATION.md) 已把连续误差接口写成逐单元可核验的不等式，并证明满足这些不等式会给有限矩形内的实际解。独立有理输运的384²样本复现原菱形演化的同点信号。192²/384²的早期普通浮点管道预测使用**假定**边界误差；48²/96²失败也保留。新增 [A-BOUND01](ONSET_BOUNDARY_CERTIFICATION.md) 对冻结 ε=0.05 数据的整条出射边给出实际误差界：r 约7.28e-6、κ 约2.29e-6、θ 约1.76e-3；报告保存精确有理上界。随后 A-GRID01 已将这些界贯穿全部二维单元，原光滑候选的转移仍未完成。

[已证边界输入的二维预测](CERTIFIED_BOUNDARY_TUBE_FORECAST_2026-10-16.json) 核对了出射 Hermite 数据哈希及入射真空多项式完全匹配。384² 浮点传播预测覆盖全域，假想 2m−r 下界约0.2115；二维残差及传播仍是 E0，不是实际陷俘证书。实际入口为 `certify_onset_boundary.py`、`verify_onset_boundary_kernel.py` 和 `explore_certified_boundary_tube.py`，均位于本目录。

2026-10-17 的 [A-GRID01 完整证书](FULL_TRANSPORT_GRID_CERTIFICATE_2026-10-17.json) 已通过全部147456个单元及严格误差传播，最小不等式余量大于9.86e-10，实际终点2m−r>0.21144、κ>0、ν<0。这是在文档列明的 binary64 算术假设下取得的计算机辅助局部陷俘证书，超出了早期 E0 预测；其输入仍仅为冻结平滑中性实验，不能宣布原 η 候选已被排除。复算入口为 `verify_interval_transport_grid.py`（亦以 `-O` 运行）和 `certify_transport_grid.py`。

    python research/goal_a/verify_neutral_transport.py
    python -O research/goal_a/verify_neutral_transport.py
    python research/goal_a/explore_transport_tube.py
    python research/goal_a/verify_rational_transport_cell.py
    python -O research/goal_a/verify_rational_transport_cell.py

1. **初值层**：全体 \|a\|≤2 的明确初值族已有连续半径正屏障；\|a\|>2 的扫描成员仍需认证，浮点近似误差也须与解析初值存在分开。支持/单位固定；Δ 失正仅拒绝这份坐标数据。
2. **演化层**：径向 shift 的弱场规范比较和带电双负膨胀探索已取得；下一步是实际有限因果域的连续 PDE 误差及坐标/约束控制。A-EVOL02 §6 已写出把 r,m,W 包络升级为实际陷俘的明确充分条件，当前尚无这些输入。
3. **候选层**：在幅度、固定相位与剖面方向寻找合法的色散/形成 bracket；不能预设单调性，不能用初始或有限时无陷俘认证色散。
4. **全局层**：负侧完整色散、端点与正侧真正形成和精确 RN 终态仍是最终目标主体。A-TAIL01 要求允许迟时预算退化；不能用与正质量端点矛盾的一致尾假设把它“解决”。

第 1 项仅剩较大幅度扩展，不应无目的完善它而推迟第 2–4 项。小数据完整色散已有新增内部证明链；需要独立核对 A-NULL01 的光学及边界论证。有限耦合端点入口是 A-HOR01 与 A-JET01/JET03。A-GRID01 已完成冻结平滑实验的有限因果域认证，下一步须兑现原光滑参数转移及相容 AF Cauchy 接口，才能对原候选使用 L001；通过必要筛选后再推进高阶匹配和全局预算。不能把局部 jets 当完整 RN 或临界性。A-HYP01 的非局部/中心/边界接口也仍缺。不能将小数据结论延用到未经控制的大幅度族。用户最终目标只在 ACCEPTANCE 的全部门槛闭合后完成。

## 外部来源核对

2026-10-16 实时核对 [Kehle–Unger 2402.10190](https://arxiv.org/abs/2402.10190) 的摘要：三分支严格存在定理为 Einstein–Maxwell–Vlasov；不能移植成带电标量全局定理。

实时核对 [Gundlach–Martel 2511.14874v3](https://arxiv.org/abs/2511.14874v3) 的版本记录与摘要，并定点阅读 [v2 §V.5](https://arxiv.org/html/2511.14874v2#S5.SS5)：其正则中心数值方法和电荷符号变化提示可作为演化基准，不提供本项目全部族的禁止或存在定理。未复核全文证明，未导入其代码。

本轮新增核对 [Schneider 2608.23355v1](https://arxiv.org/html/2608.23355v1) 的有限耦合三段特征剖面、Definition 1、相关定理及 Remark 2/9，并以 PDF 对照。A-SCH01 记录归一化与横向交换子接口；仅从其形状启发独立构造 A-HOR01，不把低正则拼接或有限时间下界升级为目标 A 的全局结论。

## GitHub 同步

本轮成果使用 [草稿 PR #5](https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/pull/5) 持续同步，分支为 codex/goal-a-research-2026-10-16。后续修改先核对实际分支头和已提交文件，避免依赖本地旧 Git 引用。目标保持进行中。
