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
