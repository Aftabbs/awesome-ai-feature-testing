"""
Multimodal eval starter — VQA accuracy + caption faithfulness.
"""

from __future__ import annotations

import json
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).parent
client = OpenAI()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def vqa(image_url: str, question: str) -> str:
    rsp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question + " Answer in one short phrase."},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
    )
    return (rsp.choices[0].message.content or "").strip().lower()


def matches(pred: str, expected_keywords: list[str]) -> bool:
    p = pred.lower()
    return any(k.lower() in p for k in expected_keywords)


def main() -> None:
    cases = load_jsonl(ROOT / "dataset.jsonl")

    correct = 0
    for case in cases:
        ans = vqa(case["image_url"], case["question"])
        ok = matches(ans, case["expected_keywords"])
        correct += int(ok)
        print(f"{case['id']:>10}  {'PASS' if ok else 'FAIL'}  pred={ans!r}")

    print()
    print(f"Accuracy: {correct}/{len(cases)} ({correct/len(cases):.0%})")


if __name__ == "__main__":
    main()
