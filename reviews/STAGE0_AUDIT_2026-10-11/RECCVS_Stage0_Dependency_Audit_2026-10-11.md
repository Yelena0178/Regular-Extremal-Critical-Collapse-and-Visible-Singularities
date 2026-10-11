# RECCVS：阶段0研究基线与证明依赖审计

日期：2026-10-11（Asia/Shanghai）。本次授权范围：冻结附件基线、整理L001–L023依赖、来源、适用域、目录和缺口。此前Chat模式的计划/判断不作为额外证据。

## 核心结果

23份原稿分解为78项核心结论、条件推论和应用接口，登记36个输入节点、203条直接依赖边。图检查未发现未定义ID或有向环；L014–L015和导入有限阶两稿的互引需要按命题/小节拆开。原稿数学正确性仍待独立复核。

最关键的结果分层为：

* L001–L006主要提供基础筛选、约束族、物理潮汐与小数据接口。
* L007–L015对实际形成解的应用依赖I001及相应实际域/全零jets；泛化的单截面和抽象外边定理可在独立列明的条件下使用。
* L016中心曲率恒等式与L018有限区间谱工具不以极端形成输入为核心前提；它们在本种子上的动态应用另有未取得输入。
* L020–L021认证领先辅助族；L023需要真实有限阶分支和完整Minkowski入射填充。L022的锥预算与完整时空误差传播是两个接口。

A–D均保持开放。具体端点根、共同填充与Cauchy实现、修复稳定预算、中心端点动态分类尚未完成。

## 冻结范围

仓库名称采用本次用户给出的 `Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities`。本轮未读取Git HEAD或issue实时明细，也未修改远端仓库。可复核基线为三份附件的SHA-256以及ZIP内203项的完整清单。

| 附件 | SHA-256 |
| --- | --- |
| RECCVS_First_Period_Trapping_2026-10-09.zip | 346ba992740af3791c660dd1bdb742910a8d4c277430affbb4b77852f5745382 |
| RECCVS_Global_Central_Control_2026-10-09.md | 325b614a7c3e97cce820f3ae6323849cf5f24e45f804b3951e73c1fd759f291a |
| RECCVS_First_Round_2026-10-09.md | 109eafbc52e3e6166d611942e48e4ef56707e104b38203dccecad0e6eadbfc2b |

依赖边由前置指向使用者。定义/条件输入、已写的内部证明、历史计算证书和外部定理调用分别记录。后文的“已写”或“有证书”均不表示本轮已经独立认证。

## 本轮检查的范围

本轮检查23原稿副本的字节一致性、来源定位与哈希、78条逐命题记录、36个输入节点、203条直接边的ID闭合/拓扑排序以及包内文件映射。未运行数学证书、非线性端点求根、时空演化或新增研究推导。所列缺口包括下一阶段审查风险，不能作为已证明的反例。

## 进度报告

* 本轮完成项：附件基线、23稿/78项依赖、来源定位、六目录映射、缺口/回路登记及文件一致性检查。
* 剩余项：阶段1独立接口复核；R01–R08按批准计划推进；A–D保持开放。
* 卡点：实际根、完整共同实现、强拓扑修复预算及中心/全未来控制。
* 下一步：进入阶段1，先核对L023与An–Lim接口，另按计划审查形成模块依赖。


---

# L001–L023 完整依赖关系表

基线：2026-10-11。本表读取原稿，按核心命题和应用分开登记。所有证明保持内部待审状态；目录位置不是证明状态。

SYS/TOPO/VIS 是 MODEL.md 的定义；其余输入的完整陈述与来源见 INPUT_REGISTER.md。原稿逐字保留，路径与哈希见 SOURCE_MAP.csv。

| 稿件 | 核心前置结果 | 条件性应用/实例输入 | 输入假设 | 适用域 | 限制 |
| --- | --- | --- | --- | --- | --- |
| L001 有限时间严格陷俘的阈值排除 | SYS、TOPO、CAUCHY、PENROSE | 黑洞集合应用另需完整 I+ 与可预测性接口 | 光滑约束数据、Σ≅R³空间完备；有限紧光滑区中有正半径严格陷俘球 | 固定参考片及其 X^s 相对邻域 | 给不完备与不在闭包D/N；U⊂B 另有条件。 |
| L002 受控正则约束初值曲线 | SYS、TOPO；约束 ODE | L006 是后续应用 | 固定 e,f,g,r0,R0；小 p；Δ≥1/2 的闭合 bootstrap | 中心至唯一 AF 端的初始数据，全族固定支持/尺度 | 初始未陷俘、满足约束与光滑参数依赖；非零 p 的完整色散不由本稿给出。 |
| L003 径向平行传播潮汐分量 | SYS、VIS；warped-product/Raychaudhuri | B/C 应用需真实增长、有限仿射与可见性 | 仿射径向零线，固定物理初点归一化，平行角向框架 | 实际光滑正半径线段 | 只将物理一阶导数变成潮汐分量；不推出K、有限参数或可见性。 |
| L004 中心出射线对数聚焦 | SYS、VIS、REG_CENTER、POS_DOMAIN | 限定无黑洞推论另需全部中心线覆盖/完整性/同一I+ | 实际中心发出线，r_s(0)=b>0；面积坐标公式仅在r_s>0 | 实际最大正膨胀段；完备有界半径推论另加S=∞ | 能量发散可来自r_s→0；不自动是曲率发散。 |
| L005 电荷—聚焦与光滑反误判例 | L004、SYS；CHAR用于反例局部实现 | 陷俘排除应用另需振幅积分上界与反向膨胀 | Q(0)=0；正膨胀仅为面积坐标版条件；反例是独立正半径片 | 实际有限零线；另有光滑局部特征反例 | 总电荷下界不给实际出射通量下界；局部反例不是全局形成解。 |
| L006 小数据全局接口与部分完备性 | L002、SYS、KL | TOPO、VIS 的完整色散验收尚缺最后接口 | 固定e、N≥14、γ∈(1/2,1)，归一化与ADM/Coulomb主项扣除后小数据 | L002 的充分小振幅族；最终内锥线另限ρ≤(1-η)t | 径向零与最终内锥因果完备；一般非径向外锥线及完整I+未验收。 |
| L007 有限时间实际内侧未陷俘薄带 | I001 的实际内侧与 RN jets、SYS | L001 是后续筛选 | 每个有限T已有实际宽度aT与相应Taylor jets；固定ν<0 | 0<U≤bT，1≤t≤T | bT依赖T；形成期和深中心不覆盖；零jets不给非零尾系数。 |
| L008 全入射截面聚焦与三次跨越 | SYS、POS_DOMAIN；MGHD用于ν传播 | 中心公式需REG_CENTER；极端三跨越需外端jets | 每个积分前缀实际存在；中心端项仅在完整正则中心截面置零 | 单个实际入射截面；形成期保留rHλH边项 | 一次跨越保持是额外动力学条件；没有全未来无陷俘证明。 |
| L009 全时间未陷俘楔域 | L008.前缀积分、L010.输运；SYS、HORIZON、CHAR | I001/INSEG 用于同一Cauchy解识别 | 固定种子、e,a0,N,A；先定常数后定c,η | 0≤U≤η，t≥1，Ut≤c，r≥1/2 | 不覆盖Ut>c、形成期、深中心；引用后编号L010不构成循环。 |
| L010 中心相容与电流号障碍 | SYS；CHAR用于局部反例 | I001/INSEG 仅为晚时零视界应用；REG_CENTER用于积分终端 | P=D_Uφ、T=D_tφ、A_t=0；保留Wilson相位 | 实际正半径特征片；到中心的复积分等式另有中心条件 | 复积分是中心必要条件；电荷比值无由正能量给出的最大值原理。 |
| L011 全剩余域正通量预算 | SYS；L010用于Wilson式；L009用于楔域闭合 | L001用于真实超支后的筛选；I001/INSEG用于视界积分 | 真实初始点/中心、真实存在段；晚时Wilson式需要视界零值 | 每条实际出射线；楔域或额外尾下界的条件性子域 | 全深部预算尚未验证；尾下界及后续存在性没有取得。 |
| L012 固定宽度全时间实际内侧控制 | L008、L010；L009§4的延续机制；SYS、HORIZON、CHAR | I001/INSEG用于实际MGHD识别；全局边界解释另需完整视界 | 同一C∞种子、全零视界jets；N先取足够大、A固定后缩η | 固定0≤U≤η、全部t≥1，r≥3/4 | 不覆盖深中心；曲率有界与连续度量延拓不给方程解/C²/C∞延拓。 |
| L013 实际散射迹刚性与增长 | L012；SYS、HORIZON | 其外边供L014、L015应用 | 同一固定种子；反向吸收需N再增大、η再缩小 | 固定近视界条带，极限在闭U区间[a,η]；h积分到0需支配界 | h>0依赖实际初始场非零；无初值族统一h/T下界。 |
| L014 抽象外边下的全余域体积与寿命 | SYS、OUTER_INPUT、POS_DOMAIN；INSEG用于实际全域 | L013或L015.OUTER提供外边的实例；REG_CENTER用于中心截面/轴线 | 外边全部t≥1存在且α_b/t²→h_b>0；固定外边 | 更深实际连通余域；电磁/半径与轴式只在仍有正则中心时 | 外边输入为显式条件；不决定λ号、曲率或r=0延拓。 |
| L015 首个非零点与轴线有限固有寿命 | I001、L012、L013；CHAR；L014的抽象估计 | OUTER实例供L014；轴线结论供L016条件推论 | 正则中心唯一、全局标签/入射连通、完整视界；分中心是否活到t=1 | 同一实际MGHD轴线与选择的固定外边 | 有限类时固有长度；不等于零仿射奇点，轴线在黑洞内。 |
| L016 正则中心曲率与物理导数 | SYS、REG_CENTER；L014.AXIS用于坐标表达 | L015+实际增长假设用于有限固有时曲率推论 | 实际四维光滑正则中心；无磁荷；规范不变物理导数 | 中心事件及其逐事件趋轴极限 | K=(20/3)\|Dτφ\|⁴是局部恒等式；动态增长和趋轴统一界未取得。 |
| L017 中心电荷的尖锐径向能量障碍 | SYS、REG_CENTER、BESSEL | 极端视界应用需R=M、\|Q\|=M与相应端点 | 完整实际入射截面、ν<0、Q(0)=0、φ(R)=0 | 单个完整正则中心截面；尖锐性只在径向函数类 | 总S下界不决定L008前缀号；全零jets严格性无统一间隙。 |
| L018 有限实际区间谱陷俘判据 | SYS、VIS、FINITE_INTERVAL、SL | L001用于陷俘后的阈值排除 | 真实V=\|D_Lφ\|²；r>0、ν<0；中心或记录Robin初值 | 有限实际仿射区间[0,ell] | 谱公式不提供实际V包络；正证书只覆盖该区间。 |
| L019 内部边际球刚性与仿射预算 | SYS、L010、POS_DOMAIN | 严格陷俘应用另需预算后仍实际存在 | λ内部触零；推Q=±r需要U邻域λ≥0；未来刚性需全段邻域λ≥0 | 正半径实际内部点或边际射线 | 不适用外视界/中心/未知边界；尚无指定种子的触零证据。 |
| L020 固定八阶领先剖面证书 | KDEF、E020；稿内滤波与核论证 | L021用此辅助剖面；实际形成另需FLIFT | K=8,n=88,σ=1/20；能量归一化；精确系数与积分 | x≥0辅助半线；J变号证书紧化覆盖全半线 | λ≈0.5046与核下界属于领先辅助对象；有限振幅根未认证。 |
| L021 截断、矩修复与周期族 | L020、E021 | FLIFT须接收此具体族；L023几何门槛专用 | a=2^-1000,B=2^20,T=1048578；\|c_s\|≤2^-4096；解析bump定义 | 单块比较、严格电流核心及全周期半线 | 超越积分矩阵以解析定义精确修复；有理脚本只覆盖其中有理部分。 |
| L022 光滑尾界与锥/时空误差预算 | FSMOOTH的逐步预算；SYS；L018用于谱判据 | COMMON_FLOW、实际数值包络和已认证a,h,β是条件输入 | 每一步确实精确修复并满足预算；参考锥已认证正余量 | 同一光滑极限的固定Ck尾；锥[0,1]；共同实际区间另加条件 | 锥预算已给公式；C_flow、共同域和实际W包络尚缺。 |
| L023 第一周期严格陷俘机制 | FLIFT、MINK_FILL、ANLIM；具体族另用L021、E023 | 光滑排除另需FSMOOTH、CAUCHY、修复预算；最后用L001 | 真实端点根、固定周期族、完整Minkowski入射锥；23.6充分条件 | 指定长脉冲分支的有限第一周期发展；具体门槛是几何门槛 | 充分长分支条件性排除；未冻结任意原光滑种子；m_geom不是m_lift。 |

## 阅读次序

几何主链中 L010 的基本输运应先于 L009 阅读。L014 的抽象外边估计先读，再读 L015 的外边构造与轴线应用。L016 的中心曲率恒等式可独立读，末节的动态推论最后读。领先构造链为 L020 → L021 → 有限阶提升输入 → L023；L022 的锥预算与时空误差接口分别读。


---

# 输入与外部结果登记表

“条件输入”须在每次应用中被验证；来源登记不等于证明通过。公共论文仅固定附件内版本，阶段0未检索新版、勘误或重新审查全文。标准 Cauchy/Penrose 工具的精确版本尚须补定。分情况证明中的多个前置结果用于不同分支，不表示所有相应额外假设须在一个分支中同时成立。

| ID | 名称/状态 | 准确输入 | 前置模块 | 来源与定位 |
| --- | --- | --- | --- | --- |
| SYS | D001：EMCSF 归一化；定义输入 | 四维、球对称、无质量复标量、无磁荷、固定 e≠0；签名与 Maxwell 取向按 MODEL.md。 | 无项目前置 | `RECCVS/definitions/MODEL.md`；RECCVS-D001 |
| TOPO | D002–D003：强拓扑与色散集合；定义输入 | 约束空间 X^s，s≥6；AF/Coulomb 主项单列；D 要求所有因果测地完整、完整 I+ 与衰减。 | 无项目前置 | `RECCVS/definitions/MODEL.md`；RECCVS-D002、D003 |
| VIS | D004：物理归一化与可见性；定义输入 | 零线仿射或类时固有时；框架在固定物理初点归一化；可见性接到同一完整 I+。 | 无项目前置 | `RECCVS/definitions/MODEL.md`；RECCVS-D004 |
| REG_CENTER | 实际正则中心；条件输入 | 四维实际光滑正则中心；Q=O(r^3)、m=O(r^3)，中心取极限；使用时必须标明该中心事件仍属于实际发展。 | 无项目前置 | `RECCVS/definitions/MODEL.md`； |
| POS_DOMAIN | 实际正半径光滑域；条件输入 | r>0、Ω²>0、ν<0；所积分的段确实存在于同一实际解；未来双零方向取向固定。 | 无项目前置 | `RECCVS/definitions/MODEL.md`； |
| INSEG | 同一实际入射连通段；条件输入 | 由 U=0 至所考察点的正半径前缀属于实际发展；只有明确到达正则中心时才使用中心端边项。 | 无项目前置 | `RECCVS/inputs/AUDIT.md`；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/04_global_development_and_horizon.md`； |
| HORIZON | 全零 jets 的晚时极端视界数据；条件输入 | M=Q_H=1，U=0、t≥1：r=Q=Ω²=1、λ=φ=0、ν=-a0<0，横向标量 jets 全零；t=1 内侧数据属于同一光滑种子。 | 无项目前置 | `RECCVS/inputs/AUDIT.md`；`RECCVS/proofs/RECCVS_L009.md`；`RECCVS/proofs/RECCVS_L012.md`； |
| OUTER_INPUT | L014.1：抽象外边输入；条件输入 | 固定 U=b 的全部 t≥1 外边：0<r_b≤R≤1、λ_b≥0、r_bλ_b≤C_b/t²、α_b/t²→h_b>0、α_b≥a0。 | 无项目前置 | `RECCVS/proofs/RECCVS_L014.md`；§1，L014.1 |
| FINITE_INTERVAL | 实际有限仿射区间；条件输入 | 中心归一化 γ 在 [0,ell] 实际光滑存在，r(s)>0 对 s>0；正半径起点版本另记录 r_s(0)/r(0)。 | 无项目前置 | `RECCVS/proofs/RECCVS_L018.md`； |
| TAIL_LOWER | 实际非零尾部下界；未取得的条件 | 同一实际线对全部 t≥t1 存在且 r≥r_->0、Ω²≤C(1+t)^(-γ)、\|T\|≥c(1+t)^(-β)，c>0。 | 无项目前置 | `RECCVS/proofs/RECCVS_L011.md`；L011.4；不是现有种子的已知尾部 |
| COMMON_FLOW | 共同实际域与流误差；未取得的条件 | 共同紧光滑域、同一物理初点/仿射归一化、Wilson 比较；强范数输入差到实际 W 的 C_flow 界。 | 无项目前置 | `RECCVS/proofs/RECCVS_L022.md`；§3 |
| MINK_FILL | 完整 Minkowski 入射填充；尚未冻结的条件 | 从左端球面至中心的整条初始入射锥为 Minkowski；共同 Cauchy 实现包含相应有限依赖域。 | 无项目前置 | `RECCVS/proofs/RECCVS_L023.md`；§2；不是仅球面 jets 或局部平直空隙 |
| PERIODIC_PROFILE | 有限阶提升的周期族假设；抽象条件 | 固定 K、T、紧 c 球；光滑周期 z_c、端点共同开空隙、均值 E/C 正、C≥0、λ<μ、形成核正。 | 无项目前置 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/01_profile_construction.md`；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/03_nonlinear_lifting.md`； |
| KDEF | 形成核的完整定义；定义输入 | I_C(x)=∫_0^x C+∫_x^∞e^(x-y)C；I_E(x)=∫_0^x(1-e^(y-x)/2)E+(1/2)∫_x^∞e^(x-y)E；𝒦=2λI_C-2I_E。 | 无项目前置 | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/01_profile_construction.md`；文件首段；给 L020 缺省记号补足来源 |
| FRBASE | 有限阶提升：半径/参数基底；内部未独立复核 | 固定周期族；q=O(δ)、q-δp=O_C1(δ²)、R 与一阶参数导数一致控制。 | PERIODIC_PROFILE | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/03_nonlinear_lifting.md`；§2–3 |
| FRPOS | 半径正性与初始 q 下界；内部未独立复核 | 由 Riccati 正壁、周期平均、核紧区间/尾区及有限脉冲比较取得 q≥aδ、H_L>0。 | FRBASE、KDEF、PERIODIC_PROFILE | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/04_radius_positivity.md`；§1–5 |
| FENDPOINT | 有限阶背景端点与完整球面数据；内部未独立复核 | 多项式 Volterra 核、非零下三角对角元、KU D_K 最高阶字段。 | SYS | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/02_endpoint_matching.md`；§1–5 |
| FLIFT | 有限阶非线性分支存在；内部未独立复核；非有效门槛 | 对每个充分大 m 存在局部精确根 (c_m,τ_m)，c_m→0、τ_m→τ0；17 维具体根仍未认证。 | FRBASE、FRPOS、FENDPOINT | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/finite_order/03_nonlinear_lifting.md`；§4–6；K=8 时为 17 个实条件 |
| FLOCAL | Bondi 共同低阶寿命；内部未独立复核 | 有符号半径 Bondi 光滑解、完整正半径方程、固定阶中心响应及参数 C1 控制。 | SYS | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/02_smooth_data_and_local_evolution.md`；§2–5；四维中心解释另在 FCENTER |
| FSMOOTH | 同一光滑种子与逐阶修复；内部未独立复核 | 非退化有限基族之后逐阶精确修复、同一终端空隙、可求和 C^(n-1) 与 β 预算。 | FLIFT、FLOCAL | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/02_smooth_data_and_local_evolution.md`；§6.1–6.4 |
| FCENTER | 实际四维中心、接合与 cap；内部未独立复核 | 中心奇偶、实际笛卡尔实现、一次 ERN 边值实现、共同条带和顶点填充。 | FSMOOTH、FLOCAL、CHAR、CAUCHY | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/03_regular_center_and_gluing.md`；§2–5 |
| FGLOBAL | 全局 Cauchy/外部/视界识别；内部未独立复核 | 实际保留域、单端 AF Cauchy 面、MGHD 识别、完整 I+ 及视界从中心出发。 | FCENTER、MGHD、CHAR | `RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/04_global_development_and_horizon.md`；§2–6 |
| I001 | 导入的光滑极端形成输入；组合性内部输入 | 固定 eM>1/2 的一份同一光滑、正则中心、单端 AF、真正塌缩形成解；全局标签/晚时精确 ERN 按导入稿。 | FGLOBAL | `RECCVS/inputs/AUDIT.md`；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/01_main_theorem.md`；AUDIT.md 的 I001 及主定理；没有临界族或非零视界尾部 |
| I002 | 限定视界类的严格半门槛；内部计算输入 | 限定正则起源、有限时间精确端点等假设下 \|e\|M>1/2；不是一般渐近极端禁止结果。 | SYS | `RECCVS/inputs/AUDIT.md`；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/05_strict_half_threshold.md`；AUDIT.md 的 I002；L001–L023 核心 DAG 无需该输入 |
| CHAR | 正半径特征适定与约束传播；外部来源待逐项复核 | KU 2211.15742 Proposition 2.1/Remark 2.1，球面数据 Proposition 2.3；GL 1709.09137 §10 的局部约束机制。 | 无项目前置 | `RECCVS/literature/2211.15742.txt`；`RECCVS/literature/1709.09137.txt`；仅局部工具；GL 弱耦合全局主定理不在此输入内 |
| MGHD | 球对称全局商空间与 ν 传播；外部来源待逐项复核 | Kommemi 1107.0949v2 Proposition 2.1、3.1 及实际域接口，保留约定与连通性假设。 | 无项目前置 | `RECCVS/literature/1107.0949.txt`； |
| KOM_EXT | 正半径延拓原理；外部来源待逐项复核 | Kommemi Theorem 1.8/§4：整个去端点因果菱形在实际发展，r 有正下界且体积有限。 | 无项目前置 | `RECCVS/literature/1107.0949.txt`；r=0 端点与已有 CH 片不能直接验收 |
| CAUCHY | 有限时间强拓扑 Cauchy 稳定性；标准工具；明确版本/定理号未固定 | 固定谐和/Lorenz 规范；共同有限光滑参考片及足够高 Sobolev 控制，约束/规范传播与几何唯一性。 | 无项目前置 | `RECCVS/proofs/RECCVS_L001.md`；`RECCVS/inputs/formation/RN-Black-Hole-Lab/proof/03_regular_center_and_gluing.md`；L001 证明1–3；形成 proof/03 §1；见缺口 G01 |
| PENROSE | Penrose 零测地不完备定理；标准工具；明确版本/定理号未固定 | NEC、整体双曲、非紧 Cauchy 面、闭严格陷俘二曲面。 | 无项目前置 | `RECCVS/proofs/RECCVS_L001.md`；L001 证明4–5；见 G01 |
| KL | Kauffman–Lindblad 小数据定理；外部来源待逐项复核 | 2109.03270v2 Theorem 11.1，固定 N≥14、γ∈(1/2,1)，转换后加权数据范数足够小。 | 无项目前置 | `RECCVS/literature/2109.03270.txt`；`RECCVS/proofs/RECCVS_L006.md`；L006 §1–3；公开源状态按附件版本固定 |
| ANLIM | An–Lim 带电陷俘形成接口；外部来源及归一化待独立复核 | 2005.04090v1 Theorem 1.3、证明(2.16)及§3；正确物理宽度、初始两锥及实际发展接口。 | 无项目前置 | `RECCVS/literature/2005.04090.txt`；`RECCVS/proofs/RECCVS_L023.md`；L023 §1；R05 待办 |
| SL | 有限区间 Sturm–Liouville 工具；标准工具；稿内给出所需主要恒等式 | 有界实际 V≥0、H1 稠密性、紧嵌入与首 Rayleigh 值取到。 | 无项目前置 | `RECCVS/proofs/RECCVS_L018.md`；§1–3；不提供实际 V 的误差包络 |
| BESSEL | J0 首零点与加权 Poincaré；标准特殊函数工具 | J0(jx)>0 对 0≤x<1，J0(j)=0；j=j0,1；稿内给出 ground-state 与边项论证。 | 无项目前置 | `RECCVS/proofs/RECCVS_L017.md`；§2–3 |
| E020 | L020 历史有理/整数证书；附件中已有；本轮未重跑数学认证 | 固定剖面、矩、J 分子、Bernstein/Descartes 覆盖；验收范围为领先辅助剖面。 | 无项目前置 | `RECCVS/experiments/freeze_filtered_profile.py`；`RECCVS/experiments/certify_filtered_J.py`；`RECCVS/experiments/filtered_K8_n88_sigma1over20.json`；`RECCVS/experiments/filtered_K8_n88_J_certificate.json`；`RECCVS/experiments/ROUND_07_VERIFICATION.md`； |
| E021 | L021 历史可行族证书；附件中已有；本轮未重跑数学认证 | 精确有理系数/核心 Bernstein 包络；光滑 cutoff、bump 与超越积分矩阵的证明仍在正文。 | 无项目前置 | `RECCVS/experiments/certify_admissible_profile.py`；`RECCVS/experiments/filtered_K8_n88_admissible_certificate.json`；`RECCVS/experiments/ROUND_07_VERIFICATION.md`； |
| E023 | L023 历史门槛代数检查；附件中已有；本轮未重跑数学认证 | 仅检查充分条件的代数；JSON 明记 finite_amplitude_root_certified=false。 | 无项目前置 | `RECCVS/experiments/check_first_period_thresholds.py`；`RECCVS/experiments/first_period_threshold_certificate.json`； |

## 形成输入的拆分

FRBASE → FRPOS；FRBASE、FRPOS、FENDPOINT → FLIFT → FSMOOTH → FCENTER → FGLOBAL → I001。FLOCAL 从本规范的算子/局部演化论证给出，并与 FLIFT 一起供 FSMOOTH 使用。该拆分是文献依赖记录，不是对导入证明的独立认证。

PERIODIC_PROFILE 是抽象假设；L021 是具体实例。把 L021 代入 FLIFT 的实例并不等于已经得到有效门槛或具体根。I002 不承担 A 的普遍禁止结论。


---

# 逐命题来源、假设与适用域

下列审计ID是定位标签，不新增数学命题，也不改变原稿编号。每个源定位包含原始路径、行号和该文件SHA-256；机器数据见 CLAIMS.json。核心证明边与应用边分别记录，解释性前后引用不自动成为证明依赖。

## L001：有限时间严格陷俘的阈值排除

原稿：`RECCVS/proofs/RECCVS_L001.md`；包内：`foundations/RECCVS_L001.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L001.PERSIST 严格陷俘有限时间持久 | SYS、TOPO、CAUCHY | 固定有限紧光滑参考片、严格负余量、共同规范 | 该参考数据的相对强邻域 | `RECCVS/proofs/RECCVS_L001.md`，行15–32，## 证明 | 按列出的假设与域使用 |
| L001.EXCLUDE 不在N/D闭包 | L001.PERSIST、PENROSE | NEC、MGHD、非紧完备Cauchy面 | 固定候选及其邻域 | `RECCVS/proofs/RECCVS_L001.md`，行5–14，## 精确命题 | U⊂B需要另加全局可预测性/零无穷远条件 |
| L001.BH 附加可预测性下黑洞邻域 | L001.EXCLUDE、VIS | 另有全局可预测性/Kommemi陷俘遮蔽假设及适当I+识别 | 满足额外假设的邻域 | `RECCVS/proofs/RECCVS_L001.md`，行5–14，## 精确命题 | 本引理自身不给这些额外全局前提 |

## L002：受控正则约束初值曲线

原稿：`RECCVS/proofs/RECCVS_L002.md`；包内：`foundations/RECCVS_L002.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L002.DATA 完整正则AF约束数据 | SYS、TOPO | 固定紧支持f,g与小p；Δ正性bootstrap | 整张初始面 | `RECCVS/proofs/RECCVS_L002.md`，行21–48，## 证明 | 按列出的假设与域使用 |
| L002.FAMILY 参数光滑、统一范数及非零电荷 | L002.DATA | 电荷首项非零时再给Q非零 | 固定小p族 | `RECCVS/proofs/RECCVS_L002.md`，行21–48，## 证明 | 初始膨胀不能代替未来色散 |

## L003：径向平行传播潮汐分量

原稿：`RECCVS/proofs/RECCVS_L003.md`；包内：`singularity/RECCVS_L003.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L003.TIDAL Ric(L,L)与PP角向潮汐 | SYS、VIS、POS_DOMAIN | 仿射径向L与平行角框架 | 实际零线光滑段 | `RECCVS/proofs/RECCVS_L003.md`，行1–16，# RECCVS-L003：径向平行传播潮汐分量 | 标量K、有限参数、可见性另证 |

## L004：中心出射线对数聚焦

原稿：`RECCVS/proofs/RECCVS_L004.md`；包内：`geometry/RECCVS_L004.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L004.IDENTITY 仿射/面积聚焦恒等式 | SYS、VIS、REG_CENTER、POS_DOMAIN | r_s(0)=b>0；面积式只在r_s>0 | 实际正膨胀段 | `RECCVS/proofs/RECCVS_L004.md`，行33–46，## 证明 | 按列出的假设与域使用 |
| L004.LOG 完备有界半径的对数障碍 | L004.IDENTITY | S=∞、r_s>0、r≤RH | 该完整实际线 | `RECCVS/proofs/RECCVS_L004.md`，行5–32，## 精确陈述 | 有限S的退化版本同节；不推出曲率发散 |
| L004.FINITE 有限仿射正半径膨胀退化的能量障碍 | L004.IDENTITY | S<∞、r→R*>0、r_s→0；仍在r_s>0段 | 该线的有限仿射端 | `RECCVS/proofs/RECCVS_L004.md`，行5–32，## 精确陈述 | 即使端点可光滑继续也成立；不验收曲率奇异 |
| L004.NOBH 限定覆盖类中无黑洞 | L004.IDENTITY | 每条线完整、积分有界、全域由这些线覆盖、同一完整I+识别 | 仅满足全部额外假设的类 | `RECCVS/proofs/RECCVS_L004.md`，行47–54，## 明确限定类中的禁止结论 | 按列出的假设与域使用 |

## L005：电荷—聚焦与光滑反误判例

原稿：`RECCVS/proofs/RECCVS_L005.md`；包内：`geometry/RECCVS_L005.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L005.CHARGE 电荷—聚焦Cauchy–Schwarz | SYS、L004.IDENTITY | Q(0)=0；面积版需r_s>0 | 实际有限零线 | `RECCVS/proofs/RECCVS_L005.md`，行5–32，## 电荷不等式的精确陈述与证明 | 迫使陷俘还需振幅积分上界与另一膨胀负号 |
| L005.COUNTER 能量发散而潮汐有界的局部实现 | SYS、CHAR | 给定实际相容两特征边；正半径 | 局部光滑反例片 | `RECCVS/proofs/RECCVS_L005.md`，行33–58，## 完全光滑的局部面积能量发散 | 不是I001正则中心全局模型 |

## L006：小数据全局接口与部分完备性

原稿：`RECCVS/proofs/RECCVS_L006.md`；包内：`foundations/RECCVS_L006.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L006.GLOBAL 小数据归一化与全局解接口 | SYS、L002.DATA、L002.FAMILY、KL | 固定e与N≥14；转换后来源范数足够小 | L002充分小族 | `RECCVS/proofs/RECCVS_L006.md`，行27–55，## 约束族进入来源数据空间；`RECCVS/proofs/RECCVS_L006.md`，行16–26，## 归一化转换：固定 e 的合法同构 | 按列出的假设与域使用 |
| L006.RADIAL 所有径向零线完整 | L006.GLOBAL | 来源C0与好角向导数界；中心穿越 | 该小数据发展中的径向零线 | `RECCVS/proofs/RECCVS_L006.md`，行56–73，## 从估计直接补出的几何结论 | 按列出的假设与域使用 |
| L006.INNERCONE 最终内锥因果线完整 | L006.GLOBAL | 固定η>0，晚时ρ≤(1-η)t；连接系数可积 | 满足内锥条件的因果线 | `RECCVS/proofs/RECCVS_L006.md`，行56–73，## 从估计直接补出的几何结论 | 全部非径向外锥线和完整I+仍缺 |

## L007：有限时间实际内侧未陷俘薄带

原稿：`RECCVS/proofs/RECCVS_L007.md`；包内：`geometry/RECCVS_L007.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L007.STRIP 每个有限T实际未陷俘薄带 | SYS、I001 | 有限T已存在内侧区与RN横向jets、紧域C4界 | 0<U≤bT，1≤t≤T | `RECCVS/proofs/RECCVS_L007.md`，行26–48，## 证明及宽度 | 按列出的假设与域使用 |
| L007.ZEROJETS 精确接合没有非零视界jet尾系数 | I001、HORIZON | 全部标量jets为零 | 该精确形成输入 | `RECCVS/proofs/RECCVS_L007.md`，行49–57，## 确切推进与未覆盖部分 | 按列出的假设与域使用 |

## L008：全入射截面聚焦与三次跨越

原稿：`RECCVS/proofs/RECCVS_L008.md`；包内：`geometry/RECCVS_L008.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L008.PREFIX 视界前缀积分与膨胀号 | SYS、POS_DOMAIN | 完整实际前缀；ν传播可由MGHD提供 | 单条入射前缀 | `RECCVS/proofs/RECCVS_L008.md`，行5–25，## 1. 不需要中心边界的视界积分 | 按列出的假设与域使用 |
| L008.CENTER 完整中心截面的积分因子公式 | SYS、REG_CENTER、POS_DOMAIN | 该截面确实连接中心；ν<0 | 该截面全部正半径点 | `RECCVS/proofs/RECCVS_L008.md`，行26–55，## 2. 在确实到达正则中心的截面上使用面积半径 | 按列出的假设与域使用 |
| L008.ONECROSS 一次跨越充分排除陷俘 | L008.CENTER | 外端λH≥0；实际Q/r满足指定一次跨越 | 单截面 | `RECCVS/proofs/RECCVS_L008.md`，行56–68，## 3. 单次跨越充分条件：控制整张截面 | 跨越条件的全时间传播尚未证明 |
| L008.THREECROSS 深部陷俘至少三次跨越 | L008.CENTER | 晚时极端外端、Q_r(M)=0、完整中心截面 | 该截面 | `RECCVS/proofs/RECCVS_L008.md`，行69–79，## 4. 深部陷俘必须伴随至少三次电荷—半径跨越 | 按列出的假设与域使用 |

## L009：全时间未陷俘楔域

原稿：`RECCVS/proofs/RECCVS_L009.md`；包内：`geometry/RECCVS_L009.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L009.WEDGE 楔域几何/场统一bootstrap | SYS、HORIZON、L008.PREFIX、L010.TRANSPORT | N,A固定；先定粗常数后缩c,η | Ut≤c的实际过去矩形 | `RECCVS/proofs/RECCVS_L009.md`，行46–89，## 2. 几何bootstrap：电荷扰动比半径缺口高阶；`RECCVS/proofs/RECCVS_L009.md`，行90–123，## 3. 场bootstrap：保留纯相位的结构 | 按列出的假设与域使用 |
| L009.EXIST 同一全时间楔域发展 | L009.WEDGE、CHAR | 低阶正半径界及每个有限矩形高阶输运 | 0≤U≤η，t≥1，Ut≤c | `RECCVS/proofs/RECCVS_L009.md`，行124–143，## 4. 有限时间延续，及如何得到同一个全时间域 | 按列出的假设与域使用 |
| L009.ACTUAL 楔域识别进同一Cauchy发展 | L009.EXIST、I001、INSEG | 共同实际边、几何唯一性/MGHD接口 | 原形成种子的楔域 | `RECCVS/proofs/RECCVS_L009.md`，行124–143，## 4. 有限时间延续，及如何得到同一个全时间域 | 按列出的假设与域使用 |

## L010：中心相容与电流号障碍

原稿：`RECCVS/proofs/RECCVS_L010.md`；包内：`geometry/RECCVS_L010.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L010.TRANSPORT 共变波输运与Wilson积分 | SYS、POS_DOMAIN | A_t=0、P=D_Uφ、T=D_tφ | 实际光滑正半径片 | `RECCVS/proofs/RECCVS_L010.md`，行5–27，## 1. 共变输运方程 | 按列出的假设与域使用 |
| L010.CENTER 中心复积分必要相容 | L010.TRANSPORT、REG_CENTER | 入射段到中心；晚时视界T=0 | 仍正则的完整中心截面 | `RECCVS/proofs/RECCVS_L010.md`，行28–47，## 2. 正则中心给出的复积分条件 | 不是全部四维中心光滑性的充分条件 |
| L010.PHASE 电流号不由正能量决定 | SYS、CHAR | 两组局部相容角点/特征数据 | 局部正半径反例 | `RECCVS/proofs/RECCVS_L010.md`，行48–59，## 3. 单次跨越没有由能量给出的最大值原理 | 按列出的假设与域使用 |

## L011：全剩余域正通量预算

原稿：`RECCVS/proofs/RECCVS_L011.md`；包内：`geometry/RECCVS_L011.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L011.BUDGET 每条实际线的必要充分预算 | SYS、POS_DOMAIN | 真实起点；中心起点另要求REG_CENTER | 已有实际出射线光滑段 | `RECCVS/proofs/RECCVS_L011.md`，行5–26，## 1. 每条实际出射线上的必要充分预算 | 按列出的假设与域使用 |
| L011.WILSON 晚时预算的Wilson表示 | L011.BUDGET、L010.TRANSPORT、INSEG | 视界T=0；形成期通量单独扣除 | 晚时实际连通域 | `RECCVS/proofs/RECCVS_L011.md`，行27–48，## 2. 将未知的出射尾部换成实际入射积分 | 按列出的假设与域使用 |
| L011.WEDGE 楔域正预算闭合 | L011.BUDGET、L009.WEDGE | 同一楔域内高阶平坦性 | Ut≤c | `RECCVS/proofs/RECCVS_L011.md`，行49–57，## 3. L009覆盖域的预算确已闭合 | 按列出的假设与域使用 |
| L011.FORCED 额外非零尾下的强制聚焦 | L011.BUDGET、TAIL_LOWER | 2β≤γ+1；线在全部未来实际存在 | 满足额外下界的线 | `RECCVS/proofs/RECCVS_L011.md`，行58–76，## 4. 有条件的晚时强制聚焦判据 | 原种子未证该尾下界；候选排除再调用L001.EXCLUDE |

## L012：固定宽度全时间实际内侧控制

原稿：`RECCVS/proofs/RECCVS_L012.md`；包内：`geometry/RECCVS_L012.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L012.KERNEL 显式Liouville有界核表示 | SYS、POS_DOMAIN | 比较量F,Θ定义；零特征边误差 | 每个有限过去矩形 | `RECCVS/proofs/RECCVS_L012.md`，行43–79，## 2. 一个显式、有界的积分核 | 按列出的假设与域使用 |
| L012.STRIP 固定宽度全时间bootstrap | L012.KERNEL、L008.PREFIX、L010.TRANSPORT、HORIZON | 同一C∞输入；N→A→粗常数→η的选取次序 | 0≤U≤η、t≥1；r≥3/4 | `RECCVS/proofs/RECCVS_L012.md`，行80–124，## 3. 给定粗bootstrap时的几何精确估计；`RECCVS/proofs/RECCVS_L012.md`，行125–154，## 4. 场估计：以高阶平坦性吸收固定耦合；`RECCVS/proofs/RECCVS_L012.md`，行155–179，## 5. 闭合度量bootstrap | 按列出的假设与域使用 |
| L012.EXIST 固定条带实际全时间发展 | L012.STRIP、CHAR、I001、INSEG | 使用L009§4的有限矩形延续机制；同一实际边识别 | 固定条带全部有限t | `RECCVS/proofs/RECCVS_L012.md`，行180–187，## 6. 全时间存在的量词；`RECCVS/proofs/RECCVS_L009.md`，行124–143，## 4. 有限时间延续，及如何得到同一个全时间域 | 按列出的假设与域使用 |
| L012.PP 有限仿射长度与全部径向PP曲率界 | L012.STRIP、L012.EXIST、VIS | 每条固定U>0；t=1规范化框架 | 0<U≤η的固定出射线 | `RECCVS/proofs/RECCVS_L012.md`，行188–214，## 7. 有限仿射长度及有界曲率 | 长度U↓0可发散；本片没有曲率发散 |
| L012.BOUNDARY 非退化连续度量边界 | L012.STRIP、L012.KERNEL、L012.EXIST | 固定U1>0闭区间；可积源与支配收敛 | V=-1/t的正半径边界片 | `RECCVS/proofs/RECCVS_L012.md`，行215–227，## 8. 连续边界接口与保留的正则性限制 | 方程解/C²/C∞延拓未验收；MGHD内不可继续的解释另用I001全局接口 |
| L012.MGHD_EDGE 完整视界下MGHD内常规端点障碍 | L012.PP、I001、MGHD | 完整视界与实际MGHD整体双曲性；假想端点的因果过去包含全部晚时视界段 | 每条固定U>0的t→∞端 | `RECCVS/proofs/RECCVS_L012.md`，行215–227，## 8. 连续边界接口与保留的正则性限制 | 因果紧性论证待独立复核；不等于方程解延拓正则性结论 |

## L013：实际散射迹刚性与增长

原稿：`RECCVS/proofs/RECCVS_L013.md`；包内：`center/RECCVS_L013.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L013.LIMIT 散射迹与α/t²极限 | L012.STRIP、L012.BOUNDARY | 固定同一种子；端点支配函数可积 | [a,η]极限及(0,η]增长 | `RECCVS/proofs/RECCVS_L013.md`，行40–56，## 2. 极限与正系数 | 按列出的假设与域使用 |
| L013.RIGID h=0与初始零场等价 | L013.LIMIT、L012.STRIP、L010.TRANSPORT | 先选足够大N、再缩η；常数独立于时间且选取合法 | 同一固定近视界条带 | `RECCVS/proofs/RECCVS_L013.md`，行61–81，## 4. 反向估计：不丢失Wilson相位 | 按列出的假设与域使用 |
| L013.OUTER 非零初始场提供正增长外边 | L013.RIGID、L013.LIMIT | 实际初始场在[0,η]不恒零 | 固定b=η的全时间外边 | `RECCVS/proofs/RECCVS_L013.md`，行82–89，## 5. 进入全中心估计的接口 | h与晚时阈值没有族统一界 |

## L014：抽象外边下的全余域体积与寿命

原稿：`RECCVS/proofs/RECCVS_L014.md`；包内：`center/RECCVS_L014.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L014.VOLUME 抽象外边给全余域有限体积 | SYS、OUTER_INPUT、POS_DOMAIN、INSEG | 对实际连通前缀作单调穷尽；不预设末端中心 | 整个实际D_b余域 | `RECCVS/proofs/RECCVS_L014.md`，行24–47，## 2. 全余域有限体积：无需中心边界条件 | 按列出的假设与域使用 |
| L014.CENTER 中心截面电磁积分与加权半径界 | L014.VOLUME、REG_CENTER | 该截面确实以正则中心结束 | 仍存在中心的完整截面 | `RECCVS/proofs/RECCVS_L014.md`，行48–74，## 3. 入射段仍以正则中心结束时：全深部电磁积分与半径控制 | 按列出的假设与域使用 |
| L014.AXIS dτ/dt=1/(2α)轴线恒等式 | SYS、REG_CENTER | dr\|Γ=0、Δ→1；相容双零坐标 | 实际正则轴线 | `RECCVS/proofs/RECCVS_L014.md`，行75–105，## 4. 中心固有时间：一个精确全局接口 | 按列出的假设与域使用 |
| L014.LIFETIME 外边下中心剩余固有长度有限 | L014.AXIS、OUTER_INPUT、INSEG | 中心在固定外边更深处且仍存在 | 该正则轴线的实际剩余段 | `RECCVS/proofs/RECCVS_L014.md`，行75–105，## 4. 中心固有时间：一个精确全局接口 | 不推曲率、零仿射长度或可见性 |
| L014.EXTENSION 体积可供正半径延拓原理调用 | L014.VOLUME、KOM_EXT | 整个去端点菱形实际存在、r≥r0>0、紧初始边 | 仅满足全部延拓前提的菱形 | `RECCVS/proofs/RECCVS_L014.md`，行106–118，## 5. 能调用的正半径延续与不能调用的结论 | 按列出的假设与域使用 |

## L015：首个非零点与轴线有限固有寿命

原稿：`RECCVS/proofs/RECCVS_L015.md`；包内：`center/RECCVS_L015.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L015.NONZERO 中心与视界电荷差强迫非零场 | SYS、I001、INSEG、REG_CENTER | 中心活到t=1，完整该截面，QH=1/QΓ=0 | 实际t=1截面 | `RECCVS/proofs/RECCVS_L015.md`，行17–29，## 2. t=1上的实际完整截面与非平凡性 | 按列出的假设与域使用 |
| L015.GAPOUTER 零场空隙后构造合法正外边 | L015.NONZERO、SYS、CHAR、I001 | 首非零点c>0；有限ERN参考矩形、固定宽度、反向Goursat唯一性 | 同一解首非零点旁条带 | `RECCVS/proofs/RECCVS_L015.md`，行50–80，## 4. 首个非零点旁的固定宽度、全部时间实际条带；`RECCVS/proofs/RECCVS_L015.md`，行30–49，## 3. c>0：只有已证零场区才识别为电真空；`RECCVS/proofs/RECCVS_L015.md`，行81–103，## 5. 反向特征唯一性强迫增长系数为正 | w≥0选择的延拓不自动属于原MGHD |
| L015.OUTER 两种非零起点情形均提供外边 | L015.NONZERO、L013.OUTER、L015.GAPOUTER | c=0用L012–13；c>0用本稿§3–5 | 中心活到t=1时同一实际全时间外边 | `RECCVS/proofs/RECCVS_L015.md`，行5–16，## 1. 命题：去除近视界非零假设 | 按列出的假设与域使用 |
| L015.LIFETIME 全部轴线寿命分支固有长度有限 | L015.OUTER、L014.LIFETIME、L014.AXIS、I001 | t_end=∞用外边；t_end<∞用视界α在有限区间正下界 | 同一实际MGHD轴线 | `RECCVS/proofs/RECCVS_L015.md`，行104–122，## 6. 轴线有限寿命的完整分情况 | 这一层不依赖先证明曲率奇异或深部λ号 |

## L016：正则中心曲率与物理导数

原稿：`RECCVS/proofs/RECCVS_L016.md`；包内：`center/RECCVS_L016.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L016.CURVATURE 中心精确曲率/质量恒等式 | SYS、REG_CENTER | 旋转对称、无磁荷；逐事件中心极限 | 四维实际正则中心 | `RECCVS/proofs/RECCVS_L016.md`，行37–56，## 3. Einstein方程及Riemann分解 | 不依赖I001、L012或L015 |
| L016.PHYSICAL Dτφ=4αT=P/(-ν) | L014.AXIS、REG_CENTER | 中心空间共变梯度为零 | 实际正则轴线 | `RECCVS/proofs/RECCVS_L016.md`，行57–71，## 4. 双零导数与物理导数的区别 | 按列出的假设与域使用 |
| L016.SINGULAR 有限固有时曲率判据 | L016.CURVATURE、L016.PHYSICAL、L015.LIFETIME | 另加limsup\|αΓTΓ\|=∞ | 该轴线有限固有时端点 | `RECCVS/proofs/RECCVS_L016.md`，行72–83，## 5. 已知有限寿命之后的准确曲率判据 | 增长前提未证；趋轴邻域与零仿射/可见性另证 |

## L017：中心电荷的尖锐径向能量障碍

原稿：`RECCVS/proofs/RECCVS_L017.md`；包内：`center/RECCVS_L017.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L017.POINCARE 加权Poincaré与ground-state分解 | BESSEL | 中心有界且足够光滑的复f，f(R)=0；相容端点极限 | 独立径向函数类 | `RECCVS/proofs/RECCVS_L017.md`，行30–51，## 2. 加权 Poincaré 不等式及其证明 | 按列出的假设与域使用 |
| L017.SHARP S≥4j\|Q\|/(\|e\|R²)与径向尖锐性 | SYS、REG_CENTER、L017.POINCARE | 完整入射截面、Q(0)=0、φ(R)=0；Wilson输运 | 该截面及独立径向函数类 | `RECCVS/proofs/RECCVS_L017.md`，行52–80，## 3. 完成平方：同时保留场幅度和相位 | 径向极值不认证全时空约束实现 |
| L017.RATIO 极端截面αΓ/αH下界 | L017.SHARP、SYS | R=M、\|Q\|=M；仍连接正则中心 | 该极端完整截面 | `RECCVS/proofs/RECCVS_L017.md`，行81–93，## 4. 它闭合什么、不闭合什么 | φ_r(R)=0给严格性但无统一间隙；不决定陷俘号 |

## L018：有限实际区间谱陷俘判据

原稿：`RECCVS/proofs/RECCVS_L018.md`；包内：`collapse/RECCVS_L018.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L018.SIGN 首谱值与实际端点膨胀同号 | SYS、VIS、FINITE_INTERVAL、SL | 真实V；r>0与ν<0 | 有限实际区间 | `RECCVS/proofs/RECCVS_L018.md`，行38–53，## 2. 证明：不预设未陷俘 | 按列出的假设与域使用 |
| L018.CERT 正/负有限区间积分证书 | L018.SIGN | 可靠V_-≤V≤V_+；实际区间存在 | 该有限区间 | `RECCVS/proofs/RECCVS_L018.md`，行54–72，## 3. 无须本征求解的有限时间证书 | 按列出的假设与域使用 |
| L018.CENTER 中心χ与二阶物理导数桥梁 | L018.CERT、REG_CENTER | χ>0；ell=π/√χ的整段存在；\|D_L²φ\|≤χ/(2π) | 从该中心发出的实际有限线 | `RECCVS/proofs/RECCVS_L018.md`，行73–92，## 4. 从中心物理导数到陷俘的定量桥梁 | χ大本身不提供存在长度或二阶界 |
| L018.ROBIN 正半径初点Robin版本 | L018.SIGN | 记录w0=r_s(0)/r(0)，固定仿射尺度 | 不从中心起算的实际段 | `RECCVS/proofs/RECCVS_L018.md`，行93–102，## 5. 不从中心起算的实际线 | 按列出的假设与域使用 |

## L019：内部边际球刚性与仿射预算

原稿：`RECCVS/proofs/RECCVS_L019.md`；包内：`collapse/RECCVS_L019.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L019.FIRST 内部首次触零刚性 | SYS、POS_DOMAIN | U内部点；U邻域λ≥0才能推λ_U=0 | 有限紧实际光滑片内的正半径球 | `RECCVS/proofs/RECCVS_L019.md`，行5–21，## 1. 首次触零的约束 | 按列出的假设与域使用 |
| L019.BUDGET 无陷俘未来边际射线预算 | L019.FIRST、L010.TRANSPORT | 每个未来点的U邻域λ≥0；整段实际存在 | 该内部边际射线 | `RECCVS/proofs/RECCVS_L019.md`，行22–56，## 2. 无陷俘假设下的整个未来边际射线 | φ0≠0才有有限预算；超预算但仍存在才推出陷俘 |

## L020：固定八阶领先剖面证书

原稿：`RECCVS/proofs/RECCVS_L020.md`；包内：`collapse/RECCVS_L020.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L020.PROFILE 固定有理剖面与八个零矩 | E020 | K=8,n=88,σ=1/20；能量归一化 | 辅助半线x≥0 | `RECCVS/proofs/RECCVS_L020.md`，行5–32，## 1. 全部参数固定 | 按列出的假设与域使用 |
| L020.CURRENT 正电流滤波论证 | L020.PROFILE | 高斯有理多项式及上半平面根结构 | x>0辅助剖面 | `RECCVS/proofs/RECCVS_L020.md`，行33–45，## 2. 正电流的解析证明 | 按列出的假设与域使用 |
| L020.J J恰一次简单负到正变号 | L020.PROFILE、E020 | 精确分子与六叶整数覆盖证书 | 紧化全半线 | `RECCVS/proofs/RECCVS_L020.md`，行46–75，## 3. 一次变号的整数证书 | 按列出的假设与域使用 |
| L020.KERNEL 𝒦单调且≥𝒦(0)>2^-854 | L020.PROFILE、L020.J、KDEF | 核ODE/边界按KDEF；正端点精确比较 | 全辅助半线 | `RECCVS/proofs/RECCVS_L020.md`，行76–112，## 4. 从正性升级为单调性和端点最小值 | 按列出的假设与域使用 |

## L021：截断、矩修复与周期族

原稿：`RECCVS/proofs/RECCVS_L021.md`；包内：`collapse/RECCVS_L021.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L021.FIX 光滑截断与精确零矩修复 | L020.PROFILE、L020.CURRENT | 固定ρ,bump与积分矩阵A；A^-1解析有界 | 单块紧支持剖面 | `RECCVS/proofs/RECCVS_L021.md`，行51–78，## 3. 矩矩阵的明确可逆性；`RECCVS/proofs/RECCVS_L021.md`，行5–34，## 1. 固定的光滑函数；`RECCVS/proofs/RECCVS_L021.md`，行35–50，## 2. 截断误差的实数上界 | 这里精确不意味着所有超越积分都是有理数 |
| L021.CORE 电流核心可靠正余量 | L020.PROFILE、E021 | 核心Bernstein正性与小C1修复 | [3/4,33/4]及修复核心 | `RECCVS/proofs/RECCVS_L021.md`，行79–90，## 4. 电流核心的精确包络 | 按列出的假设与域使用 |
| L021.FAMILY 周期族M_s(z_c)=c_s | L021.FIX、L021.CORE | 固定T及\|c_s\|≤2^-4096；共同端点开空隙 | 整个具体周期族 | `RECCVS/proofs/RECCVS_L021.md`，行91–110，## 5. 固定周期与半线矩坐标 | 按列出的假设与域使用 |
| L021.KERNEL λ<3/5与周期核>2^-855 | L021.FAMILY、L020.KERNEL、KDEF | 单块L1比较与周期精确求和 | 全周期半线及参数球 | `RECCVS/proofs/RECCVS_L021.md`，行111–141，## 6. 核与耦合余量 | 实际形成另需有限振幅FLIFT实例 |

## L022：光滑尾界与锥/时空误差预算

原稿：`RECCVS/proofs/RECCVS_L022.md`；包内：`collapse/RECCVS_L022.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L022.TAIL 同一光滑极限固定Ck尾界 | FSMOOTH | 每步确实满足δ_*2^-n；N≥k+1 | 同一修复序列 | `RECCVS/proofs/RECCVS_L022.md`，行5–22，## 1. 尾部不是无控制的无限对象 | 按列出的假设与域使用 |
| L022.CONE 显式锥几何安全预算 | SYS | 参考r/t≥a,H/t≥h,β>0与场范数已认证 | 同一仿射锥[0,1] | `RECCVS/proofs/RECCVS_L022.md`，行23–95，## 2. 不含隐藏连续依赖常数的锥几何预算 | a,h,β尚需具体有限成员 |
| L022.FLOW 修复尾误差的实际W传播 | L022.TAIL、COMMON_FLOW | 共同域、同一物理线、经过证明的C_flow | 该共同有限实际域 | `RECCVS/proofs/RECCVS_L022.md`，行96–110，## 3. 真正的时空传播还需要什么 | 这是尚未取得输入的条件性接口 |
| L022.DECISION 总误差下正/负谱判决 | L022.FLOW、L018.CERT | 可靠数值包络、严格余量ρ、总误差满足门槛 | 同一有限实际区间 | `RECCVS/proofs/RECCVS_L022.md`，行111–136，## 4. 尾部误差与数值误差合并后的判决 | 不是原种子的已完成实际符号证书 |

## L023：第一周期严格陷俘机制

原稿：`RECCVS/proofs/RECCVS_L023.md`；包内：`collapse/RECCVS_L023.md`。

| 审计ID/结论 | 直接前置 | 额外假设 | 适用域 | 原稿来源 | 边界 |
| --- | --- | --- | --- | --- | --- |
| L023.ANLIM 保守充分条件给严格陷俘 | SYS、ANLIM、MINK_FILL、POS_DOMAIN | 23.1及完整外部经典发展接口；边际升级保持Q²/r²<1 | 有限第一周期特征发展 | `RECCVS/proofs/RECCVS_L023.md`，行5–37，## 1. 外部接口和归一化审计 | 按列出的假设与域使用 |
| L023.FIRST 第一周期质量/半径/电荷/物理宽度 | FLIFT、MINK_FILL | 真实有限根；固定可行周期族；q≤bδ，C≥0 | 真实第一物理周期[t1,t2] | `RECCVS/proofs/RECCVS_L023.md`，行58–99，## 3. 第一物理周期的质量集中：精确而非平均展开；`RECCVS/proofs/RECCVS_L023.md`，行100–125，## 4. 第一周期电荷小，但不能略过仿射尺度 | 按列出的假设与域使用 |
| L023.BRANCH 充分长指定分支严格陷俘 | L023.FIRST、L023.ANLIM、FLIFT | 23.6；c_m,τ_m,ρ_m的真实分支渐近 | 指定完整Minkowski填充分支 | `RECCVS/proofs/RECCVS_L023.md`，行126–162，## 5. 分支负号结论 | 不是全部极端形成解的禁止定理 |
| L023.MGEOM L021族显式几何长度门槛 | L021.KERNEL、L021.FAMILY、L023.FIRST、E023 | μ=3/5、指定τ带、m≥2^2104156 | 该具体族的几何充分条件 | `RECCVS/proofs/RECCVS_L023.md`，行140–162，### L021族的显式几何长度门槛 | 端点根门槛m_lift仍非有效 |
| L023.SMOOTH 可选择修复保留陷俘并排除候选 | L023.BRANCH、FSMOOTH、CAUCHY、L001.EXCLUDE | 共同特征/Cauchy实现；实际输入强范数误差<ε_trap | 选定有限成员及足够小修复的光滑极限 | `RECCVS/proofs/RECCVS_L023.md`，行163–175，## 6. 光滑修复及目标的准确影响 | 具体ε_trap与未冻结原光滑种子仍待认证；L022可提供尾预算 |


---

# 依赖缺口与循环审计

## 判定范围

阶段0检查的是陈述的依赖与来源。未运行端点求根、PDE演化、历史数学认证脚本，也未逐行独立验证全部解析估计。下表区分未取得输入、独立审查风险、记号缺省和版本管理缺省，均不自动等同于原命题错误。

| 编号/类型 | 涉及结论 | 发现 | 实际影响 | 关闭条件/任务 |
| --- | --- | --- | --- | --- |
| G01 来源版本未固定 | L001.PERSIST、L001.EXCLUDE、FCENTER | Cauchy强拓扑稳定性与Penrose工具已被标准形式调用，但本包没有唯一固定的公开原始定理版本/编号；正半径CHAR已给来源仍待逐项核对。 | 不影响登记为条件输入；影响独立审查者确认全部正则性与量词。 | 阶段1固定准确版本、规范、Sobolev阶数及几何唯一性/传播陈述。；R05/R06 |
| G02 导入解析链未独立复核 | FLIFT、FSMOOTH、FCENTER、FGLOBAL、I001 | 形成包的有限阶、同一种子、中心、全局识别均有正文，但仍是内部稿；符号PASS不能升级其PDE/因果结论。 | L007–L015的实际MGHD应用保持条件性；L023局部分支另列所需输入。 | 按模块逐项审查，避免把I001整体当成无条件黑箱。；R01/R02/R05/R06 |
| G03 具体非线性根缺失 | FLIFT、L021.KERNEL、L023.FIRST | 17个实有限振幅残差尚无固定m的认证根；C1渐近余项常数和m_lift尚未有效化。 | 领先核、零矩与参数球证书不能指定实际有限成员。 | 给规范化残差、Jacobian及统一C1余项，认证参数盒与根。；R01 |
| G04 两个长度门槛未合并 | L023.MGEOM | m_geom=2^2104156只验证几何充分条件；另有未有效化的端点提升门槛。 | 取m=m_geom不能自动声称已有形成成员。 | 用有效提升门槛和几何门槛共同选择m，必要时收紧保守包络。；R01/R03 |
| G05 完整填充/共同实现未冻结 | MINK_FILL、L023.BRANCH、L009.ACTUAL | 左端Minkowski球面数据与中心局部平直不唯一指定整入射锥；旧任意光滑种子的实现尚未与L023分支一一识别。 | 不能把条件性分支排除自动改成对旧指定种子的终审。 | 冻结完整入射锥、规范、共同Cauchy面及依赖域；记录所选对象。；R02 |
| G06 外部陷俘定理接口待审 | L023.ANLIM、ANLIM | L023采用证明(2.16)定义并记录引言定义差异、场尺度、电流号和物理宽度；该接口尚未独立复核。 | L023负号机制继续保留外部接口条件；历史有理门槛检查仅覆盖代数。 | 逐假设复查Theorem1.3、§3与实际发展/严格升级接口。；R05/R03 |
| G07 修复预算到实际强拓扑的传递缺失 | L022.CONE、L022.FLOW、L023.SMOOTH | L022给出锥上C1安全预算；共同实际域、C_flow或ε_trap及锥数据到Cauchy强范数映射尚未认证。 | 当前不能对任意既有光滑修复宣称保留陷俘；按足够小预算选择修复仍是条件性存在陈述。 | 优先检查修复支撑与有限依赖域；否则定量稳定或重新验证扰动后的陷俘定理输入。；R04 |
| G08 全时间bootstrap/反向唯一性待审 | L012.STRIP、L012.EXIST、L013.RIGID | 时间统一核界、最高阶有限矩形延续、N相关常数和反向吸收顺序是已写出的关键论证，尚未独立复核。 | 属于审查风险，不是已发现的反例；不能从图无环推出这些估计成立。 | 按同一固定种子和合法N→A→η顺序逐式检查。；R06 |
| G09 全局标签/零场空隙延续待审 | L015.NONZERO、L015.GAPOUTER、L015.LIFETIME | t=1完整实际截面、ERN参考紧矩形的有限步连续依赖、反向Goursat唯一性及MGHD识别仍需要逐项独立复核。 | w≥0所选局部延拓不属于已识别原MGHD；中心已提前终止分支必须单独处理。 | 核对I001实际覆盖与有限步稳定常数、实际边的唯一性识别。；R06 |
| G10 中心端点动态分类缺口 | L016.SINGULAR | αΓTΓ的实际增长/有界性及趋轴Q/r²、m/r³和归一化导数控制尚未取得。 | 有限类时固有寿命不能升级为曲率奇异或某种中心延拓；目标C另需零仿射与可见性。 | 在已审查实际域内研究规范不变中心与趋轴估计，按强/弱正则性分类。；R07 |
| G11 其他候选的全域陷俘号开放 | L008.ONECROSS、L011.WILSON、L018.CERT、L019.BUDGET | 全深部前缀符号、实际V包络及所需有限区间存在性未取得；入射电荷能量下界不提供出射T下界。 | 有限体积、L017尖锐常数和近视界正号都不能认证全域无陷俘；L023只处理指定填充分支。 | 对新候选取得真实有限负证书，或闭合全部实际通量预算。；R03/R08 |
| G12 完整色散与真正阈值缺口 | L006.INNERCONE、L001.EXCLUDE | L006尚未覆盖任意外锥非径向因果线和完整I+；现有形成输入也没有同一C1完整三分支族。 | 当前没有A的合格临界基点；无有限陷俘只是必要条件。 | 补足完整色散端，构造受控同一参数族并逐侧证明全局性质。；R08/后续A |
| G13 曲率、仿射与可见性接口缺口 | L003.TIDAL、L012.PP、L016.SINGULAR | 实际非零首项、近临界共同误差、标量曲率收缩、有限零仿射端点及逃逸到同一I+均未取得。 | B、C未证明；黑洞内轴线不完备不提供可见性。 | 按B/C各自量词分别建立，D另需约束空间与可微结构。；后续B/C/D |
| G14 核记号来源已补定位 | KDEF、L020.KERNEL | L020没有重新写I_C/I_E完整积分定义；阶段0已从有限阶剖面稿首段补足并登记KDEF。 | 这是跨稿记号/来源缺省，不是已发现的核正性证明错误。 | 后续正式编辑时给明确交叉引用；本轮保持原文不改。；阶段0已登记 |
| G15 证书覆盖与精确修复的区别 | E020、E021、E023、L021.FIX | 整数/有理脚本、解析光滑截断与超越积分矩阵、实际时空根认证是不同覆盖层；本轮未重跑历史数学认证。 | 精确矩修复是函数/积分层的精确等式；不能把全部内容描述成一个有理计算证书。 | 各证书分别记录输入、适用域、算法、拒绝路径与尚未覆盖部分。；R01/R03 |
| G16 远端Git版本未观测 | 基线管理 | 本次已冻结三附件及ZIP全部203项的SHA-256；远端仓库commit与4个issue的实时明细未读取。 | 可追溯基线是附件快照，不声称已同步Git HEAD或修改仓库。 | 需要与远端绑定时，再记录具体commit并做文件差异比较。；版本管理补充项 |

## 回路与拆分

| 回路 | 原稿中的关系 | 阶段0判定 | 正确读取方式 |
| --- | --- | --- | --- |
| C01：L014 ↔ L015 | L014§1说L015可提供外边；L015用L014求轴线寿命 | 整稿引用层的表面回路；抽象定理与其实例不同 | 先证明L014在OUTER_INPUT下的估计；L015.OUTER独立构造外边；再应用L014得到L015.LIFETIME |
| C02：有限阶提升稿 ↔ 半径正性稿 | 提升§5用半径稿q≥aδ吸收初始项；半径稿引用提升的q=δp+O(δ²) | 需按小节拆分；未发现不可消解的显式回路 | 提升§2–3基底FRBASE → 半径正性FRPOS → 提升§4–6的jets/IFT，而非两个整文件互作黑箱 |
| C03：L013/L015的后续引用 | L013末节指向L014–15应用，L015在c=0分支使用L012–13 | 后续应用引用不能当作L013的证明前提 | L012 → L013；L013.OUTER供L015两分支构造；L014在抽象外边下独立成立 |
| C04：L022与L023的稳定应用 | L022条件性说明误差如何保留实际负证书；L023说可选修复保留陷俘 | 未发现正文中的证明循环；存在把未取得输入当成结果的风险 | 先有有限实际陷俘与共同域/稳定阈值，再兑现修复预算；C_flow和ε_trap不能由尾部求和本身得到 |
| C05：I001与内部寿命/曲率 | L007–15用I001的实际MGHD/视界身份；源形成稿没有引用这些新L稿 | 本快照未发现I001借L015/L016反向证明自身的显式循环 | I001形成链保持独立来源；内部分类是其后果；如未来用分类反证I001，须另列完整论证 |

由114个输入/逐命题节点与203条直接证明/陈述输入边组成的记录图，经拓扑检查全部可排序，没有未定义ID和有向环。这个结论只针对当前人工拆分并登记的依赖图，不认证条件输入已兑现，也不排除正文中尚待数学审查的隐藏先验。

## 不能混同的对象

1. L020的辅助半线w、L021的周期族z_c、有限m的真实端点根、同一光滑极限Φ∞、诱导Cauchy数据必须分别登记。
2. λ≈0.5045578903是领先比值；L021–23的具体测试耦合为μ=3/5。单位M=1固定后二者仍承担不同作用。
3. μ>1/2的限定形成门槛不证明A不存在，也不证明A存在。
4. 每个有限T的局部余量、一个固定种子的全时间条带余量、参数族统一余量是不同量词。
5. 中心固有时、零线仿射参数和坐标t/V长度分别验收。
6. 边际球、严格陷俘球、零测地不完备、黑洞身份、曲率奇异和可见性分别验收。


---

# 建议目录结构与原稿映射

本包是六目录方案的可查看副本；未移动或修改远端仓库。L编号保持不变，目录只表示内容归属。原稿按原字节复制；文件SHA-256与旧路径见SOURCE_MAP.csv。

| 目录 | 数学职责 | 本包原稿/材料 | 后续应放入 |
| --- | --- | --- | --- |
| foundations/ | 模型、规范、约束空间、强拓扑、标准稳定/不完备工具、小数据基线 | MODEL.md；FORMATION_INPUT_AUDIT.md；L001、L002、L006 | 外部定理的准确版本与归一化表；完整色散接口 |
| geometry/ | 实际双零域、Raychaudhuri/Gauss/波输运、膨胀号及近视界控制 | L004、L005、L007、L008、L009、L010、L011、L012 | 共同实际域、全通量估计、正半径延拓 |
| center/ | 中心相容、散射迹、全余域体积、轴线寿命、中心曲率、电荷能量障碍 | L013、L014、L015、L016、L017 | 趋轴估计、有限寿命端点的强/弱分类 |
| collapse/ | 有限区间陷俘、形成剖面、非线性提升实例、修复预算与第一周期机制 | L018、L019、L020、L021、L022、L023 | 17维根、完整填充、第一周期实际输入、新候选与A族 |
| singularity/ | 规范不变潮汐、曲率、有限仿射奇点、可见性与稳定性 | L003；本阶段未新增奇点定理 | B/C/D的各自证明与因果边界分类；可延拓结果也按正则性记录 |
| verification/ | 基线、来源、依赖表、检查器、证书、拒绝记录与审查状态 | 本阶段审计文件；sources/中已有形成稿、历史脚本/证书和原始文献文本 | 独立审查报告；根/流误差证书；复算日志；缺口状态 |

## verification/文件说明

| 文件 | 用途 |
| --- | --- |
| DEPENDENCY_TABLE.md | 23份整稿的核心前置、应用前置、假设、适用域和限制 |
| CLAIM_CATALOG.md / CLAIMS.json | 78个逐命题/推论/接口的精细来源与依赖 |
| INPUT_REGISTER.md / INPUTS.json | 36个定义、外部结果、导入模块和条件输入 |
| GAPS_AND_CYCLES.md / GAPS.json | 16项缺口/风险/定位问题和5组回路关系分析 |
| BASELINE.json | 三附件哈希及ZIP全部203项的原始路径/大小/哈希；remote_commit为空 |
| SOURCE_MAP.csv / LEMMAS.json | 23原稿从旧路径至六目录的对应与字节哈希 |
| dependency_graph.json / dependency_edges.csv | 直接依赖与应用/解释性边分层记录 |
| check_audit_package.py / CHECK_RESULTS.json | 检查原稿字节、来源范围、ID闭合和图的拓扑顺序；不检查数学真实性 |
| INCLUDED_SOURCE_MAP.json | 本包附带来源副本与原始ZIP路径/哈希的对应 |
| PACKAGE_FILES_SHA256.json | 包内全部交付文件的哈希索引；不包含该索引自身 |
| sources/ | 形成证明与支持稿、历史experiments、五份原始文献文本、旧摘要与任务记录；均标为来源材料 |

## 迁移规则

本轮保持原稿正文不变，故原稿中的旧相对路径仍以原始RECCVS布局为解释基准。来源对照表负责定位新副本；真正迁移仓库时再统一修复路径。旧ROUTES_AND_TASKS为历史来源，当前R01–R08以本次用户说明为准。

本包没有纳入原项目全部文献PDF、所有旧轮次档案和完整Git历史；它是阶段0的依赖审计包，不能宣称恢复整个研究项目。
