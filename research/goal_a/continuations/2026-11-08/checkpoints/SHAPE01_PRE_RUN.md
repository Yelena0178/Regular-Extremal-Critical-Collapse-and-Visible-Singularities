# SHAPE01 运行前检查点
2026-11-08；源版本 53681923，解析证明 proofs/SHAPE01.md，初值实现核验 results/SHAPE_INITIAL_CHECKS.json 已通过（有限浮点核对，非 PDE 认证）。
输入仅 eta=-0.5,+0.5；T=15；512 scout 后各自选择事件射线，512/1024 trace。已有结果禁止覆盖。
命令：python -X utf8 computations/shape_probe.py --eta -0.5 --steps 512 --output results/SHAPE_M_SCOUT_N512.json
正侧改 eta=0.5、文件 M 改 P。trace 追加 --scout 对应文件，输出改 TRACE_N512/N1024。
运行前输入、源码和证明已保存；每次进程日志在 logs/，结果含环境/源码哈希/失败状态。演化器不支持步中恢复，若中断则该单次运行从头重启；已完成的其他输入不重跑。
所有 A1–A6 仍 OPEN。完整 Goal A 不因初值证明完成。
