---
name: repo-paper-auditor
description: Build a GMCM repository-to-paper evidence matrix and audit claims, method consistency, figures, units, and causal language. Use once question results or a draft paper exist, especially before handoff or final review.
---

# Repository paper auditor

这是 v0.9 最高优先级证据审计。先读 `AGENTS.md`、官方题目索引和目录清单，再按 Q1/Q2/Q3… 建索引；优先扫描 `problem_files/`、`materials/`、`notes/`、`src/`、`results/`、`figures/`、`paper/`，不要无脑全文读取所有文件。官方当年规则只信已核实的 `materials/gmcm_year_override.md`。

读取并执行 [Evidence-Calibrated Communication Policy](../../rubrics/evidence_calibrated_communication.md)，核对 claim 与证据以及代码/README 表达；Evidence > Rhetoric。

沿 `题目 → 数学模型 → 代码 → 结果 → 图 → paper claim` 追踪。输出 `reports/evidence_matrix.md`：

| Claim | Question | Requirement | Model | Code | Result | Figure | Paper Location | Evidence Strength | Status |
|---|---|---|---|---|---|---|---|---|---|

Evidence Strength 只用 `STRONG / MODERATE / WEAK / NONE`；Status 只用 `PASS / MISSING / UNSUPPORTED / CONFLICT / OVERCLAIM / CAUSALITY_RISK / DEFINITION_RISK / UNIT_CONFLICT / DIMENSION_RISK / ORDER_OF_MAGNITUDE_RISK / UNCERTAINTY_PROPAGATION_RISK / VALIDATION_MISSING / METHOD_MISMATCH`。

重点检索“显著、明显、精确、有效、稳定、鲁棒、导致、影响、最优、提升、降低、优于”。逐条核对统计/工程证据，并严格区分 correlation、association、prediction、causality。没有因果设计不得保留因果结论；弱/负结果不得隐藏。论文方法、代码与运行配置不一致（如正文五折、代码三折时间切分）标 `METHOD_MISMATCH` 且为 Critical。

读取 `../../corpus/derived/validation_patterns.md`、`paper_structure_patterns.md`、`common_mistakes.md` 作为检查维度，不要求当前模型复制历史案例。可用时调用/吸收 `scientific-critical-thinking` 的通用偏差、混杂、替代解释与推断强度检查；不得机械套医学专用证据等级。单位工程题可用 `uncertainty-and-units`，统计结论可用 `statistical-analysis`。

每张正文图记录 Evidence Purpose：`EDA / MECHANISM / MODEL / RESULT / VALIDATION / SENSITIVITY / OPTIMIZATION / DECISION`；无法回答支持何种 claim 时标 `DECORATIVE_FIGURE`。

## 表达与证据一致性

对积极措辞和谨慎措辞做对称核验：结论应与指标、同口径比较、变化方向/幅度及稳定性一致。`UNJUSTIFIED_POSITIVE_LANGUAGE` 与 `UNJUSTIFIED_HEDGING` 必须有原句、证据位置和允许的修订；不把“弱、不稳定、不显著、未优于、无法识别因果”当成自动删除词。

将数据、假设或实验支持的局限标记为 `VALID_LIMITATION` 并保留，检查正文、摘要和 handoff 是否遗漏影响解释的边界。无技术信息的自我贬低才归为 `DEFENSIVE_WRITING`。数值冲突、方法与代码不一致、隐藏负结果、因果过度声明或改写改变证据强度均按 `CRITICAL` 处理。

扫描最终仓库中的注释和 README：是否解释 WHY、ASSUMPTION、CONSTRAINT、非显然逻辑，是否声称未经实验验证的性能提升。逐项复核 `TODO / HACK / temporary / maybe / probably` 的当前有效性和影响；已失效的删除或更新，仍存在的问题保留技术说明，不能只删标记。纯显然代码复述可压缩，不删除复现信息。

在 `reports/evidence_matrix.md` 后附表达审计表：

| Location / original wording | Claim / matrix row | Evidence anchor | Communication finding or VALID_LIMITATION | Severity | Allowed revision / retain reason |
|---|---|---|---|---|---|

表达类别与现有 Evidence Matrix `Status` 分开记录，不扩展或混淆证据状态枚举。`VALID_LIMITATION` 的 Severity 写 `—`，不当缺陷计数。终审负责跨段重复和整体叙事，本审计负责修订不得越过证据边界。

当 `competition_mode: true`，每个问题增加 `estimated_fix_time`、`expected_score_gain`、`risk`、`priority`，并分类 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH`。优先高收益、低风险、30 分钟内修复；审计不自动重构模型。

供 mm 预检时，矩阵 Question 使用 qN。未解决问题可附 `Question / Finding / Severity / Resolution` 表；
CRITICAL 未解除写 OPEN，修复且复验后才写 RESOLVED/FIXED；全局问题用 all。保留证据位置，
不把自然语言里出现 CRITICAL 一词当作机器已正确识别的保证。
