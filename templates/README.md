# 数学建模竞赛项目

填写比赛名称、年份、赛题、官方截止时间及团队 J/F/L。将官方题目放入 `problem_files/`，数据放入 `data/raw/`，规则和模板放入 `materials/`。

在此目录运行 `codex`，先使用 `$contest-project-bootstrap` 检查材料和协作安排，再使用 `$modeling-reviewer` 审查第一问路线。

遵循 [AGENTS.md](AGENTS.md)；目录职责见 [project/project-layout.md](project/project-layout.md)，工具链版本见 [notes/toolchain_versions.md](notes/toolchain_versions.md)。

每一问依次交付建模路线、可运行代码、真实结果、验证、图表和 `notes/handoff_qN.md`；通过 `$result-auditor` 后交给论文负责人，终稿使用 `$final-paper-reviewer`。

计算环境由团队为本题建立，在 `project/` 记录 Python/求解器版本、依赖锁定、随机种子、数据校验和及重跑命令。此初始化工具不会安装 NumPy、绘图库、LaTeX、Word 渲染或求解器。

MathModel Skill 是本项目 `.agents/skills/` 内的官方包副本，版权与来源见 `.agents/third-party/MathModel-Skill/LICENSE` 和 `.agents/mathmodel-source.json`。其他全局工具仍随机器缓存；比赛期间不要运行工具链更新。

请团队自行决定原始题目、数据、第三方技能副本和论文是否可进入远程仓库，不要提交密钥或受限材料。
