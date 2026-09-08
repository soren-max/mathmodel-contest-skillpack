---
name: paper-handoff
description: Turn an audited contest question into a structured J/F-to-paper-owner handoff with mathematical formulation, execution provenance, figures, limitations, and exact permitted paper numbers. Use when a question is ready for writing or its results have changed.
---

# Paper handoff

读取该问路线、代码入口、实际结果、图表和审计。若审计为 BLOCKED 或关键证据缺失，可生成标明“草稿/不可用于论文”的交接清单，不能放行关键数值。审计未做时先核验或建议调用可用的 `result-auditor`。

写入 `notes/handoff_qN.md`；已有版本保留修订依据，结果改变后同步更新。论文负责人不应从代码重新猜测结果。每一问统一使用以下结构，填真实内容而非保留占位文字：

```markdown
# Question
## Goal
## Variables
## Assumptions
## Mathematical formulation
## Algorithm
## Code entry
## Key results
## Figures
## Figure interpretation
## Validation
## Engineering / practical interpretation
## Limitations
## Exact numbers allowed in paper
```

`Question` 标明题号、交付人、审查人、版本和审计状态。变量列单位/索引/定义域；数学表达写出目标、约束、估计式或递推关系。算法解释关键步骤和停止条件。

`Code entry` 提供从项目根目录执行的真实命令、输入版本/校验和、环境、种子、配置和输出位置。没有实际运行的命令标记为待运行。

`Key results` 和 `Exact numbers allowed in paper` 为每个数字记录：指标定义、原始精度、允许展示值、单位、样本量/分母、区间（若有）、来源文件及行/键、对应实验。所有四舍五入使用统一规则；不存在的区间不能编造。

每幅图给出相对路径、生成脚本、数据来源、图注、图支持的结论与不支持的解释。实践含义不得越过统计证据；限制与审计要求原样传递给 L。末尾列出尚待决策的问题及负责人。
