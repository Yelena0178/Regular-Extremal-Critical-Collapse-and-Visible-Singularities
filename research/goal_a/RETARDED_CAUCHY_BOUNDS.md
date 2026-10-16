# A-RET01：小数据的迟时内部质量、电荷界

2026-10-16。内部证明稿，未经外部独立数学审查。本文件在 Cauchy 片上积分 Gauss 和质量约束，不预设 Bondi 终态存在。用途：给 A-GEO01 的全时间电荷界，以及未来零无穷远构造后所需的零终态接口。

## 1. 假设与来源对应

在 D001 正则中心球对称解上，每张空间片的面积半径 \(r\) 从零严格增加至无穷；\(n,s,z,W\) 沿用 [A-GEO01](CAUSAL_COMPLETENESS.md)。假设
\[
0<c\le z\le C,\qquad |W|<z,\qquad |W|/z\le C.
\tag{R1}
\]
这里 \(c,C\) 不依赖时间。固定坐标标签 \(t\) 和 \(\rho\)，设
\[
q=t-R_*(t,\rho),\quad A=1+t+R_*,\quad B=1+|q|,
\quad -C\le\partial_rq|_t\le-c<0.
\tag{R2}
\]
要求 \(r\le CA\)。使用 \(q=t-R_*\)，与来源 \(q^*=R_*-t\) 符号相反。\(R_*\) 是来源带时间截止的径向坐标，**不是已经证明存在的几何光学函数**。

设 \(1/2<s<1<s_0\)，\(\mathfrak w(q)=1\) 对 \(q\ge0\)，对 \(q<0\) 取 \(B^{s-s_0}\)。假设
\[
|\phi|\le C\epsilon A^{-1}B^{1/2-s}\mathfrak w,\qquad
|\Pi|+|D_s\phi|\le C\epsilon A^{-1}B^{-1/2-s}\mathfrak w .
\tag{R3}
\]
这是 [Kauffman–Lindblad v2](https://arxiv.org/html/2109.03270v2) (10.17a,c) 在统一有界的坐标/规则框架变换后的零阶后果。球对称下无角向标量能量；所有场使用 D001 的一次固定归一化转换。可取
\[
\gamma=3/4,\quad s=2/3,\quad s_0=5/4,\quad
\mu=1/10,\quad0<\delta\le1/100.
\]
满足来源 Theorem 10.3 的全部严格指数不等式；\(s_0=\gamma+1/2\) 也与其耦合应用一致。实际小量另选使来源常数要求成立。

## 2. 两个精确径向约束与有限区间 Hardy 界

Gauss 和质量恒等式给
\[
Q_r=\frac e z r^2\Im(\phi\overline\Pi),\qquad
m_r=r^2\left(\varrho-\frac Wzj\right),\quad
\varrho=\tfrac12\left(|\Pi|^2+|D_s\phi|^2+\frac{Q^2}{r^4}\right).
\tag{R4}
\]
这里 \(j=-T(n,s)\)；\(Q(0)=m(0)=0\)。因 \(|j|\le\varrho\) 和 \(|W|<z\)，
\[
0\le m_r\le C\left[r^2(|\Pi|^2+|D_s\phi|^2)+\frac{Q^2}{r^2}\right].
\tag{R5}
\]

对任意有限 \(R>0\)，由中心 \(Q=O(r^3)\) 和分部积分，
\[
I_R:=\int_0^R\frac{Q^2}{r^2}\,dr
=-\frac{Q(R)^2}{R}+2\int_0^R\frac{QQ_r}{r}\,dr
\le2I_R^{1/2}\left(\int_0^RQ_r^2\,dr\right)^{1/2}.
\]
故
\[
I_R\le4\int_0^RQ_r^2\,dr
\le C e^2\sup_{0\le r\le R}(r^2|\phi|^2)
                   \int_0^Rr^2|\Pi|^2\,dr .
\tag{R6}
\]
外端边界项为负，不能错误地把它当成需要 \(Q(R)=0\) 的条件。

## 3. 全时间、全半径界

令 \(E_\phi(t,R)=\int_0^Rr^2(|\Pi|^2+|D_s\phi|^2)\,dr\)。
由 \(r/A\le C\)、\(|dr/dq|\le C\)，(R3) 给
\[
E_\phi(t,\infty)\le C\epsilon^2
\left[\int_0^\infty(1+q)^{-1-2s}dq
     +\int_0^\infty(1+v)^{-1-2s_0}dv\right]\le C\epsilon^2,
\]
\[
\int_0^\infty|Q_r|\,dr\le C|e|\epsilon^2
\left[\int_0^\infty(1+q)^{-2s}dq
     +\int_0^\infty(1+v)^{-2s_0}dv\right]\le C|e|\epsilon^2 .
\]
积分域从实际 \(q\in(-\infty,t]\) 扩大到整条实轴，只增加上界。特别是
\[
\sup_{t,r}|Q(t,r)|\le C|e|\epsilon^2,\qquad
\sup_{t,r}r^2|\phi(t,r)|^2\le C\epsilon^2.
\tag{R7}
\]
用 (R6)、(R5) 再得
\[
0\le m(t,r)\le C\epsilon^2+Ce^2\epsilon^4
\quad\hbox{对所有 }t,r.
\tag{R8}
\]
本证明不使用因果测地完备、Bondi 坐标或未来终态，故 (R7) 可先用于 A-GEO01。

## 4. 迟时内部改进

固定一个片上的点 \((t,R)\)，设其 \(q_R=t-R_*(t,\rho_R)\ge0\)。在整个 \(0\le r\le R\) 上 \(q\ge q_R\)，外区权重为 1。重复上述积分：
\[
E_\phi(t,R)\le C\epsilon^2(1+q_R)^{-2s},
\tag{R9}
\]
\[
|Q(t,R)|\le C|e|\epsilon^2(1+q_R)^{1-2s},
\quad
\sup_{r\le R}r^2|\phi|^2\le C\epsilon^2(1+q_R)^{1-2s}.
\tag{R10}
\]
这里用 \(2s>1\)，所以电荷积分的尾部可积。由 (R6) 的有限区间版本，
\[
\int_0^R Q^2/r^2\,dr
\le Ce^2\epsilon^4(1+q_R)^{1-4s}.
\]
于是
\[
0\le m(t,R)\le
C\epsilon^2(1+q_R)^{-2s}
+Ce^2\epsilon^4(1+q_R)^{1-4s}.
\tag{R11}
\]
取 \(s=2/3\)，分别得到电荷 \(O((1+q_R)^{-1/3})\)、标量质量 \(O((1+q_R)^{-4/3})\)、电磁积分质量 \(O((1+q_R)^{-5/3})\)。常数不随 \(t,R,q_R\) 改变，但可依赖固定模型、指数及小数据阈值。

## 5. 到零 Bondi 终态的准确剩余接口

若以后另证：

1. 存在正确识别的规则完整 \(\mathcal I^+\)，出射面有单位 Bondi 时间 \(u_B\)；
2. 该面向无穷远时面积半径 \(r\to\infty\)，且对于充分迟的 \(u_B\)，面上靠近无穷远的全部点满足
   \(q(t,\rho)\ge U(u_B)\ge0\)，其中 \(U(u_B)\to\infty\)；
3. 每个有限 \(u_B\) 的 Bondi 质量和电荷极限确实存在；

则由 (R10)、(R11) 及 \(\varpi=m+Q^2/(2r)\)，先固定 \(u_B\) 取 \(r\to\infty\)，再取 \(u_B\to\infty\)，得到
\[
Q_f=0,\qquad M_f=0.
\]
这是有明确未闭合前提的推论。**不把 \(q=t-R_*\) 直接叫作 Bondi 时间，也不交换两种极限。** 无穷远极限的存在性不能由 (R11) 的上界替代；真实出射线与 \(q\) 的关系必须利用其 ODE 和好度量分量另证。

本文件给的是实际 Cauchy 片内部的估计，允许初始 ADM 质量、电荷非零。它们在越来越远的辐射区保留，不与上述迟时内部界矛盾。也不提供未知正质量极端端点附近统一的辐射尾界。
