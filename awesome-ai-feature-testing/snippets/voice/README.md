# Voice (ASR) starter — 60 seconds

Tests: WER and CER on a small held-out audio set.

## Run

```bash
pip install -r requirements.txt

# Place 5 audio files at samples/01.wav ... samples/05.wav (paths in dataset.jsonl).
# Or download from a public dataset (Common Voice, LibriSpeech) and update paths.

export OPENAI_API_KEY=...
python evaluate.py
```

## Files

- `requirements.txt` — openai, jiwer
- `evaluate.py` — transcribes via Whisper API; computes WER + CER
- `dataset.jsonl` — 5 (audio_path, gold_transcript) pairs

## Sourcing audio

For a quick demo, use any of:

- [LibriSpeech dev-clean](https://www.openslr.org/12/) (~5MB samples)
- [Common Voice](https://commonvoice.mozilla.org/en/datasets) — free, multilingual
- Your own short recordings

Update `dataset.jsonl` to point to your files.
