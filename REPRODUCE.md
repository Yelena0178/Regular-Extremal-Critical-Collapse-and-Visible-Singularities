# 复算说明

## 当前工作树与导航检查（2026-10-20）

在仓库根目录执行。下面三项仅检查导航与文件字节，不运行研究实验：

```bash
python checks/update_navigation.py --check
python checks/verify_navigation.py
python checks/verify_manifest.py
```

新增研究文件后运行 `python checks/update_navigation.py --write` 刷新 [完整研究索引](research/goal_a/FILE_INDEX.md) 与根目录清单，再执行上述检查。维护规则见 [task-rules](task-rules.md)。

当前 FILE_MANIFEST.json 覆盖 Git 已跟踪及未忽略文件（排除自身和被忽略输出），包括后续研究与历史材料；它不表示文件已提交。10-10 原始清单按原字节保存在 checks/FILE_MANIFEST_2026-10-10.json，仅用于历史比对。旧快照报告均保持原范围。

## 后续研究的按需复算

先从 [研究首页](research/goal_a/README.md) 选定专题，再读相应研究稿、脚本输入 / 输出和报告范围。完整脚本与证据见 [文件索引](research/goal_a/FILE_INDEX.md)。后续研究没有一个覆盖所有成果的统一定理验证器。

| 任务 | 代表入口 | 依赖及注意事项 |
|---|---|---|
| 初值与约束 | `python research/goal_a/verify_research.py`、`python research/goal_a/verify_initial_constraints.py` | 前者使用标准库，后者需要 SymPy；生成检查结果，不证明未来发展 |
| 最新约束路径代数 | `python research/goal_a/verify_constraint_contraction.py` | 需要 SymPy；精确代数检查不能替代首个边界或 RN 终态证明 |
| 极坐标 / shift 演化 | `verify_evolution.py`、`verify_areal_shift.py`，均在 research/goal_a/ | 按 requirements-evolution.txt 使用 NumPy；有限时间基准 |
| 区间网格证书 | `verify_interval_transport_grid.py`、`certify_transport_grid.py`，均在 research/goal_a/ | 阅读 A-GRID01 的输入、算术假设和有限域范围；全网格可能耗时 |
| 求根与候选比较 | 研究首页中对应核验脚本 | 按 requirements-shooting.txt 使用 NumPy / SciPy；E0 与严格证书分开 |

研究脚本可能生成或覆盖原目录中的 JSON、日志和数值结果；本次导航整理未重新执行这些研究实验。需要检查 `-O` 时，以各稿列明的普通 / 优化执行范围为准。

## 第七轮证书复算（原 0.1.0 快照范围）

在仓库根目录执行，建议 Python 3.11 或以上。本次环境版本见 checks/PACKAGING_VERIFICATION.json。

```bash
python3 checks/reproduce.py
python3 checks/verify_manifest.py
```

核心流程仅用 Python 标准库：重新生成 K=8、n=88、σ=1/20 的有理剖面，逐个复算 J 和可行族证书、第一周期门槛；与原 JSON 比较；检查 Python -O 下结果相同；检查 n=44 和篡改输入确实被拒绝。
输出写入 checks/generated/，不会改写原证书。脚本执行时间取决于机器；全程不调用远程数据。

可选核代数检查需要原 requirements-kernel.txt 中的 SymPy：

```bash
python3 -m pip install -r experiments/requirements-kernel.txt
python3 checks/reproduce.py --with-kernel
```

SymPy 检查只核对 L012 显示的核恒等式，不认证其 PDE 控制或延续。本次打包环境无 SymPy，因此没有重新运行这个可选检查；保留原 KERNEL_ALGEBRA_RESULT.txt 作为历史记录。

## 直接运行原脚本

```bash
python3 experiments/freeze_filtered_profile.py --K 8 --n 88 --sigma 1/20 --output checks/generated/profile.json
python3 experiments/certify_filtered_J.py checks/generated/profile.json checks/generated/J_certificate.json
python3 experiments/certify_admissible_profile.py checks/generated/profile.json checks/generated/admissible_certificate.json
python3 experiments/check_first_period_thresholds.py
```

freeze_filtered_profile.py 的原默认 n=44 是失败试算，复算可行族时必须显式指定 n=88。

## 第七轮计算范围

通过结果认证相应有限有理代数与充分门槛。光滑截断及 PDE 分支的分析论证仍要阅读正文；没有具体有限振幅非线性根认证、没有实际中心时空演化、没有独立数学审查。

输入形成包自有 REPRODUCE.md 保留其历史作用；本入口不自动将那些检查称为本项目完整定理验证。
