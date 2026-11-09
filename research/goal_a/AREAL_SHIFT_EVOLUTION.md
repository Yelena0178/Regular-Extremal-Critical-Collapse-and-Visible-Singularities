# A-EVOL02：保留同一 Cauchy 数据的径向 shift 演化

2026-10-16。D001 的直接 ADM 约化与探索实现；内部推导，未经外部独立审查。尚未证明此约束重解方案的局部适定性、数值稳定性或严格收敛定理。

## 1. 几何变量与视界

\[
g=-\alpha^2dt^2+b^2(dr+\beta dt)^2+r^2d\omega^2,\quad
W=-n(r),\quad\beta=\alpha W,\quad
z=b^{-1}=\sqrt{1-2m/r+W^2},\quad c=\alpha z.
\]

m 为 Hawking 质量，Q 为同一有向电荷；Aᵣ=0，P=bΠ，X=∂ᵣφ，S=|P|²+|X|²，C=Re(P X̄)。面积半径固定给 K 的本征值

\[
k_t=W/r,\qquad k_r=W_r-rzC,\qquad
\operatorname{tr}K=W_r+2W/r-rzC.
\tag{S1}
\]

初始取 W=0，并保留 A-INC01 的 φ、Π、h、K、E；此时 P、m、Q 恰回到原初值构造。初始 lapse 可取原极切片的 lapse。后续切片不同，不可直接按相同坐标 t 比较两个解的波形。

归一化零膨胀为

\[
\theta_+=2(z-W)/r,\qquad\theta_-=-2(z+W)/r.
\tag{S2}
\]

物质特征速度为 −β±c；1+log 规范速度为 −β±z√(2α)，谐切片的规范速度与物质速度一致。若 W>0、m/r=1/2，则 z=W>0，b 和 lapse 可以保持有限；不会仅因 1−2m/r 变号而停止。双负号的数值样本仍须误差认证，才能作为实际严格陷俘证据。

## 2. 全部演化与径向约束

固定 e=3/5。标量和电势为

\[
\phi_t=\beta X+cP-ieA_t\phi,\qquad
P_t=r^{-2}\partial_r[r^2(cX+\beta P)]-ieA_tP,
\tag{S3}
\]
\[
Q_r=er^2\Im(\phi\bar P),\qquad (A_t)_r=-\alpha Q/(zr^2).
\tag{S4}
\]

Hamiltonian 与动量约束联合给

\[
m_r=\frac{Q^2}{2r^2}+\frac{r^2z^2}{2}S+r^2WzC.
\tag{S5}
\]

角向 ADM 演化与带平移的 lapse 条件给

\[
W_t=\beta W_r-z^2\alpha_r
+\alpha\left[\frac m{r^2}+\frac{rz^2}2S-\frac{Q^2}{2r^3}\right],
\tag{S6}
\]
\[
(\log\alpha)_t=\beta(\log\alpha)_r
-\kappa[W_r+2W/r-rzC],\quad
\kappa=2\ (1+\log),\quad\kappa=\alpha\ (\text{harmonic}).
\tag{S7}
\]

(S6) 来自 kₜ 方程：用 Hamiltonian 消去空间 Ricci 张量中的 bᵣ 和动量约束消去 kᵣ，随后乘 r；βW/r 与 αW²/r 两项恰抵消。标量对角向 Ricci 的直接贡献为零，但通过约束留下 S 项。不能将极切片 lapse 的椭圆 ODE 与 (S7) 同时强加。谐切片使规范特征保持在物理零锥上，便于后续审查切除边界；本轮没有由此证明切除方案适定。

未用于重解约束的时间传播恒等式为

\[
Q_t=er^2\Im[\phi\,\overline{cX+\beta P}],
\tag{S8}
\]
\[
m_t=r^2\alpha z[WzS+(z^2+W^2)C].
\tag{S9}
\]

W=0 时 (S5)、(S8)、(S9) 分别退化到 A-EVOL01 的约束和传播。对 m 的公式可由 mₜ=r²Tₜ{}ʳ、mᵣ=−r²Tₜ{}ᵗ 直接检查；径向 Maxwell 张量在二维轨道上的混合形式为 −Q²/(2r⁴)δ，因此其 Tₜ{}ʳ=0。

## 3. 正则中心与离散

φ、P、logα 偶，W 奇；m,Q=O(r³)，z(0)=1，W/r→Wᵣ(0)。中心取 Wₜ(0)=0、

\[
(\log\alpha)_t(0)=-3\kappa(0)W_r(0),\qquad
P_t(0)=3c(0)\phi_{rr}(0)+3\beta_r(0)P(0)-ieA_t(0)P(0).
\]

仅令中心变量有限，不足以保证正确 Taylor 系数，必须保留 A-EVOL01 的 r² 体积权重。给定场和 W，(S5) 的单格隐式中点可用 z 的正根解二次方程；不要求 mᵣ 在陷俘区保持非负。空间度量正定要求 z²>0，不能误用 1−2m/r>0 作为新的停止条件。

**实际离散使用交错网格。** φ、P、logα 在节点，W 在半格；节点 W 由相邻半格平均，原点取零。半格源中的 m/r³、Q/r³ 先按中心极限正则化后插值，不能直接把 m、Q 的普通平均除以半格半径的高次幂。lapse 方程中的 Wᵣ+2W/r 通过半格通量及精确球体积计算；标量平移通量同样处理。

## 4. 一条必要的离散稳定性修正

最初的同点网格在无物质 Minkowski 线性规范子系统
\[
L_t=-2(W_r+2W/r),\qquad W_t=-L_r
\]
产生了增长实部：单位区间 N=16/32/64 时最大实部约 5.358/10.716/21.432。该问题随加密变快，不能把那一版强场的负号或停止当作物理证据。

现取节点到半格梯度 G、节点正体积矩阵 H₀、半格权重 H₁=diag(hr²face)，令 D=−H₀⁻¹GᵀH₁。实际径向通量差正是此 D，因此
\[
L_t=-2DW,\quad W_t=-GL,\qquad
\frac d{dt}\left(\tfrac12 L^TH_0L+W^TH_1W\right)=0
\]
（原点通量为零，外端节点固定）。这是平直线性半离散规范子系统的能量恒等式；谐切片把系数 2 改为 1 并相应修改能量即可。它不证明非线性耦合系统、RK4 或强场的稳定性。复算入口同时检查加权反对称关系和谱实部。

## 5. 必须兑现的检验与限制

1. 穿越 RN 外视界的 Kerr–Schild 环：m=M−Q²/(2r)，z=(2−D)⁻¹/²，α=z，W=(1−D)z，D=1−2M/r+Q²/r²。检查 (S5)/(S6) 与零膨胀符号；这只是电真空环，不是正则中心塌缩。此处冻结 lapse 只测试角向 Einstein 恒等式，不宣称 KS lapse 是 1+log 或谐切片的稳态。
2. 弱场同一 Cauchy 数据：独立质量/电荷时间传播、空间度量 ADM 演化、中心 Taylor 迹；各规范按中心固有时比较 |φ|，不按相同坐标时间或复相位比较。
3. 强场必须另做网格、边界与误差核查；规范震荡、lapse 趋零、空间度量失正等计算停止仍记未知。

## 6. 将数值负号升级为实际陷俘所需的明确门槛

假设已在同一实际有限因果域内证明一个球的区间包络
\[
r\in[r_-,r_+],\quad m\in[m_-,m_+],\quad W\in[w_-,w_+].
\]
若 r₋>0、w₋>0，且
\[
\mu_*=2m_-/r_+-1>0,\qquad
\sigma_*=1-2m_+/r_-+w_-^2>0,
\]
则该球严格陷俘。证明：z²=1−2m/r+W²≥σ*>0，W²−z²=2m/r−1≥μ*>0，所以 W>z>0。若 z₊²=1−2m₋/r₊+w₊²，则还得到
\[
\theta_+\le-\frac{2\mu_*}{r_+(w_++z_+)},\qquad
\theta_-\le-\frac{2w_-}{r_+}.
\]
这些是精确几何和区间代数的充分条件。输入包络必须来自实际解存在、规范/坐标识别、初值/有限边界误差及连续 PDE 误差；网格差、总质量漂移、浮点舍入检查不能自行充当它们。当前数值报告没有这份包络，因此不作实际陷俘认证，也不按 L001 正式排除一个目标 A 候选。

来源：项目 D001、A-INC01、A-EVOL01；规范定义核对 [Baumgarte–de Oliveira 2201.08857，式 (1)–(2)](https://arxiv.org/abs/2201.08857)。[Alcubierre gr-qc/0210050](https://arxiv.org/abs/gr-qc/0210050) 说明 Bona–Massó 规范的震荡/激波须另审；不能将本轮具体停止归因于其一般机制而不检查。两文均不提供本模型的适定性、陷俘形成或目标 A。
