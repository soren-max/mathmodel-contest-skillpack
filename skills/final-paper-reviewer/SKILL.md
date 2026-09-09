---
name: final-paper-reviewer
description: Review a near-final mathematical modeling contest paper from a judge's perspective, checking question coverage, mathematical arguments, evidence consistency, submission readiness, and reproducibility. Use at final integration or pre-submission review.
---

# Final paper reviewer

读取官方题目、当届规则、整合稿与最终渲染文件、各问 handoff 和结果审计。以数学建模竞赛评委视角检查，不凭语言流畅度代替证据质量。

若仓库包含 `../../corpus/derived/`，同时读取 `abstract_patterns.md`、`validation_patterns.md`、`figure_patterns.md` 与 `reviewer_checklist.md` 作为证据完整性检查框架。它们提供检查维度而不是历史模型标准；不得要求当前论文复刻案例模型。相对路径不存在时记录 corpus 不可用并继续现有审查。

逐项给出“符合 / 问题 / 未验证 / 不适用”，记录页码、章节或文件位置：

1. 是否逐问回答题目与交付要求。
2. 是否有清晰数学表达、变量和假设。
3. 模型选择理由与 baseline 是否成立。
4. 前后问题是否递进、接口与误差传播是否解释。
5. 数据是否支持模型与假设。
6. 正文、摘要、表格、图和原始产物数值是否一致。
7. 图是否回答问题，图注、单位与可读性是否充分。
8. 是否过度声明，是否将相关/预测写成因果。
9. 是否有必要验证及真实实验依据。
10. 敏感性/稳健性是否充分或有合理的不适用说明。
11. 模型优缺点是否具体且与证据一致。
12. 摘要是否包含方法和可追溯核心数值。
13. 结论是否真正回答问题及实际含义。
14. 是否残留 TODO、占位符、示例数字、未解析引用。
15. 是否误带内部绝对路径、AI 对话、Prompt、Agent 调试信息；必须保留当届规则要求的 AI 使用说明，不能用清理来隐瞒使用。
16. 引用是否真实存在并支持对应主张；无法查证的引用标记未验证。
17. 附录代码是否有依赖、数据来源、命令、配置、种子和可复现性证据。

检查最终 PDF/Word 的页数、匿名要求、公式/图表渲染及附件，以当届官方规则为准；未获得渲染能力时明确限制。不要捏造比赛规则。

在 `notes/final_paper_review.md` 输出问题列表，按下列级别排序：

- **Critical**：漏答主问、关键证据不可信、伪造引用/数据、严重数值冲突或不符合已核实提交要求；先修复并复验。
- **Major**：论证、选择理由、验证、敏感性或解释存在明显缺口，影响评委判断。
- **Minor**：不改变结论的文字、图注、排版和一致性问题。

每项写明位置、证据、影响、最小修复、负责人建议与复验条件。列出未验证范围与剩余风险，不能把未验证视为通过。允许提出修改或执行已授权的修复，不自动投稿、推送或对外发送。最终模型及提交稿由团队人工复核。
