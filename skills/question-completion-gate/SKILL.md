---
name: question-completion-gate
description: Gate each GMCM question as BLOCKED, PARTIAL, MVP_CLOSED, or CLOSED. Use during timed competition handoffs to prevent polishing one question while later questions lack a runnable evidence loop.
---

# Question completion gate

读取该问题意、模型计划、代码入口、真实运行产物、验证、图表、解释、限制、数字 registry、审计和 handoff。不能以文件名存在代替内容或运行证据。

只选择一个状态：

- `BLOCKED`：题意/数据/关键证据冲突，或主结果因泄漏、错误指标、不可行解、方法不一致而不可信。
- `PARTIAL`：已有工作但尚未达到端到端最小闭环。
- `MVP_CLOSED`：problem understood、mathematical formulation、实际运行代码、数值结果、至少一项有用验证、至少一张有用图/表、解释、限制和 paper handoff 均存在。
- `CLOSED`：在 MVP_CLOSED 上完成充分验证、批准数字、完整图表、最终解释，且 evidence audit 无阻断。

输出 `reports/question_status.md`，逐问列证据位置、缺口、下一步、负责人和依赖。确实无需图时必须有可审查理由和替代表格，不可静默放行。

比赛策略是 `each question → MVP_CLOSED → next question → later improvement`。当 `competition_mode: true`，建议增加 `estimated_fix_time`、`expected_score_gain`、`risk`、`priority`，分类 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH`；不为低收益升级破坏已稳定闭环。

## mm 机器索引（工具可用时）

审查当前证据后，读取 `mm gate qN --json` 的 artifact_sha256，在同一 reports/question_status.md
每问保留一个 `<!-- mm-gate {"question":"q1","verdict":"PARTIAL","artifact_sha256":"实际审查的指纹"} -->`。
verdict 必须与正文一致，可用 BLOCKED/PARTIAL/MVP_CLOSED/CLOSED；CLI readiness 不能代替你的判断。
原流程初次 gate 可报 PARTIAL 并列出待补 evidence/handoff，完成下游产物后复验同一关卡。
产物变动要重新审查；mm refresh 仅更新 cache，不续签 verdict。工具不可用则保留常规报告，
明确未绑定机器指纹，不为满足格式编造证据。
