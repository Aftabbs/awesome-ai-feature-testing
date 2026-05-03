# Classifiers & structured-output extractors

Classifiers and structured extractors are the underrated workhorses of AI features — sentiment classification, intent routing, entity extraction, JSON-output extractors. Their evals are the most rigorous in the AI feature space because outputs are structured and ground truth is feasible.

This page covers: text classification, intent routing, NER and entity extraction, structured-output (JSON) extractors, multi-label classification, calibration-sensitive classifiers.

---

## Testing patterns

### 1. Per-class accuracy / F1

**What it tests:** For each class, recall and precision against labeled ground truth.

**Tools:** sklearn (`classification_report`, `confusion_matrix`), [Evidently](https://github.com/evidentlyai/evidently).

**When to use:** Always.

---

### 2. Macro-F1 vs micro-F1

**What it tests:** Aggregate accuracy per-class (macro) vs overall (micro). Disagreement signals class imbalance.

**Tools:** sklearn (`f1_score(average='macro')`).

---

### 3. Calibration

**What it tests:** Are confidence scores actually calibrated? When the model says 90%, is it right 90% of the time?

**Tools:** [scikit-learn calibration_curve](https://scikit-learn.org/stable/modules/calibration.html), [netcal](https://github.com/EFS-OpenSource/calibration-framework).

**When to use:** Any classifier whose downstream uses confidence (e.g. "escalate when confidence <0.7").

---

### 4. Schema validity (for JSON extractors)

**What it tests:** Does the model output valid JSON conforming to a schema?

**Tools:** JSONSchema, Pydantic, BehaviorCI `must-be-json`, Promptfoo `is-json`.

---

### 5. Field-level accuracy (for structured extraction)

**What it tests:** For each field in the output schema, accuracy of the extracted value.

**Tools:** Custom Python checks per field type (string match, numeric match, date match within tolerance).

---

### 6. NER P/R/F1

**What it tests:** Named entity recognition: precision, recall, F1 per entity type.

**Tools:** [seqeval](https://github.com/chakki-works/seqeval), [SpaCy's evaluator](https://spacy.io/api/language#evaluate).

---

### 7. Locale parity

**What it tests:** Does the classifier perform equally across language / locale segments?

**Tools:** Stratified eval; per-locale F1 spread.

---

### 8. Latency at scale

**What it tests:** p95 latency under production load.

**Tools:** [k6](https://k6.io/), [locust](https://github.com/locustio/locust), [wrk2](https://github.com/giltene/wrk2).

---

### 9. Adversarial robustness

**What it tests:** Resistance to typos, paraphrases, encoding tricks, prompt injection.

**Tools:** [TextAttack](https://github.com/QData/TextAttack), [Garak](https://github.com/leondz/garak).

---

### 10. Concept drift detection

**What it tests:** Does production data distribution shift over time? Is the classifier still accurate against the new distribution?

**Tools:** [Evidently](https://github.com/evidentlyai/evidently), [Alibi Detect](https://github.com/SeldonIO/alibi-detect), [NannyML](https://github.com/NannyML/nannyml).

---

## Recommended tools

### Classification / NER eval

- **[scikit-learn](https://github.com/scikit-learn/scikit-learn)** — F1, calibration, confusion matrix.
- **[seqeval](https://github.com/chakki-works/seqeval)** — sequence labeling.
- **[netcal](https://github.com/EFS-OpenSource/calibration-framework)** — calibration metrics.
- **[Evidently](https://github.com/evidentlyai/evidently)** — drift + classification eval.
- **[Alibi Detect](https://github.com/SeldonIO/alibi-detect)** — drift / outlier detection.
- **[NannyML](https://github.com/NannyML/nannyml)** — production drift estimation.

### LLM classification (when LLMs do the classifying)

- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — schema-validating bundles.
- **[DeepEval](https://github.com/confident-ai/deepeval)** — `ClassificationMetric`.
- **[Promptfoo](https://github.com/promptfoo/promptfoo)** — assertion-based.
- **[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)** — research-grade.
- **[Giskard OSS](https://github.com/Giskard-AI/giskard-oss)** — bias / fairness for classifiers.

### Structured output / JSON

- **[Outlines](https://github.com/dottxt-ai/outlines)** — structured generation (constrained sampling).
- **[Instructor](https://github.com/jxnl/instructor)** — Pydantic-typed outputs.
- **[Marvin](https://github.com/PrefectHQ/marvin)** — LLM-as-function with typed outputs.

### Adversarial / robustness

- **[TextAttack](https://github.com/QData/TextAttack)** — adversarial attacks for NLP.
- **[Garak](https://github.com/leondz/garak)** — LLM vulnerability scanner.
- **[checklist](https://github.com/marcotcr/checklist)** — behavioral testing for NLP models.

### NER

- **[spaCy](https://github.com/explosion/spaCy)** — NER + eval.
- **[NER-Eval](https://github.com/davidsbatista/NER-Evaluation)** — entity-level evaluation.

### Datasets

- **[CoNLL-2003](https://huggingface.co/datasets/eriktks/conll2003)** — NER classic.
- **[CLINC150](https://github.com/clinc/oos-eval)** — intent classification with OOS detection.
- **[Banking77](https://huggingface.co/datasets/PolyAI/banking77)** — banking intent.
- **[GLUE](https://gluebenchmark.com/)** — general language understanding.
- **[SuperGLUE](https://super.gluebenchmark.com/)** — harder.
- **[XGLUE](https://github.com/microsoft/XGLUE)** — multilingual.

---

## Sample rubric (intent classifier)

```yaml
type: schema-rubric
exemption: schema-rubric

per-class-accuracy:
  by: queue
  classes:
    refund: { recall: 0.97, precision: 0.93, weight: 4 }
    churn-risk: { recall: 0.95, precision: 0.85, weight: 5 }
    # ... 12 more ...

calibration:
  metric: ECE
  target: <= 0.05
  weight: 2

invariants:
  - id: refund-mentioning-not-other
    type: function
    function: src.evals.checks.refund_force_route
    target: 1.00
    weight: 5

  - id: low-confidence-escalates
    type: function
    function: src.evals.checks.low_conf_escalates
    target: 1.00
    weight: 3

aggregate:
  scoring: macro-f1
  pass_threshold: 0.91

gates:
  latency_p95_max_absolute_ms: 200
```

See the [classifier cookbook](https://github.com/Aftabbs/claude-code-rules-for-ai-features/blob/main/cookbook/classifier-feature.md) for the full version.

---

## Failure-mode catalog (classifier-specific)

See [FAILURE-MODES.md#classifiers](../FAILURE-MODES.md#classifiers).

- **Calibration drift after data shift.** Headline accuracy stable, but ECE blew up.
- **Locale parity break.** Accuracy on Spanish dropped 8pp; English unchanged.
- **OOD over-confidence.** Out-of-distribution input still gets 90%+ confidence.
- **Multi-label leak.** Single-label classifier stops being single-label silently.
- **Refusal regression on lookalike phrases.** Slight paraphrase of a refused class is now accepted.
- **JSON schema drift.** Field rename in schema; model still outputs old field name.
- **Trailing-newline format break.** Output validates as JSON only after stripping.
- **Most-common-class fallback.** Classifier defaults to most-frequent class on uncertain input rather than escalating.
- **Threshold regression.** Confidence threshold for `escalate` was 0.7; new model's confidence distribution shifted, so 0.7 means something different.

---

## Run this in 60 seconds

```bash
cd snippets/classifier
export OPENAI_API_KEY=...

# 100-case intent classification with calibration check
python evaluate.py
```

See [snippets/classifier/](../snippets/classifier/).

---

## Maturity ladder for classifier testing

- **L0** — accuracy on a small held-out set.
- **L1** — per-class F1 + confusion matrix.
- **L2** — calibration (ECE) + per-class invariants.
- **L3** — merge-gating bundle + locale stratification + drift monitor.
- **L4** — continuous + adversarial robustness + concept-drift alerting.

L3 is the bar for production classifiers; calibration discipline is the dividing line.

---

## See also

- [chatbots.md](chatbots.md) — for upstream intent classification
- [agents.md](agents.md) — for tool selection (a classifier in disguise)
- [search.md](search.md) — for ranking-with-classification hybrids
