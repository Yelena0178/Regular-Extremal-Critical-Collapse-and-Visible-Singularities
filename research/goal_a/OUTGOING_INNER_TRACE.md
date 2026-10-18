# A-EXIT05：壳后零边界的真实质量与电荷预算

2026-10-17。内部条件性解析估计；依赖 A-EXIT04 在已存在远场发展上的先验界，未经独立审查。没有证明中心全未来正则或完整色散。

## 1. 零初值提供额外小量

取壳后边 C={u=−R,v≥R}。初始角点 (−R,R) 在平直内区边缘，精确满足 Ψ=Q=m=0。记 δ=LC_R≤1/4、S=A/(1−δ)、J=δS。

A-EXIT04 的移动下端积分给：对每个已存在的有限边段，

\[
\int_R^V|\chi|dv\le J,\qquad
|\Psi(-R,v)|\le\int_R^v|\chi|ds\le J.
\tag{T1}
\]

这里第二个上界使用该边 Ψ 初始为零，强于条带一般的 |Ψ|≤S。所有无限积分记号在未证明延拓时均理解为对有限 V 的统一上界。

## 2. 电荷及其总变差

由于 θ=χ−λΨ/r，Gauss 方程精确化为 Q_v=e Im(Ψ conjugate(χ))。因此令 F(v)=∫ᴿᵛ|χ|，有

\[
\int_R^V|Q_v|dv
\le |e|\int_R^V F(v)F'(v)dv
\le\frac{|e|J^2}{2}=:q_c.
\tag{T2}
\]

于是 |Q|≤q_c。这里证明的是总变差界，不只是允许符号抵消的净电荷界。没有假设回流电荷与外壳电荷同号。

## 3. 斜边条带的 L² 回流界

取 l=3/16、G=8/3，ρ(v)=R+l max(0,v−R−L)。对参与 u 积分的各条零线，r≥ρ(v)。χ 的积分起点在初始片或领先电真空边，两处均为零。故

\[
|\chi(-R,v)|\le LGS
 \left[\frac{M}{2\rho^3}+\frac{q^2}{2\rho^4}
 +\frac{|e|q}{4\rho^2}\right].
\]

将 v∈[R,R+L] 的启动段与后续段分开，得到

\[
\int_R^V|\chi|^2dv\le E_c:=3L^2G^2S^2
\left\{\frac{M^2}{4}\left(\frac L{R^6}+\frac1{5lR^5}\right)
+\frac{q^4}{4}\left(\frac L{R^8}+\frac1{7lR^7}\right)
+\frac{e^2q^2}{16}\left(\frac L{R^4}+\frac1{3lR^3}\right)\right\}.
\tag{T3}
\]

不能直接把矩形的 B5 用在整条斜边区域；这里显式保留了长度≤L 的启动段预算。

## 4. Hawking 质量与重整化质量

实际质量方程为

\[
m_v=\frac{Q^2\lambda}{2r^2}
 +\frac{|\chi-\lambda\Psi/r|^2}{2\kappa}.
\]

在 C 上 λ>0、κ≥3/8、f=λ/κ≤3/2，故

\[
0\le m_v\le\frac{Q^2\lambda}{2r^2}
 +\frac83|\chi|^2+\frac{3\lambda|\Psi|^2}{2r^2}.
\]

由 dr=λdv、r≥R、初始 m=0，得

\[
0\le m\le m_c:=\frac83E_c+\frac{3J^2}{2R}
 +\frac{q_c^2}{2R},\qquad
0\le\varpi\le m_c+\frac{q_c^2}{2R}.
\tag{T4}
\]

这控制实际几何质量，而不把 χ 的 L² 范数直接当成质量。沿此出射边 m_v≥0，与一般 varpi 的不定号输运并不矛盾。

## 5. 显式成员的严格预算及作用域

使用 A-EXIT04 的同一成员和有理预算，精确有理运算给

\[
J<1/2000,\quad q_c<10^{-7},\quad
E_c<2\times10^{-12},\quad
\sup_C\varpi<11\times10^{-12}.
\]

对应近似值为 J≈0.0004626174、q_c≈6.42045×10⁻⁸、E_c≈1.92704×10⁻¹²、m_c≈1.00372×10⁻¹¹。近似值仅便于阅读；严格比较由 [verify_outgoing_inner_trace.py](verify_outgoing_inner_trace.py) 的 Fraction 运算完成。

这些上界对每段已存在的远场边界统一，尚不声称无穷边界已经存在。更不声称质量小就足够排除中心集中：仍须建立适合带电、正则中心系统的特征数据范数，控制径向/零向导数、非紧支撑尾及中心反射，再兑现相应全局定理。此前固定 L002 小振幅族的 A-SD01 不能直接覆盖这组数据。

本稿实际补上了“远场回流变量”到“中心接口上的质量、电荷总变差”的转换。它没有完成近临界负侧到达出口、中心散射或三分支终态。

后续 [A-EXIT06](CENTER_WEIGHTED_NORM_AUDIT.md) 发现固定宽度远移壳的启动回流径向导数具有非零 R⁻² 主项，故 k>2 的带权 C¹ 范数不会随 R→∞ 变小。不能仅凭本稿的小质量预算调用这种中心小数据定理。
