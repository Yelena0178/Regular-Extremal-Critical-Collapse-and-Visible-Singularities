# ASYM03–04 恢复检查点 — 2026-11-08
源版本53681923不变，ASYM纯渐近数据与SHAPE01壳是不同候选。
本轮证明：H=D_r²phi满足含移动方向/电磁交换子的线性沿线输运；H=H_*+(.0015+.00525i)t^(-i)+O(t^-1)。B_rr→0、A_rr→.5，全部沿线度量C²及电磁C¹必要jets相容。任意有限H(0)可用齐次解处理。
核心新接口：Γ位于外域的未来入射边界，外侧u<0是混合未来/过去特征问题；不能直接调用通常未来Goursat。RN对照固定物理宽度对应初始标签~2R²/v。
验证：verify_asym03.py符号式、删交换子负控制及到t1024的两容差ODE通过，最大差5.17e−10；verify_asym04_coordinates.py精确RN传播式通过。均非实际外带PDE认证。
证据文件：proofs/ASYM03_REGULAR_SECOND_DERIVATIVES.md、reviews/ASYM04_EXTERIOR_REALIZATION_GATE.md、reviews/ASYM03_RESULTS.md、results/ASYM03_SECOND_JET_CHECKS.json、results/ASYM04_COORDINATE_CHECKS.json。
A1–A6仍OPEN。没有实际MGH、视界身份、Bondi终态、正则中心/AF初值或三分支。无后台计算；未提交推送。

下一唯一优先动作：角点/横截边界与实际外部积分系统。
1. 固定ASYM01在s=0的r,Q,nu,phi,P与ASYM03选定有限H(0)=0；在v=0外侧面积半径r≥rΓ(0)选一个明确光滑自由标量延拓，匹配phi、U=P/nu、H，保留电势径向规范。
2. 从B_r=B r|U|²、Q_r=−e r² Im(phi conjugate(U))和lambda_r=B(1−Q²/r²)/(2r)−lambda/r构造完整短横截约束，核对角点同一对象；不要把Γ的未来数据改成过去输入。
3. 用D_LU与Maxwell等式写出真实外带混合积分系统，明确晚时权重及rho≈1/v特征层。目标是固定delta>0的实际域，不是任意有限时间各取delta(T)>0。
4. 成功/退出：若仅完成短角点则明确余下实际无限时外带估计，不能换成不断添加局部文档；如关键非线性项无法闭合，记录具体项和所需数据/范数并审查路线。
只验证新变化；旧实验不重复。全部本地保存，不能称云端备份。
