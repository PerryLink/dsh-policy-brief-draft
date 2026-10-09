# dsh-policy-brief-draft — Verificação dos elementos de um relatório de políticas

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-policy-brief-draft` lê uma lista de verificação dos elementos de um relatório de políticas (ou de um estudo) —o cabeçalho do documento mais uma linha por secção— e verifica a completude e a coerência interna dessa lista: se cada secção expõe o seu ponto, se um ponto tem evidência de apoio, se a evidência cita uma fonte, se a data-limite dos dados é analisável e não é posterior à data de revisão, se os dados caem dentro da janela de frescura que configurar, se uma recomendação nomeia quem a executaria, se o cabeçalho declara o título e o destinatário do relatório e se não há números de secção repetidos.

## Como é a saída

![Terminal demo of dsh-policy-brief-draft: real output over its PB-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-policy-brief-draft/main/docs/assets/dsh-policy-brief-draft-demo.png)

Saída real deste plugin sobre o seu próprio fixture de teste `PB-001` — não é uma simulação. O pacote de regras não inventa citações, por isso cada achado nomeia a cláusula aplicada e avisa que o seu texto não foi obtido.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Uma secção é só material e nenhuma conclusão: a coluna do ponto está vazia. | `PB-001` reporta essa secção, porque se espera que cada secção exponha o seu ponto. Verifica apenas que a célula `point` está preenchida, por isso não julga se o ponto está certo nem se acrescenta algo novo. A regra está limitada a `warn` porque o número do artigo não foi obtido. |
| Preenchemos a coluna da evidência e a da fonte. O que é que a verificação confirma, afinal? | Apenas que ambas as células estão preenchidas. `PB-002` exige `evidence` para cada ponto e `PB-003` exige `sourceRef` ao lado dela. `PB-002` não julga se a evidência é suficiente, real ou se sustenta o ponto; `PB-003` não consegue verificar se a fonte existe nem se os dados coincidem com ela, porque o plugin lê a lista de verificação e nunca as fontes, pelo que uma citação inventada passa. |
| A data-limite dos dados está escrita como `2026-03-15 09:30`, e uma secção tem uma data posterior a hoje. | As duas formas, `2026-03-15` e `2026-03-15 09:30`, são reconhecidas. `PB-004` reporta um `dataAsOf` posterior à data de revisão, ou seja, ou a data foi mal preenchida ou a secção cita dados que ainda não existem, e um valor que não consegue analisar é reportado à parte em vez de ser omitido em silêncio. Não julga se os dados são fiáveis. |
| A regra de frescura reporta `skipped`. Isso significa que os dados estão bem? | Não. `PB-005` vem com `maxDays: 0`, ou seja, por configurar, por isso reporta-se em `skipped` em vez de inventar um número; configure `maxDays` (por exemplo `maxDays: 90`) para a ativar. Um achado significa então apenas que os dados são mais antigos do que a janela que definiu, nunca que sejam inutilizáveis, e citar dados antigos é por vezes correto, por isso diga porquê na observação. A regra é `info`. |
| Uma secção apresenta uma recomendação mas não diz quem a executaria. | `PB-006` reporta essa secção: uma vez preenchida a célula `recommendation`, a célula `implementer` passa a ser exigida. Uma secção que apenas analisa a situação atual e não recomenda nada não é reportada, por isso a regra não incomoda as secções de diagnóstico. Verifica que o implementador é nomeado, não se a recomendação é viável nem se esse órgão é o adequado. |
| O que deve o próprio relatório declarar, e pode o mesmo número de secção repetir-se? | `PB-007` exige que o cabeçalho declare `title` e `recipient`, e outros campos do cabeçalho, como a classificação ou o tema, podem ser acrescentados aos seus `fields` se o seu próprio formulário os registar. `PB-008` reporta um `sectionNo` que aparece duas vezes na tabela, ignorando espaços, porque um número repetido impede apontar um ponto sem ambiguidade. `PB-007` verifica apenas que essas células do cabeçalho estão preenchidas, não que o título seja acertado ou o destinatário o órgão certo, e `PB-008` compara apenas os números. |

## Normas que segue

| Documento | Número | Regras que o citam |
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

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-policy-brief-draft
dsh --profile <name> --dump-config | grep 'dsh-policy-brief-draft'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/policy-brief-draft.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-policy-brief-draft
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-policy-brief-draft contributors.
