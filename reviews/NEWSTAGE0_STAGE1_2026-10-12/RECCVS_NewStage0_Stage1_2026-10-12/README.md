# RECCVS 新阶段0核心规格 / 新阶段1首项

**所有数学结论：GPT 主张，未经外部独立审查。**

主报告：`RECCVS_NewStage0_Stage1_2026-10-12.md`。详细定义、误差、验收身份限制、陷俘推导、逐项复用、自审和来源分别见 `details/01`–`08`。

本包没有新PDE演化或真正临界曲线。11:05原计划全文未取回，2–9编号映射待核。旧ψ0条件固定，指定实际严格陷俘未无条件认证。

```bash
python3 code/exact_recompute.py
python3 code/verify_package.py
```

第一入口只核有限代数、证据状态和来源身份。第二入口核包字节。旧辅助回归：`python3 sources/checks/reproduce.py`；它在sources/checks/generated写生成输出，原冻结源不改动。归档工具有些依赖旧完整包的数据和第三方库，清单已逐项记录，不把所有归档脚本声称为本包独立运行入口。
