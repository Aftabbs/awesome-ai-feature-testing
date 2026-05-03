# Code-gen starter — 60 seconds

Tests: compile + lint + test execution on 5 small Python tasks.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...
python evaluate.py
```

## Files

- `requirements.txt` — openai, ruff, pytest
- `evaluate.py` — generates code, writes to a temp dir, runs compile + ruff + pytest
- `tasks.jsonl` — 5 task descriptions with inline tests
