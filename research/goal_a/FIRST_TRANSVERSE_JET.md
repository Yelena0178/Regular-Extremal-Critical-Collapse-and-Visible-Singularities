# A-JET01：固定有限耦合下的一阶横向标量匹配

2026-10-16。内部定理与证明稿，未经外部独立数学审查。延续 A-HOR01，处理此前未消除的三个实残差。**本结果是光滑特征数据及一阶横向标量 jet 的存在论证，不是完整 RN 拼接、正则中心全未来或目标 A 临界族。**

## 1. 命题与有效性边界

固定 D001、\(e=3/5,R=5\)。存在 \(\beta_0,\eta_0>0\)，其中可取 \(\eta_0\le2^{-160}\)，使任意固定
\[
0<\eta<\eta_0,\qquad 0<\beta<\beta_0
\]
均有下述数据：光滑场 \(\phi\)，由终端 \(r(1)=R,r'(1)=0\) 求出的 Raychaudhuri 半径、从零起算的 Gauss 电荷、Minkowski 起点的 \(\nu\) 及 \(P=D_u\phi\)，满足
\[
Q(1)=R=5,\qquad P(1)=0,\qquad
r>5/8,\qquad H=-4r\nu>\beta/8192.
\tag{J1}
\]
有 \(r'\ge0\)，对仍有非零未来标量梯度的点严格为正；整个零锥没有严格陷俘球。所有纵向端点 jets 光滑匹配，且起点可接 A-HOR01 的 Minkowski 顶点帽。

对于固定正 \(\eta\)，调节参数可随 \(\beta\) 光滑选取；每个正 \(\beta\) 上，三个实残差对三个实调节量的 Jacobian 非退化。这里没有给出可计算的 \(\beta_0,\eta_0\)，也没有认证某个指定浮点根的区间盒。下面的存在结论来自明确极限 Jacobian 和隐函数定理，不来自数值残差小。

## 2. 一个不增加纵向电荷的修复方向

记 A-HOR01 第 4 节平滑后的早期场为 \(\psi_{\eta,s}(x)\)，定义域 \(0\le x\le1\)，两端全阶平坦。对 \(\eta=0\) 记原三段 C0 场为 \(\psi_{0,s}\)。固定
\[
g(y)=
\begin{cases}
\exp(4-[y(1-y)]^{-1}),&0<y<1,\\0,&\text{其余},
\end{cases}
\quad I_g=\int_0^1g(y)\,dy>0.
\]
取三个实未知量 \(z=(s,\Re W,\Im W)\)，并定义
\[
\phi(v)=
\begin{cases}
\psi_{\eta,s}(v/\beta),&0\le v\le\beta,\\
\beta Wg((v-\beta)/(1-\beta)),&\beta\le v\le1.
\end{cases}
\tag{J2}
\]
固定正 \(\eta,\beta\) 时它全局 \(C^\infty\)，包括接点 \(\beta\)。后段相位固定，所以
\[
\Im(\phi\overline{\phi'})=
\frac{\beta^2|W|^2}{1-\beta}\Im(gg')=0.
\tag{J3}
\]
它对 Gauss 电荷没有直接贡献，但不是没有能量；半径和先前充电效率会发生二阶变化，必须在同一个求解中保留。

## 3. 用固定区间 ODE 定义实际残差

令 \(f=r/R,\ q=Q/R\)。后段坐标为 \(y=(v-\beta)/(1-\beta)\)，半径满足
\[
f_{yy}=-\beta^2|W|^2(g')^2f,\quad
f(1)=1,\quad f_y(1)=0.
\tag{J4}
\]
其解、前端值 \(f_b=f(0)\) 和 \(p_b=f_y(0)\) 对 \(\beta,s,W\) 光滑，并且
\[
f=1+O(\beta^2),\quad p_b=O(\beta^2)
\tag{J5}
\]
于有界 W 集合一致。

早段坐标为 \(x=v/\beta\)，向过去解
\[
f_{xx}=-|\psi_{\eta,s,x}|^2f,\quad
f(1)=f_b,\quad f_x(1)=\frac{\beta}{1-\beta}p_b,
\]
\[
q_x=eR f^2\Im(\psi_{\eta,s}\overline{\psi_{\eta,s,x}}),
\quad q(0)=0,\quad q_f=q(1).
\tag{J6}
\]
注意最后半径导数为 \(O(\beta^3)\)，不是 O(β) 的自由项。后段 q 恒为 \(q_f\)。

早段 \(H=\beta\widehat H\)，其中
\[
\widehat H_x=1-q^2/f^2,\quad
\widehat H(0)=f(0)/f_x(0),\quad
\widehat\nu=-\widehat H/(4Rf).
\]
从 A-HOR01 的实际波输运条件得到
\[
\mathcal J_{\rm early}
=\beta J_{\rm early},\quad
J_{\rm early}=\int_0^1
 \left(\widehat\nu_x-\frac{ieq}{4f}\right)\psi_{\eta,s}\,dx .
\tag{J7}
\]
后段的 H 则为
\[
H(y)=\beta\widehat H(1)
+(1-\beta)\int_0^y(1-q_f^2/f^2)\,dt,\qquad
\nu=-H/(4Rf).
\]
因此精确地
\[
\mathcal J_{\rm late}=\beta C_{\rm late}W,\quad
C_{\rm late}=\int_0^1
\left(\nu_y-\frac{ieq_f(1-\beta)}{4f}\right)g\,dy.
\tag{J8}
\]
实际 \(P(1)\) 由 \(RP(1)=\mathcal J_{\rm early}+\mathcal J_{\rm late}\) 给出。定义缩放残差
\[
\mathcal E_{\beta,\eta}(s,W)=
\left(q_f-1,\ 
\Re[J_{\rm early}+C_{\rm late}W],\
\Im[J_{\rm early}+C_{\rm late}W]\right).
\tag{J9}
\]
所有积分在固定 x、y 区间；r 的正下界和 \(f_x(0)>0\) 在基准邻域内成立。式 (J4)–(J9) 本身也给 \(\beta=0\) 的辅助延拓，甚至可向小负 β 形式延拓以应用通常的隐函数定理。**β=0 不是一个实际光滑时空或 Cauchy 数据极限。**

## 4. 明确可逆的极限 Jacobian

先取 \(\eta=0\)。令
\[
k(s)=K\sqrt{(1-s)/s},\quad
K=\Phi\cos^2\Phi(1-\Phi^2)/2,\quad \Phi=1/2,
\quad s_0=\frac{9K^2}{1+9K^2}.
\]
于是 \(3k(s_0)=1\)，且 \(s_0\) 严格位于 A-HOR01 的认证区间内。
在 \(\beta=0\)，后段半径为一，早段即原基准：
\[
q_f=3k(s),\quad J_{\rm early}=J_0(s).
\]
**离开电荷零集时不能忽略后段的几何项。** 在此辅助极限上
\[
H(y)=(1-q_f^2)y,\quad
\nu_y=-\frac{1-q_f^2}{4R},
\]
故
\[
C_0(s)=
-\left(\frac{1-[3k(s)]^2}{4R}
+\frac{ie\,3k(s)}4\right)I_g.
\tag{J10}
\]
在电荷根处 \(C_*=C_0(s_0)=-ieI_g/4\ne0\)。
取
\[
W_0=-J_0(s_0)/C_*.
\]
该复数由有限显式积分定义，不要求预先认证它非零。

写 \(a=eI_g/4>0\)。极限对 \(z=(s,\Re W,\Im W)\) 的实 Jacobian 形如
\[
D_z\mathcal E_{0,0}=
\begin{pmatrix}
d&0&0\\
A&0&a\\
B&-a&0
\end{pmatrix},\quad
d=3k'(s_0)=-\frac1{2s_0(1-s_0)}<0.
\]
\[
\boxed{\det D_z\mathcal E_{0,0}=d\,a^2\ne0.}
\tag{J11}
\]
A、B 包含实际半径、H、电流对 s 的全部导数，不需要猜测它们的值，也没有将带电虚核丢掉。这里的相位可控性依赖非零背景电荷和耦合；中性系统不能用同一个论证。

## 5. 平滑化后的 C1 参数依赖：补充必要接口

A-HOR01 只证明了平滑化的 H1 小误差；单有该误差不能自动推出 Jacobian 连续。以下给出额外论证。

把 s 限制在 \(s_0\) 的一个小闭邻域。选一族光滑递增映射 \(v=F_s(t)\)，固定 0、1，把两个固定参考接点送到 \(v_1(s),v_2(s)\)，并在各接点的固定小邻域内恰为平移。可在接点间光滑插值；缩小 s 邻域后 \(F_s'\) 有统一正上下界，各有限阶参数导数有界。这个映射只用于证明参数依赖，不改变实际物理数据。

在固定 t 域，\(\psi_{0,s}\circ F_s\) 的折点固定。两边值对所有 s 相等，所以其 s 导数的值也相等；函数及 s 导数均属于 H1。故
\[
s\longmapsto\psi_{0,s}\circ F_s\quad\text{属于 }C^1(H^1).
\]
平滑层的截止函数在此坐标中不随 s 平移；接点值差及其 s 导数同为 \(O(|t-t_j|)\)。因此截止导数的 \(1/\eta\) 与这个一阶零点抵消，给
\[
\|\psi_{\eta,s}\circ F_s-\psi_{0,s}\circ F_s\|_{H^1}
+\|\partial_s(\psi_{\eta,s}\circ F_s
                  -\psi_{0,s}\circ F_s)\|_{H^1}
\le C\sqrt\eta.
\tag{J12}
\]
常数依赖固定 s 邻域，有限且不随 η 改变；端点 0、1 可令 \(F_s\) 恒等，论证相同。

例如拉回后的半径一阶系统为
\[
f_t=F_s' p,\qquad
p_t=-|\partial_t(\psi_{\eta,s}\circ F_s)|^2f/F_s'.
\]
其系数对 s 在 L1 中 C1；由 (J12)，系数及 s 导数一致收敛。在线性 ODE 的变分积分式上用有限区间 Gronwall，得半径解及参数导数收敛。Gauss、H 和 (J7) 的系数同样是 H1/C0 场及有界几何量的乘积，分母 r、\(f_x(0)\) 远离零，故其解及端点积分也 C1 收敛。对 β、W 的导数只改变光滑终端数据或后段 ODE，估计在有界邻域内一致。

这证明
\(\mathcal E_{\beta,\eta}\to\mathcal E_{\beta,0}\)
在基准附近按未知量 z 的 C1 范数收敛，且对 β 连续，满足带连续参数的隐函数定理所需条件。没有把移动折点的普通 H1 参数导数直接当作已经存在。

## 6. 三实残差的精确根与非退化性

由 (J11) 和上述 C1 收敛，存在 \(\beta_0,\eta_0>0\)，使小 β、η 的方程
\(\mathcal E_{\beta,\eta}=0\) 有唯一邻近分支
\[
s=s(\beta,\eta),\qquad W=W(\beta,\eta).
\]
它对 η 连续，对固定正 η 随 β 光滑；\(D_z\mathcal E\) 在该分支保持可逆。特别是
\[
q_f=1,\quad \mathcal J=\beta(J_{\rm early}+C_{\rm late}W)=0,
\]
从而 Q(1)=5、P(1)=0 精确成立。固定正 η 时，记 β=0 的电荷根为 \(s_\eta\)，则由 (J5)–(J6) 有
\[
s(\beta,\eta)-s_\eta=O(\beta^2),\qquad W=O(1).
\tag{J13}
\]

若原始残差取 \((Q/R-1,\Re\mathcal J,\Im\mathcal J)\)，其 Jacobian 行列式为
\(\beta^2\det D_z\mathcal E\)；若首项用 Q−R，再乘 R。因此每个正 β 的原始系统非退化，但逆界不在 β→0 时统一。这里 β 是先构造再冻结的辅助量，不是目标 A 的临界参数。

## 7. 约束余量不会被一阶修复耗尽

取 \(\eta_0\le2^{-160}\)。A-HOR01 在其光滑电荷根有 \(\widehat H>1/2048\)。
由 (J5)、(J6)、(J13) 及参数连续依赖，修复后的整个早段有
\[
\widehat H\ge1/4096,\quad
H(v)\ge\beta/4096,\quad0\le v\le\beta
\]
对足够小 β 成立。半径相对基准的改变为 \(O(\beta^2)\)，保持 \(r>5/8\)。

在后段，q=1 精确恒定，且 \(f=1+O(\beta^2)\)、f≤1。于是
\[
H(y)=H(\beta)+(1-\beta)\int_0^y(1-f^{-2})dt
\ge H(\beta)-C\beta^2.
\]
再缩小 \(\beta_0\)，得 \(H>\beta/8192\)。这是全区间解析估计，不依赖数值采样 H 的正号。因 r>0、\(|\phi'|^2\ge0\)、终端 r'=0，Raychaudhuri 积分给 r'≥0，因此没有在该零锥上制造严格陷俘球。

场的纵向平坦性和 P(1)=0 使 v≥1 延拓后的第一横向标量 jet 也为零。**更高横向 jets 并未被这三个条件消除**；正则中心的全未来和外部/视界邻域的 RN 收敛仍须另证。

## 8. 实际复算与未认证的量

    python research/goal_a/explore_first_jet.py
    python research/goal_a/verify_first_jet.py
    python -O research/goal_a/verify_first_jet.py

依赖固定在 [requirements-shooting.txt](requirements-shooting.txt)。代码在早段使用 C0 解析转移，在后段使用真正 C∞ bump；**未分辨正 η 的平滑层**，所以数值根不是上述光滑分支的区间根证书。正 η 的存在来自第 5–7 节。

[探索报告](FIRST_JET_EXPLORATION_2026-10-16.json) 的 β=0.01、0.003、0.001、0.0003 根都观测到三个缩放残差接近浮点舍入量，H 的采样最小值为正。独立 Gauss 积分、后段波输运的两种积分形式、既有基准横向矩、三档 ODE 容差和有限差分 Jacobian 见 [检查报告](FIRST_JET_CHECKS_2026-10-16.json)。辅助极限行列式数值约 −0.0124565；其严格非零来自 (J11)，不是有限差分。

尚无某个指定 β、η 的有效常数和区间根盒，不能声称报告中任一点已严格落入解析存在范围；不能将极小数值残差、正采样预算或一阶 jet 成功写成目标 A 完成。

## 9. 下一项实质任务

先处理第二及更高横向标量 jets 和相应几何/电磁匹配，控制多方向修复的共同预算。随后必须在同一实际正则中心发展上筛查有限时间严格陷俘，并实现完整 Cauchy 数据及色散邻侧。本结果没有把辅助 β→0 极限当成固定 X6 的临界端点；中心归一化仿射总时长在该极限可能发散，必须按实际正 β 分别计算。
