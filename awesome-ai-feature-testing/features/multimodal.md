# Multimodal & vision

Multimodal features (vision-LMs, audio-LMs, image+text) are scored across more dimensions than pure-text models. Eval discipline is younger than for text; expect more LLM-as-judge, more pairwise human preference, more domain-specific scorers.

This page covers: VQA, image captioning, document understanding, multimodal classification, vision agents, audio understanding.

---

## Testing patterns

### 1. Vision-text alignment

**What it tests:** Do generated captions / answers match the visual content?

**Tools:** [CLIPScore](https://github.com/jmhessel/clipscore), [BLIPScore](https://github.com/salesforce/BLIP), [VQAScore](https://github.com/linzhiqiu/CLIP-FlanT5), [VBench](https://github.com/Vchitect/VBench).

---

### 2. VQA accuracy

**What it tests:** Visual question answering against labeled ground truth.

**Tools:** [VQAv2](https://visualqa.org/), [GQA](https://cs.stanford.edu/people/dorarad/gqa/), [TextVQA](https://textvqa.org/), [DocVQA](https://www.docvqa.org/).

---

### 3. Document understanding

**What it tests:** Reading text in images (OCR + understanding), table extraction, form parsing.

**Tools:** [DocVQA](https://www.docvqa.org/), [InfographicVQA](https://www.docvqa.org/), [ChartQA](https://github.com/vis-nlp/ChartQA).

---

### 4. Counting & spatial reasoning

**What it tests:** "How many X are in this image?" "Is A to the left of B?"

**Tools:** [CountBench](https://github.com/teowu/Q-Bench), spatial-VQA datasets.

---

### 5. Hallucination on absent objects

**What it tests:** When asked "what color is the X?" and there's no X, does the model say so or invent?

**Tools:** [POPE](https://github.com/RUCAIBox/POPE), [HallusionBench](https://github.com/tianyi-lab/HallusionBench).

---

### 6. Cross-modal robustness

**What it tests:** Same question phrased differently → same answer. Same image rotated / cropped → same answer.

**Tools:** Adversarial VQA datasets, custom paraphrase / transform pipelines.

---

### 7. Bias / fairness across demographics

**What it tests:** Does the model perform equally well across demographic groups in images?

**Tools:** [FACET](https://github.com/facebookresearch/FACET), [VLBiasBench](https://github.com/jong-cs/VLBiasBench), Inclusion-aware datasets.

---

### 8. Audio-LM tasks

**What it tests:** Audio understanding (sound classification, audio captioning, music understanding).

**Tools:** [AudioCaps](https://github.com/cdjkim/audiocaps), [AudioBench](https://github.com/AudioLLMs/AudioBench).

---

## Recommended tools

### Multimodal eval frameworks

- **[OmniEvalKit](https://github.com/OpenBMB/OmniEvalKit)** — modular toolbox across modalities.
- **[GAGE](https://github.com/HiThink-Research/GAGE)** — unified eval for LLMs, MLLMs, audio, diffusion.
- **[VLMEvalKit](https://github.com/open-compass/VLMEvalKit)** — vision-LM benchmark suite.
- **[lmms-eval](https://github.com/EvolvingLMMs-Lab/lmms-eval)** — large-scale multimodal eval.
- **[Eureka ML Insights](https://github.com/microsoft/eureka-ml-insights)** — Microsoft framework for foundation models.
- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — supports multimodal via custom function rules.
- **[DeepEval](https://github.com/confident-ai/deepeval)** — multimodal metrics added 2025.
- **[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)** — multimodal-friendly.

### Vision-LM benchmarks

- **[MMBench](https://github.com/open-compass/MMBench)** — comprehensive VLM eval.
- **[MMMU](https://github.com/MMMU-Benchmark/MMMU)** — massive multi-discipline.
- **[SEED-Bench](https://github.com/AILab-CVC/SEED-Bench)** — generative comprehension.
- **[MathVista](https://github.com/lupantech/MathVista)** — math reasoning in visual contexts.
- **[OCRBench](https://github.com/Yuliang-Liu/MultimodalOCR)** — OCR-heavy tasks.
- **[ScienceQA](https://github.com/lupantech/ScienceQA)** — science QA with images.
- **[POPE](https://github.com/RUCAIBox/POPE)** — object hallucination.
- **[HallusionBench](https://github.com/tianyi-lab/HallusionBench)** — visual hallucination.

### Document understanding

- **[DocVQA](https://www.docvqa.org/)**, **[InfographicVQA](https://www.docvqa.org/)**, **[ChartQA](https://github.com/vis-nlp/ChartQA)** — document benchmarks.
- **[Donut](https://github.com/clovaai/donut)** — OCR-free doc understanding.

### Audio-LM

- **[AudioCaps](https://github.com/cdjkim/audiocaps)** — audio captioning.
- **[AudioBench](https://github.com/AudioLLMs/AudioBench)** — comprehensive audio-LM eval.
- **[Dynamic-SUPERB](https://github.com/dynamic-superb/dynamic-superb)** — speech understanding.

### Vision encoders / metrics

- **[CLIP](https://github.com/openai/CLIP)**, **[OpenCLIP](https://github.com/mlfoundations/open_clip)**, **[SigLIP](https://huggingface.co/google/siglip-so400m-patch14-384)** — vision-text alignment.
- **[DINOv2](https://github.com/facebookresearch/dinov2)** — vision foundation.
- **[DreamSim](https://github.com/ssundaram21/dreamsim)** — perceptual similarity.

### Bias / fairness

- **[FACET](https://github.com/facebookresearch/FACET)** — image classification fairness.
- **[VLBiasBench](https://github.com/jong-cs/VLBiasBench)** — VL bias eval.

---

## Failure-mode catalog (multimodal-specific)

See [FAILURE-MODES.md#multimodal](../FAILURE-MODES.md#multimodal).

- **Object hallucination.** Model claims to see things not in the image.
- **Counting failure.** "How many people?" → off-by-N.
- **Text-in-image hallucination.** Model invents text it "sees" in image.
- **Spatial inversion.** Left/right confusion.
- **Color drift.** Model claims a wrong color confidently.
- **Aspect-ratio sensitivity.** Same image, cropped differently → different answer.
- **Diagram-vs-photograph confusion.** Model misclassifies UI screenshots as photos and vice versa.

---

## Run this in 60 seconds

```bash
cd snippets/multimodal
export OPENAI_API_KEY=...

python evaluate.py
```

The snippet runs a 5-case VQA + caption faithfulness check using a small VLM. See [snippets/multimodal/](../snippets/multimodal/).

---

## Maturity ladder for multimodal testing

- **L0** — vibes.
- **L1** — VQA accuracy on a small held-out set.
- **L2** — multi-dimensional eval: alignment + hallucination + spatial.
- **L3** — merge-gating bundle: above + cost + latency + bias.
- **L4** — continuous + drift detection + adversarial paraphrase coverage.

L2 is most production multimodal teams' bar; L3 is rare.

---

## See also

- [image-gen.md](image-gen.md) — text-to-image (the inverse direction)
- [classifiers.md](classifiers.md) — for image classification
- [voice.md](voice.md) — for audio-language
