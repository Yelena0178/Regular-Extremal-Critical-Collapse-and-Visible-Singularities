# 复算说明

在仓库根目录执行，建议 Python 3.11 或以上。本次环境版本见 checks/PACKAGING_VERIFICATION.json。

```bash
python3 checks/reproduce.py
python3 checks/verify_manifest.py
```

核心流程仅用 Python 标准库：重新生成 K=8、n=88、σ=1/20 的有理剖面，逐个复算 J 和可行族证书、第一周期门槛；与原 JSON 比较；检查 Python -O 下结果相同；检查 n=44 和篡改输入确实被拒绝。
输出写入 checks/generated/，不会改写原证书。脚本执行时间取决于机器；全程不调用远程数据。

可选核代数检查需要原 requirements-kernel.txt 中的 SymPy：

```bash
python3 -m pip install -r experiments/requirements-kernel.txt
python3 checks/reproduce.py --with-kernel
```

SymPy 检查只核对 L012 显示的核恒等式，不认证其 PDE 控制或延续。本次打包环境无 SymPy，因此没有重新运行这个可选检查；保留原 KERNEL_ALGEBRA_RESULT.txt 作为历史记录。

## 直接运行原脚本

```bash
python3 experiments/freeze_filtered_profile.py --K 8 --n 88 --sigma 1/20 --output checks/generated/profile.json
python3 experiments/certify_filtered_J.py checks/generated/profile.json checks/generated/J_certificate.json
python3 experiments/certify_admissible_profile.py checks/generated/profile.json checks/generated/admissible_certificate.json
python3 experiments/check_first_period_thresholds.py
```

freeze_filtered_profile.py 的原默认 n=44 是失败试算，复算可行族时必须显式指定 n=88。

## 计算范围

通过结果认证相应有限有理代数与充分门槛。光滑截断及 PDE 分支的分析论证仍要阅读正文；没有具体有限振幅非线性根认证、没有实际中心时空演化、没有独立数学审查。

输入形成包自有 REPRODUCE.md 保留其历史作用；本入口不自动将那些检查称为本项目完整定理验证。
