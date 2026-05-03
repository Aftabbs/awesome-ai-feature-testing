# Maturity matrix — how solved is testing in each AI feature category

How well-developed is testing methodology for each AI feature category? This matrix scores each category on five dimensions:

- **Tools** — quality and breadth of OSS / commercial eval tools
- **Datasets** — availability and coverage of open benchmarks
- **Failure modes** — how well the failure-mode catalog is documented
- **CI patterns** — how easy it is to integrate into modern CI/CD
- **Production observability** — how mature monitoring and drift detection are

Each is scored 1–5. 5 = mature; 1 = nascent.

The matrix is intended for self-assessment and prioritization. If your feature falls in a category with score 2–3 on a dimension, expect to invest more in custom tooling.

> Last updated: 2026-05-02. PRs welcome with reasoning.

---

## Matrix

| Feature | Tools | Datasets | Failure modes | CI patterns | Prod observability | Total |
|---|---|---|---|---|---|---|
| **Chatbots** | 5 | 4 | 5 | 5 | 5 | **24/25** |
| **Classifiers** | 5 | 5 | 5 | 5 | 5 | **25/25** |
| **Translation** | 5 | 5 | 4 | 4 | 4 | **22/25** |
| **Voice (ASR)** | 5 | 5 | 4 | 4 | 4 | **22/25** |
| **RAG** | 4 | 4 | 5 | 4 | 4 | **21/25** |
| **Code-gen** | 4 | 5 | 4 | 4 | 4 | **21/25** |
| **Search & ranking** | 5 | 4 | 4 | 4 | 4 | **21/25** |
| **Summarizers** | 4 | 4 | 4 | 4 | 4 | **20/25** |
| **Voice (TTS)** | 4 | 4 | 3 | 3 | 3 | **17/25** |
| **Agents** | 3 | 3 | 4 | 3 | 3 | **16/25** |
| **Multimodal** | 4 | 4 | 3 | 3 | 3 | **17/25** |
| **Image-gen** | 3 | 3 | 4 | 2 | 2 | **14/25** |

---

## Discussion

**Most mature:** Classifiers and chatbots. 30 years of NLP tooling means classifier evaluation is a solved problem. Chatbots have benefited from the LLM ecosystem's investment in conversational eval.

**Mid-tier:** RAG, code-gen, search, summarizers. Tools and datasets are good but production observability + CI patterns lag.

**Least mature:** Image-gen and agents. For image-gen, evaluation tools are still primarily academic; production monitoring barely exists. For agents, the surface area of multi-step failure is too new for tools to have caught up.

---

## What "5" means per dimension

### Tools (5/5)

- Multiple production-grade OSS frameworks
- Integration with popular CI tools (GitHub Actions, GitLab CI)
- Active maintenance with releases in last 90 days

### Datasets (5/5)

- Multiple labeled benchmark datasets, open-licensed
- Covers diverse domains and demographics
- Continuously updated to avoid contamination

### Failure modes (5/5)

- Documented catalog with repros
- Common modes have associated test recipes
- Industry conferences track new modes

### CI patterns (5/5)

- Standard PR-block patterns documented
- Pre-commit hooks available
- Multiple tools have GitHub Action / equivalent

### Production observability (5/5)

- Multiple OSS observability tools
- Drift detection automated
- Cost / latency / quality dashboards available out of the box

---

## Self-assessment ladder (per feature)

This is the L0–L4 ladder reused on each feature page. Apply it to your team's status:

- **L0** — vibes / manual testing only
- **L1** — small offline test set; runs on demand
- **L2** — comprehensive offline rubric; runs in CI on PR; baseline locked in git
- **L3** — merge-gating bundle + cost / latency gates; rollback path drilled
- **L4** — continuous + drift detection + adversarial rotation + per-segment scoring

Most production AI features in 2026 sit at L2–L3. L4 is reserved for safety-critical or high-volume features where the investment is justified.

For a methodology to get from L0 → L3, see the [10 commandments](https://github.com/Aftabbs/claude-code-rules-for-ai-features) and the [adoption guide](https://github.com/Aftabbs/claude-code-rules-for-ai-features/blob/main/adoption.md).
