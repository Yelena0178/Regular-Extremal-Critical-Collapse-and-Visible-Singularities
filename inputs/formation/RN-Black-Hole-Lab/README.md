# 光滑球对称塌缩至极端 Reissner–Nordström 黑洞

研究证明稿，2026-10-08。尚待外部独立逐行审查。

本仓库收录球对称无质量 Einstein–Maxwell–带电标量场系统的主定理证明稿及必要依赖。现有稿为各环节写出论证；这不等于主定理已获独立验证。有限代数检查不认证解析估计、无穷阶收敛、PDE 存在性或全局因果结论。

## 主命题

按正文的方程归一化、解类及列明的构造与适定性假设，对每个 M>0、|e|M>1/2，现有稿构造同一份光滑球对称初始数据：初始空间为 R³，中心正则、单端渐近平坦、空间度量完备。其最大未来整体双曲发展具有完整未来零无穷远和非空黑洞区；事件视界从真实正则中心事件发出，有限先进时间之后，整个外部与视界精确为质量 M、电荷绝对值 M 的极端 RN。初始面位于可向零无穷远发送信号的区域；一般闭曲面结论按主稿中的严格定义与文献假设理解。

必要性证明针对正文明确规定的同一视界类，提出严格 |e|M>1/2 与等号不可达。上述充分性和必要性均处于待独立验证的内部证明稿阶段。实际黑洞内侧不要求电真空；光滑性不包括未来奇异边界的延拓。

## 阅读顺序

1. [主定理与总体论证](proof/01_main_theorem.md)
2. [剖面构造](proof/finite_order/01_profile_construction.md)、[端点匹配](proof/finite_order/02_endpoint_matching.md)、[非线性提升](proof/finite_order/03_nonlinear_lifting.md)、[半径正性](proof/finite_order/04_radius_positivity.md)
3. [同一光滑数据与局部演化](proof/02_smooth_data_and_local_evolution.md)
4. [四维正则中心、RN 接合与顶点填充](proof/03_regular_center_and_gluing.md)
5. [全局发展、外部覆盖与事件视界](proof/04_global_development_and_horizon.md)
6. [严格半阈值必要性](proof/05_strict_half_threshold.md)

证明依赖和审查重点见 [VERIFICATION.md](VERIFICATION.md)。检查运行方式见 [REPRODUCE.md](REPRODUCE.md)。逐文件位置与上传步骤见 [UPLOAD_GUIDE.md](UPLOAD_GUIDE.md)。

## 来源、编排和辅助工作

证明稿由已有项目材料整理，AI 参与推导、编码与编辑；此次整理未进行独立数学认证。已去掉阶段任务代号，改为数学主题，未据此提升原证明状态。详细原始文件映射见 [SOURCE_MAP.json](SOURCE_MAP.json)。历史阶段文字不代表当前仍保留同名缺口，当前状态见 VERIFICATION.md。

文献见 [references.bib](references.bib) 及各章末尾。第三方论文使用引用链接，不随仓库再分发。当前未指定对全部内容统一适用的开放许可证；公开范围和再使用许可是不同决定。
