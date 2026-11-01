# A-EVOL03：中性双零演化及已知解基准

2026-10-16。方法与数值证据均属 **E0**；不提供连续 PDE 误差证书。原 L001–L023 不改写。

## 1. 同一模型的精确中性子系统

固定 D001 和 e=3/5。在电荷为零、标量经常相位旋转为实数的区域，取电磁势为零；Maxwell 电流精确为零，这给带电模型的中性实标量子系统。设

\[
g=-e^Sdu\,dv+r^2d\omega^2,\quad \psi=r\phi,\quad
\nu=r_u,\ \lambda=r_v,\quad
m=\frac r2(1+4e^{-S}\nu\lambda).
\]

D001 的球对称方程化为

\[
(r^2)_{uv}=-\frac{e^S}{2},\qquad
A:=\frac{r_{uv}}r=-\frac{\nu\lambda+e^S/4}{r^2}
                  =-\frac{e^Sm}{2r^3},
\tag{N1}
\]
\[
\psi_{uv}=A\psi,\qquad S_{uv}=-2\phi_u\phi_v-2A.
\tag{N2}
\]

另两条 Raychaudhuri 方程

\[
r_{uu}-S_ur_u+r\phi_u^2=0,\qquad
r_{vv}-S_vr_v+r\phi_v^2=0
\tag{N3}
\]

留作独立数值残差检查。它们不是由数值上显式强制满足得到的零残差。

未来零法向取 L=2e^{-S/2}∂v、L̄=2e^{-S/2}∂u，g(L,L̄)=−2，则
θout=4e^{-S/2}λ/r、θin=4e^{-S/2}ν/r。正半径处双负号才是本次筛选关注的量。

## 2. 离散方法和中心作用域

[neutral_characteristic.py](neutral_characteristic.py) 在等步长双零网格上对 (r²,S,ψ) 作菱形单元积分与局部 Picard 迭代。单元内 e^S 使用四角 e^S 的算术平均。报告记录实际完成的 u、迭代末差、停止原因；人为 lapse/迭代 guard 触发仅表示计算停止。

规则轴为 u=v。用 t=(u+v)/2、x=(v−u)/2，r 是 x 的奇函数，φ、S 为偶函数。轴线上 e^{S/2}=r_x。L016 给 m/r³→|Dτφ|²/6，故

\[
A|_\Gamma=-\phi_u\phi_v/3.
\tag{N4}
\]

轴线的 r_x 与 φ 由同一 t 的 x=h、2h 样本作偶奇 Taylor 外推。一般基准默认在 k=ceil(√N) 个单元中使用 (N4)，物理宽度 kh/2→0；对光滑精确解，替代 A 的误差为 O(x²)。这只是局部一致性说明，**不是**包含该轴线闭合的稳定性或收敛定理。

候选的 [A-SCREEN01](NEUTRAL_CAUSAL_SCREEN.md) 使用另一种模式：若初始锥在 v≤Vcap 精确 Minkowski，且全部演化 u<Vcap，则这一区域直接填入精确真空解，并将中心近似单元数设为零。报告的 axis_closure_cell_iterations 必须为零；筛选信号不依赖上述 Taylor 轴线近似。

## 3. 平直波与收缩 FLRW 的独立比较

固定几何的平直波基准：r=(v−u)/2、S=0、ψ=F(v)−F(u)，F 为支持在 (2,4) 的显式光滑 bump。演化到 u=4.4，包含波穿越轴线；轴线精确 φ=2F′(u)。该基准仅检验波与中心处理，不能检验引力回授。

全耦合比较使用收缩平直 FLRW 的精确解：

\[
b=1-t/T_0,\quad a=\sqrt b,\quad r=ax,\quad
S=\log b,\quad\phi=\frac{\sqrt3}{2}\log b,\quad T_0=4.
\tag{N5}
\]

直接求导给 ν=(−a+a′x)/2、λ=(a+a′x)/2、a′=−1/(2T₀a)。代入 (N1)–(N3) 成立。其轴线 m/r³=1/(8T₀²b³)，t=2 时为 1/16。λ<0 等价于 u+3v>4T₀，ν始终负；因此可用已知严格陷俘点测试符号提取。**这个基准不渐近平坦，不是目标 A 候选。**

数值域 v≤4.8、u≤2.4，最晚 t=3.6<T₀；固定比较点 (2.2,4.7) 在精确光滑区域中陷俘。N=96/192/384 的最大误差为：

| N | r | S | φ | t=2、r趋零的 m/r³ 数值 |
|---|---|---|---|---|
| 96 | 1.14e−5 | 2.55e−4 | 3.56e−5 | 0.06243851 |
| 192 | 2.95e−6 | 6.44e−5 | 8.73e−6 | 0.06245776 |
| 384 | 7.57e−7 | 1.62e−5 | 2.15e−6 | 0.06247125 |

场误差约二阶，但中心 m/r³ 的误差仅缓慢下降，**不声称其二阶**。独立两条约束的最大残差下降；最细固定陷俘点 θout≈−0.5885、θin≈−9.218。平直 ψ 误差在舍入尺度。

初试的“固定四格中心闭合＋e^S 几何平均”版本被中心质量系数拒绝：N=96/192 时 m/r³约0.06505/0.06509，而精确值0.0625。点值场误差看似下降不能掩盖这约4%的中心系数偏差；失败对照保留在报告中。

## 4. 复算与尚缺的结论

    python research/goal_a/verify_neutral_characteristic.py
    python -O research/goal_a/verify_neutral_characteristic.py

依赖 [requirements-shooting.txt](requirements-shooting.txt)。[报告](NEUTRAL_CHARACTERISTIC_RESULTS_2026-10-16.json) 含源文件哈希、全部基准、约束残差与失败对照。通过仅说明这些已知解比较和显式数值检查通过。未给非线性稳定性、连续解误差、全中心未来、完整 I⁺、实际候选陷俘或目标 A 证书。
