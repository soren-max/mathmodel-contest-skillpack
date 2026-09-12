# Human-in-the-loop repository E2E benchmark

两个小型、原创、合成仓库：Case A 工程时序预测；Case B 单机调度。包含题意、CSV 数据、可运行标准库代码、真实生成的结果和存在缺陷的论文段落。无需网络、科学包或完整历史数据。不扩 corpus。

这些不是完整旧题，不是完整模拟赛，也不能完全自动评估 LLM reasoning。`expected_findings.json` 是人工标注答案；确定性测试只验证样例可重跑、锚点存在和已植入缺陷仍在，不把它当 Codex recall/precision 成绩。

## 一次人工运行

1. 在临时目录复制一个 fixture，**先移出 expected_findings.json**，避免答案泄漏。保留独立评估者副本。初始化临时 Git repo；不要修改 fixture 源或真实比赛项目。
2. 从临时项目根运行上面的 problem.md 复现命令，保存原始结果。Case B feasibility 为 false 是故意的缺陷，不是 runner 故障。
3. 在该临时项目启动已安装的 `codex`。首次明确任务：“这是合成审计演练，审查现有方法、代码、结果和稿件；保存报告，不修改原始数据/代码/论文，不重跑到原输出目录。”不要向审查者提供 expected findings。
4. 按唯一 workflow 的对应阶段调用：`$data-contract-auditor` → `$modeling-reviewer`（只审查已给路线）→（已有 model/code）→ `$result-auditor` → `$verified-number-registry` → `$question-completion-gate` → `$repo-paper-auditor` → `$paper-handoff`。Case B 的路线/结果阶段使用现有 `$structured-optimization` 辅助。BLOCKED 时 registry 不批准、handoff 仅标草稿/不可用于论文。
5. 对已有 draft 调用 `$gmcm-final-reviewer` 进行可用范围内的审查；当前样例没有真实渲染终稿或完整 handoff，须记录输入缺失，不能声称满足最终提交前置条件。可分别跑 FULL 与明确要求的 competition_mode FAST，保存不同报告副本。不要靠造出 PASS 前置物解除阻断。
6. 保存 `reports/`、`notes/`、未批准 registry、命令、Codex/SkillPack commit、模式、起止时间、交互次数。结束审查后，评估者才打开 expected_findings.json 对照。

复制示例（从 SkillPack 根运行）：

```bash
case_dir="$(mktemp -d -t mm-e2e.XXXXXX)"
cp -R benchmarks/e2e/case_a_engineering "$case_dir/project"
mv "$case_dir/project/expected_findings.json" "$case_dir/expected_findings.json"
git -C "$case_dir/project" init
cd "$case_dir/project"
python3 src/forecast.py
codex
```

CLI 登录、交互、模型/预算等由现场环境决定。本轮不增加脆弱 subprocess 自动聊天系统，不在 CI 调用 Codex。

## 人工评分

按“发现了真实根因 + 定位代码/结果/论文证据 + 说明后果”计 detected；只喊风险、复述 planted 标题、只报缺 registry/handoff 不算抓住根因。允许同义分类或合并多个相关 finding，但每个必要事实必须明确覆盖。预期外真实问题经证据复核后可计 useful major，不机械当虚报。

| 字段 | 记录规则 |
|---|---|
| Critical findings detected | 命中的 expected critical IDs 与报告锚点 |
| Critical findings missed | 未定位/未解释的 expected critical IDs |
| False critical findings | 被标 critical 但没有证据或与文件事实矛盾的项，逐条说明 |
| Useful major findings | 真实、可操作、影响作答或审计的 major；记录 owner 和修复 |
| Runtime / interaction burden | 墙钟时间、人工提示次数、总轮次、报告体积、模型/模式 |
| recall-like | detected / planted critical 总数；该样例必须抓住全部 planted critical 才通过关键召回 |
| precision-like | confirmed critical / all reported critical；报告分母，不把零报告定义为满分 |

**人工 acceptance**：全部 planted critical 被抓住；无 false critical；major 建议有用；未隐瞒局限、未批准不可信数字。若存在多个等价拆分，先按根因归并再评分。用两例只能识别明显回归，不推断总体能力或比赛获奖概率。

每次评估另存记录（不要覆盖 expected labels）：

```text
Case / SkillPack SHA / Codex version / model / review_mode:
Start / End / Runtime / Interaction count:
Critical findings detected (IDs + evidence):
Critical findings missed:
False critical findings:
Useful major findings:
Recall-like numerator / denominator:
Precision-like numerator / denominator:
Too-heavy output / routing error / evaluator notes:
Human verdict:
```
