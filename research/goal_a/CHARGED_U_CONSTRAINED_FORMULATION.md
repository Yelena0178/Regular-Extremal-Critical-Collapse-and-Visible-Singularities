# A-CHG03：沿较短 u 方向输运质量、标量和电荷

2026-10-17。内部等价改写及精确代数复核；随后新增八分量整边有理证书和新方向的十二变量区间核审计，见 `frozen_charged_u_boundary.py`、`verify_frozen_charged_u_boundary.py`、`charged_u_interval_kernel.py`、`verify_charged_u_kernel.py`。普通和优化运行均通过对应有限检查；没有运行此改写的完整二维区间证书。它针对 A-CHG01 的关断段误差预算失败，不能被当成已经解决失败。进一步不同形状的研究见 `ALTERNATIVE_CHARGED_CANDIDATES.md`。

## 1. 等价系统

保留 D001 的 r、κ、θ、ν、z、m、φ、Q、Aᵤ 定义，f=1−2m/r。rᵤ、κᵤ、θᵤ、νᵥ、zᵥ、∂ᵥAᵤ 与 A-CHG01 相同；用另外三条真实约束替换质量、标量和电荷的 v 方程：

\[
 m_u=\frac{Q^2\nu}{2r^2}+\frac12f\nu|z|^2,
\]
\[
 \phi_u=\nu z/r-ieA_u\phi,\qquad
 Q_u=-er\nu\Im(\phi\bar z).
\tag{UC1}
\]

因而沿 u 的八个实分量是 r、κ、Re θ、Im θ、m、Re φ、Im φ、Q；沿 v 的四个实分量是 ν、Re z、Im z、Aᵤ。这个选择需要在出射边认证更多已知解析量，而不是只认证原来的四个分量。

## 2. 被替换方程仍然传播

定义缺陷

\[
 E=r_v-\kappa f,\quad T=\phi_v-\theta/r,
 \quad J=Q_v-er\Im(\phi\bar\theta),
\]
\[
 H=m_v-Q^2\kappa f/(2r^2)-|\theta|^2/(2\kappa).
\]

按 UC1 的 u 方程及未改动的 v 方程求导，精确得到

\[
 E_u=0,\qquad T_u=-\nu zE/r^2-ieA_uT,
\]
\[
 J_u=-e\nu\Im(\phi\bar z)E-er\nu\Im(T\bar z),
\]
\[
 H_u=-\nu|z|^2H/r
       -\{Q^2\nu/r^3-m\nu|z|^2/r^2\}E
       +(Q\nu/r^2)J.
\tag{UC2}
\]

因此若出射边的解析约束数据使 E=T=J=H=0，它们在有界正分母区域继续为零。被替换的四个 v 方程随之恢复；加上原系统的共形 Einstein 恒等式，得到相同的 D001 解。不能省掉 UC1 中的 Q²ν/(2r²) 电磁项。

`verify_charged_u_constraints.py` 对四个齐次恒等式逐项作精确复 Laurent 多项式检查，并拒绝遗漏电磁质量项的变体。普通及 `python -O` 均通过。这不是 PDE 误差证书。

## 3. 对当前失败的可能帮助与尚需兑现的接口

原布局让 m、φ、Q 的边界误差沿完整 v 区间积累；关断段的当前盒失去严格压缩，不能由改变数值提议器绕过。UC1 将它们放在较短的 u 方向，并使用同一锥上可解析认证的 m、φ、Q 作为直接入流。它可能改善预算，但仍须实际验证所有单元，不能预先断言改善幅度。

下一次证书必须补齐：八个入流分量的完整有理误差；相应十二变量残差及 Jacobian 核；方向调整后的共享 Hermite 参考；全部单元的严格压缩；最终 λ 区间。如果这些仍不通过，应细分参考和误差预算，而不能将本改写直接写成实际陷俘结论。
