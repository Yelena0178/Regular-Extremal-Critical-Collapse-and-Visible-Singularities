# Goal A 可恢复检查点 GA-R20261023-02

时间：2026-10-23（America/New_York，UTC−04:00）；精确生成时间见旁附 JSON。Goal **active / OPEN**，没有用户暂停，也没有达到完成门槛。本轮边界为研究回合交接，非证明完成。

## 契约、版本与工作树

- 权威 GOAL：[ACCEPTANCE.md](ACCEPTANCE.md)，GA-2026-10-16-v1；本轮仅附加定义展开，不改 A1–A6。D001 及采用的 10-12 01/02 是模型/拓扑/终态来源。
- 分支 `codex/goal-a-research-2026-10-16`，HEAD `5803c9afe81080eea33cc4f12123fa4cef1b8c21`；唯一工作树为本仓库。配置上游 origin 同名分支，但本地无其 remote-tracking ref，不能断言当前远端状态。本轮未 fetch、切分支、提交或推送。
- 入场已有 STATUS/RESULTS/ROADMAP/README/FILE_INDEX/FILE_MANIFEST、中心 observer 及许多未跟踪方向/偏置族文件。均予保留。observer 差异仅为 accepted-row 只读回调，但其只读语义需要调用方保证，不能单凭注释证明无副作用。
- 所有保留的 dirty/untracked 文件、权威来源和当前证据 SHA-256，见 [RECOVERY_SNAPSHOT_2026-10-23_R02.json](RECOVERY_SNAPSHOT_2026-10-23_R02.json)。快照排除自身及将重生成的 FILE_INDEX/FILE_MANIFEST；不形成循环哈希。R01 的 [历史快照](RECOVERY_SNAPSHOT_2026-10-23.json)保持原字节，其对后来修改的导航/检查点哈希不再作当前状态证据；R02 入场时核对该快照全部一致。接受文件还登记修改前 Git HEAD 字节哈希。
- 没有既存统一 GOAL/CLAIMS/ATTEMPTS 管理账：沿用 ACCEPTANCE=GOAL，README/ROADMAP=STATE，各研究稿编号=CLAIMS，本节及历史专题正文=ATTEMPTS，此文件=恢复指针；不另建平行研究体系。历史 canonical/charged_floor 快照只是特定旧代码/失败证据，不是当前完整研究检查点。

## STATE：依赖图与三轴状态

必要图：A1 AND A2 AND A3 AND A4 AND A6 → A5/完整 Goal A；A5 的拓扑论证还使用强连续及 D∩Bform=∅。A6 支撑所有分析边，不能由 A5 反推前提。

| 义务/声明 | 逻辑 | 证据 | 审计/当前缺口 |
|---|---|---|---|
| A1：通过极端端点的同一合法曲线 | OPEN | 已有各候选约束分析/初值证书 | 旧证书不提供极端端点 |
| A2：整个负侧 D | OPEN | 小数据及 A-EXIT01–23 内部稿 | 不能推广到整个近端点负侧；A6 接口待兑现 |
| A3：真正形成及完整 I⁺ | OPEN | A-CAUS01 条件性接口 | 实际中心逃逸与完整终态边界缺失 |
| A4：精确 RN/双极限/端点质量正等式 | OPEN | A-END01 必要门槛 | Γ=H⁺ 未证明，不能替代最终参数 |
| A5：同一三分支边界 | CONDITIONAL | 已有拓扑蕴含 | 前提 A1–A4 尚未闭合 |
| A6：全部依赖 | OPEN | 各专题内部审计/有限核验 | 没有整体数学认证 |
| A-PATH01 P14 首个边界选择 | CONDITIONAL | ANALYTIC | 小数据链、实现及稳定性前提；未重审全部依赖 |
| M02.1/2/3/5 局部引理 | PROVED | ANALYTIC，有限等式 EXACT_ALGEBRA | INTERNAL_AUDIT；详见 A-MARG02 的精确范围 |
| M02.4 最终视界排除接口 | CONDITIONAL | ANALYTIC | INTERNAL_AUDIT；缺 Γ 的最终视界身份/晚时覆盖/仿射完整 |
| M02 应用于目标候选 | CONDITIONAL | ANALYTIC | 缺候选实际无陷俘与邻域控制，不能判全局排除 |
| O01.1–6：径向积分、低电荷门槛、规则中心条件、质量反例、移动层演化及充分预算蕴含 | PROVED | ANALYTIC；等式 EXACT_ALGEBRA | INTERNAL_AUDIT；精确假设见 A-OPT01 |
| O01-APP：对正半径近边际候选闭合 O9 右侧全时积分 | OPEN | 待分析 | 共同实际层、内端通量/出射回流/带电项及 q₀<1 均未兑现 |
| 四次入射光学诊断 | 有限样本记录；无全局推论 | EXPERIMENTAL | INTERNAL_AUDIT；源码/报告哈希匹配，无连续 PDE 包络 |

本轮闭合的是局部辅助必要筛选；**没有新增一个完整 A1–A6 验收门槛的闭合证据**。所有“无有限陷俘的色散极限”应用仍挂在 L001/有限实际域稳定性接口上，未以旧记录的 PROVED 字样越过它。

## ATTEMPTS：恢复与本轮增量

| ID | 输入/方法 | 实际结果与失败签名 | 排除范围/下一判别 |
|---|---|---|---|
| HIST-AXIS-1022 | 正则轴线补入旧 A020，s=1001/1000 | 旧外部正样本未覆盖中心，三档出现中心负 λ | 旧“筛选通过”作废；没有连续陷俘证书 |
| HIST-DIR-1022 | 固定 Q(r)，改变 d | 强入射低电荷聚焦，强出射排走核心质量 | 不再只细分 d≈.7–.8；候选/全模型均未被严格排除 |
| HIST-BIAS-1022 | β∈[−2,2] 改电荷分布、精确积分归一化 | 工作树已有实现、整矩形初值证书及有限报告；README §5 的“尚未实现”是旧叙述 | 不重做已有代码；未从未审计报告继承任何全局结果 |
| R23-MARG-01 | 从实际无陷俘开集内点极小值展开双零方程 | M1 迫使 |Q|=r；两侧偏离的符号给邻近陷俘 | 仅有限实际开集；不能拿 λ<0 网格样本直接套 λ=0 引理 |
| R23-MARG-02 | 波方程+交换子、仿射测地式、Ric(N,N) | M2/M3 给 c≠0 二次增长，c=0/P≠0 为正常数 | 缺视界身份则不作目标候选排除；有限仿射必须另分支 |
| R23-MARG-03 | Taylor 及完整混合方程 | M4 近边际定量判据、尖锐 √2 常数 | 缺共同邻域/二阶控制，低电荷有限样本仍是探索 |
| R23-VERIFY-01 | 精确符号核验与负对照 | 初次以结构相等比较展开式失败，改为 simplify(差)=0 后通过；数学公式未改 | 有限代数，非 PDE 证明；见核验 JSON |
| R23-OPT-01 | 替代 M4 的 K/Ω 规范界 | 直接积分 d(rλ)/dr=κ(1−Q²/r²)，κ_r/κ=r|D_Nφ|²，得到 O1–O5 | 移除二阶规范界，仍缺实际光学预算 |
| R23-OPT-02 | 试以 Hawking 质量控制 B | O6 仅控制 rf w；O7 在固定层 f>0、m有界而B→∞ | 该质量-only推理 REFUTED；不反驳实际目标族 |
| R23-OPT-03 | 对固定面积层求 v 导数 | 保留移动端点后得 O8；Young 吸收得 O9 | 给出实际全局估计靶，尚未证明其右侧可积 |
| R23-OPT-04 | d=.5与.8 两档实际入射诊断 | 四次均完成；残差加密比3.8–4.9；.5低电荷负f，.8最小f仍为初始约.1988 | 没有新的端点候选或连续陷俘证书；不继续只降低λ |
| R23-OPT-VERIFY | 精确/解析迹反驳检查 | 非零通量FLRW、曲线Minkowski、丢端点负对照通过；首次测试错误要求舍入噪声继续缩小，改为噪声阈值后通过 | 数学和诊断公式未改；仍无独立带电中心动态基准 |

## 证据完整性及复算

本轮实际核对两份 CHARGE/BIASED 初值证书的当前源码哈希、方向族汇总引用的各报告字节哈希，均相符。尚未重算旧有理证书每个区间，也未重放演化或重新证明 A-EXIT 分析；它们保留原有作用域。核对方向族报告自己的 source_sha256 的结果另存旁附快照，不能用汇总的旧布尔值代替当前检查。

仓库根复算命令：

```powershell
python -X utf8 research/goal_a/verify_finite_marginal_rigidity.py
python -X utf8 research/goal_a/verify_incoming_optical_depth.py
python -X utf8 research/goal_a/audit_incoming_optical_depth.py
python -X utf8 .agents/skills/math-research-goal-runner/scripts/validate_skill.py --self-test
python checks/update_navigation.py --write
python checks/update_navigation.py --check
python checks/verify_navigation.py
python checks/verify_manifest.py
```

运行环境 Python 3.13、SymPy 1.14.0；有限恒等式用精确符号算术。技能自检检查包装与记账，不检查数学真伪。导航/字节清单检查也不认证数学。

R01 实际结果：M02 代数核验五项检查及三项负对照通过；技能 28 项隔离控制通过；导航生成一致性、当前导航本地链接、当前字节清单均 PASS。17 份继承证据的当前来源检查全部相符。R02 新增 O01 精确恒等式、质量反例、解析迹控制及端点遗漏负对照通过；四份演化报告源码和字节审计一致。所有四个运行句柄均已返回 exit_code=0，无待轮询任务。未据此升级任何全局证明。

## 下一轮直接执行的研究动作

1. 首先逐项核对旁附 JSON 的来源哈希；若有变化只重审受影响依赖。读取 A-MARG02 §4 的 M4，不重新通读历史档案。
2. 主攻 **O01-APP（OPEN）**：从 A-OPT01 O8/O9 出发，尝试以实际质量通量和波方程取得固定正半径层的 ∫dv λ(a)w(a) 与 ∫∫[|D_vφ|²/κ+e²κQ²|φ|²/r²]drdv 控制。明确固定 r 与固定 u 导数差异；不得把质量总界直接换成 B 界（O7反例），不得删内端入流。预期判别：可对低电荷层闭合 B bootstrap，或出现确切不可积的回流/带电/内端项。
3. 优先做解析推导。若需检验 O8 的候选有限迹，现有四份 `INCOMING_OPTICAL_D*_2026-10-23.json` 已存常v的完整抽样点；只包含五条射线，不足以求固定面积层的连续v导数。可以扩展 observer 新存固定面积端点通量与径向积分，再做一次指定有限域判别，不重新泛扫d。不要覆盖旧报告；新版本另记源码和无误差证书标记。
4. 若 O9 必需积分在极端尺度不可控制，研究该退化能否支持正质量、电荷共同滞留，结合 A-TAIL01 的非一致晚时辐射要求；不能为了闭合证明加入全参数一致衰减。仍保留只在无限晚时趋近边际的路线；M02.2 的有限球后置修复排除不适用于它。

无待用户回答的问题。继续原冻结目标；保留所有条件性接口及失败证据，不降低验收。
