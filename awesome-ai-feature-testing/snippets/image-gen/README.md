# Image-gen starter — 60 seconds

Tests: prompt fidelity (CLIP score) + NSFW classification.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...
python evaluate.py
```

## Files

- `requirements.txt` — openai, transformers, torch, pillow
- `evaluate.py` — generates 5 images with DALL·E, computes CLIPScore, runs NSFW filter
- `prompts.jsonl` — 5 prompts (4 SFW + 1 borderline)
