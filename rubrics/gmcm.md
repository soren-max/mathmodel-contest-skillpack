# GMCM Stable Rubric

适用于中国研究生数学建模竞赛的长期稳定审查逻辑。每项记录 `PASS / PARTIAL / FAIL / NOT FOUND / NOT APPLICABLE` 及证据位置；当年页数、格式、提交和特别规则只从 `gmcm_year_override.md` 读取。

## Problem Understanding

- 是否逐问回答并交付题目要求的数字、方案、解释或文件。
- 是否把实际/工程问题正确抽象为数学对象。
- 输入、输出、观测时点、粒度、单位和问题边界是否明确。
- 图、网络、状态、集合、曲线、随机过程或可行域等数学对象是否定义清楚。

## Mathematical Modeling

- 是否定义 state variables、decision variables、parameters 和 assumptions。
- 是否写出核心数学关系、目标函数、硬/软约束、边界/初始条件。
- 模型是否具有可推导、可计算、可验证的数学实质，而非算法名称列表。
- 符号、定义域、维度和前后问接口是否一致。

## Model Selection

- 为什么模型适合当前题目与机制？
- 为什么当前样本量、标签、粒度、独立性和范围支持它？
- 最简单可信 baseline 是什么，是否按同一口径运行？
- 输出是否能服务后续问题，误差与不确定性如何传递？

## Multi-question Progression

- Q1→Q2→Q3→… 是否传递明确产物，而非每问更换无关算法。
- 优先检查：parameter identification→model→prediction→optimization；mechanism→simulation→optimization；data relationship→surrogate→constrained decision；state estimation→control/scheduling。
- 每个接口是否记录 schema、单位、时间/空间尺度、适用域和不确定性。

## Computation

- 代码是否真实运行，入口、输入版本、配置、环境和输出能否定位。
- 参数、随机种子、停止条件和 solver 状态是否有依据。
- 结果能否由命令重现；是否检查数值容差、收敛和稳定性。
- 失败运行、负结果与人工修改是否完整披露。

## Validation

- 按问题类型检查 baseline、holdout、time/group split、residual、error metrics、model comparison、sensitivity、robustness、perturbation、simulation、feasibility 和 engineering plausibility。
- 数据预处理是否只在训练数据拟合；是否存在 temporal/target/group leakage。
- 指标定义、方向、分母、单位、聚合和置信区间是否正确。
- 没有必要验证时必须说明为什么不适用，不能伪装为已通过。

## Optimization

- decision variables、objective、hard/soft constraints 和 feasible region 是否先于 solver 定义。
- solver 是否匹配解析、LP/MILP/CP/凸、连续、多目标或启发式结构。
- 是否独立重算目标、逐条检查约束、检查边界并记录 gap/status。
- 是否完成 post-optimality、敏感性、鲁棒性和工程可行性检查。
- 无严格证据时仅称 `best solution found`、`near-optimal candidate` 或 `recommended solution`。

## Innovation

- 创新优先来自问题抽象、模型结构、数据与机理结合、新约束、指标、求解设计、验证设计和工程解释。
- “采用较新算法”本身不构成创新；复杂模型没有可靠增益时不得宣称明显更优。

## Engineering Value

- 结果是否转化为参数建议、运行策略、控制/调度方案、风险判断或工程解释。
- 建议是否位于已验证范围，单位、数量级、安全边界和实施条件是否合理。
- 相关、关联、预测与因果是否严格区分。

## Paper Quality

- 是否按 `paper_narrative.md` 形成逐问的 Problem → abstraction → formulation/selection → computation → result/interpretation → validation → conclusion → next-question 闭环。
- 摘要是否逐问包含硬要求 Problem、Method、Result；只有三项全部存在才通过。Model 属于 Method，Meaning 可增强 Result，但不能代替具体结果。
- 摘要所有关键数字是否逐项来自 `approved_for_paper: true` 的 registry 条目；“效果良好”等无具体结果的表述按 Result 缺失处理。
- 核心公式是否具有建立理由、数学表达、变量/意义/后续用途三段语境，避免公式堆砌。
- 核心图表是否具有 Purpose、Observation、Interpretation、Implication，避免只写“如图所示”。
- 公式、变量、图表、正文、结论和 handoff 数值是否一致。
- 模型名称、参数、样本数、评价指标、最优值、变化百分比和显著性结论是否可追溯到 code/config/derivation、result、Evidence Matrix 及适用的批准 metric。
- 每张正文图是否有 Evidence Purpose：EDA / MECHANISM / MODEL / RESULT / VALIDATION / SENSITIVITY / OPTIMIZATION / DECISION。
- 无法支持 claim 的图标记 `DECORATIVE_FIGURE` 并移除或降级。
- 模型介绍是否优先回答 “Why this model for this problem?”；算法数量和百科式介绍不得代替数学叙事。
- 优秀论文 corpus 是否只用于学习组织与论证方式，且没有复制或近似改写原文表达。
- 限制、引用、复现说明、匿名/格式和 AI 使用披露是否满足已核实的当年规则。
