# A-INC01：带电入射准备的正则 Cauchy 初值族

2026-10-16。性质：D001/D002 约束的直接推导和小振幅 ODE 存在证明；**内部证明稿，未经外部独立审查**。扩展 L002 的用途为产生非零径向动量、可调相位电荷的候选。没有证明演化色散、形成或临界性，也不声称首创。

## 1. 数据与精确约束

固定 0<r₀<R、e=3/5，实函数 ψ∈C∞c((r₀,R)) 非零；固定支持和尺度。幅度 a 与相位频率 ω 为参数。记

\[
\Delta=1-2m/r,\quad h=\Delta^{-1}dr^2+r^2d\omega_{S^2}^2,
\quad \phi=a\frac{\psi(r)}r e^{-i\omega r},\quad A_\Sigma=0,
\]
\[
\Pi=\frac{a\sqrt\Delta}{r}(\psi'-i\omega\psi)e^{-i\omega r},
\qquad E=\frac{Q\sqrt\Delta}{r^2}\partial_r.
\tag{I1}
\]

K 的混合本征值取 (kᵣ,kₜ,kₜ)，其中 kₜ=0。设

\[
P=\psi'(\psi'-\psi/r)+\omega^2\psi^2,\qquad
k_r=-\frac{a^2\sqrt\Delta}{r}P.
\tag{I2}
\]

以 m(r₀)=Q(r₀)=0 解

\[
Q'=e\omega a^2\psi^2,
\tag{I3}
\]
\[
m'=\frac{Q^2}{2r^2}+\frac{a^2\Delta}{2}
\left[\psi'^2+(\psi'-\psi/r)^2+2\omega^2\psi^2\right].
\tag{I4}
\]

这里 m 是初始片 Hawking 质量：kₜ=0 给 n(r)=0，因此 1−2m/r=|∇Σr|²。只在 Δ>0 的解段使用这些公式。

**Gauss 检查。** Dᵣφ=a e⁻ⁱωʳ(ψ'−ψ/r−iωψ)/r，由 (I1)

\[
e\Im(\phi\bar\Pi)=e\omega a^2\sqrt\Delta\,\psi^2/r^2,
\quad \operatorname{div}_hE=\sqrt\Delta Q'/r^2.
\]

故恰得 (I3)。电荷由正则中心积分产生；ω 翻号使 Q 翻号，几何不变。

**动量检查。** 径向 Maxwell 场无 Poynting 通量，标量给

\[
j_r=-\Re(\Pi\overline{D_r\phi})=-a^2\sqrt\Delta P/r^2.
\]

任意球对称混合本征值满足

\[
\nabla^j(K_{rj}-h_{rj}\operatorname{tr}K)
=2[(k_r-k_t)/r-k_t'].
\]

取 kₜ=0 后，动量约束要求 kᵣ=r jᵣ，正是 (I2)。不将 K=0 与非零 jᵣ 同时强加。

**Hamiltonian 检查。** kₜ=0 使 (tr K)²−|K|²=0；R(h)=4m'/r²。由

\[
\rho=\tfrac12\{Q^2/r^4+|\Pi|^2+\Delta|D_r\phi|^2\}
\]

得到 m'=r²ρ，即 (I4)。全部三个约束同时成立。

## 2. “入射准备”的准确含义

按项目 K 的号数，Kθθ=−r n(r)，故 n(r)=0。令 L=n+√Δ∂ᵣ、L̲=n−√Δ∂ᵣ，g(L,L̲)=−2。于是

\[
D_{\underline L}(r\phi)=r\Pi-\sqrt\Delta\partial_r(r\phi)=0.
\tag{I5}
\]

这是初始片上 rescaled scalar rφ 的一个特征分量为零，作为入射准备条件。不把它称为演化中无反散射；jᵣ 也不必逐点同号。初始膨胀为 ±2√Δ/r，因此所有正半径球未陷俘；事件视界身份仍未知。

## 3. 小振幅全局正则存在

固定 |ω|≤W。定义

\[
C_Q=|e|W\int_{r_0}^R\psi^2dr,
\quad C_1=\frac12\int_{r_0}^R
[\psi'^2+(\psi'-\psi/r)^2+2W^2\psi^2]dr,
\]
\[
C_2=C_Q^2\left(\frac{R-r_0}{2r_0^2}+\frac1{2R}\right).
\]

取 a₀>0 使

\[
2(C_1a_0^2+C_2a_0^4)/r_0<1/2.
\tag{I6}
\]

在 Δ≥1/2 的 bootstrap 区域，(I3) 给 |Q|≤C_Qa²；(I4) 给 m≥0、Δ≤1，且支持内 m≤C₁a²+C_Q²a⁴(R−r₀)/(2r₀²)。外区显式为

\[
Q=Q_\infty,\quad m=M-Q_\infty^2/(2r),
\quad M=m(R)+Q_\infty^2/(2R).
\tag{I7}
\]

因此全域 m≤M≤C₁a²+C₂a⁴，(I6) 改善 Δ>1/2，ODE 连续依赖与延续闭合。内区 m=Q=K=φ=Π=0，中心平直；ψ 在边界全阶平坦，因此接合光滑。h 完备（Δ≤1），外区精确电真空初始尾满足 AF。固定扣除 1/r 度量和 1/r² 电场主项后，余项及其导数具规定的带权可积性。

在此参数紧集，ODE 右端及重建数据对 (a,ω) 光滑；中心固定平直、支持固定、外尾显式，故参数映射在固定 X⁶ 中光滑，各成员 C∞；每个固定阶范数有共同界。ωa≠0 时 Q∞=eωa²∫ψ² 非零。这完成合法候选族的局部存在；大幅度只能在另行核实 Δ>0 和外尾正定的参数域使用。

## 4. 小振幅电荷效率与固定宽度限制

记 B=∫ψ²、A=∫ψ'²，λ=A/B>0。分部积分给

\[
\int(\psi'-\psi/r)^2dr=\int\psi'^2dr,
\]

故一致地对 |ω|≤W，

\[
M=a^2(A+\omega^2B)+O(a^4),\qquad Q_\infty=e\omega a^2B,
\]
\[
\lim_{a\to0,a\ne0}\frac{|Q_\infty|}{M}
=\frac{|e\omega|}{\lambda+\omega^2}
\le\frac{|e|}{2\sqrt\lambda}.
\tag{I8}
\]

最优相位频率 |ω|=√λ。Dirichlet Poincaré 不等式 λ≥π²/(R−r₀)² 给

\[
\sup_\omega\lim_{a\to0}|Q_\infty|/M\le |e|(R-r_0)/(2\pi).
\tag{I9}
\]

对非零 C∞c 剖面，等号所需的整区间正弦不在 C∞c 内。窄壳高频并不无限提高电荷效率；扩大支持属于选择不同固定族，不能在目标曲线上随参数缩放单位。

(I8)–(I9) 仅为这类初值的 ADM 比和小振幅极限，不是终态比，不给目标 A 的质量门槛，也不禁止其他数据类。数值生成器使用闭支持在 [r₀,R]、端点全阶平坦的 bump；它同样可取在略大的开壳中以符合 C∞c 的记法。

## 5. 仍需完成

1. 在合法参数域中构造/采用符合本系统和规范的实际演化方法，先完成 Minkowski 和小数据基准。
2. 在固定支持族中研究不止幅度的参数方向，避免把第二类近中性阈值误认为目标极端阈值。
3. 全部色散、真正形成、晚时终态、候选中心行为和临界身份均未证明。

推导来源：[D001/D002](../../definitions/MODEL.md)、[L002](../../proofs/RECCVS_L002.md)。[Gundlach–Martel 2511.14874v3](https://arxiv.org/abs/2511.14874v3) 仅作为带电正则中心演化方法和基准方向，未将其数值结果或其他规范系数用作本命题证明。
