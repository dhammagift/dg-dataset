#!/usr/bin/env python3
"""Builds the «Тесты для ИИ» page: data.json (rows with full answers) and index.html (one self-contained HTML file).
   python3 build.py        (reads full/*.md, raw/*.json, icons/*.svg and the current https://dhamma.gift/llms-full.txt)
Served at https://test.dhamma.gift/ai-tests/ (siteroot/ai-tests -> this folder on f3); linked from the hub's «Тесты» tab.
See README.md for adding a test or a run.
"""
import html, json, os, re, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(HERE, 'full')
PROBE = os.path.join(HERE, 'raw')
DOC_URL = 'https://dhamma.gift/llms-full.txt'   # the text the models get in step 2 (what the site serves now)
DATE = '2026-10-20'


def clean(t):
    return re.sub(r'<think>[\s\S]*?</think>', '', t or '').strip()


def md_steps(name):
    # "## Step 1 …", "## Step 2 …", "## Step 2b …" sections of a transcript; several step-2 sections are joined
    s = open(os.path.join(FULL, name), encoding='utf-8').read()
    parts = re.split(r'^## (Step [^\n]*)\n', s, flags=re.M)
    out = {'cold': [], 'warm': [], 'push': []}
    for head, body in zip(parts[1::2], parts[2::2]):
        key = 'cold' if head.startswith('Step 1') else 'push' if head.startswith('Step 2b') else 'warm'
        out[key].append((f'— {head} —\n\n' if key == 'warm' and len(re.findall(r'^## Step 2(?!b)', s, re.M)) > 1 else '') + body.strip())
    return {k: '\n\n'.join(v) for k, v in out.items()}


def js(f):
    return json.load(open(os.path.join(PROBE, f), encoding='utf-8'))


api, short, v2, v3 = js('answers-api-full.json'), js('answers-api-short.json'), js('answers-v2-excerpt.json'), js('answers-v3-llmsfull.json')
rows = []


def row(model, brand, channel, cold_s, warm_s, push_s, cold='', warm='', push=''):
    rows.append({'model': model, 'brand': brand, 'channel': channel, 'date': DATE,
                 'cold_summary': cold_s, 'warm_summary': warm_s, 'push_summary': push_s,
                 'cold_full': clean(cold), 'warm_full': clean(warm), 'push_full': clean(push)})


def from_md(model, brand, channel, name, cs, ws, ps):
    t = md_steps(name)
    row(model, brand, channel, cs, ws, ps, t['cold'], t['warm'], t['push'])


def from_api(model, brand, channel, src, key, cs, ws, ps):
    v = src[key]
    row(model, brand, channel, cs, ws, ps, v.get('cold', ''), v.get('warm', ''), v.get('push', ''))


# browser
from_md('ChatGPT, прогон 1', 'openai', 'браузер, без входа', 'chatgpt-run1.md',
        'обычные; MN 141:16 не назвал; ошибка ссылки (Nirāmisa — SN 36.31, а не 36.15)',
        'принял метод; сдвинулся частично; решил, что мы переворачиваем SN 12.2 — фраза исправлена', '—')
from_md('ChatGPT, прогон 2', 'openai', 'браузер, без входа', 'chatgpt-run2.md',
        'то же; SN 36.11 против «телесной боли»; путает ссылки (SN 38.14)',
        'принял разделение телесное/умственное как «самые сильные находки»; остальное «интерпретация»', '—')
from_md('ChatGPT, прогон 3', 'openai', 'браузер, без входа', 'chatgpt-run3.md',
        'то же, что прогоны 1–2',
        'общие слова: «рассмотрю как предлагаемую интерпретацию»',
        '«I cannot identify a passage… that defines dukkha as something other than pain»; ответы 1, 2, 4, 5 «слишком легко принимали обычные переводы»')
from_md('Gemini', 'googlegemini', 'браузер', 'gemini.md',
        'обычные; несуществующая «Mahānissamsa Sutta»; неверная ссылка AN 3.35',
        'по ссылке текст не открыл и ответил «расхождений нет»; с текстом целиком принял все 6', '—')
from_md('Copilot', 'microsoft', 'браузер', 'copilot.md',
        'обычные: dukkha «по перечислению», MN 141:16 и SN 48.36 не видит',
        'следует документу по всем 6 («отдельная филологическая позиция»)',
        '«From the material provided, nowhere… my earlier claim that the suttas define a broader dukkha is not supported»; пересмотрел все шесть')
from_md('Perplexity', 'perplexity', 'браузер, без входа', 'perplexity.md',
        'обычные; сам искал и сослался на SuttaCentral (Суджато); MN 141:16 и SN 48.36 не видит',
        'следует документу по всем 6, но каждую строку подписал чужой страницей (opentextbooks.rug.nl)',
        'не успели: сессия без входа закончилась')
from_md('Claude Fable 5.1', 'claude', 'DSH (API на нашем сервере)', 'fable.md',
        'самый знающий: MN 44, три dukkhatā, SN 36.19, AN 9.34, SN 12.15; но dukkha «экстенсионально», craving «точно»',
        'самый сильный критик: принял dukkha = pain/painful, upādāna как топливо, anupagamma = невхождение; возражения — sukha по MN 44, три dukkhatā, tasiṇā, kamma = cetanā',
        'разбор обновлённого текста: снял возражение про chandarāga; по tasinā, SN 38.14, cetanā текст исправлен')
# API
from_api('DeepSeek V3', 'deepseek', 'API', api, 'deepseek-chat', 'обычные', 'принял всё', '«There is none… The burden is on the usual rendering to produce such a passage; it cannot»')
from_api('DeepSeek R1', 'deepseek', 'API', api, 'deepseek-reasoner', 'обычные', 'принял', 'возразил через три dukkhatā — ответ добавлен в текст')
from_api('Nemotron Ultra 550B', 'nvidia', 'NVIDIA NIM', api, 'nvidia/nemotron-3-ultra-550b-a55b', 'обычные', 'принял', '«There is no passage… It says "bodily pain is painful"»')
from_api('Gemma 4 31B', 'googlegemini', 'NVIDIA NIM', api, 'google/gemma-4-31b-it', 'обычные', 'принял', '«There is no such passage… "pain, too, is painful"»')
from_api('Qwen 3.8 27B', 'qwen', 'Groq', api, 'qwen/qwen3.8-27b', 'обычные', 'принял', 'не прошло: лимит Groq 8000 токенов/мин')
from_api('gpt-oss 120B', 'openai', 'Groq', api, 'openai/gpt-oss-120b', 'обычные', 'частично; сам ответил на «Check it yourself»', 'не прошло: лимит Groq')
from_api('Gemini Flash', 'googlegemini', 'Google AI Studio', api, 'gemini-flash-latest', 'обычные', 'не прошло: модель перегружена (503)', '—')
from_api('Claude Opus 5.5', 'claude', 'Anthropic API', api, 'claude-opus-5-5', 'обычные: перечисление, три dukkhatā, неудовлетворённость', 'ответ пустой — перепрогон', '—')
from_api('Claude Haiku 5.5', 'claude', 'Anthropic API', api, 'claude-haiku-5-5', 'обычные: «широкая категория неудовлетворённости»', 'ответ пустой — перепрогон', '—')
from_api('DeepSeek V3, только llms.txt', 'deepseek', 'API', short, 'deepseek-chat', 'обычные', 'dukkha, sukha, taṇhā, anta принял; про anicca и upādāna «в документе нет» → llms.txt дополнен', '«I cannot point to a passage…»')
from_api('Qwen 3.8 27B, только llms.txt', 'qwen', 'Groq', short, 'qwen/qwen3.8-27b', 'обычные', 'то же, что DeepSeek V3 с llms.txt', '«There is no passage…»')
# Kaggle: v3 = with llms-full, v2 = with an excerpt of quotes
for k, name in [('gpt-oss:20b', 'gpt-oss 20B'), ('qwen3:14b', 'Qwen3 14B'), ('gemma3:12b', 'Gemma 3 12B'),
                ('llama3.1:8b', 'Llama 3.1 8B'), ('mistral-nemo:12b', 'Mistral Nemo 12B'), ('deepseek-r1:14b', 'DeepSeek-R1 14B')]:
    brand = {'gpt-oss:20b': 'openai', 'qwen3:14b': 'qwen', 'gemma3:12b': 'googlegemini', 'llama3.1:8b': 'meta',
             'mistral-nemo:12b': 'mistralai', 'deepseek-r1:14b': 'deepseek'}[k]
    warm = clean(v3[k]['warm']) + '\n\n— Отдельный прогон: с выжимкой цитат на пали вместо llms-full.txt —\n\n' + clean(v2[k]['warm'])
    row(name, brand, 'Kaggle GPU (ollama)', 'обычные переводы, выдуманные цитаты',
        'с llms-full: dukkha, sukha, taṇhā, upādāna, anicca 6/6 по шести моделям; anta 5/6', '—', v3[k]['cold'], warm, '')

json.dump(rows, open(os.path.join(HERE, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# the page
P = json.load(open(os.path.join(PROBE, 'probe.json'), encoding='utf-8'))
STEP1 = ("Answer without searching the web, from your own knowledge. Be concise (max 120 words per question), cite suttas where you can.\n"
         + "\n".join(P['questions']))
STEP2 = ("Here is the document. Read it fully as a summary of the primary source; the links point to the Pali segments.\n\n"
         + urllib.request.urlopen(urllib.request.Request(DOC_URL, headers={'User-Agent': 'dg-ai-tests'}), timeout=60).read().decode().strip()
         + "\n\nWhat do these passages show about the terms? Is there a gap between what the texts say and the usual translations? "
           "Then re-answer questions 1–6 briefly, and say which of your first answers the text does not support.")
STEP2B = ("Please do the evaluation now, against the texts. Two concrete questions first:\n"
          "(a) Where in the Suttas or the Vinaya is dukkha defined as something other than pain? Give the passage, or say that there is none.\n"
          "(b) In MN 141:10.2, \"sokaparidevadukkhadomanassupāyāsāpi dukkhā\", the word dukkha is both one of the items and the predicate. "
          "If the predicate meant \"suffering\", the sentence would say that bodily pain is suffering — yet MN 141:17 assigns mental pain to domanassa. How do you read it?\n"
          "Then re-answer questions 1–6 briefly, and say which of your first answers the text does not support.")
icons = {}
for f in os.listdir(os.path.join(HERE, 'icons')):
    svg = open(os.path.join(HERE, 'icons', f), encoding='utf-8').read()
    m = re.search(r'<path d="([^"]+)"', svg)
    if m:
        icons[f[:-4]] = m.group(1)
TESTS = [{'id': 'sutta-terms', 'date': DATE, 'title': 'Термины сутт: dukkha, taṇhā, anta, anicca, upādāna, sukha',
          'intro': 'Как модели понимают термины сутт: сначала без материала, потом после чтения нашего справочника llms-full.txt. Каждая модель — в новом чате.',
          'steps': [{'title': 'Шаг 1 — без материала', 'note': 'Вставить как есть.', 'prompt': STEP1},
                    {'title': 'Шаг 2 — с материалом', 'note': 'Кнопка копирует промпт вместе с полным текстом llms-full.txt (~2700 слов) — модели не всегда открывают ссылки.', 'prompt': STEP2, 'preview': STEP2.split('\n\n')[0] + '\n\n[здесь текст llms-full.txt, ~2700 слов]\n\n' + STEP2.rsplit('\n\n', 1)[1]},
                    {'title': 'Шаг 2b — прямые вопросы (в том же чате)', 'note': 'Решающая проверка.', 'prompt': STEP2B}],
          'rows': rows,
          'footnote': '2b (а) «где dukkha определена как не-боль?»: DeepSeek V3, Nemotron Ultra, Gemma 4, Qwen 3.8, Copilot — «нет такого места»; ChatGPT — «I cannot identify a passage». DeepSeek R1 возразил через три dukkhatā — ответ добавлен в текст. Perplexity цитирует только то, что есть в его поиске — dhamma.gift там пока нет.'}]
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
out = tpl.replace('/*__TESTS__*/[]', json.dumps(TESTS, ensure_ascii=False).replace('</', '<\\/')).replace('/*__ICONS__*/{}', json.dumps(icons))
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(out)
print(len(rows), 'rows;', round(len(out) / 1024), 'KB')
