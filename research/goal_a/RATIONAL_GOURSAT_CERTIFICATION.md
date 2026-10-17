# A-GOUR01：有限因果域的有理输运与逐单元误差管道

2026-10-16。**内部分析命题；实际候选的连续 PDE 证书尚未取得，目标 A 仍开放。** 本文把 [A-SCREEN01](NEUTRAL_CAUSAL_SCREEN.md) 的误差需求细化为可逐项核验的局部不等式，不将浮点预测当作已满足的前提。

## 1. 不在出射零膨胀处退化的变量

在 D001 的中性实标量区域，取 r>0、ν=r_u<0、Ω²>0，并定义

\[
\kappa=-\frac{\Omega^2}{4\nu}>0,\quad
\theta=r\phi_v,\quad z=\frac{r\phi_u}{\nu},\quad
f=1-\frac{2m}{r},\quad\lambda=\kappa f.
\tag{G1}
\]

按 X=(r,κ,θ,ν,z,m) 排列，前3个分量沿 u、后3个沿 v 满足

\[
\begin{array}{lll}
r_u=\nu,&\kappa_u=\kappa\nu z^2/r,&
\theta_u=-\kappa f\nu z/r,\\
\nu_v=2\kappa m\nu/r^2,&
z_v=-\theta/r-2\kappa mz/r^2,&
m_v=\theta^2/(2\kappa).
\end{array}
\tag{G2}
\]

右端 F(X) 全为有理函数，分母只有 r、κ；没有 λ、f 或 m 的分母。故 λ=0 不引入这个系统的系数奇点。ν保持负号是当前图和变量的前提，不是已经证明的全未来性质。

### 约束与原双零系统的等价接口

对 (G2) 的光滑解，定义尚未预设为零的缺陷

\[
E=r_v-\kappa f,\qquad G=m_u-\tfrac12f\nu z^2.
\]

直接求导，**不先使用** E=G=0，得到

\[
E_u=2\kappa G/r,\qquad G_v=-m\nu z^2E/r^2.
\tag{G3}
\]

若初始边 u=0 上 E=0、入射边 v=Vcap 上 G=0，则它们的齐次 Volterra 积分系统在任一系数有界的有限矩形上唯一为零。可用足够小子矩形上的 sup 范数压缩并有限拼接证明，不需要陷俘遮蔽、无穷远或全未来假设。

令 ζ=νz。(G2) 给 ζ_v=−νθ/r、θ_u=−λζ/r，所以 ζ/r 与 θ/r 的交叉导数相等；固定角点 φ后可重建 φ_u=ζ/r、φ_v=θ/r。取 Ω²=−4κν：

\[
r_{uv}=2\kappa m\nu/r^2=-\Omega^2m/(2r^2),\qquad
S_{uv}=-2\phi_u\phi_v+\Omega^2m/r^3,
\quad S=\log\Omega^2.
\tag{G4}
\]

其中第二式由
S_u=νz²/r+ν_u/ν、(ν_u/ν)_v=(ν_v/ν)_u 展开得到。u-Raychaudhuri 直接由 κ_u 恢复；v-Raychaudhuri 由 m_v、质量恒等式与 ν≠0恢复。因此满足上述边界约束的 (G2) 解确实恢复 [A-EVOL03](NEUTRAL_CHARACTERISTIC_METHOD.md) 的中性 Einstein–scalar 方程，而非任意六变量模型。

本次输入的初始锥 S=0、r″=−r(φ′)²，中心帽 Vcap=2rcap。其边界满足

\[
\nu_0(v)=-v/(4r_0(v)),\quad\kappa_0(v)=r_0(v)/v,\quad
m_0(v)=(r_0-vr'_0)/2,\quad\theta_0=r_0\phi'_0.
\tag{G5}
\]

这些式子与 (G2) 的 v 向方程相容；z₀从0沿其线性 v 方程积分。另一条精确真空边为
r=rcap−u/2、κ=1/2、θ=z=m=0、ν=−1/2，故 (G3) 的两个边界条件成立。**数值 ODE 并未自动认证这些精确函数与近似边界间的误差。**

## 2. 逐单元后验存在与误差命题

设矩形 K=[a,a+hᵤ]×[b,b+hᵥ]，hᵤ,hᵥ>0；前3个分量给定左边 u=a 的连续入流值，后3个给定下边 v=b 的连续入流值。取连续、分片 C¹ 的近似 X̄，在该单元内逐方向定义残差

\[
R_i=\partial_{d_i}\bar X_i-F_i(\bar X),\qquad
d_i=u\ (i\le3),\quad d_i=v\ (i\ge4).
\]

假设已**实际证明**以下有限数据：

- 近似在全单元的逐分量值域盒 B；正向半径向量 M_i>0；B+[-M,M] 满足 r>0、κ>0、ν<0。
- 全单元 |R_i|≤δ_i，δ_i≥0；相应整条入流边的误差 ≤b_i，b_i≥0。
- 在凸盒 B+[-M,M] 上 |∂ⱼF_i|≤Lᵢⱼ，Lᵢⱼ≥0。
- 令 h_i=hᵤ 或 hᵥ 与输运方向一致，严格不等式

\[
\boxed{\quad b_i+h_i\big(\delta_i+\sum_jL_{ij}M_j\big)<M_i
\quad (i=1,\ldots,6).\quad}
\tag{G6}
\]

则该单元存在唯一的连续输运解 X，且 |X_i−X̄_i|<M_i；入流数据和 F光滑时具有相应光滑性。对有共同边的有限单元网格，可把前一单元的**整条边**误差作为后一个的 b_i，递推获得全矩形解与同样的误差覆盖。

### 证明

对 w=X−X̄，将各自方向的方程积分成

\[
(Tw)_i=e_i^{in}+\int\big[F_i(\bar X+w)-F_i(\bar X)-R_i\big]ds.
\tag{G7}
\]

在闭球 ||w||_M=maxᵢ sup|w_i|/M_i≤1 中，均值定理和前提给 |(Tw)_i|≤b_i+h_i(δ_i+ΣLᵢⱼM_j)<M_i。该球映入自身内部；同一估计给 Lipschitz 常数

\[
q=\max_i\frac{h_i\sum_jL_{ij}M_j}{M_i}<1.
\]

于是 Banach 不动点定理给唯一解。闭球位于分母有正下界的盒中，故 F及导数有界，没有在该单元证明之外假设延续存在。光滑入流数据的横向差商满足相应线性积分方程；以同样局部压缩、逐阶求导取得所需正则性。

沿网格递推时，相邻单元同一入流分量直接相同，其余分量在共同边满足相同的一维输运 ODE，并有同一角点值，由 ODE唯一性相同；因此所有分量在共同边匹配。有限拼接得到矩形解。若边界还满足第1节的约束条件，(G3) 恢复 Einstein解。证毕。

该命题的“唯一”首先指误差球内唯一；同一有界正分母区域中的其他局部解也由局部 Lipschitz 唯一性与延续一致。它不证明中心、AF端或矩形外的未来。

## 3. 有限代数如何提供残差上界

若 X̄逐单元是双变量多项式，则残差分子依次为

\[
\begin{array}{l}
N_r=\bar r_u-\bar\nu,\\
N_\kappa=\bar r\bar\kappa_u-\bar\kappa\bar\nu\bar z^2,\\
N_\theta=\bar r^2\bar\theta_u+
 \bar\kappa\bar\nu\bar z(\bar r-2\bar m),\\
N_\nu=\bar r^2\bar\nu_v-2\bar\kappa\bar m\bar\nu,\\
N_z=\bar r^2\bar z_v+\bar\theta\bar r+2\bar\kappa\bar m\bar z,\\
N_m=2\bar\kappa\bar m_v-\bar\theta^2.
\end{array}
\tag{G8}
\]

分别除以 1、r、r²、r²、r²、2κ。这避免先对近似导数与非线性源各自取宽区间而丢失抵消。若多项式转换为单位单元上的张量 Bernstein 形式，基函数非负且和为1，所以其值域包含在系数的最小值与最大值之间；从而给显式 δ。Jacobian 同样是有理函数，可在 B+[-M,M] 用有理区间运算取 L。

完整计算机辅助证明还必须：用有理网格与共享节点/导数精确重建 Hermite多项式，验证全域与边界的上界，再以向外舍入核验 (G6)。**把各单元浮点系数直接当作互相连续的精确多项式不够**：独立舍入可能破坏共同边的精确匹配。应从共享的精确二进制节点值和导数重建，或另证跳跃误差并修改定理。

## 4. 本次实际实现和证据等级

[neutral_transport.py](neutral_transport.py) 给 (G2)、显式 Jacobian及独立矩形梯形求积；[verify_neutral_transport.py](verify_neutral_transport.py) 用已有有理 Laurent 代数核对 (G3)、标量可积性、质量恒等式和混合 Einstein式，拒绝两个错误波输运版本，并比较精确收缩 FLRW。它还核查一个有限有理 (G6) 核及错误输入拒绝；**这个核不验证调用方提供的 δ、L、b。**

[transport_defect.py](transport_defect.py) 构造双三次 Hermite近似，在形成 (G8) 后用 Bernstein系数估算残差，并预测逐单元半径。所有 NumPy系数和上界均为普通浮点，**未向外舍入**；边界误差是明确标注的假定值。因此即使预测管道覆盖全域，也不产生实际连续解证书。

主实验仍冻结 A-SCREEN01 的 β=0.003 C0早段尺度与 ε=0.05的已分辨开启实验，在 (u*,v*)=(Vend/2,31Vend/32) 比较。192²、384² 的预测管道可以覆盖整个矩形；在假定极小边界误差下，端点各分量半径量级分别为
(0.013,0.026,0.060,0.054,0.116,0.060) 与
(0.0029,0.0049,0.0114,0.0106,0.0234,0.0114)。这些是认证可行性预测，**不是已证误差**。48²、96²的预测失败也保留；不把预测失败当物理奇点。

初始实现若每格将整个输入半径乘1.08，会产生与网格格数有关的假指数放大；已改为仅对本格新增量加余量。预测代码仍须经独立核对，不能因经验半径下降就假定其严格有效。

另有 [rational_transport_cell.py](rational_transport_cell.py) 实现**真正的单元级有理检查核**：从共享节点精确重建 Hermite多项式，以 Fraction精确取 Bernstein残差，以既有192位向外舍入有理区间核取 Jacobian，再精确核对 (G6)。在192²强场近似的最后一个单元，取 Mᵢ=1/50、**假定**整条入流边误差 bᵢ≤1/100，六个严格余量均约0.00886以上；检查还验证了相邻单元共享边的精确 C1匹配，拒绝过大的边界误差。这个单元证明确实使用精确运算，但其入流误差仍未获前置单元的证明，所以**不是实际候选的局部或全域陷俘证书**。

## 5. 下一项可兑现的证明义务

    python research/goal_a/verify_neutral_transport.py
    python -O research/goal_a/verify_neutral_transport.py
    python research/goal_a/explore_transport_tube.py
    python research/goal_a/verify_rational_transport_cell.py
    python -O research/goal_a/verify_rational_transport_cell.py

精确代数和已知解比较见 [检查报告](NEUTRAL_TRANSPORT_CHECKS_2026-10-16.json)，实际候选与失败预测见 [管道预测](TRANSPORT_TUBE_FORECAST_2026-10-16.json)，带未证入流前提的单元核见 [有理检查报告](RATIONAL_TRANSPORT_CELL_CHECKS_2026-10-16.json)。当前未解决的关键输入是：

1. 原光滑开启函数及 Raychaudhuri/横向边界 ODE的严格误差，特别是 θ的整边误差；不能把任意假定的10⁻¹⁰写成实测上界。
2. 共享 Hermite多项式的精确重建、所有单元的向外舍入 Bernstein/Jacobian包络，以及严格 (G6) 核查。
3. 若有限域证书取得，仍要转移到 A-JET01 的实际正 β、正 η光滑根族及相容 AF Cauchy实现，才能用 L001 作临界基点排除。

这一局部认证路线不取代最终验收。完整色散侧、正质量极端真正形成、附近带电亚极端终态及固定 X6曲线均仍需另证。
