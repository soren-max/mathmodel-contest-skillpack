# 三人比赛 Git 工作流

使用 `main` 加短期 feature branches。保持小提交和清晰文件归属，比赛期间不设计复杂 GitFlow。

| 分支示例 | 内容 |
| --- | --- |
| `j/q1-modeling` | 第一问数学路线和实现 |
| `f/q1-data` | 第一问数据、实验、图表及核验 |
| `l/paper-q1` | 第一问论文表达与整合 |

流程：pull → branch → work → commit → push → PR → review → merge。

```bash
git switch main
git pull --ff-only
git switch -c j/q1-modeling
# 完成当前问的小闭环并运行对应验证
git add src/q1.py notes/q1_model_plan.md
git commit -m "feat: add question 1 baseline"
git push -u origin j/q1-modeling
# 在 GitHub 开 PR，由另一位 owner 审查后合并
```

拉取前先检查 `git status`，保留未提交工作。冲突由相关 owner 按真实接口解决，不盲目选一方。禁止自动 force push、`reset --hard` 或改全局 Git config；普通 push 被拒绝时先 fetch/review 差异。

在 `project/` 记录文件归属、公共指标定义和合并顺序；同时编辑整合稿前先协调。合并结果变化后，重新运行对应审计并更新 handoff。不要自动提交受限数据、凭据、日志或没有授权公开的官方附件。

SkillPack 自身的 `sources.lock` 更新同样走 review。竞赛工程的版本记录随项目提交；项目 MathModel 副本是否进入远程由团队决定，随副本保留许可证与来源，不把第三方声明成原创。
