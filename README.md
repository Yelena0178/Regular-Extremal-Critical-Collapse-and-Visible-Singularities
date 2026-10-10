# 正则极端临界塌缩与可见奇点

**Regular Extremal Critical Collapse and Visible Singularities · RECCVS**

四维球对称 Einstein–Maxwell–charged scalar field 系统的数学相对论研究项目。
研究正则中心、单端渐近平坦初值能否在真正全局色散/黑洞边界形成非零质量极端终态，以及其内部边界、曲率与可见性。

研究材料截止 **2026-10-09 第七轮**；本仓库整理日期 **2026-10-10**，快照版本 **0.1.0**。
本次整理未补证新的数学定理。目标 A–D 仍开放；证明稿尚待独立数学复核。

## 当前成果

| 成果 | 证明入口 | 准确范围 |
|---|---|---|
| 有限时间严格陷俘的阈值排除 | [L001](proofs/RECCVS_L001.md) | 标准稳定性与不完备定理的组合；用于候选筛选 |
| 近视界实际内侧控制 | [L007–L012 索引](proofs/INDEX.md) | 特殊精确接合输入的薄带、楔域及固定宽度全时间条带 |
| 全中心体积控制与轴线有限寿命 | [L013–L016 索引](proofs/INDEX.md) | 条件于形成输入及前置估计；有限固有寿命不等于曲率奇点 |
| 深中心的有限区间陷俘判据 | [L018](proofs/RECCVS_L018.md)、[L019](proofs/RECCVS_L019.md) | 判据针对实际解；尚未认证原种子的全部所需输入 |
| 固定八阶领先剖面及精确证书 | [L020](proofs/RECCVS_L020.md)、[L021](proofs/RECCVS_L021.md) | 辅助领先剖面与周期族；不是有限振幅端点根或时空演化 |
| 修复尾部的定量预算 | [L022](proofs/RECCVS_L022.md) | 给出锥误差接口；陷俘保留仍须实际有限时间稳定域 |
| 第一周期严格陷俘机制 | [L023](proofs/RECCVS_L023.md) | 条件于有限阶形成分支、完整 Minkowski 入射填充及 An–Lim 定理接口；充分长成员陷俘 |

**目前最强的候选筛选结论：** 指定实现的充分长有限阶分支含严格陷俘球，因此不能作为完备色散侧临界基点。原来尚未冻结的任意光滑种子未获无条件认证；本结论也不禁止全部极端形成解。

## 阅读顺序

1. [成果总览](RESULTS.md)与[当前状态](STATUS.md)：结论、假设和未闭合项。
2. [模型与目标定义](definitions/MODEL.md)：作用量、规范、约束空间、可见性。
3. [形成输入审计](inputs/AUDIT.md)：旧形成项目能提供什么。
4. [全部 23 份证明索引](proofs/INDEX.md)：按主题阅读，编号保持原样。
5. [第七轮评审](reviews/ROUND_07.md)与[研究路线](proofs/ROUTES_AND_TASKS.md)。
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
| `definitions/` | 模型及命题定义 |
| `proofs/` | 23 份原证明稿与路线记录 |
| `experiments/` | 精确计算脚本、输入和原证书 |
| `inputs/` | 形成输入、历史支持材料、接口审计 |
| `literature/` | 文献矩阵、定理定位、版本与来源链接 |
| `reviews/` | 七轮记录及原始首页，作为研究历史 |
| `checks/` | 当前打包复算结果和材料来源记录 |

## 复算与审查

```bash
python3 checks/reproduce.py
python3 checks/verify_manifest.py
```

核心证书使用 Python 标准库。L012 核代数的原脚本另需 SymPy，执行方法见 [REPRODUCE.md](REPRODUCE.md)。通过计算只说明相应代数证书复现，不认证完整 PDE、因果结构或独立同行审查。

## 来源、许可与贡献

本次打包保留全部 23 份证明正文。材料重组和排除清单见 [PROVENANCE.md](PROVENANCE.md)。第三方论文全文未放入主仓库，版本化链接见 [literature/SOURCES.md](literature/SOURCES.md)。完整原始快照随交付包单独提供。

尚未选定统一再使用许可，见 [LICENSE_NOTICE.md](LICENSE_NOTICE.md)。引用元数据见 `CITATION.cff`；其中不含尚未创建的仓库 URL。
欢迎提交逐条数学复核与反例，具体要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。
