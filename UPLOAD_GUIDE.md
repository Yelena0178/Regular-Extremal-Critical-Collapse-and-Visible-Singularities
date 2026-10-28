# 获取、同步与引用仓库

实际仓库：[RECCVS](https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities)。2026-10-28 核对时，默认分支 `main` 为 `3d5bf6b`；R31 成果在 `codex/goal-a-research-2026-10-16`，已同步提交 `1f4f888`，通过[草稿 PR #5](https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities/pull/5)组织审查。

## 获取当前研究材料

```bash
git clone --branch codex/goal-a-research-2026-10-16 https://github.com/Yelena0178/Regular-Extremal-Critical-Collapse-and-Visible-Singularities.git RECCVS
cd RECCVS
git status --short --branch
```

若已克隆但只跟踪 main，可显式获取研究分支：

```bash
git fetch origin refs/heads/codex/goal-a-research-2026-10-16:refs/remotes/origin/codex/goal-a-research-2026-10-16
git switch codex/goal-a-research-2026-10-16
```

切换前先保存已有本地改动。Windows 上若历史包路径触及长度限制，可使用 `git -c core.longpaths=true clone ...`。不要因路径报错而删去历史证据。

## 字节完整性与恢复

执行 [REPRODUCE](REPRODUCE.md) 的只读检查。`.gitattributes` 固定现有文件的换行约定；不得对已归档证据统一格式化、转换换行或重写 JSON。新文件的检出字节也须与清单相符。

R31 原科学记录与当轮导航均可从 `1f4f888` 恢复；该提交包含同步所需的换行属性。后续导航调整及旧检查点兼容方式见[维护记录](checks/REPOSITORY_AUDIT_2026-10-28.md)。缓存、自动生成检查输出及被忽略的第三方网页不属于原创研究成果清单；第三方论文按[版本化来源](literature/SOURCES.md)获取。

## 更新与引用

维护步骤见 [task-rules](task-rules.md)。提交前刷新索引、清单并检查证据收据；推送至当前研究分支后核对远端 SHA，更新现有 PR 的范围说明。合并状态以 GitHub 为准。

[CITATION.cff](CITATION.cff) 的 `0.1.0 / 2026-10-10` 是早期快照元数据，不是 R31 的新版本发布。引用后续材料须同时给出提交 SHA、研究稿编号和日期。许可仍按 [LICENSE_NOTICE](LICENSE_NOTICE.md)，不因本次整理更改。
