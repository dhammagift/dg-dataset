---
license: cc-by-4.0
language:
  - pi
  - ru
  - en
pretty_name: "Dhamma.Gift: the Suttas read by the Suttas' own definitions"
tags:
  - pali
  - pali-canon
  - sutta
  - vinaya
  - buddhism
  - theravada
  - parallel-corpus
  - glossary
task_categories:
  - translation
size_categories:
  - 10K<n<100K
configs:
  - config_name: parallel_pli_ru
    data_files: data/parallel_pli_ru.jsonl
  - config_name: glossary
    data_files: data/glossary.jsonl
---

# Dhamma.Gift: the Suttas read by the Suttas' own definitions

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23491473.svg)](https://doi.org/10.5281/zenodo.23491473)

The Suttas define their own key terms. The question *"Katamañca, bhikkhave, X?"* ("And what, monks, is X?") is answered, and the answer closes with *"idaṁ vuccati X"* ("this is called X"). The texts can also be checked against one another. The Buddha's criterion for any teaching is to check it against the Suttas and the Vinaya, not the authority of whoever reports it ([AN 4.180](https://dhamma.gift/an4.180:2.6?lang=en)).

This dataset is the [Dhamma.Gift](https://dhamma.gift) project's reading of the Pali Canon (Sutta and Vinaya) on that basis. It holds three things, and every record links to the Pali segment it rests on:

| File | What it is |
|---|---|
| `data/parallel_pli_ru.jsonl` | The project's own Russian translation ("o"), segment by segment with the Pali root text (Mahāsaṅgīti edition, SuttaCentral Bilara). |
| `data/glossary.jsonl` | Pali terms with the project's Russian rendering, and the places where the Suttas define each term. |
| `texts/{en,ru}/` | *Principles by Suttas*: the criteria the Suttas give for checking a teaching. *Rationale*: where common renderings of terms such as *dukkha*, *sukha*, *taṇhā*, *upādāna*, *anta*, *kāma* and *kamma* do not fit the Suttas' own definitions, passage by passage. |

## Examples

What the text says, with its place:

- *dukkha* is defined as bodily pain, and mental pain is a separate term, *domanassa*: *"Yaṁ kho, bhikkhave, kāyikaṁ dukkhaṁ kāyikaṁ asātaṁ … idaṁ vuccati, bhikkhave, dukkhaṁ"* ([DN 22](https://dhamma.gift/dn22:18.18?lang=en), [MN 141](https://dhamma.gift/mn141:16.1?lang=en)).
- *sukha*, as a faculty, is bodily pleasant feeling, and the mental one is *somanassa* ([SN 48.36](https://dhamma.gift/sn48.36?lang=en)).
- Where real thirst is described (heat, desert, exhaustion), the texts use *tasinā* / *tasita*, not *taṇhā* ([SN 12.68](https://dhamma.gift/sn12.68?lang=en)). *Taṇhā* goes together with delight and passion and "delights here and there" (*nandīrāgasahagatā tatratatrābhinandinī*, [SN 56.11](https://dhamma.gift/sn56.11?lang=en)).

## Records

`parallel_pli_ru.jsonl`, one line per segment:

```json
{"id": "an10.113:1.3", "text": "an10.113", "pli": "Adhammañca viditvā anatthañca, …", "ru": "Не-дхамму узнав и бесцельное, …", "url": "https://dhamma.gift/an10.113:1.3?lang=ru"}
```

`glossary.jsonl`, one line per term:

| Field | Meaning |
|---|---|
| `pali`, `ru` | The term and the project's Russian rendering |
| `defined_in` | Texts where the term is defined by the formula *"Katamā…? … idaṁ vuccati …"* |
| `definition_url`, `definition_pli` | The first such definition, its link and its Pali |
| `compounds_defined` | Compounds of the term that have a definition of their own |
| `pattern_hits` | Texts matched by the definition patterns *Katam…? / … vuccati* (candidates, reviewed over time) |
| `pattern_hits_broad`, `vinaya_hits` | Wider patterns (*Ko…*, *ayaṁ…*, *Kiñ…*, *ariyassa vinaye*), and the Vinaya's Vibhaṅgas |

The glossary is filled in gradually. Terms without a definition yet have empty lists.

## Scope

- **Covered:** the four Nikāyas, the Udāna, Itivuttaka and Sutta Nipāta, and the Vinaya's Vibhaṅgas.
- **Translation:** the Russian translation covers a part of the canon, 844 texts so far, and grows.
- **Not included:** the Abhidhamma, and translations by other authors.

## Cite

Dhamma.Gift. *Dhamma.Gift: the Suttas read by the Suttas' own definitions* (dataset). Zenodo. https://doi.org/10.5281/zenodo.23491473 (all versions).

## Sources and license

- **The project's own content** is licensed CC BY 4.0: commercial use is allowed, with attribution to Dhamma.Gift and a link to https://dhamma.gift. This covers the Russian translation, the glossary renderings and the texts.
- **The Pali root text** is from [SuttaCentral](https://suttacentral.net) (CC0).

Built by `build.py` from public sources:
- [dhammagift/offline-data](https://github.com/dhammagift/offline-data): the translations;
- [suttacentral/sc-data](https://github.com/suttacentral/sc-data): the Pali;
- [dhammagift/dg-docs](https://github.com/dhammagift/dg-docs): the texts;
- the project's glossary sheet.

The same material is readable on the site: [Principles by Suttas](https://dhamma.gift/docs/sutta/), [Rationale](https://dhamma.gift/docs/rationale/), [Hatthipada](https://dhamma.gift/hatthipada/?lang=en) (the four noble truths, every word opened by the Suttas' definitions), [llms-full.txt](https://dhamma.gift/llms-full.txt).

---

**По-русски.** Собственный русский перевод проекта Dhamma.Gift («o»), сегмент к сегменту с пали. Глоссарий терминов с местами, где сутты сами их определяют. «Принципы по суттам» и «Обоснование». Каждая запись ссылается на сегмент на dhamma.gift. Лицензия CC BY 4.0: можно использовать, в том числе коммерчески, со ссылкой на Dhamma.Gift.
