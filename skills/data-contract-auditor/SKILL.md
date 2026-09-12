---
name: data-contract-auditor
description: Audit raw and processed data contracts before GMCM modeling. Use after intake or cleaning to verify schema, units, ranges, missingness, keys, time order, impossible values, and target availability without modifying raw data.
---

# Data contract auditor

读取题目数据说明、`AGENTS.md`、清洗代码及数据文件清单；`data/raw/` 永远只读。先按题目和表建立索引，只抽样读取验证所需内容，不默认加载所有大文件。

为 raw 与 processed 分别检查：column names、dtype、units、missingness、valid ranges、uniqueness/key、duplicate rows、temporal ordering、impossible values、categorical vocabulary、target availability、行数变化和转换来源。区分题目规定、数据观察和审计推断；未知写 `UNVERIFIED`。

简单数据优先用标准库或轻量 Python assertions；只有多表、复杂 schema 或流水线复用价值明确时才建议 Pandera。不得为了 Pandera 增加依赖，不自动安装包，不原地修复 raw。输出 `reports/data_contract.md`，包含 raw contract、cleaning delta、processed contract、失败样例数量、模型可用范围和阻断项。

状态使用 `PASS / UNVERIFIED / CONFLICT / DEFINITION_RISK / UNIT_CONFLICT / DIMENSION_RISK / ORDER_OF_MAGNITUDE_RISK`。键、目标、时间顺序、单位或不可逆数据丢失影响主结论时标为阻断。

当 `competition_mode: true`，每个建议增加 `estimated_fix_time`、`expected_score_gain`、`risk`、`priority`，并只给 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH`。优先高收益、低风险、30 分钟内修复。

供 mm 导航时，在报告开头增加独立 `verdict: PASS` 或实际未通过状态；仅当数据契约已核验且无阻断时填 PASS。
该机器字段不替代逐项契约、失败样例和模型可用范围。
