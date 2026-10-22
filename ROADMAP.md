# 下一步研究任务

本地任务更新：2026-10-22。主线为 [全局阈值优先](research/goal_a/GLOBAL_THRESHOLD_ROUTE.md)，最终标准见 [目标 A 验收](research/goal_a/ACCEPTANCE.md)。每项验收材料注明实际解、规范、区域、常数及依赖。

[中心筛选更新](research/goal_a/REGULAR_AXIS_CAUCHY_SCREEN.md)已补入晚期正则轴线数值更新，s=1001/1000 在三档网格均出现强负 λ，不再作为早期筛选通过候选。下一步应研究改变中心聚焦相关自由数据，或取得该有限负信号的连续陷俘证书；还需独立带电中心动态基准和带初始化误差的 PDE 控制。外部正样本不证明色散，中心负样本也尚未认证实际陷俘。继续保留全部结果并同步 GitHub，不启动额外审查。

## 当前优先任务

[A-AF04](research/goal_a/ROTATING_CAUCHY_AF_IMPLEMENTATION.md)已给出具体自由函数与约束 E0 实现；[A-AF05](research/goal_a/ROTATING_AF_CONTINUOUS_BARRIER.md)对两组冻结规范数据完成列明算术假设下的全半径及整条收缩路径正性认证。下一步应演化这些确切定义的 Cauchy 初值，或取得到原特征域的强范数转移；它们尚未继承原种子的边缘球或通过早期未来筛选，不能直接作为 P01 的陷俘上端。

| 优先项 | 现有入口 | 必须补足的证据 |
|---|---|---|
| P01 定位首个边界候选 | [A-PATH01](research/goal_a/CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md) | 兑现同一路径的小端色散与陷俘上端前提，定位候选并判定是否在 D 外；无有限规则陷俘不等于已形成极端黑洞 |
| P02 证明真正形成 | [A-AF03](research/goal_a/AF_REALIZATION_WITH_TRANSVERSE_FLUX.md)、[A-CAUS01](research/goal_a/MARGINAL_SEED_CAUSAL_INTERFACE.md) | 独立复核完整 AF 实现；提供初始中心逃逸见证并覆盖整片；区分定理意义 I⁺ 完整性和目标全部边界条款 |
| P03 识别极端终态与因果身份 | [A-END01](research/goal_a/FINITE_MARGINAL_TAIL_GATE.md) | 判定边缘锥是否为最终事件视界；证明目标范数中的 RN 收敛、Bondi / 视界终态一致及正质量精确极端性 |
| P04 核对完整色散出口链 | A-EXIT01–23，见[研究首页](research/goal_a/README.md) | 有限 Cauchy 适定性、中心与外区拼接、高阶范数和共同支撑类相对稳定性的所有前提；不能无证明延伸到临界端点 |
| P05 闭合同一曲线三分支 | [ACCEPTANCE](research/goal_a/ACCEPTANCE.md)、[尾部障碍](research/goal_a/BONDI_TAIL_OBSTRUCTION.md) | 固定强拓扑的同一 C¹ 约束曲线、负侧完整色散、端点真正极端形成、正侧亚极端 RN，以及真正边界身份 |

有限域证书、脉冲形状扫描与 jets 修复作为上述任务的按需工具；不再默认优先扩展它们。只改变保留边缘球的 AF 外尾不能提供色散负侧。

## 第七轮历史任务（2026-10-09）

以下 R01–R08 保留旧任务编号，用于追溯其当轮缺口，不表示当前仍全部未启动。有限端点根的历史内部认证、后续有限域证书及转移状态须结合 [研究首页](research/goal_a/README.md)、[阶段记录](research/goal_a/PROGRESS_ARCHIVE_2026-10-20.md) 和后续审查阅读。

| 编号 | 任务 | 验收条件 |
|---|---|---|
| R01 | 有效化有限振幅端点提升 | 明确参数范围、C¹ 余项、非退化界；认证 17 个实残差的一个具体根 |
| R02 | 冻结指定中心填充与共同实现 | 完整 Minkowski 入射锥、相容角点、共同 Cauchy 数据及有限依赖域 |
| R03 | 认证第一周期的实际输入 | 对冻结成员核对 L023 的质量、宽度、电荷、中心仿射归一化及存在域 |
| R04 | 给光滑修复保留预算 | 同一有限实际陷俘域的强范数稳定界、尾部和总误差小于其容差 |
| R05 | 独立审查 L023 | An–Lim 原定理量、归一化、电流符号接口、边际到严格陷俘和适定性逐项审核 |
| R06 | 独立审查全中心控制链 | L012–L015 的固定宽度量词、反向估计、零场空隙、实际域和轴线固有时 |
| R07 | 分类中心有限寿命端点 | 实际 αΓTΓ、趋轴曲率及指定正则性中的延拓；可见性另证 |
| R08 | 筛选新的临界候选 | 在固定尺度约束族中证明真正色散邻侧、黑洞侧及极端边界身份 |

R01–R05 旨在认证并筛掉一个指定实现，不应继续以证明该分支全深中心无陷俘为目标。
完整 A–D 与其他研究路线保留在 [原任务规格](proofs/ROUTES_AND_TASKS.md)。
