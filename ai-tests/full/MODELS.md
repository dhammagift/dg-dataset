# AI test «Термины сутт»: models asked (2026-10-20)
Steps: 1 cold · 2 with llms-full.txt (or llms.txt) · 2b the direct questions (a) "where is dukkha defined as other than pain?" (b) MN 141:10.2

| Model | Channel | Cold | With material | 2b (a) |
|---|---|---|---|---|
| gpt-oss 20B, Qwen3 14B, Gemma 3 12B, Llama 3.1 8B, Mistral Nemo 12B, DeepSeek-R1 14B | Kaggle GPU (ollama) | 6/6 usual renderings, invented citations | excerpt: dukkha 6/6, sukha 4/6, taṇhā 4/6, anicca 4/6, anta 0/6, upādāna 0/6; llms-full: 5 terms 6/6, anta 5/6 | — |
| ChatGPT (no login), runs 1–3 | browser | usual; misses MN 141:16; wrong refs | accepts method + bodily/mental distinction; rest "interpretation" | "I cannot identify a passage…" |
| Gemini | browser | usual; non-existent suttas | link not opened → "no gap"; full text pasted → accepted all 6 | — |
| Copilot | browser | usual (dukkha "by enumeration", misses MN 141:16, SN 48.36) | follows the doc on all 6 ("a specific philological argument") | "nowhere"; revised all six |
| DeepSeek Chat (V3) | API | usual | accepted | "There is none" |
| DeepSeek Reasoner (R1) | API | usual | accepted | objects via three dukkhatā → text answers it now |
| Nemotron Ultra 550B | NVIDIA | usual | accepted | "There is no passage" |
| Gemma 4 31B | NVIDIA | usual | accepted | "There is no such passage" |
| gpt-oss 120B | Groq | usual | partly; 2b too big for 8k TPM | — |
| Qwen 3.8 27B | Groq | usual | accepted (llms-full and llms.txt) | llms.txt run: "There is no passage" |
| DeepSeek Chat, Qwen 3.8 (llms.txt only) | API | — | dukkha, sukha, taṇhā, anta accepted; anicca/upādāna "not in the document" → llms.txt extended | — |
| Claude Opus 5.5, Haiku 5.5, Fable 5.1 | Anthropic API | usual (enumeration, three dukkhatā) | empty replies (script bug, to fix) | — |
| Perplexity | browser | usual; cites SuttaCentral (Sujato); misses MN 141:16 and SN 48.36 | follows the doc on all 6, but cites a random page (opentextbooks.rug.nl) for our text | not reached (login wall) |
| Not reached | — | Gemini Pro (no free quota), Gemini Flash (503), Kimi K2.6 / Mistral Large 2 (NVIDIA 404), DeepSeek V4.1 / GLM-5.3 (timeout), OpenRouter paid (key limit) | | |
