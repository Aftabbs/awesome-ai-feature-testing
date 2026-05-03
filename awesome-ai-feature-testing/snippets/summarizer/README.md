# Summarizer starter — 60 seconds

Tests: faithfulness + length + anti-padding.

## Run

```bash
export OPENAI_API_KEY=...
npx behaviourci test
```

## Files

- `bundle.yaml` — BehaviorCI bundle
- `prompt.md` — system prompt
- `dataset.jsonl` — 8 short articles to summarize
