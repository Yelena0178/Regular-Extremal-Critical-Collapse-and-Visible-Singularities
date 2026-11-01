# 来源与保存范围

## 2026-10-28 材料完整性与历史界限

R31 研究已同步到研究分支 `codex/goal-a-research-2026-10-16`。本次重整导航，原研究首页按原字节保存在 [PROGRESS_ARCHIVE_2026-10-28](research/goal_a/PROGRESS_ARCHIVE_2026-10-28.md)，旧证明、验收、科学脚本、报告、数值文件及快照保持原字节。导航差异与收据核对见[维护记录](checks/REPOSITORY_AUDIT_2026-10-28.md)。

当前仓库公开材料范围由 [FILE_MANIFEST](FILE_MANIFEST.json) 列明。下文 `source-archives/` 及原始 ZIP 指早期交付包，不表示这些附件位于当前 Git 仓库；未在仓库中的原交付附件不能从 Git 凭空恢复。第三方论文使用 [版本化来源链接](literature/SOURCES.md)，不把全文缺席误记为本次研究成果丢失。

## 2026-10-20 本地后续研究与导航

在原 main 基线 `3d5bf6b` 之后，本地 research/goal_a/ 累积 10-16 至 10-20 的研究稿、代码、证书与探索记录。当前入口见 [仓库地图](atlas-map.md) 和 [研究首页](research/goal_a/README.md)，全文件分类见 [FILE_INDEX](research/goal_a/FILE_INDEX.md)。

本次保留研究文件原路径及证据内容，将整理前研究首页全文保存到 research/goal_a/PROGRESS_ARCHIVE_2026-10-20.md。更新根目录摘要的同时，保留其明确标日期的第七轮成果和任务；不把历史快照改写为新的证明结果。

原 FILE_MANIFEST.json 按原字节保存为 checks/FILE_MANIFEST_2026-10-10.json；根目录清单更新为当前已跟踪及未忽略文件的字节清单，排除自身和被忽略输出。清单和研究索引由 checks/update_navigation.py 维护。历史校验清单不应直接用于当前修改后的工作树。

本地整理不表示已提交或推送；本次没有独立复核数学证明或重新执行研究计算。

## 原始来源与 0.1.0 保存范围（2026-10-10）

本仓库来自 RECCVS_First_Period_Trapping_2026-10-09.zip，另加入第一轮和第四轮单独 Markdown。
23 份证明稿、模型、任务规格与既有脚本保留原正文。首页重写；原首页在 reviews/ORIGINAL_README_2026-10-09.md 保存。

checks/SOURCE_MAP.json 记录复制和排除文件的原始 SHA-256。排除项在交付包 source-archives/ 内的原始 ZIP 完整保留，包括第三方文献全文、导入 ZIP 与 RN 扫描示例。此交付可恢复全部用户提供材料；主仓库是便于阅读和复算的整理版。

本次新增说明、索引、复算包装及校验程序属于项目整理，没有重新证明或独立认证原数学主张。
reviews/ROUND_07_FILE_MANIFEST.json、历史校验值及输入包自己的 SOURCE_MAP.json 按原快照解释；当前整理版完整性使用根目录 FILE_MANIFEST.json。
