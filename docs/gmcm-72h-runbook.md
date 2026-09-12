# GMCM 72 小时现场 Runbook

按官方截止时间倒推；下列 T+72h 是演练框架，不是任何年份的官方截止声明。指定 J/F/L 真名与交叉审查人，所有时间写入项目看板。打开 `mm status` / `mm next`，按唯一 workflow 推进每问 MVP。

| 时间 | 当班动作 | 交付/检查点 |
|---|---|---|
| Phase 0：开赛前 | J：install/verify、mm doctor、锁定 SHA/依赖、准备复现环境；F：确认数据工具；L：准备官方模板/编译；共同核对当年规则 | 无缺失核心环境；年度规则 verified + 官方来源；工具链冻结；72h 值班/备份安排 |
| T+0–2h | 共同读题选题；bootstrap；F 清点附件、data-contract；J 初步路线/baseline；L 记录问题要求 | 官方材料完整；核实 questions；J/F/L 分工；逐问输入输出和依赖 |
| T+2–8h | J 做 Q1 最小模型/核心代码、Q2 route；F 跑实验/验证和第一张结果图表；L 并行论文骨架/符号表 | Q1 可重跑输出；真实 run manifest；Q2 路线明确；论文不等待所有模型完成 |
| Day 1 night | 审计 Q1、批准数字、gate、矩阵、handoff、复验；为其余问题做路线决策 | 至少一问 MVP_CLOSED；其余问题路线和下一依赖明确；交接休息 |
| Day 2 AM | J 推进核心问题；F 实验与独立验证同步；L 整合已有 handoff | 每问代码→结果→验证闭环；不只累计实验，不审计 |
| Day 2 PM | 后半问题 MVP；按收益做必要优化/敏感性；L 持续同步图表和叙事 | 前后问 schema/单位一致；约束检查；新数字走 registry |
| Day 2 night | 用 mm status 逐问排缺口；优先补尚未闭环问题；已闭环问题暂停低收益升级 | 尽量全部 MVP_CLOSED；未完成项有负责人、时间和最小解法 |
| Day 3 AM | 补必要验证；核对 registry、Evidence Matrix、handoff；变化后复审 gate | 可写数字获批；claim 有证据；所有交接与当前结果一致 |
| Day 3 PM | L 整合完整论文和摘要 PMR，渲染唯一终稿；J/F 交叉核验；gmcm-final-reviewer 默认 FULL | final review 有范围、位置、严重度、最小修复与复验条件 |
| Last 6h | 停止无收益换模型；修复明确影响作答/证据的问题 | 稳定可重跑版本；修复有收益、回滚依据和 owner |
| Last 3h | freeze numbers；只修 CRITICAL 和高价值 MAJOR；不重构；明确要求时可 FAST 终审 | 数字清单冻结；若必须改数，同步 registry→图表→matrix→handoff→paper 并复审 |
| Last 1h | mm refresh；按正常 Git 流程保存；mm final-check；J/F/L 人工核对终稿、附件与官方要求 | READY FOR HUMAN FINAL REVIEW 后仍人工核验和提交；保存提交回执 |

## 角色执行卡

| Owner | 负责到底的工作 | 交给下一人的内容 |
|---|---|---|
| J | modeling、core code、technical QA、hard decision、final validation | 数学对象/约束/接口、关键实现、审查结论、取舍决定 |
| F | data、EDA、experiment execution、figures、result verification | 数据契约、运行命令/配置/产物、验证证据、可重生成图表 |
| L | paper skeleton、equations/exposition、handoff integration、abstract、consistency、final assembly | 逐问叙事、PMR 摘要、引用统一、唯一渲染终稿及提交材料 |

J 不长期承担普通数据清洗、普通绘图、排版。F/L 是交付 owner，不是等 J 分派的辅助；阻断跨角色接口时三人短同步，避免并发覆盖同一文件。每次轮休前交接下一依赖与精确运行位置。

## 每 4–6 小时短同步（5–10 分钟）

1. `mm status`：current question status；已有闭环是否因结果变化失效？
2. blocked items：最小解除条件、owner、截止时间。
3. next dependency：下一问到底需要哪个文件/字段/单位？
4. numbers changed? 记录 metric_id 与关联稿件位置。
5. paper sync needed? L 确认 handoff/图表/摘要是否同步；`mm refresh` 更新缓存。

## 卡住时

主结论泄漏、硬约束违反、关键数字冲突：BLOCKED，先最小修复并重验。环境缺可选包不等于必须安装；优先用已有环境的可运行 baseline。某问没完时不为另一问追求更漂亮的指标；Complete first → Validate → Improve。

提交前以 [execution-cli.md](execution-cli.md) 的 source-of-truth 为准。FAST 只缩小审查范围和报告体积，不降低证据门槛；未检查内容写明，不能声称 FULL 通过。人工核验包括当年匿名、格式、页数、引用、AI 使用披露与附件要求，规则仅来自核实后的官方材料。
