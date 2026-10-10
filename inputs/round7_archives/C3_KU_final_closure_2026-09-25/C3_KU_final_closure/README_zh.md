# 本轮交付

本包保留原始 N=50 有理 profile，完成 A–I 的解析证明稿及对应审计。先读 `00_status.md`，核心证明在 `01_uniform_C1_residual_theorem.md`；合并全文为 `FINAL_PROOF.md`。

结论的类型是：存在足够小的有限振幅、有限长度和修正参数，使精确三阶残差为零，并满足全程半径/横向半径正负号条件。端点按 KU 球面数据逐项匹配后，复用其全局化证明，得到至少 C2 的球对称 EMCSF 塌缩时空，最终精确为极端 RN，且 |e|M<0.57。

已独立重建六 moments、右逆、current 与 K 的连续区间证书；脚本只需 Python 标准库。原系数没有重新优化。

尚未完成的是明确指定 δ*、L*、c* 后的 interval Newton/Krawczyk 数值成员证书。不要将包内 profile 正性区间证书误认成这一证书。详见 `10_remaining_gaps.md`。
