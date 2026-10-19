# dsh-policy-brief-draft — Policy brief element completeness and data-freshness check

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-policy-brief-draft` reads one policy-brief outline — the document header plus one row per section — and checks that outline's own completeness and internal consistency: that each section states its point, that a point carries supporting evidence, that the evidence cites a source, that the data cutoff parses and is not later than the review date, that the figures fall inside the data-freshness window you configure, that a recommendation names who would implement it, that the header declares the brief's title and its recipient, and that no section number is repeated.

## Install

```sh
dsh plugin --profile <name> add dsh-policy-brief-draft
dsh --profile <name> --dump-config | grep 'dsh-policy-brief-draft'
```

## What it looks like

![Terminal demo of dsh-policy-brief-draft: real output over its PB-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-policy-brief-draft/main/docs/assets/dsh-policy-brief-draft-hero.png)

![Animated terminal demo of dsh-policy-brief-draft](https://raw.githubusercontent.com/PerryLink/dsh-policy-brief-draft/main/docs/assets/dsh-policy-brief-draft-demo.gif)

Real output from this plugin over its own `PB-001` test fixture — not a mock-up. The rule pack ships no invented quotations: every finding names the article it applied, and every `excerpt` is now a verbatim quotation from a document this repository has read.

## What it answers

| You ask | What it answers |
|---|---|
| One section is all material and no conclusion: the point column is empty. | `PB-001` reports that section, because every section is expected to state its point. It checks only that the `point` cell is filled, so it does not judge whether the point is right or whether it says anything new. It is an `error`: article 19(3) requires 「观点鲜明」, and that article was read verbatim on 2026-10-13. |
| We filled in the evidence column and the source column. What does the check actually verify? | Only that both cells are filled. `PB-002` requires `evidence` for every point and `PB-003` requires `sourceRef` beside it. `PB-003` is an `error`, because article 20(4) lists 「引文等是否准确」 among the review points before a document is issued; `PB-002` stays a `warn`, because no article requires one citation per point. `PB-002` does not judge whether the evidence is sufficient, real, or actually supports the point; `PB-003` cannot check that the source exists or that the figures match it, because the plugin reads the checklist and never the sources, so a fabricated citation passes. |
| The data cutoff reads `2026-03-15 09:30`, and one section carries a date later than today. | Both `2026-03-15` and `2026-03-15 09:30` are read. `PB-004` reports a `dataAsOf` that falls after the review date, meaning either the date was filled in wrongly or the section cites data that does not exist yet, and a value it cannot parse is reported on its own instead of being silently skipped. It is an `error`: article 19(2) requires 「分析问题实事求是」 and article 20(4) requires 「时间」 to be accurate, and a cutoff after the review date cannot be true. It does not judge whether the data itself is reliable. |
| The freshness rule reports `skipped`. Does that mean the data is fine? | No. `PB-005` ships with `maxDays: 0`, which means unconfigured, so it reports itself in `skipped` rather than inventing a number; set `maxDays` (for example `maxDays: 90`) to switch it on. A hit then means only that the data is older than the window you set, never that it is unusable, and citing older data is sometimes right, so say why in the remark. The rule is `info`. |
| A section makes a recommendation but never says who would carry it out. | `PB-006` reports that section: once the `recommendation` cell is filled, the `implementer` cell is required. A section that only analyses the current situation and makes no recommendation is not reported, so the rule does not nag status-only sections. It checks that the implementer is named, not whether the recommendation is feasible or that body the right one. |
| What must the brief itself declare, and may the same section number appear twice? | `PB-007` requires the header to declare both `title` and `recipient`, and further header fields such as classification or topic can be added to its `fields` if your own form records them. `PB-008` reports a `sectionNo` that appears twice in the table, ignoring whitespace, because a repeated number stops a reviewer from pointing at one point unambiguously. `PB-007` checks only that those header cells are filled, not that the title is apt or the recipient the right body, and `PB-008` compares the numbers alone. |

## Standards it follows

| Document | Number | Cited by rules |
|---|---|---|
| 《党政机关公文处理工作条例》 | 中办发〔2012〕14号（全文已取得，逐字回填至各条 `excerpt`） | PB-001, PB-002, PB-003, PB-004, PB-005, PB-006, PB-007, PB-008 |

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
> **The clause text is now in the pack, and the severities were re-derived from it (2026-10-13).** The
> regulation governs how a document is *drafted and issued*; this plugin checks whether a brief's *outline*
> records its points, evidence, sources and recommendations. Those are two different things, so the rule was
> applied article by article rather than in bulk:
>
> - **Raised to `error`** where an article states the requirement the check looks for: `PB-001` (19(3)
>   「观点鲜明」), `PB-003` (20(4) lists 「引文等是否准确」 as a pre-issuance review point) and `PB-004`
>   (19(2) 「分析问题实事求是」 with 20(4) 「时间」 — a cutoff after the review date cannot be true).
> - **Left at `warn` even though the text was obtained**, because the article is about something else:
>   `PB-002` (no article requires one citation per point), `PB-006` (none requires naming an implementer),
>   `PB-008` (none requires unique section numbers), and **`PB-007`**, whose article 9 governs the eighteen
>   format elements of a formal document rather than two columns of a working outline — calling a blank header
>   cell a `direct` breach of article 9 would dress a register gap up as a regulatory one.
> - **Still `info`**: `PB-005`, whose window is your editorial convention and is not in the regulation at all.
>
> So **3 rules are `error`, 4 are `warn` and 1 is `info`** — the split is the point, not a compromise:
> obtaining a text licenses a `direct` citation only where the text actually says the thing being checked.
> See `rules/evidence/clause-verification-gongwen-tiaoli-direct.md`, which also records where it disagrees with
> the earlier analysis in `clause-verification.md`.
>
> **The data-freshness window ships unset.** How stale is too stale is your editorial rule — a quick brief may
> demand last month's figures while an annual analysis legitimately cites the year's data — so `PB-005`'s
> `maxDays` starts at `0` and the rule reports itself in `skipped` rather than inventing a number. A finding
> there means "older than the window you set", never "unusable"; citing older data is sometimes right, and the
> fix is to say why in the remark.

## Compatibility

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-rc.2`. `engines.dsh` is declared as `>=0.2.1-0 <0.3.0` and is enforced by the host since 0.2.1 |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native` and `ptc`; for a long brief use `ptc` |

## What it does

Registers the `policy_brief_draft` tool. It reads one brief outline — the document header plus one row per
section — applies a versioned rule pack, and returns a report.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `PB-001` | each section states its point | error | direct |
| `PB-002` | each point has supporting evidence | warn | principle |
| `PB-003` | the evidence cites a source | error | direct |
| `PB-004` | the data date parses and is not in the future | error | direct |
| `PB-005` | the data is fresh enough under your window (off by default) | info | local |
| `PB-006` | a recommendation names its implementer | warn | principle |
| `PB-007` | the brief names its title and recipient | warn | direct |
| `PB-008` | section numbers are unique | warn | principle |
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

## PerryLink DSH Plugin Family

This project is part of the DeepSeek Harness plugin family from [PerryLink](https://github.com/PerryLink). The roster stays collapsed below so every README keeps a short first screen; expand it to see every row and its status.

<details>
<summary>Expand all plugins</summary>

| Plugin | Status |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** |  |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** |  |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** |  |
| **[dsh-demurrage-ledger](https://github.com/PerryLink/dsh-demurrage-ledger)** |  |
| **[dsh-doublecheck](https://github.com/PerryLink/dsh-doublecheck)** |  |
| **[dsh-drill-script-check](https://github.com/PerryLink/dsh-drill-script-check)** |  |
| **[dsh-eia-guide-check](https://github.com/PerryLink/dsh-eia-guide-check)** |  |
| **[dsh-emergency-plan](https://github.com/PerryLink/dsh-emergency-plan)** |  |
| **[dsh-essay-rubric-check](https://github.com/PerryLink/dsh-essay-rubric-check)** |  |
| **[dsh-evidence-check](https://github.com/PerryLink/dsh-evidence-check)** |  |
| **[dsh-export-ctl-check](https://github.com/PerryLink/dsh-export-ctl-check)** |  |
| **[dsh-fast](https://github.com/PerryLink/dsh-fast)** |  |
| **[dsh-fmea-table-check](https://github.com/PerryLink/dsh-fmea-table-check)** |  |
| **[dsh-forecast-penalty](https://github.com/PerryLink/dsh-forecast-penalty)** |  |
| **[dsh-fund-research](https://github.com/PerryLink/dsh-fund-research)** |  |
| **[dsh-github](https://github.com/PerryLink/dsh-github)** |  |
| **[dsh-gongwen-flow-check](https://github.com/PerryLink/dsh-gongwen-flow-check)** |  |
| **[dsh-gongwen-word-check](https://github.com/PerryLink/dsh-gongwen-word-check)** |  |
| **[dsh-guard-plan-qc](https://github.com/PerryLink/dsh-guard-plan-qc)** |  |
| **[dsh-hazchem-check](https://github.com/PerryLink/dsh-hazchem-check)** |  |
| **[dsh-hazplan-check](https://github.com/PerryLink/dsh-hazplan-check)** |  |
| **[dsh-hidden-risk-map](https://github.com/PerryLink/dsh-hidden-risk-map)** |  |
| **[dsh-hs-classify](https://github.com/PerryLink/dsh-hs-classify)** |  |
| **[dsh-icd-rule-check](https://github.com/PerryLink/dsh-icd-rule-check)** |  |
| **[dsh-industry-research](https://github.com/PerryLink/dsh-industry-research)** |  |
| **[dsh-lawcite-adapter](https://github.com/PerryLink/dsh-lawcite-adapter)** |  |
| **[dsh-laya](https://github.com/PerryLink/dsh-laya)** |  |
| **[dsh-lc-doc-check](https://github.com/PerryLink/dsh-lc-doc-check)** |  |
| **[dsh-learning-gap-check](https://github.com/PerryLink/dsh-learning-gap-check)** |  |
| **[dsh-library](https://github.com/PerryLink/dsh-library)** |  |
| **[dsh-local-ai](https://github.com/PerryLink/dsh-local-ai)** |  |
| **[dsh-lsp-actions](https://github.com/PerryLink/dsh-lsp-actions)** |  |
| **[dsh-mask](https://github.com/PerryLink/dsh-mask)** |  |
| **[dsh-mcp-panel](https://github.com/PerryLink/dsh-mcp-panel)** |  |
| **[dsh-medrec-qc](https://github.com/PerryLink/dsh-medrec-qc)** |  |
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** |  |
| **[dsh-nsfc-form-check](https://github.com/PerryLink/dsh-nsfc-form-check)** |  |
| **[dsh-nurse-record-check](https://github.com/PerryLink/dsh-nurse-record-check)** |  |
| **[dsh-observe](https://github.com/PerryLink/dsh-observe)** |  |
| **[dsh-origin-rvc-check](https://github.com/PerryLink/dsh-origin-rvc-check)** |  |
| **[dsh-ota-review-check](https://github.com/PerryLink/dsh-ota-review-check)** |  |
| **[dsh-output-styles](https://github.com/PerryLink/dsh-output-styles)** |  |
| **[dsh-paper-doc-adapter](https://github.com/PerryLink/dsh-paper-doc-adapter)** |  |
| **[dsh-permission-rules](https://github.com/PerryLink/dsh-permission-rules)** |  |
| **[dsh-permit-report-check](https://github.com/PerryLink/dsh-permit-report-check)** |  |
| **[dsh-pipeline-check](https://github.com/PerryLink/dsh-pipeline-check)** |  |
| **[dsh-pleading-draft](https://github.com/PerryLink/dsh-pleading-draft)** |  |
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** |  |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** |  |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** |  |
| **[dsh-policy-brief-draft](https://github.com/PerryLink/dsh-policy-brief-draft)** |  |
| **[dsh-power-loss-split](https://github.com/PerryLink/dsh-power-loss-split)** |  |
| **[dsh-power-ticket-check](https://github.com/PerryLink/dsh-power-ticket-check)** |  |
| **[dsh-ppap-check](https://github.com/PerryLink/dsh-ppap-check)** |  |
| **[dsh-protest-deadline](https://github.com/PerryLink/dsh-protest-deadline)** |  |
| **[dsh-railway-window](https://github.com/PerryLink/dsh-railway-window)** |  |
| **[dsh-repair-order-qc](https://github.com/PerryLink/dsh-repair-order-qc)** |  |
| **[dsh-research-report](https://github.com/PerryLink/dsh-research-report)** |  |
| **[dsh-review-reply-check](https://github.com/PerryLink/dsh-review-reply-check)** |  |
| **[dsh-rulefile-check](https://github.com/PerryLink/dsh-rulefile-check)** |  |
| **[dsh-safety-brief-check](https://github.com/PerryLink/dsh-safety-brief-check)** |  |
| **[dsh-score](https://github.com/PerryLink/dsh-score)** |  |
| **[dsh-session-sync](https://github.com/PerryLink/dsh-session-sync)** |  |
| **[dsh-site-log-check](https://github.com/PerryLink/dsh-site-log-check)** |  |
| **[dsh-skill-pack-security](https://github.com/PerryLink/dsh-skill-pack-security)** |  |
| **[dsh-soe-decision-check](https://github.com/PerryLink/dsh-soe-decision-check)** |  |
| **[dsh-soilwater-check](https://github.com/PerryLink/dsh-soilwater-check)** |  |
| **[dsh-sop-sync-check](https://github.com/PerryLink/dsh-sop-sync-check)** |  |
| **[dsh-spc-gbt-adapter](https://github.com/PerryLink/dsh-spc-gbt-adapter)** |  |
| **[dsh-talk](https://github.com/PerryLink/dsh-talk)** |  |
| **[dsh-tender-extract](https://github.com/PerryLink/dsh-tender-extract)** |  |
| **[dsh-tender-matrix](https://github.com/PerryLink/dsh-tender-matrix)** |  |
| **[dsh-test-drive](https://github.com/PerryLink/dsh-test-drive)** |  |
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** |  |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 FROZEN — see the repo README |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 FROZEN — see the repo README |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 FROZEN — see the repo README |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 FROZEN — see the repo README |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 FROZEN — see the repo README |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRED — see the repo README |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRED — see the repo README |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRED — see the repo README |

</details>## License

[Apache License 2.0](LICENSE) © 2026 dsh-policy-brief-draft contributors.
