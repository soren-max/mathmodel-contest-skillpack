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

## mm 现场导航配置

按官方材料确认全部题号后才把 questions_verified 改为 true；不要用 cache 手改状态。

```mm-layout
{
  "questions": ["q1", "q2", "q3", "q4"],
  "questions_verified": false,
  "competition_mode": true,
  "final_paper": "paper/final.pdf",
  "reproduction_entry": "src/reproduce.py",
  "required_python_modules": []
}
```

`mm status` / `mm next` 只读，`mm refresh` 只原子更新 `project/contest_state.json`。
产物协议见安装源 SkillPack 的 `docs/execution-cli.md`，或仓库对应版本文档；不复制整套 docs。
运行后保存 `results/qN_run.json`（entry、command、exit_code、inputs、config、outputs、figures 相对路径）。
审计 `notes/qN_audit.md` 写独立 `verdict: PASS` / `PASS WITH LIMITATIONS` / `BLOCKED`；
验证 `reports/qN_validation.md` 写 `verdict: PASS` 和 `evidence: <真实验证文件>`，均保留解释和证据正文。
`reports/data_contract.md` 用独立 `verdict: PASS` 标识已核验的数据契约。
Gate 读取 `mm gate qN --json` 的 artifact_sha256，审查后在 `reports/question_status.md` 写
`<!-- mm-gate {"question":"qN","verdict":"MVP_CLOSED","artifact_sha256":"实际审查的指纹"} -->`。
可用 verdict 为 BLOCKED/PARTIAL/MVP_CLOSED/CLOSED；预检不自动签发闭环。
终审在 `reports/gmcm_final_review.md` 写独立 review_mode、verdict、artifact_sha256 字段，指纹从 `mm final-check --json` 获取。
证据变化后必须复审，refresh 不能续签审查。
