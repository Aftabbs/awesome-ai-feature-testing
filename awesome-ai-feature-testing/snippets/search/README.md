# Search starter — 60 seconds

Tests: NDCG@10 + Recall@10 on a 50-doc / 30-query mini-corpus.

Uses sentence-transformers for dense retrieval against in-memory store.

## Run

```bash
pip install -r requirements.txt
python evaluate.py
```

(No API key needed — runs entirely with `sentence-transformers`.)

## Files

- `requirements.txt` — sentence-transformers, scikit-learn, numpy
- `evaluate.py` — embeds docs and queries; ranks; computes NDCG/Recall
- `corpus.jsonl` — 50 short docs across 5 topics
- `qrels.jsonl` — 30 queries with gold doc_ids
