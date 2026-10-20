# Тесты для ИИ

How AI models understand the Pali Canon's terms. Each model gets a test in three steps:
1. cold, from its own knowledge;
2. after reading https://dhamma.gift/llms-full.txt;
3. 2b, the direct questions.

The page shows the steps (with copy buttons) and every model's answers, as a short summary plus the full text.

- **Page:** `index.html`, one self-contained HTML file. It is served at https://test.dhamma.gift/ai-tests/ (on f3, `siteroot/ai-tests` points to this folder in the `/root/work/dg-dataset` checkout) and linked from the hub's «Тесты» tab.
- **Build:** `python3 build.py`. It reads `full/*.md` (answers pasted from browser chats), `raw/*.json` (API and Kaggle runs), `icons/*.svg` (Simple Icons, CC0) and the current llms-full.txt from the site, and writes `data.json` and `index.html`.

## Adding a run

- **Browser chat:** save the model's answers to `full/<model>.md` under `## Step 1 (cold)`, `## Step 2 (with llms-full.txt)`, `## Step 2b`, verbatim. Add a `row(...)` line in `build.py` with the brand (an icon name from `icons/`), the channel and the short Russian summaries.
- **API:** add the answers to `raw/answers-api-full.json` (`{model: {cold, warm, push}}`) and a `from_api(...)` line.
- Then run `python3 build.py`, commit and push. f3 serves the folder as it is, so run `git pull` in `/root/work/dg-dataset` there.

## Adding a test

Add an entry to `TESTS` in `build.py`: id, date, title, intro, steps with their prompts, rows and footnote.

## Rules (owner)

- Answers go in verbatim.
- Models' objections are recorded here. They do not go into llms-full.txt, unless many models repeat one and the owner agrees.
- No secrets: API keys live only in `/root/.secrets` on the servers.
