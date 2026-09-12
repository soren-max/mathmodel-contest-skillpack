# mm 执行层与产物协议

`mm` 是标准库实现的检查/导航 CLI，不是 Agent：不选模型、不写论文、不执行实验、不调用外部 API、不改结果、不操作 Git 写入。除 `refresh` / `status --refresh` 外均只读；刷新只写 `project/contest_state.json`。在项目根运行，或使用 `mm --project /path/to/contest status`。全部子命令支持 `--json`。

| 命令 | 输出 / 退出码 |
|---|---|
| `mm status` | 真实产物推导的状态、逐项缺口、STATE_DRIFT、一个下一步；正常检查返回 0 |
| `mm next` | 一个固定流程中的下一步及原因；返回 0 |
| `mm gate q1` | deterministic precheck + 当前 artifact_sha256；PARTIAL/BLOCKED 返回 1，就绪返回 0 |
| `mm refresh` / `mm status --refresh` | 检测到的 drift、changed fields、推荐行动；临时文件 + fsync + atomic replace |
| `mm doctor` | 环境、安装、项目 Skill 与依赖检查；FAIL 返回 1，只有 WARN 返回 0 |
| `mm final-check` | NOT READY 返回 1；READY FOR HUMAN FINAL REVIEW 返回 0；始终人工确认提交 |

格式/路径/读取错误返回 2，并显示具体错误。`status` 返回 0 只表示完成检查，不表示可提交。预检不能证明数学正确、真实运行或报告诚实。

## 唯一事实来源

| Truth | Source |
|---|---|
| Problem truth | official materials / `problem_files/` |
| Code truth | `src/`（或布局映射的 `code/`）+ run config |
| Result truth | reproducible results |
| Paper number truth | `results/paper_metrics.yaml` |
| Claim truth | `reports/evidence_matrix.md` |
| Question completion truth | `reports/question_status.md`，由 question-completion-gate 审查 |
| Paper writing input | `notes/handoff_qN.md` |
| Final paper verdict | `reports/gmcm_final_review.md` |
| contest_state | navigation cache only；不批准数字、不覆盖任何报告 |

JSON cache 的 `schema_version: 1`、competition、competition_mode、questions 保持机器可读；每问包含 status、precheck、checks、artifacts、review_verdict、review_fresh、artifact_sha256。初始 questions 为空，首次 refresh 从布局和产物生成。手改 status 无法提升实际状态；CLI 比较每个字段并输出 STATE_DRIFT。缓存丢失或损坏可 refresh 修复；不依赖缓存找问号，也不会执行缓存中的路径或命令。

## 现场最小产物协议

沿用现有 Markdown 报告；机器字段是报告的索引，不替代正文证据。旧报告若没有可识别字段，保守显示 MISSING/UNVERIFIED，人工/对应 Skill 审查后补字段。不要为了绿灯伪造标记。

在 `project/project-layout.md` 维护唯一 `mm-layout` fenced JSON 块。`questions` 须按官方题目核对，之后才设置 `questions_verified: true`；初始化默认 q1–q4 只是待确认导航范围。CLI 还合并文件名、gate、registry 中发现的 qN，不能通过从 cache 删除某问隐藏缺口。错误题号须回源纠正。`competition_mode` 默认为 true。

可选 `artifacts.q1` 映射 `model_plan/run/audit/validation/handoff` 到非标准相对路径；Evidence Matrix 始终以 `reports/evidence_matrix.md` 为唯一来源，不映射为副本。`final_paper` 和 `reproduction_entry` 指向唯一终稿和复现入口。`required_python_modules` 仅列本项目明确需要的 import 名称；缺失为 FAIL，其余可选包缺失只是 WARN。所有路径必须在项目内；不接受外部路径。

默认产物：

- `notes/bootstrap.md`：官方材料、题号和 J/F/L；`reports/data_contract.md` 顶层独立行 `verdict: PASS` 表示数据关卡通过。
- `notes/q1_model_plan.md`：现有 modeling-reviewer 的数学计划，CLI 仅查非空。
- `results/q1_run.json`：实际运行后保存的 manifest，见下例；输入、配置、代码、输出和图表必须非空。CLI 不运行其中 command，也不从文件名推断“运行成功”。
- `notes/q1_audit.md`：独立行 `verdict: PASS` / `PASS WITH LIMITATIONS` / `BLOCKED`；继续保留完整审计正文。
- `reports/q1_validation.md`：独立行 `verdict: PASS` 与 `evidence: results/q1_validation.json`，正文解释真实验证；该证据文件必须存在。
- `notes/handoff_q1.md`：现有完整交接。CLI 仅检查非空，内容由 gate/handoff/final-reviewer 审查。

```json
{
  "entry": "src/q1.py",
  "command": "python3 src/q1.py --config results/q1_config.json",
  "exit_code": 0,
  "inputs": ["data/processed/input.csv"],
  "config": "results/q1_config.json",
  "outputs": ["results/q1_result.json"],
  "figures": ["results/q1_table.csv"]
}
```

`figures` 可列图或替代表格；空列表不放行。所有输入文件须列出；大文件逐字节哈希有耗时，CLI 不重跑实验。配置、辅助代码、官方材料、审计、validation、handoff、矩阵、registry 和 manifest 引用的输入/结果进入内容指纹。共享代码、矩阵或 registry 改动会保守使受影响导航快照失效，要求复审；mtime 不用于判定。

Registry 默认使用 JSON-compatible YAML，无额外依赖。普通 YAML 只在已有 PyYAML 时解析，缺 parser 为 UNVERIFIED；不会自动安装。检查必需字段、批准状态、PASS、重复 metric_id 和脚本/结果路径；无法自动验证所有格式的 source_field 数值与摘要数字，仍由 registry Skill/终审核对。当前保守策略：registry 内任何冲突/未批准条目均阻断数字预检与 final-check，历史候选数字应保存在独立实验记录而非正式 registry。

Evidence Matrix 沿用 `Claim / Question / ... / Status` 表，Question 使用 q1/Q1。只有本问至少一行且所有 Status 为 PASS 才就绪。问题表可追加 Severity 和 Resolution 列；也可在文末增加 `Question / Finding / Severity / Resolution` 表。`CRITICAL` 未明确 `RESOLVED` 或 `FIXED` 则阻断；全局问题用 `all`。自然语言隐含问题由 reviewer 审查，CLI 不做关键词语义推理。

## Gate 与状态

`PRECHECK_BLOCKED`：audit/gate BLOCKED 或未解决 critical；`PRECHECK_PARTIAL`：MVP 必需产物不齐；`PRECHECK_MVP_READY`：计划、代码/运行、审计、validation、图/表、批准数字、handoff 齐全；`PRECHECK_CLOSED_READY`：再加本问 Evidence Matrix 全 PASS。后两者均不等于 LLM gate verdict。

`NOT_STARTED / PARTIAL / MVP_READY / BLOCKED` 由当前产物推导。只有 `$question-completion-gate` 审查后，在 `reports/question_status.md` 每问写一个元数据注释，verdict 为 MVP_CLOSED/CLOSED 且 hash 与当前 `mm gate q1 --json` 一致，才显示对应闭环状态：

```text
<!-- mm-gate {"question":"q1","verdict":"MVP_CLOSED","artifact_sha256":"<reviewed artifact_sha256>"} -->
```

PARTIAL/BLOCKED 也用同一字段；不要由 CLI 自动签发闭环。正文保留证据位置、缺口、负责人、依赖。没有 hash 的旧闭环报告不自动升级；旧表中的 BLOCKED 仍阻断。重复/矛盾的元数据报错。产物变化后闭环 hash 陈旧，显示 REVIEW_STALE 并退回 readiness；refresh 不“续签” gate。

固定流程不变：初次 gate 可以记录 PARTIAL 与下游交接缺口，然后 repo-paper-auditor → paper-handoff，再对同一关卡复验。`mm next` 优先最早未闭环问题的缺失步骤；已经 MVP_CLOSED 的问题不为追求 CLOSED 抢占后续问题。可选 exemplar/PaperSpine 不被自动强插。

## 提交前

完成终稿后用 `mm final-check --json` 获取 final artifact_sha256。终审 Skill 阅读当前文件后在 `reports/gmcm_final_review.md` 写独立字段：

```text
review_mode: full
verdict: PASS
artifact_sha256: <reviewed final artifact_sha256>
```

未通过则写 BLOCKED/PARTIAL，不能为预检绿灯写 PASS。FAST 也必须满足该模式全部硬门并记范围。hash 包含所有逐问快照、gate、矩阵、registry、年度规则、终稿、paper 目录文件和复现入口；终审报告自身不纳入 hash，避免自引用。修改任何证据/论文后重审。`PASS WITH LIMITATIONS` 必须在正文记录允许的限制。

执行 `mm refresh`，由团队按正常 Git 流程保存修改，再运行 `mm final-check`。检查未闭环/blocked、registry、critical、handoff、有效终审、已核实规则与来源、终稿、复现入口、tracked raw PDF/corpus、staged/unstaged diff whitespace、工作区、TODO/HACK。`paper/` 内 PDF 是论文输出，不因扩展名拒绝；其他 tracked PDF 保守列为需人工处理的原始材料。高风险 TODO/HACK 须带 CRITICAL/HIGH_RISK/FIX_NOW，阻断；普通 TODO/HACK 列 WARN 交人工分诊，不把任何 TODO 一概断言为严重缺陷。

即使 READY FOR HUMAN FINAL REVIEW，J/F/L 仍要核对官方材料、数字、匿名/格式/引用、AI 披露与提交包。Git clean 和机器标记不能证明可以自动提交。
