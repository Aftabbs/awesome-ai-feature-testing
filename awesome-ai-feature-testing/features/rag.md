# RAG & grounded QA

RAG (Retrieval-Augmented Generation) features look easy to test on accuracy and pathologically easy to ship with high hallucination rates and silent retrieval failures. The common failure pattern: the eval set scores 87% groundedness; production groundedness is closer to 60% because the eval set didn't cover real query distribution.

Test the retrieval, the generator, and the integration separately. Then add an end-to-end groundedness gate.

This page covers any feature that retrieves before generating — internal QA, customer-facing knowledge base bots, doc-grounded summarization, citation-required Q&A.

---

## Testing patterns

### 1. Retrieval recall@k

**What it tests:** Does the retriever surface the relevant chunks for each query in the top-k?

**Tools:** [BEIR](https://github.com/beir-cellar/beir), [RAGAS](https://github.com/explodinggradients/ragas), [continuous-eval](https://github.com/relari-ai/continuous-eval), custom Python (sklearn metrics).

**When to use:** Always. Bad retrieval makes good generation impossible.

**Cost / effort:** Medium. Need a (query, relevant_doc_ids) labeled set.

**Common pitfalls:**
- Recall@5 is the most common metric; teams report it without saying what k is.
- A high recall@5 with low recall@1 means re-ranking matters.

---

### 2. Retrieval precision and source diversity

**What it tests:** Are the top-k retrieved chunks actually relevant, or are some "near misses" diluting the context?

**Tools:** RAGAS (`context_precision`), Phoenix evaluators, custom check against gold relevance labels.

**When to use:** Especially when context window is tight or chunks are long.

---

### 3. Groundedness / faithfulness

**What it tests:** Does every claim in the generated answer have support in the retrieved context?

**Tools:** [RAGAS](https://github.com/explodinggradients/ragas) (`faithfulness`), [DeepEval](https://github.com/confident-ai/deepeval) (`FaithfulnessMetric`), [trulens](https://github.com/truera/trulens) (groundedness feedback), [Phoenix](https://github.com/Arize-ai/phoenix), [continuous-eval](https://github.com/relari-ai/continuous-eval).

**When to use:** Always for any factual-answer feature.

**Cost / effort:** Medium-high. Most groundedness checks are LLM-as-judge — apply Rule 5 (judge has its own eval set).

---

### 4. Citation correctness

**What it tests:** Are citations formatted correctly? Do cited doc_ids resolve to real documents? Does the cited content actually support the claim?

**Tools:** Custom function (URL/ID resolver) + LLM-as-judge for "does cite support claim?"

**When to use:** Any feature that surfaces citations to users.

---

### 5. Hallucination on no-result

**What it tests:** When retrieval returns nothing relevant, does the generator say "I don't know" or fabricate?

**Tools:** [RAGTruth dataset](https://huggingface.co/datasets/wandb/RAGTruth-processed), custom adversarial set with empty/irrelevant retrieval.

**When to use:** Always.

**Common pitfalls:**
- Forgetting to test the empty-retrieval case is the most common ship-time bug.

---

### 6. Tenant / scope isolation

**What it tests:** Does retrieval ever return docs from another tenant / user / scope it shouldn't have access to?

**Tools:** Custom function check verifying every cited doc's tenant/scope matches the query's.

**When to use:** Any multi-tenant SaaS RAG. This is a P0 violation when it fails.

---

### 7. Query rewriting quality

**What it tests:** When the pipeline rewrites the user query before retrieval, does the rewrite preserve intent?

**Tools:** Pairwise judge (BEIR, RAGAS), human-in-the-loop labeling.

**When to use:** Any RAG with a query-rewriting step.

---

### 8. Chunk quality (offline)

**What it tests:** Are chunks retrievable units? Do they end mid-sentence? Mid-table?

**Tools:** [chunking-eval](https://github.com/brandonstarxel/chunking_evaluation) from Chroma, custom inspection scripts.

**When to use:** Any time you change chunking strategy.

---

### 9. Index-time PII

**What it tests:** Was the indexed content scrubbed of PII before embedding?

**Tools:** Microsoft Presidio (re-scan the index), custom script to sample-and-scan.

**When to use:** Any RAG over corporate or customer data. **A unique challenge for RAG**: PII enters at index time, not query time.

---

### 10. Reranker discriminative power

**What it tests:** Does the reranker actually re-order in a meaningful way, or is it adding cost without value?

**Tools:** Compare retrieval@k with and without reranker on the same eval; see if the gold doc moves toward top-1.

**When to use:** When deciding whether to add a reranker, or auditing if you should remove one.

---

### 11. Cross-doc reasoning (multi-hop)

**What it tests:** Can the system answer questions whose answer requires combining info from 2+ retrieved docs?

**Tools:** [HotpotQA](https://github.com/hotpotqa/hotpot), [MuSiQue](https://github.com/StonyBrookNLP/musique), [2WikiMultiHopQA](https://github.com/Alab-NII/2wikimultihop), [LongBench](https://github.com/THUDM/LongBench).

**When to use:** RAG features intended for analytical / synthesis questions.

---

### 12. Date / recency awareness

**What it tests:** Does the system prefer recent docs when the question is time-sensitive? Does it flag outdated answers?

**Tools:** Custom function checking citation `retrieved_at` vs question time signals.

**When to use:** RAG over a corpus that ages (news, policy docs, eng docs).

---

### 13. Cost per call decomposition

**What it tests:** Where in the pipeline does cost come from — embedding, retrieval, reranking, generation, judge?

**Tools:** Phoenix, Langfuse, Opik, Helicone (any with cost-per-step tracing).

**When to use:** Always; cost regressions in RAG are silent and compound.

---

### 14. End-to-end answer quality (the integration test)

**What it tests:** All of the above, end-to-end, on a held-out set with stratification by question type.

**Tools:** RAGAS, continuous-eval, BehaviorCI, DeepEval.

**When to use:** Required for shipping. The integration eval is the contract.

---

## Recommended tools

### RAG-specific eval frameworks

- **[RAGAS](https://github.com/explodinggradients/ragas)** — purpose-built RAG eval. Faithfulness, answer-relevance, context-precision, context-recall.
- **[continuous-eval](https://github.com/relari-ai/continuous-eval)** — data-driven RAG eval framework with cost-aware metrics.
- **[DeepEval](https://github.com/confident-ai/deepeval)** — RAG-specific assertions plus general LLM eval.
- **[trulens](https://github.com/truera/trulens)** — feedback functions for RAG observability.
- **[Phoenix](https://github.com/Arize-ai/phoenix)** — RAG eval + tracing in one platform.

### Retrieval evaluators

- **[BEIR](https://github.com/beir-cellar/beir)** — heterogeneous retrieval benchmark.
- **[MTEB](https://github.com/embeddings-benchmark/mteb)** — embedding model benchmark.
- **[ir_datasets](https://github.com/allenai/ir_datasets)** — standardized IR datasets.

### Index / chunking evaluators

- **[chunking_evaluation](https://github.com/brandonstarxel/chunking_evaluation)** — Chroma's chunking eval framework.
- **[unstructured](https://github.com/Unstructured-IO/unstructured)** — quality of doc parsing.

### Generation / faithfulness evaluators

- **[FactScore](https://github.com/shmsw25/FActScore)** — atomic-fact-level groundedness.
- **[FActScore](https://github.com/shmsw25/FActScore)** — fine-grained factuality eval.
- **[Lynx](https://github.com/PatronusAI/Lynx)** — hallucination detection by Patronus.
- **[KubernetesAI's hallucination detector](https://github.com/HillZhang1999/KCD)** — research-grade.

### Multi-hop / long-context benchmarks

- **[LongBench](https://github.com/THUDM/LongBench)** — long-context benchmark.
- **[HotpotQA](https://github.com/hotpotqa/hotpot)** — multi-hop QA dataset.
- **[MuSiQue](https://github.com/StonyBrookNLP/musique)** — composable multi-hop questions.
- **[LV-Eval](https://github.com/infinigence/LVEval)** — long-context eval.

### General eval (with strong RAG support)

- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — bundle-level pass/fail with rule + semantic checks; pairs with RAGAS for the deep metrics.
- **[Promptfoo](https://github.com/promptfoo/promptfoo)** — eval-as-code; supports RAG-style assertions.
- **[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)** — research-grade.

### Observability with RAG features

- **[Langfuse](https://github.com/langfuse/langfuse)** — strong tracing for retrieval + gen.
- **[Opik](https://github.com/comet-ml/opik)** — debug, evaluate, monitor.
- **[OpenLIT](https://github.com/openlit/openlit)** — OpenTelemetry-native.

### Datasets

- **[RAGTruth](https://huggingface.co/datasets/wandb/RAGTruth-processed)** — labeled hallucination dataset.
- **[Natural Questions](https://github.com/google-research-datasets/natural-questions)** — Google's QA benchmark.
- **[TriviaQA](https://github.com/mandarjoshi90/triviaqa)** — open-domain QA.
- **[FinanceBench](https://github.com/patronus-ai/financebench)** — finance-specific RAG benchmark.

### Vector store and reranker primitives

- **[Pinecone](https://www.pinecone.io/)**, **[Qdrant](https://github.com/qdrant/qdrant)**, **[Weaviate](https://github.com/weaviate/weaviate)**, **[Chroma](https://github.com/chroma-core/chroma)** — vector stores; the eval is mostly downstream of which one you pick.
- **[Cohere Rerank](https://docs.cohere.com/docs/rerank-overview)**, **[mxbai-rerank](https://huggingface.co/mixedbread-ai/mxbai-rerank-large-v1)** — rerankers worth benchmarking.

---

## Sample rubric

```yaml
feature: kb-rag
spec: specs/kb-rag.md

behaviors:
  - id: every-claim-grounded
    type: semantic
    judge: evals/judges/groundedness-judge.yml
    pass_threshold: 80
    weight: 3

  - id: cites-real-docs
    type: function
    function: src.evals.checks.citations_resolve
    pass_threshold: 100
    weight: 3

  - id: no-cross-tenant
    type: function
    function: src.evals.checks.tenant_scope
    pass_threshold: 100
    weight: 5

  - id: empty-retrieval-says-idk
    type: function
    function: src.evals.checks.empty_retrieval_idk
    pass_threshold: 100
    weight: 2

aggregate:
  pass_threshold: 0.88
```

See the [chatbot RAG cookbook](https://github.com/Aftabbs/claude-code-rules-for-ai-features/blob/main/cookbook/rag-feature.md) for the full version with all 10 rules applied.

---

## Failure-mode catalog (RAG-specific)

See [FAILURE-MODES.md#rag](../FAILURE-MODES.md#rag) for the catalog. Highlights:

- **Confident citation of irrelevant doc.** Top-1 is low-relevance; model cites it confidently.
- **Cross-tenant leak.** Shared template doc returned across tenants.
- **Hallucinated chunk_id.** Model invents IDs when uncertain.
- **Cite-but-contradict.** Cite a doc that disagrees with the claim.
- **Stale-data confidence.** Old article cited as current.
- **Empty-retrieval fabrication.** No relevant chunks → model invents an answer.
- **Multi-hop reduce.** Question needs 2 docs; model only cites one and answers from one.
- **Index-time PII leak.** Indexed doc had PII; surfaced in retrieval.
- **Reranker degeneracy.** Reranker collapses on irrelevant query, top-1 is random.
- **Long-tail entity confusion.** "John Smith" in two docs about different John Smiths conflated.

---

## Run this in 60 seconds

```bash
cd snippets/rag
export OPENAI_API_KEY=...

# Run RAGAS faithfulness + answer-relevance on a 10-case mini set
python evaluate.py
```

See [snippets/rag/](../snippets/rag/) for the dataset, embeddings, and the small in-memory store.

---

## Maturity ladder for RAG testing

- **L0** — vibes. "Sounds about right."
- **L1** — retrieval @k recall on a small labeled set, run before deploy.
- **L2** — full RAG bundle: retrieval recall, faithfulness, answer-relevance, no-cross-tenant. Runs in CI.
- **L3** — merge-gating bundle + cost & latency gates per stage. Index-time PII enforcement.
- **L4** — continuous production scoring + drift detection per index version + adversarial / multi-hop coverage.

L3 is the realistic bar for production RAG in 2026.

---

## See also

- [chatbots.md](chatbots.md) — for conversational RAG
- [agents.md](agents.md) — for agent-orchestrated retrieval
- [search.md](search.md) — pure search & ranking, no generation
- [classifiers.md](classifiers.md) — for query-classification routing
