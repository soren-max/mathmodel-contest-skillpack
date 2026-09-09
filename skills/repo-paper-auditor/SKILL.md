---
name: repo-paper-auditor
description: Build a GMCM repository-to-paper evidence matrix and audit claims, method consistency, figures, units, and causal language. Use once question results or a draft paper exist, especially before handoff or final review.
---

# Repository paper auditor

这是 v0.9 最高优先级证据审计。先读 `AGENTS.md`、官方题目索引和目录清单，再按 Q1/Q2/Q3… 建索引；优先扫描 `problem_files/`、`materials/`、`notes/`、`src/`、`results/`、`figures/`、`paper/`，不要无脑全文读取所有文件。官方当年规则只信已核实的 `materials/gmcm_year_override.md`。

沿 `题目 → 数学模型 → 代码 → 结果 → 图 → paper claim` 追踪。输出 `reports/evidence_matrix.md`：

| Claim | Question | Requirement | Model | Code | Result | Figure | Paper Location | Evidence Strength | Status |
|---|---|---|---|---|---|---|---|---|---|

Evidence Strength 只用 `STRONG / MODERATE / WEAK / NONE`；Status 只用 `PASS / MISSING / UNSUPPORTED / CONFLICT / OVERCLAIM / CAUSALITY_RISK / DEFINITION_RISK / UNIT_CONFLICT / DIMENSION_RISK / ORDER_OF_MAGNITUDE_RISK / UNCERTAINTY_PROPAGATION_RISK / VALIDATION_MISSING / METHOD_MISMATCH`。

重点检索“显著、明显、精确、有效、稳定、鲁棒、导致、影响、最优、提升、降低、优于”。逐条核对统计/工程证据，并严格区分 correlation、association、prediction、causality。没有因果设计不得保留因果结论；弱/负结果不得隐藏。论文方法、代码与运行配置不一致（如正文五折、代码三折时间切分）标 `METHOD_MISMATCH` 且为 Critical。

读取 `../../corpus/derived/validation_patterns.md`、`paper_structure_patterns.md`、`common_mistakes.md` 作为检查维度，不要求当前模型复制历史案例。可用时调用/吸收 `scientific-critical-thinking` 的通用偏差、混杂、替代解释与推断强度检查；不得机械套医学专用证据等级。单位工程题可用 `uncertainty-and-units`，统计结论可用 `statistical-analysis`。

每张正文图记录 Evidence Purpose：`EDA / MECHANISM / MODEL / RESULT / VALIDATION / SENSITIVITY / OPTIMIZATION / DECISION`；无法回答支持何种 claim 时标 `DECORATIVE_FIGURE`。

当 `competition_mode: true`，每个问题增加 `estimated_fix_time`、`expected_score_gain`、`risk`、`priority`，并分类 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH`。优先高收益、低风险、30 分钟内修复；审计不自动重构模型。
