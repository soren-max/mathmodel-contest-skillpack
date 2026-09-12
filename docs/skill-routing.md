# GMCM Skill Routing Authority

按需要选择 Primary；Secondary 只补原子能力，不签发 Primary 的结论。`mm` 给出确定性导航，不调用 Skill，不另建 orchestrator。唯一流程见 [workflow.md](workflow.md)，现场节奏见 [gmcm-72h-runbook.md](gmcm-72h-runbook.md)。

| Need | Primary | Secondary / Optional | Must NOT Replace |
|---|---|---|---|
| 题目/材料解析 | MathModel problem-doc-model-selector | contest-project-bootstrap 检查材料/分工 | 不代替 modeling-reviewer 的赛题路线决策 |
| 赛题路线决策 | modeling-reviewer | exemplar-paper-retriever，最多三篇结构参照 | 历史案例或模型选择器不能替代当前数据/baseline 证据 |
| 代码/实验实现 | MathModel model-code-and-result-generator | K-Dense statsmodels 等原子能力 | 不能自行批准结果或数字 |
| 数据契约 | data-contract-auditor | statistical-analysis；已有环境中的 Pandera | 通用 QA 不代替数据源/目标可得性检查 |
| 结果真实性 | result-auditor | scientific-critical-thinking / statistical-analysis / uncertainty-and-units | MathModel quality-assurance-auditor 不能替代 result-auditor |
| 数字批准 | verified-number-registry | result-auditor 提供运行证据 | 写作器、handoff、手改 cache 不能批准数字 |
| 优化结构 | structured-optimization | 按结构使用已有 solver/原子工具 | 求解器名称不能替代数学模型，可行性检查不能省略 |
| 仓库→论文一致性 | repo-paper-auditor | MathModel quality-assurance-auditor 补一般检查 | 通用 QA 不能替代 Evidence Matrix / repo-paper-auditor |
| 逐问完成度 | question-completion-gate | mm gate 产物预检 | CLI readiness 不能替代 LLM gate verdict |
| J/F → L | paper-handoff | 批准 registry 与 Evidence Matrix | L 不重新猜数；写作器不覆盖证据范围 |
| 图表 | scibox-figure / scibox-diagram | MathModel 已有结果生成入口 | 装饰图不能替代验证；绘图工具不批准 claim |
| 论文写作 | MathModel paper-formal-writer | PaperSpine，仅在整合有收益时 | PaperSpine 不重新选模型、重新计算数字或覆盖 Evidence Matrix |
| GMCM 最终内容审稿 | gmcm-final-reviewer | 通用语言/引用/排版检查 | MathModel QA / PaperSpine final audit 不替代 GMCM 终审 |
| 状态、环境、提交前确定性检查 | mm status/next/gate/doctor/final-check | 人工按建议调用上述 Skill | mm 不做任何建模或语义审查 |

MathModel paper-workflow-orchestrator 不能替代本仓库唯一 GMCM workflow。上游工具要求自己的生成目录时，在 project-layout 记录映射；不启动竞争流程。K-Dense 只使用已选择的原子 Skills，不自动扩大安装范围。

J 负责数学路线、核心代码、技术 QA、关键决策和最终验证；F 负责数据、EDA、实验、图表及结果独立核验；L 负责骨架、公式/表达、handoff 整合、摘要、一致性和最终装配。交付缺口退回对应 owner；Complete first → Validate → Improve，不让 J 长期接管普通清洗、绘图或排版。
