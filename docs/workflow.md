# 从开赛到交付

赛前 clone SkillPack、运行 install/verify，并在新临时项目演练一次。仅赛前按需 update，审查变更后提交锁文件。比赛中冻结所有全局工具和计算依赖；先完成、再验证、再改进。

| 阶段 | 主责与工具 | 交付 |
| --- | --- | --- |
| 启动 | J/F/L，contest-project-bootstrap | 官方材料、规则、分工、目录、环境与接口 |
| 逐问路线 | J 主责，F/L 交叉审查，modeling-reviewer | 数学表述、baseline、候选路线、MVP、升级条件 |
| 数据与实现 | F/J，MathModel Standard | 只读原始数据、处理脚本、真实实验、可追溯结果 |
| 验证 | F/J，result-auditor | 泄漏/指标/约束/稳健性/数值一致性审计 |
| 绘图 | F，scibox-figure / scibox-diagram | 从真实数据生成的图、图注和解释 |
| 逐问交接 | J/F → L，paper-handoff | notes/handoff_qN.md 与明确允许写入的数值 |
| 论文整合 | L 主责，全员 review，paper-spine | 数学表达、章节递进、证据与主张对应 |
| 最终审查 | 全员，final-paper-reviewer | 优先修 Critical，其次 Major，最终人工复核 |

MathModel Standard 提供项目中的分解、选择、数据、代码、证据与写作工作流。本仓库五个 Skill 补充团队审查与交接接口，不替换其原文。先用 `/skills` 确认实际发现的名称，再按当前任务调用；不同时启动多个负责整篇论文的入口。

常用起始提示：

```text
使用 $contest-project-bootstrap 检查当前比赛项目，列出材料缺口和 J/F/L 接口，不开始复杂建模。
使用 $modeling-reviewer 审查第一问，比较至少两条路线并给出 baseline 和 MVP。
使用 $result-auditor 检查第一问的真实结果与图表，标明尚未验证的部分。
使用 $paper-handoff 将第一问交给 L，逐个标注允许写入论文的数值及来源。
使用 $final-paper-reviewer 对最终稿逐问审查，优先报告 Critical。
```

原始数据 → 处理代码 → 实验配置/种子 → 结果文件 → 图表 → handoff → 正文/摘要，每一环必须有可定位来源。BLOCKED 的主结论不可写成正式结果；负 R² 和失败实验保留并解释。L 不从脚本猜数字，J/F 不只交图而不交数学表达与验证。

当上游生成目录与模板不同，在 `project/project-layout.md` 记录实际映射和唯一提交稿；不随意修改第三方技能去强制统一路径。若需改变流程，在本项目的 AGENTS/notes 中明确约定。
