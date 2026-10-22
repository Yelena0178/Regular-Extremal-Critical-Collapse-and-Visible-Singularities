# A-NULL01：小数据的实际出射光学函数与完整零无穷远

2026-10-16。内部证明稿，未经外部独立数学审查。本文件补齐 A-KL01 所列光学及 Bondi 接口；仅用于 L006 已接入 Kauffman–Lindblad 定理的充分小光滑球对称数据。所有小量阈值可继续缩小，不涉及未知正质量极端端点。

## 1. 已有输入、记号与具体来源

使用 [A-GEO01](CAUSAL_COMPLETENESS.md) 的全局规则图、面积半径导数、全部因果完备和最大未来发展识别，以及 [A-RET01](RETARDED_CAUCHY_BOUNDS.md) 的全时间质量、电荷与标量界。先于本文件得到的估计包括
\[
r_\rho=1+O(\epsilon),\quad r_t=O(\epsilon),\quad
0\le m\le C_e\epsilon^2,\quad |Q|\le C_e\epsilon^2,\quad
r|\phi|\le C\epsilon,\quad 1-2m/r\ge1/2.
\tag{N1}
\]
这里 \(\rho\) 是原笛卡尔半径，\(r\) 是面积半径；\(\epsilon\) 为 KL 数据小量，不是目标 A 的参数区间。

来源固定为 [Kauffman–Lindblad, arXiv:2109.03270v2](https://arxiv.org/html/2109.03270v2)。本轮定点核对 §5 的 (5.2)、(5.23)–(5.25)、Lemma 5.6 的 (5.42)–(5.46)、Theorem 11.1 以及 (12.12)–(12.13)、(13.2)–(13.3)。取 \(N\ge14\)、\(\gamma=3/4\)、\(0<\delta\le1/100\)，物质指数沿用 A-RET01 的 \(s=2/3,s_0=5/4\)。

记来源的径向坐标和质量系数为
\[
R_*=\rho+M_K\widetilde\chi(\rho/(1+t))\log\rho,\quad
q=t-R_*,\quad A=1+t+R_*.
\tag{N2}
\]
\(M_K\) 是来源的质量主项系数，不是 Bondi 终态质量。截止在 \(\rho/(1+t)\le1/4\) 为零、在该比值 \(\ge3/4\) 为一；轴附近没有对数奇点。固定模型转换后 \(M_K=O_e(\epsilon^2)\)。下文即使只用 \(M_K=O(\epsilon)\) 也足够。

## 2. 实际零速及径向导数界

在 \((t,R_*)\) 轨道图中，出射零线满足
\[
\frac{dR_*}{dt}=f(t,R_*),\qquad
f=1+O(\epsilon),\qquad 19/20\le f\le21/20.
\]
设 \(\mathscr F(v)=g^{tt}v^2-2g^{tR_*}v+g^{R_*R_*}\)。出射根为 \(\mathscr F(f)=0\)，且 \(\partial_v\mathscr F(f)=-2+O(\epsilon)\)。

这给出一个可直接检查的来源转换：\(\mathscr F(1)\) 是逆度量的好 \(LL\) 收缩。Lemma 5.6 分解中的 Minkowski 倍数与角向投影均在此收缩中消失；剩下的质量项为二阶余项，以及仅在截止过渡带
\(\mathcal T=\{1/4\le\rho/(1+t)\le3/4\}\) 出现的一阶对数项。因此
\[
|f-1|\le C\epsilon\left[
A^{-1-\gamma+\delta}
+(1+t)^{-2+2\delta}(1+q_+)^{1-\delta}\right]
+\frac{CM_K\log(2+A)}A{\bf1}_{\mathcal T}
+\frac{CM_K^2\log^2(2+A)}{A^2}.
\tag{N3}
\]
其中 \(q_+=\max(q,0)\)。应用隐函数微分，并用 (13.2)、好方向的 (12.13) 及坐标系数的导数界，得到
\[
|\partial_{R_*}^{\,j}f|
\le C_j\left[\epsilon(1+t)^{-2+2\delta}
       +M_K\frac{\log(2+t)}{(1+t)^2}
       +M_K^2\frac{\log^2(2+t)}{(1+t)^3}\right],
\quad 1\le j\le3.
\tag{N4}
\]
需说明两处导数细节：

- 第一次微分的主项是 \(\partial_{R_*}\mathscr F(1)\)，好收缩的导数由 (13.2) 加切向导数控制；余项含 \((f-1)\partial g\)，按 (N3) 与 (12.13) 的乘积估计，比 (N4) 的上界更小。后续径向微分用平移交换场版本的相同估计；\(N-6\ge8\) 留有足够导数。
- 对 \(R_*\gtrsim1+t\)，径向框架导数的 \(1/\rho\) 系数有额外远区衰减；对 \(\rho\le(1+t)/2\)，直接使用内区普通导数界。靠轴用笛卡尔 Taylor 正则性处理，不能在 \(\rho=0\) 除以 \(\rho\)。

尤其 (N4) 的右端在 \(t\in[0,\infty)\) 可积。(N3) 的截止项本身没有这种全时间可积性，必须沿实际零线处理。

## 3. 中心发出零线的迟时比较

以中心坐标发出时间 \(u\ge0\) 标记实际出射线：
\[
R(t,u)|_{t=u}=0,\qquad R_t=f(t,R),\qquad t\ge u.
\]
这里 \(u\) 还不是单位 Bondi 时间，也不是中心固有时。由 \(f\ge19/20\) 和 \(\rho\ge(19/20)R_*\)，当 \(t\ge8(1+u)\) 时
\[
\frac{\rho(t,u)}{1+t}\ge
\left(\frac{19}{20}\right)^2\frac{t-u}{1+t}
\ge\frac{2527}{3200}>\frac34.
\tag{N5}
\]
所以实际线在该时刻以后永不再进截止过渡带。在此前 \(\mathcal T\) 上 \(A\asymp1+t\)，从而
\[
\int_u^\infty
 \frac{\log(2+A)}A{\bf1}_{\mathcal T}\,dt
\le C\log(2+u).
\tag{N6}
\]
积分区间的端点比至多为固定常数；不能把它替换为从 \(u\) 到无穷的 \(\int\log(t)/t\)。

令 \(a=1+u\)。在 \(|q|+1\le2a\) 的连续 bootstrap 中，由 \(q_t=1-f\)、(N3) 得
\[
|q(t,u)-u|
\le C\left[
\epsilon a^\delta+M_K\log(2+u)
+M_K^2\frac{1+\log^2(2+u)}a\right]
=:\mathcal E(u).
\tag{N7}
\]
其中非线性项的积分为
\((2a)^{1-\delta}\int_u^\infty(1+t)^{-2+2\delta}dt
=2^{1-\delta}a^\delta/(1-2\delta)\)。
由于 \(\delta<1\)，所有右端项除以 \(a\) 一致有界；缩小数据阈值可使 \(\mathcal E(u)\le a/4\) 对所有 \(u\ge0\) 成立，严格改善 bootstrap。因此 (N7) 全未来成立，并且
\[
q(t,u)\ge u/2\quad(u\ge1).
\tag{N8}
\]
对每个固定 \(u\)，(N3) 沿线可积，故 \(q(t,u)\) 还有有限极限 \(q_\infty(u)\)。不把这个极限本身用作未经验证的全局坐标。

## 4. 光学标签的非退化、早期出射面与覆盖

参数变分 \(J=R_u\) 满足
\[
J(u,u)=-f(u,0),\qquad J_t=f_{R_*}(t,R)J.
\]
由 (N4)，
\[
0<c\le-J(t,u)\le C<\infty,
\tag{N9}
\]
且固定有限 \(u\) 区间上，\(J\) 及其前两阶 \(u\) 导数有统一界。后者由变分方程再微分得到，右端依次含
\(f_{R_*R_*}J^2\)、\(f_{R_*R_*R_*}J^3\) 及低阶项，均由 (N4) 的可积核控制。

正 \(u\) 图覆盖初始中心出射面内侧的未来。外侧零线向过去交初始片，补以负标签：轴附近先用短时向过去的光滑解定义发出时间的相容初始值，再光滑、严格单调地接到远区 RN 延迟标签。初始径向导数取固定正上下界；不能在原点任意指定 \(-R_*\) 后默认角点所有 jets 相容。应用同一流变分估计，负标签图与中心图在正半径重叠区光滑相接。

初始标量紧支撑之外选一个实际出射面 \(u=u_-<0\)。其外侧是初始电真空区的因果决定域，标量及其导数为零，球对称电真空由质量、电荷常数的 RN 解描述。此面提供第 7 节输运使用的**早期外侧零数据**。不能用 \(u=0\) 的中心出射面替代它，该面可能与入射脉冲相交。

任何实际点的出射线反向追踪，在有限 \(t\) 内交轴或初始片，正向则 \(r\to\infty\)。标签有序且 (N9) 非退化，故给出唯一 AF 端的一套相容出射面，不会把不同人造边界当作不同零无穷远。

## 5. 出射面积半径图和 Bondi 归一化

写原轨道度量为 \(a_0dt^2+2b_0dt\,dR_*+c_0dR_*^2\)。设
\[
\sigma=b_0+c_0f=1+O(\epsilon),\qquad
\lambda=\frac{dr(t,R(t,u))}{dt}=1+O(\epsilon)>0.
\]
在实际 \((u,r)\) 图中，
\[
g=-G\overline G\,du^2-2G\,du\,dr+r^2d\omega^2,\qquad
G=-J\sigma/\lambda,\quad
\overline G=G\mathfrak d,\quad
\mathfrak d=1-\frac{2m}{r}.
\tag{N10}
\]
所以 \(0<c\le G,\overline G\le C\)。固定有限标签区间的大半径端，物质好导数由
\[
D_{\,\partial_t+f\partial_{R_*}}\phi
=D_{\widetilde L}\phi+(f-1)D_{\partial_{R_*}}\phi
\]
及 (N3)、(N7)、KL (10.17) 给
\[
|\phi|\le C_U/r,\quad |D_r\phi|\le C_U/r^2,\quad
|D_u(r\phi)|+|D_u^2(r\phi)|\le C_U.
\tag{N11}
\]
这里 \(D_u\) 是固定 \(r\) 的共变导数；为得到最后一个界，先在来源规则框架调用至二阶的交换场估计，再使用 (N4)、(N9) 给出的有界坐标向量及其导数。系数的普通 \(u\) 导数有界；不假设它们对 \(U\to\infty\) 一致。

径向 Einstein 方程为
\[
\partial_r\log G=r|D_r\phi|^2.
\tag{N12}
\]
它非负且在大半径为 \(O_U(r^{-3})\)。因此存在连续正极限 \(G_\infty(u)\)，满足 \(c\le G_\infty\le C\)，收敛在有限标签区间一致，误差 \(O_U(r^{-2})\)。

定义单位 Bondi 时间
\[
u_B(u)=\int_{u_{\rm ref}}^u G_\infty(v)\,dv.
\tag{N13}
\]
于是 \(du_B/du\) 有正上下界，\(u\to\infty\) 当且仅当 \(u_B\to\infty\)。尚须验证边界正则性；这由第 7–8 节补足，而不是只靠此参数重命名。

## 6. 带电径向规范与精确输运方程

在轨道图取 \(A_r=0\)、\(A_u\to0\) 于无穷远。因 D001 的取向，
\[
F_{ur}=\frac{GQ}{r^2},\qquad
A_u=\int_r^\infty\frac{GQ}{s^2}\,ds,\qquad
\partial_rA_u=-\frac{GQ}{r^2}.
\tag{N14}
\]
积分由 (N1)、(N10) 收敛；相同曲率的势在单连通轨道图相差规范变换，标量同时变换。不能直接要求原 Lorenz 规范的带电辐射场有极限。

记 \(\psi=r\phi\)、\(h=\partial_r\psi\)。精确径向方程是
\[
\frac{G_r}{G}=\frac{|h-\psi/r|^2}{r},\quad
m_r=\frac{\mathfrak d}{2}|h-\psi/r|^2+\frac{Q^2}{2r^2},\quad
Q_r=e\Im(\psi\overline h),
\tag{N15}
\]
\[
\overline G_r=G\left(\frac{2m}{r^2}-\frac{Q^2}{r^3}\right).
\tag{N16}
\]
最后一个等式是 (N15) 中标量项的精确抵消。令
\[
\mathcal T=\partial_u-\frac{\overline G}{2}\partial_r,\quad
\mathfrak a=\frac{\overline G_r}{2}-ieA_u,\quad
\mathfrak b=-\frac{\overline G_r}{2r}+\frac{ieGQ}{2r^2}.
\]
则波方程等价于
\[
\mathcal T h=\mathfrak a h+\mathfrak b\psi.
\tag{N17}
\]
可独立从
\(-D_u(r^2D_r\phi)+\partial_r(-r^2D_u\phi+r^2\overline G D_r\phi)=0\)
展开核对。交换子项 \(-ie(\partial_rA_u)\psi/2\) 不可遗漏。

## 7. 电荷极限与有限标签正则性

先由 (N11)、(N15) 及全局有界 \(Q,m\) 得 \(m_r=O_U(r^{-2})\)，所以 \(m\to M_B(u)\) 存在，误差 \(O_U(r^{-1})\)。但初步 \(Q_r=O_U(r^{-1})\) 不可积，尚不能据此宣称 \(Q_B\) 存在。

对任意有限 \(U>u_-\)，从点 \((u,r)\)、\(u\in[u_-,U]\) 沿 \(\mathcal T\) 向过去，半径增加且只增加 \(O(U-u_-)\)。在足够大的 \(r\) 端，整条特征均留在该大半径区，并于 \(u_-\) 有 \(h=\psi=0\)。由
\[
|\mathfrak a|=O_U(r^{-1}),\quad
|\mathfrak b|=O_U(r^{-2}),\quad |\psi|\le C_U
\]
及有限区间 Gronwall，得
\[
h=O_U(r^{-2}).
\tag{N18}
\]
于是 \(\psi\to\Phi(u)\)、\(Q\to Q_B(u)\)，误差都为 \(O_U(r^{-1})\)，因为 \(\psi_r=h\)、\(Q_r=e\Im(\psi\bar h)\) 现在均可积。这是电荷极限证明的实质新增步骤。

以下导数控制说明规则性，不将“极限存在”偷换成光滑性：

1. 微分 (N17) 一次。由 (N15)–(N16)，
   \(\mathfrak a_r=O_U(r^{-2})\)、\(\mathfrak b_r=O_U(r^{-3})\)，所以
   \[
   \mathcal T h_r=(\mathfrak a+\overline G_r/2)h_r
                      +(\mathfrak a_r+\mathfrak b)h+\mathfrak b_r\psi,
   \]
   给 \(h_r=O_U(r^{-3})\)。再微分一次同理给 \(h_{rr}=O_U(r^{-4})\)；所需 \(m_{rr},Q_{rr},G_{rr}\) 直接由 (N15) 及已得低阶界求出。
2. (N17) 给 \(h_u=O_U(r^{-2})\)，再对 \(r\) 微分给 \(h_{ur}=O_U(r^{-3})\)。Maxwell 和质量的时间方程为
   \[
   Q_u=-e\Im(\psi\overline{D_u\psi})
                          +\overline G e\Im(\psi\overline h),
   \tag{N19}
   \]
   \[
   m_u=-G^{-1}|D_u\psi|^2
            +\overline G G^{-1}
                  \Re[D_u\psi\,\overline{(h-\psi/r)}].
   \tag{N20}
   \]
   它们给 \(Q_u,m_u=O_U(1)\)。\(G_u\) 的初步有界性来自 (N10) 和流变分；(N14) 因而给 \(A_{u,u}=O_U(r^{-1})\)，即势分量对 \(u\) 的导数，不是二形式分量。
3. (N11) 转换到普通导数得到 \(\psi_u,\psi_{uu}=O_U(1)\)；转换用刚得到的势及其导数界。微分 (N17) 对 \(u\)，用上一项及 \(h_{ur}\) 得 \(h_{uu}=O_U(r^{-2})\)。所以 \(\psi\to\Phi\) 为有限标签区间上的 \(C^2_u\) 收敛。由 (N12) 的对数积分及其前两阶 \(u\) 导数，\(G_\infty\) 属 \(C^2\)，相应导数均匀收敛。

还需 \(r^2h\) 的极限以控制紧化后的电磁场。令 \(Y=r^2h\)。有 \(Y_r=O_U(r^{-1})\)，而
\[
Y_u=\frac{\overline G}{2}Y_r+
       (\mathfrak a-\overline G/r)Y+r^2\mathfrak b\psi.
\]
右端与 \(ieG_\infty Q_B\Phi/2\) 的差在 \(r\to\infty\) 时一致趋零；初始 \(Y(u_-,r)=0\)。固定 \(r\) 对 \(u\) 积分，得到
\[
Y\longrightarrow H(u)=\frac{ie}{2}
               \int_{u_-}^uG_\infty Q_B\Phi\,dv .
\tag{N21}
\]
这里不需要先假定 \(Y\) 的极限存在。

## 8. 规则零边界及其完整性

令 \(x=1/r\)，物理度量的共形紧化为
\[
\widehat g=x^2g
=-x^2G^2(1-2mx)\,du^2+2G\,du\,dx+d\omega^2.
\tag{N22}
\]
在任意有限 \(u\) 区间，(N15)、(N18)–(N21) 给：
\[
G\to G_\infty,\quad G_x\to0,\quad
G_{xx}\to-G_\infty|\Phi|^2,\quad
G_{ux}\to0,\quad G_{uu}\to(G_\infty)_{uu}.
\]
例如 \(G_{xx}=r^4G_{rr}+2r^3G_r\)，将 (N15) 微分即可取极限；仅需
\(h=O(r^{-2}),h_r=O(r^{-3})\)。又 \(m_r=O(r^{-2})\)、\(m_{rr}=O(r^{-3})\)、\(m_u,m_{uu}=O_U(1)\)；含质量的项为 \(2x^3G^2m\)，其至二阶所有边界贡献均趋零。因此 \(\widehat g\) 在 \(x=0\) 有 \(C^2\) 的非退化 Lorentz 延拓。

电磁二形式为 \(F=-GQ\,du\wedge dx\)。由
\[
Q_u\to-e\Im(\Phi\overline{\Phi'}),\quad
Q_x=-er^2\Im(\psi\bar h)\to-e\Im(\Phi\overline H),
\]
它有 \(C^1\) 延拓；\(\psi\) 有 \(C^1\) 延拓。边界是规则零超曲面，按第 4 节识别为唯一 AF 端的 \(\mathcal I^+\)。

在 (N13) 的 Bondi 归一化中，边界度量的交叉项是 \(2du_Bdx\)，且 \(du_B^2\) 系数及其 \(x\) 一阶导数在边界为零。因此边界生成线的 \(u_B\) 是该共形规范的仿射参数；\(u_B\to\infty\)，边界向未来完整。物理出射零线的仿射参数满足 \(ds/dr=G/C_0\)，故其物理仿射长度也无限。

每个实际点沿其出射线到达这个相同的 \(\mathcal I^+\)，所以整个最大未来发展属于 \(J^-(\mathcal I^+)\)，黑洞区为空。这里结论来自已构造的边界及逃逸线，不是由“没有陷俘球”直接替代。

## 9. Bondi 通量与零终态

有限 \(u\) 极限和 (N19)–(N20) 的一致收敛给
\[
\frac{dQ_B}{du}=-e\Im(\Phi\overline{\Phi'}),\qquad
\frac{dM_B}{du}=-\frac{|\Phi'|^2}{G_\infty}.
\tag{N23}
\]
此处 \(M_B=\lim m=\lim\varpi\)，因为 \(Q\) 有界且 \(r\to\infty\)。单位 Bondi 时间下质量通量为
\(dM_B/du_B=-|d\Phi/du_B|^2\)。不把 ADM 参数代入这些终态式。

最后对 \(u\ge1\)，整条实际出射面的 (N8) 使 A-RET01 的迟时内部界可用。**先固定出射面取 \(r\to\infty\)**：
\[
|Q_B(u)|\le C_e\epsilon^2(1+u)^{-1/3},\qquad
0\le M_B(u)\le
C_e\epsilon^2(1+u)^{-4/3}
+C_e\epsilon^4(1+u)^{-5/3}.
\tag{N24}
\]
再由 \(u\leftrightarrow u_B\) 的正上下界取晚时极限，得到
\[
M_f=Q_f=0.
\]
不存在参数极限与时间极限的交换，也不要求初始 ADM 质量或电荷为零。

## 10. 作用域与复算

本文件与 A-GEO01、A-RET01 合用，给 L006 小数据的完整零无穷远、每点逃逸、Bondi 极限及零终态的内部证明。共同规则标签下的局部衰减在 [A-SD01](SMALL_DATA_DISPERSION.md) 汇总。它们不提供目标 A 的正质量临界端点，也不把新入射大幅度扫描自动判为色散。

    python research/goal_a/verify_null_infinity_algebra.py

该脚本独立展开带电波算子，核对径向标量项抵消、Maxwell 兼容、电势号数及 Bondi 通量归一化；有限代数通过不认证全篇分析论证。
