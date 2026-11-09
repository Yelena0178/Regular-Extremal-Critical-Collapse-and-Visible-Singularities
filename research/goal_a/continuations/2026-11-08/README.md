# Goal A 续研档案（2026-11-08）

2026-11-09 同步。研究基于提交 `53681923d0fc83e574f8ec42d82d2b87b54d265c`。A1–A6 的完整验收仍开放。见[冻结契约](../../ACCEPTANCE.md)。

| 研究线 | 已保存的结论及范围 | 证据与恢复 |
|---|---|---|
| SHAPE01–02 | 固定初始电荷的径向形状族、有限演化与冻结射线相位代价。向外形状的有限容量指标由约 .251 增至 .277，诊断半径增大，实际电荷比下降。 | [结果报告](reviews/SHAPE01_RESULTS.md)、[核验](results/SHAPE_COMPARISON.json)、[检查点](checkpoints/2026-11-08_SHAPE01.md) |
| VAR01–02 | 合法初值方向的完整约束切向、坐标反馈与自然方向的初始电流符号。有限域变分估计依赖实际参考域与正分母管。 | [结果报告](reviews/VAR01_RESULTS.md)、[初值核验](results/VAR01_INITIAL_TANGENT.json)、[检查点](checkpoints/2026-11-08_VAR01.md) |
| ASYM01–02 | 独立的纯渐近射线候选满足仿射聚焦一阶矩、射线 Maxwell 约束及第一横向衰减条件。 | [结果报告](reviews/ASYM01_RESULTS.md)、[射线级数证书](certificates/ASYM01_RATIONAL_RAY.json)、[检查点](checkpoints/2026-11-08_ASYM01.md) |
| ASYM03–04 | 同一纯渐近射线的沿线度量 C² 和电磁场 C¹ 必要极限与极端 RN 相容。实际固定宽度外域涉及混合未来与过去的特征边界。 | [结果报告](reviews/ASYM03_RESULTS.md)、[外域接口审查](reviews/ASYM04_EXTERIOR_REALIZATION_GATE.md)、[检查点](checkpoints/2026-11-08_ASYM03.md) |

[依赖表](DEPENDENCIES.md)和[续研步骤](NEXT_STEP.md)记录实际外带、正则中心延拓、完整终态与同一三分支曲线仍需满足的条件。原档案中的日期、工作树和同步状态按各轮记录理解。

## 复算与来源

脚本与回执采用原研究工作区布局。为保留历史字节和输入依赖，在 Windows PowerShell 中从本仓库根创建一个独立复算目录。需要 Python、NumPy、SciPy 和 SymPy。

```powershell
$bundle = (Resolve-Path 'research/goal_a/continuations/2026-11-08').Path
$replay = Join-Path ([IO.Path]::GetTempPath()) ('goal-a-replay-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path (Join-Path $replay 'source') | Out-Null
git -c core.longpaths=true worktree add --detach (Join-Path $replay 'source/goal-a') 53681923d0fc83e574f8ec42d82d2b87b54d265c
Copy-Item -Path (Join-Path $bundle '*') -Destination $replay -Recurse
Push-Location $replay
Move-Item results/ASYM03_SECOND_JET_CHECKS.json results/ASYM03_SECOND_JET_CHECKS.saved.json
python -X utf8 computations/verify_asym03.py
Pop-Location
```

其他核验入口及原始演化参数见各轮检查点和 `computations/` 中的脚本。复算目录应保留输入回执，需重新生成的输出先另存。正式形状对照见 [SHAPE_COMPARISON.json](results/SHAPE_COMPARISON.json)。带 `DRAFT` 的旧汇总留存以便审计。

公开档案将四份文件中的本机绝对路径改为相对引用或工作区占位符，并重算受影响的档案哈希。数学文本、计算源程序和数值保留。来源版本见[来源收据](source/PROVENANCE_2026-11-08.json)。
