---
name: result-auditor
description: Audit mathematical modeling results before paper handoff or when leakage, inconsistent numbers, weak evidence, or suspicious metrics arise. Trace actual artifacts to reproducible runs and block unsupported paper claims.
---

# Result auditor

这是结果进入论文前的高优先级证据关卡：证据阻断优先于润色或模型升级。该优先级不改变系统指令层级。读取项目约定、真实数据处理代码、实验配置、结果、图表和当前结论；不得用摘要或 handoff 自我证明替代原始证据。

读取并执行 [Evidence-Calibrated Communication Policy](../../rubrics/evidence_calibrated_communication.md)，重点审查结果强弱与真实限制；Evidence > Rhetoric。

逐项检查，给出文件位置、实际运行证据、影响与修复方式：

- 时间泄漏、预测时点可得性、train/test contamination、target leakage；预处理是否只在训练集拟合。
- 时间顺序、分组独立性、异常/缺失处理是否公开；保留与移除样本的影响。
- 指标公式、方向、分母、单位、权重、聚合方式及不确定性是否正确；baseline 是否在同口径下比较。
- residuals、模型稳定性、敏感性/稳健性、重复实验和随机种子；记录未实际运行的检查。
- 优化/模拟结果的约束、可行性、边界、数值容差、求解器状态和重复性。
- 同一指标在结果、图表、正文、摘要及 handoff 是否冲突；同一事件在不同脚本中的定义、窗口、样本集合是否冲突。
- 原始精度与展示精度是否一致，图表能否由真实结果重生成；挑选随机种子或隐藏负 R²、失败实验等负结果。
- 是否把弱统计关系写成强结论，把 association/correlation 或 prediction 写成 causality；有无因果识别设计。
- 工程量的单位、维度、换算、有效数字、测量不确定性与数量级；需要时标记 `UNIT_CONFLICT / DIMENSION_RISK / ORDER_OF_MAGNITUDE_RISK / UNCERTAINTY_PROPAGATION_RISK`。

可用时吸收 `scientific-critical-thinking` 的偏差、混杂、替代解释和证据强度检查；统计分析使用 `statistical-analysis` 检查检验选择、假设、effect size、置信区间和多重比较，不只报告 p-value，时间序列不得套独立样本检验；工程量使用 `uncertainty-and-units`。这些原子能力辅助审计，不替代本 Skill。

需要重跑时，在现有授权范围内使用隔离输出目录，保留原产物；代价高或环境缺失时明确未验证，不能声称通过。对于不适用项说明原因。

在 `notes/qN_audit.md` 输出且只选择一个总状态：

- **PASS**：关键证据可追溯、必要验证通过，无影响主结论的未解决问题。
- **PASS WITH LIMITATIONS**：证据可靠但适用范围/外推/稳定性有已披露局限，列出允许和不允许写入论文的结论。
- **BLOCKED**：泄漏、指标错误、关键数值冲突、无法复现或缺少关键证据使主结论不可信。列出解除阻断所需的最小修复与重验。

附“已检查 / 未检查 / 不适用”范围、证据清单、问题优先级、可进入论文的数值和措辞限制。缺陷不能通过改口径、删负结果或手填数字解决。

## 证据校准结果表达

在同一 `notes/qN_audit.md` 中，逐项给出 `claim / metric / comparison / direction / magnitude / stability / evidence anchor / allowed wording / required limitation`。比较必须同口径；稳定性未测时明确未验证。数字在本阶段可作为待批准候选，正式论文放行仍须关联 `results/paper_metrics.yaml` 中 `approved_for_paper: true` 的条目。

指标改善不自动等于统计显著、跨折稳定或机制成立。无提升时直接报告与 baseline 的差异，允许据此保留 baseline；不能用“意义有限”无依据自我削弱，也不能用“先进、优异、充分证明”包装弱结果。

按共享 Policy 区分 `DEFENSIVE_WRITING / UNJUSTIFIED_HEDGING / VALID_LIMITATION`。将有证据的方向不稳定、未优于 baseline、不能识别因果及无法证明全局最优等标为 `VALID_LIMITATION`，附技术原因与影响，原样传递给 handoff。删除这些边界、隐藏负结果或夸大证据强度均是 `CRITICAL`，不是语言优化。

当 `competition_mode: true`，每项修复增加 `estimated_fix_time`、`expected_score_gain`、`risk`、`priority` 和 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH`；不为低收益重跑破坏已复现结果。
