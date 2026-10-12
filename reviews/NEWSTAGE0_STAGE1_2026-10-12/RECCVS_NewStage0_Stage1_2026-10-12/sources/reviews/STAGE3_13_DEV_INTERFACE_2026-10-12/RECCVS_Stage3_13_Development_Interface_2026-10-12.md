# 阶段 3.13：候选端点冻结与同一发展接口核验

**所有数学结论：GPT 主张，未经外部独立审查。** 本轮的自审、源文对照、精确计算与解析证明稿均不构成外部独立审查。本文没有把未核验的有限正则接口升级为已经获得独立认证的定理。

## 1. 本轮决定

候选 ψ₀ 的定义、固定标签、增强强范数、椭圆下界和条件固定状态全部冻结。对同一发展接口，本轮展开了模型专属的约化/规范传播，复核共同域嵌入的逻辑顺序，并补出“紧支撑重切片的最大性转移”引理。因此，在明示的实际解、Cauchy 与有限正则发展接口成立时，可以确认：从候选端点重新建立的双向 MGHD 与原双向 MGHD 是同一物理解，允许时空等距识别和 U(1) 规范变换。

**ψ₀ 目前仍仅可条件固定。** 尚不能给不继承这些数学接口的无条件认证。Pa 的数字缺失只影响原同伦共同常数的数字实例化；它不是候选端点升级的必要卡点。原 ψa=ψ₀ 也不是同一发展识别所需结论。

“无条件认证”与“外部独立审查”分开登记：前者要求本文不再悬置实际输入/适用接口；后者是证据审查状态。本轮没有完成前者，所有数学结论仍保持后者的未审查标注。

## 2. 冻结端点与两个坐标标签

固定 μ=3/5、m_geom=2^2104156；ADM=Q=1。原根摘要不变：

`7845f2276b7dc12669d9e27861704bdee99f395458c35647fc9c734f93fb6dc2`。

冻结常数为

\[
L=2^{2104156}1048578,\quad H=2^{100}e^{200(L+4)},\quad a=e^{-8H},
\]
\[
D_8=e^{e^{102H}},\quad N_7=e^{e^{200H}},\quad
\epsilon=e^{-e^{300H}},\quad \kappa_{AF}=e^{-8H-2L}/64.
\]

ε 在本文等于前轮 ε*。候选定义

\[
u(x)=\begin{cases}e^{-1/x},&x>0,\\0,&x\le0,\end{cases}\quad
b_0(t)=u(16(t-5/16))u(16(7/16-t)),
\]
\[
I_b=\int b_0(t)dt>1/1296,\quad \psi_0=b_0/I_b,
\quad P_{\psi_0}<2^{247}.
\]

原 d_base、K 与近中心前移图 f 不变。候选外侧图为

\[
d_0=d_{base}+K\psi_0,\quad
K=a/8-\int_{t_0}^{t_R}d_{base},\quad
U=\sigma_0^{new}(t)=-\int_{t_0}^{t}d_0(s)ds.
\]

路径参数的 τ=0 表示原 ψa，τ=1 表示候选 ψ₀，不能混淆这两个 0。候选前移面记作 S_b=Σ−,ψ₀，原前移面为 S_a=Σ−,ψa，未前移的原面为 S_old。

冻结标签 y：中心沿用 harmonic Cartesian 图标签，外侧沿用旧 areal Cartesian 标签，在 f=0 的开环带精确接回。R=|y| 在中心一般不等于实际面积半径 r。整个增强带权范数均在 y 标签计算，权指数 −1：γ−Id−hADM、Φ、a 在 H6_−1；K、E−ECoul、B、Π 在 H6_0；加 ADM、Q 有限参数，按分量范数和计量。参考主项沿用 ζAF=θ(R−2)。径向规范必须同步变 Φ、Π 相位。

端点证据冻结为

\[
\boxed{\gamma_y\ge\epsilon/2\,Id,\quad
\|\Psi_{-,\psi_0}^{rad}\|_{X_{-1}^{6,enh}(y)}\le B_0^u,}
\tag{2.1}
\]
\[
B_6^u=2^{34008+2^{41}}(1+N_7)\epsilon^{-15},
\]
\[
\boxed{B_0^u=2+2^{2056}\epsilon^{-8}
(1+2^{31}N_7+2^8B_6^u)^{12}
+2^{120}\kappa_{AF}^{-8}+2^{2301}.}
\tag{2.2}
\]

若全局另用 areal Cartesian 标签 x，则冻结零阶界 γx≥ε/8 Id。未认证 x 标签的六阶范数也可直接取 B0u。

原固定同伦另冻结 Pbar=max(Pa,2^247)、Dbar=e^(100H)+(a/8)Pbar、d*=a²/2^20、J*=a²e^(−2L)/2^21，以及前轮的 Bpath(Pa)、cpath(Pa)。法函数界为 g⁻¹(dFτ,dFτ)≤−2d*；cpath=min(1,α,a²/(2^25e^(2H)Dbar²))。这些是已固定一个光滑路径的共同有限界，仍非 Pa 独立的数字证书。

文件身份、定义表达式与接口状态见 frozen/ENDPOINT.json、INPUT_LOCK.json；前轮完整证据包按字节保存于 frozen/stage312。冻结不改变各项的条件性审查状态，也没有提供全空间物理场的数值网格。

## 3. “同一发展”必须满足什么

同一根、同一 ADM/Q、同一函数预算不足以确认同一发展。需要比较实际限制到切片的数据和场，而不是比较常数。

设 (M_a,g_a,A_a,Φ_a) 是原双向 MGHD，j_b:S_b→M_a 是候选嵌入。若存在候选数据的 MGHD (M_b,g_b,A_b,Φ_b)，真正需要的是保持未来取向的满等距映射 I:M_a→M_b，且

\[
I\circ j_b=i_b,\quad I^*g_b=g_a,
\quad I^*A_b=A_a+d\chi,\quad I^*\Phi_b=e^{-i\mu\chi}\Phi_a.
\tag{3.1}
\]

场强相等 I*Fb=Fa；Π 与 Φ 按同一相位变换。χ 可以取足够的局部有限 Sobolev 正则性；其全局规范成员资格仍须与所选规范群相容。这里采用前轮允许径向消势的规范群，不追加“χ 必须在无穷远趋常数”的限制。

环境流 hτ 将嵌入图送到另一张图，但一般 hτ*g≠g，不能令 I=h₁。规范 χ 也不移动切片。重新演化识别依靠几何唯一性和最大性，数据是同一原场沿新图的真实抽取。一般有 Ψb(y)≠Ψa(y)，不会认证两张切片的初值函数逐点相同。

## 4. 模型专属约化：主符号核验

沿用 D001：D=∇+iμA、Jb=μ Im(Φ̄ DbΦ)、G=2T，T=TEM+TSF。Ricci 右侧为

\[
S_{ab}=2F_{ac}F_b{}^c-\tfrac12g_{ab}F^2
+2\Re(D_a\Phi\overline{D_b\Phi}).
\]

设 Hρ=g^ab Γρ_ab、L0=g^ab∂aAb。采用

\[
R_{ab}-Q_{ab}=S_{ab},\quad
Q_{ab}=\tfrac12(g_{a\rho}\partial_bH^\rho+g_{b\rho}\partial_aH^\rho),
\]
\[
\nabla_aF^a{}_b+\partial_bL_0=J_b,\qquad D^aD_a\Phi=0.
\tag{4.1}
\]

L0 是坐标函数，物理 Lorenz 散度 C=∇aA^a=L0−HρAρ。两者仅在 H=0 时一致。

直接展开 Maxwell 行：

\[
\nabla_aF^a{}_b
=g^{ac}\partial_a(\partial_cA_b-\partial_bA_c)
-H^cF_{cb}-g^{ac}\Gamma^d_{ab}F_{cd},
\]
\[
\partial_bL_0=(\partial_bg^{ac})\partial_aA_c
+g^{ac}\partial_b\partial_aA_c.
\]

混合二阶势项相消，得到

\[
\boxed{g^{ac}\partial_a\partial_cA_b
=J_b+H^cF_{cb}+g^{ac}\Gamma^d_{ab}F_{cd}
-(\partial_bg^{ac})\partial_aA_c.}
\tag{4.2}
\]

右侧没有二阶 g。标量完整展开为

\[
\boxed{g^{ab}\partial_a\partial_b\Phi
=H^c\partial_c\Phi-2i\mu A^a\partial_a\Phi
-i\mu(L_0-H^cA_c)\Phi+\mu^2A^aA_a\Phi.}
\tag{4.3}
\]

Einstein 行主部为 −g^cd∂c∂dgab/2，其余只含 g、g⁻¹、∂g、A、∂A、Φ、∂Φ。故所有实变量构成同一 Lorentz 主符号的对角拟线性波系统。g 对称计 10 分量，A 为 4，复 Φ 为 2。

没有先令 H=L0=0 来删去标量式中的一阶项；否则不能用完整 KG 保证下一节的电流守恒。主符号的 Maxwell 消项是一般代数身份；程序还在数个非对角有理 Lorentz 度量上复核 Einstein 全部二阶 jet 系数，后者是有限抽样核验，不能替代一般解析身份。

## 5. 规范与约束传播：三角次序

### 5.1 Maxwell 规范先恢复

完整 KG 给

\[
\nabla_aJ^a=\mu\Im(\bar\Phi D^aD_a\Phi)=0.
\]

反对称 F 的双散度为零。对约化 Maxwell 取散度，获得

\[
\boxed{\square_g L_0=0.}
\tag{5.1}
\]

在候选面上选未来坐标 t，g00=−1、g0i=0、gij=γij，并初始化

\[
\dot g_{ij}=-2K_{ij},\quad \dot g_{00}=2tr_\gamma K,
\quad \dot g_{0i}=\gamma^{kl}(\partial_k\gamma_{li}-\tfrac12\partial_i\gamma_{kl}),
\]
\[
A_0=0,\ A_i=a_i,\quad \dot A_i=E_i,
\quad \dot A_0=\gamma^{ij}\partial_i a_j,
\quad \dot\Phi=\Pi.
\tag{5.2}
\]

直接得 H|S=L0|S=0。初始时间分量 ∇aF^a_0=−divγE，J0=μ Im(Φ̄Π)，而冻结 Gauss 是 divγE=μ Im(ΦΠ̄)=−J0。因此 (4.1) 的 b=0 行给

\[
\dot L_0=J_0+div_\gamma E=0.
\]

在真实约束数据的依赖域，线性波唯一性给 L0=0，Maxwell 方程恢复。非约束 cutoff 外域不能据此恢复。

### 5.2 应力守恒再恢复 Einstein 规范

本项目符号下，直接应力恒等式为

\[
\nabla^aT^{EM}_{ab}=F_{bc}(J^c-\nabla^cL_0),
\qquad\nabla^aT^{SF}_{ab}=-F_{bc}J^c,
\]
\[
\boxed{\nabla^aT_{ab}=-F_{bc}\nabla^cL_0.}
\tag{5.3}
\]

于是先由 L0=0 得物质应力守恒，再用 Bianchi 传播 H。用协变 H_b=g_bρHρ，

\[
Q_{ab}=\nabla_{(a}H_{b)}-\tfrac12(\partial_\rho g_{ab})H^\rho.
\tag{5.4}
\]

Bianchi 给 ∇a(Qab−gab trQ/2)=−2Fbc∇cL0。左侧主部为 □gHb/2，其余为 H、∇H 的线性项；L0=0 后是齐次线性波系统。

因为 H 在初面恒为零，其空间导数为零。在 (5.2) 的初面坐标，Einstein 缺陷 Eab=Gab−2Tab 满足

\[
E_{00}=-\tfrac12\dot H^0,\quad
E_{0i}=\tfrac12\gamma_{ij}\dot H^j.
\tag{5.5}
\]

Hamiltonian/momentum 约束给 E00=E0i=0，故 nH=0。线性唯一性得 H=0，Einstein 方程恢复，且 C=L0=0。

这补明“L0 → 应力 → H”的三角顺序。线性能量唯一性、实际约束与足够正则性是分析前提；算术程序并不证明它们。本轮也没有重新证明历史特征拼接确实满足约束。

## 6. 有限 H⁶ 的接口核验范围

候选初始化位移局部 H6、速度 H5，γ 下界 ε/2、初始 g00=−1 和 g0i=0。局部双曲系数有有限 Moser 常数。短时令 −g00≥c>0、gij ξiξj≥c|ξ|²，可对空间导数至 5 阶的波能量得到

\[
\frac{d}{dt}E_5^{1/2}
\le C(c^{-1},\|U\|_{H^6},\|\partial_tU\|_{H^5})
(1+E_5^{1/2}).
\tag{6.1}
\]

差方程的最高新项为 (g1⁻¹−g2⁻¹)∂²U2，在 H4 由 H5 的系数差与 H4 的二阶旧场控制，故 H5×H4 差能量可闭合。线性化迭代、正 guard、低一阶收缩和强拓扑逼近是适定性路线，未给新数字寿命，也不由 (6.1) 一条式子宣称完整命名定理已全文核验。

AF 方面 γ−Id~1/R 不能套全空间无权 H6。实际紧核预算与精确 ERN 尾给统一局部 H6 初值界，可以采用局部 cutoff、有限传播和重叠唯一性建立同一初面邻域；不把 cutoff 非约束外域嵌入原物理解。全局发展还需类别闭合、等距重叠和规范拼接。

### 6.1 最关键的正则性关口：H⁶ 场、H⁷ 坐标与规范

只比较两个约化解的同坐标唯一性，不等于几何唯一性。需要协调坐标与 U(1) 规范，且不损失所选解类别。

一条具体适配路线是：在实际 H6 解上，由 Einstein 方程和一阶物质式取得 Ric∈H5、∇Ric∈H4（局部、逐切片）。对 □gX=0，记 P=∇X、W=∇²X。交换导数后为

\[
\square_gP=Ric*P,\quad
\square_gW=Riem*W+Ric*W+\nabla Ric*P.
\tag{6.2}
\]

星号只表示固定有限缩并，本式不声明各个曲率项的精确符号。Riem∈H4、∇Ric∈H4，因而 Hessian 方程在 H5×H4 层的强迫有 H4 预算；配合 H7×H6 的坐标初值，可建立 X 的 H7 能量。这解释本模型为何具备适配潜力，但仍需完成其张量线性能量、初始高阶相容、非特征切片迹及反坐标/拉回的逐项证明。

物理 Lorenz 规范可通过 □gχ=−∇aA^a、χ|S=0、nχ|S=−A(n)|S 构造。朴素估计可能只给 χ∈H6、A+dχ∈H5；不能自动写成 H6 势。可在已协调的 wave 坐标中，用真实 Maxwell 的线性势方程及 H6 初值，再以较低正则唯一性比较来恢复 H6 势，随后由 dχ 的 H6 正则恢复 χ∈H7。**本轮登记这条明确的提升路线，不把其全部类别兼容性和全局规范拼接标为已认证。**

### 6.2 原始来源对照与未适配项

| 原始来源 | 实际核查到的内容 | 本项目可用范围 / 缺口 |
|---|---|---|
| HKM (1977)，Caltech 作者记录 | 一般拟线性局部理论的摘要；作者旧 PDF 地址读取失败，记录是 metadata-only | 阶数门槛足够；Theorem III 的完整假设尚未逐项全文核验 |
| Kommemi，arXiv:1107.0949，§1.1.4 | 表述光滑 charged-EMKG 的唯一光滑最大未来发展 | 不能替代本项目有限 H6 的双向 MGHD 接口 |
| Chruściel，arXiv:1112.5779v2，§3.1 | 列出 H1/H2、A0–A3 的发展接口；正式主定理以真空为对象 | 可作核验结构；需替换为全部带电场、协调 gauge，并验证 H7 坐标/拉回 |
| Parlongue，arXiv:1109.0644，§2 | 在 s-admissibility 下给非真空几何唯一性；包含固定背景 matter 的存在/有限传播与式(7)稳定要求 | 是候选适配工具；charged potential 的 admissibility 与规范匹配尚未核完 |
| Wong，arXiv:1310.1318v3，Def.18 / Thm.21 / Remark10 | 最大构造要求存在、唯一性、唯一延拓、局部拼接；低正则类别需兼容 | 不会自动提供本模型局部理论；Hausdorff 与 Sobolev/gauge 拼接仍需验收 |
| Kauffman–Lindblad，arXiv:2109.03270，Thm.1.5 | 光滑小 AF 数据的耦合系统全局稳定性 | 本候选预算巨大，不符合其小数据用途 |

详细定位与访问状态见 SOURCE_AUDIT.md。没有把真空、平直 MKG、光滑发展、摘要或标题当作本项目的完整有限 H6 认证。

## 7. 共同域嵌入：先建立域，再使用环境流

负 U 实际条带和旧人工域 N 已存在。旧 N 的下边 U>σa(t)−a/16 可能不容纳整个 ψ 同伦。先在同一坐标、同一实际场的重叠上形成

\[
\widehat N=N\cup\mathcal D,\quad
\mathcal D=(-a/8,0)\times(t_0,t_R)\times S^2,
\quad M_G=int\,D_{\widehat N}(S_{old}).
\tag{7.1}
\]

实际条带存在与全域 S_old 的闭、无边缘、acausal 性是冻结输入/前轮几何证明。仅对 M_G 调用发展嵌入接口，不能称整个 Nhat 为 MGHD。

复核 D⊂MG 的一个明确补充：对因果曲线，U、t 在未来不减，

\[
|\dot\omega|^2\le \Omega^2r^{-2}\dot U\dot t
\le 2\cdot128^2\dot U\dot t.
\]

任意尾段的球面长度满足

\[
\operatorname{length}(\omega)
\le256\sqrt{|\Delta U||\Delta t|}.
\tag{7.2}
\]

因此若 U、t 收敛，角变量也是 Cauchy，不会以无限角振荡躲避矩形穿越。对 F_a=U−σa(t)>0 的点，过去不交图而离开矩形只能遇 U=−a/8 或 t=t0，在该出口 F_a<0；F_a<0 的点向未来同理遇 F_a>0。若尾段留在内部，其坐标极限可延长；若极限到图，图亦是实际内部点。故每条相关不可延曲线必交 S_old，D 属于其共同依赖域内部。

在**有限正则发展嵌入接口成立时**取得固定 j:MG→Ma，才把 D 的紧走廊视为 Ma 中的实际区域。随后定义前轮外侧环境流

\[
W_\tau=\Delta\sigma(t)
\chi((U-\sigma_\tau(t))/m_o)\partial_U,
\quad m_o=a/2^{15},
\quad\Delta\sigma=\sigma_0^{new}-\sigma_a.
\tag{7.3}
\]

支撑在 t∈(1/4,1/2)，图距 U 两边至少 a/8192、a/4096；mo 小于两余量。固定紧支撑流 hτ 把 Sa 送到 S−,τ，中心和尾不动；spacelike 由冻结共同界给出。没有使用“候选先在 Ma 中”来证明其走廊先在 Ma 中，逻辑顺序没有这一循环。

## 8. 重切片最大性转移：本轮新增引理

### 8.1 几何前提

采用一个固定、对开域限制和所需兼容坐标/规范变换闭合的解类别 C。设 Ma 为原数据的双向 MGHD，S 为其 Cauchy 面。hθ 为固定紧集之外恒等的环境微分同胚族，h0=id，各 Sθ=hθ(S) 连通、spacelike；原/端点数据以及所用映射均属 C 的允许正则类别。

前轮紧支撑变形引理给所有 Sθ 是 Ma 的 Cauchy 面。其理由是：用以 S 为零面的 Cauchy temporal 函数 T，取 |T|>C 的两个连通 level，避开紧支撑和所有 Sθ。它们处于 Sθ 的两侧；每条不可延因果曲线从过去侧走到未来侧。连通 spacelike 面的未来穿越方向相同，故不可能重复穿越。这是全局 Cauchy 论证，不以局部类空性单独代替。

### 8.2 最大性转移证明

由 S1 的 Cauchy 性，Ma 是 S1 数据的发展。若存在将 Ma 嵌入另一个 S1-Cauchy 发展 N 的开放保未来等距嵌入 f，考察 f 推送的紧支撑环境流。因支撑紧且位于开放 f(Ma) 内，它可以在 N 外部延为恒等。所有像 f(Sθ) 仍连通、spacelike。

N 中 f(S1) 是 Cauchy 面。对反向环境族应用同一变形引理，f(S) 也成为 N 的 Cauchy 面。场按 f 等距/U(1) 识别，因此 N 同时是原 S 数据的发展，而 f 是原数据的 Cauchy 扩展。原 Ma 的最大性禁止其为真扩展，所以 f 必须满射。

\[
\boxed{\text{紧支撑 spacelike 重切片不改变双向 MGHD 的最大性，}
\text{前提是发展/映射处于同一允许类别。}}
\tag{8.1}
\]

若候选数据的 Mb 存在且具有共同发展到 MGHD 的嵌入性质，Ma→Mb 是这样的 f，故为满等距识别，并满足 (3.1)。这补上了“嵌入候选面”与“重新演化的最大发展相同”之间的缺环。定理没有以新 ψ 的定义就假设 Mb=Ma，也没有把 h1 当作等距映射。

### 8.3 原面、前移面与候选面之间的应用

原 Ma 的最大性最初针对 S_old。不能仅因 Sa 在 Ma 中是 Cauchy 面就不加说明地把最大性改标到 Sa。

近中心原前移图为 s=f(R)，可用内侧路径 s=θf(R)，0≤θ≤1。令 q 为前轮的斜率上界，γmargin=1−q，α=γmargin/2，δg<ε/4096，γmargin>ε。则

\[
g^{-1}(d(s-\theta f),d(s-\theta f))
\le-1+\theta^2q^2+16\delta_g<-\alpha,
\]
\[
\gamma_\theta\ge(1-\theta^2q^2-8\delta_g)Id\ge\alpha Id.
\tag{8.2}
\]

所有内图在实际 C 内，因为 θf+R≤f+R≤b<r0+ε/2。取 mc=ε/128，在该图附近用 f(R)χ((s−θf)/mc)∂s 得固定紧支撑环境流；人工锥余量至少 ε/8−ε/128=15ε/128。图导数乘 θ 不增，原高阶非特征迹路线可沿这族使用，所需类别相容仍列入待核接口。

第一段从 S_old 到 Sa 用内侧流，第二段从 Sa 到 Sb 用 (7.3) 外侧流。内侧 r<1/4，外侧 r≥ρ>1/4，支撑分离。两段合成紧支撑 spacelike 环境路径。因此 (8.1) 连续转移原最大性到 Sa、Sb。**在同一实际发展及兼容有限正则类别前提成立时，Mb 与 Ma 是同一最大物理解。**

本文比较双向 MGHD；若只取某张切片的最大未来发展，两者对应 Ma 内不同的未来子域，不能声称这两个未来子域逐点相同。Kommemi 的“最大未来发展”与本节双向对象须区分。

## 9. 升级为无条件认证的验收清单

| 编号 | 需完成的数学证据 | 本轮状态 |
|---|---|---|
| U1 | 同一根的实际条带、中心约束域、C8 相容、RN 重叠等历史存在输入 | 已冻结身份；未重新认证全部历史解析输入 |
| U2 | 候选的增强 H6 迹与规范预算，及其使用的 B6/Sobolev 乘积常数 | 已冻结完整条件证据；历史迹/场前提仍继承 |
| U3 | 明确解类别 C、H6 场与 H7 坐标/规范，局部存在与恢复约束 | 主符号/传播已展开；完整能量、trace/拉回及规范提升需验收 |
| U4 | 模型专属几何唯一性、唯一延拓、非紧初面局部拼接，MGHD 的 Hausdorff/Sobolev/U(1) 重叠相容 | 来源假设已逐项列出；未全部认证 |
| U5 | 从共同 MG 到原 Ma 的非循环嵌入，以及重切片最大性转移 | 本轮给条件性证明；依 U1–U4 和原 Cauchy 输入 |

Pa 数字化、ψa=ψ₀、一般 H6 Lipschitz 数字常数、任意扰动数据统一寿命，都不是这个固定候选同一发展识别的必要条件。它们有其他用途，不能把非必要项当作本轮唯一卡点。

精确 Minkowski 开帽、C∞ 接合和 G05 是原更大目标的独立条件，不由本轮有限正则识别推出，也不混入本轮固定候选接口的必要清单。

## 10. 本轮进度报告

- **本轮完成项**：候选端点全部证据、坐标和条件状态按字节冻结；展开 EMCSF 对角波主部和 L0→应力→H 的约束传播；复核共同域嵌入顺序并补角变量收敛证据；补紧支撑重切片的最大性转移，明确 Ma 与 Mb 的条件识别；完成源文逐假设对照、自审及精确复算。
- **剩余项**：实际场/高阶迹等历史前提的完整认证；有限正则局部理论、H7 坐标与 gauge 提升、非紧初面和全局规范/发展拼接的验收。
- **卡点**：当前不能由已查到的光滑、真空、摘要或条件性抽象定理直接认证本项目全部有限 H6 接口。Pa 数字缺失仍在，但不是候选升级的必要障碍。
- **下一步**：以 §6.1 为依据，完成“兼容非特征切片的 H6/H7 坐标迹与拉回”及“Lorenz 势正则提升和 U(1) 重叠拼接”两条模型专属引理，再对 U3/U4 做最终验收；其前 ψ₀ 保持条件固定。

**所有数学结论：GPT 主张，未经外部独立审查。**


---

# 阶段 3.13 自审

**所有数学结论：GPT 主张，未经外部独立审查。** 这是同一 GPT 工作流的内部复核，不是第三方审查。

## 1. 本轮修补与保留

| 检查点 | 处理及结果 |
|---|---|
| 端点定义是否漂移 | 前轮证据包按字节冻结；ENDPOINT.json 对 member、candidate、selection、path 与前轮 STATUS 做精确相等检查 |
| 六阶范数是否混用标签 | B0u 只在固定 y 标签；全局 areal x 的零阶下界是 ε/8，未声明相同六阶预算 |
| 同伦端点是否混淆 | τ=0 为 ψa，τ=1 为 ψ₀；“ψ₀”下标不是同伦参数 |
| 是否把环境流当作等距映射 | 明确 hτ 只移图；实际识别 I 由发展唯一性与最大性取得 |
| Cauchy 面是否足够说明重新演化相同 | 增加紧支撑重切片最大性转移；在扩展中反推旧面仍 Cauchy，然后用原最大性 |
| 是否循环使用候选已经嵌入原发展 | 先建立共同 MG 的依赖域、取得固定嵌入，再构造走廊环境流 |
| 双空矩形穿越是否漏角变量 | 加球面长度尾估计；U、t 的极限同时控制角变量 Cauchy 性 |
| Lorenz 与坐标 gauge 是否混用 | 区分 L0 与 C=L0−H·A；完整 KG 保留，先传播 L0 再传播 H |
| Gauss 与电流符号 | E_i=F(n,e_i)，J0=μ Im(Φ̄Π)，divE=−J0；故 dotL0=0 |
| 初始 harmonic 符号 | dotgij=−2K、dotg00=2trK；非对角 γ 的四组有理初始化复算 H=0 |
| 应力因子 | G=2T、Ric=S；Bianchi 缺陷强迫为 −2F dL0，未丢因子 2 |
| 正则性是否失一阶 | 朴素 χ 的 H6 不足以保持 A 的 H6；把势方程恢复及 χ 的 H7 提升明确列为路线缺口 |
| 是否冒用来源 | 光滑、真空、小数据结果、作者摘要与条件性抽象理论各自限制登记，未当作全模型认证 |
| Pa 是否是升级必要卡点 | 不是固定候选识别的必要项；仍限制原路径常数数字化，单独记录 |
| 是否误认未来子域 | 比较双向 MGHD；不同切片的最大未来发展可以是同一时空的不同未来子域 |

## 2. 最大性转移的逐项前提

1. 原 Ma 是 S_old 数据的双向 MGHD；不是只知道某个局部解。
2. 内侧、外侧图在同一实际 Ma 中；这依赖实际中心域、实际负 U 条带及共同 MG 的嵌入接口。
3. 环境族固定紧支撑、各图 spacelike、连通，且嵌入/逆流正则性属于同一允许类别 C。
4. 候选 Mb 是真实候选数据的 MGHD，允许将任一候选 Cauchy 发展嵌入 Mb。
5. f:Ma→Mb 的推送流支撑紧且位于开放 f(Ma) 内，才可在外部延为恒等。
6. 反向族在 Mb 中保持 spacelike；其起点 f(Sb) 是 Cauchy 面，遂得 f(S_old) 也是 Cauchy 面。
7. 这时 Mb 才是原数据的 Cauchy 扩展；原最大性才推出 f 满射。

以上为条件性解析证明链；脚本只检查其依赖图无环，未证明七条前提。

## 3. Cauchy 保持的补充证明检查

在 globally hyperbolic N 中选完整时间样向量场，将 N 写为时间流线乘原 Cauchy 面。紧支撑变形面 Sθ 到原面的时间流线投影是局部微分同胚：其核只能沿时间样方向，而 Sθ 是 spacelike。投影在紧集之外沿用原面，故是 proper；像既开又闭，从而满射。

proper 局部微分同胚是有限覆盖。选紧支撑之外一点，其时间流线完全避开紧支撑，只有一个原面交点，所以覆盖度是 1。Sθ 因此是全局时间流线图，处于两个 Cauchy temporal level 之间。每条不可延因果曲线必从过去侧到未来侧；spacelike 图的穿越方向统一，交点恰一。这里使用原面连通、非紧且同胚 R³，以及适用正则性下的 globally hyperbolic 时间流结构。

此补充避免仅凭“局部类空”宣称全局 Cauchy。它仍依赖类别 C 中允许的时间流/图正则性，没有代替 U3/U4。

## 4. 冻结证据的边界

INPUT_LOCK 锁定 28 个文件：前轮证明包、端点表达式、两个历史接口文本。它锁定字节身份，不能认证那些文字的解析前提已经成立。根摘要不是实际场的全空间数值证书；冻结的 C8 场、约束、拼接和高阶迹仍继承原项目状态。

以前 STATUS 中更大目标的 gaps 保持在冻结副本中。本轮 STATUS 另分 fixed_candidate_required_gaps 与 other_project_open_items；这属于必要性分析的澄清，不是把历史缺口删除或悄悄关闭。

## 5. 精确计算的边界

Maxwell 混合主部与 Q 的 first-jet 系数以形式多项式精确消零。Einstein 主部只在三组点度量上检查 100 个独立二阶 jet 基；这些检查排错有用，但不是对所有度量的一般计算机证明。一般主部身份在 PROOF 中作为解析推导主张登记。

初值 gauge、应力 trace reversal、规范相位与有理余量通过精确算术；程序不证明线性波唯一性、H6 局部存在、几何唯一性、非特征迹、全局拼接、实际约束或外部独立认证。

**自审结论：条件识别路线已补明，ψ₀ 条件固定不升级；U1–U4 的实质性接口仍需验收。GPT 主张，未经外部独立审查。**


---

# 阶段 3.13 原始来源核验

**数学适用性判断：GPT 主张，未经外部独立审查。** 访问与正文定位是来源记录；从来源到本模型的适配是本文的推断，未宣称原作者认证本项目。日期：2026-10-12（项目文件日期沿用前轮）。未复制文献全文。

| 来源 | 本轮可核对位置 / 获取状态 | 实际边界与采用方式 |
|---|---|---|
| Hughes–Kato–Marsden (1977), *Well-posed quasi-linear second-order hyperbolic systems...* | [Caltech 作者记录](https://authors.library.caltech.edu/records/yqzjw-rqj49)，摘要及 metadata-only 说明；旧作者 PDF 地址返回 502 | 摘要支持一般拟线性局部理论背景；不声称已全文核完 Theorem III 的全部假设。本轮直接展开模型主符号，完整适定性验收仍保留 |
| Kommemi, arXiv:1107.0949 | [PDF](https://arxiv.org/pdf/1107.0949)，§1.1.4，PDF 第 5 页 | 来源明确使用 smooth 数据与唯一 smooth maximal future development。仅支持光滑带电模型背景，不能直接替代有限 H6 双向发展 |
| Chruściel, arXiv:1112.5779v2 | [PDF](https://arxiv.org/pdf/1112.5779)，Thm.1.1；§3.1 PDF 第 11–12 页；§3.2 第 19–21 页；Appendix B | 主定理是真空；§3.1 的 H1/H2、A0–A3 用作接口清单。H7 坐标波、H6 拉回和 isometry 正则性需在本带电系统及 gauge 中验收 |
| Parlongue, arXiv:1109.0644 | [PDF](https://arxiv.org/pdf/1109.0644)，§2 第 3–4 页，式(7)、Thm.2.0.3；§3 坐标导数论证 | 几何唯一性以 s-admissibility 为前提，要求固定背景 matter 的适定性/传播与稳定性。charged potential 的全部适配未完成；标量/Maxwell 的个别例子不等于自动覆盖耦合规范系统 |
| Wong, arXiv:1310.1318v3 | [作者 HTML](https://arxiv.org/html/1310.1318v3)，Def.18、Thm.21、Remark10 | 抽象最大构造要求存在、唯一性、唯一延拓、局部性。Sobolev 类别与重叠闭合需另外验证；未从抽象框架凭空取得本模型局部定理 |
| Kauffman–Lindblad, arXiv:2109.03270 | [PDF](https://arxiv.org/pdf/2109.03270)，Thm.1.5 | 光滑小 AF 初值的全局稳定性；本项目巨大预算不符合该小数据用途，不用于关闭固定候选接口 |
| Huneau 作者讲义 | [PDF](https://huneau.perso.math.cnrs.fr/cours.pdf)，Thm.4.3.4、5.1.1 | 变量系数线性定理的较强系数要求、半线性示例不能不加适配地当作完整 H6 拟线性系统证明；本轮仅作排除性检查 |

## 对照接口的可审查要求

- **H1/H2**：本项目全部 16 个实场分量的局部约化存在、同 wave 坐标/初值唯一性和有限传播；PROOF §4–5 的规范恢复需配线性能量唯一性。
- **A0/A1**：固定初面的等距自同构唯一性与 H7 的兼容映射；还须同步 U(1) 场识别。
- **A2/A3**：坐标波在 H7 的非特征初值和 trace、逆映射与 H6 拉回；不能只写一个粗波能量式。
- **Matter admissibility**：固定 H6 背景下的 charged Maxwell–scalar（含规范）的适定性、局部性与稳定性；不以平直 MKG 冒充动态 g。
- **Globality**：Hausdorff 的重叠拼接、Sobolev 类别闭合与规范 cocycle；局部几何唯一性本身不足以认证所有全局步骤。

本轮来源判断仅给出认证路线及适用限制；详细模型推导属于 PROOF 的 GPT 主张。没有依据文献标题、摘要或高阶数就把 ψ₀ 升级为无条件认证。


---

# 精确复算记录：阶段 3.13

**所有数学结论：GPT 主张，未经外部独立审查。** 环境 Python 3.12.14；仅标准库 Fraction 与附带形式多项式引擎。无浮点大指数实例化，无外部 CAS，未使用采样图替代证明。

## 结果

本轮 **433 项全部通过**；前轮 **116 项全部通过**并与冻结结果 JSON 精确相等。两组共 549 项，其中包括证据身份和依赖顺序检查，不能统称 549 个数学定理。

| 检查组 | 项数 | 范围 |
|---|---:|---|
| 冻结 SHA256 | 28 | 前轮证据及两份接口文本的字节身份 |
| 端点对象与前轮一致 | 4 | member、candidate、selection、path |
| 状态/根身份 | 3 | 条件固定、ψa 身份未认证、根摘要 |
| Maxwell 混合二阶消项 | 4 | 四个输出分量，符号系数精确为零 |
| 点度量逆与时间 guard | 6 | 三组非对角有理 Lorentz 度量 |
| Einstein 主部 | 300 | 每组点度量的 100 个独立二阶 metric-jet 基；每基检查全部 10 个输出 |
| harmonic/L0/约束初始符号 | 16 | 四组非对角 γ 的精确初始化 |
| Q 协变化 first-jet 系数 | 40 | 10 个对称 (a,b)，4 个收缩方向 |
| 应力 trace/source、Gauss、U(1)、电流共轭 | 5 | 形式代数消项；不证明 PDE 守恒本身 |
| 角长度与走廊余量、内图恒等式 | 8 | 有理安全因子及全 θ 形式身份 |
| 无环依赖顺序 | 19 | 条件接口逻辑链；不证明根前提 |
| **本轮合计** | **433** | 全部 passed |

前轮基线包括候选七阶 bump 预算、归一化下界、共同 d/J 界、类空/带权预算余量等 116 项；完整结果保留于 frozen/stage312/verification/RESULTS.json，本轮复跑记录见 verification/BASELINE_RECHECK.json。

## 重现

在解压后的包根目录运行：

```bash
python3 -B code/check_interface.py
python3 -B frozen/stage312/code/check_bounds.py
```

第二条会在冻结副本的 verification 写回确定性结果；原本的 SHA256 锁保留。若代码、输入或输出格式改变，首先核对 INPUT_LOCK；不要静默更新锁来掩盖变化。

本轮新结果与依赖图位于 verification/RESULTS.json、verification/DEPENDENCIES.json。MANIFEST.json 保存交付包内各文件散列，自身不自引用；ZIP 完整性另以打包后 CRC/成员字节验证。

## 解析与算术的边界

全度量的一般 Einstein 主符号仍是解析推导主张；三组有理点核验只检查系数实现。PDE 局部理论、几何唯一性、实际约束场、全局 Cauchy/最大性和 gauge 拼接均未由程序证明。所有对应状态保持 conditional / open，无外部独立审查。


---

# 冻结端点表达式与身份

**所有数学结论：GPT 主张，未经外部独立审查。** 完整基线材料见 ZIP 内 frozen/stage312；本表以字符串保存超大预算，禁止用浮点截断冒充实例。

| 名称 | 冻结表达式 |
|---|---|
| L | `2^2104156*1048578` |
| H | `2^100*exp(200*(L+4))` |
| a | `exp(-8*H)` |
| epsilon | `exp(-exp(300*H))` |
| D8 | `exp(exp(102*H))` |
| N7 | `exp(exp(200*H))` |
| kappa_AF | `exp(-8*H-2*L)/64` |
| P_psi0 | `<2^247` |
| Ib | `>1/1296` |
| B6u | `2^(34008+2^41)*(1+N7)*epsilon^(-15)` |
| B0u | `2+2^2056*epsilon^(-8)*(1+2^31*N7+2^8*B6u)^12+2^120*kappa_AF^(-8)+2^2301` |
| Pbar | `max(Pa,2^247)` |
| Dbar | `exp(100*H)+(a/8)*Pbar` |
| dstar | `a^2/2^20` |
| Jstar | `a^2*exp(-2*L)/2^21` |
| cpath | `min(1,alpha,a^2/(2^25*exp(2*H)*Dbar^2))` |
| Mbar | `D8*exp(200*H)*(1+Pbar)` |
| Cpath | `(2^2001*Mbar)^(16^201)` |
| B6 | `2^(34000+2^41)*(1+N7)*alpha^(-8)*epsilon^(-7)` |
| Bc | `2^30*Cpath+2^8*B6` |
| Bg | `2^2048*alpha^(-8)*(1+Bc)^12` |
| Bpath | `2+Bg+2^120*kappa_AF^(-8)+2^2301` |

```json
{
  "member": {
    "mu": "3/5",
    "m_geom": "2^2104156",
    "ADM_mass": 1,
    "charge": 1,
    "root_sha256": "7845f2276b7dc12669d9e27861704bdee99f395458c35647fc9c734f93fb6dc2"
  },
  "candidate": {
    "P_bound": "<2^247",
    "ellipticity_frozen_labels": "epsilon*/2",
    "ellipticity_global_areal": "epsilon*/8",
    "strong_budget_frozen_labels": "B0u, PROOF (8.2)",
    "same_numeric_H6_budget_in_global_areal_claimed": false,
    "status": "conditional on inherited field, central graph, extraction, Cauchy/MGHD interfaces"
  },
  "selection": {
    "conditional_actual_fixed_slice": true,
    "unconditional_certification": false,
    "original_psi_identity_with_candidate_certified": false,
    "tau_0": "original psi_a",
    "tau_1": "candidate psi_0"
  },
  "coordinate_labels": {
    "y": "center harmonic Cartesian, outside areal Cartesian, fixed ring join",
    "x": "globally areal; ellipticity epsilon/8; B0u H6 not certified"
  }
}
```

**所有数学结论：GPT 主张，未经外部独立审查。**
