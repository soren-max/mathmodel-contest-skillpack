---
name: modeling-reviewer
description: Review a mathematical modeling contest solution route before substantial implementation or a major model change. Compare justified alternatives, a baseline, data support, and an achievable MVP; prevent automatic algorithm selection.
---

# Modeling reviewer

读取该问官方要求、已确认的数据字典、前后问接口和已有路线。不要将建议当作已完成的实验，不因缺少复杂方法否定可解释的简单方案。

在 `notes/qN_model_plan.md` 对以下十项给出可检查的回答：

1. 数学本质是什么：估计、识别、预测、评价、决策、控制、优化或组合？题目要求的结论是什么？
2. 输入/输出是什么：变量、单位、时间粒度、可观测性、约束及依赖？
3. baseline 是什么，如何在同一评价口径下运行？
4. 至少两种候选路线；比较假设、数据需求、解释性、复杂度、计算成本和预期失效条件。
5. 现有数据是否支持这些假设，样本量、缺失及切分是否足够？
6. 模型是否有清晰数学表达，参数和结果能否解释？
7. 输出是否能服务后续问题，误差如何传递？
8. 最大失败风险及其最小验证实验是什么？
9. MVP 路线是什么，怎样尽早形成可运行、可验证的逐问闭环？
10. 什么证据与时间预算允许升级模型，停止升级的条件是什么？

给出推荐路线、选择理由、baseline、验证计划和当前未证实假设。不得机械套用“预测→XGBoost、评价→TOPSIS、优化→GA”，不得仅凭算法流行程度选择。若数据不支持复杂方案，先选能解释并验证的 MVP。

普通合理实施选择可以直接推进；只有缺少的题意或输入会改变结论时才询问用户。审查并不自动授权超出当前任务的实验、环境修改或外部动作。
