---
name: paper-handoff
description: Turn an audited GMCM question into a paper-ready mathematical narrative and evidence handoff with traceable formulas, results, figures, validation, conclusions, and exact permitted paper numbers. Use when a question is ready for writing or its results have changed.
---

# Paper handoff

先完整读取 `../../rubrics/paper_narrative.md`，再读取该问题意、路线、代码入口、实际结果、图表、`reports/evidence_matrix.md`、`results/paper_metrics.yaml` 和审计。目标是让论文负责人直接获得一条“问题 → 数学抽象 → 模型 → 结果 → 解释 → 验证 → 结论”的写作证据链，而不是算法说明书。

同时读取 [Evidence-Calibrated Communication Policy](../../rubrics/evidence_calibrated_communication.md)，将证据允许的表达范围交给论文负责人；Evidence > Rhetoric。

若审计为 `BLOCKED` 或关键证据缺失，可生成标明“草稿/不可用于论文”的交接清单，但不能放行关键数值或正式 claim。审计未做时先核验或建议调用可用的 `result-auditor`。不得用 handoff 自我证明结果。

写入 `notes/handoff_qN.md`；已有版本保留修订依据，结果改变后同步更新。文件元数据标明题号、交付人、审查人、版本、审计状态、对应 run/config 和更新时间。论文负责人不应从代码重新猜测结果。

## Question narrative packet

每一问按以下顺序交付真实内容，不能保留占位文字：

```markdown
# Problem
# Mathematical Abstraction
# Assumptions / Variables
# Model Formulation
# Model Selection Reason
# Solver / Computation
# Numerical Results
# Interpretation
# Validation
# Question Conclusion
# Link to Next Question
# Reproduction and Provenance
# Formula Context Ledger
# Figure and Table Evidence Ledger
# Abstract-ready Problem–Method–Result
# Traceability and Claim Boundaries
# Open Issues and Owners
```

叙事顺序的内容要求以 `paper_narrative.md` 为硬门槛。尤其：

- `Model Selection Reason` 必须先回答 “Why this model for this problem?”：连接问题结构、数据条件、机制/约束、输出需求、baseline 或备选模型；不得用百科式算法介绍代替选择理由。
- `Solver / Computation` 只保留求解当前 formulation 所需的步骤、参数来源、停止条件与 solver 状态，区分模型和求解器。
- `Numerical Results` 给出对题目有用的结果、单位、比较口径、`metric_id` 和结果位置；负结果或弱证据不得隐藏。
- `Interpretation` 解释结果产生的原因、数学/工程意义以及证据边界，不能只换一种说法复述数字。
- `Question Conclusion` 必须逐项写清本问答案、最重要结果、结论、限制、对下一问的支撑；最后一问连接总体建议。
- `Link to Next Question` 必须交付实际传递的产物、schema、单位、适用域和不确定性；没有递进关系时明确暴露结构问题，不能虚构连接。

## Formula context ledger

每个核心公式各占一行：

```markdown
| Formula ID | Before equation: why this relation | Equation | After equation: variables/units + meaning + downstream use | Derivation/evidence anchor | Status |
|---|---|---|---|---|---|
```

只有 `Before equation / Equation / After equation` 完整且符号与正文一致才可标 `READY`。孤立公式、公式堆砌或只给统一符号表均标 `NOT READY`。

## Figure and table evidence ledger

每个核心图表各占一行：

```markdown
| ID / path | Purpose | Observation | Interpretation | Implication / claim boundary | Generator + source result | Status |
|---|---|---|---|---|---|---|
```

不得以“结果如图 X 所示”作为图表分析。`Observation` 写图表直接呈现的事实，`Interpretation` 写其含义，`Implication` 写它支持和不支持的结论。记录生成脚本、数据/结果来源、样本/场景、单位和正文落点。

## Abstract-ready packet

为本问只生成一行：

```markdown
| Question | Problem | Method | Result | Approved metric IDs / evidence | Status |
|---|---|---|---|---|---|
```

`Problem / Method / Result` 是摘要硬要求；模型包含在 `Method` 中，不另拆字段。`Result` 必须具体、可验证；只有泛化评价时标 `NOT READY`。摘要关键数字必须逐个关联 `approved_for_paper: true` 的 `metric_id`。Meaning / Engineering Value 可作为 Result 后增强，但不能代替 Result。

PMR 是信息结构，不是句式模板；摘要可自然组织，不要求逐问使用“针对问题 X，本文首先……然后……最终……”。来源与状态列是审计元数据，不是新增摘要必备要素。

## Reproduction, traceability, and claims

`Reproduction and Provenance` 提供从项目根目录执行的真实命令、输入版本/校验和、环境、种子、配置和输出位置。没有实际运行的命令标记为待运行。

为论文拟出现的模型名称、参数、样本数、评价指标、最优值、提升/降低百分比和显著性结论逐项建立 traceability ledger，至少列出：论文 claim、类型、code/config/derivation、result artifact、`metric_id`（数值项）、Evidence Matrix 行、允许措辞和状态。缺少任一必要链路时标 `NOT TRACEABLE`。

所有数值只从 `results/paper_metrics.yaml` 中 `approved_for_paper: true` 的条目放行，不得另行抄 CSV 或临时重算后写入。`Exact Claims Allowed` 必须由当前 Evidence Matrix 支持；冲突、未批准数字、无检验的显著性、无证书的全局最优及越过相关/预测证据的措辞写入 `Claims NOT Allowed`。

在 `Traceability and Claim Boundaries` 内交付以下表达范围表，逐 claim 定位，不另造数字来源：

| Claim / Evidence Matrix row | Exact Claims Allowed | Claims NOT Allowed | VALID_LIMITATION to retain | Technical reason / consequence / possible remedy |
|---|---|---|---|---|

允许措辞保留指标、比较、方向、幅度、已验证的稳定性与适用域。真实限制按 `Scope → Technical reason → Consequence → Possible remedy` 组织，remedy 仅是条件性后续方案。负结果、弱关联及不确定性不能在交接时变成积极结论；无信息的自我贬低可删除。

图表与结果解释均受 Evidence Matrix 约束；无法验证原因时，交付已支持的含义及机制未知的边界，不能为完成叙事编造原因。正文段落各有信息功能，算法背景仅保留本题所需；结论综合最终答案、关键数字和工程策略，避免机械复制摘要或验证过程。

优秀论文 corpus 仅可学习章节组织、数学叙事、结果解释、验证写法和摘要结构；不得复制或近似改写原文。限制与审计要求原样传递给 L，末尾列出待决策问题及负责人。

若下游明确使用 PaperSpine，把本 handoff 作为 materials 中的逐问 source of truth：叙事链进入 section blueprint，公式账本和图表账本进入逐单元 writing rationale，Evidence Matrix/追溯账本进入 evidence bank 与 claim register，摘要行进入逐问 PMR 审计。PaperSpine 不得重新猜数、重新选模或覆盖 GMCM 内容门槛，其产出仍须经过 `gmcm-final-reviewer`。
