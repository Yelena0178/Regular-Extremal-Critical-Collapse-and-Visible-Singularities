# 研究成果与证据范围

研究截至 2026-10-27 / R31；本页于 2026-10-28 按成果而非回合整理。完整 Goal A 仍 OPEN。逐轮叙述见[原研究首页归档](research/goal_a/PROGRESS_ARCHIVE_2026-10-28.md)，以下汇总不升级原稿的逻辑或审计状态。

## 10-23 至 R31 的主要成果

| 成果 | 逻辑状态与作用域 | 证据 / 审计 | 尚缺什么 |
|---|---|---|---|
| [MARG02 有限边际刚性](research/goal_a/FINITE_MARGINAL_RIGIDITY.md) | PROVED：指定实际无陷俘区域的局部命题；最终视界应用 CONDITIONAL | ANALYTIC / EXACT_ALGEBRA；INTERNAL_AUDIT | 因果身份与全局终态 |
| [ESC01 中心逃逸](research/goal_a/CENTER_ESCAPE_CHARACTERISTIC_EXTENSION.md)、[BOND02 Bondi 桥](research/goal_a/ACTUAL_BONDI_COMPLETENESS_BRIDGE.md) | PROVED：稿内指定种子及外区命题；不是目标族全参数结论 | ANALYTIC / EXTERNAL_THEOREM；INTERNAL_AUDIT，列明源前提 | 强 RN 终态、极端端点和三分支连接 |
| [RN20 静态冻结](research/goal_a/STATIC_GEOMETRY_FREEZING_AND_RN_ROBIN.md) | 实际 A/D/K 输入下的有限窗冻结；充分远固定 RN 的物理 Robin 低频结论 | ANALYTIC，有限复模态对照；INTERNAL_AUDIT | 实际输入与全频控制 |
| [SPACE21 Green 公式](research/goal_a/FINITE_RADIUS_RN_GREEN_AND_LOCAL_BODY.md) | 完整有限半径公式及明确输入下的紧径向体源控制 | ANALYTIC / EXACT_ALGEBRA，有限 ODE；INTERNAL_AUDIT | 无穷源区由后续 CONE22 处理；真实边界未消失 |
| [CONE22 无限径向体源](research/goal_a/INFINITE_RADIAL_RN_BODY_TRANSFER.md) | 指定双尺度源包络下的低频全空间幅度与辐射导数界 | ANALYTIC，有限积分和加密对照；INTERNAL_AUDIT | 实际 A/D/K、真实迹和高频 |
| [LOCAL23 未来局部化](research/goal_a/FULL_RN_FUTURE_LOCALIZATION.md) | 实际质量预算与完整 RN 核给扩张过去窗局部化；未来 W 为滤波功能 | ANALYTIC / EXACT_ALGEBRA，有限 ODE / 积分；INTERNAL_AUDIT | 过去 W 点态尾、实际 A/D 闭合及强视界终态 |

所有配套脚本与报告在[专题导航](research/goal_a/README.md)和[完整索引](research/goal_a/FILE_INDEX.md)。完整依赖与失败尝试见[R31 检查点](research/goal_a/RECOVERY_CHECKPOINT.md)。以下保留早期成果及其当时范围；例如 A-CAUS01 的原缺口须结合后续 ESC01 / BOND02 阅读。

## 后续成果（2026-10-16 至 10-22）

10-22 构造推进：[A-DIR01](research/goal_a/CHARGE_PRESERVING_DIRECTION_FAMILY.md)以固定电荷分布的方向族隔离中心聚焦机制，给出精确初始通量分解及整族全半径初值正性证明稿。1024段有理求积包围 Q∞，结合线性约束比较得到全部 d∈[−1,1] 的 f>10⁻⁷；浮点初始化误差与未来演化均未认证。10次有限筛选保留负样本、停止和两档加密；较强出射成员的中心样本改善伴随核心质量流失，尚无正质量长期滞留证据。完整代码、证书、回归和复算入口见该稿。

10-22 后续：[A-AXIS01 正则轴线接口与中心筛选](research/goal_a/REGULAR_AXIS_CAUCHY_SCREEN.md)给出条件于光滑解的九个轴线极限、三个带电领先系数，以及含中心的特征演化实现。已知 FLRW/复相位 FLRW/Minkowski 基准通过有限加密检查。补入中心后，同一 s=1001/1000 候选在三档网格出现强负 λ，位置不在旧外部楔区；因此下述“保留新候选”的判断已被更新。实际陷俘、失稳是否对应奇点、三分支全局终态均未证明。

10-22 新增：[规范 Cauchy 有限未来筛选及参数延伸](research/goal_a/CANONICAL_CAUCHY_EARLY_SCREEN.md)。同一 A020 自由函数路径 s=1001/1000 的初值全半径正性经区间屏障认证，并由约束比较覆盖 [0,1001/1000]。候选 t≤4 的512/1024/2048步最小 λ 约为 3.63e−4、3.34e−4、3.27e−4；t≤8 单档也无负样本。附初始化、Cauchy 演化、基准测试、完整有限记录及历史源码。演化为 E0，不能升级为连续未来、临界点或三分支证明。

基础衔接：[10-11 至 10-12 阶段审查](reviews/README.md)中，16 实维消元材料记录了冻结有限八阶 jet 端点系统的内部根认证；后续共同 Cauchy、条带、强范数与发展接口仍为条件性推进，阶段 3 整体未闭合。该有限根证据不等于目标 A 的临界基点。

| 材料 | 新增内容 | 适用边界 |
|---|---|---|
| [研究专题与完整证据导航](research/goal_a/README.md) | 初值、演化基准、小数据链、有限耦合种子、横向匹配、带电特征与区间工具 | 逐项区分解析稿、有限代数、E0 与有限域证书 |
| [A-GRID01](research/goal_a/FULL_TRANSPORT_GRID_CERTIFICATION.md)及[A-TRANSFER01](research/goal_a/THIN_ONSET_PARAMETER_TRANSFER.md) | 冻结 ε=0.05 中性实验 147456 单元认证；原 R=5 小参数路线条件性筛选 | 列明 binary64 假设；不是所有原光滑种子或完整未来的认证 |
| A-EXIT01–23，见[研究首页](research/goal_a/README.md) | 完整出射约束至中心分析、I⁺、零 Bondi、局部二阶衰减及共同支撑类相对稳定出口 | 依赖前置分析和待复核适定性接口；不识别正质量端点 |
| [A-AF03](research/goal_a/AF_REALIZATION_WITH_TRANSVERSE_FLUX.md) | 对两个旋转种子保留非零横向场的完整 AF 初值非有效实现稿 | 有限特征片段实现不证明真正形成或 RN 终态 |
| [A-AF04](research/goal_a/ROTATING_CAUCHY_AF_IMPLEMENTATION.md) | 两个旋转来源候选的具体光滑自由函数及中心到 RN 外尾约束数值重求解 | E0；改变原种子，尚缺连续半径误差及重构后未来筛选；ADM 参数不作为终态 |
| [A-AF05](research/goal_a/ROTATING_AF_CONTINUOUS_BARRIER.md) | 两组冻结规范数据各经 3,555,328 个闭区间屏障检查；完整 AF 及整条合法收缩路径有共同 f>3/10000 | 依赖列明算术假设；不保留原特征种子，不认证未来筛选、临界点或三分支 |
| [A-CAUS01](research/goal_a/MARGINAL_SEED_CAUSAL_INTERFACE.md) | 条件性黑洞区、外部定理意义的完整 I⁺及正几何质量下界；提出逃逸见证接口 | 依赖 A-AF03；初始片全部逃逸仍缺 |
| [A-END01](research/goal_a/FINITE_MARGINAL_TAIL_GATE.md) | 末端非零横向通量与曲率终态门槛 | 若边缘锥成为最终事件视界才阻碍目标 RN 收敛，因果身份未证 |
| [A-PATH01](research/goal_a/CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md) | 初始未陷俘的约束收缩路径及首个色散边界候选 | 依赖小数据链和陷俘上端；是否在 D 外、极端 RN 与右侧终态仍缺 |

完整后续文件见 [FILE_INDEX](research/goal_a/FILE_INDEX.md)。**这些进展没有完成目标 A；目标 B–D 也仍开放。**

下文保留截至 2026-10-09 的基础成果叙述；其中“下一次”指当轮任务，当前优先级以 [ROADMAP](ROADMAP.md) 为准。

## 全中心控制

L012 在特殊精确极端接合输入上建立固定宽度的全时间实际内侧控制。L013 进一步从实际散射迹得到

\[
\alpha(b,t)/t^2\longrightarrow h_b>0,\qquad \alpha=-\nu/\Omega^2,
\]

并以实际初始标量非平凡性判别正增长系数。L015 单独处理近视界零场空隙。
L014 将外边增长经入射 Raychaudhuri 传到实际深中心域：对足够晚的 T，

\[
\iint_{t\ge T}\Omega^2\,dUdt\le\frac{2R}{h_bT}.
\]

若截面仍终止于正则中心，另有电磁截面积分与加权半径界。轴线满足

\[
\frac{d\tau_\Gamma}{dt}=\frac{1}{2\alpha_\Gamma},\qquad
\tau_\Gamma(t)-\tau_\Gamma(T)\le\frac{1}{h_bT}.
\]

这是条件性的有限未来固有长度结论。它不证明曲率发散，也不排除跨 Cauchy 边界延拓。

## 中心曲率与深中心判据

L016 给实际光滑正则中心的精确关系

\[
K_\Gamma=\frac{20}{3}|D_\tau\phi|^4,\qquad D_\tau\phi=4\alpha_\Gamma T_\Gamma.
\]

曲率问题因此需要控制乘积 \(\alpha_\Gamma T_\Gamma\)，不能只看坐标导数衰减。
L017 给入射电荷—能量障碍；L018 给实际中心出射线的有限区间谱判据；L019 给内部边际球的局部刚性。入射能量下界不能未经波输运估计直接变成出射聚焦下界。

## 固定领先剖面及精确证书

L020 固定 K=8、n=88、σ=1/20，八个 Laplace 矩精确为零。领先参数约为 0.5045578902627281；脚本认证有理区间 \(1/2<\lambda_0<51/100\)。这个领先参数不是已冻结的有限振幅成员的耦合质量积。

J 的精确整数 Bernstein/Descartes 证书覆盖全半线，证明恰一次负到正变号；辅助形成核下界超过 \(2^{-854}\)。L021 指定光滑截断、矩修复和周期族，全族周期核下界超过 \(2^{-855}\)。

函数与截断的分析论证仍要人工复核；有限代数脚本的成功不自动认证每个光滑估计。

## 第一周期陷俘机制

L023 在原有限阶非线性端点分支存在、整条初始入射锥选为 Minkowski、并可调用 An–Lim 带电陷俘形成接口的条件下，对实际第一周期得到

\[
\eta_0\ge1-e^{-T}-b\delta,\quad d_0\le e^{b\delta T}-1,
\]
\[
\epsilon\le(\mu\delta C_0/\rho_0)^2,\qquad
\Delta v\le2b\delta(e^T-1).
\]

固定周期后，质量比有正下界，而正确中心归一化的半径宽度、电荷比和仿射宽度可随分支变小。
原稿用这些估计满足外部定理的严格余量，从而在指定充分长分支得到实际严格陷俘球。结合 L001，这一实现不能充当完备色散侧临界基点。

原稿显式几何门槛 \(m\ge2^{2104156}\) 极为保守。它只认证几何充分条件；非线性端点提升另有尚未有效化的门槛，不能把该数值解释为已经求出的成员。
门槛脚本给出质量比余量至少 15543/32768，明确不认证非线性零点或数值时空。

## 下一次可升级的结论

冻结具体有限振幅端点根，固定整锥及共同 Cauchy 实现，再取得陷俘保留的光滑修复预算，才能把指定分支结论升级为具体光滑种子的认证。
一般临界存在、曲率端点和可见性均须另外证明。
