---
name: verified-number-registry
description: Create or audit the authoritative GMCM paper-number registry in results/paper_metrics.yaml. Use before paper handoff, after result changes, or when abstract, tables, figures, and prose contain conflicting metrics.
---

# Verified number registry

`results/paper_metrics.yaml` 是论文核心数字的唯一批准入口。若文件不存在，从本技能目录的 `../../templates/paper_metrics.yaml` 建立空 registry；详细字段以 `../../schemas/paper_metrics.schema.json` 为准。JSON 是有效 YAML，基础检查可只用 Python 标准库；只有项目已使用普通 YAML 语法时才需要 PyYAML。

每条指标必须包含：`question`、`metric_id`、`description`、`value`、`unit`、`definition`、`source_script`、`source_result`、`source_field`、`rounding`、`validation_status`、`approved_for_paper`、`notes`。路径必须相对项目根目录，源脚本、结果文件和字段必须存在且可追溯到真实运行。

审计同一 `metric_id` 的多个值、单位/定义/样本/窗口口径、rounding、缺失来源和 stale result。状态只用 `PASS / UNVERIFIED / CONFLICT / DEFINITION_RISK / UNIT_CONFLICT`。存在 `CONFLICT`、`DEFINITION_RISK` 或 `UNIT_CONFLICT` 时必须令 `approved_for_paper: false`；不得用手填数字解除冲突。

摘要、正文、表格和图注优先引用 `approved_for_paper: true` 条目。成员不得从不同 CSV 各自重算后直接写论文。结果变化时先更新可重跑产物和 registry，再同步图表、handoff 与论文。

当 `competition_mode: true`，冲突修复增加 `estimated_fix_time`、`expected_score_gain`、`risk`、`priority` 和 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH`；数字冲突永远优先于文字润色。
