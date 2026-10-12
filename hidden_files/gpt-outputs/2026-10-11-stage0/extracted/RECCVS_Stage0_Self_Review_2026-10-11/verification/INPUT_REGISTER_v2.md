# 修订输入登记

定义、条件、内部模块、外部接口与证书分别解释；无项目前置不表示输入已验证。

| 输入/模块 | 准确陈述 | 前置 | 未验证状态 | 来源 |
| --- | --- | --- | --- | --- |
| SYS D001：EMCSF 归一化 | 四维、球对称、无质量复标量、无磁荷、固定 e≠0；签名与 Maxwell 取向按 MODEL.md。 | 无项目前置 | 定义输入 | `RECCVS/definitions/MODEL.md` L1–96 |
| TOPO D002–D003：强拓扑与色散集合 | 约束空间 X^s，s≥6；AF/Coulomb 主项单列；D 要求所有因果测地完整、完整 I+ 与衰减。 | 无项目前置 | 定义输入 | `RECCVS/definitions/MODEL.md` L1–96 |
| VIS D004：物理归一化与可见性 | 零线仿射或类时固有时；框架在固定物理初点归一化；可见性接到同一完整 I+。 | 无项目前置 | 定义输入 | `RECCVS/definitions/MODEL.md` L1–96 |
| REG_CENTER 实际正则中心 | 四维实际光滑正则中心；Q=O(r^3)、m=O(r^3)，中心取极限；使用时必须标明该中心事件仍属于实际发展。 | 无项目前置 | 条件输入 | `RECCVS/definitions/MODEL.md` L1–96 |
| POS_DOMAIN 旧复合条件（兼容ID） | 旧 POS_DOMAIN 等于 SMOOTH_DOMAIN 与 NU_NEG 的合取；修订核心图不再用它代替单独的光滑域。 | SMOOTH_DOMAIN、NU_NEG | 兼容ID；不作为最小前置 | `RECCVS/proofs/RECCVS_L008.md` L7–9 |
| INSEG 同一实际入射连通段 | 由 U=0 至所考察点的正半径前缀属于实际发展；只有明确到达正则中心时才使用中心端边项。 | 无项目前置 | 条件输入 | `RECCVS/inputs/AUDIT.md` L1–61；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/04_global_development_and_horizon.md` L1–284 |
| HORIZON 全零 jets 的晚时极端视界数据 | M=Q_H=1，U=0、t≥1：r=Q=Ω²=1、λ=φ=0、ν=-a0<0，横向标量 jets 全零；t=1 内侧数据属于同一光滑种子。 | 无项目前置 | 条件输入 | `RECCVS/inputs/AUDIT.md` L1–61；`RECCVS/proofs/RECCVS_L009.md` L1–154；`RECCVS/proofs/RECCVS_L012.md` L1–232 |
| OUTER_INPUT L014.1：抽象外边输入 | 固定 U=b 的全部 t≥1 外边：0<r_b≤R≤1、λ_b≥0、r_bλ_b≤C_b/t²、α_b/t²→h_b>0、α_b≥a0。 | 无项目前置 | 条件输入 | `RECCVS/proofs/RECCVS_L014.md` L1–118 |
| FINITE_INTERVAL 旧区间总称（兼容ID） | 中心区间与正半径区间是两个不同实例类型；使用 CENTER_INTERVAL 或 POS_INTERVAL，不能无条件互换。 | 无项目前置 | 兼容ID；修订核心图不使用 | `RECCVS/proofs/RECCVS_L018.md` L7–17；`RECCVS/proofs/RECCVS_L018.md` L95–101 |
| TAIL_LOWER 实际非零尾部下界 | 同一实际线对全部 t≥t1 存在且 r≥r_->0、Ω²≤C(1+t)^(-γ)、\|T\|≥c(1+t)^(-β)，c>0。 | 无项目前置 | 未取得的条件 | `RECCVS/proofs/RECCVS_L011.md` L1–81 |
| COMMON_FLOW 共同实际域与流误差 | 共同紧光滑域、同一物理初点/仿射归一化、Wilson 比较；强范数输入差到实际 W 的 C_flow 界。 | 无项目前置 | 未取得的条件 | `RECCVS/proofs/RECCVS_L022.md` L1–139 |
| MINK_FILL 完整 Minkowski 入射填充 | 从左端球面至中心的整条初始入射锥为 Minkowski；共同 Cauchy 实现包含相应有限依赖域。 | 无项目前置 | 尚未冻结的条件 | `RECCVS/proofs/RECCVS_L023.md` L1–175 |
| PERIODIC_PROFILE 周期族及矩坐标的完整假设 | 固定 K,T、c 的紧球和 τ 的正紧区间；所需 x/c 导数一致有界，共同端点开空隙；E、C 均值有统一正下界且 C≥0；精确半线矩 M_s(z_c)=c_s（1≤s≤K）；λ0<μ，τ0=-log(1-λ0/μ)/(2 Ebar0) 位于所选 τ 区间内部；核在所需 c 球上正。 | 无项目前置 | 抽象条件；L021可作为具体实例，尚无实际根认证 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/03_nonlinear_lifting.md` L3–7；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/03_nonlinear_lifting.md` L141–149；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/01_profile_construction.md` L69–83 |
| KDEF 形成核的完整定义 | I_C(x)=∫_0^x C+∫_x^∞e^(x-y)C；I_E(x)=∫_0^x(1-e^(y-x)/2)E+(1/2)∫_x^∞e^(x-y)E；𝒦=2λI_C-2I_E。 | 无项目前置 | 定义输入 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/01_profile_construction.md` L1–91 |
| FRBASE 有限阶提升的半径/参数基底 | 固定周期族与正紧τ区间；q=O(δ)、q-δp=O_C1(δ²)在全部x≥0一致；R、1/R及一次参数导数的统一界仅在0≤x≤L=mT的有限脉冲，不能移到无限半线。 | PERIODIC_PROFILE | 内部证明模块；未独立验收 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/03_nonlinear_lifting.md` L9–41 |
| FRPOS 周期后q下界及实际锥H正性 | 小δ下0≤q≤bδ在x≥0；q≥aδ仅对x≥T，且q(0)=0；无限周期H∞≥c*δt对0<t≤1；有限脉冲H_L≥H∞>0仅在其真实锥段t_-=exp(-L)≤t≤1，故ν<0。常数依赖固定族，有限成员的严格余量不宣称对m→∞不退化。 | FRBASE、KDEF、PERIODIC_PROFILE | 内部证明模块；未独立验收 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/04_radius_positivity.md` L3–13；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/04_radius_positivity.md` L65–93 |
| FENDPOINT 线性背景端点与三角可逆性 | 仅指 Volterra 多项式核、对角元非零及普通/协变标量 jets 三角转换；不包含非线性完整球面 ERN 匹配。 | SYS | 内部证明模块；未独立验收 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/02_endpoint_matching.md` L3–47 |
| FLIFT 局部真实分支及联合端点非退化 | 在精确矩坐标等完整假设下，用有限 jets 的 C1 收敛及线性三角端点可逆性得到每个充分大 m 的局部精确根和可逆 Jacobian。量词非有效；不提供任何固定 m 的认证根。 | PERIODIC_PROFILE、FJETS、FENDPOINT | 内部条件性存在模块；未独立验收/未有效化 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/03_nonlinear_lifting.md` L141–149 |
| FLOCAL Bondi 共同低阶寿命 | 有符号半径 Bondi 光滑解、完整正半径方程、固定阶中心响应及参数 C1 控制。 | SYS | 内部未独立复核 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/02_smooth_data_and_local_evolution.md` L1–498 |
| FSMOOTH 同一种子逐阶精确修复 | 以 FLIFT 非退化基点、完整有限阶球面匹配及 FLOCAL 固定阶响应/共同寿命为输入；执行每步精确根、共同终端空隙、可求和预算，才得到同一光滑种子。 | FLIFT、FSPHERE、FLOCAL | 内部证明模块；指定修复序列未计算/独立验收 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/02_smooth_data_and_local_evolution.md` L384–471 |
| FCENTER 实际四维中心、接合与 cap | 中心奇偶、实际笛卡尔实现、一次 ERN 边值实现、共同条带和顶点填充。 | FSMOOTH、FLOCAL、CHAR、CAUCHY | 内部未独立复核 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/03_regular_center_and_gluing.md` L1–374 |
| FGLOBAL 全局 Cauchy/外部/视界识别 | 实际保留域、单端 AF Cauchy 面、MGHD 识别、完整 I+ 及视界从中心出发。 | FCENTER、MGHD、CHAR | 内部未独立复核 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/04_global_development_and_horizon.md` L1–284 |
| I001 导入的光滑极端形成输入 | 固定 eM>1/2 的一份同一光滑、正则中心、单端 AF、真正塌缩形成解；全局标签/晚时精确 ERN 按导入稿。 | FGLOBAL | 组合性内部输入 | `RECCVS/inputs/AUDIT.md` L1–61；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/01_main_theorem.md` L1–230 |
| I002 限定视界类的严格半门槛 | 限定正则起源、有限时间精确端点等假设下 \|e\|M>1/2；不是一般渐近极端禁止结果。 | SYS | 内部计算输入 | `RECCVS/inputs/AUDIT.md` L1–61；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/05_strict_half_threshold.md` L1–69 |
| CHAR 正半径特征适定与约束传播 | KU 2211.15742 Proposition 2.1/Remark 2.1，球面数据 Proposition 2.3；GL 1709.09137 §10 的局部约束机制。 | 无项目前置 | 外部来源待逐项复核 | RECCVS/literature/2211.15742.txt；RECCVS/literature/1709.09137.txt；仅局部工具；GL 弱耦合全局主定理不在此输入内 |
| MGHD 球对称全局商空间与 ν 传播 | Kommemi 1107.0949v2 Proposition 2.1、3.1 及实际域接口，保留约定与连通性假设。 | 无项目前置 | 外部来源待逐项复核 | RECCVS/literature/1107.0949.txt； |
| KOM_EXT 正半径延拓原理 | Kommemi Theorem 1.8/§4：整个去端点因果菱形在实际发展，r 有正下界且体积有限。 | 无项目前置 | 外部来源待逐项复核 | RECCVS/literature/1107.0949.txt；r=0 端点与已有 CH 片不能直接验收 |
| CAUCHY 有限时间强拓扑 Cauchy 稳定性 | 固定谐和/Lorenz 规范；共同有限光滑参考片及足够高 Sobolev 控制，约束/规范传播与几何唯一性。 | 无项目前置 | 标准工具；明确版本/定理号未固定 | `RECCVS/proofs/RECCVS_L001.md` L1–41；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/03_regular_center_and_gluing.md` L1–374 |
| PENROSE Penrose 零测地不完备定理 | NEC、整体双曲、非紧 Cauchy 面、闭严格陷俘二曲面。 | 无项目前置 | 标准工具；明确版本/定理号未固定 | `RECCVS/proofs/RECCVS_L001.md` L1–41 |
| KL Kauffman–Lindblad 小数据定理 | 2109.03270v2 Theorem 11.1，固定 N≥14、γ∈(1/2,1)，转换后加权数据范数足够小。 | 无项目前置 | 外部来源待逐项复核 | `RECCVS/proofs/RECCVS_L006.md` L1–76 |
| ANLIM An–Lim 带电陷俘形成接口 | 2005.04090v1 Theorem 1.3、证明(2.16)及§3；正确物理宽度、初始两锥及实际发展接口。 | 无项目前置 | 外部来源及归一化待独立复核 | `RECCVS/proofs/RECCVS_L023.md` L1–175 |
| SL 有限区间 Sturm–Liouville 工具 | 有界实际 V≥0、H1 稠密性、紧嵌入与首 Rayleigh 值取到。 | 无项目前置 | 标准工具；稿内给出所需主要恒等式 | `RECCVS/proofs/RECCVS_L018.md` L1–107 |
| BESSEL J0 首零点与加权 Poincaré | J0(jx)>0 对 0≤x<1，J0(j)=0；j=j0,1；稿内给出 ground-state 与边项论证。 | 无项目前置 | 标准特殊函数工具 | `RECCVS/proofs/RECCVS_L017.md` L1–105 |
| E020 L020 历史有理/整数证书 | 固定剖面、矩、J 分子、Bernstein/Descartes 覆盖；验收范围为领先辅助剖面。 | 无项目前置 | 附件中已有；本轮未重跑数学认证 | `RECCVS/experiments/ROUND_07_VERIFICATION.md` L1–11 |
| E021 L021 历史可行族证书 | 精确有理系数/核心 Bernstein 包络；光滑 cutoff、bump 与超越积分矩阵的证明仍在正文。 | 无项目前置 | 附件中已有；本轮未重跑数学认证 | `RECCVS/experiments/ROUND_07_VERIFICATION.md` L1–11 |
| E023 L023 历史门槛代数检查 | 仅检查充分条件的代数；JSON 明记 finite_amplitude_root_certified=false。 | 无项目前置 | 附件中已有；本轮未重跑数学认证 | RECCVS/experiments/check_first_period_thresholds.py；RECCVS/experiments/first_period_threshold_certificate.json； |
| SMOOTH_DOMAIN 同一实际光滑正半径域 | r>0、Ω²>0，积分前缀/特征片确实属于同一实际解；不附加 ν 或 λ 的符号。 | 无项目前置 | 显式条件；指定实例未独立验收 | `RECCVS/proofs/RECCVS_L003.md` L3–12；`RECCVS/proofs/RECCVS_L010.md` L7–26 |
| NU_NEG 入射膨胀负号 | 未来取向固定且 ν=r_U<0；只在膨胀号数、陷俘判断或需除以 ν 的面积坐标中要求。 | 无项目前置 | 显式条件；指定实例未独立验收 | `RECCVS/proofs/RECCVS_L008.md` L7–9；`RECCVS/proofs/RECCVS_L018.md` L7–17 |
| AFFINE_NORM 径向仿射尺度与固定框架 | 径向零线切向仿射平行输运；初点按实际单位类时法向归一化，或明确记录固定的正仿射比例。局部公式不要求可见性/I+。 | 无项目前置 | 归一化约定；指定线仍需核实 | `RECCVS/proofs/RECCVS_L003.md` L3–12；`RECCVS/proofs/RECCVS_L018.md` L7–17；`RECCVS/proofs/RECCVS_L019.md` L33–37 |
| CENTER_INTERVAL 实际中心起算有限区间 | 实际中心归一化 [0,ell]；r(0)=0、r_s(0)=1，r(s)>0 对 s>0，真实 V=\|D_Lφ\|² 有界且 ≥0，非中心 ν<0。 | 无项目前置 | 显式条件；指定实例未独立验收 | `RECCVS/proofs/RECCVS_L018.md` L7–17 |
| POS_INTERVAL 实际正半径起算有限区间 | r(0)>0、全段 r>0，记录固定仿射尺度及 w0=r_s(0)/r(0)，真实 V 有界且 ≥0；陷俘解释另用 NU_NEG。 | 无项目前置 | 显式条件；指定实例未独立验收 | `RECCVS/proofs/RECCVS_L018.md` L95–101 |
| FJETS 有限非线性 jets 与 C1 端点误差 | 固定 K 的五行输运层级、Minkowski 初始边量级及 C1(c,τ) 误差；以 FRBASE 和 FRPOS 的基底与 q 下界为输入。 | SYS、FRBASE、FRPOS、FENDPOINT | 内部证明模块；未独立验收 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/03_nonlinear_lifting.md` L61–139 |
| SPHERE_KU KU完整球面数据定义与约束接口 | KU Definition 2.3、Proposition 2.3、Lemma 4.2：球面字段阶数、约束输运及 ERN 规范轨道条件；须核对其版本、规范与相容条件。 | 无项目前置 | 外部接口；调用位置已核对，原定理适用性待独立验收 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/02_endpoint_matching.md` L49–65 |
| FSPHERE 真实有限阶球面匹配 | 有限 jets、真实端点零点、正半径/横向膨胀及 KU 字段接口共同给完整 D_K 和右端 ERN 轨道；不得用于反向证明线性端点可逆性。 | FJETS、FLIFT、FRPOS、SPHERE_KU | 内部证明模块；未独立验收 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/02_endpoint_matching.md` L49–61 |
| REPAIR_BUDGET 已兑现的逐步尾预算 | 同一序列从 n=N0 起每步确有 \|\|Φ_(n+1)-Φ_n\|\|_(C^(n-1))+\|β_(n+1)-β_n\|<δ*2^-n；求 Ck 尾须 N≥max(N0,k+1)。预算存在陈述与计算兑现分开。 | 无项目前置 | 显式条件；指定实例未独立验收 | `RECCVS/proofs/RECCVS_L022.md` L7–21；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/02_smooth_data_and_local_evolution.md` L430–461 |
| REPAIR_TO_STRONG 修复种子到共同实际强拓扑的桥 | 固定共同特征/Cauchy实现、同一有限实际参考片、足够高固定 Ck/Sobolev 阶数及误差传递界；种子尾小必须实际推出稳定定理所需输入误差<ε_trap。 | 无项目前置 | 未验证的应用门；旧G07保留 | `RECCVS/proofs/RECCVS_L023.md` L165–173；`RECCVS/proofs/RECCVS_L022.md` L98–109 |
| FINITE_CONE23 L023有限锥约束输入（不含端点求根） | 固定光滑周期族 C≥0、E均值正；L=mT、δ=τ/L>0，q_x=-q+q²+δE、R_x=-qR、零初值 q(0)=0/R(0)=1；同一仿射形成锥约束、正半径、左端完整平直球面、m1=Q1=φ1=0、H(t1)=t1/q1；实际使用前需验证 H>0/ν<0。此条件不声称端点根存在。 | 无项目前置 | 显式几何输入；根存在与整入射锥另列 | `RECCVS/proofs/RECCVS_L023.md` L40–56；`RECCVS/proofs/RECCVS_L023.md` L63–95 |
