# Evidence-Calibrated Communication Policy

证据校准表达与防御性写作控制。适用于建模说明、代码注释、README、结果、handoff、论文正文、摘要及终审；通过现有 Skills 执行，不新增 orchestrator，不处理字体字号等排版问题。

## Evidence > Rhetoric

证据强度优先于修辞。改写不得改变数值、比较口径、方法事实、适用域、不确定性或推断强度，不得隐藏负结果和真实局限。目标是减少模板表达、机械连接词、无意义自我削弱、重复观点和算法说明书写法，增加自然数学叙事、证据驱动表达、作者判断和工程解释：confident but evidence-calibrated。

禁止把 AI detector、AI score、降低 AI 检测率或绕过 AI 检测作为优化目标或质量指标。表达质量按信息功能、逻辑与证据判断。

## Defensive writing 与 valid limitation

按句子提供的技术信息及证据分类，不按谨慎词命中次数分类：

| 类别 | 判断依据 | 处理 |
|---|---|---|
| `DEFENSIVE_WRITING` | 无证据、自我贬低、没有信息增量 | 删除；若背后有真实技术问题，改写为具体边界 |
| `UNJUSTIFIED_HEDGING` | 无依据地用“可能、也许、意义有限”等削弱 claim | 核对证据后删除空泛保留语或写明不确定性的来源 |
| `VALID_LIMITATION` | 数据、假设或实验支持的适用限制，即 evidence-calibrated limitation | 保留并随 claim 传递，不算写作缺陷 |

“由于能力有限”“本文模型较为简单”“可能存在诸多不足”“结果仅供参考”“受篇幅限制无法深入讨论”“仍有很多值得进一步研究之处”若没有实际技术信息，应删除或重写。简单模型本身不是缺陷。

以下表达在有相应证据时必须保留：不同时间折的关联方向不稳定；模型未显著优于 baseline；缺少实际事件时刻且无因果识别设计，因此只能解释统计关联；优化结果是启发式获得的最佳可行解，无法证明全局最优。没有显著性检验时只能报告指标比较，不能把“未优于”写成“未显著优于”。

不得自动删除 `only / limited / weak / unstable / not significant / did not outperform / uncertain / cannot identify causality`。是否保留的依据是证据；证据不足时写明未知内容，不能为了语气坚定补造结论。

真实 limitation 推荐写成 `Scope → Technical reason → Consequence → Possible remedy`。例如：数据未记录实际振打触发时刻，无法构造严格事件前后窗口，周期与峰值的结论限于统计关联；若取得设备触发日志，可进行事件窗口分析。remedy 是条件性后续方案，不冒充已经完成的验证。没有观察到的局限不得凭空制造。

## 自然句式与段落功能

- “首先、其次、再次、然后、最后、综上所述”不完全禁用；仅在确有明确顺序或总结关系时使用，避免将各问写成流水账。
- 用内容关系过渡：因果“由于/因此”、转折“然而/相比之下”、递进“在上述模型基础上/进一步将/由此可将”、承接“根据问题一得到的/利用前述估计结果”、条件“在满足约束的条件下”、解释“这表明/从工程角度看”。因果连接词不能将关联偷换为因果；不要为了变化强换词，逻辑清晰优先。
- 避免连续多个“本文采用/本文建立/本文得到/本文分析”。按内容混合短句、复合句、条件句、解释句、数学表达和必要插入说明；不得故意制造长难句、文学化表达、模糊主语或不必要倒装。目标是 precise、compact、readable。
- 每段至少承担 `Problem / Reasoning / Definition / Model / Evidence / Interpretation / Transition / Conclusion` 中一种信息功能，不要求将标签写进论文。只介绍常识、重复标题或上一段、夸模型、介绍算法百科的段落，应考虑删除或压缩；理解本题模型所必需的背景可以保留。

## 跨段 semantic claim 审查

按“对象、条件、方向、幅度及推断范围”识别同一观点，不以字面相似代替语义审查。必须检查：相同观点换词重复；同一优势多章反复出现；摘要、正文、结论机械复制；模型评价与结论重复；问题分析与模型建立重复；图前图后重复同一句结论。

相同 semantic claim 优先保留证据更强、位置更合理的一处，其余删除、压缩或赋予新的信息功能。摘要的独立可读性、结论的最终答案和理解 claim 所必需的限制仍须保留；压缩不能使任何一问缺少 Problem/Method/Result，也不能移除正文唯一证据。

## 建模与代码表达

建模说明回答数学结构、baseline、升级理由、新模型针对的 baseline 缺陷、数据能否支持复杂度、后续问题是否需要该输出。优先采用 `Baseline → observed deficiency → justified upgrade → validation`；未运行的比较只能是验证计划。

没有明确模型比较设计时，不得用“为提高精度加入多个先进模型”“考虑到不足再加入模型 X”“为保证可靠同时采用 A/B/C/D”作为选择理由。禁止 algorithm stacking for reassurance。已有同口径比较设计时，写清候选假设、评价标准与停止条件。

代码注释和 README 解释 `WHY / ASSUMPTION / CONSTRAINT / NON-OBVIOUS LOGIC`，保留运行与复现所需内容，不复述显而易见代码。例如 `pd.read_csv(...)` 无需配“Read CSV file”；时间排序可说明 `Keep chronological order because downstream validation is time-based.`

未经实验验证，不写 `This feature significantly improves performance`；可写 `Candidate lag feature; validate against the lag-0 baseline before use.` 最终仓库中的 `TODO / HACK / temporary / maybe / probably` 逐项核对是否仍成立：解决过的更新或删除，未解决的说明技术影响，真实不确定性保留。不得靠删标记隐藏未完成工作。

## 结果与安全表达范围

结果直接报告 `metric / comparison / direction / magnitude / stability`：给出指标、同口径 baseline、变化方向与幅度，以及实际检查过的稳定性；未测稳定性应注明，不补造。避免“效果一般所以意义有限”与“优异效果充分证明先进性”两种极端。

以下数字仅是措辞示例，不是可用论文证据：

- “随机森林测试集 RMSE 为 4.21，相比线性基线 5.03 降低 16.3%。”实际采用前，两个指标及降低比例都须经 registry 批准；该句本身不证明显著性或稳定性。
- “该模型 RMSE 为 5.08，未优于线性基线的 5.03，因此后续分析仍采用线性基线。”负结果可成为模型选择依据，不能被润色成提升。

所有核心论文数字来自 `results/paper_metrics.yaml` 且 `approved_for_paper: true`。表达的强弱由真实指标、检验和 `reports/evidence_matrix.md` 决定，不按形容词偏好决定。

## 摘要、正文、公式与图表

执行 [Paper Narrative Contract](paper_narrative.md) 的逐问内容与追溯要求。正文推荐用问题、数学抽象、变量/假设、模型、选择理由、求解、结果、解释、验证、结论和下一问接口组织内容；不是“算法 A 介绍 → B 介绍 → C 介绍 → 结果”。

模型介绍优先回答 **Why this model here?**，只保留影响本题建模的算法原理。例如引入随机森林应联系当前数据支持的非线性、交互及线性 baseline 缺陷，不堆算法发展史，也不把这些特征假定为已证实事实。

核心公式检查 `Before: 为什么需要 → Equation: 数学关系 → After: 变量、数学/工程意义、后续使用`；无解释的连续公式以及从未用于求解或结果分析的公式需要修复或删除。

核心图表形成 `Purpose → Observation → Interpretation → Implication`。“结果如图 5 所示”不构成分析。所有解释受 Evidence Matrix 约束；例如功率下降幅度最大，不能单凭这一观察就断言原始电压冗余最大。机制未验证时可说明可支持的决策含义、候选解释及其边界，不得为了补解释伪造机制。

摘要每问最高优先级的三个必备要素是 **Problem / Method / Result（HARD REQUIREMENT）**。Model 属于 Method，Interpretation / Engineering Meaning 是 Result 后的增强，不增加第四、第五个必备要素。终审必须原样输出：

| Question | Problem | Method | Result | Status |
|---|---|---|---|---|

三项全部存在、具体、与证据一致才 PASS。“针对问题一建立模型 A”到此结束不通过；“效果较好、具有较高精度、取得显著提升、模型有效”而无结果证据，按 Result 缺失处理。Result 优先包含数值、参数、误差、比例、可支持的最优方案、分类结果、阈值或工程策略；核心数字逐项关联批准 registry，非数值结果也须有证据。

PMR 是信息结构，不是固定句式；不要强制每问写“针对问题 X，本文首先……然后……最终……”。

结论聚焦每问最终答案、关键数字、策略含义和总体工程意义，不复制摘要，不重复模型百科、算法流程或完整验证过程。仅保留真正影响结论解释的限制，并确保详细局限仍可定位。

## Findings 与修改等级

类别与严重程度分别记录；同一类别按实际影响分级，关键词不自动决定 finding。`VALID_LIMITATION` 是应保留的审计判断，没有缺陷等级。

| Finding | 检查内容 |
|---|---|
| `DEFENSIVE_WRITING` | 无技术信息的自我贬低 |
| `TEMPLATE_WRITING` | 机械连接、句式和流水账 |
| `REPETITIVE_CLAIM` | 跨段同义重复，没有新信息功能 |
| `ALGORITHM_ENCYCLOPEDIA` | 通用算法知识替代本题选择理由与模型 |
| `EQUATION_WITHOUT_NARRATIVE` | 核心公式缺动机、解释或用途 |
| `RESULT_WITHOUT_INTERPRETATION` | 结果缺数学/工程含义或适用边界 |
| `FIGURE_WITHOUT_CLAIM` | 核心图表缺四要素或不能支撑 claim |
| `UNJUSTIFIED_POSITIVE_LANGUAGE` | 无证据的积极包装、显著性或优越性 |
| `UNJUSTIFIED_HEDGING` | 无依据削弱 claim，须与 VALID_LIMITATION 区分 |

| Severity | 判据 | 处理 |
|---|---|---|
| `CRITICAL` | 改变证据强度、隐藏负结果、因果过度声明、数值与结果冲突、方法与代码冲突；关键数字未经批准或关键 claim 不可追溯 | 必修，修复后复验，不能靠措辞掩盖 |
| `MAJOR` | 一问缺 Problem/Method/Result、大量算法百科、结果无解释、严重重复、多问叙事断裂 | 修复内容缺口；若还改变证据或存在数值/方法冲突，相关问题升为 CRITICAL |
| `MINOR` | 机械连接词、个别句式重复、局部生硬措辞 | 局部修订，不扰动已验证内容 |

严重程度不等于通过状态：摘要缺 PMR 虽是 MAJOR，仍不得把该问判 PASS，也不能给出内容通过建议。`competition_mode: true` 时优先 CRITICAL 和影响作答的 MAJOR，不在 MINOR 上花大量时间；按现有 `estimated_fix_time / expected_score_gain / risk / priority` 与 `FIX_NOW / FIX_IF_TIME / DO_NOT_TOUCH` 排序，不把语言分数替代证据要求。

## 现有 Skill 的责任

| Skill | 执行职责与产物 |
|---|---|
| modeling-reviewer | 在 model plan 中阻止防御性加模型，记录 baseline 缺陷、升级证据和验证计划 |
| result-auditor | 在 audit 中让结论强弱匹配指标，保留负结果、稳定性信息和真实限制 |
| paper-handoff | 交付 Evidence Matrix 支持的允许表达、禁止表达及必须保留的限制 |
| repo-paper-auditor | 核对 claim 与代码/证据，检查注释和 README 中的未验证结论及未完成标记 |
| gmcm-final-reviewer | 终审叙事、重复和表达，输出 PMR 表、分类 findings 与保留的 VALID_LIMITATION |
