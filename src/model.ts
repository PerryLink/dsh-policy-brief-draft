/**
 * dsh-policy-brief-draft — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'policy_brief_draft'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  sectionNo: ['序号', '要点序号', '编号', 'sectionNo'],
  section: ['章节', '对策章节', '部分', 'section'],
  point: ['核心观点', '观点', '结论', 'point'],
  evidence: ['支撑依据', '依据', '论据', 'evidence'],
  sourceRef: ['出处', '数据来源', '引用出处', 'sourceRef'],
  dataAsOf: ['数据截止日期', '截止日期', '数据日期', 'dataAsOf'],
  recommendation: ['建议事项', '对策建议', '建议', 'recommendation'],
  implementer: ['建议实施主体', '实施主体', '责任单位', 'implementer'],
  risk: ['风险提示', '风险', '不确定性', 'risk'],
  drafter: ['撰稿人', '起草人', '撰写人', 'drafter'],
  note: ['备注', '说明', 'note', 'remark'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'sections', '要点'],
  columns: COLUMNS,
  header: {
  title: ['title', '专报标题', '文件标题'],
  topic: ['topic', '专题', '主题'],
  recipient: ['recipient', '报送对象', '呈报对象'],
  draftedAt: ['draftedAt', '成文日期', '撰写日期'],
  classification: ['classification', '密级', '信息等级'],
  checkedAt: ['checkedAt', '核对日期'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '核心观点',
  'point',
  '支撑依据',
  'evidence',
  '建议事项',
  'recommendation',
  '章节',
  'section',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
