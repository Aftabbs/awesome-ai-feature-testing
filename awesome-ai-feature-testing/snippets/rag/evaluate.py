"""
Tiny RAG eval starter — recall@k, faithfulness, answer-relevance.

Replace the in-memory store with your real one. Replace `client` calls with
your provider of choice. The eval pattern stays the same.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).parent

client = OpenAI()
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def embed(texts: list[str]) -> np.ndarray:
    return embedder.encode(texts, normalize_embeddings=True)


def retrieve(query: str, doc_emb: np.ndarray, docs: list[dict], k: int = 3) -> list[dict]:
    q_emb = embed([query])[0]
    sims = doc_emb @ q_emb
    top_k = np.argsort(-sims)[:k]
    return [{**docs[i], "score": float(sims[i])} for i in top_k]


def generate(query: str, retrieved: list[dict]) -> str:
    if not retrieved or retrieved[0]["score"] < 0.3:
        return json.dumps({"answer": "I don't have enough context to answer that.", "citations": []})

    ctx = "\n".join(f"[{r['id']}] {r['text']}" for r in retrieved)
    rsp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer using only the provided context. Cite [doc_id] for every claim. "
                    "If the context does not support the answer, say so. Output JSON: "
                    '{"answer": str, "citations": [str]}'
                ),
            },
            {"role": "user", "content": f"Context:\n{ctx}\n\nQuestion: {query}"},
        ],
        response_format={"type": "json_object"},
    )
    return rsp.choices[0].message.content or "{}"


def score_groundedness(answer: str, ctx: str) -> float:
    """A simple groundedness check — for production, use RAGAS or trulens."""
    rsp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You score groundedness 0-100. 100 = every factual claim in the answer is "
                    "supported by the context. 0 = the answer fabricates. Output JSON: "
                    '{"score": int, "rationale": str}'
                ),
            },
            {"role": "user", "content": f"Context:\n{ctx}\n\nAnswer:\n{answer}"},
        ],
        response_format={"type": "json_object"},
    )
    out = json.loads(rsp.choices[0].message.content or "{}")
    return float(out.get("score", 0))


def main() -> None:
    docs = load_jsonl(ROOT / "docs.jsonl")
    cases = load_jsonl(ROOT / "dataset.jsonl")

    doc_texts = [d["text"] for d in docs]
    doc_emb = embed(doc_texts)

    grounded_scores: list[float] = []
    recall_hits = 0
    empty_correct = 0

    for case in cases:
        retrieved = retrieve(case["input"], doc_emb, docs, k=3)
        answer = generate(case["input"], retrieved)
        ctx = "\n".join(r["text"] for r in retrieved)
        grounded = score_groundedness(answer, ctx)
        grounded_scores.append(grounded)

        gold_ids = set(case.get("expected_doc_ids", []))
        retrieved_ids = {r["id"] for r in retrieved}
        if gold_ids and gold_ids <= retrieved_ids:
            recall_hits += 1

        if not case.get("expected_doc_ids") and "I don't have enough" in answer:
            empty_correct += 1

        print(
            f"{case['id']:>10}  retrieved={','.join(str(r['id']) for r in retrieved)}  "
            f"grounded={grounded:.0f}"
        )

    has_gold = sum(1 for c in cases if c.get("expected_doc_ids"))
    no_gold = len(cases) - has_gold
    print()
    print(f"Recall@3:           {recall_hits}/{has_gold}")
    print(f"Empty handled:      {empty_correct}/{no_gold}")
    print(f"Mean groundedness:  {np.mean(grounded_scores):.1f} / 100")


if __name__ == "__main__":
    main()
