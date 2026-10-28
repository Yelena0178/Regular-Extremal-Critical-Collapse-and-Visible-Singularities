# A-EXIT03：从特征边界控制远场条带几何

2026-10-17。内部先验估计及证明稿，未经独立审查。改进 A-EXIT02 的几何假设：以下界由相容特征边界数据和明确的大半径条件推出，而不是在整个区域另行假定。该命题只针对已存在的光滑实际解矩形，尚不证明 Cauchy 出口实现、中心发展或完整色散。

## 1. 变量与边界

沿用 A-EXIT02，另令 ζ=D_u(rφ)、N=−ν、f=1−2varpi/r+Q²/r²、W=ζ−νΨ/r=rD_uφ。在规则区域中

\[
\lambda=\kappa f,\quad\Omega^2=4\kappa N,
\quad\partial_v\log N=\frac{2\kappa}{r^2}(\varpi-Q^2/r),
\]
\[
\partial_u\log\kappa=-\frac{|W|^2}{rN},\quad
Q_u=-e\Im(\Psi\bar\zeta),\quad
\varpi_u=-\frac{f}{2N}|W|^2+\frac QrQ_u,
\tag{S1}
\]
\[
\partial_v\zeta=\overline{\mathcal V}\Psi,\qquad
D_u\chi=\mathcal V\Psi.
\tag{S2}
\]

取 u∈[0,ℓ]、v∈[v₀,V]，固定 e=3/5，ℓ>0。假设边界数据光滑、满足全部特征约束和角点兼容性，且：

- v=v₀ 上：N=1/2、r≥R≥1、|Ψ|≤A、|ζ|≤Z₀，其中 A>0、Z₀≥0。
- u=0 上：Ψ=χ=0、κ=1/2、Q=Q₀、varpi=M₀。它是出射电真空边，r_v=f/2；不能再任意指定不相容的 r(v)。

上述 N 的归一化固定 u 的尺度，ℓ 是这个规范下的宽度。两条边界上的约束意味着各边界值不能独立任选；特别是 M₀、Q₀ 与内部解的关系仍须在 Cauchy 实现时检查。

## 2. 显式常数与半径条件

定义

\[
Z=Z_0+1,\quad K=Z+2A,\quad
q=|Q_0|+2|e|A\ell Z+1,\quad
M=|M_0|+4\ell K^2+1,
\]
\[
C_R=\frac{2M}{R^2}+\frac{4q^2}{3R^3}+\frac{2|e|q}{R}.
\]

要求以下六个不等式：

\[
2M/R+q^2/R^2\le1/2,\qquad
4M/R+2q^2/R^2\le1/4,
\tag{S3a}
\]
\[
4\ell K^2/R\le1/4,\qquad
\ell C_R\le1/4,\qquad 2AC_R\le1/2,
\tag{S3b}
\]
\[
2|e|qA\ell Z/R\le1/2.
\tag{S3c}
\]

对固定边界预算，全部可由足够大的有限 R 实现。没有通过改变 e 或长度单位取得小量。

## 3. 严格改善的先验界

在从角点连续延伸的光滑解矩形上，作假设

\[
1/4\le N\le1,\quad1/4\le\kappa\le1/2,
\quad |\Psi|\le2A,\quad|\zeta|\le Z,
\quad|Q|\le q,\quad|\varpi|\le M.
\tag{S4}
\]

以下逐项改善 S4，并证明 r≥R，排除这些界的首次失效。

**半径与势。** S3a 给 1/2≤f≤3/2，故 λ>0，r≥r(u,v₀)≥R。又 λ/Ω²=f/(4N)≥1/8。A-EXIT02 的势积分界恰为上述 C_R。

**标量。** A-EXIT02 中 B=0，由 ℓC_R≤1/4 得 |Ψ|≤4A/3。由 S2 沿 v 积分，并使用 S4 的 |Ψ|≤2A，得

\[
|\zeta|\le Z_0+2AC_R\le Z_0+1/2<Z.
\]

**电荷。** 沿 u 积分 S1，得 |Q|≤|Q₀|+2|e|AℓZ=q−1。

**质量。** |W|≤Z+2A/R≤K，且 f/(2N)≤3。因此

\[
|\varpi|\le|M_0|+3\ell K^2+2|e|qA\ell Z/R
\le|M_0|+3\ell K^2+1/2<M.
\]

这里仅用 varpi_u 的绝对值界；没有假设带电重整化质量单调。

**κ。** S1 给 κ≤1/2，且

\[
\left|\log\frac{\kappa}{1/2}\right|
\le4\ell K^2/R\le1/4,
\quad\kappa\ge\tfrac12e^{-1/4}\ge3/8.
\]

κ≤1/2 是方程的精确单调上界，不需要把这个上界严格改善。

**N。** 使用 dr=κf dv，

\[
\left|\log\frac{N(u,v)}{N(u,v_0)}\right|
\le\int_R^\infty4(M/r^2+q^2/r^3)dr
=4M/R+2q^2/R^2\le1/4.
\]

因 N(u,v₀)=1/2，且 e^{-1/4}≥3/4、e^{1/4}≤4/3，得到

\[
3/8\le N\le2/3,\quad 3/8\le\kappa\le1/2,
\quad\lambda\ge3/16,\quad\Omega^2\le4/3.
\tag{S5}
\]

边界上的启动也可由相同连续性论证完成：v=v₀ 的 N、Ψ、ζ 已给定，κ、Q、varpi 由 u 约束控制；u=0 的 κ、Q、varpi、Ψ 已给定，N、ζ 由 v 方程控制。边界预算必须先满足相容性，不能用此论证免除约束。

所有改善均与 V 无关。对任何已存在的有限矩形，标准首次失效论证给上述界。若要声称整个无限条带存在，还须兑现局部适定性及高阶延拓判据；本稿未把零阶先验界自动当作这些定理。

## 4. 已兑现与未兑现的接口

本稿为 A-EXIT02 提供 c=1/8、l=3/16、G=4/3，及固定 M,q、振幅 S≤4A/3，均来自边界预算。于是其回流界可在每个已存在的有限矩形上使用相同常数。

这比将几何界作为区域内假设更强，但仍没有覆盖：Cauchy 数据到这组特征边界的实现；壳后的 u>ℓ 长尾；向中心传播与反射；全未来延拓和实际 I⁺；近临界族到达该出口。S3 的 R 也必须是实际迟时几何量，不能在共同初值上随参数送到无穷。

有限有理一致性例：e=3/5、A=1、Z₀=1、ℓ=1、M₀=5、Q₀=1、R=4096 满足 S3。它只证明常数条件非空，**不是相容特征数据或临界候选的认证**。

复核：[verify_outgoing_strip_bootstrap.py](verify_outgoing_strip_bootstrap.py) 检查变量改写和该有理例的六项严格余量；不替代上述分析证明或未兑现接口。

后续 [A-EXIT04](OUTGOING_CAUCHY_STRIP.md) 将完整 A-EXIT01 数据沿斜 Cauchy 边界接入同类估计，修正 κ 的上界为 1，并给出一个满足全部半径条件的显式光滑成员。仍未完成无限未来延拓和中心回流控制。
