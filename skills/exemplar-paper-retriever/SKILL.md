---
name: exemplar-paper-retriever
description: Retrieve up to three structurally similar GMCM exemplar paper cards for a current mathematical modeling problem. Use when selecting a modeling route, looking for reusable decomposition, validation, or optimization patterns, or asking what past high-value papers can teach without copying topic-specific methods.
---

# Exemplar paper retriever

先读取当前问题、数据说明、交付要求和已知约束。历史论文只提供候选结构，不能替代当前证据。

## Corpus routing

从本技能目录以 `../../corpus/derived/` 定位语料。先读 `core_corpus.md`，再按任务只读必要的模式文件；确定候选后读取对应 `paper_cards/<ID>.md`。默认不读取原始 PDF 或 `corpus/extracted/`。路径不存在时明确报告 corpus unavailable，不凭记忆补全。

常用路由：拆题读 `problem_decomposition_patterns.md`；选模读 `model_selection_patterns.md`；优化读 `optimization_patterns.md`；验证读 `validation_patterns.md`；写作/终审读 `abstract_patterns.md`、`figure_patterns.md`、`paper_structure_patterns.md`、`reviewer_checklist.md`；避坑读 `common_mistakes.md`。

## Retrieval procedure

1. 用一句话判断当前数学本质，并列出输入、输出、状态、决策变量、目标、约束、数据支持和验证需求；未知项写 UNKNOWN。
2. 按数学结构与证据需求匹配 `core_corpus.md`，不按题号、年份或应用关键词匹配。
3. 最多选三篇；每篇必须带来不同且相关的价值。弱匹配宁可不推荐。
4. 用 paper card 核对原文证据与分析标签，不把 `[ANALYST INFERENCE]` 写成论文事实。
5. 输出后回到当前问题，说明哪些候选结构仍须由当前数据实验决定。

## Output

对每篇给出：

- `Paper`: ID 与标题
- `Why structurally similar`: 对齐数学对象、输入输出、状态/决策、目标/约束或验证，而非表面领域
- `Reusable structure`: 可复用的拆题、数学结构、验证或图表证据
- `Do not copy`: 题目特定参数、算法、阈值、假设或未经验证做法
- `Current evidence needed`: 当前题目采用前必须补的最小证据

最后给出“不采用历史案例也成立”的 baseline/MVP。不得把案例数量凑满三篇，不得给历史论文排名，不得用历史结果证明当前模型有效。
