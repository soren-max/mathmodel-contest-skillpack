# MathModel Contest SkillPack

Reusable Codex workflow for mathematical modeling competitions.

Supported:

- CUMCM
- China Postgraduate Mathematical Contest in Modeling / Huawei Cup
- MCM / ICM
- MathorCup
- other modeling competitions

Goals: correct problem decomposition, justified model selection, reproducible computation,
leakage-free validation, result consistency, paper-ready evidence, reviewer-oriented QA.

这是工具链管理仓库：保存锁定版本、安装脚本、项目模板和五个原创流程 Skill，**不镜像或 vendor 第三方完整源码**。第三方从官方 GitHub 克隆至用户缓存，版权归原作者。本工具不保证获奖；最终建模和论文必须人工复核。

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
mm-init ~/projects/CUMCM-2027
cd ~/projects/CUMCM-2027
codex
```

先使用 `$contest-project-bootstrap`，放入官方材料、确认 J/F/L 分工，再使用 `$modeling-reviewer`。完整流程见 [docs/workflow.md](docs/workflow.md)。

## 安装边界

| 内容 | 缓存/源 | 安装位置 |
| --- | --- | --- |
| MathModel Standard，10 Skills | `~/.local/share/mathmodel-stack/MathModel-Skill` | 仅由 mm-init 复制官方 Codex 包到 `<project>/.agents/skills/` |
| scibox-figure、scibox-diagram | `~/.local/share/mathmodel-stack/sci-box` | `~/.codex/skills/` 下同名软链接 |
| paper-spine | `~/.local/share/mathmodel-stack/PaperSpine` | `~/.codex/skills/paper-spine` 链接官方 `dist/codex/skills/paper-spine` |
| 五个自定义 Skills | 本仓库 `skills/` | `~/.codex/skills/` 下同名软链接 |
| mm-init | 本仓库 `bin/mm-init` | `~/.local/bin/mm-init` 软链接 |

不要删除或移动安装后的本仓库和缓存，否则链接会失效。MathModel 不全局安装，不混装 Standard/Lite。检测到同名全局 MathModel 时会停止并提示人工处理。

**Codex 路径兼容性：** 按本项目约定保留 `${CODEX_HOME:-~/.codex}/skills`。当前 [OpenAI 官方文档](https://developers.openai.com/codex/skills/) 列出的用户级发现目录为 `~/.agents/skills`，项目级为 `.agents/skills`，并支持目录软链接。不同版本对旧路径支持可能不同；安装后用 `/skills` 核对这 8 个全局 Skill。若当前版本不发现旧路径，可自行为这 8 个目录逐个添加 `~/.agents/skills/<name>` 软链接；先检查同名冲突，不要把整个 `.codex/skills` 再复制一遍。安装器会提示该兼容项，不修改 Codex settings，也不将“文件存在”当成实际路由已验证。

PaperSpine 官方安装器会写入多个宿主并替换已有目录，因此这里只链接其提交内已生成的 Codex 包，不执行全宿主安装，也不安装 `/paperspine` prompt；通过 `$paper-spine` 使用。许可证与具体路径见 [docs/third-party.md](docs/third-party.md)。

安装只需要 Python 标准库，不会自动安装科学计算依赖、求解器、绘图环境、LaTeX 或 Word 渲染工具。按赛题建立独立计算环境，并记录可重跑命令。

## 版本锁定与更新

[config/sources.lock](config/sources.lock) 是 JSON，记录 repo、branch、完整 commit SHA、官方 Skill 路径和预期名称。普通安装只检出锁定 SHA；已有对象齐全时可离线重装，不跟随上游 HEAD。缓存有本地修改、来源不符、文件冲突或布局变化时停止，不覆盖用户文件。

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

- `install.sh`：依赖与冲突检查、官方 clone/fetch、固定提交 checkout、全局链接、mm-init 链接，最后执行与 `verify.sh` 相同的检查。
- `verify.sh`：只读检查，输出 PASS / WARN / FAIL；FAIL 返回非零，PATH/CLI/发现路径提示为 WARN。不会修改环境。
- `mm-init <directory>`：独立 Git 项目、11 组工作目录、10 个项目级 Skill、许可证、来源 JSON、模板和含 UTC 时间及四项 commit 的版本记录。已有父仓库内的子目录会被拒绝，避免误接入其他项目。
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
| result-auditor | PASS / PASS WITH LIMITATIONS / BLOCKED 的证据审计 |
| paper-handoff | J/F → L 的统一逐问数学/结果交接 |
| final-paper-reviewer | Critical / Major / Minor 的终稿问题清单 |

## 文档与测试

- [工作流](docs/workflow.md)
- [竞赛适配](docs/competitions.md)
- [三人 Git 工作流](docs/git-workflow.md)
- [来源与许可证](docs/third-party.md)

```bash
bash -n install.sh
bash -n update.sh
bash -n verify.sh
bash -n bin/mm-init
python3 -m unittest discover -s tests -v
git diff --check
```

集成测试使用临时目录和本地 Git 上游，覆盖锁定安装、幂等、冲突保护、版本更新/回退、已有比赛冻结、路径隔离与版本记录，不修改真实比赛或用户配置。
