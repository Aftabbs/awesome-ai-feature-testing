"""
Search eval starter — NDCG@10 + Recall@10 on a tiny corpus.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics import ndcg_score

ROOT = Path(__file__).parent

K = 10


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> None:
    docs = load_jsonl(ROOT / "corpus.jsonl")
    queries = load_jsonl(ROOT / "qrels.jsonl")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    doc_emb = model.encode([d["text"] for d in docs], normalize_embeddings=True)

    ndcgs: list[float] = []
    recalls: list[float] = []

    doc_ids = [d["id"] for d in docs]

    for q in queries:
        q_emb = model.encode([q["query"]], normalize_embeddings=True)[0]
        sims = doc_emb @ q_emb

        # NDCG@k requires a relevance vector for every doc; binary 1/0 here.
        relevance = np.array([1.0 if d in q["gold_doc_ids"] else 0.0 for d in doc_ids])
        scores_ranked = sims
        ndcg = float(ndcg_score([relevance], [scores_ranked], k=K))

        top_k_idx = np.argsort(-sims)[:K]
        top_k_ids = {doc_ids[i] for i in top_k_idx}
        gold = set(q["gold_doc_ids"])
        recall = len(top_k_ids & gold) / max(len(gold), 1)

        ndcgs.append(ndcg)
        recalls.append(recall)

        print(
            f"{q['id']:>10}  ndcg@{K}={ndcg:.3f}  recall@{K}={recall:.2f}  "
            f"top1={doc_ids[int(top_k_idx[0])]}"
        )

    print()
    print(f"Mean NDCG@{K}:   {np.mean(ndcgs):.3f}")
    print(f"Mean Recall@{K}: {np.mean(recalls):.2%}")


if __name__ == "__main__":
    main()
