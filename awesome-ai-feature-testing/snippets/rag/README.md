# RAG starter — 60 seconds

Tests: retrieval recall + groundedness (faithfulness) + empty-retrieval handling.

Uses a tiny in-memory document store (5 docs) and RAGAS for the eval.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...
python evaluate.py
```

## Files

- `requirements.txt` — RAGAS, openai, sentence-transformers
- `evaluate.py` — runs retrieval + generation + scoring
- `docs.jsonl` — 5-doc corpus
- `dataset.jsonl` — 6 test queries (1 with no good doc)
