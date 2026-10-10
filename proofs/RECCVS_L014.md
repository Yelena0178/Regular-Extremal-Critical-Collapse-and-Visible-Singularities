# RECCVS-L014：整个实际中心余域的体积、聚焦权重与轴线寿命

2026-10-09。D001；项目内部证明稿，尚待独立复核。该证明作用于整个实际余域，不假定深中心未陷俘，也不预设中心永久存在。

## 1. 可直接验证的外边输入

设同一实际发展含固定出射外边U=b>0、全部t≥1，满足
\[
 0<r_b(t)\le R\le1,\quad \lambda_b(t)\ge0,\quad
 r_b\lambda_b\le C_b t^{-2},\quad
 \alpha_b(t)/t^2\longrightarrow h_b>0.
\tag{L014.1}
\]
且α_b≥a₀>0。L013非零情形可取b=η；L015还给实际存在电真空空隙时的另一条合法外边。固定R、C_b、h_b及晚时阈值T_b，仅依赖固定解。

令D_b为每个t上从U=b开始的**实际连通入射正半径段**之并。右端可以是正则中心、奇异/其他未来边界或无穷坐标端；下面第一部分不指定它。对每个实际前缀，入射约束给
\[
 \alpha(U,t)\ge\alpha_b(t),\quad
 \nu=-\alpha\Omega^2<0,\quad 0<r(U,t)\le r_b(t).
\tag{L014.2}
\]
这包含实际黑洞内的全部更深点；连通性和全局标签使用I001已审计的入射段性质，不添加第二份中心填充。

## 2. 全余域有限体积：无需中心边界条件

对任意实际前缀[b,U]，
\[
 \int_b^U\Omega^2(x,t)dx
 =\int_b^U\frac{-\nu(x,t)}{\alpha(x,t)}dx
 \le\frac{r_b(t)-r(U,t)}{\alpha_b(t)}
 \le\frac R{\alpha_b(t)}.
\tag{L014.3}
\]
对实际段作单调穷尽，并用t≥T_b时α_b≥h_bt²/2，得到
\[
 \boxed{\int_{T}^{\infty}\int_{D_b(t)}\Omega^2dUdt
 \le\frac{2R}{h_bT}\quad(T\ge T_b).}
\tag{L014.4}
\]
早期[1,T_b]部分≤R(T_b−1)/a₀。四维体积元为(Ω²r²/2)dUdt dω，因此
\[
 \operatorname{Vol}_4(D_b)\le2\pi R^2
                      \iint_{D_b}\Omega^2dUdt<\infty.
\tag{L014.5}
\]
面积半径、陷俘符号和末端正则性均未被预设。体积常数随h_b↓0可发散；没有参数一致性的结论。

## 3. 入射段仍以正则中心结束时：全深部电磁积分与半径控制

这里只对实际终端为正则中心Γ(t)的截面陈述，不能将非正则边界的rλ项置零。正则中心给rλ→0、Q=O(r³)、m=O(r³)。半径混合方程等价于
\[
 (r\lambda)_U=\frac{\Omega^2}{4}(Q^2/r^2-1).
\tag{L014.6}
\]
设V(t)=∫_b^{U_Γ(t)}Ω²dU。积分到实际中心，精确得到
\[
 \boxed{\int_b^{U_\Gamma(t)}\Omega^2\frac{Q^2}{r^2}dU
       =V(t)-4r_b\lambda_b\le V(t)
       \le\frac R{\alpha_b(t)}.}
\tag{L014.7}
\]
不要求深部λ≥0。对截面上的任意实际U，两种非负积分的前缀分别不超过V(t)，故
\[
 |r\lambda(U,t)|\le r_b\lambda_b+\frac{V(t)}4
 \le\frac{C_*}{t^2}\quad(t\ge T_b).
\tag{L014.8}
\]
在V=−1/t规范，因∂_V=t²∂_t，得到全深部
\[
 |\partial_V(r^2)|=2t^2|r\lambda|\le2C_*.
\tag{L014.9}
\]
这是加权半径的绝对值界，不是λ的正号。若所有晚时截面仍到正则中心，则每条一直存在的固定U线上r²有晚时极限；这里不额外声称联合U连续性、中心曲率有界或完整场方程延拓。若入射截面先遇非正则终端，L014.7必须保留其4r_endλ_end项，不能继续调用上述中心结论。

## 4. 中心固有时间：一个精确全局接口

正则中心满足
\[
 \Delta=1-2m/r=-4\Omega^{-2}\nu\lambda=4\alpha\lambda
 \longrightarrow1.
\]
若Γ写为U=U_Γ(t)，由dr|_Γ=0，
\[
 U_\Gamma'(t)=\frac{\lambda_\Gamma}{-\nu_\Gamma},\qquad
 \left(\frac{d\tau_\Gamma}{dt}\right)^2
     =\Omega_\Gamma^2U_\Gamma'
     =\frac{\lambda_\Gamma}{\alpha_\Gamma}.
\]
因此，不依赖轴线坐标斜率的恒等式是
\[
 \boxed{\frac{d\tau_\Gamma}{dt}=\frac1{2\alpha_\Gamma(t)},
 \quad\lambda_\Gamma=\frac1{4\alpha_\Gamma}.}
\tag{L014.10}
\]
中心属于D_b(t)时，α_Γ≥α_b。对任意实际正则中心段T≤t<t_end、T≥T_b，
\[
 \boxed{\tau_\Gamma(t)-\tau_\Gamma(T)
 \le\int_T^t\frac{ds}{h_bs^2}
 \le\frac1{h_bT}.}
\tag{L014.11}
\]
允许t_end有限或无限。若轴线保持正则至t=∞，它仍有有限未来固有长度。球对称轴线的单位切向加速度被全部空间旋转固定，只能为零；所以轴线是四维类时测地线，有限固有长度给类时测地线不完备。

这一推论不等于曲率奇点。MGHD中的有限参数边界可能是可延拓的Cauchy边界，必须另证曲率发散或指定正则性的不可延拓性。它也不是用户目标C要求的有限**零测地线仿射**曲率端点。

## 5. 能调用的正半径延续与不能调用的结论

Kommemi，arXiv:1107.0949v2，Theorem1.8/§4：若候选p与实际q形成D=(J⁺(q)∩J⁻(p))\{p}⊂Q⁺，且该整个D上0<r₀≤r≤R、体积有限，则p仍为实际常规点。L014.4–5提供其中的体积接口，不要求无陷俘。

但必须保留D\{p}全在实际发展和紧实际初始边的条件。一个已有Cauchy视界片的过去零边可能含其他非实际边界点，不能仅凭有限体积和正半径将它抹掉。r→0中心端点更不满足r₀条件。

全聚焦的剩余关键量仍是L011：
\[
 \Omega^{-2}\lambda=B(U)
  -\int_{\tau_0(U)}^t r\Omega^{-2}|T|^2ds.
\tag{L014.12}
\]
本引理不给右侧正号，也不给r→0的P、T或曲率强界。它排除了“外边增长不能传到深中心”和“还须先假定深中心无陷俘才能控制其体积”的障碍，未闭合整个域的未陷俘性或可见奇点。
