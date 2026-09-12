# GMCM v1 Release Readiness

当前版本：**GMCM-first v0.95**。总体：**READY WITH LIMITATIONS**。
本轮完成执行层硬化，不代表 72 小时真实比赛表现已验证。

| 项目 | 状态 | 可核查证据 |
|---|---|---|
| Core skills complete | READY | 11 个现有自定义 Skills；未新增 Skill |
| Corpus complete | READY | Core Corpus v1，8 篇原创提炼；本轮未扩充 |
| Deterministic benchmark | PASS | `python3 benchmarks/run_benchmarks.py`，5/5 smoke cases |
| CI | 配置完成；远端结果见本分支 PR checks | `.github/workflows/ci.yml`；push/PR；Python 3.10 / 3.12；本地同等检查通过后提交 |
| Routing documented | READY | `docs/skill-routing.md` + templates/AGENTS.md 精简规则 |
| 72h runbook complete | READY | `docs/gmcm-72h-runbook.md`，J/F/L、4–6h 同步、6h/3h/1h freeze |
| mm CLI tested | READY | 50 项离线测试（含 `tests/test_contest.py`），临时目录、缓存篡改/陈旧、阻断、只读、原子更新、final-check |
| E2E fixtures ready | READY | 工程预测 + 单机调度；真实运行结果、planted findings、人工评价规则；不等同 LLM 评估通过 |
| Real rehearsal completed | NOT READY | 尚未进行；只有 `docs/rehearsal-template.md` 空白模板 |

v1.0 的必要条件：执行层、CI PASS、routing、runbook、E2E fixtures，以及**至少一份完整真实旧题演练记录**（逐问 MVP 时间、可复现产物、论文、终审、冻结与复盘）。没有演练最多 READY WITH LIMITATIONS；远端 CI 未通过时不能声称 CI PASS。基础检查失败或真实闭环阻断未解决则 NOT READY。

## 实战限制

1. 尚未完成真实旧题全流程演练，72h 节奏与交接成本未经实测。
2. E2E 目前只验证 fixture 完整性/复现；Codex 发现率、虚报与交互负担待人工运行记录。
3. 机器字段与内容指纹需要现有 Skill/owner 正确维护；旧报告未绑定时保守拒绝闭环。CLI 不证明语义、真实运行或来源字段数值正确。
4. 共享 registry/矩阵/代码变更会保守使多问审查失效；大输入的内容哈希增加状态检查耗时。比赛中需测量并遵守数字冻结。
5. 年度规则、实际 Codex skill discovery、科学计算/求解器环境与终稿提交包仍需现场 doctor 和 J/F/L 核验；可选依赖不自动安装。

推荐发布：v0.95。完成演练并关闭暴露的实际阻断后，再判断 v1.0；本轮停止扩 Skill、corpus 与 orchestrator。
