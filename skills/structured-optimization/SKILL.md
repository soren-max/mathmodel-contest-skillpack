---
name: structured-optimization
description: Formulate and audit GMCM optimization problems before choosing a solver. Use for allocation, scheduling, routing, packing, engineering design, control, or genuine multiobjective decisions; do not use merely because a heuristic could be run.
---

# Structured optimization

先写 `Decision Variables / Objective / Hard Constraints / Soft Constraints / Feasible Region`，并给单位、定义域、约束来源、容差和独立 feasibility checker。Model first; solver second。

按结构选择：解析/闭式 → LP/MILP/convex/CP-SAT → 光滑连续优化 → 真正多目标 → heuristic/metaheuristic。Pyomo 适合 LP/MILP/NLP、多期计划和资源/工程优化；OR-Tools 适合 scheduling、assignment、routing、packing、整数和逻辑约束；`scipy.optimize` 适合小中规模明确连续目标/约束；pymoo 只用于真实冲突目标。

使用 pymoo 前回答：是否真有多个目标；能否把一个目标变为 hard constraint；weighted sum 是否更有决策意义；是否确实需要 Pareto front。否则不要使用 NSGA-II/III、MOEA/D。不得把“优化”等同遗传算法。

结果必须独立执行：逐条 hard constraint、目标重算、边界检查、solver status/gap、敏感性、随机种子稳定性和工程数量级。启发式无严格证据时仅写 `best solution found / near-optimal candidate / recommended solution`，不得称 global optimum。任何约束违反使结果 `BLOCKED`，修复后必须重验。

依赖均按题安装并固定版本；基础环境不默认安装 Pyomo、OR-Tools、pymoo 或额外求解器。

当 `competition_mode: true`，修复建议增加 `estimated_fix_time`、`expected_score_gain`、`risk`、`priority` 与 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH`；优先修 hard constraint、错误目标和不可复现，避免低收益换 solver。
