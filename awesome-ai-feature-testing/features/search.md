# Search & ranking

Search and ranking features are the closest AI feature to traditional ML — they have decades of IR methodology. Newer challenges: semantic search via embeddings, hybrid (BM25 + dense), reranker stacking.

This page covers: dense retrieval, hybrid search, reranking, recommendation systems, semantic search, learning-to-rank.

---

## Testing patterns

### 1. Recall@k

**What it tests:** Fraction of queries where the relevant document is in the top k retrieved.

**Tools:** [BEIR](https://github.com/beir-cellar/beir), [trec_eval](https://github.com/usnistgov/trec_eval), [MTEB](https://github.com/embeddings-benchmark/mteb).

---

### 2. Precision@k

**What it tests:** Fraction of top-k results that are relevant.

**Tools:** Same as Recall@k.

---

### 3. NDCG@k / MRR

**What it tests:** Quality of the ranked order, weighted by position.

**Tools:** sklearn (`ndcg_score`), trec_eval, BEIR.

---

### 4. Coverage / catalogue diversity

**What it tests:** Across many queries, what fraction of the catalogue surfaces in top-k? Are popular items dominating?

**Tools:** Custom Python aggregation.

---

### 5. Semantic similarity quality (embedding eval)

**What it tests:** Embedding model's ability to cluster similar items / distinguish dissimilar ones.

**Tools:** [MTEB](https://github.com/embeddings-benchmark/mteb), [BEIR](https://github.com/beir-cellar/beir), [SentEval](https://github.com/facebookresearch/SentEval).

---

### 6. Hybrid blend tuning

**What it tests:** When combining BM25 + dense, what blend ratio gives best NDCG@k?

**Tools:** [vespa eval](https://github.com/vespa-engine/vespa) for production-grade; sklearn for offline.

---

### 7. Personalization quality

**What it tests:** For recommendation features, are recommendations actually relevant per-user?

**Tools:** [RecBole](https://github.com/RUCAIBox/RecBole), [Cornac](https://github.com/PreferredAI/cornac), implicit feedback metrics.

---

### 8. Cold-start performance

**What it tests:** How does the system perform on new users / new items with little signal?

**Tools:** Stratified eval; cold-start cohort labeling.

---

### 9. Latency at scale

**What it tests:** p95 / p99 latency under load.

**Tools:** [k6](https://k6.io/), [locust](https://github.com/locustio/locust).

---

## Recommended tools

### IR / search eval

- **[BEIR](https://github.com/beir-cellar/beir)** — heterogeneous IR benchmark.
- **[MTEB](https://github.com/embeddings-benchmark/mteb)** — embedding model benchmark.
- **[trec_eval](https://github.com/usnistgov/trec_eval)** — NIST classic.
- **[ir_datasets](https://github.com/allenai/ir_datasets)** — datasets + eval.
- **[ranx](https://github.com/AmenRa/ranx)** — fast IR evaluation library.

### Recommendation eval

- **[RecBole](https://github.com/RUCAIBox/RecBole)** — recommendation toolbox.
- **[Cornac](https://github.com/PreferredAI/cornac)** — multimodal recommender.
- **[implicit](https://github.com/benfred/implicit)** — implicit-feedback CF.

### Vector store / search benchmarks

- **[ANN-Benchmarks](https://github.com/erikbern/ann-benchmarks)** — ANN performance.
- **[Big-ANN-Benchmarks](https://github.com/harsha-simhadri/big-ann-benchmarks)** — billion-scale.

### Hybrid search

- **[Vespa](https://github.com/vespa-engine/vespa)** — search engine with strong eval tooling.
- **[Elasticsearch + dense vectors](https://github.com/elastic/elasticsearch)** — has ML evaluator.
- **[OpenSearch](https://github.com/opensearch-project/OpenSearch)** — fork with native vector support.

### LLM-as-judge for relevance

- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — semantic relevance judges.
- **[DeepEval](https://github.com/confident-ai/deepeval)** — `RetrievalRelevanceMetric`.

### Datasets

- **[MS MARCO](https://github.com/microsoft/MSMARCO-Passage-Ranking)** — large web search dataset.
- **[Natural Questions](https://github.com/google-research-datasets/natural-questions)** — search-oriented QA.
- **[TREC tracks](https://trec.nist.gov/)** — yearly research datasets.
- **[Amazon Reviews](https://nijianmo.github.io/amazon/index.html)** — recommendation.
- **[Movielens](https://grouplens.org/datasets/movielens/)** — recommendation classic.

---

## Sample rubric (semantic search feature)

```yaml
behaviors:
  - id: ndcg-at-10
    type: function
    function: src.evals.checks.ndcg_at_k
    config: { k: 10 }
    pass_threshold: 0.78
    weight: 3

  - id: recall-at-10
    type: function
    function: src.evals.checks.recall_at_k
    config: { k: 10 }
    pass_threshold: 0.92
    weight: 2

  - id: distinct-domains-in-top-10
    type: function
    function: src.evals.checks.distinct_domains
    config: { k: 10, min_distinct: 4 }
    pass_threshold: 0.85
    weight: 1

  - id: tenant-scope
    type: function
    function: src.evals.checks.tenant_scope
    pass_threshold: 100
    weight: 5

aggregate:
  pass_threshold: 0.85

gates:
  latency_p95_max_absolute_ms: 150
```

---

## Failure-mode catalog (search-specific)

See [FAILURE-MODES.md#search](../FAILURE-MODES.md#search).

- **Stale-result confidence.** Top result is from 2018; top-1 score high.
- **Reranker collapse.** Reranker permutes irrelevantly on ambiguous queries.
- **Embedding drift.** Embedding model upgraded; index not re-embedded; silent regression.
- **Tenant leak.** Search returns docs across tenant boundaries.
- **Filter bubble.** Personalization narrows result set so much that exploration is impossible.
- **Cold-start collapse.** New users get popular items only; never converges.
- **Long-tail entity confusion.** Same name, different entities conflated.
- **Locale failure.** Spanish query returning English-only docs.

---

## Run this in 60 seconds

```bash
cd snippets/search
export OPENAI_API_KEY=...

# 50-query mini-search eval with NDCG@10 + recall@10
python evaluate.py
```

See [snippets/search/](../snippets/search/).

---

## Maturity ladder for search testing

- **L0** — manual query testing.
- **L1** — NDCG@k on a held-out set.
- **L2** — multi-metric: NDCG + recall + diversity.
- **L3** — merge-gating bundle + tenant isolation + cost / latency.
- **L4** — continuous + per-cohort drift + adversarial query coverage.

L3 is the bar for production search.

---

## See also

- [rag.md](rag.md) — for retrieval-as-context
- [recommendation systems](https://github.com/awesome-list-recommendation) — for personalization
- [classifiers.md](classifiers.md) — for query classification
