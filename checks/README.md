# 检查与文件维护

从仓库根目录运行，脚本使用 Python 标准库。

| 入口 | 范围 |
|---|---|
| `update_navigation.py --write` | 根据 Git 已跟踪及未忽略文件刷新研究 FILE_INDEX.md 和当前 FILE_MANIFEST.json |
| `update_navigation.py --check` | 只读核对索引和清单是否与当前文件集合、内容一致 |
| `verify_navigation.py` | 检查当前导航文档中的本地文件链接 |
| `verify_manifest.py` | 校验清单中每个文件的大小和 SHA-256；不判断数学正确性 |
| `reproduce.py` | 复现第七轮辅助剖面和充分门槛，输出到被忽略的 generated/；不覆盖全部后续研究 |
| `PACKAGING_VERIFICATION.json`、`SOURCE_MAP.json` | 10-10 打包验证与来源历史记录 |
| `FILE_MANIFEST_2026-10-10.json` | 原清单按原字节保存，仅作历史证据 |

后续研究的核验脚本仍位于 research/goal_a/，入口见 [研究导航](../research/goal_a/README.md) 和 [复算说明](../REPRODUCE.md)。本目录维护程序不更改研究证据。
