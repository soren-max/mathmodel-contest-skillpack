# 项目目录与产物约定

| 路径 | 职责 |
| --- | --- |
| `data/raw/` | 只读原始数据，保留来源与哈希 |
| `data/processed/` | 脚本生成的数据，保留处理规则 |
| `src/` | 逐问代码、公共模块与执行入口 |
| `results/` | 原始精度结果、`paper_metrics.yaml`、实验配置及运行日志 |
| `figures/` | 由真实结果生成的论文图，保留绘图入口 |
| `notes/` | 路线审查、结果审计、handoff、版本记录 |
| `reports/` | data contract、问题闭环状态、Evidence Matrix 与 GMCM 终审 |
| `paper/` | 论文整合稿与最终提交稿 |
| `materials/` | GMCM rubric、已核实当届规则、模板、参考材料 |
| `project/` | J/F/L 看板、接口约定、环境与复现命令 |
| `problem_files/` | 官方赛题原件 |
| `.agents/skills/` | 冻结的官方 MathModel Codex Standard 技能包 |
| `.agents/third-party/` | 随项目保留的上游许可证 |

推荐逐问命名：`src/q1.py`、`results/q1/`、`figures/q1_*`、`notes/q1_model_plan.md`、`notes/q1_audit.md`、`notes/handoff_q1.md`。为结果建立“代码 → 输入 → 配置/种子 → 输出 → 图表 → 论文数值”追溯链。

上游若生成 `paper_output/` 或 `paper_rewriting_output/`，在此追加实际映射和唯一提交稿位置，不把临时输出当作最终提交稿。
