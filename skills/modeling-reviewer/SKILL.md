---
name: modeling-reviewer
description: Review a mathematical modeling contest solution route before substantial implementation or a major model change. Compare justified alternatives, a baseline, data support, and an achievable MVP; prevent automatic algorithm selection.
---

# Modeling reviewer

读取该问官方要求、已确认的数据字典、前后问接口和已有路线。不要将建议当作已完成的实验，不因缺少复杂方法否定可解释的简单方案。

读取并执行 [Evidence-Calibrated Communication Policy](../../rubrics/evidence_calibrated_communication.md) 的证据边界、建模与代码表达规则；Evidence > Rhetoric。

在 `notes/qN_model_plan.md` 按以下决策顺序回答：

1. `What is the mathematical structure?`：估计、识别、预测、评价、决策、控制、优化或组合；定义状态、决策与数学对象。
2. `What is the simplest credible baseline?`：给出同样本、同切分、同指标的可运行 baseline。
3. `What does the data support?`：样本量、缺失、标签、粒度、独立性、时间/分组切分与适用范围。
4. `What model can serve later questions?`：明确输出 schema、单位、依赖和误差传播。
5. `What validation is necessary?`：baseline、holdout、residual、敏感性、稳健性、可行性或机理检验。
6. 最后才选择 implementation / solver，并说明复杂度、成本、失效条件和停止升级条件。

输出至少包含：`Problem Type / Inputs / Outputs / State Variables / Decision Variables / Candidate Models / Baseline / Recommended MVP / Upgrade Condition / Failure Risks / Historical Analogues`。候选至少包含简单可解释路线；统计预测优先讨论 OLS、GLM、ARIMA 或其他可信 baseline，必要时使用 `statsmodels`，再考虑 RF/XGBoost/深度学习。复杂模型未可靠超越 baseline 时不得声称明显更优。

不得机械套用“预测→XGBoost、评价→TOPSIS、优化→GA”，不得仅凭算法流行程度选择。若数据不支持复杂方案，先选能解释并验证的 MVP。

## 防止防御性加模型

模型升级按 `Baseline → observed deficiency → justified upgrade → validation` 说明。model plan 中记录 baseline 的实际缺陷及结果位置、新模型具体解决什么、数据能否支持增加复杂度、后续问题是否需要该模型输出，以及同口径比较设计和停止升级条件。尚未观察到的缺陷只能列为待检验假设，未运行的比较不能写成性能提升。

没有明确模型比较设计时，不接受“为提高精度加入多个先进模型”“考虑到不足再加入模型 X”“为保证可靠同时采用 A/B/C/D”的理由；禁止 algorithm stacking for reassurance。模型比较本身可以是合理设计，但须有候选假设、评价口径与选择规则。

说明优先回答为什么本题需要该模型，不堆通用算法知识；简单 baseline 没被可靠超越时，可以直接选择 baseline，并将负结果作为依据。删除空泛自我贬低，保留数据、假设和实验支持的限制。实现建议与注释解释 WHY、ASSUMPTION、CONSTRAINT 或非显然逻辑，不预写未经验证的优势。

## 可选 Historical Exemplar Check

当当前路线需要结构参照或存在明显选择分歧时，可读取 `../../corpus/derived/core_corpus.md`、`model_selection_patterns.md` 与最多三张 `paper_cards/`，按数学对象、状态/决策、目标、约束和验证需求匹配历史案例。记录“为什么结构相似、可借鉴什么、不可复制什么”；不得按题号或应用名硬配。

历史案例只产生候选结构，不能作为模型正确性的证据，不能覆盖当前题意、当前数据、当前约束和当前 baseline。若相对路径不存在，跳过该可选检查并记录 corpus 不可用，不臆造历史结论。

当 `competition_mode: true`，修改建议增加 `estimated_fix_time`、`expected_score_gain`、`risk`、`priority`，并分类 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH`。优先高收益、低风险、30 分钟内闭环。

普通合理实施选择可以直接推进；只有缺少的题意或输入会改变结论时才询问用户。审查并不自动授权超出当前任务的实验、环境修改或外部动作。
