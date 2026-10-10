# GitHub 上传位置说明

## 上传方式

解压交付 ZIP 后得到 RN-Black-Hole-Lab 文件夹。打开该文件夹，把里面的文件与子文件夹放到 GitHub 仓库根目录；不要在仓库里再套一层 RN-Black-Hole-Lab，也不要只上传 ZIP。

例如 README.md 位于仓库首页，proof/01_main_theorem.md 位于仓库的 proof 文件夹。无需更改文件夹名或文件名。若已有旧版 README，先查看并保留需要的作者信息，再用本版内容更新；不要自动删除仓库中无关内容。

优先使用桌面浏览器或电脑 Git 客户端上传整个解压目录。逐个上传时，在相应文件夹位置上传文件，按下表保持路径。仅创建文件的界面适合复制 Markdown；PDF 需要文件上传入口。

## 目录用途

| 目录或文件 | 用途 |
|---|---|
| README.md | 首页、主命题和阅读顺序 |
| proof/ | 当前证明正文 |
| supporting/ | 必要来源原稿和源码选段 |
| checks/ | 可运行脚本、原输出和本次运行日志 |
| review/ | 最新审查状态的来源说明 |
| references.bib | 文献 |
| VERIFICATION.md | 证明状态和审查重点 |
| REPRODUCE.md | 核查运行方式 |
| SOURCE_MAP.json | 文件来源及编辑范围 |
| SHA256SUMS.txt | 此次交付文件摘要 |

## 逐文件位置

| 文件 | GitHub 位置 |
|---|---|
| `.gitignore` | 仓库根目录下同名路径 |
| `README.md` | 仓库根目录下同名路径 |
| `REPRODUCE.md` | 仓库根目录下同名路径 |
| `SOURCE_MAP.json` | 仓库根目录下同名路径 |
| `UPLOAD_GUIDE.md` | 仓库根目录下同名路径 |
| `VERIFICATION.md` | 仓库根目录下同名路径 |
| `checks/PACKAGING_RUN.json` | 仓库根目录下同名路径 |
| `checks/center_and_gluing/RESULTS_NEW.json` | 仓库根目录下同名路径 |
| `checks/center_and_gluing/check_bondi_center_jets.py` | 仓库根目录下同名路径 |
| `checks/center_and_gluing/check_p0_4567.py` | 仓库根目录下同名路径 |
| `checks/center_and_gluing/check_realization_identities.py` | 仓库根目录下同名路径 |
| `checks/expected/center_and_gluing/RESULTS_INHERITED.txt` | 仓库根目录下同名路径 |
| `checks/expected/center_and_gluing/RESULTS_NEW.json` | 仓库根目录下同名路径 |
| `checks/expected/global_development/RESULTS_GA_GB.json` | 仓库根目录下同名路径 |
| `checks/expected/global_identities/RESULTS_GLOBAL.json` | 仓库根目录下同名路径 |
| `checks/expected/smooth_data/RESULTS.json` | 仓库根目录下同名路径 |
| `checks/global_development/RESULTS_GA_GB.json` | 仓库根目录下同名路径 |
| `checks/global_development/check_ga_gb.py` | 仓库根目录下同名路径 |
| `checks/global_identities/RESULTS_GLOBAL.json` | 仓库根目录下同名路径 |
| `checks/global_identities/check_global.py` | 仓库根目录下同名路径 |
| `checks/requirements.txt` | 仓库根目录下同名路径 |
| `checks/run_all.py` | 仓库根目录下同名路径 |
| `checks/smooth_data/RESULTS.json` | 仓库根目录下同名路径 |
| `checks/smooth_data/check_p0.py` | 仓库根目录下同名路径 |
| `proof/01_main_theorem.md` | 仓库根目录下同名路径 |
| `proof/02_smooth_data_and_local_evolution.md` | 仓库根目录下同名路径 |
| `proof/03_regular_center_and_gluing.md` | 仓库根目录下同名路径 |
| `proof/04_global_development_and_horizon.md` | 仓库根目录下同名路径 |
| `proof/05_strict_half_threshold.md` | 仓库根目录下同名路径 |
| `proof/finite_order/01_profile_construction.md` | 仓库根目录下同名路径 |
| `proof/finite_order/02_endpoint_matching.md` | 仓库根目录下同名路径 |
| `proof/finite_order/03_nonlinear_lifting.md` | 仓库根目录下同名路径 |
| `proof/finite_order/04_radius_positivity.md` | 仓库根目录下同名路径 |
| `references.bib` | 仓库根目录下同名路径 |
| `review/current_review_status.md` | 仓库根目录下同名路径 |
| `supporting/center_localization_original.md` | 仓库根目录下同名路径 |
| `supporting/finite_order_original.pdf` | 仓库根目录下同名路径 |
| `supporting/finite_order_source_excerpts/01_framework.tex` | 仓库根目录下同名路径 |
| `supporting/finite_order_source_excerpts/02_necessity.tex` | 仓库根目录下同名路径 |
| `supporting/finite_order_source_excerpts/04_profile.tex` | 仓库根目录下同名路径 |
| `supporting/finite_order_source_excerpts/05_linear.tex` | 仓库根目录下同名路径 |
| `supporting/finite_order_source_excerpts/06_positivity.tex` | 仓库根目录下同名路径 |
| `supporting/finite_order_source_excerpts/07_lifting.tex` | 仓库根目录下同名路径 |
| `supporting/finite_order_source_excerpts/08_global.tex` | 仓库根目录下同名路径 |
| `supporting/source_excerpts/rebuilt_closure_2026-10-08.tex` | 仓库根目录下同名路径 |
| `supporting/source_excerpts/smooth_realization_2026-09-28.tex` | 仓库根目录下同名路径 |
| `SHA256SUMS.txt` | 仓库根目录 |

程序名称中少量旧缩写保持原样，保证运行行为不变。supporting 中 TeX 文件是来源选段，不能独立编译。

本轮新增审查记录：`review/SECOND_REVIEW.md`，放在根目录的 review 文件夹。
