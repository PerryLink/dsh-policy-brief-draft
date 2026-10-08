# dsh-policy-brief-draft — 政策专报要素核对

`dsh-policy-brief-draft` 读取一份政策专报（或研究报告）要素核对表——文件表头加每节一行——核对这份表自身的齐备与自洽：每节是否写明核心观点、观点是否有支撑依据、依据是否注明出处、数据截止日期是否可解析且不晚于核对日、数据是否落在你配置的新鲜度窗口内、建议事项是否写明实施主体、表头是否声明专报标题与报送对象、要点序号是否重复。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 有一节全是材料、没有结论，观点栏是空的。 | `PB-001` 会报出这一节：每节都应写明核心观点。它只核对 `point` 栏是否填写，因此不判断观点是否正确、是否有新意。因本次未取得明文条号，本条封顶 `warn`。 |
| 依据栏和出处栏都填了，插件到底核对了什么？ | 只核对这两栏是否填写。`PB-002` 要求每个观点都有 `evidence`，`PB-003` 要求其旁注明 `sourceRef`。`PB-002` 不判断依据是否充分、是否真实、是否支持该观点；`PB-003` 不能核对出处是否存在、数据是否与出处一致——插件读的是核对表本身，从不读被引材料，编造的出处也会通过。 |
| 数据截止日期写成 `2026-03-15 09:30`，另有一节写的是晚于今天的日期。 | `2026-03-15` 与 `2026-03-15 09:30` 两种写法都能识别。`PB-004` 报出晚于核对日的 `dataAsOf`，即日期填错了或引用了尚未产生的数据；解析不了的值单独报出，不会静默跳过。数据本身是否可靠，它不判断。 |
| 新鲜度那条报的是 `skipped`，是不是说明数据没问题？ | 不是。`PB-005` 出厂 `maxDays: 0`，即未配置，于是它报告自身进入 `skipped`，而不是自己编一个天数；配置 `maxDays`（例如 `maxDays: 90`）才会启用。命中只表示数据比你配置的窗口更旧，不表示数据不可用——引用旧数据有时是必要的，请在备注里说明原因。本条为 `info`。 |
| 有一节写了建议，但没写由谁来实施。 | `PB-006` 会报出这一节：`recommendation` 栏一旦填写，就要求填写 `implementer` 栏。只作现状分析、不提建议的节不会被报出，本条不会去打扰这类节。它只核对实施主体是否填写，不判断建议是否可行、主体是否恰当。 |
| 专报本身要声明什么？同一序号能在表里出现两次吗？ | `PB-007` 要求表头声明 `title` 与 `recipient` 两项，如果你的表式还记录密级或专题，把它们加进它的 `fields` 即可。`PB-008` 报出表内重复出现的 `sectionNo`，比较时忽略空白字符，因为序号重复会让评审意见无法准确指认要点。`PB-007` 只核对表头这两栏是否填写，不判断标题是否贴切、报送对象是否恰当；`PB-008` 只比对序号本身。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
|---|---|---|
| 《党政机关公文处理工作条例》 | 中办发〔2012〕14号（本次未取得条文） | PB-001, PB-002, PB-003, PB-004, PB-005, PB-006, PB-007, PB-008 |

**Boundary:** this plugin checks a **政策专报要素核对表** for what a brief can be held to mechanically — that
each section states its point, that a point has supporting evidence, that the evidence cites a source, that the
data date parses and is not in the future, that the figures are fresh enough under your window, that a
recommendation names who would implement it, that the brief names its title and recipient, and that section
numbers are unique. It does **not** decide whether a point is right, whether the evidence is sufficient,
whether a recommendation is feasible, whether the data is reliable, or whether the brief should be submitted.
**Those are judgements about research quality and decision value.**

> ### ⚠️ What this plugin can and cannot see
>
> **It reads a checklist, not the sources or the data.** So it can only check that a source is *cited* — never
> that the source exists or that the figures match it. `PB-003` says so in its own note, and the README's
> troubleshooting section repeats it: a fabricated citation will pass, because verifying sources is a different
> job.
>
> **《党政机关公文处理工作条例》(中办发〔2012〕14号) was obtained and read verbatim**, and
> `rules/evidence/clause-verification.md` records which articles were quoted — article 8(10) (a report serves to
> brief a superior body), article 19 (drafting: 「分析问题实事求是」「所提政策措施和办法切实可行」「观点鲜明」)
> and article 20(4), which lists 「引文等是否准确」 as a review point before issuance.
>
> **The rule `excerpt` fields still say "本次未取得", and every rule remains `warn` or `info`.** The regulation
> governs how a document is *drafted and issued*; this plugin checks whether a brief's *outline* records its
> points, evidence, sources and recommendations. Calling a blank column a `direct` breach of 「观点鲜明」 would
> dress a register gap up as a regulatory one — the over-claim this family exists to avoid. Half the rules rest
> on your own editorial conventions in any case.
>
> **The data-freshness window ships unset.** How stale is too stale is your editorial rule — a quick brief may
> demand last month's figures while an annual analysis legitimately cites the year's data — so `PB-005`'s
> `maxDays` starts at `0` and the rule reports itself in `skipped` rather than inventing a number. A finding
> there means "older than the window you set", never "unusable"; citing older data is sometimes right, and the
> fix is to say why in the remark.

## Compatibility

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-policy-brief-draft
dsh --profile <name> --dump-config | grep 'dsh-policy-brief-draft'
```

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

## License

[Apache License 2.0](LICENSE) © 2026 dsh-policy-brief-draft contributors.
