# Third-party sources and attribution

本仓库是安装与工作流管理工具。以下项目及其 Skill 归原作者所有，不属于本仓库原创内容；不将完整上游源码存入本仓库。根目录 MIT LICENSE 只适用于本项目自有代码与文档。

**当前 pinned commit 的唯一权威记录是 [config/sources.lock](../config/sources.lock)**，`update.sh` 只更新这一份记录，避免文档中的第二份“当前版本”失同步。可直接查看锁文件或运行 `bash verify.sh` 获取当前锁定 SHA。

| 项目 / GitHub | 用途 | 官方分支与安装来源 | 许可证（初始化时核验） |
| --- | --- | --- | --- |
| [yushui2022/MathModel-Skill](https://github.com/yushui2022/MathModel-Skill) | 问题分解、模型选择、数据、代码、证据、建模论文工作流 | standard；缓存完整 repo，仅将 `packages/codex/.agents/skills/` 复制到比赛项目 | MIT；Copyright (c) 2026 yushui2022，保留 LICENSE |
| [jihe520/sci-box](https://github.com/jihe520/sci-box) | scibox-figure、scibox-diagram | main；缓存完整 repo，全局链接 `skills/scibox-figure`、`skills/scibox-diagram` | 未发现仓库级 LICENSE，锁内记为 NOASSERTION；不能视为整个仓库采用 MIT |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | 中后期重构、论证审查、面向评委的论文审核 | main；缓存完整 repo，全局链接 `dist/codex/skills/paper-spine` | MIT；Copyright (c) 2026 PaperSpine contributors，保留 LICENSE |

初始化时实查的版本如下（历史快照，更新后以锁文件为准）：

| 项目 | 初始化 pinned commit |
| --- | --- |
| MathModel-Skill | `0cc261d90d21e4ed540b02b0c71018cdcd47af58` |
| sci-box | `9687d2a52037e92bf68a781b9b1e061ca03c8125` |
| PaperSpine | `1fe46f0e76aab800db381b0a0c392cebe14d86bf` |

sci-box 内 `skills/scibox-diagram/ATTRIBUTION.md` 与 `assets/icons/tabler/LICENSE` 为 Tabler 图标提供单独署名和 MIT 文本，版权归 Paweł Kuna。这不等同于 sci-box 全仓库许可。缓存和链接完整保留这些文件；如需再分发其脚本/模板，应先向上游确认授权范围。

PaperSpine 的官方 `install.sh` 调用 `src/scripts/sync_local_installs.py`，默认安装多个宿主，且复制函数会删除/替换目标目录。本仓库需要避免覆盖与多宿主副作用，因此使用官方已生成的 Codex 布局，不执行其全宿主 installer、不手改 dist，也不冒充重新实现了 PaperSpine。

MathModel 项目副本另附 `.agents/third-party/MathModel-Skill/LICENSE` 与 `.agents/mathmodel-source.json`。全局链接依赖完整缓存，缓存中保留 Git 历史元数据、根许可证和内含素材署名。升级前复核许可证、布局及上游安装副作用，不默认未来提交与当前版本相同。
