#!/usr/bin/env python3
"""Builds the Dhamma.Gift dataset from its public sources (see README.md).

    python3 build.py --offline-data DIR --pali-root DIR --docs DIR [--sheet CSV_URL_OR_FILE]

  --offline-data  a checkout of github.com/dhammagift/offline-data (dhammagift/translation/ru is read)
  --pali-root     sc_bilara_data/root/pli/ms of github.com/suttacentral/sc-data
  --docs          a checkout of github.com/dhammagift/dg-docs (the Dhamma pages, en and ru)
  --sheet         the glossary sheet as CSV (default: its public export)
"""
import argparse, csv, glob, io, json, os, re, urllib.request

SITE = 'https://dhamma.gift'
SHEET = 'https://docs.google.com/spreadsheets/d/1s7n7ogJhdtSIweVO9aad63_k7lWrZgyPRUFg34AobMg/export?format=csv&gid=0'
HERE = os.path.dirname(os.path.abspath(__file__))


def pali_roots(root):
    out = {}
    for p in glob.glob(os.path.join(root, '**', '*_root-pli-ms.json'), recursive=True):
        out[os.path.basename(p).split('_root-')[0]] = json.load(open(p, encoding='utf-8'))
    return out


def parallel(offline_data, roots, path):
    # only the project's own translation ("ru-o"): "+edited+o" files are someone else's translation edited by the project
    texts = segs = 0
    with open(path, 'w', encoding='utf-8') as f:
        for p in sorted(glob.glob(os.path.join(offline_data, 'dhammagift', 'translation', 'ru', '**', '*_translation-ru-o.json'), recursive=True)):
            sid = os.path.basename(p).split('_translation-')[0]
            pli, ru = roots.get(sid), json.load(open(p, encoding='utf-8'))
            if not pli:
                print(f'warning: no Pali root for {sid}'); continue
            rows = [(k, pli[k].strip(), ru[k].strip()) for k in pli if (ru.get(k) or '').strip() and pli[k].strip()]
            for k, pt, rt in rows:
                f.write(json.dumps({'id': k, 'text': sid, 'pli': pt, 'ru': rt, 'url': f'{SITE}/{k}?lang=ru'}, ensure_ascii=False) + '\n')
            texts += bool(rows); segs += len(rows)
    return texts, segs


def ids(cell):
    # "mn9, sn12.2 … (+15)" -> ["mn9", "sn12.2"]; the sheet truncates long lists for reading
    return [x for x in re.split(r'[,\s]+', re.sub(r'….*$', '', cell or '')) if re.match(r'^[a-z]', x)]


def glossary(sheet, path):
    raw = urllib.request.urlopen(sheet, timeout=60).read().decode() if sheet.startswith('http') else open(sheet, encoding='utf-8').read()
    n = 0
    with open(path, 'w', encoding='utf-8') as f:
        for r in list(csv.reader(io.StringIO(raw)))[2:]:
            r += [''] * (15 - len(r))
            pali = r[1].strip()
            if not pali or not re.search(r'[a-zāīūṁṇñṭḍḷṅ]', pali, re.I) or pali.startswith(('Составные', 'Compounds')):
                continue
            rec = {'pali': pali, 'ru': r[2].strip(),
                   'defined_in': ids(r[8]), 'definition_url': r[9].strip() or None, 'definition_pli': r[10].strip() or None,
                   'compounds_defined': [x.strip() for x in r[11].split(',') if x.strip()],
                   'pattern_hits': ids(r[12]), 'pattern_hits_broad': ids(r[13]), 'vinaya_hits': ids(r[14])}
            f.write(json.dumps(rec, ensure_ascii=False) + '\n'); n += 1
    return n


def to_markdown(md):
    # the docs' MDX as plain Markdown: components become links to the site
    md = re.sub(r'^---\n[\s\S]*?\n---\n', '', md)
    md = re.sub(r'^import .*\n', '', md, flags=re.M)
    md = re.sub(r'^<a id="[\w-]+"></a>\n+', '', md, flags=re.M)
    md = re.sub(r'<PageTools\s*/>\n?|<img [^>]*/>\n?', '', md)
    url = lambda to: SITE + re.sub(r'\?$', '', re.sub(r'\?&', '?', re.sub(r'[?&]hide=id\b', '', to)))
    items = []
    def browser(m):
        items.extend(re.findall(r"label: '((?:[^'\\]|\\.)*)', desc: '((?:[^'\\]|\\.)*)', src: '([^']*)'", m.group(1)))
        return '\n'.join(f"- [{l}]({url(s)}): {d}".replace("\\'", "'") for l, d, s in items)
    md = re.sub(r'<SuttaBrowser items=\{\[([\s\S]*?)\]\}\s*/>', browser, md)
    # <SuttaLink index={n}>text</SuttaLink>, or self-closing with the component's default text
    md = re.sub(r'<SuttaLink index=\{(\d+)\}\s*(?:/>|>([^<]*)</SuttaLink>)',
                lambda m: f'[{m.group(2) or "Читать →"}]({url(items[int(m.group(1))][2])})' if int(m.group(1)) < len(items) else '', md)
    md = re.sub(r'<SiteLink to="([^"]*)">([\s\S]*?)</SiteLink>', lambda m: f'[{m.group(2)}]({url(m.group(1))})', md)
    left = re.search(r'<[A-Z][A-Za-z]*[\s/>]', md)
    if left:
        raise SystemExit(f'unconverted component: {md[left.start():left.start() + 60]}')
    return re.sub(r'\n{3,}', '\n\n', md).strip() + '\n'


def texts(docs):
    pages = {'principles-by-suttas': 'sutta', 'rationale': 'rationale'}
    src = {'en': os.path.join(docs, 'docs', 'dhamma'), 'ru': os.path.join(docs, 'i18n', 'ru', 'docusaurus-plugin-content-docs', 'current', 'dhamma')}
    for lang, d in src.items():
        os.makedirs(os.path.join(HERE, 'texts', lang), exist_ok=True)
        for name, f in pages.items():
            md = open(os.path.join(d, f + '.md'), encoding='utf-8').read()
            md = re.sub(r'\]\(#([\w-]+)\)', lambda m: f']({SITE}{"/ru" if lang == "ru" else ""}/docs/{f}{"" if lang == "ru" else "/"}#{m.group(1)})', md)
            md = re.sub(r'\]\(/(principles|rationale|sutta)\)', lambda m: f']({SITE}{"/ru" if lang == "ru" else ""}/docs/{m.group(1)})', md)
            open(os.path.join(HERE, 'texts', lang, name + '.md'), 'w', encoding='utf-8').write(to_markdown(md))


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--offline-data', required=True); a.add_argument('--pali-root', required=True)
    a.add_argument('--docs', required=True); a.add_argument('--sheet', default=SHEET)
    o = a.parse_args()
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    t, s = parallel(o.offline_data, pali_roots(o.pali_root), os.path.join(HERE, 'data', 'parallel_pli_ru.jsonl'))
    g = glossary(o.sheet, os.path.join(HERE, 'data', 'glossary.jsonl'))
    texts(o.docs)
    print(f'parallel: {t} texts, {s} segments; glossary: {g} terms; texts: en, ru')


if __name__ == '__main__':
    main()
