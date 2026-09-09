---
name: contest-project-bootstrap
description: Initialize or check a mathematical modeling contest workspace, official materials, directory layout, Git readiness, and J/F/L ownership before modeling begins. Use at contest kickoff or when resuming an unorganized contest project.
---

# Contest project bootstrap

先读项目 `AGENTS.md`、`README.md` 和已有版本记录，尊重现有项目约定。用户要求新建时使用可用的 `mm-init <project>`；已有项目先检查，不重新覆盖。

检查并记录：

- 官方赛题原件、全部附件、当届规则、模板、提交截止时间及来源是否齐全；缺材料要明确列出，不能猜赛题。
- `materials/gmcm.md`（未初始化项目可回退到 SkillPack 的 `../../rubrics/gmcm.md`）是否可读，`materials/gmcm_year_override.md` 是否只含已核实当年规则；`verified: false` 时不得据此判断提交格式。
- `data/raw/`、`data/processed/`、`src/`、`results/`、`figures/`、`notes/`、`reports/`、`paper/`、`materials/`、`project/`、`problem_files/` 是否齐全；原始数据保持只读，`results/paper_metrics.yaml` 存在。
- 项目是否独立 Git 仓库、当前分支和未提交改动；不要触碰相邻比赛仓库，不自动 force push 或清理已有工作。
- 项目 `.agents/skills/` 的 MathModel Standard 是否可发现、是否与 Lite 或全局同名 Skill 重复，`notes/toolchain_versions.md` 是否存在。
- J/F/L 三位 owner 的逐问分工、接口、交叉审查人与时间表；三人共同负责，不默认一主两辅。
- 可运行环境与缺失依赖、数据来源/校验和、结果与图表输出位置、论文唯一整合稿。

将可用材料、缺口、负责人、下一步写入 `notes/bootstrap.md`。缺官方材料时可完成目录、分工和环境检查，但明确哪些工作尚不能开始。不安装未经确认的重型环境，不直接开始复杂建模。

结束时给出第一问需要澄清的输入/输出及 baseline 任务；固定下一步为 `data-contract-auditor`，再进入 `modeling-reviewer`。此 Skill 不自动授权子代理、外部消息、提交或推送。
