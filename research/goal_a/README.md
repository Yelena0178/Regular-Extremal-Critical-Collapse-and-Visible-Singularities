# 目标 A：当前状态与专题导航

数学记录截至 **2026-10-27 / R31**；导航维护：2026-10-28。**完整 Goal A 为 OPEN。** [ACCEPTANCE](ACCEPTANCE.md) 固定 A1–A6，不因材料整理改变。[当前状态](../../STATUS.md)给验收差距，[路线图](../../ROADMAP.md)给研究优先级。

## 先读哪些材料

1. [冻结契约](ACCEPTANCE.md)与[D001](../../definitions/MODEL.md)：模型、强初值空间、三分支量词和强终态。
2. [R31 检查点](RECOVERY_CHECKPOINT.md)：STATE 依赖、三轴状态、ATTEMPTS 失败记录及当轮下一步。
3. 下表中相关研究稿，再读配套脚本和报告；所有文件在[完整索引](FILE_INDEX.md)。
4. [2026-10-28 维护记录](../../checks/REPOSITORY_AUDIT_2026-10-28.md)：解释后续导航差异及如何恢复旧快照。

## 六条研究线

| 研究线 | 证明 / 分析入口 | 核验与证据入口 | 当前界限 |
|---|---|---|---|
| 合法初值与候选 | [A-AF05 连续半径屏障](ROTATING_AF_CONTINUOUS_BARRIER.md)、[A-DIR01 电荷方向族](CHARGE_PRESERVING_DIRECTION_FAMILY.md) | [屏障脚本](certify_rotating_af_barrier.py)、[方向族初值证书](CHARGE_SHELL_INITIAL_CERTIFICATE_2026-10-22.json) | 初值合法不证明未来；未认证极端端点 |
| 有限未来与失败候选 | [正则轴线筛选](REGULAR_AXIS_CAUCHY_SCREEN.md)、[入射光学深度](INCOMING_OPTICAL_DEPTH_GATE.md) | [中心筛选汇总](CENTERED_CAUCHY_SCREEN_SUMMARY_2026-10-22.json)、[光学筛选审计](INCOMING_OPTICAL_SCREEN_AUDIT_2026-10-23.json) | 补入中心后的负样本修正了旧外部正样本判断；有限信号非连续 PDE 认证 |
| 完整色散出口 | [小数据](SMALL_DATA_DISPERSION.md)、[A-EXIT23](OUTGOING_SUPPORTED_STABILITY.md)，依赖顺序见下表 | [完整索引](FILE_INDEX.md)中的 outgoing / center 核验和报告 | 指定数据类的内部分析链；目标近端点负侧未接入 |
| 特定种子的真正形成与 Bondi 外区 | [ESC01 中心逃逸](CENTER_ESCAPE_CHARACTERISTIC_EXTENSION.md)、[BOND02 完整性桥](ACTUAL_BONDI_COMPLETENESS_BRIDGE.md) | [逃逸核验](verify_center_escape_extension.py)、[Bondi 核验](verify_actual_bondi_bridge.py)、[报告](ACTUAL_BONDI_BRIDGE_CHECKS_2026-10-23.json) | 特定输入的内部解析结论；目标族全参数 A3 和强 RN 终态仍 OPEN |
| RN 外区解析工具 | [RN20 静态冻结](STATIC_GEOMETRY_FREEZING_AND_RN_ROBIN.md) → [SPACE21 有限半径 Green](FINITE_RADIUS_RN_GREEN_AND_LOCAL_BODY.md) → [CONE22 无限径向体源](INFINITE_RADIAL_RN_BODY_TRANSFER.md) → [LOCAL23 未来局部化](FULL_RN_FUTURE_LOCALIZATION.md) | [R31 核验](verify_full_rn_future_localization.py)、[R31 报告](FULL_RN_FUTURE_LOCALIZATION_CHECKS_2026-10-27.json) | 参考算子及明确输入下的估计；实际过去 W、A/D 闭合、高频与强视界仍缺 |
| 极端端点与三分支连接 | [PATH01 首个边界](CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md)、[END01 终态门槛](FINITE_MARGINAL_TAIL_GATE.md)、[MARG02 边际刚性](FINITE_MARGINAL_RIGIDITY.md) | [收缩核验](verify_constraint_contraction.py)、[刚性核验](verify_finite_marginal_rigidity.py) | 无已认证正质量极端临界点；同一 C¹ 曲线三分支未构造 |

## 逻辑、证据、审计分别阅读

| 轴 | 含义 |
|---|---|
| 逻辑状态 | PROVED 必须连同精确命题与前提阅读；CONDITIONAL 表示应用前提未兑现；OPEN 是未闭合义务；限定类 REFUTED 不代表 Goal A 被反证 |
| 证据类型 | ANALYTIC / EXTERNAL_THEOREM / EXACT_ALGEBRA / 区间证书 / EXPERIMENTAL 各支持不同范围 |
| 审计状态 | 当前主要为 INTERNAL_AUDIT；来源前提核对和有限负控制不能替代独立数学复核 |

最新 LOCAL23 的未来 W **滤波功能**存在不等于 W 点态尾。条件性外区控制不能冒充完整 A4，更不能单独给出 A1–A6。

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


## 历史、运行与恢复

- [截至 R31 的原研究首页](PROGRESS_ARCHIVE_2026-10-28.md)：原字节保存，含 10-22 至 10-27 逐轮进展与早期专题表；其“最新”和同步状态按原日期理解。
- [10-20 之前首页](PROGRESS_ARCHIVE_2026-10-20.md)、[10-11 至 10-12 审查](../../reviews/README.md)：早期路线与有限根的准确范围。
- [R31 快照](RECOVERY_SNAPSHOT_2026-10-27_R31.json)：221 个文件哈希和 55 份报告 / 源码收据。之后的导航改动另记，不改写旧快照。
- [复算说明](../../REPRODUCE.md)、[检查入口](../../checks/README.md)：环境、只读检查、覆盖输出的研究复算和恢复方式。

所有证明稿、脚本、JSON、日志和 NPZ 仍在原路径。新增材料先关联主题及证据，再按[维护规则](../../task-rules.md)更新索引和清单。
