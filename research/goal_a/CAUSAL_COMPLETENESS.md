# A-GEO01：球对称小数据发展的全部未来因果测地线完备性

2026-10-16。内部证明稿，未经外部独立数学审查。补充原 L006；不改写其历史正文。这里证明一个几何判据，并核对 Kauffman–Lindblad 小数据解的适用接口。它不构造目标 A 的临界族，也不单独证明完整零无穷远。

## 1. 几何判据与量词

采用 D001 的 Einstein–Maxwell–无质量带电标量方程。设光滑球对称发展有全局规则笛卡尔图
\((t,x)\in[0,\infty)\times\mathbb R^3\)，中心光滑，\(\rho=|x|\)，面积半径为 \(r\)。要求：

1. \(dt\) 是时间样协向量，所有未来因果向量满足 \(dt>0\)、\(|dx/dt|\le C\)；笛卡尔 Christoffel 系数全局有界。每个有限时间、有限坐标半径区域均在实际光滑发展中。
2. \(c\rho\le r\le C\rho\)。在每个时间片，令 \(n\) 为未来单位法向，\(s\) 为单位向外径向向量，
   \[
   z=s(r)>0,\qquad W=-n(r),\qquad
   \mathfrak d=|\nabla r|^2=z^2-W^2=1-\frac{2m}{r}.
   \]
   有 \(z,|W|\le C\)、\(\mathfrak d\ge d>0\)。轨道空间 Kodama 向量 \(K\) 取未来方向，满足 \(g(K,K)=-\mathfrak d\)、\(K(r)=0\)，且 \(0<K^t\le C\)。
3. 对 \(r\ge1\)，\(|Q|/r\le B\)，常数对整个未来成立。
4. 对每个固定 \(R\)，
   \[
   \int_0^\infty\sup_{|x|\le R}|\Gamma(t,x)|\,dt<\infty.
   \tag{G1}
   \]

这些是一个解的全未来估计；并非声称未知近临界族具有相同的常数。结论：**每条未来不可延零测地线的仿射长度、每条未来不可延类时测地线的固有时均无限。**

## 2. Hawking 质量的非负性

记 \(\varrho=T(n,n)\)、\(j=-T(n,s)\)，其中 \(T=T_{\rm EM}+T_{\rm SF}\)，D001 给 \(G=2T\)。球对称质量恒等式为
\[
s(m)=r^2(z\varrho-Wj).
\tag{G2}
\]
由主导能量条件 \(|j|\le\varrho\)、\(z>|W|\)，右端非负。沿时间片从正则中心 \(m=0\) 积分，得到 \(m\ge0\)。不使用重整化质量在两个零方向均单调这种错误假设。

## 3. 测地线的精确半径加速度

在任一正半径双零小图，
\[
g=-\Omega^2du\,dv+r^2d\omega^2,\quad
\nabla^2_{uu}r=-r|D_u\phi|^2,\quad
\nabla^2_{vv}r=-r|D_v\phi|^2,
\]
\[
r_{uv}=-\frac{\Omega^2m}{2r^2}
             +\frac{\Omega^2Q^2}{4r^3}.
\]
设测地线以 \(a\) 参数化，\(\kappa=-g(\dot\gamma,\dot\gamma)\)；类时取固有时所以 \(\kappa=1\)，零线取仿射所以 \(\kappa=0\)。由旋转 Killing 场守恒，
\(\ell^2=r^4|\dot\omega|^2\ge0\) 为常数，且
\(\Omega^2\dot u\dot v=\kappa+\ell^2/r^2\)。

完整时空 Hessian 的角向项为
\(\mathfrak d\,\ell^2/r^3\)。故精确地
\[
\ddot r=
-r\bigl(|D_u\phi|^2\dot u^2+|D_v\phi|^2\dot v^2\bigr)
-\frac{\kappa m}{r^2}+\frac{\kappa Q^2}{2r^3}
+\frac{\ell^2}{r^3}
 \left(1-\frac{3m}{r}+\frac{Q^2}{2r^2}\right).
\tag{G3}
\]
此式只在 \(r>0\) 使用；穿轴延续在笛卡尔图中处理。特别是 \(m\) 为 Hawking 质量。RN 中 \(m=M-Q^2/(2r)\)，(G3) 化为
\[
\ddot r=-\frac{\kappa M}{r^2}+\frac{\kappa Q^2}{r^3}
+\frac{\ell^2}{r^3}
 \left(1-\frac{3M}{r}+\frac{2Q^2}{r^2}\right),
\]
与 RN 有效势的独立微分一致。

对 \(r\ge1\)，(G2)、(G3) 和假设 3 给单侧上界
\[
\ddot r\le C_{\kappa,\ell,B}
:=\frac{\kappa B^2}{2}+\ell^2\left(1+\frac{B^2}{2}\right).
\tag{G4}
\]
负的标量聚焦项不需要另加绝对值估计。

## 4. 有限参数终点的穷尽排除

反设某条不可延未来因果测地线有有限 \(a_*<\infty\)。令 \(y=dt/da>0\)、\(V=d\gamma/dt=(1,dx/dt)\)。测地线方程给
\[
\frac{d\log y}{dt}=-\Gamma^0_{\alpha\beta}V^\alpha V^\beta,
\qquad
|\dot y|\le C_1y^2.
\tag{G5}
\]

**先证明 \(t\to\infty\)、\(y\to\infty\)。** 若 \(t\) 有限，因果速度界使位置留在有限坐标紧域；(G5) 在有限 \(t\) 区间控制 \(y\)，位置和速度都有有限极限，光滑测地线 ODE 可延续，矛盾。

若存在 \(a_n\uparrow a_*\) 及 \(y(a_n)\le H\)，由 Riccati 比较，在
\(a-a_n<(2C_1H)^{-1}\) 内 \(y(a)\le2H\)（\(C_1=0\) 时直接成立）。充分大的 \(n\) 覆盖余下有限参数区间；于是 \(t(a)\) 有限，仍矛盾。因此 \(y\to\infty\)。

**第一种情形：半径最终有界。** 由 \(r\asymp\rho\) 和 (G1)，(G5) 的右端沿该线对 \(t\) 可积，故 \(y\) 有有限正上下界。这与 \(y\to\infty\) 矛盾。

**第二种情形：半径无界，但不趋向无穷远。** 存在固定 \(r_0>0\) 和任意接近 \(a_*\) 的返回点 \(r\le r_0\)。无界性给穿插其中的 \(r>2r_0\) 点，故可取一列内部最大值点 \(a_n\uparrow a_*\)，其 \(r(a_n)\ge r_0\)、\(\dot r(a_n)=0\)。

在这样的转向点，测地线的轨道投影垂直于 \(\nabla r\)，所以
\[
\dot\gamma_{\rm orb}
=\sqrt{\frac{\kappa+\ell^2/r^2}{\mathfrak d}}\,K,\qquad
y=K^t\sqrt{\frac{\kappa+\ell^2/r^2}{\mathfrak d}}
\le C\sqrt{\frac{\kappa+\ell^2/r_0^2}{d}}.
\tag{G6}
\]
零线若 \(\ell=0\)，转向点本来就不可能；其他情形 (G6) 给有界 \(y\) 子列，矛盾。

**第三种情形：\(r\to\infty\)。** 从某个 \(a_0\) 起 \(r\ge1\)，积分 (G4) 两次：
\[
r(a)\le r(a_0)+\dot r(a_0)(a-a_0)
                +\tfrac12C_{\kappa,\ell,B}(a-a_0)^2.
\]
有限 \(a_*\) 使右端有界，矛盾。三种情形穷尽，判据得证。

## 5. Kauffman–Lindblad 小数据接口

来源固定为 [arXiv:2109.03270v2](https://arxiv.org/html/2109.03270v2)，Theorem 11.1、(12.12)–(12.13)、(13.2)–(13.3) 和 Theorem 1.1 的 (1.32)。只调用原 L006 已构造并转换到来源数据空间的光滑小振幅族。取足够小的数据量 \(\epsilon_{\rm KL}\)，使其增长指数 \(\delta<1/100\)。

- 全局 \(C^0\) 小量控制给统一因果锥、\(dt\) 时间样和 \(r\asymp\rho\)。小数据图由球对称数据及旋转相容规范得到，不能只从一般非球对称结论假设面积半径存在。
- 对球对称逆度量，在单位欧氏切向量上写
  \(g^{AB}_{\rm tangent}=b(t,\rho)\delta^{AB}\)，则
  \(r=\rho b^{-1/2}\)。好角向迹导数 (1.32)，加上扣除的质量主项，给
  \[
  |b-1|+\rho(|b_t|+|b_\rho|)\le C\epsilon_{\rm KL}.
  \]
  这里完整 \(b\) 包含质量主项；该主项的截止支撑远离轴，\(\rho|\partial b_0|\) 一致小。于是 \(r_\rho=1+O(\epsilon_{\rm KL})\)、\(r_t=O(\epsilon_{\rm KL})\)，从而 \(z=1+O(\epsilon_{\rm KL})\)、\(W=O(\epsilon_{\rm KL})\)、\(\mathfrak d\ge1/2\)。
- 在轨道图中 \(K^t=r_\rho/\sqrt{-\det g_{\rm orb}}\)，有统一正上下界。(12.13) 加质量主项给全局有界的笛卡尔 \(\Gamma\)。固定 \(\rho\le R\) 时，晚时质量截止为零，且 \(q^*\asymp-t\)，故
  \[
  \sup_{\rho\le R}|\Gamma|\le C_R\epsilon_{\rm KL}(1+t)^{-2+\delta},
  \]
  有限早时区由光滑性补足 (G1)。不在全外锥上声称 \(\Gamma\) 对时间绝对可积。
- [A-RET01 §3](RETARDED_CAUCHY_BOUNDS.md) 由 Gauss 约束和标量点态界直接给所有时间的 \(\sup_r|Q|\le C_e\epsilon_{\rm KL}^2\)。这一步不使用当前判据或零无穷远，所以无循环。

因此原 L006 的充分小成员满足全部假设，**全部未来因果测地线完备**。这比原文的径向/最终内锥结论更强；仍不把它自动登记为完整色散 \(D\)。

## 6. 与最大未来发展的识别

统一因果锥和全时间图使每个 \(t\) 片为 Cauchy 片：不可延因果曲线若在图的内部有有限时间端，则因果速度界给有限空间端，局部因果延续排除这一端。用初始数据的局部解把图向过去延长一个小开时间条带，得到无边界的光滑全局双曲时空，未来完备性不受影响。

[Galloway–Ling–Sbierski, arXiv:1704.00353, Theorem 3.6](https://arxiv.org/pdf/1704.00353) 的单向版本说明：光滑全局双曲且未来类时测地完备的时空，在任何 \(C^0\) 延拓中没有未来边界。只调用这一单向结论；不声称这里已证明过去完备。

局部唯一性把该解嵌入相同数据的最大整体双曲发展。若最大未来发展还含图以外的未来点，从该点向过去连接初始片的类时曲线会给嵌入图的未来边界，与上一定理矛盾。因此图已覆盖最大未来发展。该步骤没有借未构造的 \(\mathcal I^+\) 识别黑洞。

## 7. 验收限度与复核

新增闭合的是小数据接口中的全部因果完备和未来最大性。尚需：规则完整 \(\mathcal I^+\) 的构造、每点逃逸到同一 \(\mathcal I^+\)、Bondi 极限、工作标签下的完整局部衰减接口。目标 A 的极端端点、邻侧连接和真正形成更未取得。

后续补充：[A-NULL01](SMALL_DATA_NULL_INFINITY.md) 与 [A-SD01](SMALL_DATA_DISPERSION.md) 已为同一小数据接口写出上述零无穷远、Bondi 及局部衰减的内部证明；仍待独立数学复核，不延伸到未知临界族。

    python research/goal_a/verify_causal_algebra.py

该标准库脚本验证 (G3) 的轨道/角向组合、RN 有效势独立核对及错误质量替换的拒绝；不把有限代数复算当作上述分析证明或外部审查。
