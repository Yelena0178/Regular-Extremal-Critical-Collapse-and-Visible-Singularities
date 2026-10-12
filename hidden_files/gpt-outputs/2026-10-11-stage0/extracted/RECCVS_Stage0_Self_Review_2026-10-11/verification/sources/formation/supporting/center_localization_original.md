# OPEN B：完整非线性中心局部化估计

2026-09-28。接续 `OPEN_B_smooth_center_route_2026-09-28.md`。

本文只处理中心局部修正的有限阶横向导数估计，不宣称已经完成光滑全局塌缩主定理。核心做法是在中心附近改用 Bondi 面积半径坐标及变量 \(h=\partial_R(R\phi)\)，先估计完整耦合系统，再转回原来的双零坐标。本文的证明尚需外部独立审查。

## 1. 精确命题与适用范围

固定一个光滑正则中心背景锥，采用原稿规范

\[
g_{(4)}=-e^\ell dUdt+r^2d\omega^2,\qquad A=A_UdU,
\qquad \ell(0,t)=0,
\]

并固定 \(r(0,0)=0\)、\(r_t(0,0)=\beta>0\)、\(e\in\mathbb R\)。中心处电势为零；横向坐标用中心固有时 \(u\) 归一化为 \(U=2\beta u\)。假定 \(r(0,t)>0\) 对 \(0<t\le b\)。不要求整个锥上 \(r_t>0\)：面积半径坐标只在中心附近使用。

记 \(\Phi(t)=\phi(0,t)\)，取 \(\chi\in C^\infty\)，在零点附近为 1，在 \([1,\infty)\) 为零。对固定整数 \(n\ge2\)，作修正

\[
\Phi_\varepsilon(t)=\Phi(t)+\frac{a}{n!}t^n\chi(t/\varepsilon),
\qquad a\in\mathbb C.
\tag{1.1}
\]

所有横向导数均指满足正则中心相容条件的完整 EMCSF 锥导数。可以对已有的光滑正则局部发展应用下述结论；也可以将证明视为对其递归锥导数层级的估计。本估计不单独承担局部时空存在定理或全局延拓定理。

**中心局部化命题。** 令 \(c=(4\beta^2)^{-1}\)。对任意固定 \(d>0\)，在 \([d,b]\) 上有

\[
\partial_U^j(\phi_\varepsilon-\phi)=O(\varepsilon(1+|\log\varepsilon|)),
\qquad 0\le j\le n,
\tag{1.2}
\]

\[
\boxed{\displaystyle
\partial_U^{n+1}(\phi_\varepsilon-\phi)(0,t)
=-\frac{(n+1)\beta c^{n+1}}{r(0,t)}a
+O(\varepsilon(1+|\log\varepsilon|)).}
\tag{1.3}
\]

与此同时，下列几何、电磁导数的差也为同一量级：

\[
\partial_U^j(r_\varepsilon-r),\quad 0\le j\le n+1;
\qquad
\partial_U^j(\ell_\varepsilon-\ell,Q_\varepsilon-Q,A_{U,\varepsilon}-A_U),
\quad0\le j\le n.
\tag{1.4}
\]

常数依赖固定阶数、背景的有限多个光滑范数、\(d,b,\beta,e,\chi\) 和 \(a\) 的有界范围，不要求对 \(n\to\infty\) 一致。对于固定 \(\beta\) 的光滑有限参数背景族，以上估计也成立于这些参数及 \((\Re a,\Im a)\) 的 \(C^1\) 范数中，常数在紧参数集上一致。

因此，上一稿第 6 节要求的最高阶响应系数，在这里指定的中心规范下为

\[
\kappa_n(\Phi)=-\frac{(n+1)\beta c^{n+1}}{r(0,b)}\ne0.
\tag{1.5}
\]

以下给出推导，并特别说明不能省略的平均算子、几何反馈和坐标转换。

## 2. 中心附近的完整 Bondi 系统

在 \(r_t>0\) 的中心小邻域取 \(R=r\)，用中心固有时 \(u\) 标记出射零锥。写

\[
g_{(4)}=-g\,s\,du^2-2g\,du\,dR+R^2d\omega^2,
\qquad A=\alpha\,du,
\tag{2.1}
\]

其中 \(g(u,0)=s(u,0)=1\)、\(\alpha(u,0)=Q(u,0)=0\)。此处的小写 \(g\) 是 Bondi 系数，不是四维度量。

定义平均算子、标量变量及差值

\[
\mathsf H f(R)=\frac1R\int_0^R f(x)\,dx=\int_0^1f(\theta R)\,d\theta,
\]
\[
h=\partial_R(R\phi),\qquad f=\mathsf Hh=\phi,
\qquad q=h-f=R\phi_R.
\tag{2.2}
\]

由原双零约束方程得到以下精确关系：

\[
L:=\log g=\int_0^R\frac{|q(x)|^2}{x}\,dx,
\tag{2.3}
\]
\[
Q=e\int_0^R x\,\operatorname{Im}\big(f(x)\overline{h(x)}\big)\,dx,
\qquad
\alpha=-\int_0^R\frac{g(x)Q(x)}{x^2}\,dx,
\tag{2.4}
\]
\[
s=\mathsf H\left[g\left(1-\frac{Q^2}{R^2}\right)\right].
\tag{2.5}
\]

对应的完整标量演化为

\[
\boxed{\quad h_u=a_0(h)h_R+B(h),\qquad a_0(h)=\frac{s}{2},\quad}
\tag{2.6}
\]
\[
B(h)=\frac{s_R}{2}(h-f)-ie\alpha h
+\frac{ie,gQ}{2R}f.
\tag{2.7}
\]

式 (2.3)–(2.7) 包括标量引起的引力反馈和电磁反馈，并非固定背景测试波方程。

### 2.1 规范和符号的核对

原方程 \(Q_t=er^2\operatorname{Im}(\phi\overline{\phi_t})\) 在固定 \(u\) 下变为
\(Q_R=eR^2\operatorname{Im}(\phi\overline{\phi_R})\)，即 (2.4)。电势方程变为 \(\alpha_R=-gQ/R^2\)。Raychaudhuri 方程给出 \((\log g)_R=R|\phi_R|^2\)，即 (2.3)。角向 Einstein 方程给出 \((Rs)_R=g(1-Q^2/R^2)\)。

为核对带电波方程，令 \(\psi=R\phi\)。从 \(D^aD_a\phi=0\) 直接展开得

\[
2\psi_{uR}=\frac1R\partial_R(R^2s\phi_R)
-2ie\alpha\psi_R-ieR\alpha_R\phi.
\]

代入 \(h=\psi_R\)、\(q=R\phi_R\)、\(\alpha_R=-gQ/R^2\)，即得 (2.6)–(2.7)。最后一个电荷项的正号由此固定。

### 2.2 中心阶数

对于光滑 \(h\)，

\[
q=O(R),\quad g-1=O(R^2),\quad Q=O(R^3),
\quad\alpha=O(R^2),\quad s-1=O(R^2),\quad B=O(R^2).
\tag{2.8}
\]

故 \(a_0(0)=1/2\)、\(a_{0,R}(0)=0\)、\(B(0)=B_R(0)=0\)。这些恒等式对每个 \(u\) 成立，不能把中心看成任意给定的入射边。

## 3. 横向导数层级及最高局部微分项

记

\[
h_j=\partial_u^jh|_{u=0},\quad f_j=\mathsf Hh_j,
\quad q_j=h_j-f_j,
\]

并对 \(L,g,Q,\alpha,s\) 使用相同下标。以下均是普通导数而非除以阶乘的 Taylor 系数。

完整约束层级为

\[
(L_j)_R=\frac1R\sum_{k=0}^j{j\choose k}q_k\overline{q_{j-k}},
\tag{3.1}
\]
\[
(Q_j)_R=eR\sum_{k=0}^j{j\choose k}
\operatorname{Im}(f_k\overline{h_{j-k}}),
\tag{3.2}
\]
\[
(\alpha_j)_R=-\frac1{R^2}\sum_{k=0}^j{j\choose k}g_kQ_{j-k},
\tag{3.3}
\]
\[
s_j=\mathsf H\left[g_j-
\frac1{R^2}\sum_{k+l+m=j}\frac{j!}{k!l!m!}g_kQ_lQ_m\right].
\tag{3.4}
\]

这里 \(g_j\) 由 \(g=e^L\) 的有限乘积法则决定；\(L_j(0)=Q_j(0)=\alpha_j(0)=0\)，且 \(g_j(0)=s_j(0)=0\) 对 \(j\ge1\)。式 (3.1) 的和为实数。

若 \(B_j=\partial_u^jB|_{u=0}\)、\(a_j=s_j/2\)，则

\[
\boxed{h_{j+1}=\sum_{k=0}^j{j\choose k}a_k\partial_Rh_{j-k}+B_j.}
\tag{3.5}
\]

以上构成一个逐阶可计算的闭合层级。

### 引理 3.1：有限阶微分结构

固定 \(N\) 及 \(C^N\) 有界的光滑种子集合。对 \(1\le j\le N\)，有

\[
h_j=a_0(h)^j\partial_R^jh+\mathcal R_j(h),
\tag{3.6}
\]

且在此集合上

\[
\|\mathcal R_j(\widetilde h)-\mathcal R_j(h)\|_{C^0}
\le C_N\|\widetilde h-h\|_{C^{j-1}}.
\tag{3.7}
\]

相应的混合估计为：当 \(m+j\le N\) 时，余项在 \(C^m\) 中的差由 \(C^{m+j-1}\) 输入差控制。常数可依赖两种子的 \(C^{m+j}\) 上界。有限参数的一次微分满足同类估计。

**证明。** 给出需要的算子规则，以免把 (3.7) 当成未证的“无导数损失”断言。

首先

\[
\partial_R^m\mathsf Hv=\int_0^1\theta^m v^{(m)}(\theta R)\,d\theta,
\qquad
\frac{v-\mathsf Hv}{R}=\int_0^1\theta v'(\theta R)\,d\theta.
\tag{3.8}
\]

其次，(2.3) 的一次变分为

\[
DL(h)[v]=2\operatorname{Re}\int_0^R
\frac{\overline q}{x}\,(v-\mathsf Hv)\,dx.
\tag{3.9}
\]

背景因子 \(q/x\) 光滑。因此在背景 \(C^{k+1}\) 有界时，该一次变分将 \(C^k\) 输入映入 \(C^{k+1}\)。二次变分的被积函数为
\(2\operatorname{Re}[(v-\mathsf Hv)\overline{(w-\mathsf Hw)}]/x\)：将一个零点消失因子用 (3.8) 除以 \(x\)，只需在该因子上多用一阶导数。更高变分来自指数的有限乘积，不产生新的奇性。

对 (2.4)，一次变分的被积函数分别为

\[
ex\operatorname{Im}\{(\mathsf Hv)\overline h+f\overline v\},
\qquad
-\frac{Dg[v]Q+gDQ[v]}{x^2}.
\]

第一式也可将虚部改写为
\(\operatorname{Im}\{(\mathsf Hv)\overline q+f\overline{(v-\mathsf Hv)}\}\)。这显示中心消失阶数。结合 \(Q=O(x^3)\)，第二式无不可积项。对 (2.5) 及 (2.7) 用相同规则；\(s_R\) 的最高种子阶数为零，\(B\) 的最高种子阶数也为零，系数的光滑上界可多用一阶背景导数。

从而得到下列导数计数规则：\(h_j\) 的空间 \(m\) 阶导数至多使用种子的 \(m+j\) 阶；\(a_j\) 的空间 \(m\ge1\) 阶导数至多使用 \(m+j-1\) 阶输入差，系数上界可使用 \(m+j\) 阶背景；\(a_j\) 本身至多使用 \(j\) 阶输入差；\(B_j\) 的空间 \(m\) 阶导数至多使用 \(m+j\) 阶输入差。

这些规则也适用于约束的高阶时间导数。例如 (3.1) 的最高阶项为 \(2\operatorname{Re}(\overline q_0q_j)/R\)，其中除以 \(R\) 的因子可固定为背景 \(q_0\)。其余项有 \(1\le k\le j-1\)，把 \(q_k/R\) 写成 (3.8) 至多使用 \(h_k\) 的一阶导数，即种子的 \(k+1\le j\) 阶。对差分展开时将差落在最高阶因子上，并让另一个光滑因子承担除法。其余约束式同理；所有乘积只有有限项。

现在对 (3.5) 归纳。\(j=1\) 时余项为 \(B\)。若 (3.6) 对 \(j\) 成立，则 \(a_0\partial_Rh_j\) 唯一产生 \(a_0^{j+1}\partial_R^{j+1}h\)；其余部分只含至多 \(j\) 阶输入。\(k\ge1\) 的项 \(a_k\partial_Rh_{j-k}\) 也只含至多 \(j\) 阶输入；\(B_j\) 同样如此。上述算子规则给出相应差分界，完成 (3.6)–(3.7) 的归纳。再作 \(m\) 次空间微分，得到混合版本。对参数微分只增加乘积项，不增加空间微分阶数。证毕。

**重要限制。** 本引理不是说终端映射在全部 \(C^{n-1}\) 数据上连续到第 \(n+1\) 阶。第 \(n\) 阶局部微分项已经在 (3.6) 中显式保留，不能被余项估计吞掉。

## 4. 局部修正的边界层估计

先在 Bondi 种子中考虑

\[
\widetilde f-f=\frac{z}{n!}R^n\chi(R/\varepsilon),
\qquad v_\varepsilon=\widetilde h-h=\partial_R[R(\widetilde f-f)].
\tag{4.1}
\]

则 \(v_\varepsilon\) 支撑于 \([0,\varepsilon]\)，满足

\[
\|v_\varepsilon\|_{C^k}\le C\varepsilon^{n-k}\ (k\le n),\qquad
v_\varepsilon^{(k)}(0)=0\ (k<n),\quad
v_\varepsilon^{(n)}(0)=(n+1)z.
\tag{4.2}
\]

由引理 3.1，令 \(\Delta h_j=\widetilde h_j-h_j\)，得到

\[
|\Delta h_j(R)|\le C\left[
\varepsilon^{n-j}\mathbf1_{R\le\varepsilon}
+\varepsilon^{n-j+1}\right],\qquad0\le j\le n.
\tag{4.3}
\]

其中主要项是 \(a_0^jv_\varepsilon^{(j)}\)；系数变化乘以有界的最高阶输入仍被右端余项控制。固定阶的混合导数满足相应版本。

特别地，

\[
|\Delta h_n|\le C(\mathbf1_{R\le\varepsilon}+\varepsilon),\quad
\|\Delta h_n\|_{L^1(0,R_*)}\le C\varepsilon,
\tag{4.4}
\]
\[
|\mathsf H\Delta h_n(R)|\le C\{\min(1,\varepsilon/R)+\varepsilon\}.
\tag{4.5}
\]

这里 \(R_*\) 为固定中心邻域的外半径。

### 4.1 中心最高阶值是精确的

在中心，(3.5)、(2.8) 及 (3.8) 表明

\[
h_n(0)=2^{-n}h^{(n)}(0)
+P_n(h(0),h'(0),\ldots,h^{(n-1)}(0)),
\tag{4.6}
\]

其中 \(P_n\) 是由有限次乘积、共轭和中心 Taylor 运算形成的光滑表达式，不含中心以外的数据。原因是所有非局部积分在中心的 Taylor 系数都由同阶或低阶中心系数决定，且 \(a_0(0)=1/2\)。故

\[
\boxed{\Delta h_n(0)=\frac{n+1}{2^n}z.}
\tag{4.7}
\]

无需在这一步取 \(\varepsilon\to0\)。

## 5. 最高阶几何反馈的估计

低于第 \(n\) 阶的场由 (4.3) 及其混合版本直接趋近。需要单独处理包含 \(h_n\) 的最高阶约束。

取 \(\eta_\varepsilon=\varepsilon(1+|\log\varepsilon|)\)。由 (4.4)–(4.5)，

\[
\int_0^{R_*}(|\Delta h_n|+|\mathsf H\Delta h_n|)\,dR
\le C\eta_\varepsilon.
\tag{5.1}
\]

对数来自平均算子作用于边界层后产生的 \(\varepsilon/R\) 尾部，不能直接删去。

在 (3.1) 中，将最高阶部分写为

\[
\frac{2}{R}\operatorname{Re}(\overline q_0q_n).
\]

\(q_0/R\) 光滑有界，故其差分积分由 (5.1) 控制。其余项只含 \(h_j\)、\(j<n\)，按 (4.3) 控制。于是

\[
\|\Delta L_n\|_\infty+\|\Delta g_n\|_\infty\le C\eta_\varepsilon.
\tag{5.2}
\]

同理，由 (3.2) 的最高阶项
\(eR\operatorname{Im}(f_0\overline{h_n}+f_n\overline{h_0})\)，可得

\[
|\Delta Q_n(R)|\le C\begin{cases}
R^2,&R\le\varepsilon,\\
\varepsilon R+\varepsilon R^2,&R\ge\varepsilon.
\end{cases}
\tag{5.3}
\]

因而 \(\|\Delta Q_n/R\|_\infty\le C\varepsilon\)。代入 (3.3)，内区积分贡献为 \(O(\varepsilon)\)，外区至多为 \(O(\varepsilon\int_\varepsilon^{R_*}R^{-1}dR)\)，从而

\[
\|\Delta\alpha_n\|_\infty\le C\eta_\varepsilon.
\tag{5.4}
\]

在 (3.4) 中，最高 \(Q_n\) 总是乘以 \(Q_0/R^2=O(R)\)，故

\[
\|\Delta s_n\|_\infty\le C\eta_\varepsilon.
\tag{5.5}
\]

由 \((Rs_n)_R\) 的公式还得到

\[
\|R\Delta(s_n)_R\|_\infty\le C\eta_\varepsilon.
\tag{5.6}
\]

最后逐项展开 (2.7) 的第 \(n\) 阶时间导数。最高阶项分别为

\[
\frac12(s_n)_Rq_0+\frac12(s_0)_Rq_n,
\quad-ie(\alpha_nh_0+\alpha_0h_n),
\]
\[
\frac{ie}{2R}(g_nQ_0f_0+g_0Q_nf_0+g_0Q_0f_n).
\]

利用 \(q_0=O(R)\)、\((s_0)_R=O(R)\)、\(\alpha_0=O(R^2)\)、\(Q_0=O(R^3)\)，以及 (4.4)–(5.6)，得到

\[
\boxed{\|\Delta B_n\|_{L^1(0,R_*)}\le C\eta_\varepsilon.}
\tag{5.7}
\]

低阶交叉项使用 (4.3) 即可。这一步保留了全部非线性反馈；没有把 \(g,Q,\alpha,s\) 固定为背景。

## 6. 最高阶标量响应

因为 \(\partial_u^{n+1}\phi=\mathsf Hh_{n+1}\)，对 (3.5) 的 \(k=0\) 项分部积分：

\[
R\partial_u^{n+1}\phi(R)
=a_0(R)h_n(R)-\tfrac12h_n(0)
\]
\[
\hspace{1cm}+\int_0^R\left[
-(a_0)_Rh_n+\sum_{k=1}^n{n\choose k}a_k\partial_Rh_{n-k}+B_n
\right]dx.
\tag{6.1}
\]

在任意固定 \(R\ge R_d>0\)，外端边界项的差为 \(O(\varepsilon)\)。积分中第一项用 (4.4)；\(1\le k<n\) 时使用低阶混合估计；\(k=n\) 时使用 (5.5)，因为它只乘固定的 \(h_0'\)。特别注意 \(k=1\)：\(\Delta\partial_Rh_{n-1}\) 在内区只一致有界，未必一致趋零；但其支撑主要部分长为 \(O(\varepsilon)\)，而外区余项为 \(O(\varepsilon)\)，故它的 \(L^1\) 范数仍为 \(O(\varepsilon)\)。不能在这项上误用全区间的 \(C^0\) 小量。最后一项由 (5.7) 控制。因此

\[
\boxed{\displaystyle
\Delta\partial_u^{n+1}\phi(R)
=-\frac{n+1}{2^{n+1}R}z+O(\eta_\varepsilon).}
\tag{6.2}
\]

低阶则由 (4.3) 取平均得到，特别是对 \(j\le n\)，\(\Delta\partial_u^j\phi\to0\) 于每个固定正半径区间。

在整个中心邻域内还有加权界

\[
\sup_{0<R\le R_*}R\,|\Delta\partial_u^{n+1}\phi(R)|\le C.
\tag{6.3}
\]

它允许第 \(n+1\) 阶未加权导数在缩小的边界层内达到 \(O(\varepsilon^{-1})\)，所以不能声称获得了全中心区间上的该阶一致未加权界。

## 7. 原仿射种子的变换与双零坐标

### 7.1 从 \(t\) 到 \(R\) 的种子变换

背景 \(R=r(0,t)\) 满足 \(R=\beta t+O(t^3)\)。修正后半径由同一 Raychaudhuri 初值问题确定。

对于 (1.1)，在 \(t\le C\varepsilon\) 内逐次微分
\(\Delta r''=-|\Phi'|^2\Delta r-\Delta(|\Phi'|^2)\widetilde r\)，得到

\[
|\partial_t^k\Delta r|\le C\varepsilon^{n+2-k},\qquad 0\le k\le n+1.
\tag{7.1}
\]

在中心邻域的其余部分，零阶和一阶差为 \(O(\varepsilon^{n+1})\)，高阶差由相同背景 ODE 控制。因 \(r_t\) 在此邻域有共同正下界，逆函数微分给出相同的有限阶估计。

将新旧种子分别写到它们各自的 Bondi 面积半径上，得到

\[
\widetilde h(R)-h(R)=v_\varepsilon(R)+w_\varepsilon(R),
\]

其中 \(v_\varepsilon=\partial_R[R\,a\,t_0(R)^n\chi(t_0(R)/\varepsilon)/n!]\) 支撑于 \(R\le C\varepsilon\)，\(t_0\) 是背景逆函数；且

\[
\|v_\varepsilon\|_{C^k}\le C\varepsilon^{n-k},\qquad
\|w_\varepsilon\|_{C^k}\le C\varepsilon^{n+1-k},\qquad k\le n.
\tag{7.2}
\]

这些界由链式法则和 (7.1) 得到：内区中种子每多微分一次损失一个 \(\varepsilon\)，而逆函数的修正提供 \(\varepsilon^{n+2}\)；外区中局部修正恒零，只剩背景与逆函数的小改变量。

中心低于第 \(n\) 阶的导数相同，第 \(n\) 阶差精确为

\[
\Delta h^{(n)}(0)=(n+1)\beta^{-n}a.
\tag{7.3}
\]

因此第 4–6 节继续成立，只需将支撑 \(\varepsilon\) 换成 \(C\varepsilon\)，并令 \(z=\beta^{-n}a\)。\(w_\varepsilon\) 的贡献是余项。

### 7.2 双零横向导数

固定入射零坐标 \(t\) 时

\[
\partial_U=\frac1{2\beta}\mathcal D,
\qquad \mathcal D=\partial_u-\frac{s}{2}\partial_R.
\tag{7.4}
\]

同时 \(e^\ell=g r_t/\beta\)。在初始锥上 \(g r_t=\beta\)，所以确实恢复 \(\ell=0\) 的原仿射规范。

展开 \(\mathcal D^{n+1}\phi\) 时，唯一的纯最高时间项是 \(\partial_u^{n+1}\phi\)。其余项包含至少一个 \(R\) 导数，且标量时间阶数至多为 \(n\)。这里用到的混合估计可以明确写为：对 \(j+m\le n+1\)、\(m\ge1\)，在固定正半径区间上，

\[
\Delta\partial_R^m\partial_u^j\phi=O(\eta_\varepsilon).
\tag{7.4a}
\]

证明是从 \(\partial_Rf_j=(h_j-f_j)/R\) 继续微分：最高只出现 \(\partial_R^{m-1}h_j\)，其总阶数 \(j+m-1\le n\)。当等于 \(n\) 时，引理 3.1 中唯一不小的局部项支撑于 \(R\le C\varepsilon\)，在所考察区间恒零；其他项由 \(C^{n-1}\) 小量控制。平均项 \(f_j\) 用 (4.3)–(4.5)。同理，\(s_j\) 的混合空间导数总阶数至多为 \(n\) 时，至少一个空间导数的情况使用约束式 (3.4)，纯时间最高阶则使用 (5.5)。由此所有系数和混合项的差确为 \(O(\eta_\varepsilon)\)。

同样，\(r_U=-s/(4\beta)\) 控制半径至 \(n+1\) 阶；\(\ell=\log(g r_t/\beta)\) 和 \((r_t)_U=-s_Rr_t/(4\beta)\) 控制 lapse 至 \(n\) 阶；\(Q\)、\(A_U=\alpha/(2\beta)\) 的横向导数由约束控制。

因此在中心邻域的任意固定小正半径截面上，

\[
\Delta\partial_U^{n+1}\phi
=-\frac{n+1}{2^{n+1}R}\frac{a}{\beta^n}\frac1{(2\beta)^{n+1}}
+O(\eta_\varepsilon)
=-\frac{(n+1)\beta c^{n+1}}R a+O(\eta_\varepsilon),
\tag{7.5}
\]

并得到 (1.2)、(1.4) 所列低阶差的初值估计。

## 8. 沿完整连接锥的传播

固定一个中心附近的正半径截面 \(t=d_0\)。在 \([d_0,b]\) 上半径有正下界，不再使用 Bondi 面积半径坐标，因此终端 \(r_t=0\) 不构成坐标问题。

原完整双零系统具有以下阶数封闭性：

- 半径至 \(n+1\) 阶的输运使用 lapse 至 \(n\) 阶；
- lapse 至 \(n\) 阶的输运只使用标量至 \(n\) 阶；
- 电荷与电势至 \(n\) 阶只使用相同或更低阶的场；
- 标量至 \(n\) 阶构成低阶封闭层级。

这是直接对原方程作有限次 \(U\) 微分得到的：例如 \(\ell_{Ut}\) 微分 \(n-1\) 次时，\(D_U\phi\) 的最高阶是 \(\partial_U^n\phi\)，不会出现 \(\partial_U^{n+1}\phi\)。

在固定正半径区间，这些有限阶方程的右端为场变量、已知切向种子及低阶导数的光滑表达式。用共同有界邻域内的有限维 ODE 差分估计和 Grönwall 不等式，(1.2)、(1.4) 从 \(d_0\) 传播到 \(b\)。外区种子修正在 \(\varepsilon<d_0\) 时恒零。

对最高标量导数 \(Y=\partial_U^{n+1}\phi\)，原波动方程给出

\[
Y_t=-\frac{r_t}{r}Y+F_n,
\tag{8.1}
\]

其中 \(F_n\) 只涉及上述低阶层级及其由方程确定的切向导数。关键是 \(r_U\phi_t/r\) 产生的最高几何项是 \(\partial_U^{n+1}r\)，已经在 (1.4) 中，而电势项最高使用 \(\partial_U^n A_U\)。

于是

\[
\Delta(rY)(t)=\Delta(rY)(d_0)+O(\eta_\varepsilon),
\]

结合 (7.5) 及 \(\Delta r=O(\eta_\varepsilon)\)，得到 (1.3)。这里不是忽略外区自引力，而是用精确的阶数结构证明它只进入已经受控的余项。

## 9. 参数的一次微分

设背景、耦合及旧维修方向依赖有限参数 \(\theta\)，并在一个紧参数集上具有所需光滑范数的共同界；保持 \(\beta\) 固定。对 (2.3)–(3.5)、(6.1)、(7.1) 和外区 ODE 作 \(\theta\)、\(\Re a\)、\(\Im a\) 的一次微分。

每个新增项仍有以下结构之一：一个受控的背景参数导数乘原差分；一个中心局部化输入参数导数；或最高阶 \(h_n\) 差分的平均。截断函数不依赖这些参数，故支撑尺度不变。第 3 节的乘积和除法规则、第 5 节的 \(L^1\) 估计逐项适用，给出同一个 \(O(\eta_\varepsilon)\) 界。

最高阶中心值 (4.7)、(7.3) 也可以直接对参数微分。因此 (1.2)–(1.4) 的收敛具有上一稿条件性迭代所需的有限参数 \(C^1\) 意义。

这里并不声称存在一个对无限多个参数统一有界的逆算子，也不要求跨阶一致常数。

若维修参数包括变化的 \(\beta\)，只要它在紧参数集上有共同正下界，同样可以处理。此时 (7.3) 的右端为 \((n+1)\beta(\theta)^{-n}a\)，(7.4) 的变换因子为 \((2\beta(\theta))^{-1}\)，对这些显式因子直接微分即可。在种子变换中，\(\partial_\theta t_0(R)=O(R)\)；因此截断的参数微分虽然带来 \(1/\varepsilon\)，但在其支撑上由 \(R=O(\varepsilon)\) 抵消。式 (7.2) 保持相同阶数。

## 10. 本估计完成的部分与未完成的部分

本稿针对中心局部修正给出：完整耦合层级、中心边界层控制、最高阶几何反馈的积分估计、非零终端响应、坐标转换以及有限参数的一次微分控制。关键误差尺度是 \(\varepsilon(1+|\log\varepsilon|)\)。

尚须另行完成的工作包括：对实际采用的有限阶基点和全部维修参数核对联合 Jacobian；将递归锥数据落实到满足四维中心光滑相容性的同一个局部发展；以及新中心数据的完整全局化。不能只凭本文就把光滑存在主定理标记为完成。

## 11. 文献及核验范围

中心特征表述的文献核对：Mädler、Gannouji、Gallo，*Characteristic initial value problems for the Einstein-Maxwell-scalar field equations in spherical symmetry*，Phys. Rev. D 111, 124015 (2025)，https://arxiv.org/html/2503.24162v2 。本文使用的 Bondi 系统由项目原双零方程重新推导；并未把该文当作本局部化估计或全局存在性的现成证明。

本稿应优先独立复核：引理 3.1 的差分阶数计数、式 (5.3) 的电荷边界层估计，以及第 7 节的混合导数转换。代数脚本只能核对方程符号及有限阶中心系数，不能替代这些解析估计。

随附 `../checks/center_and_gluing/check_bondi_center_jets.py` 对非零复背景和 \(e=3/2\) 使用有理数复系数的二元形式幂级数，按完整系统递推，核查 \(n=2,\ldots,6\) 的中心公式 (4.7)。还核查 Bondi Maxwell 补充方程

\[
Q_u-sQ_R+eR^2\operatorname{Im}(\phi\overline{\phi_u})
-e^2R^2\alpha|\phi|^2=0
\]

至 \(u^1R^5\) 的各系数。所有检查通过；脚本不包含关于余项收敛或 PDE 存在性的断言。


---
编排说明：本文件由 2026-10-08 来源包整理，任务代号改为数学主题；具体来源见根目录 SOURCE_MAP.json。正文中的历史验收范围按原阶段保留，当前整链状态以根目录 VERIFICATION.md 为准。
