# GMCM 从开赛到交付

赛前 clone SkillPack、运行 install/verify，并在临时项目演练。仅赛前主动更新；比赛中冻结工具链。总原则是 Problem first、Evidence first、Complete first → Validate → Improve。

固定唯一流程：

```text
contest-project-bootstrap
→ data-contract-auditor
→ modeling-reviewer
→ optional exemplar-paper-retriever
→ model/code
→ result-auditor
→ verified-number-registry
→ question-completion-gate
→ repo-paper-auditor
→ paper-handoff
→ paper
→ PaperSpine if useful
→ gmcm-final-reviewer
```

MathModel Standard 继续提供项目级原子工作能力，sci-box 负责图，PaperSpine 只在论文整合确有收益时使用。本仓库不引入另一套数学建模 orchestrator。比赛推进单位是 `each question → MVP_CLOSED → next question → later improvement`。

常用起始提示：

```text
使用 $contest-project-bootstrap 检查当前比赛项目、官方材料和 J/F/L 接口。
使用 $data-contract-auditor 在不修改 data/raw 的前提下检查原始与处理数据契约。
使用 $modeling-reviewer 审查第一问，比较候选路线并给出 baseline 和 MVP。
必要时使用 $exemplar-paper-retriever 按数学结构检索最多三篇案例。
使用 $result-auditor 检查真实运行、泄漏、指标、约束与验证。
使用 $verified-number-registry 批准可进入论文的核心数字。
使用 $question-completion-gate 判断该问是否已达到 MVP_CLOSED。
使用 $repo-paper-auditor 建立题目到论文 claim 的 Evidence Matrix。
使用 $paper-handoff 将已审计的问题交给 L。
使用 $gmcm-final-reviewer 从数学、实验与竞赛三个视角审查终稿。
```

原始数据 → 处理代码 → 实验配置/种子 → 结果 → registry → 图表 → Evidence Matrix → handoff → 正文/摘要，每一环必须可定位。BLOCKED 主结论不可写成正式结果；负 R²、弱关系和失败实验保留并解释。

上游目录与模板不同时，在 `project/project-layout.md` 记录实际映射和唯一提交稿。比赛开始后按 [competition-freeze.md](competition-freeze.md) 冻结流程。
