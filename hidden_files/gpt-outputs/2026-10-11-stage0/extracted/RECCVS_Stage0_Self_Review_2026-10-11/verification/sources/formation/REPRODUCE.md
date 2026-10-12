# 运行检查与阅读来源

在仓库根目录运行：

```sh
python3 -m pip install -r checks/requirements.txt
python3 checks/run_all.py
```

使用 Python 3，SymPy 固定为 1.14.0。脚本无外部数据下载。各检查在自身文件夹中运行并写入自身输出文件；运行器把 stdout/stderr 和退出状态写入 checks/PACKAGING_RUN.json。

| 文件夹 | 检查范围 |
|---|---|
| checks/smooth_data/ | Maxwell 补充恒等式、Einstein 残差、Jacobian 和有限阶分部积分 |
| checks/center_and_gluing/ | 有限中心 jets、极坐标公式、奇偶 pivot、RN 恒等式及误差预算 |
| checks/global_identities/ | RN 与严格门槛的有限代数关系；原脚本中的历史状态不代表当前状态 |
| checks/global_development/ | 依赖域屏障、尾部和归一化的有限公式 |

checks/expected/ 保留来源包的输出，供比较。符号表达式的显示可能随环境变化，不应只按字符串判断数学一致性。

正文以 Markdown 为当前阅读版本。supporting/finite_order_original.pdf 是旧有限阶证明的来源，不是合并后的光滑主定理 PDF。supporting/finite_order_source_excerpts/ 是七份源码选段，不能独立编译；它们的完整论证以原 PDF 和当前有限阶章节共同核对。supporting/center_localization_original.md 是中心估计原稿，已注明排版 ie,gQ 应读作 ie gQ；后续修补见当前局部证明。
