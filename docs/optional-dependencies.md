# Optional Dependencies

基础安装只要求 Bash、Git 和 Python 标准库；`mm-init` 不安装科学包。所有可选依赖在具体比赛项目的隔离环境中按题安装、固定版本并记录锁文件。

| Dependency | Use when | Do not use merely because |
|---|---|---|
| statsmodels | OLS/GLM/ARIMA、可解释统计 baseline、残差与推断 | 题目出现“预测” |
| Pandera | 多表或长期复用的数据契约值得声明式验证 | 简单 assertions 已足够 |
| Pyomo | LP/MILP/NLP、多期计划、资源或工程优化 | 想把模型写得“高级” |
| Google OR-Tools | 调度、指派、路径、装箱、整数/逻辑约束、CP-SAT | 任意连续参数拟合 |
| scipy.optimize | 小中规模连续目标与明确约束 | 离散调度/路由 |
| pymoo | 真实冲突多目标且确需 Pareto front | 一个目标可自然成为硬约束 |
| SHAP | 已验证的 ML 模型确需全局/局部归因 | 模型预测能力差或需要因果解释 |
| SimPy | 队列、服务、制造、物流、通信竞争、维修或事件调度 | 题目仅含时间变量 |

SHAP attribution 不等于 causal effect。SimPy 研究需定义实体、资源、事件、时钟单位、终止条件、warm-up、独立重复和验证。Pyomo/OR-Tools 还需单独确认可用 solver；工具安装成功不等于模型正确。

## 按题启用 SHAP / SimPy Skill

普通 `install.sh` 会把它们所在的固定提交缓存到 `scientific-agent-skills`，但不会创建这两个 Skill 的全局链接。确有需要时，先确认项目 `.agents/skills/<name>` 不存在，再把缓存中的单个 `skills/shap` 或 `skills/simpy` 目录链接到当前项目；记录 pinned commit，并在比赛开始后冻结。不要链接该上游的整个 `skills/` 目录。Python 包仍需在项目隔离环境中单独安装。
