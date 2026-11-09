# 2026-10-18 GitHub 同步快照

目标 A 保持 [ACCEPTANCE.md](ACCEPTANCE.md) 的完整要求，尚未完成。以下均为内部研究材料，未经过独立数学复核。

## 本次增加的研究

- 原 R=5 小参数路线的条件性排除保留。R=10、冻结充电矩形及两种从开启段充电的候选详见 [候选记录](ALTERNATIVE_CHARGED_CANDIDATES.md) 和 [冻结证书](FROZEN_CHARGED_CERTIFICATION.md)。约束证书、有限矩形证书和 E0 筛选的作用域分别标明；未把采样无陷俘提升为全未来结论。
- 按用户要求转入 [全局阈值路线](GLOBAL_THRESHOLD_ROUTE.md)。[A-EXIT01](OUTGOING_LARGE_RADIUS_EXIT.md) 构造规则中心、完整渐近平坦的外向壳初值；它是色散出口研究对象，尚不是已证明的临界族成员。
- [A-EXIT02](OUTGOING_BACKSCATTER_BUDGET.md)、[A-EXIT03](OUTGOING_STRIP_BOOTSTRAP.md)、[A-EXIT04](OUTGOING_CAUCHY_STRIP.md)、[A-EXIT05](OUTGOING_INNER_TRACE.md) 给反散射、已存在有限外条带的闭合预算、实际 Cauchy 楔区及内侧迹控制。不能以其统一常数直接宣称无限时间延拓。
- [A-EXIT06](CENTER_WEIGHTED_NORM_AUDIT.md) 指出仅增大壳半径不能使所讨论的高权重一阶导数范数变小。[A-EXIT07](CENTER_BV_TRACE.md) 转向 BV 迹控制；[A-EXIT08](CENTER_CONE_NORM.md) 得到单条锥上的质量、电荷、紧致度与 Raychaudhuri 预算。尚缺跨所有未来锥的传播与中心控制。

## 本次复核

实际运行以下 7 个脚本，退出码均为 0；完整输出保存在 [同步验证记录](SYNC_VALIDATION_2026-10-18.json)。从 research/goal_a 目录执行 `python -X utf8 <脚本名>`，需安装脚本所用 SymPy。

1. verify_outgoing_exit.py
2. verify_outgoing_backscatter.py
3. verify_outgoing_strip_bootstrap.py
4. verify_outgoing_cauchy_strip.py
5. verify_outgoing_inner_trace.py
6. verify_center_derivative_system.py
7. verify_center_cone_norm.py

这些检查验证指定代数恒等式、符号反例及有限预算，不验证完整 PDE 存在性。本次未重跑此前昂贵的二维区间计算；原报告及复现所需 NPZ 数据一并保留。下载的第三方论文 HTML 和 Python 缓存不纳入版本控制，文献通过各研究稿中的原始链接访问。

## 未完成的核心要求

新候选的完整实际演化及相应 AF 实现接口、穿中心与全未来控制、同一条 C1 临界曲线、真正事件视界及正质量极端形成、两侧完整色散和次极端 RN 终态仍需证明。已有单锥或有限区域结果不能替代这些要求。
