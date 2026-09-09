---
name: gmcm-final-reviewer
description: Perform the final GMCM/Huawei Cup review from mathematical, experimental, and competition perspectives. Use only for a near-final paper with evidence matrix, verified numbers, rendered output, and question handoffs.
---

# GMCM final reviewer

读取官方题目、已核实当年规则、`materials/gmcm.md`（缺失时回退到 SkillPack 的 `../../rubrics/gmcm.md`）、整合稿与渲染文件、`reports/evidence_matrix.md`、`results/paper_metrics.yaml`、逐问审计/handoff 和复现入口。未验证范围不能当通过，不凭语言流畅度替代证据。

## A. Mathematical Reviewer

检查问题抽象、状态/决策/参数、假设、公式与维度、边界/约束、模型递进、推导正确性和 solver 选择。

## B. Experiment Reviewer

检查 raw/processed 数据契约、泄漏、baseline、指标/残差、时间/分组切分、随机种子、验证/稳健性、单位/数量级、约束、数值一致和可复现性。可用时吸收 `scientific-critical-thinking`、`statistical-analysis` 与 `uncertainty-and-units` 的通用检查；不新增另一套工作流。

## C. GMCM Competition Reviewer

检查逐问回答、数学深度、多问递进、真实创新、工程意义、图表证据、论文完整性、优缺点和限制。摘要背景控制在 1–2 句，每问包含 Problem / Method / Key Result；数字必须来自 `approved_for_paper: true`，正文没有的数字不得进入摘要。“效果良好、精度较高、显著改善”等没有对应指标/检验时标 OVERCLAIM。

读取 `../../corpus/derived/abstract_patterns.md`、`validation_patterns.md`、`figure_patterns.md`、`reviewer_checklist.md` 作为检查框架，不要求复刻历史论文。

输出 `reports/gmcm_final_review.md`，合并为 `CRITICAL / MAJOR / MINOR`。每项包含位置、证据、影响、最小修复和复验条件。`CRITICAL` 必修；只修高价值 `MAJOR`；`MINOR` 不得破坏稳定结果。

当 `competition_mode: true`，再给 `estimated_fix_time`、`expected_score_gain`、`risk`、`priority` 和 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH`。最终模型、数值、引用、格式和提交均需三位 owner 人工复核；此技能不自动提交。
