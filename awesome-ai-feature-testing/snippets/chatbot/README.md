# Chatbot starter — 60 seconds

Tests: persona stability + PII redaction + length compliance + tone matching.

## Run

```bash
export GROQ_API_KEY=...   # or OPENAI_API_KEY / ANTHROPIC_API_KEY
npx behaviourci test
```

Or, with Promptfoo:

```bash
npx promptfoo eval -c promptfoo.yaml
```

## Files

- `bundle.yaml` — BehaviorCI bundle (8 behaviors, 12 cases)
- `prompt.md` — the system prompt
- `dataset.jsonl` — 12 input cases
- `promptfoo.yaml` — equivalent Promptfoo config (optional)
