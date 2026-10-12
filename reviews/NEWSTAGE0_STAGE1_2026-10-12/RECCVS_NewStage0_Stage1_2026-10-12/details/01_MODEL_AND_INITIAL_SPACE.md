# 01｜统一模型、尺度与初值空间

**所有数学结论：GPT 主张，未经外部独立审查。** 定义是本轮提出并固定的工作规格；它们不构成目标解族的存在证明。

## 1. 方程与归一化

四维、签名 \((-,+,+,+)\)、球对称、单一复带电标量，标量质量与势为零、宇宙常数为零、磁荷为零。几何单位下取

\[
S=\int\sqrt{-g}\,[R-F_{ab}F^{ab}-2g^{ab}D_a\phi\overline{D_b\phi}]\,d^4x,
\quad F=dA,\quad D=\nabla+ieA,\qquad e=3/5.
\]

\[
G_{ab}=2(T^{EM}_{ab}+T^{SF}_{ab}),\quad D^aD_a\phi=0,
\quad\nabla_aF^{ab}=e\Im(\bar\phi D^b\phi),
\]
\[
T^{EM}_{ab}=F_{ac}F_b{}^c-\tfrac14g_{ab}F^2,
\quad T^{SF}_{ab}=\Re(D_a\phi\overline{D_b\phi})-\tfrac12g_{ab}|D\phi|^2.
\]

规范变换为 \(A\mapsto A+d\chi\)、\(\phi\mapsto e^{-ie\chi}\phi\)。标量和电势的坐标值不是规范不变量；\(r,Q,m_H,\varpi,F,|D\phi|\) 的几何定义须优先。

固定双零取向：未来 \(u,v\) 均增加，常 \(u\) 为出射面，

\[
g=-\Omega^2du\,dv+r^2d\omega^2,\quad g_{uv}=-\Omega^2/2,
\quad\nu=r_u,\ \lambda=r_v,\quad F_{uv}=\Omega^2Q/(2r^2).
\]

\[
m_H=\frac r2(1+4\Omega^{-2}\nu\lambda),\quad
\varpi=m_H+\frac{Q^2}{2r},\quad
1-\frac{2\varpi}{r}+\frac{Q^2}{r^2}=-4\Omega^{-2}\nu\lambda.
\]

\[
\begin{aligned}
\partial_v(\Omega^{-2}\lambda)&=-r\Omega^{-2}|D_v\phi|^2,\\
\partial_u(\Omega^{-2}\nu)&=-r\Omega^{-2}|D_u\phi|^2,\\
r_{uv}&=-\nu\lambda/r-\Omega^2(1-Q^2/r^2)/(4r),\\
Q_v&=er^2\Im(\phi\overline{D_v\phi}),\qquad
Q_u=-er^2\Im(\phi\overline{D_u\phi}),\\
\varpi_u&=-2r^2\Omega^{-2}\lambda|D_u\phi|^2+(Q/r)Q_u,\\
\varpi_v&=-2r^2\Omega^{-2}\nu|D_v\phi|^2+(Q/r)Q_v.
\end{aligned}
\]

标量波方程为
\[
(D_uD_v+D_vD_u)\phi+2\nu D_v\phi/r+2\lambda D_u\phi/r=0,
\quad [D_u,D_v]\phi=ieF_{uv}\phi.
\]
共形方程为
\[
(\log\Omega^2)_{uv}=-2\Re(D_u\phi\overline{D_v\phi})
+\Omega^2/(2r^2)+2\nu\lambda/r^2-\Omega^2Q^2/r^4.
\]
以上奇商直接公式仅用于 \(r>0\)；中心通过笛卡尔正则场和相容展开处理。\(\varpi\) 通量含带符号的电荷项，不可宣称在两个零方向都单调。

## 2. 固定尺度

一次性选择长度单位 \(\ell_0=1\)，所有参数成员用同一单位；更明确地说，物理耦合满足 \(e_{\rm phys}\ell_0=3/5\)。在本归一化中 \(r,M,Q\) 有长度量纲，\(e\) 有长度的倒数量纲，\(eM,eQ,Q/M\) 无量纲。标量无量纲，\(F\) 在正交框架中量纲为长度倒数。

固定初始渐近笛卡尔标签、中心正则标签、电荷方向、固定截断半径 \(R_{\rm ref}=2\ell_0\)。允许在各自时空中建立 Bondi/视界坐标，但必须按同一无穷远单位时间归一化，不允许随参数作时间伸缩来隐藏停留时间增长。中心时间取单位轴线固有时。

缩放 \(g\mapsto a^2g,A\mapsto aA,e\mapsto e/a,(M,Q,r)\mapsto a(M,Q,r)\) 连接不同单位表示。保持固定 \(e\) 时，不能给每个参数成员另外把 \(M_f\) 归一化为 1。旧形成成员的终端 \(r=Q=1\) 只属于那个指定构造，不成为新全族的定义。

## 3. 初值与约束

\(\Sigma\simeq\mathbb R^3\) 单端、空间完备，中心光滑，数据
\(\Psi=(\gamma,K,E,\phi_0,\Pi)\)，其中 \(K_{ij}=-g(\nabla_i n,e_j)\)、\(E_i=F(n,e_i)\)、\(\Pi=D_n\phi\)。电势在固定径向规范选代表，无磁场。

\[
\rho=\tfrac12(|E|^2+|\Pi|^2+|D_\Sigma\phi_0|^2),\quad j_i=-T(n,e_i),
\]
\[
R_\gamma+(\mathrm{tr}K)^2-|K|^2=4\rho,\quad
\nabla^j(K_{ij}-\gamma_{ij}\mathrm{tr}K)=2j_i,\quad
\mathrm{div}_\gamma E=e\Im(\phi_0\bar\Pi).
\]

正则中心要求径向标量有偶 Taylor 展开、电场 \(E=O(r)\)、\(Q=O(r^3)\)、\(m_H=O(r^3)\)、\(r/\text{径向固有距离}\to1\)。不插入点电荷，不预先假定中心有一个精确 Minkowski 开帽。旧基准的平直整锥要求是该基准的额外输入。

AF 条件：固定坐标中 \(\gamma-\delta=O(R^{-1})\)、一阶导数 \(O(R^{-2})\)、\(K=O(R^{-2})\)、电场 Coulomb 主项 \(Q_{\rm ADM}R^{-2}\partial_R\)；初批标量数据取共同紧支撑，之后如扩展须明确尾类。还要求 ADM 通量极限存在、物质能量有限。这些条件不由下述单一带权范数自动推出。

## 4. 统一强拓扑

固定 \(s=6,\delta=-1\)，沿用旧 D002 的权重约定，而非其他文献同名空间的约定：
\[
\|f\|_{H^k_\delta}^2=
\sum_{j=0}^k\int_{\mathbb R^3}(1+R)^{2(\delta+j)}|\partial^jf|^2dx.
\]
先用固定光滑截断扣除 ADM \(1/R\) 主项和 Coulomb \(1/R^2\) 主项，再分别用 \(H^6_{-1}\) 控制度量/标量，\(H^5_0\) 控制 \(K,E\) 的余项及 \(\Pi\)；把 \(M_{\rm ADM},Q_{\rm ADM}\) 作为单独的有限维参数。固定径向电势代表由其规范条件重建；若求解器显式演化电势，则另登记该代表的 \(H^6\) 预算。

例如面积半径型外区可用固定 \(\zeta(R)\) 和 \(n_i=x_i/R\) 的光滑主项模板
\(h^{ADM}_{ij}=2M_{ADM}\zeta(R)n_i n_j/R\)、
\(E_i^C=Q_{ADM}\zeta(R)n_i/R^2\)。模板只在固定外区起作用；其他 AF 坐标必须改用其相应主项，不能把各向同性坐标的模板直接套入面积半径坐标。

记满足上述约束、正则中心及 AF 条件的规范切片为 \(X^6\)，光滑数据子集为 \(X^\infty\)。目标是 \(p\mapsto\Psi_p\in X^\infty\) 在固定 \(X^6\) 拓扑中为 \(C^1\)。新路线候选初始片另外要求所有非中心球的初始膨胀一正一负；这仍不能代替“初始片在事件视界之外”的全局验收。共同初始强范数和椭圆下界要对构造出来的整条曲线另证。

旧增强 \(H^6\) 的 \(K,\Pi\) 抽取预算是更强的候选迹证据，不自动成为任意新曲线的已有性质。旧图函数 \(\psi_0\) 与新曲线端点数据 \(\Psi_{p=0}\) 是不同对象；本轮不把前者指定为后者。

## 5. 本轮适用性核验

作用量、Gauss 号数、双零 Maxwell 号数按旧 D001/D002 统一。零向量 \(k\) 满足
\(Ric(k,k)=2T^{EM}(k,k)+2|D_k\phi|^2\ge0\)。这支持有限陷俘筛选使用的零收敛条件，不能代替全局因果结构证明。

源文件：`sources/definitions/MODEL.md`。脚本复算只处理有限代数、范数模板与哈希；本文件的局部/全局分析适用性仍须按任务分别审查。
