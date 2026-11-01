# A-EXIT08：正则中心零锥的非集中范数

2026-10-17。内部约束估计，未经独立审查。它给出中心零锥上避免集中及控制光学系数的充分条件，尚未证明这些条件在全未来传播。

## 1. 数据与结论

在从正则中心出发的出射零锥上，采用 A_r=0，记 h=∂r(rφ)、Ψ=∫₀ʳh(s)ds、bar h=Ψ/r=φ、d=h−bar h。设数据光滑且满足中心相容性，并有

\[
\|h\|_\infty\le\epsilon,\qquad
\int_0^\infty|h|dr\le\eta,\qquad TV(h)\le\tau.
\tag{N1}
\]

总质量小本身不控制集中；这里增加了幅度和变差条件。对实际存在的有限锥段，也可仅假设这些量在该段具有同样上界。

令 e=3/5，并定义

\[
\delta=4\epsilon^2+\frac{e^2\epsilon^2\eta^2}{4}<1.
\tag{N2}
\]

则沿该锥从中心零初值解约束得到

\[
0\le2m/r\le\delta,\qquad
|Q|\le |e|\eta^2/2,\qquad
m\le\epsilon\eta/2+2e^2\epsilon\eta^3.
\tag{N3}
\]

若 L_opt=λ/Ω²，另有

\[
e^{-\tau^2/2}\le L_{opt}(r)/L_{opt}(0)\le1.
\tag{N4}
\]

这是单个零锥的结论。它不是“任何未来解只凭初始 N1 就色散”的命题。

## 2. 电荷和紧致度

Gauss 与质量约束在面积半径中为

\[
Q_r=e\Im(\Psi\bar h),\qquad
m_r=\tfrac12(1-2m/r)|d|^2+Q^2/(2r^2).
\tag{N5}
\]

记 F(r)=∫₀ʳ|h|。则 |Q(r)|≤|e|F(r)²/2，且 F≤min(εr,η)。于是

\[
|Q(r)|/r\le|e|\epsilon\eta/2.
\]

在 f=1−2m/r>0 的起始区间，m≥0、f≤1、|d|≤2ε，故

\[
0\le m_r\le2\epsilon^2+e^2\epsilon^2\eta^2/8.
\]

从中心积分得到 N3 的紧致度界。δ<1 排除 f 首次退化；质量方程为线性 ODE，光滑中心展开处理原点，故约束可延伸至数据给定的全部半径。

## 3. 质量预算不损失远场体积

直接分部积分给任意 T>0 的恒等式

\[
\int_0^T|h-\bar h|^2dr
=\int_0^T|h|^2dr-T|\bar h(T)|^2
\le\epsilon\eta.
\tag{N6}
\]

中心 Q=O(r³)，故相同有限区间 Hardy 论证给

\[
\int_0^T Q^2/r^2\,dr\le4\int_0^T|Q_r|^2dr
\le4e^2\eta^2\int_0^T|h|^2dr
\le4e^2\epsilon\eta^3.
\tag{N7}
\]

把 N6、N7 代入 N5 即得 N3 的质量界。有限外端的边界项为非正，不要求 Q(T)=0。

## 4. BV 控制光学退化

由中心光滑性及分部积分，

\[
d(r)=r^{-1}\int_0^r s h'(s)ds.
\]

对核 (s/r)1_{r≥s} 在 L²(dr/r) 中应用 Minkowski 不等式，注意每个 s>0 的核范数均为 1/√2，得到

\[
\left(\int_0^\infty|d(r)|^2\frac{dr}{r}\right)^{1/2}
\le TV(h)/\sqrt2.
\tag{N8}
\]

有限锥段同样成立。Raychaudhuri 方程精确给

\[
\partial_r\log(\lambda/\Omega^2)=-|d|^2/r,
\]

于是 N4 成立。这个估计不用位置权重 r^k，正是 BV 能容纳远移启动脉冲的原因。它只比较同一个锥上的光学系数，不控制无限中心时间方向的累计变化。

## 5. 对既有回流的应用

A-EXIT07 给壳后锥 h 的 ε=O(R⁻²)、η=O(R⁻¹)、τ=O(R⁻²)。平直中心帽平滑延接为 h=0，不增加这些预算。因此该锥的紧致度为 O(R⁻⁴)、质量为 O(R⁻³)、光学对数变化为 O(R⁻⁴)。每一结论都首先适用于已存在的有限边段，不预设无限锥存在。

对 A-EXIT04 的显式成员，可用 A-EXIT05 的 S、J 及 l=3/16、G=8/3 取

\[
\eta=J,\quad
\epsilon=\frac{LGS}{l}\left[\frac M{2R^3}+\frac{q^2}{2R^4}
 +\frac{|e|q}{4R^2}\right].
\]

有理计算确认 ε<1.26×10⁻⁸、δ<6.4×10⁻¹⁶、m<3×10⁻¹²。这改善了该锥的粗质量预算，仍不提供未来其它锥的同样范数。

## 6. 未闭合的动力学命题

现在可准确表述缺口：需要从这一初始锥的 (ε,η,τ) 出发，在带电耦合演化中传播适当的幅度、积分和变差界，使 N2 对所有未来锥成立，并证明完整延拓与衰减。初始估计不允许假设未来 N1，也不能用单锥 Raychaudhuri 积分替代无限时间估计。

同模型的 An–Tan BV 区域估计可作为审查线索，但其区域内小变差、几何界和局部尺寸假设仍须逐项兑现。没有将局部估计的反复应用自动当作全局定理。

复核入口：[verify_center_cone_norm.py](verify_center_cone_norm.py)。精确算术和恒等式检查不替代上述积分不等式证明或未来范数传播。
