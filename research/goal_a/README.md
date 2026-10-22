# 目标 A：当前进展与专题导航

进展材料截止 **2026-10-22**。本目录自 2026-10-16 开始，基线为 main 提交 `3d5bf6b`。**目标 A 仍未解决**；现有解析稿未经外部独立数学复核。本页汇总本地材料，远端同步状态以 Git 提交为准。

[仓库地图](../../atlas-map.md) · [正式验收](ACCEPTANCE.md) · [当前任务](../../ROADMAP.md) · [完整文件索引](FILE_INDEX.md) · [复算说明](../../REPRODUCE.md) · [整理前阶段记录](PROGRESS_ARCHIVE_2026-10-20.md)

## 当前主线与最新进展

自 10-17 采用 [全局阈值优先路线](GLOBAL_THRESHOLD_ROUTE.md)：先研究完整色散出口、形成侧及边界，再识别极端性和同一条合法初值曲线。形状扫描、有限域证书与横向匹配保留为工具。

| 进展 | 已有内容与前提 | 未闭合项 |
|---|---|---|
| 10-20：[A-PATH01 约束收缩与首个边界](CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md) | 一般非零角向外曲率下保持全参数初始未陷俘的路径；接入既有小数据链和陷俘上端后，可选首个 ∂D 候选，其有限规则未来无严格陷俘 | 候选定位、是否在 D 外、真正形成、正质量极端 RN、紧邻右侧亚极端终态 |
| 10-20：[A-CAUS01 全局因果接口](MARGINAL_SEED_CAUSAL_INTERFACE.md) | 条件于 A-AF03 实现，外部定理给非空黑洞区、该定理意义的完整 I⁺及正几何 Hawking–Bondi 质量下界 | 初始中心逃逸见证、真正形成、目标全部边界与终态条款；保留边缘球仅改变 AF 外尾不能产生色散负侧 |
| 10-20：[A-END01 横向曲率终态门槛](FINITE_MARGINAL_TAIL_GATE.md) | 两个旋转种子的非零末端 D_uφ 有有理包络；若无陷俘边缘锥成为最终事件视界，其横向 Ricci 阻碍目标 C² RN 收敛 | 该锥的事件视界身份；尚非候选的全局排除 |
| 10-18：[A-AF03 保留横向回流的 AF 实现](AF_REALIZATION_WITH_TRANSVERSE_FLUX.md) | 两个从开启段充电的光滑旋转种子，不要求横向 jets 消失的非有效完整 AF 实现论证稿 | 有效共同常数、完整二维筛选、真正形成、终态与临界连接 |
| 10-18：A-EXIT01–23 出射出口与中心链 | 从完整出射壳约束推进到 I⁺、零 Bondi 两次极限、二阶局部衰减及共同支撑类相对稳定出口的内部论证 | 分析链独立复核、有限 Cauchy 适定性接口、连接正质量临界端点和形成侧 |

## 专题导航

2026-10-22 新增：[规范 Cauchy 有限未来筛选与参数延伸](CANONICAL_CAUCHY_EARLY_SCREEN.md)。新候选 A020_W8，s=1001/1000，取得[完整初值区间证书](ROTATING_AF_BARRIER_A020_W8_S1001_N4096_2026-10-22.json)，并在 t≤4 三档网格及 t≤8 单档有限楔区保留正 λ 样本。[初始化](canonical_cauchy_data.py)、[演化器](charged_cauchy_diamond.py)、[基准检查](verify_charged_cauchy_diamond.py)、[测试记录](CHARGED_CAUCHY_DIAMOND_CHECKS_2026-10-22.json)、[有限结果汇总脚本](audit_canonical_cauchy_screen.py)与[汇总记录](CANONICAL_CAUCHY_SCREEN_AUDIT_2026-10-22.json)均归档；未来结论仍是 E0，未认证连续无陷俘或三分支终态。历史源码及所有原始 JSON/NPZ 见完整索引。

2026-10-21 新增：[A-AF04 具体空间数据与 AF 实现](ROTATING_CAUCHY_AF_IMPLEMENTATION.md)把两个旋转种子的过去薄带接到光滑自由函数及完整空间约束重求解；[独立核验](verify_rotating_af_interface.py)与[报告](ROTATING_AF_INTERFACE_CHECKS_2026-10-21.json)覆盖转换恒等式、负 u 已知解比较、加密和独立质量变量复算。结果为 E0 新初值；连续半径认证、原种子转移、重构后未来筛选与三分支仍缺。

同日后续：[A-AF05 连续半径认证](ROTATING_AF_CONTINUOUS_BARRIER.md)将两组自由函数冻结为精确二进有理系数及理想平坦权重定义。每组 3,555,328 个闭区间通过[下屏障检查](certify_rotating_af_barrier.py)，在列明算术假设下得到全半径及整条收缩路径 f>3/10000，兑现这两组新初值的完整 AF 合法性；[独立测试记录](ROTATING_AF_BARRIER_CHECKS_2026-10-21.json)保留核验范围。早期未来筛选、原种子转移和三分支仍未完成。

| 主题 | 研究入口 | 代码与证据入口 / 范围 |
|---|---|---|
| 初值与尾部障碍 | [A-IC01](INITIAL_DATA_AND_TAIL_OBSTRUCTION.md)、[A-INC01](INCOMING_CONSTRAINT_FAMILY.md)、[连续半径预算](EXACT_INITIAL_BUDGET.md)、[A-TAIL01](BONDI_TAIL_OBSTRUCTION.md) | [初值生成器](incoming_family.py)、[约束和平衡律复算](verify_research.py)；初值预算不证明未来命运，尾部论证有额外连续性前提 |
| 有限时间演化与主符号 | [A-EVOL01](POLAR_EVOLUTION.md)、[A-EVOL02](AREAL_SHIFT_EVOLUTION.md)、[A-HYP01](HARMONIC_PRINCIPAL_SYMBOL.md) | [极坐标](polar_evolution.py)、[shift 演化](areal_shift_evolution.py)、[主符号核验](verify_harmonic_symbol.py)；数值基准与正半径代数 |
| 小数据完整色散 | [A-GEO01](CAUSAL_COMPLETENESS.md)、[A-RET01](RETARDED_CAUCHY_BOUNDS.md)、[A-KL01](KL_INTERFACE_AUDIT.md)、[A-NULL01](SMALL_DATA_NULL_INFINITY.md)、[A-SD01](SMALL_DATA_DISPERSION.md) | [因果代数](verify_causal_algebra.py)、[零无穷远代数](verify_null_infinity_algebra.py)；指定小数据分析链，不可直接推广到正质量端点 |
| 有限耦合与横向匹配 | [A-HOR01](SMOOTH_HORIZON_CONSTRAINT_SEED.md)、[A-SCH01](SCHNEIDER_2026_INTERFACE_AUDIT.md)、[A-JET01](FIRST_TRANSVERSE_JET.md)、[A-JET02](SECOND_TRANSVERSE_JET.md)、[A-JET03](TWO_PULSE_SECOND_JET.md) | [一阶](verify_first_jet.py)、[二阶](verify_second_jet.py)、[双脉冲核验](verify_two_pulse_second_jet.py)；有限阶 jets 不等于完整 RN 或终态 |
| 中性筛选与有限域认证 | [A-EVOL03](NEUTRAL_CHARACTERISTIC_METHOD.md)、[A-SCREEN01](NEUTRAL_CAUSAL_SCREEN.md)、[A-GOUR01](RATIONAL_GOURSAT_CERTIFICATION.md)、[A-BOUND01](ONSET_BOUNDARY_CERTIFICATION.md)、[A-GRID01](FULL_TRANSPORT_GRID_CERTIFICATION.md) | [网格核验](verify_interval_transport_grid.py)、[147456 单元证书](FULL_TRANSPORT_GRID_CERTIFICATE_2026-10-17.json)；冻结 ε=0.05 实验、列明 binary64 假设，终点 2m−r>0.21144；不认证原 η 种子 |
| 参数转移与新形状 | [A-TRANSFER01](THIN_ONSET_PARAMETER_TRANSFER.md)、[A-NEW01/02](NEW_SHAPE_CONSTRAINTS.md) | [转移核验](verify_thin_parameter_transfer.py)、[新形状核验](verify_new_shape.py)、[jets 核验](verify_new_shape_jets.py)；原路线条件性筛选与新形状预穿轴证书 |
| 带电特征与区间工具 | [A-CHG01](CHARGED_CHARACTERISTIC_METHOD.md)、[A-CHG02](CHARGED_FINITE_DOMAIN_STABILITY.md)、[A-CHG03](CHARGED_U_CONSTRAINED_FORMULATION.md)、[高阶比较](CHARGED_SCREEN_REFINEMENT.md)、[冻结证书尝试](FROZEN_CHARGED_CERTIFICATION.md) | [十二变量核](charged_interval_kernel.py)、[u 约束核](charged_u_interval_kernel.py)、[Lobatto 比较](charged_lobatto.py)；开启/充电段有局部证书，关断与完整带电全域认证仍缺 |
| 不同充电候选与 AF 实现 | [旋转种子与指数尾](ALTERNATIVE_CHARGED_CANDIDATES.md)、[A-AF01](AF_OUTER_EXTENSION.md)、[A-AF02](PAST_COLLAR_AND_AF_REALIZATION.md)、[A-AF03](AF_REALIZATION_WITH_TRANSVERSE_FLUX.md) | [候选验证](validate_alternative_candidates.py)、[整锥约束](verify_early_charged_constraints.py)、[AF 回流核验](verify_af_transverse_flux.py)；整锥有理证书、二维 E0 与非有效实现须区分，指数尾失败保留 |
| 最新边界与终态接口 | [A-PATH01](CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md)、[A-CAUS01](MARGINAL_SEED_CAUSAL_INTERFACE.md)、[A-END01](FINITE_MARGINAL_TAIL_GATE.md) | [精确收缩](verify_constraint_contraction.py)、[实现核验](verify_contraction_implementation.py)、[末端通量证书](ROTATING_TERMINAL_FLUX_N2048_2026-10-20.json)；带前提的必要条件与边界候选 |

## 出射出口与中心分析链：A-EXIT01–23

[10-18 同步快照](SYNC_PROGRESS_2026-10-18.md) 中截至 A-EXIT08 的范围是历史范围。当前文件已推进至 A-EXIT23；各稿结论仍依赖其前置分析。

| 阶段 | 按编号阅读 |
|---|---|
| 出射壳与回流入口 | [01 完整约束](OUTGOING_LARGE_RADIUS_EXIT.md) → [02 回流](OUTGOING_BACKSCATTER_BUDGET.md) → [03 条带几何](OUTGOING_STRIP_BOOTSTRAP.md) → [04 Cauchy 接口](OUTGOING_CAUCHY_STRIP.md) → [05 内侧迹](OUTGOING_INNER_TRACE.md) |
| 中心入口与预算 | [06 导数障碍](CENTER_WEIGHTED_NORM_AUDIT.md) → [07 BV 迹](CENTER_BV_TRACE.md) → [08 零锥范数](CENTER_CONE_NORM.md) → [09 通量](CENTER_EVOLUTION_FLUX.md) → [10 同权 bootstrap](CENTER_WEAK_WEIGHT_BOOTSTRAP.md) |
| 延拓、重构与流 | [11 回流锥](OUTGOING_STRIP_CONTINUATION.md) → [12 重构](CENTER_INTEGRAL_RECONSTRUCTION.md) → [13 约束传播](CENTER_CONSTRAINT_PROPAGATION.md) → [14 局部特征](CENTER_LOCAL_CHARACTERISTICS.md) → [15 全时间流](CENTER_GLOBAL_REDUCED_FLOW.md) |
| 正则性与完整性 | [16 高阶正则](CENTER_HIGHER_REGULARITY.md) → [17 Cartesian 中心](CENTER_CARTESIAN_REGULARITY.md) → [18 因果完整](CENTER_CAUSAL_COMPLETENESS.md) → [19 拼接](OUTGOING_GLOBAL_PATCH.md) → [20 I⁺ / 零 Bondi](OUTGOING_NULL_INFINITY.md) → [21 最大发展](OUTGOING_MAXIMAL_FUTURE.md) |
| 工作范数与扰动 | [22 二阶衰减](OUTGOING_LOCAL_DECAY.md) → [23 相对稳定出口](OUTGOING_SUPPORTED_STABILITY.md) |

各 `verify_outgoing_*.py`、`verify_center_*.py` 及报告见 [完整索引](FILE_INDEX.md)。代数核验不替代适定性、全局估计或外部定理前提的解析复核。

## 阶段与文件约定

- **10-16**：初值、演化基准、小数据链、有限耦合种子及早期筛选。
- **10-17**：有限域认证、参数转移、新形状与带电工具；改为全局阈值主线。
- **10-18**：出射出口与中心链推进至 A-EXIT23；保留横向回流的 A-AF03 实现。
- **10-20**：终态门槛、全局因果接口、收缩路径与首个边界候选。
- **10-21**：两个旋转来源候选的具体光滑自由函数、约束数值重求解、规范化初值的连续半径正性认证及整条合法收缩路径；尚未认证新初值的未来。

当前优先任务见 [路线图](../../ROADMAP.md)。边界候选不自动在 D 外；初始未陷俘不等于整片逃逸；有限域计算不认证最终极端性。

研究稿、脚本、JSON、日志与数据保留原路径和内容，分类见 [完整文件索引](FILE_INDEX.md)，维护见 [例行任务规则](../../task-rules.md)。运行环境按需使用 [NumPy](requirements-evolution.txt)、[NumPy / SciPy](requirements-shooting.txt) 或 [SymPy](../../experiments/requirements-kernel.txt)；初值符号约束与精确收缩核验也需要 SymPy。具体命令、输出路径和认证范围以各稿及脚本为准。

历史复算命令、失败记录和当轮来源核对保存于 [整理前首页](PROGRESS_ARCHIVE_2026-10-20.md)。其中 PR / 分支同步叙述仅为历史记录；本次导航整理未核实或执行远端同步。
