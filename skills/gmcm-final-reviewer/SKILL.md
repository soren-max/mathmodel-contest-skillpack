---
name: gmcm-final-reviewer
description: Perform the final GMCM/Huawei Cup review of mathematics, experiments, paper narrative, abstract coverage, and claim traceability. Use only for a near-final paper with evidence matrix, verified numbers, rendered output, and question handoffs.
---

# GMCM final reviewer

读取官方题目、已核实当年规则、`materials/gmcm.md`（缺失时回退到 SkillPack 的 `../../rubrics/gmcm.md`）、`../../rubrics/paper_narrative.md`、整合稿与渲染文件、`reports/evidence_matrix.md`、`results/paper_metrics.yaml`、逐问审计/handoff 和复现入口。未验证范围不能当通过，不凭语言流畅度替代证据。本轮内容审查不处理字体、字号、页边距、行距等排版细节。

同时读取 [Evidence-Calibrated Communication Policy](../../rubrics/evidence_calibrated_communication.md)，执行表达分类、重复审查和分级；Evidence > Rhetoric，不能为语气更坚定而删真实限制或改变结论强度。

## Review mode：默认 FULL

`review_mode: full` 是默认，保留下面 A–H 的所有检查与完整报告。
只有 `competition_mode: true` **且用户明确要求快速终审**，才使用 `review_mode: fast`。
临近截止本身不构成切换许可；不额外询问已明确要求 FAST 的用户。

FAST 仅检查这十项：每问是否回答；摘要 PMR；approved paper metrics；method/code consistency；
critical evidence matrix rows；leakage；hard constraints；optimization feasibility；
major causal overclaim；final conclusions vs results。
仅报告 CRITICAL 和 high-value MAJOR（包括缺逐问答案、缺摘要 PMR 等硬门失败），忽略普通 MINOR、
句式微调与不影响结果的轻微重复。不为填满 FULL 表格扩展 FAST 范围。

FAST 报告保留：模式与明确请求依据、已检查/未检查范围、总体 verdict、逐问回答和摘要 PMR/数字来源表、
上述证据检查结果、需保留的真实限制、CRITICAL/高价值 MAJOR 的位置/影响/最小修复/复验条件。
不得把未检查范围写成通过，不声称完成 FULL 审查。FAST 与 FULL 使用相同证据门槛、数字批准、
泄漏/可行性/因果边界；摘要 PMR 缺失仍不得 PASS。
FULL 的全部逐问叙事行通过要求用于 FULL 的完整内容建议；FAST 只能给明确限定于十项的 verdict，
不能借模式省略当前检查范围内的硬门或宣称叙事全面通过。

终审输出仍为 `reports/gmcm_final_review.md`。开头用独立字段记录 `review_mode: full` 或 `fast`、
`verdict: PASS / PASS WITH LIMITATIONS / PARTIAL / BLOCKED` 中的一个实际 verdict，
以及从 `mm final-check --json` 取得、经本次阅读核对的 `artifact_sha256: <实际指纹>`。
没有 mm 时照常审查，明确未绑定机器指纹；不能为了预检绿灯签发 PASS。
任何论文/结果变动后重新核验，不直接复制旧 hash。机器字段不替代下面报告正文。

## A. Mathematical Reviewer

检查问题抽象、状态/决策/参数、假设、公式与维度、边界/约束、模型递进、推导正确性和 solver 选择。

## B. Experiment Reviewer

检查 raw/processed 数据契约、泄漏、baseline、指标/残差、时间/分组切分、随机种子、验证/稳健性、单位/数量级、约束、数值一致和可复现性。可用时吸收 `scientific-critical-thinking`、`statistical-analysis` 与 `uncertainty-and-units` 的通用检查；不新增另一套工作流。

## C. GMCM Competition Reviewer

检查逐问回答、数学深度、多问递进、真实创新、工程意义、图表证据、论文完整性、优缺点和限制。创新不得由算法数量代替；模型复杂度必须由题目结构和证据收益支撑。

## D. PAPER NARRATIVE Reviewer

将每一问视为一条完整论证链，而不是按关键词搜索。逐问检查：

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

必须明确判断并记录：

- 是否像算法拼盘，模型之间是否由逐问产物和数学对象连接；
- 模型介绍是否过长或百科化，是否挤压 formulation、result、validation；
- 是否优先解释 “Why this model for this problem?”，并以结构、数据、机制、约束、输出需求或 baseline 支撑；
- 每个核心公式是否都有 `Before equation / Equation / After equation`，其中后段含变量/单位、数学或工程意义与后续用途；
- 结果是否只有数字而没有原因、含义、证据强度和决策影响；
- 每个核心图表是否都有 `Purpose / Observation / Interpretation / Implication`，而非仅写“结果如图 X 所示”；
- 每问是否以“回答、最重要结果、结论、限制、下一问接口”形成闭环；
- 前后问题是否传递具体产物、schema、单位、适用域和不确定性，形成递进而非换算法；
- 摘要是否只有模型名而没有每问的具体结果；
- 总结是否综合总体答案、权衡、限制与工程价值，而非重复正文句子。

模型介绍的长度按功能判断：若一段通用知识删去后不影响本题的 formulation、选择理由、求解复现或结果解释，则标记为百科式冗余并要求压缩，不以机械字数阈值代替判断。

输出逐问叙事审查表：

```markdown
| Question | Problem & abstraction | Assumptions / variables | Formulation & selection reason | Solver | Result & interpretation | Validation | Conclusion & next link | Status |
|---|---|---|---|---|---|---|---|---|
```

任一环节缺失时不得将该问标为 `PASS`；给出稿件位置、缺失证据和最小内容修复，不提出纯排版修改。

## E. Abstract hard gate

摘要背景保持极短。逐问建立且在报告中原样输出：

```markdown
| Question | Problem | Method | Result | Status |
|---|---|---|---|---|
```

只有 `Problem / Method / Result` 三项全部存在、具体且与正文一致，该问才 `PASS`。Model 是 Method 的一部分，不机械拆成第四项；Meaning / Engineering Value 可增强 Result；Conclusion 可在末尾总体总结，不要求逐问标签。

三要素是信息结构而非固定句式，不要求每问“针对问题 X，本文首先……然后……最终……”。不要为去重复而删除某问必需的 Problem、Method 或 Result。

`Result` 必须给出可验证的数值、最优参数、误差、变化百分比、分类/排名/阈值或工程策略。只有“结果较好”“效果显著”“验证了模型有效性”等表述时按缺失处理。摘要所有关键数字逐个列出 `metric_id`，并核对 `results/paper_metrics.yaml` 的 `approved_for_paper: true`；未批准数字、正文没有的数字或口径冲突均为 `CRITICAL`，不能通过改写掩盖。

紧接摘要硬门表输出数字来源表；没有数字时说明本问 Result 的具体非数值证据：

```markdown
| Question | Abstract number / result | Metric ID or evidence | approved_for_paper | Body/result location | Status |
|---|---|---|---|---|---|
```

## F. Core equation and figure/table audit

核心公式逐式输出：

```markdown
| Question | Equation | Before: relationship reason | Equation/notation check | After: variables/units + meaning + downstream use | Status |
|---|---|---|---|---|---|
```

核心图表逐项输出：

```markdown
| Question | Figure/table | Purpose | Observation | Interpretation | Implication / claim boundary | Provenance | Status |
|---|---|---|---|---|---|---|---|
```

核心对象不得抽样审查。若稿件没有明确编号，使用页码/段落或可重复定位的文字锚点。

## G. Model–result–paper consistency

对论文出现的每个模型名称、参数、样本数、评价指标、最优值、提升/降低百分比和显著性结论建立追溯表：

```markdown
| Claim / value | Type | Manuscript location | Code / config / derivation | Result artifact | Approved metric ID or Evidence Matrix row | Status |
|---|---|---|---|---|---|---|
```

每项都必须到达真实 result 和 Evidence Matrix；模型名称/参数还必须到达代码/config 或数学推导，数值项还必须到达已批准 metric。任一必要链路缺失标 `NOT TRACEABLE`。求解器冒充模型、样本口径不一致、指标定义/分母漂移、无证书的“最优”和无检验的“显著”不得通过。

读取 `../../corpus/derived/abstract_patterns.md`、`paper_structure_patterns.md`、`validation_patterns.md`、`figure_patterns.md`、`reviewer_checklist.md` 作为检查框架。优秀论文 corpus 只允许学习章节组织、数学叙事、结果解释、验证写法和摘要结构；禁止复制或近似改写原文表达，也禁止迁移其结果。

## H. Evidence-calibrated communication review

按共享 Policy 逐项检查并给出证据位置：

- `DEFENSIVE_WRITING`：无技术信息的自我贬低；
- `TEMPLATE_WRITING`：机械连接词、连续相同句式、逐问流水账；有真实顺序的连接词可保留，不强制换词；
- `REPETITIVE_CLAIM`：相同观点换词重复、同一优势多章重复、摘要/正文/结论复制、评价与结论重复、问题分析与建模重复、图前图后重复；
- `ALGORITHM_ENCYCLOPEDIA`：通用算法介绍挤占本题数学模型和选择理由；
- `EQUATION_WITHOUT_NARRATIVE`：核心公式没有前因、解释或实际后续用途；
- `RESULT_WITHOUT_INTERPRETATION`：数字没有数学/工程含义或证据边界；
- `FIGURE_WITHOUT_CLAIM`：核心图表缺 Purpose、Observation、Interpretation 或 Implication；
- `UNJUSTIFIED_POSITIVE_LANGUAGE`：没有指标/比较/验证支持的优越、显著、稳定或因果语言；
- `UNJUSTIFIED_HEDGING`：没有依据的弱化，必须与 `VALID_LIMITATION` 严格区分。

每段至少承担 Problem、Reasoning、Definition、Model、Evidence、Interpretation、Transition、Conclusion 之一；无信息功能的常识、标题复述、赞美和百科内容应删减。按对象、条件、方向、幅度与推断范围归并 semantic claim，记录重复位置，优先保留证据更强、位置合理的一处，其余删除、压缩或改成新信息功能。摘要和结论为完整作答所需的简要重述可以保留。

逐条核对谨慎表达的证据，单列必须保留的 `VALID_LIMITATION` 及其范围、技术原因、后果和条件性 remedy；不用 only、limited、weak、unstable、not significant 等词表自动判错。缺乏机制证据时保留“原因未验证”的边界和已有结果含义，不能为补解释发明原因。结论应给每问答案、关键数字、策略与总体工程意义，保留影响解释的限制，不复制摘要、算法流程或完整验证过程。

输出表达审计与重复处理表：

| Location(s) / semantic claim | Paragraph function | Finding or VALID_LIMITATION | Evidence anchor | Severity | Keep / compress / rewrite / delete and reason |
|---|---|---|---|---|---|

`VALID_LIMITATION` 不是 finding，Severity 为 `—`；证据充分的限制必须保留。未发现问题的类别可在已检查范围中注明，不能为凑类别制造问题。任何修订都复核与 Evidence Matrix、批准 registry、代码/config 和审计边界是否一致，不计算 AI detector 或 AI score。

## Report and verdict

FULL 输出 `reports/gmcm_final_review.md`，至少依次包含（FAST 使用上方限定报告）：总体 verdict、逐问摘要硬门表及数字来源表、逐问 PAPER NARRATIVE 表、核心公式语境审计、核心图表四要素审计、模型—结果—论文追溯表、表达审计与重复处理表、必须保留的 `VALID_LIMITATION`、`CRITICAL / MAJOR / MINOR` findings。每项 finding 包含位置、证据、影响、最小修复和复验条件。

按影响分级：改变证据强度、隐藏负结果、因果过度声明、数字与结果冲突、方法与代码冲突，以及关键数字未批准或核心结论不可追溯，均为 `CRITICAL`；单纯缺一问 Problem/Method/Result、大量算法百科、结果无解释、严重重复或多问叙事断裂是 `MAJOR`；机械连接词、个别句式重复、局部生硬措辞是 `MINOR`。叙事或表达问题若同时改变证据，相关项升为 `CRITICAL`。

等级不替代硬门状态：摘要缺 PMR 为 `MAJOR` 仍不得 PASS。只有全部摘要行和逐问叙事行 `PASS`、无未解决 `CRITICAL`，才可给出内容层面的提交建议；语言流畅不能抵消证据或叙事失败。`CRITICAL` 必修；优先影响作答和解释的 `MAJOR`；`MINOR` 不得破坏稳定结果。

当 `competition_mode: true`，再给 `estimated_fix_time`、`expected_score_gain`、`risk`、`priority` 和 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH`。不要在 MINOR 上花大量时间；缺摘要要素等硬门问题不能因分级为 MAJOR 而忽略。最终模型、数值、引用、格式和提交均需三位 owner 人工复核；此技能不自动提交。
