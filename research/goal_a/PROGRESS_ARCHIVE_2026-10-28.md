# 目标 A：当前进展与专题导航

进展材料截止 **2026-10-27**。本目录自 2026-10-16 开始，基线为 main 提交 `3d5bf6b`。**目标 A 仍未解决**；现有解析稿未经外部独立数学复核。本页汇总本地材料，远端同步状态以 Git 提交为准。

[仓库地图](../../atlas-map.md) · [正式验收](ACCEPTANCE.md) · [当前任务](../../ROADMAP.md) · [完整文件索引](FILE_INDEX.md) · [复算说明](../../REPRODUCE.md) · [整理前阶段记录](PROGRESS_ARCHIVE_2026-10-20.md)

## 当前主线与最新进展

**10-27 第三十一回合：** [A-LOCAL23](FULL_RN_FUTURE_LOCALIZATION.md)从实际入射质量耗散取得全半径Ψ增长预算，再为固定RN完整Green核建立空间一致负时间界。联合截断的R端抵消、对角项和外段Z全部保留，人工未来截断可在扩张过去窗的全A中移除；未来体源及真实W的滤波功能也能局部化，不需实际A/D/K/H。真实过去W、A/D闭合、高频和完整Goal A仍OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_full_rn_future_localization.py)、[报告](FULL_RN_FUTURE_LOCALIZATION_CHECKS_2026-10-27.json)、[检查点](RECOVERY_CHECKPOINT.md)。
**10-27 第三十回合：** [A-CONE22](INFINITE_RADIAL_RN_BODY_TRANSFER.md)用完整RN光程、主项/余项分解与到达时间密度，关闭明确双尺度源输入下的无限径向低频体源全A幅度及辐射D导数；常数不依赖径向/时间支撑上端。RN20的实际A/D/K前提给指定三次体误差，未兑现这些前提本身。实际W、完整有限r时间截断、高频、强终态和同曲线仍OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_infinite_radial_rn_body.py)、[报告](INFINITE_RADIAL_RN_BODY_CHECKS_2026-10-27.json)、[检查点](RECOVERY_CHECKPOINT.md)。
**10-26 第二十九回合：** [A-SPACE21](FINITE_RADIUS_RN_GREEN_AND_LOCAL_BODY.md)推导完整有限半径RN Green核，核对ds源测度、对角跳跃、真实W及散度端项，保留两种RN光程延迟。全观察空间的两尺度核使固定径向源区和有效边界非线性校正在RN20的A/D/K输入下受控，不再要求这些项的时间导数。无限径向γ源范数仍可对数发散；实际W、完整体源、高频和全部Goal A验收仍OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_finite_radius_rn_green.py)、[报告](FINITE_RADIUS_RN_GREEN_CHECKS_2026-10-26.json)、[检查点](RECOVERY_CHECKPOINT.md)。
**10-26 第二十八回合：** [A-RN20](STATIC_GEOMETRY_FREEZING_AND_RN_ROBIN.md)同时冻结有限窗实际几何/电势，误差获得U^(−1+2η)时间因子，使指定非截断源的几何项也成为A/D条件下的三次量。闭上半平面Volterra、长Mellin比较及锚定相位控制把平直物理Robin的近零优势推广到充分远的固定RN参考，未预设M_S≥|Q_S|。实际统一输入、真实迹、完整有限r体源/高频、强终态和同曲线仍OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_static_geometry_rn_robin.py)、[报告](STATIC_GEOMETRY_RN_ROBIN_CHECKS_2026-10-26.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-24 第二十七回合：** [A-COM19](ORDINARY_TIME_COMMUTATION_AND_ENERGY_GATE.md)在固定Bondi规范中用普通时间交换及原波式消去二阶低层场强迫；实际A/D/K输入支付加权时间可积的体强迫，补足其径向L¹，并给交换场幅度及保留未知H_P的二阶辐射桥。真实内端仍含∂uW；P/Q_u并非原Maxwell配对，指定静态参考能量还有严格负测试值，不能自动套正能量传播。实际H_P/载频、全A/高频、强终态和同曲线仍OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_ordinary_time_commutation.py)、[报告](ORDINARY_TIME_COMMUTATION_CHECKS_2026-10-24.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-24 第二十六回合：** [A-JET18](TIMELIKE_CHARGE_AND_COEFFICIENT_JETS.md)用实际固定世界管Maxwell流及径向改进，将A/D/K条件下的有限窗电荷冻结和终电荷尾从U^(−h)提升到U^(−g)，g=1−2η；不预设Q_f。实际一阶系数时间变差可由同组输入支付，首次迹交换仍显式含F″。源范数的径向转换在半阶饱和，不能把更强时间幂直接同阶转为空间增益。统一A/D、实际载频迹条件、有限r体源/高频、强视界及同曲线仍OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_timelike_charge_jets.py)、[报告](TIMELIKE_CHARGE_JETS_CHECKS_2026-10-24.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-24 第二十五回合：** [A-TRACE17](FULL_SPACE_PHYSICAL_TRACE_AUDIT.md)审计有限r的物理W传递：对数振荡核使单独H_η不足以统一支付全A；反控制是辅助输入族，非D001反例。两尺度核与有界原函数则给一阶低频时间正则性加分离载频通道下的纯边界全A映射，允许慢变载频而不预设Q_f。实际新增迹条件、有效边界校正、有限r体源/高频及强终态仍OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_full_space_trace.py)、[报告](FULL_SPACE_TRACE_CHECKS_2026-10-24.json)、[来源收据](DLMF_MELLIN_GAMMA_RECEIPT_2026-10-24_R25.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-24 第二十四回合：** [A-UPPER16](UNIFORM_UPPER_KERNEL_AND_FUTURE_LOCALIZATION.md)以官方Kummer–Euler公式和端点分析建立完整P的空间一致上半/负时间界，保留普通M的Γ(b)。实际质量支付晚交换子在扩张过去窗的完整辐射尾移除；新Maxwell势L²余额还支付未来非线性体源。实际Green兼容性使未来W的滤波功能也可局部化，未预设或证明W点态衰减。真实过去H、全A/高频、主返回D及强终态仍OPEN。解析证据 INTERNAL_AUDIT；[核验](verify_uniform_upper_kernel.py)、[报告](UNIFORM_UPPER_KERNEL_CHECKS_2026-10-24.json)、[来源收据](DLMF_KUMMER_EULER_RECEIPT_2026-10-24_R24.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-24 第二十三回合：** [A-RETURN15](RETURNED_REMAINDER_CONE_ESTIMATE.md)以去相位符号、实际加权源和返回锥密度，控制两个返回余项的完整rad,η范数，不要求源时间导数。电荷的严格h余量吸收密度log损失；合并既有结果，全部非截断低频体源误差的辐射幅度已在明确A/D/K输入下受控。返回主项D尾、实际晚截断、空间一致单侧核、全A/高频/真实H及Goal A仍OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_returned_remainder_cone.py)、[报告](RETURNED_REMAINDER_CHECKS_2026-10-24.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-24 第二十二回合：** [A-GREEN14](PHYSICAL_TRACE_GREEN_AND_DELAY.md)建立物理W输入的完整体源Green公式。散度源内端项与实际W匹配联合后，边界Z精确抵消；真实W与其余源全部保留。核中出现延迟2(r−R_*)的返回主项，不能套旧瞬时源范数；实际锥包络加两侧卷积已给该主项的幅度小系数/三次误差界。返回余项、辐射导数、体源未来截断与全A/高频仍OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_physical_trace_green.py)、[报告](PHYSICAL_TRACE_GREEN_CHECKS_2026-10-24.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-24 第二十一回合：** [A-ROBIN13](PHYSICAL_TRACE_LOW_FREQUENCY.md)对外加Coulomb波算子的物理W输入证明近零上半平面分母无零点；系数优势与旧Dirichlet反例相反。低频边界核的负时间尾快速衰减，实际W通过精确非齐次式匹配，没有替换D001或将实际W设零。实际质量已能使新分解中的世界管晚截断在完整辐射尾范数趋零。体源Green核、全频稳定/实际W尾及完整Goal A仍OPEN。解析证据 INTERNAL_AUDIT；[核验](verify_physical_trace_low_frequency.py)、[报告](PHYSICAL_TRACE_CHECKS_2026-10-24.json)、[检查点](RECOVERY_CHECKPOINT.md)。R20中断后的快照也已补齐。

**10-23 第二十回合：** [A-CUTOFF12](RADIAL_DIVERGENCE_AND_SPECTRAL_CUTOFF.md)利用实际晚截断源的径向导数结构，将导数移到参考核，保留无穷远与世界管两端项。实际质量支付全部输入，不需统一A/H；截断导数贡献在|ω|≥T⁻ᵅ、α<1的L²谱带趋零，幅度在α<1/3趋零。阈值只是充分范围。超低频及其向完整加权点态尾的转移仍OPEN，低频集中反控制防止范数替换；不据此升级全空间A、高频、强终态或Goal A。解析证据 INTERNAL_AUDIT，[核验](verify_spectral_cutoff.py)、[报告](SPECTRAL_CUTOFF_CHECKS_2026-10-23.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第十九回合：** [A-BODY11](ACTUAL_BODY_SOURCE_AND_TERMINAL_FREEZING.md)给整个低频体源的统一源核；以每个有限窗的实际末端Bondi参数作固定远区参考，将长程电荷差变成时间衰减并转为空间可积因子。实际误差得到度量小系数加三次电荷项，不预设Q_f，也不假设瞬时M_B≥|Q_B|。完整截断源范数不能仅靠增大T趋零；另一方面，实际质量约束给精确径向Z的L²界，使晚截断在未加权时空L²中趋零，滤波辐射侧也有局部极限。真实因果/内区供能、强尾范数转移、全空间A/高频/统一A/H仍OPEN。解析证据 INTERNAL_AUDIT；[核验](verify_actual_body_source.py)、[报告](ACTUAL_BODY_SOURCE_CHECKS_2026-10-23.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第十八回合：** [A-SYMBOL10](LOW_FREQUENCY_SYMBOL_AND_TIME_TRANSFER.md)对固定 q>1/2 参考模式证明世界管低频参数导数界，再给低频时间核及完整边界辐射贡献的尾映射。实际边界动量的时间导数经分部转到核，不额外要求真实迹时间导数；未来卷积段保留。幅度阶数单独不够、η=0一般端点有log损失的反控制分列。体源贡献、全空间A、实际统一A/H及强终态仍OPEN；未将固定q的频率导数用于时变q。解析证据 INTERNAL_AUDIT，[核验](verify_low_frequency_symbol.py)、[报告](LOW_FREQUENCY_SYMBOL_CHECKS_2026-10-23.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第十七回合：** [A-TRACE09](WORLD_TUBE_RADIATION_TRANSFER.md)将实际辐射导数范数 D 化为真实世界管通量 H 加幅度 A 的径向小修正，并推导保留完整 Cauchy 迹与未来截断的辐射恒等式；散度源主振荡抵消消除虚假的无穷对数。反驳审计给出外加 Coulomb 反射模型的解析增长模，排除默认稳定的反射替代；该模型不是完整 D001，也不是 Goal A 反例。实际统一 A/H、时间尾与强视界仍 OPEN。逻辑/证据/审计分列，解析结论 INTERNAL_AUDIT；[核验](verify_world_tube_radiation.py)、[报告](WORLD_TUBE_RADIATION_CHECKS_2026-10-23.json)、[来源定位](DLMF_WHITTAKER_RECEIPT_2026-10-23_R17.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第十六回合：** [A-MOD08](MODULATED_BONDI_RADIAL_IMPROVEMENT.md)在实际 A/K 输入下由输运推出径向导数尾，再以约束改进 Q−Q_B、光学因子、项目质量及势余项。有限时 M_B(u)、Q_B(u) 进入主项后，外向区势误差多一阶径向衰减；不需预设 Q_f。参数/相位时间变差可由 A/D 支付，但只在有限增长锥内，调制系数不能当静态电真空或默认处于黑洞RN参数区间。实际统一 A/D、调制尾定理及强视界仍 OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_modulated_bondi_radial.py)、[报告](MODULATED_BONDI_RADIAL_CHECKS_2026-10-23.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第十五回合：** [A-CARRIER07](TAIL_CURRENT_AND_CARRIER_AUDIT.md)定向复核 Gajic II 主文：一般极端参考载频可使 R14 的正时间权平方预算发散，旧条件性证明保留，但不再默认由通用尾定理支付。改用实际幅度 A_η 与允许 u⁻¹ 载频的辐射导数 D_η；实际波式的精确径向核给电流因子抵消，二次控制全远区电荷/势，并条件性给终 Q 与尾界。A/D 的真实 PDE 估计仍 OPEN，强视界验收未降低。解析证据 INTERNAL_AUDIT，[核验](verify_tail_current_carrier.py)、[报告](TAIL_CURRENT_CARRIER_CHECKS_2026-10-23.json)、[主文收据](RN_TAIL_PRIMARY_RECEIPT_2026-10-23_R15.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第十四回合：** [A-INNER06](MELLIN_INNER_TRANSFER_AND_CHARGE_BOOTSTRAP.md)以 Mellin 正振荡能量接上参考 q>1/2 的长内侧区，给外向模式固定半径 O(sqrtω) 界；源项的真实 log 区间代价及交叉 Wronskian 缺口保留。沿实际过去入射线定义带权标量预算 B_σ，证明其有限窗连续，并由它统一控制幅度、电荷偏移和 LOW05 势条件；若全未来兑现还可给终电荷非零界。B_σ 的 PDE 小性仍 OPEN，未据此升级全终态或三分支。解析证据 INTERNAL_AUDIT，[核验代码](verify_mellin_charge_bootstrap.py)、[报告](MELLIN_CHARGE_BOOTSTRAP_CHECKS_2026-10-23.json)含三个有限参考对照，[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第十三回合：** [A-LOW05](LOW_FREQUENCY_SHELL_AND_ACTUAL_ERRORS.md)证明固定 RN 漂移低频壳层的统一传递、散度源估计及参考外向模式界；常数对 ω→0 一致。实际算子差精确改写为一阶散度源，临界带源范数可直接由系数幅度与全频率标量范数支付，无需先控 Q_t/γ 或假设带保持。实际有限时间应用保留重叠区、截断和全频率输入；质量只自动支付度量误差，Coulomb 势全未来 bootstrap 仍 OPEN。解析证据 INTERNAL_AUDIT，[核验](verify_low_frequency_shell.py)与[报告](LOW_FREQUENCY_SHELL_CHECKS_2026-10-23.json)含三个有限 RN ODE 控制，不认证完整 PDE/Goal A。[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第十二回合：** [A-COUL04](COULOMB_RENORMALIZATION_AND_MELLIN_GATE.md)完成实际库仑功分部及光学时间导数的一阶表示。扣库仑后的指定标量能量在 |eQ_*|>1/2 可为负；固定 e=3/5 的严格 RN 有理余量经 C∞ 逼近和实际径向约束小扰动保留，否定其自动正性。相应标量 r^p 流在 |eQ_*|≥1/2 无正统一控制，完整 RN 频率式定位 r≈q/ω 的漂移低频壳层。结论只排除指定路线，不证明失稳或 Goal A；全时间辐射和三分支仍 OPEN。解析证据 INTERNAL_AUDIT，[核验代码](verify_coulomb_mellin_gate.py)、[报告](COULOMB_MELLIN_GATE_CHECKS_2026-10-23.json)、[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第十一回合：** [A-FAR03](FAR_ZONE_RP_AND_COULOMB_BALANCE.md)由实际质量预算与 AF 锚定证明世界管幅度/电荷的全时间一致界；Maxwell 完成的 r^p 流在足够大半径给出无需小 eM 的远区积分正性，所有真实内边界保留。精确 RN 审计表明静态库仑体积分由同样增长的内边界支付，不能删除；带权质量流扣除库仑库后仍有无符号的电磁功。实际加权辐射/终 Q/RN 仍 OPEN。新解析证据 INTERNAL_AUDIT，[核验代码](verify_far_zone_rp.py)与[报告](FAR_ZONE_RP_CHECKS_2026-10-23.json)只认证列明恒等式和反控制。[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第十回合：** [A-BOND02](ACTUAL_BONDI_COMPLETENESS_BRIDGE.md)对 ESC01 新完整形成种子兑现实际 I⁺/Bondi 桥：质量约束控制光学因子，源仿射完整性与单位 Bondi 时间无界相认；实际波式和入射质量通量经两次电荷改进，给每个有限 Bondi 窗口的光滑 I⁺ 与 Q_B/M_B 提取。质量严格有序极限 M_f=𝔐_K∈[R/2,M_ADM]，不再只作符号接口。晚时 Q_f/视界一致性/RN/三分支仍 OPEN；边界 ODE 反控制排除“有限能量+F→0即Q_f存在”。解析证据 INTERNAL_AUDIT，[核验](ACTUAL_BONDI_BRIDGE_CHECKS_2026-10-23.json)不认证实际新种子的数值 PDE。[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第九回合：** [A-ESC01](CENTER_ESCAPE_CHARACTERISTIC_EXTENSION.md)给有限边缘种子的另一种 AF 补全：在稍早锥上以 O(δ⁴)+O(δ²/L) 聚焦预算关断标量，保留非零横向场，构造与初始中心相连的实际 r=4R 点，并将新 M_ADM 控制为 R+o(1)。由旧因果判据兑现整片可见与规则中心视界起源，I⁺ 完整性先保持源定理的精确含义。旧补全没有被升级；新形成族仍无极端/RN 终态或色散负侧。[核验](CENTER_ESCAPE_EXTENSION_CHECKS_2026-10-23.json)只有精确式及三个人工角点控制；新解析证明 INTERNAL_AUDIT，完整 A1–A6 OPEN。[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第八回合：** [A-CENTER03](REGULAR_CENTER_BONDI_MATCHING.md)补齐正质量有限 Bondi 外段的正则中心约束实现：带电壳精确补 Q，中性壳严格单调调 m，保持 f>0；可保留有严格质量预算的既有强场内核，并给固定 X⁶ 的光滑参数族。重读并归一化 Kommemi Proposition2.1 后兑现有限外区到完整 Cauchy 发展的转移。解析稿仍 INTERNAL_AUDIT；[核验](REGULAR_CENTER_MATCHING_CHECKS_2026-10-23.json)只认证列明恒等式/六项有限 ODE 控制。完整实际视界、全未来和三分支仍 OPEN；有限信号及中心填充均不选择极端端点。[检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第七回合：** [A-EF01](REGULAR_EF_INVERSION_AND_TRANSVERSE_GATE.md)将反演改写到规则 EF 规范，明确横向量 Z−MF 和退化权重，构造首矩消失但电荷通量非零的成对信号。[A-BON01](FINITE_BONDI_EXTERIOR_REALIZATION.md)进一步证明有限 Bondi 窗口的实际非线性 AF 外区实现及完整 AF Cauchy 外段，电荷/质量剩余约束传播已精确核验。尚未填正则中心，未建立实际视界转移或固定内半径全未来；两类新证据均不完成 Goal A。[EF核验](REGULAR_EF_INVERSION_CHECKS_2026-10-23.json)、[约束核验](FINITE_BONDI_CONSTRAINT_CHECKS_2026-10-23.json)、[当前检查点](RECOVERY_CHECKPOINT.md)。

**10-23 第六回合：** [A-MOR01 实际全域乘子](GLOBAL_COVARIANT_MORAWETZ.md)补出带 Maxwell 反馈的径向动量/乘子及所有有限域边界。中心/AF 锚定在自由波控制中给全未来幅度迹 ≤4E₀；此控制未移植到非线性强场。对 RN 外部证明常规有界 h、g=hf/r 这一类无法取得全域点态幅度正性，避免继续调同类权重。固定 ERN 的带电反演需复共轭与频移，已精确核验。[核验报告](GLOBAL_COVARIANT_MORAWETZ_CHECKS_2026-10-23.json)与[检查点](RECOVERY_CHECKPOINT.md)保留实际/参考/控制三种范围，Goal A 仍 OPEN。

**10-23 第五回合：** [A-SOURCE01 全局源审计与实际能量](GLOBAL_RN_SOURCE_NORM_AUDIT.md)完成固定 RN 波算子号数/无量纲耦合映射，核对原源权重为乘积。明确区分尾部有限与同阶吸收，并用权重/高频反驳测试否定两个直接黑箱步骤。改用实际连接交换后无顶阶标量损失；实际 Maxwell 功项可精确取消，Einstein 质量流给有明确非退化条件的正物理能量控制。幅度可积衰减和全局边界仍缺。[核验报告](GLOBAL_RN_SOURCE_NORM_CHECKS_2026-10-23.json)不认证全局 PDE，目标 A 仍 OPEN。

**10-23 第四回合：** [A-TRACE01 外环乘子审计](EXTERIOR_TRACE_MULTIPLIER_AUDIT.md)推导实际几何上的约化带电波方程、含电场/边界的乘子和固定面积迹估计。精确局部 Schwarzschild 常值标量反例否定“仅靠有界质量与物理导数通量控制幅度迹”；因此下一路线须闭合全局边界。共同共形图与径向锚定规范给一阶源分解，消除有限环未交换方程的表面导数损失；全局带权源仍 OPEN。已重读固定 RN 积分能量定理的适用定位，不作非线性应用。[新核验](EXTERIOR_TRACE_MULTIPLIER_CHECKS_2026-10-23.json)与[检查点](RECOVERY_CHECKPOINT.md)保存范围和失败记录。

**10-23 第三回合：** [A-OPT01 §9 的出射内层估计](INCOMING_OPTICAL_DEPTH_GATE.md)通过实际出射内边界抵消原正入流，用固定半径 Hawking 质量平衡和协变 Hardy 估计把 O9 体积分化为一个外端幅度平方迹。给出明确小性条件和 O13/O14 常数；既有出口衰减可经 O15/O16 支付该类迹，但未证明目标族进入这些类。[新核验报告](NULL_INNER_OPTICAL_BOOTSTRAP_CHECKS_2026-10-23.json)含质量类型、任意移动端点、相位、定性衰减不保 L² 等反驳检查。当前缺口为实际带的进入控制与外端迹，目标 A 仍 OPEN。

**10-23 第二回合：** [A-OPT01 入射光学深度门槛](INCOMING_OPTICAL_DEPTH_GATE.md)用规范不变的径向积分替代二阶规范界，给出低电荷层的 f 正下界、规则中心的内部超单位电荷必要条件、有界质量不能控制光学深度的精确反例，以及保留端点/电荷功的移动层演化式。四次有限入射诊断加密残差缩小约3.8–4.9倍，仍为 EXPERIMENTAL；没有发现正质量极端端点。[解析/负对照核验](INCOMING_OPTICAL_DEPTH_CHECKS_2026-10-23.json)、[有限报告审计](INCOMING_OPTICAL_SCREEN_AUDIT_2026-10-23.json)和[当前检查点](RECOVERY_CHECKPOINT.md)列明范围与下一估计。

**10-23 恢复与解析推进：** [不可擅改契约 GA-2026-10-16-v1](ACCEPTANCE.md)展开 A1–A6 的固定定义；[A-MARG02 有限边际刚性](FINITE_MARGINAL_RIGIDITY.md)证明实际无陷俘开集内 λ=0、ν<0 必有 |Q|=r，给出横向仿射曲率分类及近边际定量判据。对最终视界的应用仍有因果身份、完整性及一致控制前提。局部命题为 PROVED/ANALYTIC/INTERNAL_AUDIT，目标应用为 CONDITIONAL，目标 A 为 OPEN。[核验](verify_finite_marginal_rigidity.py)只覆盖精确代数和负对照；[检查点](RECOVERY_CHECKPOINT.md)恢复依赖、失败尝试、源哈希及下一具体动作。

**10-22 保持电荷的构造推进：** [A-DIR01 方向族与中心聚焦筛选](CHARGE_PRESERVING_DIRECTION_FAMILY.md)给出保持完整初始电荷分布的光滑方向族。固定 A=2/5、ω=3/20、R=10、W=4，整条 d∈[−1,1] 在列明算术假设下有全半径 f>10⁻⁷；[初值证书](CHARGE_SHELL_INITIAL_CERTIFICATE_2026-10-22.json)不依赖浮点 ODE。[有限筛选](CHARGE_SHELL_SCREEN_SUMMARY_2026-10-22.json)显示较强出射改善中心样本但排走核心质量，较强入射仍出现低电荷中心负信号。尚未获得正质量长期滞留或目标 A；下一步需改变电荷到达分布而非只细分方向参数。

**10-22 最新更正：** [A-AXIS01 正则轴线接口与中心筛选](REGULAR_AXIS_CAUCHY_SCREEN.md)补入晚期中心区后，s=1001/1000 的三档计算均出现强负 λ，不能再作为已通过早期筛选的候选。完整初值认证仍有效；实际陷俘与三分支均未证明。[轴线实现](centered_cauchy_diamond.py)、[精确极限检查](verify_regular_axis_limits.py)、[代数报告](REGULAR_AXIS_LIMITS_CHECKS_2026-10-22.json)、[已知解检查](verify_centered_cauchy_diamond.py)、[基准报告](CENTERED_CAUCHY_DIAMOND_CHECKS_2026-10-22.json)、[结果汇总脚本](summarize_centered_cauchy_screen.py)及[三档中心记录汇总](CENTERED_CAUCHY_SCREEN_SUMMARY_2026-10-22.json)均已归档。

自 10-17 采用 [全局阈值优先路线](GLOBAL_THRESHOLD_ROUTE.md)：先研究完整色散出口、形成侧及边界，再识别极端性和同一条合法初值曲线。形状扫描、有限域证书与横向匹配保留为工具。

| 进展 | 已有内容与前提 | 未闭合项 |
|---|---|---|
| 10-20：[A-PATH01 约束收缩与首个边界](CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md) | 一般非零角向外曲率下保持全参数初始未陷俘的路径；接入既有小数据链和陷俘上端后，可选首个 ∂D 候选，其有限规则未来无严格陷俘 | 候选定位、是否在 D 外、真正形成、正质量极端 RN、紧邻右侧亚极端终态 |
| 10-20：[A-CAUS01 全局因果接口](MARGINAL_SEED_CAUSAL_INTERFACE.md) | 条件于 A-AF03 实现，外部定理给非空黑洞区、该定理意义的完整 I⁺及正几何 Hawking–Bondi 质量下界 | 初始中心逃逸见证、真正形成、目标全部边界与终态条款；保留边缘球仅改变 AF 外尾不能产生色散负侧 |
| 10-20：[A-END01 横向曲率终态门槛](FINITE_MARGINAL_TAIL_GATE.md) | 两个旋转种子的非零末端 D_uφ 有有理包络；若无陷俘边缘锥成为最终事件视界，其横向 Ricci 阻碍目标 C² RN 收敛 | 该锥的事件视界身份；尚非候选的全局排除 |
| 10-18：[A-AF03 保留横向回流的 AF 实现](AF_REALIZATION_WITH_TRANSVERSE_FLUX.md) | 两个从开启段充电的光滑旋转种子，不要求横向 jets 消失的非有效完整 AF 实现论证稿 | 有效共同常数、完整二维筛选、真正形成、终态与临界连接 |
| 10-18：A-EXIT01–23 出射出口与中心链 | 从完整出射壳约束推进到 I⁺、零 Bondi 两次极限、二阶局部衰减及共同支撑类相对稳定出口的内部论证 | 分析链独立复核、有限 Cauchy 适定性接口、连接正质量临界端点和形成侧 |

## 专题导航

2026-10-22 新增：[规范 Cauchy 有限未来筛选与参数延伸](CANONICAL_CAUCHY_EARLY_SCREEN.md)。新候选 A020_W8，s=1001/1000，取得[完整初值区间证书](ROTATING_AF_BARRIER_A020_W8_S1001_N4096_2026-10-22.json)，并在 t≤4 三档网格及 t≤8 单档有限楔区保留正 λ 样本。[初始化](canonical_cauchy_data.py)、[演化器](charged_cauchy_diamond.py)、[基准检查](verify_charged_cauchy_diamond.py)、[测试记录](CHARGED_CAUCHY_DIAMOND_CHECKS_2026-10-22.json)、[有限结果汇总脚本](audit_canonical_cauchy_screen.py)与[汇总记录](CANONICAL_CAUCHY_SCREEN_AUDIT_2026-10-22.json)均归档；未来结论仍是 E0，未认证连续无陷俘或三分支终态。历史源码及所有原始 JSON/NPZ 见完整索引。

2026-10-21 新增：[A-AF04 具体空间数据与 AF 实现](ROTATING_CAUCHY_AF_IMPLEMENTATION.md)把两个旋转种子的过去薄带接到光滑自由函数及完整空间约束重求解；[独立核验](verify_rotating_af_interface.py)与[报告](ROTATING_AF_INTERFACE_CHECKS_2026-10-21.json)覆盖转换恒等式、负 u 已知解比较、加密和独立质量变量复算。结果为 E0 新初值；连续半径认证、原种子转移、重构后未来筛选与三分支仍缺。

同日后续：[A-AF05 连续半径认证](ROTATING_AF_CONTINUOUS_BARRIER.md)将两组自由函数冻结为精确二进有理系数及理想平坦权重定义。每组 3,555,328 个闭区间通过[下屏障检查](certify_rotating_af_barrier.py)，在列明算术假设下得到全半径及整条收缩路径 f>3/10000，兑现这两组新初值的完整 AF 合法性；[独立测试记录](ROTATING_AF_BARRIER_CHECKS_2026-10-21.json)保留核验范围。早期未来筛选、原种子转移和三分支仍未完成。

| 主题 | 研究入口 | 代码与证据入口 / 范围 |
|---|---|---|
| 初值与尾部障碍 | [A-IC01](INITIAL_DATA_AND_TAIL_OBSTRUCTION.md)、[A-INC01](INCOMING_CONSTRAINT_FAMILY.md)、[连续半径预算](EXACT_INITIAL_BUDGET.md)、[A-TAIL01](BONDI_TAIL_OBSTRUCTION.md) | [初值生成器](incoming_family.py)、[约束和平衡律复算](verify_research.py)；初值预算不证明未来命运，尾部论证有额外连续性前提 |
| 有限时间演化与主符号 | [A-EVOL01](POLAR_EVOLUTION.md)、[A-EVOL02](AREAL_SHIFT_EVOLUTION.md)、[A-HYP01](HARMONIC_PRINCIPAL_SYMBOL.md) | [极坐标](polar_evolution.py)、[shift 演化](areal_shift_evolution.py)、[主符号核验](verify_harmonic_symbol.py)；数值基准与正半径代数 |
| 小数据完整色散 | [A-GEO01](CAUSAL_COMPLETENESS.md)、[A-RET01](RETARDED_CAUCHY_BOUNDS.md)、[A-KL01](KL_INTERFACE_AUDIT.md)、[A-NULL01](SMALL_DATA_NULL_INFINITY.md)、[A-SD01](SMALL_DATA_DISPERSION.md) | [因果代数](verify_causal_algebra.py)、[零无穷远代数](verify_null_infinity_algebra.py)；指定小数据分析链，不可直接推广到正质量端点 |
| 有限耦合与横向匹配 | [A-HOR01](SMOOTH_HORIZON_CONSTRAINT_SEED.md)、[A-SCH01](SCHNEIDER_2026_INTERFACE_AUDIT.md)、[A-JET01](FIRST_TRANSVERSE_JET.md)、[A-JET02](SECOND_TRANSVERSE_JET.md)、[A-JET03](TWO_PULSE_SECOND_JET.md) | [一阶](verify_first_jet.py)、[二阶](verify_second_jet.py)、[双脉冲核验](verify_two_pulse_second_jet.py)；有限阶 jets 不等于完整 RN 或终态 |
| 中性筛选与有限域认证 | [A-EVOL03](NEUTRAL_CHARACTERISTIC_METHOD.md)、[A-SCREEN01](NEUTRAL_CAUSAL_SCREEN.md)、[A-GOUR01](RATIONAL_GOURSAT_CERTIFICATION.md)、[A-BOUND01](ONSET_BOUNDARY_CERTIFICATION.md)、[A-GRID01](FULL_TRANSPORT_GRID_CERTIFICATION.md) | [网格核验](verify_interval_transport_grid.py)、[147456 单元证书](FULL_TRANSPORT_GRID_CERTIFICATE_2026-10-17.json)；冻结 ε=0.05 实验、列明 binary64 假设，终点 2m−r>0.21144；不认证原 η 种子 |
| 参数转移与新形状 | [A-TRANSFER01](THIN_ONSET_PARAMETER_TRANSFER.md)、[A-NEW01/02](NEW_SHAPE_CONSTRAINTS.md) | [转移核验](verify_thin_parameter_transfer.py)、[新形状核验](verify_new_shape.py)、[jets 核验](verify_new_shape_jets.py)；原路线条件性筛选与新形状预穿轴证书 |
| 带电特征与区间工具 | [A-CHG01](CHARGED_CHARACTERISTIC_METHOD.md)、[A-CHG02](CHARGED_FINITE_DOMAIN_STABILITY.md)、[A-CHG03](CHARGED_U_CONSTRAINED_FORMULATION.md)、[高阶比较](CHARGED_SCREEN_REFINEMENT.md)、[冻结证书尝试](FROZEN_CHARGED_CERTIFICATION.md) | [十二变量核](charged_interval_kernel.py)、[u 约束核](charged_u_interval_kernel.py)、[Lobatto 比较](charged_lobatto.py)；开启/充电段有局部证书，关断与完整带电全域认证仍缺 |
| 不同充电候选与 AF 实现 | [旋转种子与指数尾](ALTERNATIVE_CHARGED_CANDIDATES.md)、[A-AF01](AF_OUTER_EXTENSION.md)、[A-AF02](PAST_COLLAR_AND_AF_REALIZATION.md)、[A-AF03](AF_REALIZATION_WITH_TRANSVERSE_FLUX.md) | [候选验证](validate_alternative_candidates.py)、[整锥约束](verify_early_charged_constraints.py)、[AF 回流核验](verify_af_transverse_flux.py)；整锥有理证书、二维 E0 与非有效实现须区分，指数尾失败保留 |
| 最新边界与终态接口 | [A-PATH01](CONSTRAINT_CONTRACTION_AND_FIRST_BOUNDARY.md)、[A-CAUS01](MARGINAL_SEED_CAUSAL_INTERFACE.md)、[A-END01](FINITE_MARGINAL_TAIL_GATE.md) | [精确收缩](verify_constraint_contraction.py)、[实现核验](verify_contraction_implementation.py)、[末端通量证书](ROTATING_TERMINAL_FLUX_N2048_2026-10-20.json)；带前提的必要条件与边界候选 |

## 出射出口与中心分析链：A-EXIT01–23

[10-18 同步快照](SYNC_PROGRESS_2026-10-18.md) 中截至 A-EXIT08 的范围是历史范围。当前文件已推进至 A-EXIT23；各稿结论仍依赖其前置分析。

| 阶段 | 按编号阅读 |
|---|---|
| 出射壳与回流入口 | [01 完整约束](OUTGOING_LARGE_RADIUS_EXIT.md) → [02 回流](OUTGOING_BACKSCATTER_BUDGET.md) → [03 条带几何](OUTGOING_STRIP_BOOTSTRAP.md) → [04 Cauchy 接口](OUTGOING_CAUCHY_STRIP.md) → [05 内侧迹](OUTGOING_INNER_TRACE.md) |
| 中心入口与预算 | [06 导数障碍](CENTER_WEIGHTED_NORM_AUDIT.md) → [07 BV 迹](CENTER_BV_TRACE.md) → [08 零锥范数](CENTER_CONE_NORM.md) → [09 通量](CENTER_EVOLUTION_FLUX.md) → [10 同权 bootstrap](CENTER_WEAK_WEIGHT_BOOTSTRAP.md) |
| 延拓、重构与流 | [11 回流锥](OUTGOING_STRIP_CONTINUATION.md) → [12 重构](CENTER_INTEGRAL_RECONSTRUCTION.md) → [13 约束传播](CENTER_CONSTRAINT_PROPAGATION.md) → [14 局部特征](CENTER_LOCAL_CHARACTERISTICS.md) → [15 全时间流](CENTER_GLOBAL_REDUCED_FLOW.md) |
| 正则性与完整性 | [16 高阶正则](CENTER_HIGHER_REGULARITY.md) → [17 Cartesian 中心](CENTER_CARTESIAN_REGULARITY.md) → [18 因果完整](CENTER_CAUSAL_COMPLETENESS.md) → [19 拼接](OUTGOING_GLOBAL_PATCH.md) → [20 I⁺ / 零 Bondi](OUTGOING_NULL_INFINITY.md) → [21 最大发展](OUTGOING_MAXIMAL_FUTURE.md) |
| 工作范数与扰动 | [22 二阶衰减](OUTGOING_LOCAL_DECAY.md) → [23 相对稳定出口](OUTGOING_SUPPORTED_STABILITY.md) |

各 `verify_outgoing_*.py`、`verify_center_*.py` 及报告见 [完整索引](FILE_INDEX.md)。代数核验不替代适定性、全局估计或外部定理前提的解析复核。

## 阶段与文件约定

- **10-16**：初值、演化基准、小数据链、有限耦合种子及早期筛选。
- **10-17**：有限域认证、参数转移、新形状与带电工具；改为全局阈值主线。
- **10-18**：出射出口与中心链推进至 A-EXIT23；保留横向回流的 A-AF03 实现。
- **10-20**：终态门槛、全局因果接口、收缩路径与首个边界候选。
- **10-21**：两个旋转来源候选的具体光滑自由函数、约束数值重求解、规范化初值的连续半径正性认证及整条合法收缩路径；尚未认证新初值的未来。

当前优先任务见 [路线图](../../ROADMAP.md)。边界候选不自动在 D 外；初始未陷俘不等于整片逃逸；有限域计算不认证最终极端性。

研究稿、脚本、JSON、日志与数据保留原路径和内容，分类见 [完整文件索引](FILE_INDEX.md)，维护见 [例行任务规则](../../task-rules.md)。运行环境按需使用 [NumPy](requirements-evolution.txt)、[NumPy / SciPy](requirements-shooting.txt) 或 [SymPy](../../experiments/requirements-kernel.txt)；初值符号约束与精确收缩核验也需要 SymPy。具体命令、输出路径和认证范围以各稿及脚本为准。

历史复算命令、失败记录和当轮来源核对保存于 [整理前首页](PROGRESS_ARCHIVE_2026-10-20.md)。其中 PR / 分支同步叙述仅为历史记录；本次导航整理未核实或执行远端同步。
