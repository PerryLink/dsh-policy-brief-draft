# dsh-policy-brief-draft — 政策专报要素核对

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

<!-- topblock:v1 -->
> **这是什么**　政策专报要素核对。输出一份「哪一行、哪一栏、差什么」的清单。
> **给谁用**　政策研究、办公室写作；不用懂命令行。
> **你交什么**　这项核对用到的原始材料（表格、清单或文书）；不改原件。Excel 可先转成 JSON/YAML，对话里也能代转。
> **它不做什么**　不判合规、不认定责任、不替代审核人；只列材料内部能逐条指认的差异。
> **怎么开始**　在 WorkBuddy / 扣子搜「文书与治理核对包」（本检查是其中一项；上架以商城为准）；或命令行：
> `dsh plugin --profile <name> add dsh-policy-brief-draft`
<!-- /topblock:v1 -->

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-policy-brief-draft?metric=downloads)](https://dshfind.com/en/plugins/PerryLink/dsh-policy-brief-draft?ref=badge)

`dsh-policy-brief-draft` 读取一份政策专报（或研究报告）要素核对表——文件表头加每节一行——核对这份表自身的齐备与自洽：每节是否写明核心观点、观点是否有支撑依据、依据是否注明出处、数据截止日期是否可解析且不晚于核对日、数据是否落在你配置的新鲜度窗口内、建议事项是否写明实施主体、表头是否声明专报标题与报送对象、要点序号是否重复。

## Install

```sh
dsh plugin --profile <name> add dsh-policy-brief-draft
dsh --profile <name> --dump-config | grep 'dsh-policy-brief-draft'
```

## 实际输出长什么样

![dsh-policy-brief-draft 工作流图：调用 → 插件 → 结果。](docs/assets/dsh-policy-brief-draft-flow.svg)

*工作流概览：调用 → 插件 → 结果。下面的示例使用实际命令面。*


本插件对自己 `PB-001` 测试夹具的**真实输出**，不是示意图。规则库不伪造引文：每条发现都会写明所引条款，而各条 `excerpt` 现已是本仓已读文件的逐字条文。

## 它回答什么问题

### 示例

下表是示例集：第一行是详细走查，其余行是简短案例。

#### 详细输出

**工具** `policy_brief_draft`

**输入**

~~~json
{"title":"某某领域投资形势分析专报","rows":[{"序号":"1","章节":"一、现状","核心观点":"","支撑依据":"全国固定资产投资统计月报（2026 年 2 月）显示本领域投资同比增长 3.1%"}]}
~~~
 
**输出**

~~~json
{
  "id": "dsh-policy-brief-draft.PB-001.de09b5a6",
  "ruleId": "PB-001",
  "severity": "error",
  "locator": {
    "row": 1,
    "field": "point"
  },
  "found": "第 1 行「point」为空",
  "expected": "「point」应填写",
  "fix": "补填核心观点；本条只核对是否写明，不判断观点是否成立"
}
~~~

*来源 `dsh-policy-brief-draft/tests/fixtures/PB-001/PB-001-unsafe.json (cases.json expects 1×PB-001); executed parseMaterial+runCheck, checkedAt=2026-10-06T00:00:00.000Z`*

| 你会问 | 它怎么答 |
|---|---|
| 有一节全是材料、没有结论，观点栏是空的。 | `PB-001` 会报出这一节：每节都应写明核心观点。它只核对 `point` 栏是否填写，因此不判断观点是否正确、是否有新意。本条为 `error`：第十九条（三）明文要求「观点鲜明」，该条已于 2026-10-13 逐字取得。 |
| 依据栏和出处栏都填了，插件到底核对了什么？ | 只核对这两栏是否填写。`PB-002` 要求每个观点都有 `evidence`，`PB-003` 要求其旁注明 `sourceRef`。`PB-003` 为 `error`：第二十条（四）把「引文等是否准确」列为签发前审核重点；`PB-002` 仍为 `warn`，因为没有条文要求"每个观点必须附一条依据"。`PB-002` 不判断依据是否充分、是否真实、是否支持该观点；`PB-003` 不能核对出处是否存在、数据是否与出处一致——插件读的是核对表本身，从不读被引材料，编造的出处也会通过。 |
| 数据截止日期写成 `2026-03-15 09:30`，另有一节写的是晚于今天的日期。 | `2026-03-15` 与 `2026-03-15 09:30` 两种写法都能识别。`PB-004` 报出晚于核对日的 `dataAsOf`，即日期填错了或引用了尚未产生的数据；本条为 `error`：第十九条（二）要求「分析问题实事求是」、第二十条（四）要求「时间」准确，而晚于核对日的截止日期在事实上不可能成立。解析不了的值单独报出，不会静默跳过。数据本身是否可靠，它不判断。 |
| 新鲜度那条报的是 `skipped`，是不是说明数据没问题？ | 不是。`PB-005` 出厂 `maxDays: 0`，即未配置，于是它报告自身进入 `skipped`，而不是自己编一个天数；配置 `maxDays`（例如 `maxDays: 90`）才会启用。命中只表示数据比你配置的窗口更旧，不表示数据不可用——引用旧数据有时是必要的，请在备注里说明原因。本条为 `info`（其天数窗口取自本机构编辑口径，条例不规定任何天数）。 |
| 有一节写了建议，但没写由谁来实施。 | `PB-006` 会报出这一节：`recommendation` 栏一旦填写，就要求填写 `implementer` 栏。只作现状分析、不提建议的节不会被报出，本条不会去打扰这类节。它只核对实施主体是否填写，不判断建议是否可行、主体是否恰当。 |
| 专报本身要声明什么？同一序号能在表里出现两次吗？ | `PB-007` 要求表头声明 `title` 与 `recipient` 两项，如果你的表式还记录密级或专题，把它们加进它的 `fields` 即可。`PB-008` 报出表内重复出现的 `sectionNo`，比较时忽略空白字符，因为序号重复会让评审意见无法准确指认要点。`PB-007` 只核对表头这两栏是否填写，不判断标题是否贴切、报送对象是否恰当；`PB-008` 只比对序号本身。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
|---|---|---|
| 《党政机关公文处理工作条例》 | 中办发〔2012〕14号（全文已取得，逐字回填至各条 `excerpt`） | PB-001, PB-002, PB-003, PB-004, PB-005, PB-006, PB-007, PB-008 |

**边界（中文译文，以英文原文为准）：** 本插件核对一份 **政策专报要素核对表** 中可被机械核对的部分——每节是否写明核心观点，观点是否有支撑依据，依据是否注明出处，数据截止日期是否可解析且不在未来，数据在你配置的窗口内是否足够新鲜，建议事项是否写明实施主体，专报是否写明标题与报送对象，以及要点序号是否唯一。它**不**判定观点是否正确、依据是否充分、建议是否可行、数据是否可靠，或专报是否应当报送。**这些是关于研究质量与决策价值的判断。**

> ### ⚠️ 本插件能看到什么、不能看到什么（以英文原文为准）
>
> **它读的是一份核对表，而不是出处或数据本身。** 因此它只能核对某个出处是否被*引用*——永远不能核对该出处是否存在，也不能核对数据是否与它一致。`PB-003` 在自身的 note 中写明了这一点，README 的排障一节也重申：编造的出处照样会通过，因为核实出处是另一件工作。
>
> **《党政机关公文处理工作条例》（中办发〔2012〕14号）已取得并逐字读过**，`rules/evidence/clause-verification.md` 记录了引用了哪些条文——第八条第（十）项（报告用于向上级机关汇报工作）、第十九条（起草：「分析问题实事求是」「所提政策措施和办法切实可行」「观点鲜明」）以及第二十条第（四）项，该项把「引文等是否准确」列为签发前的审核重点。
>
> **条款原文现已进入规则库，严重级也据此重新推导（2026-10-13）。** 该条例规范的是文件如何*起草与签发*；本插件核对的是专报的*提纲*是否记录了其观点、依据、出处与建议。这是两回事，因此规则是逐条套用的，而不是整批套用：
>
> - **条文明文写出该检查所寻找的要求之处时，提升为 `error`**：`PB-001`（19(3)「观点鲜明」）、`PB-003`（20(4) 把「引文等是否准确」列为签发前审核重点）与 `PB-004`（19(2)「分析问题实事求是」配合 20(4)「时间」——晚于核对日的截止日期不可能成立）。
> - **即使已取得原文，仍保持在 `warn`**，因为该条文讲的是另一件事：`PB-002`（没有条文要求每个观点必须附一条引文）、`PB-006`（没有条文要求写明实施主体）、`PB-008`（没有条文要求序号唯一），以及 **`PB-007`**——其第九条规范的是正式公文的十八个格式要素，而不是一份工作提纲的两栏：把一个空白的表头单元格说成对第九条的 `direct` 违反，等于把登记上的缺口包装成违规。
> - **仍为 `info`**：`PB-005`，其窗口是你的编辑口径，条例中完全没有这项规定。
>
> 因此**3 条规则为 `error`、4 条为 `warn`、1 条为 `info`**——这种划分本身就是要点，不是折中：取得原文，只在原文确实写到了被核对之事的地方，才允许作 `direct` 引用。见 `rules/evidence/clause-verification-gongwen-tiaoli-direct.md`，该文件也记录了它与 `clause-verification.md` 中早先分析不一致之处。
>
> **数据新鲜度窗口出厂时未设置。** 多旧算太旧是你的编辑口径——一份快报可能要求上个月的数据，而一份年度分析引用全年数据也属正当——因此 `PB-005` 的 `maxDays` 从 `0` 起步，该规则会把自己记入 `skipped`，而不是编一个天数。此项命中意味着「比你设置的窗口更旧」，从不意味着「不可用」；引用较旧的数据有时是对的，解决办法是在备注中说明原因。
>
> **数据新鲜度窗口出厂时未设置。** 多旧算太旧是你的编辑口径——一份快报可能要求上个月的数据，而一份年度分析引用全年数据也属正当——因此 `PB-005` 的 `maxDays` 从 `0` 起步，该规则会把自己记入 `skipped`，而不是编一个天数。此项命中意味着「比你设置的窗口更旧」，从不意味着「不可用」；引用较旧的数据有时是对的，解决办法是在备注中说明原因。

## Compatibility

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-rc.2`。**已声明 `engines.dsh`**：0.2.1 起由宿主单独裁决，范围为 `>=0.2.1-0 <0.3.0` |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/policy-brief-draft.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-policy-brief-draft
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## PerryLink DSH Plugin Family

完整清单（62 个核查器 + 通用插件）见 [按材料选核查器](https://perrylink.github.io/zh/checkers/choose/)；本仓只是其中一个。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-policy-brief-draft contributors.
