# 交付验证记录

本文件记录 2026-10-22 安装验收；数学研究状态仍由仓库原记录维护。

```powershell
python .agents/skills/math-research-goal-runner/scripts/validate_skill.py --self-test
python -O .agents/skills/math-research-goal-runner/scripts/validate_skill.py --self-test
```

测试范围：包结构、frontmatter、相对文件链接、UTF-8、围栏、Python 编译；临时副本的损坏输入拒绝；合成全实数平方非负目标初始化、传递依赖与条件性结果拒绝。合成演练详见 [README](README.md)。不测试真实 Goal A，不写入真实研究状态。

## 实测结果

- Python 3.13.5：普通模式和 `-O` 均通过，各 28 个隔离用例。测试不用 assert，因此优化模式不跳过门槛检查。
- 内置 skill-creator 的 `quick_validate.py`：`Skill is valid!`。调用时使用 `python -X utf8`；该额外检查依赖本机已有 PyYAML，交付脚本本身仅依赖标准库。
- 本机 Codex app-server 实际发现通过：初始化 JSON-RPC 后，对仓库根及 `research/goal_a` 两个 cwd 分别执行 `skills/list`（`forceReload: true`），均返回本 Skill，`scope: repo`、`enabled: true`，本 Skill 无加载解析错误。
- 发现结果中的路径为本仓库 `.agents/skills/math-research-goal-runner/SKILL.md`，未安装全局副本。

可复核发现流程：`codex app-server --stdio`，以本机 `generate-json-schema` 输出为协议依据，发送 `initialize`、`initialized` 和 `skills/list`；只检查该名称的响应，避免输出其他插件配置。

已验证的是 Codex 对 metadata/frontmatter 的真实解析和仓库级发现，以及文件正文可读和静态结构。尚未执行独立 LLM 研究回合、长期运行、真实数学结论验证或 GUI 选择器验证；发现通过不等于这些行为已通过。合成演练与回执检查不能替代模型行为评测。

源资料定位：main 当时缺少 `research/goal_a/`；正式验收及 A-PATH01/A-CAUS01/A-END01 在未合并研究 PR #5 的分支上。安装直接落在该实际研究分支，提交仅包含 Skill 包，不自动合并 PR。

## 2026-11-01：战略复盘与每轮同步更新

- 新增 PROGRESS-REVIEW、GITHUB-SYNC 和通用中文启动 prompt；更新研究入口、恢复规则及检查点模板。复盘区分局部进展与关键障碍变化，采用可配置的 5 轮 / 180 分钟有效研究时间门槛，并保留重复失败和连续复盘的升级规则。
- 普通模式及 `-O` 模式的 `validate_skill.py --self-test` 均通过现有 28 个隔离用例；内置 `quick_validate.py` 返回 `Skill is valid!`。必需文件清单已覆盖新增资源。
- 静态流程复核覆盖：持续新增辅助引理但核心前提不变仍触发复盘；有明确依赖桥的必要引理可计入战略推进；换路线或新聊天不清零；刚复盘后不在每次检查重复触发；历史无计时不伪造时长；同步失败保留提交且不形成回执提交循环。
- 本次没有开展真实数学研究、长期停滞演练或独立模型行为评测。上述流程复核与结构测试不证明模型在长期运行中必然遵从，也不提供新的 Goal A 结论。规则在实际研究轮次内执行，未创建离线定时任务。
- 仓库清单日期更新为 2026-11-01；科学材料和验收条件不因这次 skill 更新而升级。实际 GitHub 同步以交付时的本地提交、远端核对及提交链接为准，不在此文件嵌入其自身提交哈希。
