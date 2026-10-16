# A-HOR01：固定 e=3/5、终端半径 5 的光滑零锥约束种子

2026-10-16。内部构造及证明稿，未经外部独立数学审查。借用 Schneider 的显式低正则剖面形状，以下约束、归一化、平滑化和误差均从本项目 D001 重推。**只构造一条零锥上的光滑约束数据，不声称形成黑洞、匹配完整 RN、取得全未来正则中心或目标 A 临界族。**

## 1. 本轮实际构造的对象

固定长度单位，\(e=3/5,R=5\)，不随参数缩放质量。存在一个确定宽度
\(\eta=2^{-160}\) 和 \(s_\eta\in(3/20,17/100)\)，使下面明确给出的光滑场 \(\phi_\eta(v;s_\eta)\)，\(0\le v\le1\)，产生
\[
r''=-r|\phi_\eta'|^2,\quad r(1)=5,\quad r'(1)=0,\qquad
Q'=er^2\Im(\phi_\eta\overline{\phi_\eta'}),\quad Q(0)=0,
\]
\[
H=-4r\nu,\quad H'=1-Q^2/r^2,\quad H(0)=r(0)/r'(0).
\tag{S1}
\]
它满足：

- \(\phi_\eta\) 延拓为零后属于 \(C^\infty(\mathbb R)\)，所有端点纵向 jets 为零；
- \(r>5/8\)，\(r'>0\) 对 \(0\le v<1\)，\(H>1/2048\) 对 \(0\le v\le1\)，所以 \(\nu<0\)；
- \(Q(1)=r(1)=5\)，终端 Hawking 质量 \(m(1)=5/2\)、重整化质量 \(\varpi(1)=5\)；
- 起点 \(m(0)=Q(0)=0\)，可沿 \(v<0\) 的平直零锥段接到规则 Minkowski 顶点。

最后一项是零锥数据的相容平直帽，不是整个未来中心的定理。\(s_\eta\) 由连续函数的变号与中值定理给出；没有把浮点根当作精确根，也没有声称根唯一或已经构造阈值参数曲线。

## 2. 显式 C0 基准剖面

源形状见 [Schneider, arXiv:2608.23355v1, §III.2–3](https://arxiv.org/html/2608.23355v1)。固定
\[
\Phi=\tfrac12,\quad s\in[3/20,17/100],\quad
c=\sqrt{s(1-s)},\quad \lambda=c/\Phi,\quad
\alpha=\arctan(s/\Phi),
\]
\[
v_2=\frac{s}{s+\Phi\tan\Phi},\quad
t=\Phi^{1/s},\quad v_1=v_2t.
\]
场取
\[
\phi_s(v)=
\begin{cases}
\Phi e^{-i\lambda\log v_1}v/v_1,&0\le v\le v_1,\\
\Phi e^{-i\lambda\log v},&v_1\le v\le v_2,\\
\Phi e^{-i\lambda\log v_2}(1-v)/(1-v_2),&v_2\le v\le1.
\end{cases}
\tag{S2}
\]
归一化面积半径 \(f=r/R\)，由终端 \(f(1)=1,f'(1)=0\) 向过去求得
\[
f(v)=
\begin{cases}
\Phi\cos\Phi\,\sec\alpha\,
 \cos(\Phi(1-v/v_1)+\alpha),&v\le v_1,\\
\cos\Phi\,(v/v_2)^s,&v_1\le v\le v_2,\\
\cos(\Phi(1-v)/(1-v_2)),&v\ge v_2.
\end{cases}
\tag{S3}
\]
两接合点的 \(f,f'\) 连续，(S1) 的 Raychaudhuri 方程在弱意义成立。定义不含 e、R 的带符号积分
\[
C_s(v)=\int_0^v f^2\Im(\phi_s\overline{\phi_s'})\,dx,\qquad
k(s)=C_s(1)=K\sqrt{(1-s)/s},\quad
K=\frac{\Phi\cos^2\Phi(1-\Phi^2)}2.
\tag{S4}
\]
\(k\) 严格递减。使 \(Q(1)=R\) 的条件是 \(eR\,k=1\)，在本固定尺度即 \(k=1/3\)。C0 根的解析式为
\(s_0=9K^2/(1+9K^2)\)，约 0.158016；该近似只用于诊断。

## 3. 整个 s 区间的余量认证

为在平滑化后继续得到精确根，对整个 s 区间先令
\(q_s(v)=C_s(v)/k(s)\)，即暂时将终端电荷归一化为一。此归一化只用于无量纲不等式；最终根处 \(q=Q/R\)，模型的 e、R 始终固定。

令 \(a=\Phi^2=1/4,\ \tau=\tan\Phi,\ H_0=f(0)/f'(0)\)。有精确式
\[
H_0=\frac{s\,t(1-s\tau/\Phi)}{(s+\Phi\tau)^2},
\]
\[
I_{\rm ch}=
\frac{v_2}{\cos^2\Phi(1-a)^2}
\left[\frac1{1+2s}-2a+\frac{a^2}{1-2s}
                  -\frac{8as^2t}{1-4s^2}\right],
\quad
I_{\rm off}=\frac{(1-v_2)\tau}{\Phi},
\]
\[
H_1=H_0+1-I_{\rm ch}-I_{\rm off}.
\tag{S5}
\]
其中 \(I_{\rm ch},I_{\rm off}\) 分别是 \(\int(q_s/f)^2dv\) 在充电段和关断段上的积分；用原函数直接微分可核对。

在开启段 \(q=0\)，H 增加；充电段
\[
\frac qf=
\frac{(v/v_2)^s-a(v/v_2)^{-s}}{\cos\Phi(1-a)}
\]
严格增加，H 先增加再可能下降；关断段 \(q=1,f\le1\)，H 非增。因此
\(\min_vH(v)=\min(H_0,H_1)\)。

[verify_horizon_seed.py](verify_horizon_seed.py) 把 s 区间等分 256 格，以有理区间运算验证
\[
H_0,H_1>1/1024,\quad 1/4<k(s)<1/2,
\]
\[
k(3/20)>1/3+1/256,\qquad
k(17/100)<1/3-1/256.
\tag{S6}
\]
所有四则运算向外舍入至 192 个二进制小数位；sin、cos、log 2、exp 使用有理 Taylor 和显式余项，**不以浮点抽样覆盖连续区间**。k 的端点变号通过 k² 与正阈值平方比较，无需浮点开方。

另外有简单全区间界：
\[
f(0)=\Phi\cos^2\Phi-s\cos\Phi\sin\Phi>1/4,\quad
0\le f'\le f'(0)<128,\quad f'(0)>1/2.
\tag{S7}
\]
证明可用 \(\cos(1/2)>7/8,\ \sin(1/2)<1/2,\ v_2>1/3,\ t>1/128\)，从而 \(v_1>1/384\)。凹性及 \(f(1)=1\) 给 \(f'(0)\ge1-f(0)>1/2\)。所有剖面分段延拓到接点半邻域后，\(|\phi_s'|\le512\)，幅度小于一。

## 4. 明确的光滑化，不丢掉电荷根

令 \(\chi(x)=0\) 对 \(x\le0\)，\(\chi(x)=1\) 对 \(x\ge1\)，中间取
\[
\chi(x)=
\frac{e^{-1/x}}{e^{-1/x}+e^{-1/(1-x)}}.
\]
它光滑且 \(0\le\chi\le1,\ |\chi'|\le8\)。例如中间区间 \([1/4,3/4]\) 用 logistic 导数公式给界 8，两端用 \(e^{-1/x}/x^2\) 的有界性给更小界。

在每个接点 \(v_j\) 的 \([v_j-\eta,v_j+\eta]\)，用
\((1-\chi((v-v_j+\eta)/(2\eta)))\phi_{\rm left}
 +\chi((v-v_j+\eta)/(2\eta))\phi_{\rm right}\)
替换 (S2)。在 \([0,\eta]\) 乘 \(\chi(v/\eta)\)，在 \([1-\eta,1]\) 乘 \(\chi((1-v)/\eta)\)。这些区域不相交，其余保留 (S2)，延拓为零。记结果为 \(\widetilde\phi_s\)。

这是固定 \(\eta=2^{-160}\) 的明确 \(C^\infty\) 构造，且对 s 光滑。接点两侧值相等、各自导数至多 512，故
\[
\|\widetilde\phi_s-\phi_s\|_\infty\le2^{10}\eta,\quad
\|\widetilde\phi_s'-\phi_s'\|_{L^2}
\le30\cdot512\sqrt\eta<2^{-66}.
\tag{S8}
\]
差异仅在长度至多 \(6\eta\) 的区域；混合项的 \(1/\eta\) 被接点值差 \(O(\eta)\) 抵消。特别是
\[
\|\,|\widetilde\phi_s'|^2-|\phi_s'|^2\,\|_{L^1}<2^{-55}.
\tag{S9}
\]
不能用普通浮点网格“分辨”这些层来代替 (S8)–(S9)。

为控制 Raychaudhuri 的非线性影响，令 \(\widetilde f_s\) 解相同终端问题，写 \(\widetilde f=f y\)。则
\[
(f^2y')'=-f^2\delta V\,y,\quad
y(1)=1,\ y'(1)=0,\quad
\delta V=|\widetilde\phi'|^2-|\phi'|^2.
\]
其相对 Volterra 核范数至多 \(16\|\delta V\|_1<2^{-51}\)。由直接收缩估计，
\[
\|\widetilde f-f\|_\infty<2^{-50},\quad
\|\widetilde f'-f'\|_\infty<2^{-42},\quad
\widetilde f>1/8.
\tag{S10}
\]
这里不使用 \(\exp(\int|\phi'|^2)\) 这种会浪费全部余量的粗估计。正性和凹性还给 \(\widetilde f\le1\)。

定义 \(\widetilde C,\widetilde k,\widetilde q\) 同 (S4)。由 (S8)–(S10) 及 Cauchy–Schwarz，
\[
\sup_v|\widetilde C-C|<2^{-38},\quad
\sup_v|\widetilde q-q|<2^{-33}.
\]
因为 \(k\ge1/4,\widetilde k\ge1/8\)，除法稳定。继而
\[
\sup_v|\widetilde H-H|<2^{-23},
\quad
\widetilde H(v):=\frac{\widetilde f(0)}{\widetilde f'(0)}
       +v-\int_0^v\frac{\widetilde q^2}{\widetilde f^2}\,dx
>1/2048.
\tag{S11}
\]
可逐项使用
\(|\delta(f(0)/f'(0))|<2^{-38}\) 和
\(\int|\widetilde q^2/\widetilde f^2-q^2/f^2|<2^{-24}\)。

(S6) 的电荷端点变号仍然保留；\(\widetilde k(s)\) 连续，中值定理给
\(\widetilde k(s_\eta)=1/3\)。在该根处取 \(r=5\widetilde f,Q=15\widetilde C\)，所以 \(Q/R=\widetilde q\)，(S11) 正是固定 e=3/5 的真实约束。终端电荷等式精确，而非近似比值。

## 5. 纵向接合、顶点及尺度

端点场的全阶平坦性使 \(v\ge1\) 上可延拓
\(r=Q=5,\lambda=0,\nu=\nu(1)<0,\phi=0,\Omega=1\)，所有纵向 jets 光滑匹配。此时 \(m=5/2,\varpi=5\)，不是把视界 Hawking 质量写成终态质量。

对 \(v\le0\)，取
\[
r=r(0)+r'(0)v,\quad Q=\phi=0,\quad
\nu=-1/(4r'(0)),\quad\Omega=1.
\]
它在 \(v_c=-r(0)/r'(0)<0\) 有相容的 Minkowski 规则顶点。这里 v 的仿射尺度不等于中心单位法向归一化；中心单位出射仿射标签是
\(\sigma=r'(0)(v-v_c)\)，满足 \(dr/d\sigma=1\) 于顶点。若以后使用聚焦或陷俘判据，必须先作这个转换。由于本区间 \(5/4<r'(0)<640+1\)，该转换有有限正上下界；没有把每个成员的质量重新归一化为一。

C0 开启段的中心归一化仿射宽度精确为
\[
\Delta\sigma=r'(0)v_1
=5\left(\Phi^2\cos\Phi\sin\Phi+\Phi s\cos^2\Phi\right).
\]
它不是坐标宽度 \(v_1\)。在 C0 电荷根附近该宽度约 0.830，相应开启段末 Hawking 质量约 0.591；仅将 \(v_1\approx0.00456\) 填入中心归一化短脉冲定理会造成错误判决。报告保留这些 E0 数值，并不据此认证或排除中心陷俘。

沿本零锥还有
\[
m'=\frac{Q^2r'}{2r^2}+\frac{Hr}{2}|\phi'|^2\ge0,
\]
由 \(m=(r-Hr')/2\)、(S1) 直接得到，故起点零质量与终端 \(m=5/2\) 相容。本单锥上的未陷俘号数不能排除其未来内侧出现另一个严格陷俘区。

## 6. 尚未匹配的横向 jets：一个真实的下一步残差

纵向场平坦不保证 \(D_u\phi\) 在终端为零。取 \(A_v=0,\Omega=1\)，从 D001 波方程及交换子精确得到
\[
(rD_u\phi)'=-\nu\phi'-\frac{ieQ}{4r}\phi.
\]
起点 Minkowski 给 \(D_u\phi(0)=0\)，两端 \(\phi=0\)，故必要的一阶终端条件是
\[
\boxed{\ \mathcal J(\phi):=
\int_0^1\left(\nu'-\frac{ieQ}{4r}\right)\phi\,dv=0\ },
\qquad
r(1)D_u\phi(1)=\mathcal J(\phi).
\tag{S12}
\]
这是复残差，额外两项实条件。(S4) 的电荷调节没有处理它。不能因 \(\phi\) 光滑、终端 \(r=Q=\varpi=5\)，便宣称已平滑接到 RN 的时空邻域。

脚本另对 C0 解析根作三档分段 Simpson 诊断；观测 \(|D_u\phi(1)|\) 约 0.009496。此为 E0 浮点诊断，既没有认证其严格非零，也没有数值分辨 \(\eta\) 层或计算光滑根。它明确提示下一步必须解 (S12)，之后还需更高横向 jets、实际中心填充、完整 Cauchy 数据及色散邻侧；目标 A 仍开放。

## 7. 复算与证据边界

    python research/goal_a/verify_horizon_seed.py
    python -O research/goal_a/verify_horizon_seed.py

[报告](HORIZON_SEED_RESULTS_2026-10-16.json) 分开记录有理区间证书和浮点横向诊断。前者认证 (S6) 等有限连续参数不等式；光滑根的存在还使用第 4 节写出的解析稳定性及中值定理论证。两者均不认证完整时空、事件视界、黑洞终态或临界性。
