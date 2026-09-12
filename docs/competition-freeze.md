# GMCM Competition Freeze

版本：**GMCM-first v0.95**。

正式比赛开始后冻结 SkillPack、`config/sources.lock`、第三方缓存、orchestrator、项目模板和基础计算环境：

- 禁止随意升级 Skill 或更新 upstream。
- 禁止修改/新增总控 orchestrator 或引入竞争工作流。
- 禁止大规模重构工具链、批量更换模型或扩充 corpus。
- 禁止无验证地升级求解器、科学包或绘图环境。
- 只在实际阻塞题目闭环、复现、验证或提交时做最小修复。

最小修复必须记录：阻塞证据、影响范围、负责人、变更、回滚方法和复验结果。优先恢复 `MVP_CLOSED`，不得借修复之名重写稳定模型。比赛结束后再把通用修复带回 SkillPack 并走独立 PR。
