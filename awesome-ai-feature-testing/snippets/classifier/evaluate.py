"""
Classifier eval starter — per-class F1 + Expected Calibration Error.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from openai import OpenAI
from sklearn.metrics import classification_report, confusion_matrix

ROOT = Path(__file__).parent
client = OpenAI()

LABELS = ["billing", "refund", "shipping", "technical", "cancel"]


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def classify(text: str) -> tuple[str, float]:
    rsp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Classify the user message into exactly one of: {', '.join(LABELS)}. "
                    "Output JSON: {\"label\": str, \"confidence\": float in [0, 1]}. "
                    "Confidence must be calibrated — if you're unsure, give low confidence."
                ),
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )
    out = json.loads(rsp.choices[0].message.content or "{}")
    label = out.get("label", "billing")
    if label not in LABELS:
        label = "billing"
    return label, float(out.get("confidence", 0.5))


def expected_calibration_error(confidences: list[float], correct: list[bool], n_bins: int = 10) -> float:
    confs = np.asarray(confidences)
    correctness = np.asarray(correct, dtype=float)
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        mask = (confs > bins[i]) & (confs <= bins[i + 1])
        if mask.sum() == 0:
            continue
        bin_acc = correctness[mask].mean()
        bin_conf = confs[mask].mean()
        ece += (mask.sum() / len(confs)) * abs(bin_acc - bin_conf)
    return ece


def main() -> None:
    cases = load_jsonl(ROOT / "dataset.jsonl")

    preds: list[str] = []
    confs: list[float] = []
    golds: list[str] = []

    for case in cases:
        pred, conf = classify(case["text"])
        preds.append(pred)
        confs.append(conf)
        golds.append(case["label"])

    print(classification_report(golds, preds, labels=LABELS, zero_division=0))
    print()
    print("Confusion matrix:")
    cm = confusion_matrix(golds, preds, labels=LABELS)
    print("        " + " ".join(f"{l:>8}" for l in LABELS))
    for label, row in zip(LABELS, cm):
        print(f"{label:>7} " + " ".join(f"{n:>8d}" for n in row))

    correct = [p == g for p, g in zip(preds, golds)]
    ece = expected_calibration_error(confs, correct)
    print()
    print(f"Accuracy: {sum(correct) / len(correct):.2%}")
    print(f"ECE:      {ece:.3f}  (target ≤ 0.05)")


if __name__ == "__main__":
    main()
