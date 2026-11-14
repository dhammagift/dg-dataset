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
# The glossary as dg-docs publishes it (synced daily from the owner's Google Sheet, checked there: only the four Nikāyas,
# Snp, Iti, Ud and the Vinaya): the one place the sheet is read (owner 2026-11-13: «максимально в одном месте»).
GLOSSARY = 'https://raw.githubusercontent.com/dhammagift/dg-docs/main/src/data/glossary.json'
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


def glossary(src, path):
    raw = urllib.request.urlopen(src, timeout=60).read().decode() if src.startswith('http') else open(src, encoding='utf-8').read()
    n = 0
    with open(path, 'w', encoding='utf-8') as f:
        for t in json.loads(raw)['terms']:
            c = t.get('canon') or {}
            link = c.get('link') or ''
            rec = {'pali': t['pali'], 'ru': t['ru'],
                   'defined_in': c.get('where', []), 'definition_url': ('https://dhamma.gift' + link if link.startswith('/') else link) or None,
                   'definition_pli': c.get('definition'), 'compounds_defined': c.get('compounds', []),
                   'pattern_hits': c.get('patterns', []), 'pattern_hits_broad': c.get('broader', []), 'vinaya_hits': c.get('vinaya', [])}
            if t.get('kind'):
                rec['definition_type'] = t['kind'].replace('special: ', '')   # «ariyassa vinaye»: the canon redefines the word
            if t.get('forms'):
                rec['forms'] = t['forms']   # inflected forms whose DPD headwords include the term (samudda: samuddo...)
            f.write(json.dumps(rec, ensure_ascii=False) + '\n'); n += 1
    return n


def to_markdown(md):
    # the docs' MDX as plain Markdown: components become links to the site
    md = re.sub(r'^---\n[\s\S]*?\n---\n', '', md)
    md = re.sub(r'^import .*\n', '', md, flags=re.M)
    md = re.sub(r'^<a id="[\w-]+"></a>\n+', '', md, flags=re.M)
    md = re.sub(r'<PageTools\s*/>\n?|<img [^>]*/>\n?', '', md)
    md = re.sub(r'<head>[\s\S]*?</head>\n*', '', md)  # the page's own schema.org markup, not text
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
    a.add_argument('--docs', required=True); a.add_argument('--glossary', default=GLOSSARY)
    o = a.parse_args()
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    t, s = parallel(o.offline_data, pali_roots(o.pali_root), os.path.join(HERE, 'data', 'parallel_pli_ru.jsonl'))
    g = glossary(o.glossary, os.path.join(HERE, 'data', 'glossary.jsonl'))
    texts(o.docs)
    print(f'parallel: {t} texts, {s} segments; glossary: {g} terms; texts: en, ru')


if __name__ == '__main__':
    main()
