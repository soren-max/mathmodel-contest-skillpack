# GMCM Paper Narrative Contract

本契约只审查论文内容质量，不审查字体、字号、页边距、行距等排版细节。它服务于 GMCM 逐问作答、数学叙事和证据闭环；任何通用论文工作流不得覆盖本契约。

表达与修订同时执行 [Evidence-Calibrated Communication Policy](evidence_calibrated_communication.md)：Evidence > Rhetoric。自然叙事不能改变证据强度；真实局限和负结果必须保留。连接词、句式、段落功能、跨段重复及修改等级由该 Policy 统一规定。

## Per-question Narrative

每一问的正文必须形成以下可辨认的论证顺序；可以合并相邻小节或使用自然标题，但不得缺失逻辑环节：

```text
Problem
→ Mathematical abstraction
→ Assumptions / Variables
→ Model formulation
→ Model selection reason
→ Solver / computation
→ Numerical results
→ Interpretation
→ Validation
→ Question conclusion
→ Link to next question
```

- `Problem`：明确该问要求交付的对象、范围、输入和输出。
- `Mathematical abstraction`：把工程对象映射为状态、集合、图、函数、随机过程、可行域或其他数学对象。
- `Assumptions / Variables`：给出必要假设及适用边界，区分状态变量、决策变量和参数，并注明定义域、索引与单位。
- `Model formulation`：先写数学关系、目标、约束、初边值条件或统计生成机制，再谈求解器。
- `Model selection reason`：优先回答 “Why this model for this problem?”；用问题结构、数据条件、机制、约束、输出需求和 baseline/备选路线解释选择。
- `Solver / computation`：只说明怎样计算当前模型所需的关键步骤、参数来源、停止条件、状态和复现入口。不得写与本问选择无关的百科式算法史、分类或大篇原理介绍。
- `Numerical results`：给出直接回答题目的结果、单位、比较口径及证据位置。
- `Interpretation`：解释结果为何出现、数学或工程上意味着什么，以及证据允许何种强度的结论。
- `Validation`：使用与问题类型匹配的 baseline、残差、留出/分组/时间切分、灵敏度、鲁棒性、可行性重算、守恒/极限检查或其他独立证据。
- `Question conclusion`：明确本问答案、最重要数值结果、结论、限制，以及对下一问的支撑。
- `Link to next question`：指出传递给下一问的具体产物、schema、单位、适用域和不确定性；最后一问则连接总体结论与建议。

只有算法名称列表、彼此无关的模型堆叠或未传递产物的逐问拼接，均视为“算法拼盘”，不能通过本契约。

原因或机制未经验证时，区分直接观察、证据支持的含义和待验证解释，明确未知范围；不能为补全 Interpretation 编造机制或升级为因果结论。

判断模型介绍是否过长时，检查段落能否改变本题的 formulation、选择理由、求解复现或结果解释；删去后四者均不受影响的通用算法知识应删除或压缩。篇幅本身不是唯一标准，和当前问题的功能关系才是标准。

## Equation Context

每个核心公式都必须形成三段式：

1. `Before equation`：说明为什么需要建立该关系，以及它对应哪个问题机制、约束或推断目标。
2. `Equation`：给出数学表达，符号与上下标一致。
3. `After equation`：解释变量、索引、定义域与单位，说明数学/工程意义，并指出该式随后如何进入估计、仿真、优化、验证或下一问。

孤立公式、连续公式后统一补一段泛化解释、只给符号表而不解释当前关系、以及没有后续用途的公式堆砌均不通过。公式数量不代表数学深度；关系的必要性、可计算性和可验证性才构成数学叙事。

## Figure and Table Context

每个核心图表在正文或图注附近必须回答：

- `Purpose`：为什么需要该图表，它检验或回答什么。
- `Observation`：读者从图表中直接看到的趋势、比较、异常、区间或关键数值。
- `Interpretation`：该观察在模型或工程语境中的含义。
- `Implication`：它支持哪个结论、决策、验证结果或后续步骤，以及不支持什么。

只写“结果如图 X 所示”、复述坐标轴、只报数字不解释，或给出图表却不落到问题答案，均不通过。核心图表还必须能追溯到生成脚本、输入数据/结果与对应 claim。

图表解释与决策含义均受 Evidence Matrix 约束，不能由单一观察补造原因。图前说明目的、图后解释证据即可，不必在两处复述同一结论。

## Per-question Conclusion

每一问末尾必须明确覆盖五项：

1. 本问回答了什么；
2. 最重要且已核实的数值或其他具体结果；
3. 由结果支持的结论；
4. 已观察到的限制或适用边界；
5. 如何以具体产物支撑下一问，或在最后一问支撑总体建议。

结论段应综合答案、证据强度、权衡和适用边界，不能只是逐句重复结果段。

## Abstract Hard Gate

摘要背景控制在极短范围。对每一问，最高优先级且不可缺少的只有三项：

1. `Problem`：针对什么问题；
2. `Method`：建立或采用什么方法解决；模型属于 Method，不机械拆成第四项；
3. `Result`：最终得到什么具体、可验证的结果。

`Interpretation / Meaning / Engineering Value` 可以在 Result 后增强。`Conclusion` 可以在摘要末尾总体总结，不要求每问重复独立的 Conclusion 标签。验证方法可以增强可信度，但不替代三项硬要求。

PMR 是信息结构，不是固定句式；自然组织内容，不要求每问套“针对问题 X，本文首先……然后……最终……”。

Result 优先给出数值、最优参数、误差、提升/降低百分比、分类结果、排名、阈值或工程策略。只有“结果较好”“效果显著”“验证了模型有效性”等无具体结果的表述，按 Result 缺失处理。

终审必须逐问输出且仅按下表判定：

| Question | Problem | Method | Result | Status |
|---|---|---|---|---|

只有 `Problem / Method / Result` 三项全部存在且与正文一致，该问才 `PASS`。摘要中的所有关键数字必须逐项引用 `results/paper_metrics.yaml` 中 `approved_for_paper: true` 的 `metric_id`；未批准、冲突或无法追溯的数字必须删除或先回到上游核验，不得用更好看的数字替换。

单纯缺少 PMR 要素属于 `MAJOR`，仍不通过摘要硬门；关键数字未批准/冲突、证据强度改变或核心 claim 不可追溯属于 `CRITICAL`。删除问题数字后若 Result 不再具体，仍须回到上游补齐结果，不得空缺放行。

## Traceability Contract

论文中的模型名称、参数、样本数、评价指标、最优值、提升/降低百分比和显著性结论都必须有可定位来源：

```text
paper claim
→ reports/evidence_matrix.md entry
→ code/config or derivation
→ result artifact
→ verified metric when numeric
```

- 每项都必须关联真实 result artifact 与 Evidence Matrix；数值 claim 还必须关联 `results/paper_metrics.yaml` 中已批准的 `metric_id`。
- 模型名称和参数必须与真实代码、配置或数学推导及实际运行结果一致；求解器不得冒充模型。
- 样本数必须与实际数据筛选和切分记录一致。
- 评价指标必须保留定义、方向、分母、聚合、单位和适用数据集。
- “最优”必须有最优性证书/界或降级为证据允许的措辞；“显著”必须有对应检验、效应量和适用条件。
- 任一链路缺失时标记 `NOT TRACEABLE`，不得仅凭 handoff、摘要或流畅文字放行。

## Exemplar Corpus Boundary

优秀论文 corpus 只用于学习章节组织、数学叙事、结果解释、验证写法和摘要结构。不得复制或近似改写原文表达，不得迁移其数据、结果、公式编号、专有命名或未经当前题目证据支持的结论。最终文字必须由当前题目、当前模型和当前证据重新生成。
