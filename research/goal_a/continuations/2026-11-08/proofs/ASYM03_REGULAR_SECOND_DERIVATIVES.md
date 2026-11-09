# ASYM03：二阶径向标量有界与沿线规则几何二阶相容性

2026-11-08。解析证明稿 / INTERNAL_AUDIT，未经独立同行评议。固定 ASYM01 的同一射线数据，不再调参数。结论是这些数据的必要横向 jets 存在且满足下列极限；**仍未证明实际共同宽度邻域、事件视界或 A4 半条带收敛**。

## 1. 规范、变量及径向约束

在任何实现这些数据的有限规则邻域中，用入射坐标写
\[
g=-A\,dv²+2B\,dv\,dr+r²d\omega²,\quad
\mathcal L=\partial_v+\lambda\partial_r,\quad \lambda=A/(2B),\quad B>0.
\]
Γ 沿 v=s 参数化，rΓ'=λΓ，t=1+s。取沿 Γ 的电磁规范 A_𝓛=0。将电势与度量系数 A 区分；以下 D 是带电场的共变微分。令
\[
U=D_r\phi=P/\nu,\quad W=D_{\mathcal L}\phi=\phi'(s),\quad
H=D_rU,\quad d=1-Q²/r²,\quad E=Bd/(2r),\quad c=eBQ/(2r²).
\]
H 为所选规则坐标的二阶带电径向分量，不混称为双零坐标 φ_uu。约束给
\[
B_r=Br|U|²,\quad Q_r=-er²\Im(\phi\bar U),\quad
\lambda_r=E-\lambda/r.\tag{10}
\]
电磁二形式 F_vr=BQ/r²，由 D001 的 F_uv 与坐标变换得，不能改号。

## 2. 精确第二输运方程

由双零波式及混合半径式消去 ν 的输运，得到
\[
D_{\mathcal L}U=-W/r-EU+ic\phi.\tag{11}
\]
标量电磁交换子包含移动方向项：
\[
[D_{\mathcal L},D_r]=-\lambda_rD_r+2ic.
\]
特别是 D_r W=D_𝓛 U+λ_r U−2icφ，不可只保留普通坐标交换子。对(11)作 D_r，再用此式，得到
\[
D_{\mathcal L}H=-(\lambda_r+E)H+2W/r²
+[(E-\lambda_r)/r-E_r+3ic]U
+i(c_r+c/r)\phi.\tag{12}
\]
所有系数由已有数据确定，其中
\[
E_r=\frac{B_r d}{2r}+\frac B{2r}(-2QQ_r/r²+2Q²/r³)-\frac{Bd}{2r²},
\]
\[
c_r=\frac e2(B_rQ/r²+BQ_r/r²-2BQ/r³).
\]
式(12)是 H 的线性 ODE；给任意有限复值 H(0) 得唯一全半线光滑解，因为每个有限区间系数光滑。这里的全半线 ODE 存在不等于 PDE 邻域存在。

## 3. 统一晚时界及对数振荡

ASYM01 的精确尾展开、末端积分及其导数给（常数依赖固定数据及 H(0)，不依赖晚时 s）
\[
\phi=\tfrac1{10}t^{-2-i},\quad W=O(t^{-3}),\quad
U=u_1t^{-1-i}+u_2t^{-2-i}+O(t^{-4}),
\]
\[
u_1=-\tfrac3{400}(1+i),\quad u_2=-\tfrac1{20},\quad
B=1+O(t^{-3}),\quad B_r=O(t^{-2}),\quad Q_r=O(t^{-3}),
\]
\[
E,\lambda_r=O(t^{-4}),\quad E_r=1/R²+O(t^{-3}),
\quad c=\frac e{2R}+O(t^{-3}),\quad c_r=-\frac e{R²}+O(t^{-2}).
\]
此处 R=2。由(12)，
\[
H'=-a(s)H+f_1t^{-1-i}+O(t^{-2}),\quad
a=\lambda_r+E=O(t^{-4}),
\quad f_1=(-1/R²+3ie/(2R))u_1=\tfrac{21}{4000}-\tfrac3{2000}i.
\]
先以绝对 Gronwall 得 H=O(1+log t)。进一步，积分因子 μ=exp(∫₀ˢa) 有非零有限极限，μ(s)=μ∞+O(t⁻³)。主振荡的原函数为 i t⁻ⁱ，有界；其余强迫绝对可积。故改进为
\[
H=H_*+\left(\tfrac3{2000}+\tfrac{21}{4000}i\right)t^{-i}+O(t^{-1}),\tag{13}
\]
其中 H_* 是依赖角点值的有限复常数。H 一般不趋零，但有界，H'=O(t⁻¹)。这不是把 |t⁻¹⁻ⁱ| 的不可积性误当可积；用到了明确的非零对数载频 k=−1。

## 4. 度量及电磁场的全部沿线工作阶数

对(10)径向微分，不对未知横向量偷偷取零：
\[
B_{rr}=Br²|U|^4+B|U|²+2Br\Re(H\bar U)=O(t^{-1})\to0.\tag{14}
\]
这里首项 Br² 表示 B·r²，而非 B_r·r；由 B_r=Br|U|² 代入而来。也有
\[
\lambda_{rr}=E_r-\lambda_r/r+\lambda/r²\to1/R²,
\]
\[
A_{rr}=2\lambda B_{rr}+4B_r\lambda_r+2B\lambda_{rr}\to2/R²=1/2.\tag{15}
\]
这支付了 ASYM02 留下的 2λB_rr 项。A→0、A_r→0、B→1、B_r→0 已得。

时间/混合导数也需单独核对。沿 Γ 的普通导数用下标 s，固定 r 的入射时间导数用 v。由精确 ODE 和尾展开，
\[
B_s=O(t^{-4}),\ B_{ss}=O(t^{-5}),\ (B_r)_s=O(t^{-3}),
\quad A_s=O(t^{-6}),\ A_{ss}=O(t^{-7}),\ (A_r)_s=O(t^{-5}).
\]
例如 (B_r)_s 由 B、r、U 和(11)直接微分，未用未知 H_s 的额外衰减；(A_r)_s 用 λ_r=E−λ/r。对任一标量度量系数 F，
\[
F_v=F_s-\lambda F_r,\quad F_{vr}=(F_r)_s-\lambda F_{rr},
\quad F_{vv}=F_{ss}-2\lambda(F_r)_s+\lambda²F_{rr}-\lambda_sF_r.
\]
利用 λ=O(t⁻⁵)、λ_s=O(t⁻⁶)，得到沿 Γ 的 A_v,A_vr,A_vv、B_v,B_vr,B_vv 全部趋零。因此全部二阶点态 jets 与同一极端 RN 的 r=R 值相容。转换到 ρ=r−rΓ(v) 只增加含 λ、λ_s 的消失项；仍仅沿 ρ=0，不是固定 ρ 半条带范数。

电磁系数 F_vr=BQ/r²→1/R；径向导数趋 −2/R²，v 导数趋零，因为 Q_s=O(t⁻⁵)、Q_r=O(t⁻³)、Q_v=Q_s−λQ_r。故电磁场的一阶沿线 jets 也相容。φ→0、U→0、D_vφ=W−λU→0；不宣称标量 H→0，而 A4 并未单独要求所有标量二阶径向导数消失。

## 5. 作用域、退出条件与实际邻域缺口

本轮证明同一纯渐近射线数据可以通过所有上述沿线 C² 度量/C¹ 电磁必要阶数检查，而不是只检 Ric(N,N)。任何有限 H(0) 都不产生这一阶数的强制障碍。

仍未给：固定正宽度 ρ∈[0,δ] 的实际解及统一收敛、非线性横向误差/高阶范数、完整 I⁺、Γ 的事件视界身份、Bondi–视界同参、正则中心/AF过去延拓、固定 X⁶ 同一三分支。射线数据甚至还没有被证明来自任一合法全局初值。

**达到本轮退出条件：不继续靠增加形式 jets 宣称接近验收。** 下一项必须是实际正宽度邻域的可行性审查：横向特征边界自由数据、角点兼容、极端退化的传播宽度与所需函数空间；若只能得到随晚时收缩的邻域，必须明确不足以满足 A4。Goal A 仍 OPEN。
