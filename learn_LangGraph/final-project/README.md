# Fictional shop document assistant

Final project (Lessons 25–27). A standalone copy of the workflow
you built in Lessons 19–24, with its own documents and saved evaluation cases.

Run from `/Users/thomasmusieracki/Desktop/learn`:

```sh
.venv-langgraph/bin/python final-project/chat.py
.venv-langgraph/bin/python final-project/app.py cost
.venv-langgraph/bin/python final-project/app.py receipt
.venv-langgraph/bin/python final-project/app.py "shipping insurance"
.venv-langgraph/bin/python final-project/evaluate.py
```

Default generation uses a controlled fixture, without Gemini requests. To call
Gemini explicitly, use `app.py cost --mode live`. This reuses the existing root
`.env` automatically; no new key file or terminal exports are needed. Existing
terminal exports take precedence. Keep billing disabled and use free-tier quota.
With LangSmith tracing enabled, graph state is uploaded in both modes. Set
`LANGSMITH_TRACING=false` for local-only fixture practice.

## First-version scope

- `cost`: standard shipping price per order.
- `receipt`: the receipt requirement for returns.
- Other question forms are refused, even when retrieval finds a passage.
- Plain `.txt` documents, split on blank lines; filename and paragraph number
  identify a source. Inserting paragraphs can change these labels.
- Released drafts must quote the accepted sentence and cite it exactly once.
  This strict validator can reject correct paraphrases; it is not a general
  factuality checker.

## Files

| File | Purpose |
| --- | --- |
| `chat.py` | Repeated terminal input; displays only final answer/status; /help and /quit |
| `app.py` | LangGraph application, evidence gate, Gemini/fixture generation, answer gate |
| `document_search.py` | Local loading and word-overlap retrieval |
| `documents/` | Fictional shipping and returns policies |
| `cases.json` | Fixed evaluation inputs and reference outputs |
| `evaluate.py` | Compares actual application behavior with those references |

The application never reads `cases.json`. A reference answer is an evaluation
target, not evidence for generating an answer. The documents supply the answer.
If a policy changes intentionally, review the policy and expected behavior before
updating references. Do not change expectations merely to hide a failing case.

The `wrong_price` fixture deliberately changes the original $5 to $50; restore
the starter price to $5 before running the baseline suite. Seven passing fixtures
do not establish that every live model run will pass.

The terminal interface starts in fixture mode. Use `chat.py --live` to opt into
Gemini for the session. Each question starts fresh, without conversation memory.
Run names are `shop-chat-good` or `shop-chat-live`.

Lesson 26 diagnoses project runs; Lesson 27 exercises the terminal interface.
The assembled first version is intentionally limited to the scope above.

Fresh environment: install `langgraph langsmith python-dotenv google-genai`
into `.venv-langgraph`. Live generation needs `GEMINI_API_KEY`; optional
`GEMINI_MODEL` defaults to `gemini-3.5-flash-lite`. Never commit `.env`.
