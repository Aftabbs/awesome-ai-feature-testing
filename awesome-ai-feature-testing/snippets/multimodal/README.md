# Multimodal starter — 60 seconds

Tests: VQA accuracy + caption faithfulness using a vision-LM.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...
python evaluate.py
```

## Files

- `requirements.txt` — openai
- `evaluate.py` — runs VQA + caption gen on 5 stock-photo images
- `dataset.jsonl` — 5 (image_url, question, expected) tuples
