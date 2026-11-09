# 极端临界塌缩与可见奇点：仓库审读报告

审读快照为 2026-11-08，报告整理于 2026-11-09。审读对象为公开仓库 [Regular-Extremal-Critical-Collapse-and-Visible-Singularities][repo] 的主分支及 [PR #5][pr]。

**核心结论。** 仓库已经建立若干解析障碍，并对一套中性特征数据认证了有限时空区域内的严格俘获球。最新带电候选的演化与聚焦诊断可以复现，证据属于探索数值。完整 Goal A 仍为 **OPEN**，目前没有同一条初值曲线上的色散、正质量极端黑洞与带电亚极端黑洞三分支证明。可见大曲率、单解可见曲率奇点及其稳定性也仍是研究目标。

## 1. 版本、PR 与提交历史

| 对象 | 冻结版本与审读结果 |
|---|---|
| 主分支 | **3d5bf6bc40d4c3f1d66f2a7d5eaf3fd1a2e57643**，22 个提交 |
| PR #5 | **53681923d0fc83e574f8ec42d82d2b87b54d265c**，相对主分支新增 30 个提交，开放、草稿、未合并 |
| 全部 PR 与讨论 | 查询全部状态只返回 #5。已关闭 PR、普通评论、正式 review、行内 review comment 均为 0 |
| 文件变更 | 688 个文件，新增 706,134 行，删除 571 行。新增行主要来自生成的 JSON 等研究输出 |
| PR 正文版本 | 正文仍对应 **ef62243** 的 26 个提交、658 个文件。审读以实际分支头为准 |

审读覆盖 README、模型与验收定义、L001–L023 全部主证明稿、历史形成接口与有限阶根认证、PR 中的主要研究链、核心求解与认证源码、测试、提交历史及全部文件变更清单。生成数组、JSON 与日志按类型、来源、哈希及可复算结果核对。形式化重证每条引理与重跑全部历史实验超出本次核验范围。仓库内的阶段自审属于内部证据，GitHub 上的独立同行评议记录为空。[冻结版 README][readme] · [PR 与文件差异][pr-files] · [本地版本记录](../source/PROVENANCE_2026-11-08.json)

| 时段 | 提交中实际发生的变化 | 审读判断 |
|---|---|---|
| 10 月 10–12 日 | 固定模型与目标，整理 23 篇主证明稿，进行有限阶根认证并审查形成接口 | 奠定解析框架，留下光滑化、完整初值和未来演化条件 |
| 10 月 16–21 日 | 构造有限幅度约束数据，推进特征演化、中性矩形区间证明与色散出口估计 | 局部 PDE 结论开始有可核验的误差包围 |
| 10 月 22 日附近 | 引入包含正则中心的数值演化，重查先前只看外区的候选 | 中心附近出现负膨胀信号，先前外区无俘获的判断范围过窄 |
| 10 月 28 日至 11 月 1 日 | 整理 R31，补充 RN 尾部接口、传播方向分离和固定电荷幅度对照 | 候选筛选更能区分机制，尚无经认证的临界端点 |

本地项目在该快照之后另有 SHAPE、VAR 和 ASYM 系列记录，其状态与依赖见本地项目索引。本报告的 GitHub 结论以冻结版本为界。[本地状态](../STATUS.md) · [本地研究索引](../INDEX.md)

## 2. 模型、几何量与验收目标

系统是四维、球对称、渐近平直的 Einstein–Maxwell–无质量带电复标量场模型。耦合固定为 $e=3/5$，无磁荷和宇宙学常数。依仓库约定，

$$
S=\int\sqrt{-g}\,[R-F_{ab}F^{ab}-2g^{ab}D_a\phi\,\overline{D_b\phi}]\,d^4x,
\qquad D_a=\nabla_a+ieA_a.
$$

双零形式为 $g=-\Omega^2\,du\,dv+r^2d\omega^2$，记 $\nu=\partial_u r$、$\lambda=\partial_v r$。在通常外部区域 $\nu<0<\lambda$，严格俘获球要求 $\nu,\lambda<0$。Hawking 质量 $m$ 与带电重整化质量 $\varpi$ 的关系是

$$
m=\frac r2(1+4\Omega^{-2}\nu\lambda),\qquad
\varpi=m+\frac{Q^2}{2r},\qquad
1-\frac{2\varpi}{r}+\frac{Q^2}{r^2}=-4\Omega^{-2}\nu\lambda.
$$

正则中心要求 $Q,m=O(r^3)$。初始切片必须单端、空间完备、渐近平直、满足全部约束，且初始正半径球面膨胀异号。聚焦与输运由下列方程耦合。

$$
\partial_v(\lambda/\Omega^2)=-r\Omega^{-2}|D_v\phi|^2,\qquad
\partial_vQ=e r^2\operatorname{Im}(\phi\,\overline{D_v\phi}),
$$

$$
\partial_u\partial_v r=-\frac{\nu\lambda}{r}
-\frac{\Omega^2}{4r}\left(1-\frac{Q^2}{r^2}\right).
$$

电荷输运需要标量场，而标量场也使零测地线聚焦。这是构造高电荷且控制有限时俘获的主要约束。[模型定义][model]

RN 视界半径为 $r_\pm=M\pm\sqrt{M^2-Q^2}$。极端终态要求 $M=|Q|>0$，此时两根合并，表面引力 $(r_+-r_-)/(2r_+^2)$ 为零。

| 条款 | 同一条初值曲线必须满足的条件 |
|---|---|
| A1 | 在固定强拓扑 $X^6$ 中构造 $C^1$ 曲线 $p\mapsto\Psi_p$，每个成员光滑，固定耦合、尺度和规范 |
| A2 | 所有 $p<0$ 的解未来因果测地线完备，具有完整且正确识别的 $\mathcal I^+$，全部点可见，局部趋于 Minkowski，$M_f=Q_f=0$ |
| A3 | 所有 $p\ge0$ 的整个初始切片都在 $J^-(\mathcal I^+)$ 中，事件视界后来从实际正则中心事件起源，且 $\mathcal I^+$ 完整 |
| A4 | 外部与规则视界邻域收敛到同一个 RN，度量达到 $C^2$、电磁场达到 $C^1$，视界极限与 Bondi 终态一致。$p=0$ 时 $M_f=\lvert Q_f\rvert>0$，$p>0$ 时 $0<\lvert Q_f\rvert<M_f$ |
| A5 | 在所指定强拓扑下证明 $\Psi_0\in\partial\mathcal D\cap\partial\mathcal B_{\rm form}$ |
| A6 | 适定性、参数依赖、中心与无穷远控制、外部定理假设、数值到实际解的转移全部兑现 |

初值在强拓扑下连续依赖，首先控制有限时间。若色散侧在每个有限 Bondi 时间 $U$ 的质量满足 $M_{B,p}(U)\to M_{B,0}(U)$，则从 $U$ 到终态的剩余辐射量 $E_p(U)=M_{B,p}(U)-M_f(p)$ 满足

$$
\lim_{p\uparrow0}[E_p(U)-E_0(U)]=M_f(0)>0.
$$

这给出了正质量跳跃的具体要求：色散侧有一份正量级的能量要在越来越晚的时间放出。有限 Bondi 时间的连续性和这种非一致晚时行为仍需在实际解族中证明。[目标 A 验收契约][acceptance]

## 3. 主证明稿的内容与适用范围

| 证明组 | 成果 | 适用边界 |
|---|---|---|
| L001–L006 | 严格俘获稳定性、仿射聚焦、曲率和电荷预算 | 有限时局部结论及部分全局接口 |
| L007–L012 | 特殊视界数据附近的条带、楔形区域与曲率控制 | 依赖指定横向导数条件 |
| L013–L016 | 指定内部区域的中心寿命与中心曲率公式 | 中心寿命有限与可见曲率发散之间仍有证明任务 |
| L017–L019 | 尖锐径向电荷代价、谱判据、边际刚性 | 需要实际射线、径向端点条件或两侧无俘获邻域 |
| L020–L023 | 显式剖面、代数认证、光滑化条件和长周期障碍 | 领先阶或有限阶对象，以及特定路线的条件性排除 |

证明索引、形成输入和相关文献位置可在冻结快照中互查。[L001–L023 索引][proofs] · [形成输入审计][inputs]

### 严格俘获与临界候选排除

在有限时间光滑区域出现的严格俘获球，在适用的强拓扑连续依赖下对小扰动稳定。结合 Penrose 定理的假设，这样的邻域与未来零测地线完全相冲突。因此，若在某个候选的实际解中认证到严格俘获，即可把该候选排除出所要求的色散边界。边际球面 $\lambda=0$ 需要另行分析，因为严格符号的开放性在这里消失。[L001][l001]

### 电荷与聚焦的定量竞争

沿实际出射射线，记入口膨胀 $\Lambda_0=(\lambda/\Omega^2)_{\rm entry}$，定义

$$
F=\int r\Omega^{-2}|D_v\phi|^2\,dv,\qquad
F_a=\int r\Omega^{-2}(\partial_v|\phi|)^2\,dv,\qquad
H=\int r^3\Omega^2|\phi|^2\,dv.
$$

将标量场分解为幅度与相位，电荷电流只依赖相位的协变变化。由 Cauchy–Schwarz 与 Raychaudhuri 方程，

$$
|\Delta Q|^2\le e^2H(F-F_a),\qquad
\frac{\lambda}{\Omega^2}=\Lambda_0-F.
$$

对无负膨胀的每个射线前缀，$F\le\Lambda_0$，故 $|Q|\le|Q_0|+|e|\sqrt{H(\Lambda_0-F_a)}$。冻结已有射线后，这给出电荷容量的必要上界。实际修改相位会改变场方程及几何输入，容量优化的可实现性还要由耦合系统证明。[L005][l005] · [射线预算分析][focus]

L017 对连接正则中心且 $\phi(R)=0$ 的相应径向截面给出

$$
\int_0^R r|D_r\phi|^2\,dr\ge \frac{4j_{0,1}}{|e|R^2}|Q(R)|,
\qquad j_{0,1}\simeq2.4048256.
$$

该常数在指定径向函数类内最佳。若要由此得到普适的耦合—质量阈值，还需要相应径向能量的统一上界。[L017][l017]

### 有限边际与曲率诊断

在两侧都无俘获的光滑开邻域内，若 $\lambda=0$，则 $\lambda$ 取局部极小，$\partial_u\lambda=\partial_v\lambda=0$。代入混合方程与 Raychaudhuri 方程得 $|Q|=r$、$D_v\phi=0$。因此，近零膨胀数值本身不足以识别这种边际结构。纯晚时渐近边际或外部单侧邻域需要各自的论证。[有限边际刚性][marginal]

沿规范化仿射径向零向量 $L$ 有 $\operatorname{Ric}(L,L)=2|D_L\phi|^2$。在规则中心，令 $\chi=|D_\tau\phi|^2$，则

$$
R=-2\chi,\qquad R_{ab}R^{ab}=4\chi^2,\qquad
R_{abcd}R^{abcd}=\frac{20}{3}\chi^2.
$$

要建立仓库所说的可见曲率奇点，需要实际解中可追踪的曲率发散、有限仿射参数与通向正确识别的 $\mathcal I^+$ 的因果控制。面积半径坐标导数放大和数值迭代中断只能作为定位问题的线索。[L003][l003] · [L016][l016]

### 早期根认证与长周期障碍

L020–L021 使用有理运算和 Bernstein 证书验证领先阶剖面，包括正性和失败对照。后续历史审查将有限阶非线性端点条件约化为 16 个实变量，在指定大参数和解析界下验证 Krawczyk 型局部根。参数 $2^{2104156}$ 属于构造尺度。有限阶认证仍须跨越两个量词与对象上的缺口：对每个有限阶 $k$ 构造一份数据，并不提供满足所有阶条件的同一份光滑数据。端点根还需兑现完整初值与全局演化。

L023 给出特定路线的反向约束。若实际有限阶分支、完整 Minkowski 入射锥和 An–Lim 判据的接口成立，足够长的第一周期可导致严格俘获，从而由 L001 排除该实现作为目标临界点。套用外部定理时应核对质量集中量与脉冲宽度的归一化。该结论的量词限于这里的长周期方案。[L020][l020] · [L023][l023] · [An–Lim 原文](https://arxiv.org/abs/2005.04090v1)

## 4. 已复算的有限区域 PDE 认证

认证针对一套冻结的中性特征数据。它以共享的精确二进制有理 Hermite 近似表示整个矩形，用 Bernstein 形式包围单元残差，计算区间 Jacobian 界，并沿入流边传递误差。每个单元逐分量核验

$$
M_i-b_i-h_i\left(\delta_i+\sum_jL_{ij}M_j\right)>0.
$$

其中 $b_i$ 是边界误差界，$\delta_i$ 是残差上界，$L_{ij}$ 是非线性导数上界，$M_i$ 是误差半径。实际接受条件使用向外舍入的区间下界。证书依赖正确舍入的 IEEE-754 基本运算、渐进下溢、正确的 nextafter 和 Python 整数及 Fraction 运算。

独立复算通过了 $384^2=147\,456$ 个单元，最小严格余量为 $9.864805152953781\times10^{-10}$。端点包围为

$$
0.63931819\le r\le0.66215306,\qquad
\nu\le-0.81562001,\qquad 2m-r\ge0.21144096.
$$

此处 $Q=0$，光学变量 $\kappa=-\Omega^2/(4\nu)>0$，故 $\lambda=\kappa(1-2m/r)<0$。这在认证矩形内建立了实际中性解的局部严格俘获球。证书保留三个未兑现项：向原始种子的转移、完整渐近平直 Cauchy 实现，以及 Goal A。这份证书的对象也与 11 月 1 日的带电中心演化不同。[全矩形认证与复算命令][grid] · [证书输出][grid-json]

## 5. 最新带电候选、数值源码与证据等级

11 月 1 日的幅度实验固定传播方向参数和初始电荷分布，用 $a_s=s a_0$、$\omega_s=\omega_0/s^2$ 改变幅度和相位频率。Gauss 约束给出

$$
Q_s'(r)=e\omega_s r^2a_s^2=e\omega_0r^2a_0^2.
$$

因为正则中心边值相同，整个初始 $Q(r)$ 保持不变。能量项变为 $S_s=s^2G+s^{-2}P$，约束几何重新求解。初始总电荷约为 $5.76843018$，各组 ADM 质量不同。

| $s$ | 初始 ADM 质量 | 1024 步全域首负膨胀时间 | 主诊断射线 $\lvert Q\rvert/r$ | $F_a/F$ | 必要电荷容量指标 |
|---:|---:|---:|---:|---:|---:|
| $3/4$ | 5.893406 | 9.697266 | 0.145118 | 85.53% | 0.150917 |
| $1$ | 6.673542 | 14.355469 | 0.118471 | 85.16% | 0.127080 |
| $3/2$ | 7.603513 | 14.736328 | 0.238349 | 19.55% | 0.250713 |

全域首负样本与主射线预算可能位于不同点，各组主射线也不同。高幅度组的必要容量指标约提高为基准的 1.97 倍，主要变化来自可用聚焦预算。该指标度量局部冻结条件下的必要容量，终态 $Q_f/M_f$ 需要全局演化确定。三组都有负膨胀浮点信号。低幅度组后来在更新中失败，因而那次运行在停止前之外没有物理分类。

512 步的独立重放与冻结高幅度归档的首次负样本、最坏样本和诊断记录完全一致。首次负样本位于 $t=14.736328125$，$\lambda\approx-7.86256\times10^{-5}$。这说明该浮点结果可重放。由于候选缺少覆盖实际带电演化的误差包围，首负信号目前仍属候选筛选证据。[固定电荷幅度报告][amp] · [候选探针源码][probe]

正则中心求解器使用特征网格、隐式迭代与轴线专门处理，在中心附近对质量、电荷的退化源项采用不同积分权重。FLRW 和曲线坐标 Minkowski 提供了解析基准，带电 RN 提供离中心的电真空检验。动态、非零电荷且包含正则中心的独立精确基准仍缺。实现中某些小残差来自离散构造本身，评估其证明力需要区分独立检查、收敛比较与经认证的误差上界。[正则中心求解器][centered] · [带电基准核验][charged]

## 6. 全局终态尚需闭合的环节

1. **同一候选的依赖链。** 约束收缩路径可以提供从小数据到俘获端的连续路径，部分小数据色散与出射出口结论也已写成证明或接口。第一个离开色散集合的点还需要证明有正质量 ERN 终态、完整因果结构及右侧亚极端分类。用于这些结果的数据和假设目前没有在同一条曲线上全部兑现。
2. **实际形成与完整无穷远。** 特殊种子的中心逃逸与 Bondi 外区稿已经提供了局部或指定数据的进展。目标要求对同一曲线全部 $p\ge0$ 证明初始切片可见、事件视界从未来正则中心起源，以及实际 $\mathcal I^+$ 完整。
3. **晚时质量与电荷。** 在采用的规范中，若辐射场为 $\mathcal F(u)$，则 $M_B'=-|\mathcal F'|^2$，$Q_B'=-e\,\operatorname{Im}(\mathcal F\overline{\mathcal F'})$。有限能量只能控制 $\mathcal F'\in L^2$。例如令 $L=\log(\mathrm e+u)$，$\mathcal F=L^{-1/2}e^{iL}$，则 $\mathcal F\to0$ 且 $\int|\mathcal F'|^2du<\infty$，电荷通量仍可产生 $\log\log(\mathrm e+u)$ 型发散。这个边界通量例子表明还须利用耦合方程取得更强的相位或衰减控制。
4. **强 RN 收敛。** R31 的 Green 核、低频估计与未来局部化提供固定参考背景下的工具。实际耦合系统的高频、非线性误差、参考与实际几何的比较，以及规则视界邻域的强收敛仍需证明。
5. **可见曲率奇点。** Goal B 需要统一控制初值且在可见区域产生任意大的曲率。Goal C 需要在单个解中建立可见曲率发散。Goal D 需要指定拓扑下的一般性或稳定性论证。现有解析恒等式和数值线索距离这三项验收仍有各自的缺口。

相关路线、证明状态与条件可在下列冻结文档复查。[研究导航][goal] · [实际 Bondi 桥梁][bondi] · [RN 未来局部化][rn]

## 7. 与文献的关系及研究价值

Kehle–Unger 的带电标量场形成结果给出了研究极端形成的数学基础。仓库增加了固定强拓扑下同一曲线的三分支、完整因果身份以及所规定的强终态要求。带电 Vlasov 的临界极端形成工作提供临界边界的直接参照，移植到带电标量场仍需处理不同的物质方程与机制。[极端黑洞形成](https://arxiv.org/abs/2211.15742v2) · [Vlasov 临界塌缩](https://arxiv.org/abs/2402.10190v1)

Kauffman–Lindblad 的小数据结果适用于满足其正则性和小性假设的区域。靠近正质量临界候选的整个负侧需要单独的全局估计。固定 RN 背景上的带电标量场晚时研究可以提供线性输入，实际几何的尾部闭合还取决于非线性控制。[小数据适定性](https://arxiv.org/abs/2109.03270v2) · [固定 RN 晚时分析](https://arxiv.org/abs/2603.28861v1)

仓库目前最有独立研究价值的成果，是可检验的障碍定理、正则中心的电荷代价、以及有限域区间 PDE 方法。特别是中性矩形证书已经有明确的对象、误差、适用假设和端点判据，可以独立审查。最新带电候选的实验设计也更有解释力，因为它控制了初始电荷分布并重新解几何约束。

如以投稿为尺度，优先级应是选定一份数据并闭合一个可复核的命题，例如把带电候选的严格俘获信号提升为有限域认证，可靠排除该候选。若转向正向构造，则需要选定同一份数据，贯穿中心、实际外部、完整 $\mathcal I^+$ 与强终态。在这之前，扩大参数搜索只能增加线索。大型生成归档和滞后的 PR 正文也使同行较难看清哪些命题已闭合，适合以定理、假设和复算入口为单位组织投稿材料。

## 8. 复算记录与限制

下表记录 2026-11-08 冻结快照上的实际复算。此文件整理于次日，复用该次结果。

| 入口或检查组 | 结果与范围 |
|---|---|
| 导航更新检查、文件清单、导航链接、研究快照 | 通过。1,256 项文件哈希，18 个文档和 905 条链接，216 项不变的科学文件和 5 项声明的导航差异，55 份报告和 368 条回执 |
| 支持区出口、约束收缩、边际刚性、实际 Bondi 桥梁 | 对应核验脚本通过，作用域由各脚本及定理假设决定 |
| 正则中心与带电 Cauchy 核验 | 基准检查通过 |
| 有限半径 RN Green 核、无限径向体源、RN 未来局部化 | 各自的接口与计算检查通过 |
| 传播方向分离、幅度对照汇总 | 一致性检查通过。高幅度组的 512 步另行重放 |
| **python checks/reproduce.py --with-kernel** | 精确剖面、全局核与允许性证书、优化模式检查、充分阈值、失败剖面和篡改拒绝均通过 |
| **verify_interval_transport_grid.py** | 768 项有理数算术对照，及三个单元的 288 个精确 Hermite 系数核验通过 |
| **certify_transport_grid.py** | 完整中性矩形的 147,456 个单元及端点符号认证通过 |

原样在 Windows 运行主复现入口时，文本生成使用 CRLF，导致校验值与归档 LF 字节不匹配。在临时运行环境固定 LF 后通过，数学数据与源算法保持一致。部分脚本首次遇到 Windows 扩展路径与父目录引用的兼容问题，改用普通路径后通过。文件哈希核验检查材料的字节完整性，科学结论依赖各自的数学假设、误差证明和实际解范围。[冻结版复现说明][reproduce]

[repo]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities
[pr]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/pull/5
[pr-files]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/pull/5/files
[readme]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/README.md
[model]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/definitions/MODEL.md
[acceptance]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/ACCEPTANCE.md
[proofs]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/proofs/INDEX.md
[inputs]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/inputs/AUDIT.md
[l001]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/proofs/RECCVS_L001.md
[l003]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/proofs/RECCVS_L003.md
[l005]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/proofs/RECCVS_L005.md
[l016]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/proofs/RECCVS_L016.md
[l017]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/proofs/RECCVS_L017.md
[l020]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/proofs/RECCVS_L020.md
[l023]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/proofs/RECCVS_L023.md
[focus]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/TARGET_RAY_FOCUSING_REVIEW_2026-11-01.md
[marginal]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/FINITE_MARGINAL_RIGIDITY.md
[grid]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/FULL_TRANSPORT_GRID_CERTIFICATION.md
[grid-json]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/FULL_TRANSPORT_GRID_CERTIFICATE_2026-10-17.json
[amp]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/FIXED_CHARGE_AMPLITUDE_REVIEW_2026-11-01.md
[probe]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/probe_fixed_charge_amplitude.py
[centered]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/centered_cauchy_diamond.py
[charged]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/verify_charged_cauchy_diamond.py
[goal]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/README.md
[bondi]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/ACTUAL_BONDI_COMPLETENESS_BRIDGE.md
[rn]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/research/goal_a/FULL_RN_FUTURE_LOCALIZATION.md
[reproduce]: https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/blob/53681923d0fc83e574f8ec42d82d2b87b54d265c/REPRODUCE.md
