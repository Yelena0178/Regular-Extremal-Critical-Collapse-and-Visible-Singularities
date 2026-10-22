# Math Research Goal Runner：仓库级安装

安装入口：[SKILL.md](SKILL.md)。在实际研究仓库或其子目录启动 Codex，使用 `$math-research-goal-runner`。此包按 [OpenAI Skills 文档](https://learn.chatgpt.com/docs/build-skills) 放在仓库根 `.agents/skills/`，保留默认自动匹配；无需全局安装、第三方依赖或后台服务。当前聊天的工作目录若在 RECCVS 的父仓库，需在 RECCVS 中启动/选择工作目录才能按仓库规则发现它。

## 内容与用途

- 主入口保留目标契约、实际研究循环与完成门槛。
- 五份 references 按需加载目标控制、研究方法、反驳审计、证据标准及 RECCVS 适配。
- 三份 assets 提供 GOAL、CLAIMS、CHECKPOINT；后者也包含 STATE 和 ATTEMPTS 格式。复用仓库已有管理记录，安装不生成真实研究状态。
- 标准库校验器检查结构、受限 frontmatter、UTF-8、Markdown 围栏、包内文件链接与 Python 语法；临时副本测试损坏输入与条件性依赖拦截。

本包故意只使用单行纯文本 `name`/`description` frontmatter。校验器拒绝其他 YAML 写法，不能代替通用 YAML 解析器；文件链接检查不解析完整 Markdown 或标题锚点。RECCVS 源路径采用代码文本并由启动时核对，避免使通用包依赖特定仓库布局。

## 验证

在仓库根执行：

```powershell
python .agents/skills/math-research-goal-runner/scripts/validate_skill.py --self-test
python -O .agents/skills/math-research-goal-runner/scripts/validate_skill.py --self-test
```

`--check-state receipt.json` 可额外检查机器可读完成回执：顶层 `contract_version`、`next_action` 为非空字符串，`required` 为必要 gate ID 列表，`claims` 为 ID 到记录的映射。每条记录必须有 `statement`、`role`、`logic`、`evidence`（列表）、`audit`、`dependencies`（列表）、`proof_receipt`，以及六个显式布尔断言 `premises_discharged`、`external_hypotheses_checked`、`scope_covers_claim`、`global_coverage_checked`、`no_fatal_defects`、`proof_inspectable`。无外部定理/全局区域时须在回执说明不适用理由，再填写已核对。

该接口拒绝未闭合的传递依赖、环、条件结果、失败审计、纯实验/启发证据和以筛选替代必要门槛。它只检查**提供者的记账和声明**，不能核实这些布尔断言、证明真伪、证明路径内容或契约覆盖；PASS 绝不自动授权完成 Goal。Markdown 模板不强制转 JSON，也没有自动状态升级器。

## 合成研究初始化演练（不写入真实状态）

目标：证明所有实数 x 有 x²≥0，模型为有序域 R，量词为所有实数，无额外假设，完成要求为解析证明且内部审计通过。

证明义务 S1：x≥0 或 x<0；前者非负数乘积非负，后者 -x>0 且 x²=(-x)²>0。审计重点为零值和负号，不依赖数值采样。状态为 PROVED / ANALYTIC / INTERNAL_AUDIT；下一步是复查有序域乘法规则与两个分支覆盖。若乘法规则仅被假定而未在所用模型中核对，则该应用应为 CONDITIONAL，不能完成目标。

`--self-test` 构造该记账场景，并将逻辑状态改为 CONDITIONAL、引入未闭合辅助依赖、缺失依赖、循环、有限实验等，验证完成门槛拒绝。此为确定性回执测试及人工演练，**不是 LLM 行为评测或数学证明器**。跨会话演练：按检查点模板记录 contract、分支/HEAD、脏输入哈希、三个状态轴、S1 依赖、命令和下一动作；恢复先核对版本再执行 sign-split 审计，不重新扫描档案。

## 启动提示词：RECCVS Goal A

```text
使用 $math-research-goal-runner，在 Codex 长期目标模式下持续推进 RECCVS Goal A。先核对当前研究分支、工作树、最新正式 ACCEPTANCE.md 及其采用的定义，冻结原始 Goal Contract，服从 A1–A6，不改变最终命题。复用现有研究状态、证明依赖和检查点，定位关键未闭合义务，实际推导引理/估计或执行能改变路线的检验；进行反驳式审计并分别记录逻辑、证据和审计状态。不得用条件性结果、局部陷俘或有限计算替代完整三分支及真正边界结论。预算或上下文结束前保存可恢复检查点，目标未证不得标记完成。研究文件可按目标修改；提交、推送和外部操作遵守本会话授权。
```

## 启动提示词：其他数学物理项目

```text
使用 $math-research-goal-runner，在 Codex 长期目标模式下研究以下命题：[填写精确命题及权威定义/验收文件]。先提取模型、假设、量词、参数域、函数空间、正则性、目标结论与禁止替代，建立不可擅改的 Goal Contract。复用现有状态并构造关键证明依赖图，自主开展实际证明、估计、文献接口核对或认证计算；重复失败时诊断并调整路线。严格区分三个状态轴，审计隐藏假设和局部到全局的跳跃，所有必要依赖闭合后才可宣称成功。每次运行边界保存包含版本、证据和下一具体动作的检查点。不要自动套用 RECCVS 模型；Git 和外部动作依当前授权执行。
```

Skill 不创建后台任务或保证无限运行。运行时发现、模型实际遵从与数学正确性是不同验收层次；发现测试结果和未完成验证见 [交付验证记录](VALIDATION.md)。
