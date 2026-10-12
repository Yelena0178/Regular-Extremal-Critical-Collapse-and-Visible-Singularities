# RECCVS-L020：固定八阶领先剖面的精确符号与核单调性

2026-10-09。内部证明及计算证书。对象是形成构造的**领先阶辅助剖面**，不是已认证的有限振幅形成种子，也不是实际深中心解。

## 1. 全部参数固定

固定 K=8、n=88、σ=1/20，令

\[
 h(x)=x^{44}(x-176i)^{88}e^{(-1/20+i/4)x},\qquad
 z=\prod_{s=1}^{8}(\partial_x-s)h,
 \quad w=z/\sqrt{E_*},\quad
 E_*=\int_0^\infty |z'|^2dx.
\]

多项式 p 由 z=e^{(-1/20+i/4)x}p 定义，系数均为高斯有理数。`experiments/filtered_K8_n88_sigma1over20.json` 给出全部精确系数和有理积分；`freeze_filtered_profile.py` 从上述定义重新生成，未使用浮点求根。

记 E=|w'|²、C=Im(\bar w w')、λ=2∫E/∫C。精确有理运算给出

\[
 M_s(w)=\int_0^\infty e^{-sx}w(x)dx=0\quad(1\le s\le8),
 \qquad \frac12<\lambda<\frac{51}{100},
 \qquad 3<\int_0^\infty C<4,
\]

\[
 \int E=1,\qquad
 \mathcal K(0)=2\lambda\int e^{-x}C-\int e^{-x}E>2^{-854}.
\]

显示值为 λ≈0.5045578902627281、𝒦(0)≈1.2263458192940448×10⁻²⁵⁷；证明只使用精确分数及上面的有理比较。x=0 的 w 零阶为36，w'零阶为35。

## 2. 正电流的解析证明

初始 p 的根为0和176i。若 p 的根均在闭上半平面，滤波一步为 p'+(−1/20+i/4−s)p；在下半平面及实轴非根处，p'/p 的虚部非负，而零点方程要求其虚部为−1/4，矛盾。旧实根只能减少一重，故滤波后没有正实零点，全部根仍在闭上半平面。

因此对于 x>0，

\[
 \Im(w'/w)=\frac14+\sum_\rho\frac{\Im\rho}{|x-\rho|^2}\ge\frac14,
 \qquad C\ge\frac14|w|^2>0.
\]

特别地 ∥w∥₂²≤4∫C<16；这提供截断修复所需的 ∥w∥₂<4。

## 3. 一次变号的整数证书

令 l+ik=z'/z，J=λ[(1+2l)k+k']−l²−k²。写

\[
 D=|p|^2,\quad Y=p'+(-1/20+i/4)p,\quad E_p=|Y|^2,
 \quad C_p=\Im(\bar pY),\quad A_p=\Re(\bar pY).
\]

J 的正分母 D² 对应分子

\[
 N=\lambda[(D+2A_p)C_p+C_p'D-C_pD']-E_pD.
\]

N 的次数为528，原点因子为 x¹⁴²。移除该因子后，令 x=176u/(1−u)，把余下386次多项式紧化至[0,1]。其 Bernstein 系数可精确写成 N_j176ʲ/\binom{386}{j}，清除分母后全部为整数。

`certify_filtered_J.py` 通过整数 de Casteljau 二分及 Descartes 变号规则给出六叶证书：

| u 区间 | Bernstein 系数变号次数 | 两端符号 |
|---|---:|---|
| [0,1/32] | 0 | −,− |
| [1/32,1/16] | 0 | −,− |
| [1/16,1/8] | 0 | −,− |
| [1/8,1/4] | 0 | −,− |
| [1/4,1/2] | 1 | −,+ |
| [1/2,1] | 0 | +,+ |

端点都非零。变号次数0排除内部根；次数1给出至多一个根，而异号端点保证至少一个。故 J 在 x>0 恰有一个简单根 x_j，且从负变正；粗包络为176/3<x_j<176。证书含11个检查节点，覆盖全半线，未抽样遗漏尾部。

## 4. 从正性升级为单调性和端点最小值

定义

\[
 F=\int_0^x C,\quad P_E=\int_0^x E,\quad
 H=\lambda(F+C)-P_E.
\]

有 H'=|w|²J，H(0)=0、H(∞)=1。因此 H 先严格降后严格升，恰有一个由负变正的零点 x_h>x_j。

形成核满足

\[
 \mathcal K''-\mathcal K=-2H,\quad
 \mathcal K'(0)=\mathcal K(0)>0,\quad
 \mathcal K(\infty)=2,\quad \mathcal K'(\infty)=0.
\]

在[0,x_h]，只要𝒦>0就有𝒦''≥𝒦>0，所以不能首次触零；此后若有非正值，正的无穷远极限迫使出现非正内部最小值，但该点𝒦''=𝒦−2H<0，矛盾。这先证明𝒦>0。

在[0,x_j]，H≤0，故𝒦''>0、𝒦'>0。令 G=𝒦'，在[x_j,∞)有

\[
 G''-G=-2H'\le0,\qquad G(x_j)>0,\qquad G(\infty)=0.
\]

若 G 取负值，则它取得负的内部最小值，该点 G''−G>0，矛盾。因此 G≥0。x>x_j 时 H'>0，内部零最小值同样不可能，故实际 G>0。

得到此前没有量化的全半线余量：

\[
 \boxed{\mathcal K(x)\ge\mathcal K(0)>2^{-854}\quad(x\ge0).}
\]

此结论依赖此次固定剖面的精确一次变号证书，不宣称任意正电流剖面的核均单调。

## 5. 复算和范围

在项目根运行：

```bash
python experiments/freeze_filtered_profile.py --K 8 --n 88 --sigma 1/20 --output experiments/filtered_K8_n88_sigma1over20.json
python experiments/certify_filtered_J.py experiments/filtered_K8_n88_sigma1over20.json experiments/filtered_K8_n88_J_certificate.json
```

脚本仅使用 Python 标准库 Fraction 和整数运算。这里没有选定有限脉冲长度 m，没有验证非线性端点零点，没有运行时空演化。n=44试算的𝒦(0)<0，已明确拒绝，不能用其近似耦合值掩盖失去的余量。
