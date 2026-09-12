# MathModel Contest SkillPack

**Version: GMCM-first v0.95**

Current primary target:

- China Postgraduate Mathematical Contest in Modeling
- GMCM / Huawei Cup / 中国研究生数学建模竞赛

CUMCM、MCM、ICM 等以后适配；v0.95 不以通用性为目标。

Goals: correct problem decomposition, justified model selection, reproducible computation,
leakage-free validation, structured optimization, evidence consistency, paper-ready outputs,
and GMCM-oriented final review.

这是 GMCM-first 工具链仓库：保存锁定版本、项目模板、8 篇 Core Corpus 的原创提炼和 11 个边界清晰的流程 Skill，**不 vendor 第三方完整源码**。本工具不保证获奖；模型、代码、数值、引用和论文仍需三位 owner 人工审核。

## Quick Start

需要 Linux / WSL / macOS、Bash、Git、Python 3.10+、可访问 GitHub 的网络，以及另行安装的 Codex CLI。以下 SSH 克隆命令需要已经配置 GitHub SSH 访问；也可将 URL 换为 HTTPS。

首次安装：

```bash
git clone git@github.com:soren-max/mathmodel-contest-skillpack.git \
  ~/.local/share/mathmodel-contest-skillpack
cd ~/.local/share/mathmodel-contest-skillpack
bash install.sh
```

如 `verify.sh` 提示 PATH 缺少目录，在当前终端执行下面命令；需要永久生效时，自行将它加入 shell profile。安装器不会改 profile。

```bash
export PATH="$HOME/.local/bin:$PATH"
```

创建新比赛：

```bash
mm-init ~/projects/GMCM-2026
cd ~/projects/GMCM-2026
codex
```

先使用 `$contest-project-bootstrap`，放入官方材料并确认 J/F/L 分工，再执行唯一固定流程。完整顺序见 [docs/workflow.md](docs/workflow.md)。

## 安装边界

| 内容 | 缓存/源 | 安装位置 |
| --- | --- | --- |
| MathModel Standard，10 Skills | `~/.local/share/mathmodel-stack/MathModel-Skill` | 仅由 mm-init 复制官方 Codex 包到 `<project>/.agents/skills/` |
| scibox-figure、scibox-diagram | `~/.local/share/mathmodel-stack/sci-box` | `~/.codex/skills/` 下同名软链接 |
| paper-spine | `~/.local/share/mathmodel-stack/PaperSpine` | `~/.codex/skills/paper-spine` 链接官方 `dist/codex/skills/paper-spine` |
| 4 个 K-Dense 原子 Skills | `~/.local/share/mathmodel-stack/scientific-agent-skills` | 只链接 scientific-critical-thinking、statistical-analysis、statsmodels、uncertainty-and-units |
| 11 个自定义 Skills | 本仓库 `skills/` | `~/.codex/skills/` 下同名软链接 |
| mm-init / mm | 本仓库 `bin/` | `~/.local/bin/mm-init` / `mm` 软链接 |

不要删除或移动安装后的本仓库和缓存，否则链接会失效。MathModel 不全局安装，不混装 Standard/Lite。检测到同名全局 MathModel 时会停止并提示人工处理。

**Codex 路径兼容性：** 按本项目约定保留 `${CODEX_HOME:-~/.codex}/skills`。当前 [OpenAI 官方文档](https://developers.openai.com/codex/skills/) 列出的用户级发现目录为 `~/.agents/skills`，项目级为 `.agents/skills`，并支持目录软链接。不同版本对旧路径支持可能不同；安装后用 `/skills` 核对 18 个全局 Skill。若当前版本不发现旧路径，可为这些目录逐个添加 `~/.agents/skills/<name>` 软链接；先检查同名冲突，不要复制整个技能目录。安装器会提示该兼容项，不修改 Codex settings。

PaperSpine 官方安装器会写入多个宿主并替换已有目录，因此这里只链接其提交内已生成的 Codex 包，不执行全宿主安装，也不安装 `/paperspine` prompt；通过 `$paper-spine` 使用。许可证与具体路径见 [docs/third-party.md](docs/third-party.md)。

安装只需要 Python 标准库，不会自动安装科学计算依赖、求解器、绘图环境、LaTeX 或 Word 渲染工具。按赛题建立独立计算环境，并记录可重跑命令。

## 版本锁定与更新

[config/sources.lock](config/sources.lock) 是 JSON，记录 repo、branch、完整 commit SHA、license、purpose、install_mode、Skill 路径和选择清单。普通安装只检出锁定 SHA；已有对象齐全时可离线重装，不跟随上游 HEAD。缓存有本地修改、来源不符、文件冲突或布局变化时停止，不覆盖用户文件。

**赛前更新，比赛期间冻结版本。** 仅主动执行下面命令才查询新版本：

```bash
cd ~/.local/share/mathmodel-contest-skillpack
bash update.sh
git diff -- config/sources.lock
bash install.sh
bash verify.sh
# 审查更新后，把 sources.lock 纳入团队正常 Git 提交与 review。
```

`update.sh` 要求先安装且缓存与旧锁一致，fetch 指定分支，逐项显示当前/新 SHA，检出新提交并验证目录，最后原子写入锁文件。布局验证失败会将已切换的缓存检回旧 SHA；网络抓取失败不会改锁。它不会自动 commit 或 push。若上游改名/改布局，需先人工审查并更新安装映射。

全局软链接随缓存更新；项目内 MathModel 副本保持冻结。重复 `mm-init` 保留已有项目版本、技能、AGENTS、README 和最初版本记录，不自动给旧项目升级。已有项目不要混入新版本副本。团队需要归档 SkillPack commit、sources.lock、计算依赖和输入校验和。

## 命令行为与配置

- `install.sh`：依赖与冲突检查、官方 clone/fetch、固定提交 checkout、全局链接、mm-init / mm 链接，最后执行与 `verify.sh` 相同的检查。
- `verify.sh`：只读检查，输出 PASS / WARN / FAIL；FAIL 返回非零，PATH/CLI/发现路径提示为 WARN。不会修改环境。
- `mm-init <directory>`：独立 Git 项目、12 组工作目录、10 个项目级 MathModel Skill、GMCM rubric、年度规则空白覆盖、数字 registry、许可证、来源 JSON、contest_state 导航缓存和版本记录。已有父仓库内的子目录会被拒绝。
- install/update/init 共享操作锁，避免并行修改缓存。Git 网络操作设有超时，失败后先检查保留下来的目录再重试。

可选环境变量（同一安装的各命令保持一致）：

| 变量 | 默认值 | 用途 |
| --- | --- | --- |
| `MM_STACK_HOME` | `~/.local/share/mathmodel-stack` | 上游缓存 |
| `MM_CODEX_HOME` | `$CODEX_HOME`，未设置时 `~/.codex` | 隔离测试或指定安装目录 |
| `MM_BIN_DIR` | `~/.local/bin` | 命令链接目录 |

遇到同名用户文件或错误软链接，脚本显示路径并停止。请先自行备份/移走冲突项，再运行；没有 `--force`。脚本不删除用户重要目录、不 reset 用户项目、不改全局 Git 配置、不 force push、不读取 secrets 或保存 API key。

## 自定义 Skills

| Skill | 交付物 |
| --- | --- |
| contest-project-bootstrap | 启动检查、材料缺口和团队安排 |
| modeling-reviewer | 每问数学路线、baseline、候选比较和 MVP |
| exemplar-paper-retriever | 按数学结构检索最多三篇历史案例及不可照搬项 |
| data-contract-auditor | raw/processed 数据契约与阻断项 |
| result-auditor | PASS / PASS WITH LIMITATIONS / BLOCKED 的证据审计 |
| verified-number-registry | `paper_metrics.yaml` 数字来源、定义、单位与批准状态 |
| structured-optimization | 变量、目标、约束、可行域、solver 与最优后检查 |
| repo-paper-auditor | 题目到 paper claim 的 Evidence Matrix |
| question-completion-gate | BLOCKED / PARTIAL / MVP_CLOSED / CLOSED |
| paper-handoff | J/F → L 的统一逐问数学/结果交接 |
| gmcm-final-reviewer | 数学、实验、GMCM 竞赛叙事与证据一致性终审 |

## 文档与测试

- [工作流](docs/workflow.md)
- [竞赛适配](docs/competitions.md)
- [三人 Git 工作流](docs/git-workflow.md)
- [来源与许可证](docs/third-party.md)
- [可选依赖](docs/optional-dependencies.md)
- [比赛冻结](docs/competition-freeze.md)
- [GMCM rubric](rubrics/gmcm.md)
- [证据校准表达与防御性写作控制](rubrics/evidence_calibrated_communication.md)：Evidence > Rhetoric；五个现有 Skill 分阶段执行，保留真实局限和负结果，不以 AI 检测分数为目标。

```bash
bash -n install.sh
bash -n update.sh
bash -n verify.sh
bash -n bin/mm-init
bash -n bin/mm
python3 -m unittest discover -s tests -v
python3 benchmarks/run_benchmarks.py
git diff --check
```

集成测试使用临时目录和本地 Git 上游，覆盖锁定安装、幂等、冲突保护、版本更新/回退、已有比赛冻结、路径隔离与版本记录，不修改真实比赛或用户配置。

## v0.95 比赛执行层

执行层已加入；尚未完成一次真实旧题全流程演练，**不宣称 v1.0 实战验证完成**。
保留 11 个 Skill、8 篇 Core Corpus 与唯一 workflow；不增加建模能力、数据库或 orchestrator。

```bash
mm doctor
mm status
mm next
mm gate q1
mm refresh
mm final-check
```

`mm status --refresh` 可同时刷新缓存；各命令支持 `--json`，项目路径可用 `mm --project <dir> status`。
STATE_DRIFT 表示 cache 与真实产物不一致，refresh 不能替代 gate/终审复验。
提交前只会给 READY FOR HUMAN FINAL REVIEW 或 NOT READY，提交须人工确认。
终审默认 FULL；competition_mode 且用户明确要求时可 FAST，证据门槛相同。

- [CLI、状态、Source of Truth 与产物字段](docs/execution-cli.md)
- [Skill Routing Matrix](docs/skill-routing.md)
- [72h 现场 Runbook / J-F-L / Freeze](docs/gmcm-72h-runbook.md)
- [E2E fixtures 与人工评估](benchmarks/e2e/README.md)
- [v1 Readiness](docs/v1-readiness.md) / [真实旧题演练模板](docs/rehearsal-template.md)
- [GitHub Actions CI](.github/workflows/ci.yml)：离线确定性回归，不调用 Codex、不更新锁。
