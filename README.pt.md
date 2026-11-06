<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-policy-brief-draft-hero-en-dark.webp">
  <img src="docs/assets/dsh-policy-brief-draft-hero-en-light.webp" width="100%" alt="Imagem do dsh-policy-brief-draft: no topo, a lista de verificação de elementos do relatório (cabeçalho title / recipient / draftedAt / classification; a linha 1 tem o ponto-chave vazio, a evidência preenchida e os dados de 2026-02-28); no meio, os três tetos por tipo de respaldo — direct PB-001/003/004/007 com teto error, derived-from-principle PB-002/006/008 com teto warn, institutional-configuration PB-005 com teto info (maxDays=0 significa skipped); embaixo, o cartão do achado PB-001 (linha 1, point vazio) e skipped 2">
</picture>

# dsh-policy-brief-draft

**Confere um relatório de política elemento por elemento —completude e atualidade dos dados— e devolve qual linha, qual coluna e o que falta, com a conclusão nas mãos do revisor.**

Um plugin de verificação para o DeepSeek Harness, feito para pesquisadores de políticas e gabinetes de redação: entra uma lista de verificação de elementos do relatório (o cabeçalho do documento mais uma linha por seção), e um pacote de regras com citações literais (PB-001…PB-008) lista apenas as divergências que o próprio material permite apontar —sem tocar no original, sem requisições de rede e sem chamar nenhum modelo.

[Instalar](#instalação-em-três-passos) · [Configuração](#configuração) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidade)
[![npm](https://img.shields.io/npm/v/dsh-policy-brief-draft?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-policy-brief-draft)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-policy-brief-draft/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-policy-brief-draft/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidade)

[![Stars](https://img.shields.io/github/stars/PerryLink/dsh-policy-brief-draft?style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-policy-brief-draft/stargazers)
[![npm downloads](https://img.shields.io/npm/dm/dsh-policy-brief-draft?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-policy-brief-draft)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-policy-brief-draft?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-policy-brief-draft?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-policy-brief-draft/badge)](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-policy-brief-draft)
[![DSH Market](https://img.shields.io/badge/DSH_Market-listed-4B67B4?style=flat-square&labelColor=2B3245)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-mirror-C71D23?style=flat-square&labelColor=2B3245&logo=gitee)](https://gitee.com/perrylink/dsh-policy-brief-draft)

```sh
dsh plugin --profile <name> add dsh-policy-brief-draft
```

</div>

<sub>Plugin da comunidade, sem afiliação com a DeepSeek. Repositório canônico: <https://github.com/PerryLink/dsh-policy-brief-draft> (o Gitee é um espelho).</sub>

## O que é

O `dsh-policy-brief-draft` lê uma lista de verificação de elementos de um relatório de política (ou de um estudo) —o cabeçalho do documento mais uma linha por seção— e verifica a completude e a coerência interna dessa lista: se cada seção expõe o seu ponto, se um ponto tem evidência de apoio, se a evidência cita uma fonte, se a data-limite dos dados é analisável e não é posterior à data de revisão, se os dados caem dentro da janela de atualidade que você configurar, se uma recomendação nomeia quem a executaria, se o cabeçalho declara o título do relatório e o seu destinatário e se não há número de seção repetido. Devolve a lista do que está incoerente, onde e o que corrigir; não modifica o original, não faz requisições de rede e não chama nenhum modelo. Não decide se um ponto está certo, se a evidência é suficiente, se uma recomendação é viável, se os dados são confiáveis ou se o relatório deve ser enviado: esses são juízos sobre a qualidade da pesquisa e o valor para a decisão, e ficam deliberadamente fora do seu escopo.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-policy-brief-draft-flow-v5-dark.svg">
  <img src="docs/assets/dsh-policy-brief-draft-flow-v5-light.svg" width="100%" alt="Estrutura do dsh-policy-brief-draft: à esquerda, a lista de verificação (cabeçalho title / recipient / draftedAt / classification e rows[] com point, evidence, sourceRef, dataAsOf, recommendation, implementer, sectionNo, section, risk, drafter); no centro, as 8 regras empilhadas sob os três tetos — direct com teto error, derived-from-principle com teto warn, institutional-configuration com teto info, e PB-005 em skipped enquanto maxDays=0; à direita, o relatório com summary (error 1 / warn 0 / info 0), issues[] com PB-001 apontando a linha 1 com point vazio e skipped[] com PB-005 e PB-006; o rodapé lembra que o original é somente leitura e que a conclusão fica com quem revisa">
</picture>

## Instalação em três passos

1. **Instalar**:

   ```sh
   dsh plugin --profile <name> add dsh-policy-brief-draft
   ```

   Você também pode procurar "Documents and Governance Suite" no WorkBuddy / Coze (esta verificação é uma das suas partes; disponibilidade conforme o catálogo).

2. **Configuração mínima** (os padrões já funcionam):

   ```yaml
   - insert:
       - id: dsh-policy-brief-draft
         name: dsh-policy-brief-draft
   ```

   Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts` e os padrões servem como vêm; os limites por regra ficam no pacote de regras sob `rules/`.

3. **Verificar que monta**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-policy-brief-draft'
   ```

   Depois execute o exemplo incluído uma vez (cerca de um minuto):

   ```sh
   node samples/quickstart/run.mjs
   ```

   ```text
   $ node samples/quickstart/run.mjs
   policy_brief_draft: 1 issue(s) — error 1, warn 0, info 0
   skipped: 2
   ```

   A entrada de exemplo está em `samples/quickstart/input/`, a saída esperada em `samples/quickstart/expected/result.json` e a captura da primeira execução em [`docs/assets/quickstart.png`](docs/assets/quickstart.png).

**Desinstalar**: `dsh plugin --profile <name> remove dsh-policy-brief-draft` (ou remova a linha do profile patch).

## Capacidades principais

O plugin registra a ferramenta `policy_brief_draft`: lê uma lista de verificação (cabeçalho mais uma linha por seção), aplica um pacote de regras versionado e devolve um relatório estruturado. O material é JSON ou YAML; toda verificação que não possa rodar aparece em `skipped` com o seu motivo.

- **O pacote de regras é dado** — as 8 verificações ficam em `rules/policy-brief-draft.yaml`, então trocar o conjunto de regras não exige tocar no código; o pacote é validado ao carregar, não é presumido correto.
- **A gravidade segue a evidência** — uma regra derivada de um princípio (`derived-from-principle`) tem teto `warn`, e uma cujo limite vem da configuração da instituição (`institutional-configuration`) tem teto `info`; um princípio ou uma configuração local nunca é rotulado `error` (há um teste que garante isso).
- **Uma lista vazia de achados não é "tudo certo"** — toda verificação que não possa rodar se registra em `skipped` com o seu motivo; `PB-005` vem com `maxDays: 0`, então se registra em `skipped` em vez de passar em silêncio.
- **Sem julgar** — o relatório enumera diferenças e nunca se pronuncia sobre conformidade, responsabilidade ou correção; um guardião de redação obriga todo relatório a trazer o aviso legal.
- **Sem citações inventadas** — cada regra carrega `document` / `number` / `clause` / `excerpt` / `kind` / `source`; `excerpt` precisa ser uma citação literal, e quando o texto não está em mãos o pacote diz isso em vez de apresentar uma paráfrase como citação.

```text
lista do relatório (JSON/YAML) ──policy_brief_draft──▶ pacote PB-001…PB-008 ──▶ relatório (issues + skipped)
          ▲                                                                              │
          └───────────────────── o original é somente leitura, nunca é alterado ─────────┘
```

### Regras em resumo

| Regra | O que verifica | Gravidade | Tipo de base |
|---|---|---|---|
| `PB-001` | cada seção expõe o seu ponto | error | artigo literal |
| `PB-002` | cada ponto tem evidência de apoio | warn | princípio derivado |
| `PB-003` | a evidência cita uma fonte | error | artigo literal |
| `PB-004` | a data-limite é analisável e não está no futuro | error | artigo literal |
| `PB-005` | os dados são suficientemente recentes segundo a sua janela (desligada por padrão) | info | configuração institucional |
| `PB-006` | uma recomendação nomeia o seu executor | warn | princípio derivado |
| `PB-007` | o relatório declara o seu título e destinatário | warn | artigo literal |
| `PB-008` | os números de seção são únicos na tabela | warn | princípio derivado |

### Exemplos

São os pontos de entrada reais do plugin; instale uma vez e chame um. A saída abaixo é a execução real do plugin contra o seu próprio fixture de teste `PB-001`, não uma ilustração.

**Saída detalhada** — ferramenta `policy_brief_draft`, entrada:

```json
{"title":"某某领域投资形势分析专报","rows":[{"序号":"1","章节":"一、现状","核心观点":"","支撑依据":"全国固定资产投资统计月报（2026 年 2 月）显示本领域投资同比增长 3.1%"}]}
```

Saída:

```json
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
```

*Observado em `dsh-policy-brief-draft/tests/fixtures/PB-001/PB-001-unsafe.json (cases.json expects 1×PB-001); executed parseMaterial+runCheck, checkedAt=2026-10-06T00:00:00.000Z`*

### O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Uma seção é só material e nenhuma conclusão: a coluna do ponto está vazia. | `PB-001` reporta essa seção, porque se espera que cada seção exponha o seu ponto. Verifica apenas que a célula `point` está preenchida, por isso não julga se o ponto está certo nem se acrescenta algo novo. É um `error`: o artigo 19(3) exige um "ponto de vista claro", e esse artigo foi lido literalmente em 2026-10-13. |
| Preenchemos a coluna da evidência e a da fonte. O que a verificação confirma, afinal? | Apenas que ambas as células estão preenchidas. `PB-002` exige `evidence` para cada ponto e `PB-003` exige `sourceRef` ao lado dela. `PB-003` é um `error`, porque o artigo 20(4) inclui a exatidão de "citações e afins" entre os pontos de revisão antes da emissão; `PB-002` continua a ser um `warn`, porque nenhum artigo exige uma citação por ponto. `PB-002` não julga se a evidência é suficiente, real ou se sustenta o ponto; `PB-003` não consegue verificar se a fonte existe nem se os dados coincidem com ela, porque o plugin lê a lista de verificação e nunca as fontes, pelo que uma citação inventada passa. |
| A data-limite dos dados está escrita como `2026-03-15 09:30`, e uma seção tem uma data posterior a hoje. | As duas formas, `2026-03-15` e `2026-03-15 09:30`, são reconhecidas. `PB-004` reporta um `dataAsOf` posterior à data de revisão, ou seja, ou a data foi mal preenchida ou a seção cita dados que ainda não existem, e um valor que não consegue analisar é reportado à parte em vez de ser omitido em silêncio. É um `error`: o artigo 19(2) exige que a análise seja factual e o artigo 20(4) exige que a "hora" seja exata, e uma data-limite posterior à data de revisão não pode ser verdadeira. Não julga se os dados são confiáveis. |
| A regra de atualidade reporta `skipped`. Isso significa que os dados estão bem? | Não. `PB-005` vem com `maxDays: 0`, ou seja, sem configurar, por isso se reporta em `skipped` em vez de inventar um número; configure `maxDays` (por exemplo `maxDays: 90`) para a ativar. Um achado então significa apenas que os dados são mais antigos do que a janela que você definiu, nunca que sejam inutilizáveis, e citar dados antigos às vezes é correto, por isso diga porquê na observação. A regra é `info`: a sua janela de dias vem do seu critério editorial e o regulamento não fixa qualquer número de dias. |
| Uma seção apresenta uma recomendação mas não diz quem a executaria. | `PB-006` reporta essa seção: uma vez preenchida a célula `recommendation`, a célula `implementer` passa a ser exigida. Uma seção que apenas analisa a situação atual e não recomenda nada não é reportada, por isso a regra não incomoda as seções de diagnóstico. Verifica que o executor é nomeado, não se a recomendação é viável nem se esse órgão é o adequado. |
| O que deve o próprio relatório declarar, e pode o mesmo número de seção repetir-se? | `PB-007` exige que o cabeçalho declare `title` e `recipient`, e outros campos do cabeçalho, como a classificação ou o tema, podem ser acrescentados aos seus `fields` se o seu próprio formulário os registrar. `PB-008` reporta um `sectionNo` que aparece duas vezes na tabela, ignorando espaços, porque um número repetido impede apontar um ponto sem ambiguidade. `PB-007` verifica apenas que essas células do cabeçalho estão preenchidas, não que o título seja acertado ou o destinatário o órgão certo, e `PB-008` compara apenas os números. |

## Configuração

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`. Há exatamente cinco chaves de configuração, na tabela abaixo; os parâmetros por regra vêm em seguida.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/policy-brief-draft.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta (milissegundos) |

Parâmetros por regra que vale conhecer:

- `PB-005` `maxDays` — a sua janela de atualidade em dias. `0` significa que a regra não roda e aparece em `skipped`.
- `PB-006` `conditionField` / `requiredFields` — o que dispara a exigência do executor; por padrão, a coluna de recomendação. Seções que apenas analisam não precisam dele.
- `PB-007` `fields` — os campos de cabeçalho que precisam estar presentes; por padrão, título e destinatário. Acrescente `classification` se os seus relatórios tiverem marca de sigilo.

## FAQ

<details>
<summary>O meu material será alterado ou enviado?</summary>

Não. A ferramenta apenas lê o texto JSON/YAML que você entrega e **nunca altera o arquivo original**; o plugin é ESM puro, não tem código nativo, **não faz requisições de rede e não chama nenhum modelo** (ver "Compatibilidade"), portanto o material não sai da sua máquina.

</details>

<details>
<summary>Sem janela de atualidade configurada, ele passa em silêncio?</summary>

Não. `PB-005` vem com `maxDays` indefinido (`0`), então a regra se registra em `skipped` com o seu motivo: uma lista vazia de achados não pode ser lida como "não falta nada". Configure `maxDays` e ela começa a rodar; depois disso, um achado significa que os dados são mais antigos do que a janela que você definiu, nunca que sejam inutilizáveis.

</details>

<details>
<summary>O plugin instala, mas a ferramenta não aparece. E agora?</summary>

Confirme que `main` aponta para `lib/index.mjs` e que `pnpm run build` o gerou; um `main` errado faz o carregador omitir a entrada em silêncio.

</details>

<details>
<summary>A instalação é recusada por incompatibilidade. E agora?</summary>

A faixa de peers cobre `0.1.x` e `0.2.x`; se o seu runtime estiver fora dela, conceda uma isenção explícita: `dsh plugin --profile <name> allow-version dsh-policy-brief-draft@0.1.0 --dsh-version <runtime> --accept-risk`. O runtime aplica a compatibilidade de peers na instalação.

</details>

<details>
<summary>Dá para tratar um relatório inteiro, ou um diretório inteiro, numa só execução?</summary>

A ferramenta funciona nos modos `native` e `ptc`; para um conjunto grande de documentos prefira `ptc`, assim o custo do esquema é pago uma vez. Toda a aritmética é de hora local sobre as cadeias fornecidas, sem conversão de fuso horário.

</details>

## Normas que segue

| Documento | Número | Regras que o citam |
|---|---|---|
| Regulamento sobre o Tratamento de Documentos Oficiais dos Órgãos do Partido e do Governo | Zhongbanfa [2012] n.º 14 (texto integral obtido; o trecho literal já foi incorporado ao `excerpt` de cada regra) | PB-001, PB-002, PB-003, PB-004, PB-005, PB-006, PB-007, PB-008 |

**Limite:** este plugin verifica uma **lista de verificação de elementos de um relatório de política** pelo que essa lista pode exigir de forma mecânica: que cada seção exponha o seu ponto, que um ponto tenha evidência de apoio, que a evidência cite uma fonte, que a data-limite seja analisável e não esteja no futuro, que os dados sejam suficientemente recentes segundo a sua janela, que uma recomendação nomeie quem a executaria, que o relatório nomeie o seu título e destinatário, e que os números de seção sejam únicos. **Não** decide se um ponto está certo, se a evidência é suficiente, se uma recomendação é viável, se os dados são confiáveis ou se o relatório deve ser enviado. **São juízos sobre a qualidade da pesquisa e o valor para a decisão.**

> ### ⚠️ O que este plugin pode e não pode ver
>
> **Ele lê uma lista de verificação, não as fontes nem os dados.** Por isso só pode verificar que uma fonte está *citada* —nunca que exista ou que os dados coincidam com ela. `PB-003` diz isso na sua própria nota, e a seção de solução de problemas deste README repete: uma citação inventada passará, porque verificar fontes é outro trabalho.
>
> **O regulamento (Zhongbanfa [2012] n.º 14) foi obtido e lido literalmente**, e `rules/evidence/clause-verification.md` registra quais artigos foram citados: o artigo 8(10) (o relatório serve para informar um órgão superior), o artigo 19 (redação: "a análise deve ser factual", "as políticas e medidas propostas devem ser viáveis", "o ponto de vista deve ser claro") e o artigo 20(4), que inclui a exatidão de "citações e afins" entre os pontos de revisão antes da emissão.
>
> **O texto dos artigos já está no pacote e as gravidades foram novamente derivadas dele (2026-10-13).** O regulamento rege como um documento é *redigido e emitido*; este plugin verifica se o *esquema* de um relatório registra os seus pontos, evidência, fontes e recomendações. São duas coisas diferentes, por isso a regra foi aplicada artigo por artigo e não em bloco:
>
> - **Elevadas a `error`** onde um artigo enuncia o requisito que a verificação procura: `PB-001` (19(3), ponto de vista claro), `PB-003` (20(4) inclui a exatidão das citações como ponto de revisão antes da emissão) e `PB-004` (19(2), análise factual, com 20(4), hora exata: uma data-limite posterior à data de revisão não pode ser verdadeira).
> - **Mantidas em `warn` embora o texto tenha sido obtido**, porque o artigo trata de outra coisa: `PB-002` (nenhum artigo exige uma citação por ponto), `PB-006` (nenhum exige nomear um executor), `PB-008` (nenhum exige números de seção únicos) e **`PB-007`**, cujo artigo 9 rege os dezoito elementos de formato de um documento formal e não duas colunas de um esquema de trabalho: chamar `direct` a uma célula de cabeçalho vazia como violação do artigo 9 seria disfarçar uma lacuna do registro de violação normativa.
> - **Continuam em `info`**: `PB-005`, cuja janela é o seu critério editorial e não consta do regulamento.
>
> Assim, **3 regras são `error`, 4 são `warn` e 1 é `info`**: a divisão é o ponto, não uma transação: obter um texto só autoriza uma citação `direct` quando o texto diz realmente o que se verifica. Veja `rules/evidence/clause-verification-gongwen-tiaoli-direct.md`, que também registra em que discorda da análise anterior de `clause-verification.md`.
>
> **A janela de atualidade dos dados vem indefinida.** Quão antigo é demasiado antigo é o seu critério editorial —um relatório rápido pode exigir os números do mês passado, enquanto uma análise anual cita legitimamente os dados do ano—, então o `maxDays` de `PB-005` parte de `0` e a regra se registra em `skipped` em vez de inventar um número. Um achado ali significa "mais antigo do que a janela que você definiu", nunca "inutilizável"; citar dados mais antigos às vezes é correto, e a solução é explicar por quê na observação.

## Formato do material

A ferramenta aceita JSON ou YAML:

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

Os nomes das colunas são comparados sem distinguir maiúsculas de minúsculas e ignorando espaços, sublinhados e hífenes; os nomes de coluna da própria lista são preservados, de modo que um achado nomeia a coluna que leu. As datas podem ser `2026-02-28` ou `2026-02-28 09:30`. Os campos são opcionais na camada de leitura e validados pelo motor de verificação, então uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Fontes das regras

Os dados das regras ficam em `rules/policy-brief-draft.yaml`, separados do código. Cada regra traz o documento, o seu número, a cláusula na numeração própria da fonte, um `excerpt` literal, uma URL de origem e um tipo de base (`kind`). O carregador impõe que um `excerpt` seja uma citação real de pelo menos oito caracteres, e que uma verificação baseada apenas num princípio derivado (`derived-from-principle`, gravidade com teto `warn`) ou na configuração institucional (`institutional-configuration`, teto `info`) nunca seja rotulada `error`. Um pacote que exagera a sua base falha ao carregar em vez de produzir um relatório de aparência segura.

Os artigos citados vêm do Regulamento sobre o Tratamento de Documentos Oficiais dos Órgãos do Partido e do Governo (Zhongbanfa [2012] n.º 14): artigo 8(10), artigo 9 (incluindo (7) título e (8) destinatário principal), artigo 19(2)(3) e artigo 20(4). Os limites confirmados durante a verificação e as conclusões deliberadamente não extraídas estão em `rules/evidence/`, em particular `clause-verification-gongwen-tiaoli-direct.md` e `clause-verification.md`.

## Compatibilidade

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-rc.2`. `engines.dsh` é declarado como `>=0.2.1-0 <0.3.0` e o host o aplica desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native` e `ptc`; para uma lista longa use `ptc` |

## Solução de problemas

- **`PB-005` nunca roda.** A janela de atualidade está vazia (`maxDays: 0`). Quão antigo é demasiado antigo é o seu critério editorial e o plugin não o inventa; configure `maxDays` (por exemplo `90`) para ativá-la.
- **`PB-003` aceita uma fonte que eu sei ser inventada.** Ele não consegue verificar isso: verifica que uma fonte está *citada*, não que exista ou diga o que o relatório afirma.
- **`PB-005` dispara com dados que citei de propósito.** Dados antigos às vezes são os certos. Amplie `maxDays` ou registre o motivo na observação: o achado é sobre a janela, não sobre os dados.
- **`PB-006` não dispara numa seção de análise.** É deliberado: o executor só é exigido quando se formula realmente uma recomendação.
- **`PB-004` dispara com uma data no futuro.** Ou a data-limite ou a data de redação está errada; um relatório não pode apoiar-se em números que ainda não existem.
- **O plugin instala, mas a ferramenta não aparece.** Confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou; um `main` errado faz o carregador omitir a entrada em silêncio.
- **`dsh plugin add` recusa o pacote por incompatibilidade.** A faixa de peers cobre `0.1.x` e `0.2.x`; se o seu runtime estiver fora dela, conceda uma isenção explícita: `dsh plugin --profile <name> allow-version dsh-policy-brief-draft@0.1.0 --dsh-version <runtime> --accept-risk`
- **Uma regra não executou.** Leia o arranjo `skipped`; ele indica o id da regra e o motivo.
- **`check` informa `manifest-peers` como falha.** O verificador estático compara com uma faixa de peers codificada anterior à linha 0.2. O runtime aplica a compatibilidade de peers na instalação, então a faixa declarada é a correta; é um problema conhecido do `dsh-plugin-dev`.
- **Os horários parecem deslocados.** Toda a aritmética é de hora local sobre as cadeias de entrada, sem conversão de fuso horário.

## Ecossistema e qualidade

- [Espelho no Gitee](https://gitee.com/perrylink/dsh-policy-brief-draft) (espelho sincronizado; o GitHub é canônico)
- [Página do plugin no dshfind](https://dshfind.com/plugins/PerryLink/dsh-policy-brief-draft) (instalações e ranking)
- [Relatório OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-policy-brief-draft) (movido por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (no catálogo)
- [Base de conhecimento do ecossistema · escolher um verificador por material](https://perrylink.github.io/zh/checkers/choose/) (índice completo da família: verificadores + plugins gerais)

## Desenvolvimento

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest; cada regra tem fixtures conforme/violador emparelhados em tests/fixtures/<RULE>/
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes   # coerência dos README em cinco idiomas
node ../scripts/sync-shared.mjs dsh-policy-brief-draft   # atualizar src/shared a partir de ../_shared
```

O plugin é só dados: `src/model.ts` declara a forma da tabela, o kit compartilhado fornece o leitor e o motor de verificação, e o pacote de regras declara cada verificação. O pacote de regras é dado, não código: substituir `rules/*.yaml` troca o conjunto de regras sem tocar no TypeScript, e o pacote é validado ao carregar em vez de presumido correto. As imagens do README são geradas por programa por [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow) e podem ser executadas de novo; este plugin não tem UI, então o hero é um banner de 1440×576 gerado por programa (zh/en × claro/escuro) e o diagrama de estrutura `docs/assets/dsh-policy-brief-draft-flow-v5-light.svg` é um SVG escrito à mão (claro e escuro, apenas tokens da superfície de comandos).

Topics: `dsh`, `dsh-plugin`, `deepseek-harness`, `cordis`, `policy`, `brief`, `draft`

## Família e agradecimentos

Este projeto faz parte da família de plugins do DeepSeek Harness mantida pela [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Se ele for útil, **uma estrela ajuda a próxima pessoa a encontrá-lo** — nada é liberado por ela.

- [@PerryLink](https://github.com/PerryLink) — criador e mantenedor: a ferramenta `policy_brief_draft`, o pacote de regras com citações literais e o seu registro de verificação de cláusulas, e a documentação em cinco idiomas.

<details>
<summary>Expandir todos os plugins</summary>

| Plugin | Status |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 CONGELADO — ver o README do repo |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 APOSENTADO (repo arquivado) |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 CONGELADO — ver o README do repo |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 APOSENTADO (repo arquivado) |

</details>

## Licença

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-policy-brief-draft contributors

<p align="center"><sub>Apache-2.0 · Plugin da comunidade, sem afiliação com a DeepSeek.</sub></p>
