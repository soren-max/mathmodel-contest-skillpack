# Mathematical Modeling Contest Working Agreement

Correctness first. Reproducibility. Mathematical interpretability. Paper-ready outputs.

## Modeling

写代码之前，为每一问在 `notes/qN_model_plan.md` 明确：问题、变量及单位、假设、输入/输出、候选模型、baseline、选择理由。先审查数学本质与数据支持，再选择方法；不得因为模型流行就选，也不得机械套用“预测→XGBoost、评价→TOPSIS、优化→GA”。

先完成可以端到端运行的 MVP。记录后续问题对当前输出的依赖，保证指标、事件定义、单位和时间粒度一致。

## Data

`data/raw/` 永远只读；原始附件保留原文件、来源、获取日期和校验和。处理结果写入 `data/processed/`，用脚本记录每一步转换及输入输出。不得静默删除异常值：报告规则、数量、理由和保留异常值时的对照。缺失值填补、标准化及特征选择只在训练数据拟合。

## Validation

严格检查时间泄漏、train/test contamination、target leakage、metric correctness、baseline、residuals、constraints、sensitivity。按任务使用时间/分组切分；优化问题检查可行性、约束误差及求解状态。记录随机种子、重复实验、依赖版本、配置和运行命令。

负 R² 允许存在。不得为了指标好看修改评价口径、挑选样本、隐藏失败实验或负结果。比较必须使用相同样本、切分、权重和指标定义。不适用的检查说明理由，不能假装已经验证。

## Results

所有论文数字必须来自真实运行结果，能追溯到脚本、输入版本和结果文件。禁止编造、手填假数据、不一致四舍五入、图表与正文数字冲突。原始精度保留在 `results/`；展示精度统一约定。示例数据必须标注为示例，不得进入论文证据。

核心论文数字统一登记在 `results/paper_metrics.yaml`；摘要、正文、表格和图注只优先使用 `approved_for_paper: true` 的条目。存在值、定义或单位冲突时不得批准。

同一事件或指标维护唯一口径；记录样本量、单位、分母、时间窗口和不确定性。结果变动时同步重生成图、表、正文引用和 handoff。

## Claims

严格区分 correlation（相关系数）、association（统计关联）、prediction（预测能力）、causality（因果效应）。没有因果识别设计不得使用因果措辞。弱统计关系不能写成强结论，预测性能不能证明机制。

## Paper

每一问完成必须有 mathematical formulation、code、result、validation、figures、interpretation、limitations、paper handoff。确实不需要图时说明理由。

每张正文图标记 Evidence Purpose：EDA / MECHANISM / MODEL / RESULT / VALIDATION / SENSITIVITY / OPTIMIZATION / DECISION。不能说明支持何种 claim 的图标记 `DECORATIVE_FIGURE`。

J/F 在 `notes/handoff_qN.md` 交付经过审查的结果，L 不从代码中重新猜数。论文数字以 handoff 对应的真实产物为准。重大结果问题由 `result-auditor` 优先阻断；先解决证据问题，再润色。

每一问正文遵循 Problem → Mathematical abstraction → Assumptions/Variables → Model formulation → Model selection reason → Solver/computation → Numerical results → Interpretation → Validation → Question conclusion → Link to next question。模型介绍优先回答为何适合本题，不写百科式算法说明。

每个核心公式必须有建立关系的理由、公式本身、变量/单位与数学或工程意义及后续用途；每个核心图表必须有 Purpose、Observation、Interpretation、Implication。每问末尾写清答案、最重要结果、结论、限制和下一问接口。

摘要逐问硬性包含 Problem、Method、Result，三项缺一不可；模型属于 Method。所有摘要关键数字必须来自 `approved_for_paper: true` 的 registry 条目。模型名称、参数、样本数、评价指标、最优值、变化百分比和显著性结论必须可追溯到 code/config/derivation、result、Evidence Matrix 及适用的批准 metric。

优秀论文 corpus 仅学习章节组织、数学叙事、结果解释、验证写法和摘要结构，不复制或近似改写原文。

如使用 PaperSpine，只把它作为已审计 GMCM 产物的下游写作整合器：handoff、Evidence Matrix 和批准 registry 仍是 source of truth，PaperSpine 不重新选模或重算数字，最终稿仍运行 `gmcm-final-reviewer`。

`paper/` 保存整合稿。若上游工作流要求 `paper_output/` 或 `paper_rewriting_output/`，保留它们作为生成目录，在 `project/project-layout.md` 记录映射，避免多个“最终版”。不得伪造引用。

## Competition strategy

三天或有限时间比赛采用 **Complete first → Validate → Improve**。执行 `each question → MVP_CLOSED → next question → later improvement`；不要为了 Q1 完美让 Q3/Q4 未完成。赛前更新，比赛期间冻结 SkillPack、上游缓存和计算依赖版本。

## Team ownership

| Owner | 默认职责 | 交付接口 |
| --- | --- | --- |
| J | modeling / core coding / Agent / technical QA / validation / coordination | 数学路线、模型实现、统一技术接口与交叉审查 |
| F | data / experiments / visualization / verification | 数据处理、实验、图表、独立核验 |
| L | paper / mathematical expression / integration / formatting | 数学表达、逐问整合、摘要和提交格式 |

三个人都是 owner，不是一个核心两个辅助。赛前共同确认职责、逐问负责人、交叉审查人、截止时间；在 `project/` 保存任务看板。共享接口与结论，不并发覆盖同一文件。这里的角色分工不自动授权创建 AI 子代理或对外发送信息。

J 不长期承担普通数据清洗、普通绘图或格式排版；F 与 L 对各自交付完整负责，并共同审查最终数字与结论。

## Git and submission

`main` 加短期 feature branches；小步提交、PR、交叉 review 后合并。禁止自动 force push、`reset --hard` 用户项目、修改全局 Git config 或 Codex settings。不得保存 API key 或读取 secrets。

官方赛题放 `problem_files/`，官方规则与模板放 `materials/`。先核对当届赛区的匿名、格式、附件及 AI 使用/披露要求并记录来源。清理误带的内部路径、Prompt、Agent 日志；不得删除官方要求的 AI 使用披露来隐藏实际使用。最终模型和论文必须人工复核。
