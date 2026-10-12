# 逐命题修订目录

依赖分为共同前提与case_rules；来源区间保留原始逐字文本定位。此目录覆盖23稿的主要结论和显式分支/接口，未把证明中的每一个辅助不等式单独命名。

| 结论ID/题目 | 共同/分支依赖 | 应用假设（未逐实例认证） | 适用域与限制 | 来源 |
| --- | --- | --- | --- | --- |
| L001.PERSIST 严格陷俘有限时间持久 | SYS、TOPO、CAUCHY | 固定有限紧光滑参考片、严格负余量、共同规范 | 该参考数据的相对强邻域； | `RECCVS/proofs/RECCVS_L001.md` L15–32；`RECCVS/proofs/RECCVS_L001.md` L5–14 |
| L001.EXCLUDE 不在N/D闭包 | L001.PERSIST、PENROSE | NEC、MGHD、非紧完备Cauchy面 | 固定候选及其邻域；U⊂B需要另加全局可预测性/零无穷远条件 | `RECCVS/proofs/RECCVS_L001.md` L5–14 |
| L001.BH 附加可预测性下黑洞邻域 | L001.EXCLUDE、VIS | 另有全局可预测性/Kommemi陷俘遮蔽假设及适当I+识别 | 满足额外假设的邻域；本引理自身不给这些额外全局前提 | `RECCVS/proofs/RECCVS_L001.md` L5–14 |
| L002.DATA 完整正则AF约束数据 | SYS、TOPO | 固定0<r0<R0、实f,g∈Cc∞((r0,R0))及固定e；K=0、AΣ=0、φ0=pf、Π=-ipg；m(r0)=Q(r0)=0；小p使Δ≥1/2的bootstrap闭合；全部约束含动量/Gauss | 整张初始面；本项目按e≠0采用；原L002的约束构造允许e=0，但不属于带电应用 | `RECCVS/proofs/RECCVS_L002.md` L21–48；`RECCVS/proofs/RECCVS_L002.md` L5–19 |
| L002.FAMILY 参数光滑、统一范数及非零电荷 | L002.DATA | 电荷首项非零时再给Q非零 | 固定小p族；初始膨胀不能代替未来色散 | `RECCVS/proofs/RECCVS_L002.md` L21–48；`RECCVS/proofs/RECCVS_L002.md` L5–19 |
| L003.TIDAL Ric(L,L)与PP角向潮汐 | SYS、AFFINE_NORM、SMOOTH_DOMAIN | 仿射径向L与平行角框架 | 实际零线光滑段；标量K、有限参数、可见性另证 | `RECCVS/proofs/RECCVS_L003.md` L1–16 |
| L004.IDENTITY 正膨胀段的面积坐标指数恒等式 | L004.AFFINE | 仅在 r_s>0 的最大初始区间用面积半径；中心积分可积 | 实际正膨胀段； | `RECCVS/proofs/RECCVS_L004.md` L33–46；`RECCVS/proofs/RECCVS_L004.md` L5–32 |
| L004.LOG 完备有界半径的对数障碍 | L004.IDENTITY | S=∞、r_s>0、r≤RH | 该完整实际线；有限S的退化版本同节；不推出曲率发散 | `RECCVS/proofs/RECCVS_L004.md` L5–32 |
| L004.FINITE 有限仿射正半径膨胀退化的能量障碍 | L004.IDENTITY | S<∞、r→R*>0、r_s→0；仍在r_s>0段 | 该线的有限仿射端；即使端点可光滑继续也成立；不验收曲率奇异 | `RECCVS/proofs/RECCVS_L004.md` L5–32 |
| L004.NOBH 限定覆盖类中无黑洞 | L004.IDENTITY、VIS | 每条所用中心出射线全未来 r_s>0、仿射完整、E有逐线有限上界；覆盖未来域；r→∞端为同一完整I+且每线确实到达；全时空结论另核初始面与过去域 | 仅满足全部额外假设的类； | `RECCVS/proofs/RECCVS_L004.md` L47–54；`RECCVS/proofs/RECCVS_L004.md` L5–32 |
| L005.CHARGE 仿射电荷—通量不等式（允许r_s非正） | SYS、L004.AFFINE | Q(0)=0；H_S=∫r³\|φ\|²、F_S=∫r\|D_sφ\|²=b-r_s(S)；不要求 r_s 全段正 | 从实际中心起算的有限光滑段，r在非中心点正；迫使陷俘还需振幅积分上界与另一膨胀负号 | `RECCVS/proofs/RECCVS_L005.md` L7–19；`RECCVS/proofs/RECCVS_L005.md` L25–25；`RECCVS/proofs/RECCVS_L005.md` L27–31 |
| L005.COUNTER 能量发散而潮汐有界的局部实现 | SYS、CHAR | 给定实际相容两特征边；正半径 | 局部光滑反例片；不是I001正则中心全局模型 | `RECCVS/proofs/RECCVS_L005.md` L33–58 |
| L006.GLOBAL 小数据归一化与全局解接口 | SYS、L002.DATA、L002.FAMILY、KL | 固定e与N≥14；转换后来源范数足够小 | L002充分小族； | `RECCVS/proofs/RECCVS_L006.md` L27–55；`RECCVS/proofs/RECCVS_L006.md` L16–26；`RECCVS/proofs/RECCVS_L006.md` L5–54 |
| L006.RADIAL 所有径向零线完整 | L006.GLOBAL | 来源C0与好角向导数界；中心穿越 | 该小数据发展中的径向零线； | `RECCVS/proofs/RECCVS_L006.md` L56–73；`RECCVS/proofs/RECCVS_L006.md` L5–54 |
| L006.INNERCONE 最终内锥因果线完整 | L006.GLOBAL | 固定η>0，晚时ρ≤(1-η)t；连接系数可积 | 满足内锥条件的因果线；全部非径向外锥线和完整I+仍缺 | `RECCVS/proofs/RECCVS_L006.md` L56–73；`RECCVS/proofs/RECCVS_L006.md` L5–54 |
| L007.STRIP 每个有限T实际未陷俘薄带 | SYS、I001 | 每个固定有限T已有实际矩形0≤U≤aT、1≤t≤T；RN的λ、λ_U、λ_UU匹配，ν_H<0；该紧矩形C4界有限；bT可随T退化 | 0<U≤bT，1≤t≤T； | `RECCVS/proofs/RECCVS_L007.md` L26–48；`RECCVS/proofs/RECCVS_L007.md` L5–24 |
| L007.ZEROJETS 精确接合没有非零视界jet尾系数 | I001、HORIZON | 全部标量jets为零 | 该精确形成输入； | `RECCVS/proofs/RECCVS_L007.md` L49–57；`RECCVS/proofs/RECCVS_L007.md` L5–24 |
| L008.PREFIX 视界前缀积分与膨胀号 | SYS、SMOOTH_DOMAIN、NU_NEG | 完整实际前缀；ν传播可由MGHD提供 | 单条入射前缀； | `RECCVS/proofs/RECCVS_L008.md` L5–25；`RECCVS/proofs/RECCVS_L008.md` L3–24 |
| L008.CENTER 完整中心截面的积分因子公式 | SYS、REG_CENTER、SMOOTH_DOMAIN、NU_NEG | 该截面确实连接中心；ν<0 | 该截面全部正半径点； | `RECCVS/proofs/RECCVS_L008.md` L26–55；`RECCVS/proofs/RECCVS_L008.md` L3–24 |
| L008.ONECROSS 一次跨越充分排除陷俘 | L008.CENTER | 外端λH≥0；实际Q/r满足指定一次跨越 | 单截面；跨越条件的全时间传播尚未证明 | `RECCVS/proofs/RECCVS_L008.md` L56–68；`RECCVS/proofs/RECCVS_L008.md` L3–24 |
| L008.THREECROSS 深部陷俘至少三次跨越 | L008.CENTER | 晚时极端外端、Q_r(M)=0、完整中心截面 | 该截面； | `RECCVS/proofs/RECCVS_L008.md` L69–79；`RECCVS/proofs/RECCVS_L008.md` L3–24 |
| L009.WEDGE 楔域几何/场统一bootstrap | SYS、HORIZON、L008.PREFIX、L010.TRANSPORT | N,A固定；先定粗常数后缩c,η | Ut≤c的实际过去矩形； | `RECCVS/proofs/RECCVS_L009.md` L46–89；`RECCVS/proofs/RECCVS_L009.md` L90–123；`RECCVS/proofs/RECCVS_L009.md` L5–44 |
| L009.EXIST 同一全时间楔域发展 | L009.WEDGE、L009.CONTINUE | 低阶正半径界及每个有限矩形高阶输运 | 0≤U≤η，t≥1，Ut≤c； | `RECCVS/proofs/RECCVS_L009.md` L124–143；`RECCVS/proofs/RECCVS_L009.md` L5–44 |
| L009.ACTUAL 楔域识别进同一Cauchy发展 | L009.EXIST、I001、INSEG | 共同实际边、几何唯一性/MGHD接口 | 原形成种子的楔域； | `RECCVS/proofs/RECCVS_L009.md` L124–143；`RECCVS/proofs/RECCVS_L009.md` L5–44 |
| L010.TRANSPORT 共变波输运与Wilson积分 | SYS、SMOOTH_DOMAIN | 实际光滑 r>0、Ω²>0，A_t=0、P=D_Uφ、T=D_tφ；不需ν或λ正负 | 实际光滑正半径片； | `RECCVS/proofs/RECCVS_L010.md` L5–27；`RECCVS/proofs/RECCVS_L010.md` L7–26 |
| L010.CENTER 中心复积分必要相容 | L010.TRANSPORT、REG_CENTER、INSEG、HORIZON | 入射段到中心；晚时视界T=0 | 仍正则的完整中心截面；不是全部四维中心光滑性的充分条件 | `RECCVS/proofs/RECCVS_L010.md` L28–47；`RECCVS/proofs/RECCVS_L010.md` L7–26 |
| L010.PHASE 电流号不由正能量决定 | SYS、CHAR | 两组局部相容角点/特征数据 | 局部正半径反例； | `RECCVS/proofs/RECCVS_L010.md` L48–59；`RECCVS/proofs/RECCVS_L010.md` L7–26 |
| L011.BUDGET 每条实际线的必要充分预算 | SYS、SMOOTH_DOMAIN、NU_NEG | 真实起点；中心起点另要求REG_CENTER | 已有实际出射线光滑段； | `RECCVS/proofs/RECCVS_L011.md` L5–26；`RECCVS/proofs/RECCVS_L011.md` L7–17 |
| L011.WILSON 晚时预算的Wilson表示 | L011.BUDGET、L010.TRANSPORT、INSEG、HORIZON | 视界T=0；形成期通量单独扣除 | 晚时实际连通域； | `RECCVS/proofs/RECCVS_L011.md` L27–48；`RECCVS/proofs/RECCVS_L011.md` L7–17 |
| L011.WEDGE 楔域正预算闭合 | L011.BUDGET、L009.WEDGE | 同一楔域内高阶平坦性 | Ut≤c； | `RECCVS/proofs/RECCVS_L011.md` L49–57；`RECCVS/proofs/RECCVS_L011.md` L7–17 |
| L011.FORCED 额外非零尾下的强制聚焦 | L011.BUDGET、TAIL_LOWER | 2β≤γ+1；线在全部未来实际存在 | 满足额外下界的线；原种子未证该尾下界；候选排除再调用L001.EXCLUDE | `RECCVS/proofs/RECCVS_L011.md` L58–76；`RECCVS/proofs/RECCVS_L011.md` L7–17 |
| L012.KERNEL 显式Liouville有界核表示 | SYS、SMOOTH_DOMAIN | 固定q(U)>0、F(U)=∫q/4、Θ²=q[1+F(t-1)]^-2；源满足有限矩形积分表示；比较恒等式无需ν<0 | 每个有限过去矩形； | `RECCVS/proofs/RECCVS_L012.md` L43–79；`RECCVS/proofs/RECCVS_L012.md` L5–41 |
| L012.STRIP 固定宽度全时间bootstrap | L012.KERNEL、L008.PREFIX、L010.TRANSPORT、HORIZON | 同一C∞输入；N→A→粗常数→η的选取次序 | 0≤U≤η、t≥1；r≥3/4； | `RECCVS/proofs/RECCVS_L012.md` L80–124；`RECCVS/proofs/RECCVS_L012.md` L125–154；`RECCVS/proofs/RECCVS_L012.md` L155–179；`RECCVS/proofs/RECCVS_L012.md` L5–41 |
| L012.EXIST 固定条带实际全时间发展 | L012.STRIP、L009.CONTINUE、I001、INSEG | 使用L009§4的有限矩形延续机制；同一实际边识别 | 固定条带全部有限t； | `RECCVS/proofs/RECCVS_L012.md` L180–187；`RECCVS/proofs/RECCVS_L009.md` L124–143；`RECCVS/proofs/RECCVS_L012.md` L5–41 |
| L012.PP 有限仿射长度与全部径向PP曲率界 | L012.STRIP、L012.EXIST、AFFINE_NORM | 每条固定U>0；t=1规范化框架 | 0<U≤η的固定出射线；长度U↓0可发散；本片没有曲率发散 | `RECCVS/proofs/RECCVS_L012.md` L188–214；`RECCVS/proofs/RECCVS_L012.md` L5–41 |
| L012.BOUNDARY 非退化连续度量边界 | L012.STRIP、L012.KERNEL、L012.EXIST | 固定U1>0闭区间；可积源与支配收敛 | V=-1/t的正半径边界片；方程解/C²/C∞延拓未验收；MGHD内不可继续的解释另用I001全局接口 | `RECCVS/proofs/RECCVS_L012.md` L215–227；`RECCVS/proofs/RECCVS_L012.md` L5–41 |
| L012.MGHD_EDGE 完整视界下MGHD内常规端点障碍 | L012.PP、I001、MGHD | 完整视界与实际MGHD整体双曲性；假想端点的因果过去包含全部晚时视界段 | 每条固定U>0的t→∞端；因果紧性论证待独立复核；不等于方程解延拓正则性结论 | `RECCVS/proofs/RECCVS_L012.md` L215–227；`RECCVS/proofs/RECCVS_L012.md` L5–41 |
| L013.LIMIT 散射迹与α/t²极限 | L012.STRIP、L012.BOUNDARY | 固定同一种子；端点支配函数可积 | [a,η]极限及(0,η]增长； | `RECCVS/proofs/RECCVS_L013.md` L40–56；`RECCVS/proofs/RECCVS_L013.md` L5–38 |
| L013.RIGID h=0与初始零场等价 | L013.LIMIT、L012.STRIP、L010.TRANSPORT | 先选足够大N、再缩η；常数独立于时间且选取合法 | 同一固定近视界条带； | `RECCVS/proofs/RECCVS_L013.md` L61–81；`RECCVS/proofs/RECCVS_L013.md` L5–38 |
| L013.OUTER 非零初始场提供正增长外边 | L013.RIGID、L013.LIMIT | 实际初始场在[0,η]不恒零 | 固定b=η的全时间外边；h与晚时阈值没有族统一界 | `RECCVS/proofs/RECCVS_L013.md` L82–89；`RECCVS/proofs/RECCVS_L013.md` L5–38 |
| L014.VOLUME 抽象外边给全余域有限体积 | L014.PREFIX、OUTER_INPUT | 外边全部t≥1存在；α_b≥a0>0且α_b/t²→h_b>0；连通段单调穷尽；不预设中心或未陷俘 | 整个实际D_b余域； | `RECCVS/proofs/RECCVS_L014.md` L24–47；`RECCVS/proofs/RECCVS_L014.md` L5–22 |
| L014.CENTER 中心截面电磁积分与加权半径界 | SYS、L014.PREFIX、OUTER_INPUT、REG_CENTER | 该实际完整截面确以仍正则中心结束，rλ→0；只此时消去中心端项；不需深部λ≥0 | 仍存在中心的完整截面； | `RECCVS/proofs/RECCVS_L014.md` L48–74；`RECCVS/proofs/RECCVS_L014.md` L5–22 |
| L014.AXIS dτ/dt=1/(2α)轴线恒等式 | SYS、REG_CENTER | dr\|Γ=0、Δ→1；相容双零坐标 | 实际正则轴线； | `RECCVS/proofs/RECCVS_L014.md` L75–105；`RECCVS/proofs/RECCVS_L014.md` L5–22 |
| L014.LIFETIME 外边下中心剩余固有长度有限 | L014.AXIS、L014.PREFIX、OUTER_INPUT | 该正则中心段在固定外边更深处；T≥Tb，αΓ≥αb；允许 t_end有限或无限 | 该正则轴线的实际剩余段；不推曲率、零仿射长度或可见性 | `RECCVS/proofs/RECCVS_L014.md` L75–105；`RECCVS/proofs/RECCVS_L014.md` L5–22 |
| L014.EXTENSION 体积可供正半径延拓原理调用 | L014.VOLUME、KOM_EXT | 整个去端点菱形实际存在、r≥r0>0、紧初始边 | 仅满足全部延拓前提的菱形； | `RECCVS/proofs/RECCVS_L014.md` L106–118；`RECCVS/proofs/RECCVS_L014.md` L5–22 |
| L015.NONZERO 中心与视界电荷差强迫非零场 | SYS、I001、INSEG、REG_CENTER | 中心活到t=1，完整该截面，QH=1/QΓ=0 | 实际t=1截面； | `RECCVS/proofs/RECCVS_L015.md` L17–29；`RECCVS/proofs/RECCVS_L015.md` L5–15 |
| L015.GAPOUTER 零场空隙后构造合法正外边 | L015.NONZERO、SYS、CHAR、I001 | 首非零点c>0；有限ERN参考矩形、固定宽度、反向Goursat唯一性 | 同一解首非零点旁条带；w≥0选择的延拓不自动属于原MGHD | `RECCVS/proofs/RECCVS_L015.md` L50–80；`RECCVS/proofs/RECCVS_L015.md` L30–49；`RECCVS/proofs/RECCVS_L015.md` L81–103；`RECCVS/proofs/RECCVS_L015.md` L5–15 |
| L015.OUTER 两种非零起点情形均提供外边 | L015.NONZERO；分情况：c=0 ⇒ L015.NEAREDGE / c>0 ⇒ L015.GAPOUTER | 中心在t=1为实际正则点；c由15.1定义，0≤c<UΓ(1) | 中心活到t=1时同一实际全时间外边； | `RECCVS/proofs/RECCVS_L015.md` L5–16；`RECCVS/proofs/RECCVS_L015.md` L5–15 |
| L015.LIFETIME 全部轴线寿命分支固有长度有限 | I001、MGHD、REG_CENTER；分情况：t_end<∞ ⇒ L015.FINITETIME / t_end=∞ ⇒ L015.INFINITETIME | 同一实际MGHD的唯一最大正则轴线；正规中心端点可继续轴线；没有跳到第二轴线 | 同一实际MGHD轴线；这一层不依赖先证明曲率奇异或深部λ号 | `RECCVS/proofs/RECCVS_L015.md` L104–122；`RECCVS/proofs/RECCVS_L015.md` L5–15 |
| L016.CURVATURE 中心精确曲率/质量恒等式 | SYS、REG_CENTER | 旋转对称、无磁荷；逐事件中心极限 | 四维实际正则中心；不依赖I001、L012或L015 | `RECCVS/proofs/RECCVS_L016.md` L37–56；`RECCVS/proofs/RECCVS_L016.md` L5–29 |
| L016.PHYSICAL Dτφ=4αT=P/(-ν) | L014.AXIS、REG_CENTER | 中心空间共变梯度为零 | 实际正则轴线； | `RECCVS/proofs/RECCVS_L016.md` L57–71；`RECCVS/proofs/RECCVS_L016.md` L5–29 |
| L016.SINGULAR 有限固有时曲率判据 | L016.CURVATURE、L016.PHYSICAL、L015.LIFETIME | 另加limsup\|αΓTΓ\|=∞ | 该轴线有限固有时端点；增长前提未证；趋轴邻域与零仿射/可见性另证 | `RECCVS/proofs/RECCVS_L016.md` L72–83；`RECCVS/proofs/RECCVS_L016.md` L5–29 |
| L017.POINCARE 加权Poincaré与ground-state分解 | BESSEL | 中心有界且足够光滑的复f，f(R)=0；相容端点极限 | 独立径向函数类； | `RECCVS/proofs/RECCVS_L017.md` L30–51；`RECCVS/proofs/RECCVS_L017.md` L5–28 |
| L017.SHARP S≥4j\|Q\|/(\|e\|R²)与径向尖锐性 | SYS、REG_CENTER、NU_NEG、L017.POINCARE | 同一完整实际入射截面，ν<0、Q(0)=0、φ(R)=0、e≠0；中心有界/外端光滑；Wilson输运；尖锐性只在径向函数类 | 该截面及独立径向函数类；径向极值不认证全时空约束实现 | `RECCVS/proofs/RECCVS_L017.md` L52–80；`RECCVS/proofs/RECCVS_L017.md` L5–28 |
| L017.RATIO 极端截面αΓ/αH下界 | L017.SHARP、SYS | R=M、\|Q\|=M；仍连接正则中心 | 该极端完整截面；φ_r(R)=0给严格性但无统一间隙；不决定陷俘号 | `RECCVS/proofs/RECCVS_L017.md` L81–93；`RECCVS/proofs/RECCVS_L017.md` L5–28 |
| L018.SIGN 首谱值与实际端点膨胀同号 | L018.IDENTITY、CENTER_INTERVAL、SL | 中心型r(0)=0/r_s(0)=1、真实V有界，r>0于s>0、ν<0；DN型f(0)=0 | 实际中心起算有限区间； | `RECCVS/proofs/RECCVS_L018.md` L38–53；`RECCVS/proofs/RECCVS_L018.md` L5–36 |
| L018.CERT 正/负有限区间积分证书 | L018.SIGN | 可靠V_-≤V≤V_+；实际区间存在 | 该有限区间； | `RECCVS/proofs/RECCVS_L018.md` L54–72；`RECCVS/proofs/RECCVS_L018.md` L5–36 |
| L018.CENTER 中心χ与二阶物理导数桥梁 | L018.CERT、REG_CENTER、CENTER_INTERVAL | 实际χ=\|Dτφ\|²>0、V(0)=χ；同一线存在至ell=π/√χ且r>0于s>0、ν<0；全段\|D_L²φ\|≤χ/(2π) | 从该中心发出的实际有限线；χ大本身不提供存在长度或二阶界 | `RECCVS/proofs/RECCVS_L018.md` L73–92；`RECCVS/proofs/RECCVS_L018.md` L5–36 |
| L018.ROBIN 正半径初点Robin版本 | L018.IDENTITY、POS_INTERVAL、SL、NU_NEG | r(0)>0、全段r>0；真实V有界，固定仿射尺度和w0；二次型加w0\|f(0)\|²；不把DN中心定理直接作为前提 | 不从中心起算的实际段； | `RECCVS/proofs/RECCVS_L018.md` L93–102；`RECCVS/proofs/RECCVS_L018.md` L5–36 |
| L019.FIRST 内部首次触零刚性 | SYS、SMOOTH_DOMAIN、NU_NEG | U内部点；U邻域λ≥0才能推λ_U=0 | 有限紧实际光滑片内的正半径球； | `RECCVS/proofs/RECCVS_L019.md` L5–21；`RECCVS/proofs/RECCVS_L019.md` L3–20 |
| L019.BUDGET 无陷俘未来边际射线预算 | L019.FIRST、L010.TRANSPORT | 每个未来点的U邻域λ≥0；整段实际存在 | 该内部边际射线；φ0≠0才有有限预算；超预算但仍存在才推出陷俘 | `RECCVS/proofs/RECCVS_L019.md` L22–56；`RECCVS/proofs/RECCVS_L019.md` L3–20 |
| L020.PROFILE 固定有理剖面与八个零矩 | E020 | K=8,n=88,σ=1/20；能量归一化 | 辅助半线x≥0； | `RECCVS/proofs/RECCVS_L020.md` L5–32；`RECCVS/proofs/RECCVS_L020.md` L5–31 |
| L020.CURRENT 正电流滤波论证 | L020.PROFILE | 高斯有理多项式及上半平面根结构 | x>0辅助剖面； | `RECCVS/proofs/RECCVS_L020.md` L33–45；`RECCVS/proofs/RECCVS_L020.md` L5–31 |
| L020.J J恰一次简单负到正变号 | L020.PROFILE、E020 | 精确分子与六叶整数覆盖证书 | 紧化全半线； | `RECCVS/proofs/RECCVS_L020.md` L46–75；`RECCVS/proofs/RECCVS_L020.md` L5–31 |
| L020.KERNEL 𝒦单调且≥𝒦(0)>2^-854 | L020.PROFILE、L020.J、KDEF | 核ODE/边界按KDEF；正端点精确比较 | 全辅助半线； | `RECCVS/proofs/RECCVS_L020.md` L76–112；`RECCVS/proofs/RECCVS_L020.md` L5–31 |
| L021.FIX 光滑截断与精确零矩修复 | L020.PROFILE、L020.CURRENT、E021 | §1固定ρ、χ、归一化bump；§2全系数包络与H1截断误差；矩阵A精确定义且A^-1有界；d_s=M_s(χw)、α0=-A^-1d | 单块紧支持剖面；这里精确不意味着所有超越积分都是有理数 | `RECCVS/proofs/RECCVS_L021.md` L51–78；`RECCVS/proofs/RECCVS_L021.md` L5–49 |
| L021.CORE 未修复w的电流核心界与条件性C1扰动规则 | L020.PROFILE、E021 | E021核心Bernstein及系数上界；任意修复h满足\|\|h\|\|C1≤η≤1时的误差规则；本节点不自行认证具体α(c)小量 | [3/4,33/4]的w核心，以及满足给定C1小量的扰动； | `RECCVS/proofs/RECCVS_L021.md` L79–90；`RECCVS/proofs/RECCVS_L021.md` L5–49 |
| L021.FAMILY 周期族M_s(z_c)=c_s | L021.FIX、L021.CORE | 固定T及\|c_s\|≤2^-4096；共同端点开空隙 | 整个具体周期族； | `RECCVS/proofs/RECCVS_L021.md` L91–110；`RECCVS/proofs/RECCVS_L021.md` L5–49 |
| L021.KERNEL λ<3/5与周期核>2^-855 | L021.FAMILY、L020.KERNEL、KDEF | 单块L1比较与周期精确求和 | 全周期半线及参数球；实际形成另需有限振幅FLIFT实例 | `RECCVS/proofs/RECCVS_L021.md` L111–141；`RECCVS/proofs/RECCVS_L021.md` L5–49 |
| L022.TAIL 同一光滑极限固定Ck尾界 | REPAIR_BUDGET | 同一序列每步预算确已兑现；N≥max(N0,k+1)；高阶范数采用最大导数范数 | 满足预算的同一序列；不依赖有限振幅端点提升是否完成； | `RECCVS/proofs/RECCVS_L022.md` L5–22；`RECCVS/proofs/RECCVS_L022.md` L5–21 |
| L022.CONE 显式锥几何安全预算 | SYS | 参考r/t≥a,H/t≥h,β>0与场范数已认证 | 同一仿射锥[0,1]；a,h,β尚需具体有限成员 | `RECCVS/proofs/RECCVS_L022.md` L23–95；`RECCVS/proofs/RECCVS_L022.md` L5–21 |
| L022.FLOW 修复尾误差的实际W传播 | L022.TAIL、COMMON_FLOW | 共同域、同一物理线、经过证明的C_flow | 该共同有限实际域；这是尚未取得输入的条件性接口 | `RECCVS/proofs/RECCVS_L022.md` L96–110；`RECCVS/proofs/RECCVS_L022.md` L5–21 |
| L022.DECISION 总误差下正/负谱判决 | L022.FLOW、L018.CERT | 可靠数值包络、严格余量ρ、总误差满足门槛 | 同一有限实际区间；不是原种子的已完成实际符号证书 | `RECCVS/proofs/RECCVS_L022.md` L111–136；`RECCVS/proofs/RECCVS_L022.md` L5–21 |
| L023.ANLIM 保守充分条件给严格陷俘 | SYS、ANLIM、MINK_FILL、SMOOTH_DOMAIN | 23.1及完整外部经典发展接口；边际升级保持Q²/r²<1 | 有限第一周期特征发展； | `RECCVS/proofs/RECCVS_L023.md` L5–37；`RECCVS/proofs/RECCVS_L023.md` L3–56 |
| L023.FIRST 第一周期精确质量与半径宽度界 | FINITE_CONE23 | 真实锥约束、左端平直完整球面/m1=0；δ足够小的Riccati屏障0≤q≤bδ；E均值正确保q1>0；周期比较q2≤q1 | 满足这些约束的实际有限形成锥；本计算不构造端点根或整入射锥； | `RECCVS/proofs/RECCVS_L023.md` L58–99；`RECCVS/proofs/RECCVS_L023.md` L3–56 |
| L023.BRANCH 充分长指定分支严格陷俘 | L023.FIRST、L023.CHARGE、L023.WIDTH、L023.ANLIM、FLIFT、FRPOS、MINK_FILL | 同一真实端点分支c_m→0、τ_m→τ0、ρ_m→正值；T≥log4，固定b,C0,ρ0；23.6四项逐项兑现；实际经典发展接口有效 | 指定完整Minkowski填充分支；不是全部极端形成解的禁止定理 | `RECCVS/proofs/RECCVS_L023.md` L126–162；`RECCVS/proofs/RECCVS_L023.md` L3–56 |
| L023.MGEOM L021族显式几何长度门槛 | L021.KERNEL、L021.FAMILY、FINITE_CONE23、E023 | μ=3/5、T=1048578、c在指定球；τ∈[τ0/2,5τ0/4]、δ=τ/(mT)、b=2^3201、m≥2^2104156；Riccati屏障和积分约束确满足 | 上述假设下的几何充分条件计算；不保证该m的端点残差有根；移除旧版经L023.FIRST间接引入FLIFT的过强依赖；实际分支应用另见BRANCH | `RECCVS/proofs/RECCVS_L023.md` L140–162；`RECCVS/proofs/RECCVS_L023.md` L3–56 |
| L023.SMOOTH 可选择修复保留陷俘并排除候选 | L023.BRANCH、FSMOOTH、CAUCHY、REPAIR_TO_STRONG、L001.EXCLUDE | 已先获得实际严格陷俘有限成员和共同实现；选足够高固定阶预算，经过REPAIR_TO_STRONG传递后输入误差<ε_trap；实际执行同一修复序列 | 选定有限成员及足够小修复的光滑极限；ε_trap、传递界与指定序列仍未认证；C1锥预算单独不够 | `RECCVS/proofs/RECCVS_L023.md` L163–175；`RECCVS/proofs/RECCVS_L023.md` L3–56 |
| L004.AFFINE 不要求正出射膨胀的仿射聚焦恒等式 | SYS、REG_CENTER、AFFINE_NORM | 实际中心发出；r_s(0)=b>0、s>0处r>0；可允许后续r_s≤0 | 该线全部实际光滑正半径段； | `RECCVS/proofs/RECCVS_L004.md` L7–20；`RECCVS/proofs/RECCVS_L004.md` L35–35；`RECCVS/proofs/RECCVS_L004.md` L5–32 |
| L005.AREA 正膨胀段面积电荷—能量式 | SYS、L004.IDENTITY | r_s>0、Q(0)=0；面积振幅积分实际有定义 | 该实际正膨胀段； | `RECCVS/proofs/RECCVS_L005.md` L20–25 |
| L009.CONTINUE 条件于低阶界的有限矩形延续机制 | SYS、CHAR、SMOOTH_DOMAIN | 共同相容光滑特征边；每个固定有限矩形的 r、Ω²有正下界及低阶导数控制；最高阶线性输运可逐阶延续 | 符合这些条件的有限正半径矩形；本节点不证明所需界； | `RECCVS/proofs/RECCVS_L009.md` L126–140；`RECCVS/proofs/RECCVS_L009.md` L5–44 |
| L014.PREFIX 外边下单个实际前缀的α单调与截面体积界 | SYS、OUTER_INPUT、SMOOTH_DOMAIN、INSEG | 固定外边α_b>0；前缀全部实际存在，入射Raychaudhuri；ν=-αΩ² | 任一实际前缀；不要求其末端为中心； | `RECCVS/proofs/RECCVS_L014.md` L16–31；`RECCVS/proofs/RECCVS_L014.md` L5–22 |
| L015.NEAREDGE c=0分支选取近视界正外边 | L015.NONZERO、L013.OUTER | c=0，因此每个小近视界区间都有实际初始非零值；按L012–13选同一种子的N、η | 中心活到t=1时的c=0分支； | `RECCVS/proofs/RECCVS_L015.md` L23–28；`RECCVS/proofs/RECCVS_L015.md` L5–15 |
| L015.FINITETIME 有限t_end分支的轴线固有长度界 | SYS、I001、INSEG、REG_CENTER、L014.AXIS | t_end<∞；固定t0>0；实际视界在[t0,t_end]光滑且α_H正下界；每个仍正则中心段连接视界 | 不要求中心到t=1；从任意正则中心点算实际剩余长度； | `RECCVS/proofs/RECCVS_L015.md` L108–119；`RECCVS/proofs/RECCVS_L015.md` L5–15 |
| L015.INFINITETIME 无限t_end分支的轴线固有长度界 | L015.OUTER、L014.LIFETIME、I001 | t_end=∞，故中心活到t=1；UΓ随后严格增加，中心在所选b之后 | 同一实际轴线t_end=∞分支； | `RECCVS/proofs/RECCVS_L015.md` L106–106；`RECCVS/proofs/RECCVS_L015.md` L5–15 |
| L018.IDENTITY 中心/正半径端点的ground-state恒等式 | SYS、AFFINE_NORM、SMOOTH_DOMAIN | 真实 V≥0、r_ss+Vr=0；r在区间内部正；中心型需f(0)=0消边项，正半径型用w0抵消左边项 | 两种边界型分别使用；本节点不给实际区间存在性； | `RECCVS/proofs/RECCVS_L018.md` L40–46；`RECCVS/proofs/RECCVS_L018.md` L95–101；`RECCVS/proofs/RECCVS_L018.md` L5–36 |
| L023.CHARGE 第一周期电荷与两初始锥电荷比包络 | FINITE_CONE23、MINK_FILL | 固定实际e=μ、C≥0、R≤1、R(L)=ρ>0、左端Q1=0；完整Minkowski入射锥Q=0 | 指定两初始锥； | `RECCVS/proofs/RECCVS_L023.md` L102–109；`RECCVS/proofs/RECCVS_L023.md` L3–56 |
| L023.WIDTH 中心归一化的物理宽度Δv | FINITE_CONE23、MINK_FILL、AFFINE_NORM | 左端β=q1ρ/t1>0、入射/前段平直；v=2β(t-t_c)、u=U/(2β)；原始Δt不可替代Δv | 同一指定初始两锥的物理归一化； | `RECCVS/proofs/RECCVS_L023.md` L111–124；`RECCVS/proofs/RECCVS_L023.md` L3–56 |
| L018.SCREEN 实际负证书后的条件性临界筛选 | L018.CERT、L001.EXCLUDE、TOPO | 选用CERT的严格负分支；证书属固定光滑正则单端AF约束Cauchy种子；L001有限参考片强拓扑接口成立 | 该已实际认证陷俘候选及其强邻域；正证书或未判不触发筛选 | `RECCVS/proofs/RECCVS_L018.md` L89–91；`RECCVS/proofs/RECCVS_L001.md` L7–13 |
