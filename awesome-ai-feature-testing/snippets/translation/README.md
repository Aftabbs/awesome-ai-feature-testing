# Translation starter — 60 seconds

Tests: sacreBLEU + COMET on a 10-pair en→es set.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...
python evaluate.py
```

## Files

- `requirements.txt` — openai, sacrebleu, unbabel-comet
- `evaluate.py` — translates each source via gpt-4o-mini; computes BLEU + COMET
- `dataset.jsonl` — 10 (en source, es reference) pairs
