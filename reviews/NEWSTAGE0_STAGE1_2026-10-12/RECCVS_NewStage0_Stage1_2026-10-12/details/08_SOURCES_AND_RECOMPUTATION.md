# 08｜来源、冻结方式与复算记录

**所有数学结论：GPT 主张，未经外部独立审查。** 源文件冻结只证明身份，不证明其中全部解析主张成立。

## 1. 仓库版本

- [阶段3.13提交](https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/commit/41eeeb203b5d773dd77d2fd91019c8233f38ec65)：2026-10-11 19:15:13 UTC。
- [夜间总结提交](https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/commit/60c617abf60393d3ce56cf4cefd50104b3e30fef)：2026-10-11 19:37:01 UTC。本轮读取main时与此SHA相同；所有判断以完整SHA冻结，不依赖今后main变更。
- 时间换算：分别为2026-10-12 03:15:13、03:37:01 Asia/Shanghai，符合用户夜间工作时间。

`verification/REPOSITORY_METADATA.json` 保存两提交元数据和未截断递归Git树。101个用于本轮核查的文本/代码/辅助数据文件列于 `SOURCE_MANIFEST.json`；每个都计算Git对象SHA-1（包含blob头）与SHA-256，逐字节匹配冻结树。已有本地副本只有在Git对象哈希匹配时才采用；8个缺失根文件通过固定提交读取，不按名称当作同一版本。

18个 `reviews/STAGE*` ZIP 均由本地已有交付包与远端Git blob SHA核对后读取。87个Python成员位置、32个不同内容版本记录在 `ARCHIVE_TOOL_INVENTORY.json`；不同版本代码按SHA-256存放于 `tools_from_archives/`。没有为读取这些文本需要重新认证整个旧ZIP的数学内容。

## 2. 主要读取范围

模型D001–D004、L001–L023、形成包证明与有限阶证明、inputs/AUDIT、所有阶段主报告（0到3.13）、阶段1 L023审计、阶段2 Reduced16、阶段3 R02/R03与共同Cauchy实现、夜间总结。字段级状态依具体报告的日期和限制对照，不用根STATUS整段覆盖新报告。

工具作用域审计结合完整脚本文本的AST/依赖/固定路径和参数检查，以及对应证明/报告。不宣称对所有工具每行做了新的正确性证明。

## 3. 外部文献的读取限制

- [An–Lim arXiv:2005.04090v1](https://arxiv.org/abs/2005.04090v1)：本轮版本网页读取失败；针对方程迁移、打印差异和目标域的判断来自**旧阶段1已冻结的逐假设审计**。没有声称本轮重新阅读全文或闭合迁移证明。
- [Kehle–Unger arXiv:2211.15742v2](https://arxiv.org/abs/2211.15742v2)：本轮版本网页读取失败；形成接口判断依据旧冻结来源及其后续审计，不擅自替换版本。
- [Kehle–Unger arXiv:2402.10190](https://arxiv.org/abs/2402.10190)：本轮原作者摘要可读，明确物质模型为Einstein–Maxwell–Vlasov；只据此登记跨模型限制，没有迁移其阈值定理。
- 旧L006引用Kauffman–Lindblad arXiv:2109.03270v2；本轮没有重做外部小数据定理全文审计，只如实沿用L006已明示的未闭接口。

包内没有重打包第三方论文PDF；所需定位来自旧项目主报告和源文引用。数学适用性评估是本GPT主张，非文献作者对新路线的认证。

## 4. 复算入口

解压后在本包目录运行：

```bash
python3 code/exact_recompute.py
python3 code/verify_package.py
```

使用Python标准库，首次运行会更新 `verification/EXACT_RECOMPUTATION.json`。第一入口检查RN质量与根分解、视界mH、质量通量电荷项抵消、号数余量、终态区间/零质量拒绝、未来尾账缺失的证据状态，以及冻结源身份。它不证明存在/唯一性/全未来完备性。

本轮还运行旧仓库的

```bash
python3 sources/checks/reproduce.py
```

日志见 `verification/OLD_CERTIFICATE_REPLAY.log`，完整生成记录在 `verification/old_certificate_replay/`。它复算固定领先剖面、J符号、有理包络和第一周期门槛，普通及Python -O检查吻合，n=44和篡改J输入被拒绝。可选SymPy核项未运行。回归脚本历史报告的 `finite_amplitude_root_certified=false` 描述其自身辅助算术作用域，不否定后续Reduced16根稿。

所有复算都不生成真实时空网格、不证明指定实际陷俘球、不生成新的边界参数或终态数据。
