# dsh-policy-brief-draft — Comprobación de los elementos de un informe de política

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-policy-brief-draft` lee una lista de verificación de elementos de un informe de política (o de un estudio) —la cabecera del documento más una fila por sección— y comprueba la completitud y la coherencia interna de esa lista: que cada sección exponga su punto, que un punto tenga evidencia de apoyo, que la evidencia cite una fuente, que la fecha de corte de los datos se pueda analizar y no sea posterior a la fecha de revisión, que los datos caigan dentro de la ventana de frescura que usted configure, que una recomendación nombre a quien la ejecutaría, que la cabecera declare el título y el destinatario del informe y que no se repita ningún número de sección.

## Cómo se ve la salida

![Terminal demo of dsh-policy-brief-draft: real output over its PB-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-policy-brief-draft/main/docs/assets/dsh-policy-brief-draft-demo.png)

Salida real de este plugin sobre su propio fixture de prueba `PB-001` — no es un montaje. El paquete de reglas no inventa citas, así que cada hallazgo nombra la cláusula aplicada y advierte que su texto no se obtuvo.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Una sección es todo material y ninguna conclusión: la columna del punto está vacía. | `PB-001` informa de esa sección, porque se espera que cada sección exponga su punto. Solo comprueba que la celda `point` esté rellena, así que no juzga si el punto es correcto ni si aporta algo nuevo. La regla está limitada a `warn` porque no se obtuvo el número del artículo. |
| Hemos rellenado la columna de la evidencia y la de la fuente. ¿Qué verifica realmente la comprobación? | Solo que ambas celdas estén rellenas. `PB-002` exige `evidence` para cada punto y `PB-003` exige `sourceRef` junto a ella. `PB-002` no juzga si la evidencia es suficiente, real o si sostiene el punto; `PB-003` no puede comprobar que la fuente exista ni que los datos coincidan con ella, porque el plugin lee la lista de verificación y nunca las fuentes, de modo que una cita inventada pasa. |
| La fecha de corte de los datos figura como `2026-03-15 09:30`, y una sección lleva una fecha posterior a hoy. | Se reconocen las dos formas, `2026-03-15` y `2026-03-15 09:30`. `PB-004` informa de un `dataAsOf` posterior a la fecha de revisión, es decir, o la fecha se rellenó mal o la sección cita datos que aún no existen, y un valor que no puede analizar se informa por separado en lugar de omitirse en silencio. No juzga si los datos son fiables. |
| La regla de frescura informa `skipped`. ¿Significa eso que los datos están bien? | No. `PB-005` viene con `maxDays: 0`, es decir, sin configurar, así que se informa a sí misma en `skipped` en lugar de inventar un número; configure `maxDays` (por ejemplo `maxDays: 90`) para activarla. Un hallazgo entonces solo significa que los datos son más antiguos que la ventana que usted fijó, nunca que sean inutilizables, y citar datos antiguos a veces es correcto, así que indique por qué en la observación. La regla es `info`. |
| Una sección formula una recomendación pero no dice quién la llevaría a cabo. | `PB-006` informa de esa sección: una vez rellenada la celda `recommendation`, se exige la celda `implementer`. Una sección que solo analiza la situación actual y no propone nada no se informa, así que la regla no molesta a las secciones de diagnóstico. Comprueba que se nombre al implementador, no si la recomendación es viable ni si ese órgano es el adecuado. |
| ¿Qué debe declarar el propio informe, y puede repetirse el mismo número de sección? | `PB-007` exige que la cabecera declare `title` y `recipient`, y pueden añadirse otros campos de cabecera, como la clasificación o el tema, a sus `fields` si su propio formulario los recoge. `PB-008` informa de un `sectionNo` que aparece dos veces en la tabla, ignorando los espacios, porque un número repetido impide señalar un punto sin ambigüedad. `PB-007` solo comprueba que esas celdas de cabecera estén rellenas, no que el título sea acertado o el destinatario el órgano correcto, y `PB-008` compara únicamente los números. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
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

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-policy-brief-draft
dsh --profile <name> --dump-config | grep 'dsh-policy-brief-draft'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/policy-brief-draft.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-policy-brief-draft
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-policy-brief-draft contributors.
