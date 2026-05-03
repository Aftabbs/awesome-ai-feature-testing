# Summarizers & rewriters

Summarizers look easy to test ("does the summary read well?") and fail in subtle ways. The hardest failures are not noticed for weeks because the summary "reads fine."

This page covers any feature that takes content in and produces a shorter / restructured version: meeting notes, document summary, email rewrite, content shortening, style transfer.

---

## Testing patterns

### 1. Faithfulness (no hallucinated facts)

**What it tests:** Every numeric claim, name, date, or quote in the summary has support in the source.

**Tools:** [FActScore](https://github.com/shmsw25/FActScore), [SummEval](https://github.com/Yale-LILY/SummEval), DeepEval (`FaithfulnessMetric`), RAGAS (faithfulness scorer).

**When to use:** Always.

**Cost / effort:** Medium. Atomic-fact-decomposition (FActScore approach) is more reliable but more expensive than holistic LLM-as-judge.

---

### 2. Coverage (no important info dropped)

**What it tests:** Does the summary cover the key points (or stated key points) of the source?

**Tools:** [SumEval](https://github.com/chakki-works/sumeval), [BERTScore](https://github.com/Tiiiger/bert_score), pairwise reference judging (when you have a gold summary).

**When to use:** When the spec lists "key points to preserve" — common for meeting notes, exec briefs.

---

### 3. Length compliance

**What it tests:** Does the summary stay within the configured length cap?

**Tools:** Trivial — word counts, character counts, sentence counts. BehaviorCI `max-length` rule, Promptfoo regex assertions.

**When to use:** Any length-bounded feature.

---

### 4. Action-item integrity (for action-extracting summarizers)

**What it tests:** For meeting summarizers etc.: every action item has a real owner, real due date, and a verbatim source quote.

**Tools:** Custom function checks. See [chatbot cookbook](https://github.com/Aftabbs/claude-code-rules-for-ai-features/blob/main/cookbook/summarizer-feature.md).

**When to use:** Any summarizer that extracts structured action items.

---

### 5. Style / tone preservation

**What it tests:** When rewriting, does the output preserve the input's intended tone?

**Tools:** llm-behave (tone detection), DeepEval `GEval` with style criteria, Promptfoo with custom semantic.

**When to use:** Email rewriters, tone-shifting tools, brand-voice rewriters.

---

### 6. Anti-padding

**What it tests:** Does the summarizer pad with generic filler ("This was a productive meeting", "Several key points were discussed") instead of content?

**Tools:** Regex-based `must-not-contain` rules + an LLM-as-judge "is this filler" check.

**When to use:** Any summarizer where filler degrades trust.

---

### 7. Source-attribution preservation

**What it tests:** When the source has multiple speakers / authors, does the summary preserve who said what?

**Tools:** Custom function (NER + alignment), DeepEval semantic check.

**When to use:** Meeting summarizers, multi-author doc summarizers.

---

### 8. PII redaction in output

**What it tests:** Does the summary leak PII the source contained?

**Tools:** Microsoft Presidio, BehaviorCI `no-pii` rule.

**When to use:** Always when summarizing user-written content.

---

### 9. Translation drift (if multilingual)

**What it tests:** When summarizing across languages, does the meaning change?

**Tools:** Round-trip translation (translate, summarize, back-translate) + similarity metrics.

**When to use:** Any cross-lingual summarizer.

---

## Recommended tools

### Summarization-specific eval

- **[SumEval](https://github.com/chakki-works/sumeval)** — multilingual summarization eval (ROUGE, BLEU, METEOR, CIDEr).
- **[SummEval](https://github.com/Yale-LILY/SummEval)** — Yale's framework, includes coherence, consistency, fluency, relevance.
- **[FActScore](https://github.com/shmsw25/FActScore)** — atomic-fact factuality.
- **[QAGS](https://github.com/W4ngatang/qags)** — question-answering-based factuality.
- **[FRANK](https://github.com/artidoro/frank)** — factuality typology.

### General LLM eval w/ summarization support

- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — rule + semantic; built-in length / regex / no-pii.
- **[DeepEval](https://github.com/confident-ai/deepeval)** — `FaithfulnessMetric`, `SummarizationMetric`.
- **[Promptfoo](https://github.com/promptfoo/promptfoo)** — assertion-based.
- **[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)** — research-grade.
- **[continuous-eval](https://github.com/relari-ai/continuous-eval)** — strong on faithfulness.
- **[trulens](https://github.com/truera/trulens)** — feedback functions.

### Embedding-based metrics

- **[BERTScore](https://github.com/Tiiiger/bert_score)** — semantic similarity.
- **[BLEURT](https://github.com/google-research/bleurt)** — learned metric for generation quality.
- **[MoverScore](https://github.com/AIPHES/emnlp19-moverscore)** — earth-mover's distance over embeddings.

### Datasets

- **[CNN/DailyMail](https://huggingface.co/datasets/cnn_dailymail)** — classic.
- **[XSum](https://huggingface.co/datasets/EdinburghNLP/xsum)** — extreme summarization.
- **[SAMSum](https://huggingface.co/datasets/Samsung/samsum)** — dialogue summarization.
- **[Multi-News](https://huggingface.co/datasets/alexfabbri/multi_news)** — multi-document summarization.
- **[ScisummNet](https://huggingface.co/datasets/yale-nlp/SciSummNet)** — scientific paper summaries.

---

## Sample prompts

### A summarizer with a strong anti-padding clause

```markdown
Summarize the following text in ≤120 words. The summary MUST:
- Open with a single declarative sentence stating the most important point.
- Use specifics (numbers, names, dates) from the source — not paraphrases like "many users."
- Quote the source verbatim when stating someone's opinion.

The summary MUST NOT:
- Use phrases like "the discussion was productive", "several points were raised",
  "the team explored options". Describe content, not metadiscussion.
- Include facts not present in the source.
- Use exclamation marks.
```

### Faithfulness judge prompt

```markdown
You are evaluating a summary against its source for faithfulness.

For each factual claim in the summary, mark FAITHFUL if the source supports it, or
UNFAITHFUL if the source contradicts or omits it.

Output JSON:
{
  "claims": [
    {"claim": "...", "verdict": "FAITHFUL" | "UNFAITHFUL", "source_evidence": "..." | null}
  ],
  "score": <fraction faithful>
}

Source:
{{source}}

Summary:
{{summary}}
```

---

## Failure-mode catalog (summarizer-specific)

See [FAILURE-MODES.md#summarizers](../FAILURE-MODES.md#summarizers).

- **Hallucinated number.** Source says ~$2M; summary says exactly $2.0M.
- **Owner-defaulted-to-organizer.** Action item without explicit owner attributed to meeting organizer.
- **Generic-framing fallback.** "The meeting was productive."
- **Source-quote drift.** Quoted text differs from the source.
- **Action-item invention.** No one assigned action; summary lists one anyway.
- **Speaker attribution swap.** Alice said X, summary attributes to Bob.
- **Date relative-resolution failure.** "Tomorrow" not resolved to a date.
- **Coverage collapse.** 30-page input → 3-line summary that misses 4 of 5 main points.

---

## Run this in 60 seconds

```bash
cd snippets/summarizer
export OPENAI_API_KEY=...

# Run a 10-case bundle: faithfulness + length + anti-padding
npx behaviourci test
```

See [snippets/summarizer/](../snippets/summarizer/).

---

## Maturity ladder for summarizer testing

- **L0** — vibes ("reads fine").
- **L1** — length + ROUGE / BERTScore against a reference set.
- **L2** — faithfulness rubric (LLM-as-judge or atomic-fact decomposition) + anti-padding rules.
- **L3** — merge-gating bundle with all of the above + cost / latency gates.
- **L4** — continuous production scoring with FActScore-style atomic decomposition.

---

## See also

- [chatbots.md](chatbots.md)
- [code-gen.md](code-gen.md)
- [translation.md](translation.md) — for cross-lingual summarization
