# 例行整理与导航维护

## 定位与编辑

- 从 [atlas-map.md](atlas-map.md) 进入相关主题；无需遍历历史快照。
- 当前进展维护在 research/goal_a/README.md 与根目录 STATUS.md、RESULTS.md、ROADMAP.md。
- proofs/、inputs/、reviews/、hidden_files/ 中的历史材料保留日期与证据内容；旧结论不得直接升级为当前认证。
- 研究脚本、JSON 和日志原路径供导入、复算及源文件哈希使用。移动前必须检查相关引用；本次使用导航分类，保留这些路径。

## 新增研究材料后

1. 在研究首页关联研究稿、实际核验入口和主要报告，并说明假设与未完成项。
2. 进展改变时同步更新根目录状态、成果和下一步任务；历史阶段说明注明日期。
3. 从仓库根运行 `python checks/update_navigation.py --write`，刷新完整文件索引与当前字节清单。
4. 运行 `python checks/update_navigation.py --check`、`python checks/verify_navigation.py` 和 `python checks/verify_manifest.py`。

清单覆盖 Git 已跟踪及未忽略文件，不表示新增文件已经提交。旧清单 checks/FILE_MANIFEST_2026-10-10.json 是历史证据，保持原字节；不用于检验修改后的工作树。

材料整理不改变数学验收标准。提交、推送或发布依据当前用户授权；历史记录中的“未提交”不替代当前 Git 状态。

## 历史证据与检查点

- 原科学文件、报告及快照不因导航维护而重写；需要改科学内容时另立研究记录并解释证据失效范围。
- 当前导航与旧快照不同，须在维护记录逐项登记；运行 `python checks/verify_research_snapshot.py --allow-navigation-updates` 核对科学文件和所有收据。
- 新文本文件应声明明确换行属性，避免 Git 检出改变哈希。提交前用独立检出核对清单；GitHub PR 说明须对应当前研究范围。
