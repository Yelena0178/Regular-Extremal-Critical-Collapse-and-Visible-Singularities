# VAR01：固定初始电荷的真实约束切向量及有限域变分接口

2026-11-08。解析证明稿 / INTERNAL_AUDIT；未独立评审。初值部分依赖 SHAPE01 的电荷算术包围；有限域部分为条件性接口，未认证向外形状的实际 PDE。

## 1. 精确参数族，不冻结初始几何

固定 SHAPE01 的 η=1/2、a(r)、ω(r)。令 A=a'+a/r，d=4/5，c=−4/5；给定两个固定光滑有界函数 α(r)、β(r)，令 dτ=d+τα、cτ=c+τβ。取 |τ|max(‖α‖∞,‖β‖∞)≤1/5。相位 θτ(r)=∫₁₀ʳ cτ ω，φτ=a exp(iθτ)，χτ=exp(iθτ)(−dτ A−iωa)。径向规范不变。

Qτ'=eωr²a² 与 τ 无关。Sτ=a'²+dτ² A²+(1+cτ²)ω²a²；fτ 满足 SHAPE01 的完整线性约束，kτ=r√fτ(dτ A a'+cτ ω²a²)，Πτ=√fτχτ。因为 |dτ|,|cτ|≤1，同一个 fτ≥(3/7)exp(−203) 成立，保留同一固定 X⁶ 中光滑合法初值族。α、β 的每阶导数在固定支撑上有界即可；在物质外相位辅助函数不影响零物质数据。

以下点表示 τ=0、固定面积半径 r 的导数。设 Θ=∫₁₀ʳ βω、s=2dα A²+2cβω²a²，则
\[
\dot Q=0,\quad
\dot f'+(1/r+rS)\dot f=-rf s,\quad\dot f(6)=0,
\]
\[
\dot f(r)=-\int_6^r t f(t)s(t)
\exp[-\int_t^r(1/\rho+\rho S(\rho))d\rho]dt.
\]
\[
\dot\phi=i\Theta\phi,\quad
\dot\chi=i\Theta\chi-\alpha A e^{i\theta},\quad
\dot\Pi=\frac{\dot f}{2\sqrt f}\chi+\sqrt f\dot\chi,
\]
\[
\dot k=r\sqrt f(\alpha A a'+\beta\omega²a²)
+\frac{r\dot f}{2\sqrt f}(d A a'+c\omega²a²).
\]
外部 \(\dot M_{ADM}=-7\dot f(14)\)、\(\dot f=-2\dot M/r\)。这些是实际约束族的导数，不是任意指定的独立场。

若 α≥0、β=0 则 s≥0，故 dot f≤0、dot M≥0；若 α=0、β≥0 则 s≤0，故 dot f≥0、dot M≤0。结论仅是初始几何/ADM；不推出终态方向。

## 2. 坐标反馈与初始相位代价

求解器初始坐标是 proper distance xτ(r)=∫₀ʳ fτ⁻¹/²dρ。于是
\[
\dot x(r)=-\tfrac12\int_6^r f^{-3/2}\dot f\,d\rho,
\qquad \dot r|_x=-\sqrt f\dot x.
\]
对任何初始量 Y，固定 x 的导数是 dot Y|r+Y_r dot r|x，不能直接把固定面积半径切向量送入原数值网格。固定 X⁶ 的族仍在面积半径 chart 中定义；此转换只为对齐求解器输入。

初始 Ω²=1，令 J=Q_v=e r²√f(1−c)ωa²/2，P_v=r f(1−c)²ω²a²/4。物质内部 J>0，有
\[
\dot J/J=\dot f/(2f)-\beta/(1-c),\quad
\dot P_v/P_v=\dot f/f-2\beta/(1-c)=2\dot J/J.
\]
这也来自精确恒等式 P_v=J²/(e²r³a²)。所以在固定 r,a 的初始点，降低出射相位聚焦必同时降低该点出射电荷流；δf 的改善也不能打破该关系。完整初始 Gauss 电荷仍保持，因为另一零方向电流随之改变。仅看 δS<0 就声称未来电荷输送提高并不成立。

## 3. 同一实际正半径有限域上的变分方程

采用既有 CH1：Y=(r,κ,θ,ν,z,m,φ,Q,A_u)，θ,z,φ 复数（12个实分量）；这里 θ=rD_vφ，与前两节的初始相位符号含义不同。以 R,K,T,N,Z,H,Φ,q,B 分别表示其参数导数。
令 f=1−2m/r，a_c=κ(2m−Q²/r)/r²，并定义
\[
F=-2H/r+2mR/r²,
\quad C=K(2m-Q²/r)/r²
+\kappa(2H-2Qq/r+Q²R/r²)/r²-2a_cR/r.
\]
直接微分 CH1 得
\[
R_u=N,\quad K_u=(K\nu+\kappa N)|z|²/r
+2\kappa\nu\Re(Z\bar z)/r-\kappa\nu|z|²R/r²,
\]
\[
T_u=-\delta(\kappa\nu fz/r)-ie\delta(\kappa\nu Q\phi/r)-ie(B\theta+A_uT),
\]
\[
N_v=C\nu+a_cN,
\quad Z_v=-T/r+\theta R/r²-Cz-a_cZ+ie\delta(\kappa Q\phi/r),
\]
\[
H_v=\delta(Q²\kappa f/(2r²))+\Re(T\bar\theta)/\kappa-|\theta|²K/(2\kappa²),
\quad \Phi_v=T/r-\theta R/r²,
\]
\[
q_v=eR\Im(\phi\bar\theta)+er\Im(\Phi\bar\theta+\phi\bar T),
\quad B_v=2\delta(\kappa\nu Q/r²).
\]
此处 δ 严格表示 Leibniz 线性算子：δr=R、δκ=K、δν=N、δf=F、δz=Z、δQ=q、δφ=Φ；例如 δ(κQφ/r)=KQφ/r+κqφ/r+κQΦ/r−κQφ R/r²。因此不是省略未知强迫。全部系数来自同一基准发展。

固定 u 射线前缀的必要反馈可直接写为
\[
\delta\Lambda=(fN-F\nu)/(4\nu²),\qquad\Lambda=-f/(4\nu),
\]
\[
\delta H_{cap}=\int h_{cap}\left(3R/r+K/\kappa+N/\nu\right)dv
+\int r³\Omega²\,2\Re(\Phi\bar\phi)dv,
\quad h_{cap}=r³\Omega²|\phi|²,
\]
因为 Ω²=−4κν。电荷变化为 q(v)−q(v₀)，不能设为零。幅度聚焦项的导数在 |φ|>0 处由 a=|φ|、δa=Re(Φ conjugate(φ))/a 计算；跨零点宜保留总 |D_vφ|² 而非除以 a。移动入口或移动事件还须加端点/射线位移项；不能把首次负样本的事件位置冻结成固定点定理。

## 4. 条件性有限域控制与未兑现接口

设实际参考解在 K=[0,U]×[0,V] 上存在，r≥r₀>0、κ≥κ₀>0、ν≤−ν₀<0，所有变量位于一个凸紧管；CH1 的实 Jacobian 行和范数≤L，二阶导数≤L₂。给同一特征边界上的相容 C² 参数数据。则微分积分方程得到上述线性 Volterra 系统。

取 γ=2L+1，以 exp(−γ(u+v)) 加权 sup 范数。每个分量只沿自己的方向积分，Jacobian 算子范数≤L/γ<1/2，故
\[
\|\delta Y\|_{\infty,K}\le2e^{\gamma(U+V)}\|\delta b\|_\infty.
\]
对真实解差商减去该线性解，Taylor 余项≤(L₂/2)|Yτ−Y₀|²，结合相同加权逆得 O(τ) 差商余项；边界二阶导数界、管余量与 L,L₂ 决定允许 τ。小扰动保持管内可由同一积分映射及延续论证，不把该条件反过来当作参考解存在证明。相容边界的 CH2 缺陷恒为零，微分后亦为零。

**目前未兑现**：SHAPE01 实际中心到该矩形边界的认证迹、全域正分母/变量管、有效 L/L₂ 和边界误差；也没有控制 r=0 的中心延续。故本节不能给向外候选的真实未来改善，不能声称已完成有限域认证或 A6。

## 5. 本轮判别与下一工作

新增初值切向量消除了“保持初始电荷就必须固定几何”的错误限制；点态相位代价恒等式同时排除免费增加出射电流的解释。有限域变分接口明确了真实 q、几何与坐标反馈，仍未提供改善方向。

不追加同类壳扫描。优先核对中心认证/特征迹能否为此候选提供第4节实际输入；若现有工具无法提供，则需要建立该误差接口或改变构造，而不是用初始 ADM 降低替代长期滞留。
