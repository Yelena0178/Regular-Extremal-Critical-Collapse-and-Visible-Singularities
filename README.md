# 正则极端临界塌缩与可见奇点

**Regular Extremal Critical Collapse and Visible Singularities · RECCVS**

四维球对称 Einstein–Maxwell–无质量带电复标量场的数学相对论研究。研究正则中心、单端渐近平坦初值能否在完整色散与真正形成黑洞的边界产生正质量极端 RN 终态。

**目标 A–D 均未完成。** 研究成果更新至 2026-10-27 的 R31；仓库入口与材料核对更新至 2026-10-28。内部解析稿、条件性接口、有限计算各有独立作用域，均不等于完整目标证明。

当前成果位于 [研究分支](https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/tree/codex/goal-a-research-2026-10-16)，通过 [草稿 PR #5](https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/pull/5) 汇入 `main`。2026-10-28 核对时，默认分支 `main` 仍为 10-12 基线；应以正在阅读的分支和提交为准。

## 从这里开始

| 要了解什么 | 入口 |
|---|---|
| 已有什么、还缺什么 | [当前状态](STATUS.md)、[成果与证据范围](RESULTS.md) |
| 固定模型与最终要求 | [D001 模型](definitions/MODEL.md)、[Goal A 契约 A1–A6](research/goal_a/ACCEPTANCE.md) |
| 按主题审查研究 | [目标 A 专题导航](research/goal_a/README.md)、[完整文件索引](research/goal_a/FILE_INDEX.md) |
| 下一轮研究和恢复 | [路线图](ROADMAP.md)、[R31 检查点](research/goal_a/RECOVERY_CHECKPOINT.md)、[维护与恢复说明](checks/REPOSITORY_AUDIT_2026-10-28.md) |
| 下载、复算与核对证据 | [获取与同步](UPLOAD_GUIDE.md)、[复算说明](REPRODUCE.md)、[验证记录](VERIFICATION.md) |
| 查找旧证明和来源 | [仓库地图](atlas-map.md)、[L001–L023](proofs/INDEX.md)、[阶段审查](reviews/README.md)、[文献来源](literature/SOURCES.md) |

## 当前研究处于哪里

| 已保存的成果 | 尚未跨过的门槛 |
|---|---|
| 合法约束初值、连续半径证书、有限未来筛选及反例记录 | 尚无已认证的正质量极端临界端点 |
| A-EXIT01–23 小数据 / 出射出口与中心分析链 | 尚未接入同一条目标曲线的整个负侧 |
| ESC01、BOND02 特定形成种子的中心逃逸及实际 Bondi 外区内部解析稿 | 不提供该种子的强 RN 终态，也不提供临界三分支 |
| RN20 → SPACE21 → CONE22 → LOCAL23 的参考核、体源与未来局部化 | 实际过去边界迹、A/D 闭合、高频及规则视界强终态仍缺 |

最终要求是在固定强 X⁶ 拓扑下同一条 C¹ 曲线上，同时证明负侧完整色散、端点真正形成且 Mf=|Qf|>0、正侧真正形成且 0<|Qf|<Mf，以及真正边界身份。不能按文件数、检查数或已写接口数估计完成比例。精确定义以 [ACCEPTANCE](research/goal_a/ACCEPTANCE.md) 为准。

## 材料结构

| 位置 | 用途 |
|---|---|
| 根目录状态、成果、路线图 | 当前结论、证据边界和工作优先级 |
| `research/goal_a/` | 研究稿、实现、报告、数值记录、恢复快照；原路径保留 |
| `definitions/`、`proofs/` | 模型定义与早期 23 份证明稿 |
| `inputs/`、`experiments/` | 形成输入、辅助剖面及精确计算 |
| `literature/`、`reviews/`、`hidden_files/` | 外部来源、阶段审查和历史过程材料 |
| `checks/`、`FILE_MANIFEST.json` | 导航、字节完整性、证据收据和复算入口 |

按主题找文件用研究导航；按文件名找材料用完整索引；逐轮经过见 [截至 R31 的原研究首页](research/goal_a/PROGRESS_ARCHIVE_2026-10-28.md)。历史记录中的“未提交”等措辞只描述当轮状态。

## 快速检查

```bash
python checks/update_navigation.py --check
python checks/verify_navigation.py
python checks/verify_manifest.py
python checks/verify_research_snapshot.py --allow-navigation-updates
```

这些只检查材料与记录一致性。研究实验的依赖、输出及范围见 [REPRODUCE](REPRODUCE.md)；重新运行应使用独立检出，避免覆盖已归档报告。

## 来源与引用

来源和历史范围见 [PROVENANCE](PROVENANCE.md)，许可见 [LICENSE_NOTICE](LICENSE_NOTICE.md)。[CITATION.cff](CITATION.cff) 保留 0.1.0 历史版本信息并提供实际仓库地址；引用后续研究时另注明提交 SHA、研究稿编号及日期。第三方文献按 [SOURCES](literature/SOURCES.md) 的版本链接获取。审查与贡献方式见 [CONTRIBUTING](CONTRIBUTING.md)。
