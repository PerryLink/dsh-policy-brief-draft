# dsh-policy-brief-draft — Policy brief element completeness and data-freshness check

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-policy-brief-draft` reads one policy-brief outline — the document header plus one row per section — and checks that outline's own completeness and internal consistency: that each section states its point, that a point carries supporting evidence, that the evidence cites a source, that the data cutoff parses and is not later than the review date, that the figures fall inside the data-freshness window you configure, that a recommendation names who would implement it, that the header declares the brief's title and its recipient, and that no section number is repeated.

## What it looks like

![Terminal demo of dsh-policy-brief-draft: real output over its PB-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-policy-brief-draft/main/docs/assets/dsh-policy-brief-draft-demo.png)

Real output from this plugin over its own `PB-001` test fixture — not a mock-up. The rule pack ships no invented quotations, so a finding names both the clause it applied and the fact that the clause text was not obtained.

## What it answers

| You ask | What it answers |
|---|---|
| One section is all material and no conclusion: the point column is empty. | `PB-001` reports that section, because every section is expected to state its point. It checks only that the `point` cell is filled, so it does not judge whether the point is right or whether it says anything new. The rule is capped at `warn` because the clause number was not obtained. |
| We filled in the evidence column and the source column. What does the check actually verify? | Only that both cells are filled. `PB-002` requires `evidence` for every point and `PB-003` requires `sourceRef` beside it. `PB-002` does not judge whether the evidence is sufficient, real, or actually supports the point; `PB-003` cannot check that the source exists or that the figures match it, because the plugin reads the checklist and never the sources, so a fabricated citation passes. |
| The data cutoff reads `2026-03-15 09:30`, and one section carries a date later than today. | Both `2026-03-15` and `2026-03-15 09:30` are read. `PB-004` reports a `dataAsOf` that falls after the review date, meaning either the date was filled in wrongly or the section cites data that does not exist yet, and a value it cannot parse is reported on its own instead of being silently skipped. It does not judge whether the data itself is reliable. |
| The freshness rule reports `skipped`. Does that mean the data is fine? | No. `PB-005` ships with `maxDays: 0`, which means unconfigured, so it reports itself in `skipped` rather than inventing a number; set `maxDays` (for example `maxDays: 90`) to switch it on. A hit then means only that the data is older than the window you set, never that it is unusable, and citing older data is sometimes right, so say why in the remark. The rule is `info`. |
| A section makes a recommendation but never says who would carry it out. | `PB-006` reports that section: once the `recommendation` cell is filled, the `implementer` cell is required. A section that only analyses the current situation and makes no recommendation is not reported, so the rule does not nag status-only sections. It checks that the implementer is named, not whether the recommendation is feasible or that body the right one. |
| What must the brief itself declare, and may the same section number appear twice? | `PB-007` requires the header to declare both `title` and `recipient`, and further header fields such as classification or topic can be added to its `fields` if your own form records them. `PB-008` reports a `sectionNo` that appears twice in the table, ignoring whitespace, because a repeated number stops a reviewer from pointing at one point unambiguously. `PB-007` checks only that those header cells are filled, not that the title is apt or the recipient the right body, and `PB-008` compares the numbers alone. |

## Standards it follows

| Document | Number | Cited by rules |
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

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-alpha.1`. `engines.dsh` is deliberately not declared: it has no reader and cannot reject a host |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native`, `ptc` and `both`; for a long brief use `ptc` |

## What it does

Registers the `policy_brief_draft` tool. It reads one brief outline — the document header plus one row per
section — applies a versioned rule pack, and returns a report.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `PB-001` | each section states its point | warn | principle |
| `PB-002` | each point has supporting evidence | warn | principle |
| `PB-003` | the evidence cites a source | warn | principle |
| `PB-004` | the data date parses and is not in the future | warn | principle |
| `PB-005` | the data is fresh enough under your window (off by default) | info | local |
| `PB-006` | a recommendation names its implementer | warn | principle |
| `PB-007` | the brief names its title and recipient | warn | principle |
| `PB-008` | section numbers are unique | warn | principle |
## Install

```sh
dsh plugin --profile <name> add dsh-policy-brief-draft
dsh --profile <name> --dump-config | grep 'dsh-policy-brief-draft'
```

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/policy-brief-draft.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `PB-005` `maxDays` — your freshness window in days. `0` means the rule does not run.
- `PB-006` `conditionField` / `requiredFields` — what triggers the implementer requirement; the recommendation
  column by default. Sections that analyse without recommending are not asked for one.
- `PB-007` `fields` — the header fields that must be present; title and recipient by default. Add
  `classification` if your briefs carry a security marking.

## Material format

The tool accepts JSON or YAML:

```yaml
title: 某某领域投资形势分析专报
topic: 投资形势
recipient: 某某部门
draftedAt: 2026-03-12
classification: 内部
rows:
  - { 序号: '1', 章节: 一、现状,
      核心观点: 本领域投资增速连续三个季度回落，结构性分化明显,
      支撑依据: 全国固定资产投资统计月报（2026 年 2 月）显示本领域投资同比增长 3.1%,
      出处: 国家统计局月度数据，2026 年 3 月发布, 数据截止日期: 2026-02-28,
      风险提示: 月度数据存在季节因素，需结合同比口径判断 }
```

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the outline's own
column names are kept, so a finding names the column it read. Dates may be `2026-02-28` or
`2026-02-28 09:30`.

## Rule sources

Rule data lives in `rules/policy-brief-draft.yaml`. The pack's header states the citation gap in full, and each
rule's `note` repeats the part that matters for that rule. The load-time guard that normally enforces "an
excerpt must be a real quotation of at least eight characters" cannot tell a quotation from a description —
so this pack leans on the header, the per-rule notes and a test that asserts every `excerpt` admits the gap.

## Troubleshooting

- **`PB-003` passes a source I know is invented.** It cannot check that: it verifies a source is *cited*, not
  that it exists or says what the brief claims.
- **`PB-005` reports itself as skipped.** No freshness window is set. How stale is too stale is your editorial
  rule, and the plugin will not invent one.
- **`PB-005` fires on data I deliberately cited.** Older data is sometimes the right data. Either widen
  `maxDays` or record the reason in the remark — the finding is about the window, not about the data.
- **`PB-006` does not fire on an analysis section.** That is deliberate: the implementer is required only when
  a recommendation is actually made.
- **`PB-004` fires on a date in the future.** Either the data date or the drafting date is wrong; a brief
  cannot rest on figures that do not exist yet.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and
  that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if
  your runtime sits outside it, grant an explicit exemption:
  `dsh plugin --profile <name> allow-version dsh-policy-brief-draft@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer
  range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the
  declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table-plugin suite plus paired fixtures
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
node ../scripts/sync-shared.mjs dsh-policy-brief-draft   # refresh src/shared from ../_shared
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and
the check engine, and the rule pack declares every check.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-policy-brief-draft contributors.
