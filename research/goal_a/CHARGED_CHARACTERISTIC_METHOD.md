# A-CHG01：带电、规则视界特征系统及当前候选的有限域探索

2026-10-17。内部推导与 E0 实验，未经外部独立审查。有限代数和已知解比较通过，不代表新候选的连续 PDE 误差已经认证。

## 1. 与 D001 同号数的十二实变量

取 Aᵥ=0、r>0、ν<0、κ=−Ω²/(4ν)>0，定义

\[
 \theta=rD_v\phi,\quad z=rD_u\phi/\nu,
 \quad f=1-2m/r,\quad a=\kappa(2m-Q^2/r)/r^2.
\]

m 是 Hawking 质量。以 r、κ、θ 的四个实分量沿 u 输运，其余八个实分量沿 v 输运：

\[
 r_u=\nu,\quad\kappa_u=\kappa\nu|z|^2/r,
\]
\[
 \theta_u=-\kappa\nu fz/r-ie\kappa\nu Q\phi/r-ieA_u\theta,
\]
\[
 \nu_v=a\nu,\quad z_v=-\theta/r-az+ie\kappa Q\phi/r,
\]
\[
 m_v=Q^2\kappa f/(2r^2)+|\theta|^2/(2\kappa),
 \quad\phi_v=\theta/r,
\]
\[
 Q_v=er\Im(\phi\bar\theta),\quad
 \partial_vA_u=2\kappa\nu Q/r^2.
\tag{CH1}
\]

θᵤ与 zᵥ 的电磁虚部符号相反；这是 D001 交换子与波方程之和的结果。不能把 (rDᵤφ)ᵥ 的电磁符号同时用于 Dᵤ(rDᵥφ)。质量方程还含 Q²λ/(2r²)，直接套中性质量公式会漏掉电磁应力。

## 2. 约束传播与实际 Einstein 系统接口

不预设缺陷为零，定义

\[
 E=r_v-\kappa f,\quad
 G=m_u-Q^2\nu/(2r^2)-f\nu|z|^2/2,
\]
\[
 C=Q_u+er\nu\Im(\phi\bar z),\qquad
 S=D_u\phi-\nu z/r.
\]

从 (CH1) 直接求导，得到齐次系统

\[
 E_u=2\kappa G/r,
\]
\[
 G_v=-\kappa Q^2G/r^3
 +\{Q^2\nu/r^3-m\nu|z|^2/r^2\}E
 +Q\kappa fC/r^2,
\]
\[
 C_v=e\nu\Im(\phi\bar z)E+er\Im(S\bar\theta),
 \qquad S_v=\nu zE/r^2.
\tag{CH2}
\]

若 u=0 的出射边 E=0，另一条入射边 G=C=S=0，有限正半径矩形上有界系数的 Volterra 唯一性给全部缺陷为零。于是 φ 的两方向共变导数、Maxwell 方程、质量约束及半径方程相容。Ω²=−4κν 的共形 Einstein 方程也由

\[
 (\log\Omega^2)_{uv}
 =-2\nu\Re(z\bar\theta)/r^2
  -4\kappa m\nu/r^3+4\kappa\nu Q^2/r^4
\]

恢复。以上五个恒等式由精确复 Laurent 多项式逐项检查；错误的单个电磁虚部符号会被拒绝。有限算术不能替代边界兼容性和光滑解存在论证。

正分母区域中的十二实变量右侧都是有理函数。A-GOUR01 的逐格 Banach 误差管道命题因此可用相同证明推广，前四分量取 u 宽度，后八分量取 v 宽度。目前尚未实现并运行这个带电系统的全域向外舍入证书；当前候选数值全部为 E0。

## 3. 独立基准

[verify_charged_characteristic.py](verify_charged_characteristic.py) 核对五个精确传播/Einstein 恒等式、七组含非零电荷与复标量的 RHS 值，并拒绝错误波输运号数。另比较两组已知解：

* RN 电真空 M=2、Q=1、初始 r=8。以 rᵥ=f/2、rᵤ=−f/2、κ=1/2、Aᵤ=Q/r 构造独立比较；16/32/64 网格终点最大误差约 1.06e−8、2.65e−9、6.63e−10。
* 中性收缩 FLRW，同样演化十二变量并独立恢复标量。对应误差约 3.92e−3、9.77e−4、2.44e−4。

两组均为二阶经验收敛，验证器没有给数值 PDE 的严格误差。报告见 [CHARGED_CHARACTERISTIC_CHECKS](CHARGED_CHARACTERISTIC_CHECKS_2026-10-17.json)。

## 4. 新形状的有限 β 成员

[new_shape_jets.py](new_shape_jets.py) 对 R=10、Φ=0.7、ρ=1/8 重建开启/充电/关断的闭式 C0 半径、Gauss 积分及五实残差。末段使用两个支撑分离、固定相位的修复脉冲。四个浮点根的结果为

| β | 采样 min H | 锥上采样筛选 |
|---|---:|---|
| 0.003 | −1.6046e−4 | 不通过 |
| 0.001 | −4.1575e−8 | 不通过 |
| 0.0003 | 1.0947e−6 | 保留 |
| 0.0001 | 3.6490e−7 | 保留 |

即使端点残差接近零，前两项也不能作为合法种子。较紧 ODE 容差复核保留相同符号，并检查一个非零复振幅方向的辅助极限响应；这不认证正平滑宽度或指定根盒。

还不能把这些有限 β 根套入上一轮极窄的几何盒：例如 β=0.0003 的帽半径与辅助极限相差约 4.80e−6，而 A-NEW01 的认证盒半宽为 2⁻⁴²。A-NEW02 只有充分小邻域的存在性，尚无其显式阈值。[根报告](NEW_SHAPE_JETS_2026-10-17.json) 和 [复核](NEW_SHAPE_JET_CHECKS_2026-10-17.json) 都保留此限制。

## 5. 充电区域的实际探索及下一道门槛

选取 β=0.0003 的 C0 根，用其实际 r、H、P、Q 重建初始出射边，不使用辅助 β=0 几何。将中心归一化后，在 U≤0.95 Vcap 的预穿轴矩形内继续覆盖整个早期充电和关断段，尚未包括远处两个修复脉冲。v 网格按开启、对数充电、关断三段分别取 48/96/192 单元。

三次均完成，未见所采样内点的双负膨胀；但全域最小采样 λ 的位置随网格移向边界，数值约 0.00344、0.00176、0.000878，不能据此声称有正的连续下界。初始 θ 的 C0 接点和有限网格误差也尚未被严格包络。固定内点另存 r、λ、Q 和未强制的半径、标量、电荷、质量约束残差，用于判断后续修复误差方法的优先级。

报告 [NEW_SHAPE_CHARGED_SCREEN](NEW_SHAPE_CHARGED_SCREEN_2026-10-17.json) 的实际作用域只有此有限 C0 探索。完整正 η 根、其后的修复脉冲未来、物质穿轴与 I⁺ 均未数值认证。新的 [外侧延拓引理](AF_OUTER_EXTENSION.md) 与后续 [过去薄带构造](PAST_COLLAR_AND_AF_REALIZATION.md) 另给实际光滑匹配种子到 AF 初值的非有效内部证明；未来数值演化不能代替其独立数学复核。

普通加密及角点分级仍受到 C0 接合点处 θ 双侧迹不同的影响：不能把一个共享 θ 值同时当成两侧 v 求积的端点值。[charged_piecewise_screen.py](charged_piecewise_screen.py) 将三段分别演化，在共同边保留八个 v 入流分量连续，并从右侧出射 θ 值重新沿 u 输运 θ 的右侧迹。r、κ 的共同边比较误差小于 1.4e−13。48/96/192/384 档中，指定关断段内点的电荷约束残差约 0.0871、0.02235、0.005663、0.001423，接近二阶下降。

重要限制：同一点的终边 λ 依次约 −0.003189、−0.0008041、−0.0002596、−0.0001278。这是一个可能的充电后期陷俘信号，当前仍无连续误差包络和正平滑根转移，不能据此淘汰全部新分支，也不能宣称该区域无陷俘。原较粗算法的正号与新算法负号共同说明：端点号数必须经过严格误差认证。报告见 [分段探索](NEW_SHAPE_CHARGED_PIECEWISE_2026-10-17.json)。

```text
python research/goal_a/new_shape_jets.py
python research/goal_a/verify_new_shape_jets.py
python research/goal_a/charged_characteristic_screen.py
python research/goal_a/verify_charged_characteristic.py
python research/goal_a/verify_af_outer_extension.py
```

验收 A1–A6 继续保持开放。有限锥端点等式、有限域无陷俘与 AF 尾延拓都不能替代全未来三分支终态证明。
