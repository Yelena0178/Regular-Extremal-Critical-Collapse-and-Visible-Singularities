# A-EXIT02：远场条带的带电回流预算

2026-10-17。内部条件性估计，未经独立数学审查。只适用于满足明示几何界的实际解条带；没有证明 A-EXIT01 的数据在全未来满足这些界。

## 1. 使用 rφ，而不是直接把 θ 叫作回流

令 Ψ=rφ、χ=D_vΨ，采用 A_v=0、D=∂+ieA。初始纯出射条件对应 χ=0（零向量正比例归一化不影响零条件）。θ=rD_vφ=χ−λφ，因此即使纯出射，θ 也一般不为零。

由波方程、[D_u,D_v]=ieF_uv 及 F_uv=Ω²Q/(2r²)，

\[
D_uD_v\Psi=\mathcal V\Psi,\qquad
\mathcal V=\frac{r_{uv}}r+\frac{ie\Omega^2Q}{4r^2}
=\Omega^2\left[-\frac{\varpi}{2r^3}
 +\frac{Q^2}{2r^4}+\frac{ieQ}{4r^2}\right].
\tag{B1}
\]

反序 D_vD_u 的虚部号数相反。电磁项按 r⁻² 衰减，比质量项 r⁻³ 慢，不能遗漏。D_u 是实电势生成的酉相位输运，故其积分因子模长为 1，不需要把 A_u 本身作为可积小量。

## 2. 条带内的非小振幅控制

考虑实际解的矩形条带 u₀≤u≤u₁、v₀≤v≤V，记 ℓ=u₁−u₀。以下常数须对 V 一致：

\[
r\ge R>0,\quad |\varpi|\le M,\quad |Q|\le q,
\quad \lambda/\Omega^2\ge c>0.
\tag{B2}
\]

设 A=sup_u|Ψ(u,v₀)|、B=∫ᵥ₀∞|χ(u₀,v)|dv 有限（若只给有限条带，用该段积分的统一上界）。由 dr=λdv，在每条固定 u 的零线上

\[
\int_{v_0}^V|\mathcal V|dv
\le C_R:=\frac{M}{4cR^2}+\frac{q^2}{6cR^3}
 +\frac{|e|q}{4cR}.
\tag{B3}
\]

沿 u 用酉输运积分 B1，再沿 v 积分 ∂_vΨ=χ，得到

\[
S_V:=\sup_{[u_0,u_1]\times[v_0,V]}|\Psi|
\le A+B+\delta S_V,\qquad \delta=\ell C_R.
\]

若 δ<1，

\[
S_V\le\frac{A+B}{1-\delta},\qquad
\sup_u\int_{v_0}^V|\chi(u,v)|dv
\le B+\frac{\delta(A+B)}{1-\delta}.
\tag{B4}
\]

证明在每个有限 V 上进行，若条带本身延伸至无穷才可用单调极限取 V→∞。B4 不自行提供解的延伸。可取任何固定有限 A，而由增大 R 压低 δ；其中带电贡献的主阶是 |e|qℓ/R，不能只检查 M/R。

## 3. 新生成分量的 L² 界

另要求 λ≥l>0、Ω²≤G，仍对 V 一致。则 r(u,v)≥ρ(v):=R+l(v−v₀)。令 U(u,u₀;v) 为 D_u 的酉传播因子，定义

\[
\chi_{gen}(u,v)=\chi(u,v)-U(u,u_0;v)\chi(u_0,v).
\]

由 B1 与 B4，设 S=(A+B)/(1−δ)，有

\[
|\chi_{gen}(u,v)|\le\ell GS
\left[\frac{M}{2\rho^3}+\frac{q^2}{2\rho^4}
 +\frac{|e|q}{4\rho^2}\right],
\]
\[
\int_{v_0}^\infty|\chi_{gen}(u,v)|^2dv
\le\frac{3\ell^2G^2S^2}{l}
\left[\frac{M^2}{20R^5}+\frac{q^4}{28R^7}
 +\frac{e^2q^2}{48R^3}\right].
\tag{B5}
\]

用 (a+b+c)²≤3(a²+b²+c²) 和 ∫₀∞(R+lv)⁻ⁿdv=1/[l(n−1)Rⁿ⁻¹] 即得。若存在入射边数据，还须加其传播贡献，不能把 χ_gen 当作总 χ。

这只是固定规范下辐射变量的通量预算。实际标量能量包含 θ=χ−λΨ/r；中心处还需正则性消去 r⁻¹ 奇商。B5 不等于已到达中心的能量界，更不是完整色散定理。

## 4. 对新路线的实际影响与尚缺的闭合

已有一个允许非小出射振幅的回流抑制机制：固定条带宽度与质量电荷界时，新生成 χ 的 L¹ 预算随 R⁻¹ 消失，L² 预算的带电主阶随 R⁻³ 消失。这是条件性上界，并非实际解回流的渐近等式。

下一步不能继续扩大本条带而默认假设保留。必须证明：

- 从 A-EXIT01 的 Cauchy 数据得到适用的特征条带及边界预算；初始 E3 不直接等于整条 u=u₀ 边界上的 χ=0。
- 用 Einstein–Maxwell 约束闭合 B2、λ≥l、Ω²≤G；不能把初始 Δ≥1/2 偷换成全未来界。
- 控制壳后的非紧支撑尾、回流进入 r<R 区域及中心反射；固定 ℓ 条带没有覆盖整个未来。
- 将有限但可发散的迟时出口与同一条近临界初值曲线连接。

代数和积分复核见 [verify_outgoing_backscatter.py](verify_outgoing_backscatter.py)。该复核不验证 B2 的 PDE 假设。

后续 [A-EXIT03](OUTGOING_STRIP_BOOTSTRAP.md) 用相容特征边界预算和显式大半径条件，在每个已存在的光滑有限矩形上闭合 B2 及 λ、Ω² 的界。它尚不证明 Cauchy 数据实现这些边界、无限条带延拓或中心区域控制。
