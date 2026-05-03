# Classifier starter — 60 seconds

Tests: per-class F1 + calibration (ECE).

Uses an LLM as a 5-class intent classifier on customer support inputs.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...
python evaluate.py
```

## Files

- `requirements.txt` — openai, scikit-learn, numpy
- `evaluate.py` — runs the classifier; computes confusion matrix, F1, ECE
- `dataset.jsonl` — 30 labeled cases across 5 classes
