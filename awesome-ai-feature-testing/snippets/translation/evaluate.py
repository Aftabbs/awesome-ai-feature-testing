"""
Translation eval starter — sacreBLEU + COMET on 10 en→es pairs.
"""

from __future__ import annotations

import json
from pathlib import Path

import sacrebleu
from comet import download_model, load_from_checkpoint
from openai import OpenAI

ROOT = Path(__file__).parent
client = OpenAI()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def translate(en_text: str) -> str:
    rsp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate the user's English text to Spanish. Output ONLY the Spanish translation."},
            {"role": "user", "content": en_text},
        ],
    )
    return (rsp.choices[0].message.content or "").strip()


def main() -> None:
    cases = load_jsonl(ROOT / "dataset.jsonl")

    sources = [c["en"] for c in cases]
    refs = [c["es"] for c in cases]
    hyps = [translate(s) for s in sources]

    bleu = sacrebleu.corpus_bleu(hyps, [refs]).score
    print(f"Corpus BLEU: {bleu:.2f}")

    print("Loading COMET model (one-time download ~2GB)...")
    comet_path = download_model("Unbabel/wmt22-comet-da")
    comet_model = load_from_checkpoint(comet_path)

    comet_data = [{"src": s, "mt": h, "ref": r} for s, h, r in zip(sources, hyps, refs)]
    comet_scores = comet_model.predict(comet_data, batch_size=8, gpus=0)
    print(f"Mean COMET:  {comet_scores['system_score']:.3f}")

    print()
    print("Per-pair:")
    for i, c in enumerate(cases):
        print(
            f"  {c['id']:>10}  bleu_sentence={sacrebleu.sentence_bleu(hyps[i], [refs[i]]).score:.1f}  "
            f"comet={comet_scores['scores'][i]:.3f}"
        )


if __name__ == "__main__":
    main()
