# Agent starter — 60 seconds

Tests: tool-call correctness + loop bound (max 5 calls per task).

Uses 3 mocked tools (calculator, weather, calendar).

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...
python evaluate.py
```

## Files

- `requirements.txt` — openai
- `evaluate.py` — runs 5 tasks; checks tool calls + loop bound
- `tasks.jsonl` — 5 tasks
