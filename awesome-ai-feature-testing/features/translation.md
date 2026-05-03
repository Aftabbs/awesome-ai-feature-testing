# Translation & localization

Translation features are deceptively well-studied — academic MT eval has 30 years of methodology. Production AI translation is younger. The gap is in style, idiom, and domain-specific terminology.

This page covers: machine translation, document translation, real-time translation, localization (UI strings + context), translation memory.

---

## Testing patterns

### 1. BLEU / chrF / METEOR

**What it tests:** Surface overlap between translation and reference.

**Tools:** [sacreBLEU](https://github.com/mjpost/sacrebleu), [chrF](https://github.com/m-popovic/chrF), [METEOR](https://github.com/cmu-mtlab/meteor).

**When to use:** Always as a baseline; never as the only signal.

**Common pitfalls:**
- BLEU is famously bad at fluent paraphrases.
- Multi-reference is required for stable BLEU.

---

### 2. COMET / BLEURT

**What it tests:** Learned-metric translation quality (closer to human judgment than BLEU).

**Tools:** [COMET](https://github.com/Unbabel/COMET), [BLEURT](https://github.com/google-research/bleurt).

---

### 3. xCOMET / fine-grained error spans

**What it tests:** Where in the translation are the errors and what type (mistranslation, omission, addition)?

**Tools:** [xCOMET](https://github.com/Unbabel/COMET), [MQM (Multidimensional Quality Metrics)](https://themqm.org/) — schema for human / model error annotation.

---

### 4. Terminology consistency

**What it tests:** When the source uses domain-specific terms (product names, brand names), does the translation preserve them or use the right localized variant?

**Tools:** Custom function check against a glossary; [Trados / MemoQ TM tools](https://www.trados.com/) for the production side.

---

### 5. Style / register preservation

**What it tests:** Formal source → formal target. Casual source → casual target.

**Tools:** llm-behave (tone), DeepEval `GEval`, custom register classifiers.

---

### 6. PII redaction across translation

**What it tests:** Translation is faithful but: are PII tokens preserved (not "translated" into a fake target name)?

**Tools:** Microsoft Presidio + post-translation re-check that PII tokens still match.

---

### 7. Round-trip stability

**What it tests:** Translate to target, translate back to source. How close is the back-translation?

**Tools:** Any MT system + similarity metric (BLEU, BERTScore).

---

### 8. Domain-specific accuracy (legal, medical, financial)

**What it tests:** In specialized domains, is terminology correctly translated?

**Tools:** [Medical MT benchmarks](https://github.com/aizutour/medical-mt), [Legal MT eval datasets](https://huggingface.co/datasets/joelniklaus/lextreme).

---

## Recommended tools

### MT-specific eval

- **[sacreBLEU](https://github.com/mjpost/sacrebleu)** — reproducible BLEU.
- **[COMET](https://github.com/Unbabel/COMET)** — learned MT metric.
- **[BLEURT](https://github.com/google-research/bleurt)** — Google's learned metric.
- **[xCOMET](https://github.com/Unbabel/COMET)** — fine-grained spans.
- **[chrF](https://github.com/m-popovic/chrF)** — character F-score.
- **[MetricsForMT](https://github.com/EdinburghNLP/MetricsForMT)** — collection.
- **[NLLB Toolkit](https://github.com/facebookresearch/fairseq/tree/nllb)** — Meta's MT framework with eval.
- **[MQM](https://themqm.org/)** — error annotation schema.

### LLM eval w/ translation support

- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — supports translation rubrics.
- **[DeepEval](https://github.com/confident-ai/deepeval)** — has translation-quality metrics.
- **[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)** — flexible.
- **[Promptfoo](https://github.com/promptfoo/promptfoo)** — assertions for translation.

### Glossary / terminology management

- **[Trados Studio TM](https://www.trados.com/)** — proprietary; the standard.
- **[OmegaT](https://omegat.org/)** — open-source CAT tool.

### Datasets

- **[FLORES-200](https://github.com/facebookresearch/flores)** — 200-language multi-parallel.
- **[WMT shared task](https://www.statmt.org/wmt23/)** — yearly benchmarks.
- **[OPUS](https://opus.nlpl.eu/)** — large multilingual corpus collection.
- **[Tatoeba](https://github.com/Helsinki-NLP/Tatoeba-Challenge)** — multilingual sentence pairs.
- **[CoVoST](https://github.com/facebookresearch/covost)** — speech-to-text translation.
- **[ParaCrawl](https://www.paracrawl.eu/)** — web-crawled parallel data.

---

## Sample evaluator

```python
import sacrebleu
from comet import download_model, load_from_checkpoint

bleu_scorer = sacrebleu.BLEU()
comet_model = load_from_checkpoint(download_model("Unbabel/wmt22-comet-da"))

def score_translation(src, hyp, ref):
    bleu = bleu_scorer.corpus_score([hyp], [[ref]]).score
    comet = comet_model.predict([{"src": src, "mt": hyp, "ref": ref}], batch_size=1)["scores"][0]
    return {"bleu": bleu, "comet": comet}
```

---

## Failure-mode catalog (translation-specific)

See [FAILURE-MODES.md#translation](../FAILURE-MODES.md#translation).

- **Brand-name translation.** Product/brand names get "translated" into target-language equivalents.
- **Terminology drift.** Domain-specific terms picking colloquial translations rather than the official localized term.
- **Register mismatch.** Casual source → overly formal target (or vice versa).
- **Over-translation.** Idiom literally translated; meaning lost.
- **Under-translation.** Important content silently dropped.
- **PII translated.** Names, addresses, phone numbers translated into target-region equivalents.

---

## Run this in 60 seconds

```bash
cd snippets/translation
export OPENAI_API_KEY=...

# Translate a 10-pair set; compute BLEU + COMET
python evaluate.py
```

See [snippets/translation/](../snippets/translation/).

---

## Maturity ladder for translation testing

- **L0** — eyeball.
- **L1** — sacreBLEU on a held-out set.
- **L2** — sacreBLEU + COMET + terminology check.
- **L3** — merge-gating bundle: above + register + domain coverage + cost / latency.
- **L4** — continuous + xCOMET fine-grained errors + concept drift on terminology.

L2 is bar; L3 is rare except in localization-as-a-service vendors.

---

## See also

- [summarizers.md](summarizers.md) — for cross-lingual summarization
- [voice.md](voice.md) — for speech-to-speech translation
- [chatbots.md](chatbots.md) — for multilingual conversational agents
