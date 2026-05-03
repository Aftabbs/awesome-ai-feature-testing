# Tool fit matrix — which tool fits which feature

Most teams pick an eval tool first and bend it to fit their feature. The smarter move is the reverse: identify the feature, identify what testing patterns it needs, and pick the tool whose strengths match.

This matrix gives a quick "good fit / OK fit / poor fit" score per (tool × feature) pair. Use it as a starting point; your stack constraints (Python vs. TS, hosted vs. self-hosted, etc.) will narrow further.

> Last updated: 2026-05-02. Feedback welcome.

---

## Reading the table

- **Good fit** — the tool's strengths align with the feature's primary testing patterns; minimal custom code needed.
- **OK fit** — usable, but you'll write more glue.
- **Poor fit** — the tool can technically handle the feature, but you'll fight it.

A "—" means the tool isn't designed for that feature category and we don't recommend forcing it.

---

## Matrix

| Tool | Chatbot | RAG | Summarizer | Code-gen | Image-gen | Voice | Agent | Multimodal | Classifier | Translation | Search |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** | Good | Good | Good | Good | OK | OK | OK | OK | Good | Good | OK |
| **[DeepEval](https://github.com/confident-ai/deepeval)** | Good | Good | Good | Good | OK | — | OK | OK | Good | Good | OK |
| **[Promptfoo](https://github.com/promptfoo/promptfoo)** | Good | Good | Good | Good | OK | — | OK | OK | Good | OK | OK |
| **[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)** | Good | Good | Good | Good | OK | OK | Good | Good | Good | Good | OK |
| **[OpenEvals](https://github.com/langchain-ai/openevals)** | Good | Good | Good | OK | — | — | OK | OK | Good | OK | OK |
| **[RAGAS](https://github.com/explodinggradients/ragas)** | OK | Good | OK | — | — | — | OK | — | — | — | Good |
| **[trulens](https://github.com/truera/trulens)** | OK | Good | OK | — | — | — | OK | — | — | — | OK |
| **[Phoenix](https://github.com/Arize-ai/phoenix)** | Good | Good | Good | Good | OK | OK | Good | Good | Good | Good | Good |
| **[Langfuse](https://github.com/langfuse/langfuse)** | Good | Good | Good | Good | OK | OK | Good | Good | Good | Good | Good |
| **[Opik](https://github.com/comet-ml/opik)** | Good | Good | Good | Good | OK | OK | Good | Good | Good | Good | Good |
| **[Helicone](https://github.com/Helicone/helicone)** | Good | Good | Good | Good | OK | OK | Good | Good | Good | Good | Good |
| **[Evidently](https://github.com/evidentlyai/evidently)** | Good | OK | Good | OK | — | — | OK | OK | Good | OK | OK |
| **[Garak](https://github.com/leondz/garak)** | Good | OK | OK | OK | — | — | Good | OK | OK | OK | OK |
| **[PyRIT](https://github.com/Azure/PyRIT)** | Good | OK | OK | OK | — | — | Good | OK | OK | OK | OK |
| **[continuous-eval](https://github.com/relari-ai/continuous-eval)** | Good | Good | Good | OK | — | — | OK | OK | Good | OK | OK |
| **[Giskard OSS](https://github.com/Giskard-AI/giskard-oss)** | Good | OK | Good | OK | — | — | OK | OK | Good | OK | — |
| **[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)** | OK | OK | Good | Good | — | — | OK | OK | Good | Good | OK |
| **[OLMES](https://github.com/allenai/olmes)** | OK | OK | Good | Good | — | — | OK | OK | Good | Good | OK |
| **[OpenCompass](https://github.com/open-compass/opencompass)** | OK | OK | Good | Good | — | — | OK | Good | Good | Good | OK |
| **[VBench](https://github.com/Vchitect/VBench)** | — | — | — | — | Good | — | — | OK | — | — | — |
| **[T2I-CompBench](https://github.com/Karine-Huang/T2I-CompBench)** | — | — | — | — | Good | — | — | OK | — | — | — |
| **[VLMEvalKit](https://github.com/open-compass/VLMEvalKit)** | — | — | — | — | OK | — | OK | Good | — | — | — |
| **[lmms-eval](https://github.com/EvolvingLMMs-Lab/lmms-eval)** | — | — | — | — | OK | — | OK | Good | — | — | — |
| **[JiWER](https://github.com/jitsi/jiwer)** | — | — | — | — | — | Good | — | — | — | — | — |
| **[BFCL](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)** | — | — | — | OK | — | — | Good | — | — | — | — |
| **[AgentBench](https://github.com/THUDM/AgentBench)** | — | — | — | OK | — | — | Good | — | — | — | — |
| **[GAIA](https://huggingface.co/datasets/gaia-benchmark/GAIA)** | — | — | — | — | — | — | Good | — | — | — | — |
| **[WebArena](https://github.com/web-arena-x/webarena)** | — | — | — | — | — | — | Good | — | — | — | — |
| **[SWE-Bench](https://github.com/princeton-nlp/SWE-bench)** | — | — | — | Good | — | — | Good | — | — | — | — |
| **[BEIR](https://github.com/beir-cellar/beir)** | — | OK | — | — | — | — | — | — | — | — | Good |
| **[MTEB](https://github.com/embeddings-benchmark/mteb)** | — | OK | — | — | — | — | — | OK | — | — | Good |
| **[sacreBLEU](https://github.com/mjpost/sacrebleu)** | — | — | OK | — | — | — | — | — | — | Good | — |
| **[COMET](https://github.com/Unbabel/COMET)** | — | — | OK | — | — | — | — | — | — | Good | — |

---

## How to use this

1. Identify your feature category (left columns of the matrix on each feature page).
2. Pick 2–3 "Good fit" tools.
3. Read each tool's README; pick the one whose distribution model matches your stack (CLI vs library vs hosted).
4. Build a 60-second starter (we have one per category at [`snippets/`](snippets/)).
5. Re-evaluate after one quarter.

---

## What's missing

This matrix doesn't capture:

- **License compatibility.** Some tools are AGPL or commercial-restricted.
- **Stack fit.** TypeScript shops will prefer Promptfoo / Evalite over Python-only tools.
- **Hosted vs self-hosted.** Phoenix/Langfuse/Opik all have hosted offerings; some teams must self-host.
- **Multi-tool stacks.** Many production teams use 2–3 tools for different layers (e.g. BehaviorCI for merge gates + Phoenix for production traces).

---

## Contributing

PRs welcome to:

- Add new tools (with good/OK/poor scores per feature)
- Update scores when a tool gets meaningfully better or worse for a given feature
- Add comments / footnotes for "OK fit, but only with caveat X"

The bar: any score change comes with one paragraph of reasoning.
