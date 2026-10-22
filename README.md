# 正则极端临界塌缩与可见奇点

**Regular Extremal Critical Collapse and Visible Singularities · RECCVS**

四维球对称 Einstein–Maxwell–charged scalar field 系统的数学相对论研究项目。
研究正则中心、单端渐近平坦初值能否在真正全局色散/黑洞边界形成非零质量极端终态，以及其内部边界、曲率与可见性。

本地研究材料更新至 **2026-10-20**。早期 **2026-10-09 第七轮 / 0.1.0** 快照继续保留；后续研究集中于 `research/goal_a/`。本页描述当前工作树，不表示这些修改已提交或同步到 GitHub 默认分支。
**目标 A–D 仍开放；内部证明稿尚待独立数学复核。** 本次导航整理没有新增数学证明或重新认证研究结果。

[仓库地图](atlas-map.md) · [当前状态](STATUS.md) · [成果总览](RESULTS.md) · [下一步](ROADMAP.md) · [目标 A 研究首页](research/goal_a/README.md) · [完整研究文件索引](research/goal_a/FILE_INDEX.md)

## 后续研究进展（2026-10-16 至 10-20）

10-11 至 10-12 的[阶段审查](reviews/README.md)已记录旧有限八阶 jet 端点系统的内部根认证，以及共同 Cauchy / 全条带等条件性推进；阶段 3 整体仍未闭合。不能继续把该有限根笼统记作“未求出”，也不能将它当作完整形成或目标 A 认证。

当前采用 [全局阈值优先路线](research/goal_a/GLOBAL_THRESHOLD_ROUTE.md)，最终标准见 [目标 A 验收](research/goal_a/ACCEPTANCE.md)。

| 方向 | 当前材料与限制 |
|---|---|
| 初值、演化与有限域工具 | 新增约束初值族、极坐标 / shift / 特征演化、精确代数及区间工具；冻结中性实验有有限矩形陷俘证书，不等于原光滑种子或全局认证 |
| 小数据与完整色散出口 | 指定小数据分析链及 A-EXIT01–23，推进到中心完整性、I⁺、零 Bondi、二阶衰减和相对稳定出口；仍需前置分析及适定性接口复核 |
| 候选与完整 AF 实现 | 旋转种子的整锥有理证书、二维 E0 筛选和 [A-AF03](research/goal_a/AF_REALIZATION_WITH_TRANSVERSE_FLUX.md) 非有效实现稿；尚无真正形成及 RN 终态认证 |
| 10-20 全局因果与终态门槛 | [A-CAUS01](research/goal_a/MARGINAL_SEED_CAUSAL_INTERFACE.md) 条件性黑洞结论与逃逸接口；[A-END01](research/goal_a/FINITE_MARGINAL_TAIL_GATE.md) 给带事件视界身份前提的曲率门槛 |
| 10-20 同一约束路径与边界 | [A-PATH01](research/goal_a/CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md) 保持初始未陷俘的收缩路径和首个色散边界候选；候选定位、是否在 D 外、极端终态及右侧分支仍未证明 |

全部专题、A-EXIT01–23 阅读顺序、核验入口和结果文件见 [研究首页](research/goal_a/README.md) 与 [完整索引](research/goal_a/FILE_INDEX.md)。

## 第七轮基础成果（截至 2026-10-09）

| 成果 | 证明入口 | 准确范围 |
|---|---|---|
| 有限时间严格陷俘的阈值排除 | [L001](proofs/RECCVS_L001.md) | 标准稳定性与不完备定理的组合；用于候选筛选 |
| 近视界实际内侧控制 | [L007–L012 索引](proofs/INDEX.md) | 特殊精确接合输入的薄带、楔域及固定宽度全时间条带 |
| 全中心体积控制与轴线有限寿命 | [L013–L016 索引](proofs/INDEX.md) | 条件于形成输入及前置估计；有限固有寿命不等于曲率奇点 |
| 深中心的有限区间陷俘判据 | [L018](proofs/RECCVS_L018.md)、[L019](proofs/RECCVS_L019.md) | 判据针对实际解；尚未认证原种子的全部所需输入 |
| 固定八阶领先剖面及精确证书 | [L020](proofs/RECCVS_L020.md)、[L021](proofs/RECCVS_L021.md) | 辅助领先剖面与周期族；不是有限振幅端点根或时空演化 |
| 修复尾部的定量预算 | [L022](proofs/RECCVS_L022.md) | 给出锥误差接口；陷俘保留仍须实际有限时间稳定域 |
| 第一周期严格陷俘机制 | [L023](proofs/RECCVS_L023.md) | 条件于有限阶形成分支、完整 Minkowski 入射填充及 An–Lim 定理接口；充分长成员陷俘 |

**该快照的候选筛选结论：** 指定实现的充分长有限阶分支含严格陷俘球，因此不能作为完备色散侧临界基点。原来尚未冻结的任意光滑种子未获无条件认证；本结论也不禁止全部极端形成解。后续有限域证书、转移与候选状态以研究首页为准。

## 阅读顺序

1. [成果总览](RESULTS.md)与[当前状态](STATUS.md)：结论、假设和未闭合项。
2. [模型与目标定义](definitions/MODEL.md)：作用量、规范、约束空间、可见性。
3. [后续研究首页](research/goal_a/README.md)与[正式验收](research/goal_a/ACCEPTANCE.md)：当前主线、进展和缺口。
4. [形成输入审计](inputs/AUDIT.md)与[全部 23 份旧证明索引](proofs/INDEX.md)：按需核对基础依赖。
5. [第七轮评审](reviews/ROUND_07.md)、[旧研究路线](proofs/ROUTES_AND_TASKS.md)及[后续阶段记录](research/goal_a/PROGRESS_ARCHIVE_2026-10-20.md)。
6. [复算说明](REPRODUCE.md)、[本次检查记录](VERIFICATION.md)。

## 开放目标

| 目标 | 当前状态 |
|---|---|
| A：正则中心的真正全局极端临界分支 | 未证明；尚无合格且经认证的临界基点 |
| B：统一受控初值族中的可见曲率放大 | 未证明 |
| C：单解有限仿射参数的可见曲率奇点 | 未证明 |
| D：指定拓扑中的一般性与稳定性 | 未证明 |

下一步具体任务见 [ROADMAP.md](ROADMAP.md)。

## 目录

| 目录或文件 | 内容 |
|---|---|
| `atlas-map.md`、`task-rules.md` | 主题路由与例行导航维护 |
| `research/goal_a/` | 10-16 至 10-20 后续研究、演化与认证工具、证据和完整文件索引 |
| `definitions/` | 模型及命题定义 |
| `proofs/` | 23 份原证明稿与路线记录 |
| `experiments/` | 精确计算脚本、输入和原证书 |
| `inputs/` | 形成输入、历史支持材料、接口审计 |
| `literature/` | 文献矩阵、定理定位、版本与来源链接 |
| `reviews/` | 七轮记录、10-11 至 10-12 阶段审查及原始首页，见目录导航 |
| `checks/` | 当前打包复算结果和材料来源记录 |
| `hidden_files/` | 过程输出与使用记录，作为历史来源按需读取 |

## 复算与审查

```bash
python3 checks/reproduce.py
python3 checks/update_navigation.py --check
python3 checks/verify_navigation.py
python3 checks/verify_manifest.py
```

旧核心证书与导航检查使用 Python 标准库。L012 核代数另需 SymPy，后续演化 / 求根按需使用 NumPy / SciPy，入口与范围见 [REPRODUCE.md](REPRODUCE.md)。旧复算程序不覆盖全部后续研究；计算通过不认证完整 PDE、因果结构或独立同行审查。

## 来源、许可与贡献

本次打包保留全部 23 份证明正文。材料重组和排除清单见 [PROVENANCE.md](PROVENANCE.md)。第三方论文全文未放入主仓库，版本化链接见 [literature/SOURCES.md](literature/SOURCES.md)。完整原始快照随交付包单独提供。

尚未选定统一再使用许可，见 [LICENSE_NOTICE.md](LICENSE_NOTICE.md)。引用元数据见 `CITATION.cff`；其中不含尚未创建的仓库 URL。
欢迎提交逐条数学复核与反例，具体要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。
