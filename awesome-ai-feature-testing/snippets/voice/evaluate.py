"""
Voice / ASR eval starter — WER + CER on a small held-out audio set.
"""

from __future__ import annotations

import json
from pathlib import Path

import jiwer
from openai import OpenAI

ROOT = Path(__file__).parent
client = OpenAI()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def transcribe(audio_path: Path) -> str:
    with audio_path.open("rb") as f:
        rsp = client.audio.transcriptions.create(model="whisper-1", file=f)
    return rsp.text.strip()


def main() -> None:
    cases = load_jsonl(ROOT / "dataset.jsonl")

    wers: list[float] = []
    cers: list[float] = []
    for case in cases:
        audio = ROOT / case["audio_path"]
        if not audio.exists():
            print(f"{case['id']:>10}  SKIP (file missing: {audio})")
            continue

        pred = transcribe(audio)
        gold = case["gold_transcript"]
        wer = jiwer.wer(gold, pred)
        cer = jiwer.cer(gold, pred)
        wers.append(wer)
        cers.append(cer)

        print(f"{case['id']:>10}  wer={wer:.2%}  cer={cer:.2%}")
        if wer > 0.15:
            print(f"             pred: {pred}")
            print(f"             gold: {gold}")

    if wers:
        print()
        print(f"Mean WER: {sum(wers) / len(wers):.2%}")
        print(f"Mean CER: {sum(cers) / len(cers):.2%}")


if __name__ == "__main__":
    main()
