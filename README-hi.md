# dsh-policy-brief-draft — नीति ब्रीफ़ के तत्वों की पूर्णता और डेटा-ताज़गी की जाँच

`dsh-policy-brief-draft` नीति ब्रीफ़ (या शोध-प्रतिवेदन) की तत्व-चेकलिस्ट पढ़ता है — दस्तावेज़ का हेडर और प्रत्येक खंड की एक पंक्ति — और उसी चेकलिस्ट की पूर्णता तथा आंतरिक सुसंगति जाँचता है: क्या हर खंड अपना मुख्य बिंदु लिखता है, क्या बिंदु के पास आधार है, क्या आधार में स्रोत दर्ज है, क्या डेटा की अंतिम तिथि पढ़ी जा सकती है और जाँच की तिथि से बाद की नहीं है, क्या आँकड़े आपकी तय की गई ताज़गी विंडो के भीतर हैं, क्या सिफ़ारिश में लिखा है कि उसे कौन लागू करेगा, क्या हेडर ब्रीफ़ का शीर्षक और प्राप्तकर्ता घोषित करता है, और क्या कोई खंड संख्या दोहराई नहीं गई है।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| एक खंड में केवल सामग्री है, कोई निष्कर्ष नहीं — मुख्य बिंदु का कॉलम खाली है। | `PB-001` उस खंड को दर्ज करता है, क्योंकि प्रत्येक खंड में अपना मुख्य बिंदु लिखा होना अपेक्षित है। यह केवल देखता है कि `point` सेल भरा है, इसलिए यह नहीं आँकता कि बिंदु सही है या उसमें कुछ नया है। अनुच्छेद का संख्यांक न मिलने के कारण यह नियम `warn` तक सीमित है। |
| हमने आधार और स्रोत, दोनों कॉलम भर दिए हैं — जाँच असल में क्या जाँचती है? | केवल यह कि दोनों सेल भरे हैं। `PB-002` हर बिंदु के लिए `evidence` की अपेक्षा करता है और `PB-003` उसके साथ `sourceRef` की। `PB-002` यह नहीं आँकता कि आधार पर्याप्त है, सच है या उस बिंदु का समर्थन करता है; `PB-003` यह नहीं देख सकता कि स्रोत मौजूद है या आँकड़े उससे मेल खाते हैं, क्योंकि प्लगिन चेकलिस्ट पढ़ता है और स्रोत कभी नहीं, इसलिए गढ़ा हुआ स्रोत भी पास हो जाता है। |
| डेटा की अंतिम तिथि `2026-03-15 09:30` लिखी है, और एक खंड में आज के बाद की तिथि है। | `2026-03-15` और `2026-03-15 09:30`, दोनों रूप पढ़े जाते हैं। `PB-004` जाँच की तिथि के बाद की `dataAsOf` दर्ज करता है, यानी या तो तिथि गलत भरी गई है या खंड ऐसे आँकड़ों का हवाला दे रहा है जो अभी बने ही नहीं, और जो मान पढ़ा न जा सके वह अलग से दर्ज होता है, चुपचाप छोड़ा नहीं जाता। आँकड़े भरोसेमंद हैं या नहीं, यह नहीं आँकता। |
| ताज़गी वाला नियम `skipped` दर्ज कर रहा है। क्या इसका मतलब डेटा ठीक है? | नहीं। `PB-005` में `maxDays: 0` लिखा आता है, यानी कॉन्फ़िगर नहीं किया गया, इसलिए वह कोई संख्या गढ़ने के बजाय स्वयं को `skipped` में दर्ज करता है; चालू करने के लिए `maxDays` सेट करें (उदाहरण `maxDays: 90`)। तब किसी निष्कर्ष का अर्थ केवल इतना है कि डेटा आपकी तय की गई विंडो से पुराना है, यह कभी नहीं कि वह अनुपयोगी है, और पुराने आँकड़ों का हवाला देना कभी-कभी उचित होता है, इसलिए कारण टिप्पणी में लिखें। यह नियम `info` है। |
| एक खंड में सिफ़ारिश लिखी है, पर यह नहीं कि उसे कौन लागू करेगा। | `PB-006` उस खंड को दर्ज करता है: `recommendation` सेल भरा होने पर `implementer` सेल अपेक्षित हो जाता है। जो खंड केवल वर्तमान स्थिति का विश्लेषण करता है और कोई सिफ़ारिश नहीं देता, वह दर्ज नहीं होता, इसलिए यह नियम ऐसे खंडों को परेशान नहीं करता। यह देखता है कि कार्यान्वयनकर्ता लिखा है, यह नहीं कि सिफ़ारिश व्यावहारिक है या वह निकाय उपयुक्त है। |
| ब्रीफ़ को स्वयं क्या घोषित करना होता है, और एक ही खंड संख्या दो बार आ सकती है? | `PB-007` अपेक्षा करता है कि हेडर में `title` और `recipient` दोनों दर्ज हों, और यदि आपके फ़ॉर्म में गोपनीयता श्रेणी या विषय भी दर्ज होता है तो उन्हें उसके `fields` में जोड़ा जा सकता है। `PB-008` तालिका में दो बार आई `sectionNo` दर्ज करता है, तुलना करते समय खाली जगह छोड़ दी जाती है, क्योंकि दोहराई गई संख्या से किसी एक बिंदु की ओर ठीक से इशारा नहीं किया जा सकता। `PB-007` केवल यह देखता है कि हेडर की वे सेल भरी हैं, यह नहीं कि शीर्षक उपयुक्त है या प्राप्तकर्ता सही निकाय है, और `PB-008` केवल संख्याओं की तुलना करता है। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
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

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-policy-brief-draft
dsh --profile <name> --dump-config | grep 'dsh-policy-brief-draft'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/policy-brief-draft.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-policy-brief-draft
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-policy-brief-draft contributors.
