# Image & video generation

Image and video generation features (text-to-image, image-to-image, video) are unique among AI features: outputs are difficult to score deterministically, judges are immature compared to text, and human preference dominates the eval.

This page covers: text-to-image, image editing, image variation, text-to-video, video editing.

---

## Testing patterns

### 1. Prompt fidelity

**What it tests:** Does the output match the prompt's described content?

**Tools:** [VBench](https://github.com/Vchitect/VBench) (video), [T2I-CompBench](https://github.com/Karine-Huang/T2I-CompBench), [GenAI-Bench](https://github.com/linzhiqiu/genai-bench), [PaintsKill](https://github.com/Pix2Pixs/PaintsKill).

**When to use:** Always.

**Cost / effort:** Medium-high. Most fidelity scorers use vision-LM judges.

---

### 2. Compositional accuracy

**What it tests:** Multi-object prompts ("a red ball next to a blue cube on a table"). Counts. Spatial relationships.

**Tools:** [T2I-CompBench](https://github.com/Karine-Huang/T2I-CompBench), [DSG](https://github.com/j-min/DSG) (Davidsonian Scene Graph), CLIP-based scorers.

---

### 3. Aesthetic / quality scoring

**What it tests:** Sharpness, lighting, composition, "quality."

**Tools:** [LAION aesthetic predictor](https://github.com/LAION-AI/aesthetic-predictor), [HPSv2](https://github.com/tgxs002/HPSv2), [PickScore](https://github.com/yuvalkirstain/PickScore).

---

### 4. Safety / NSFW classification

**What it tests:** Output not unintentionally NSFW, violent, or unsafe.

**Tools:** [NudeNet](https://github.com/notAI-tech/NudeNet), [stable-diffusion safety checker](https://github.com/CompVis/stable-diffusion/blob/main/scripts/safety/checker.py), commercial moderation APIs.

**When to use:** Always for any user-facing image-gen.

---

### 5. Style consistency

**What it tests:** When generating multiple images for the same brand / character, do they look like the same brand / character?

**Tools:** Image embedding similarity (CLIP, DINO), face/character recognition models, [DreamSim](https://github.com/ssundaram21/dreamsim).

---

### 6. Identity / face consistency

**What it tests:** Same person across many images.

**Tools:** [InsightFace](https://github.com/deepinsight/insightface), [ArcFace](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch).

---

### 7. Hallucinated text in image

**What it tests:** Does the generated image contain garbled text (the classic stable-diffusion failure)?

**Tools:** OCR (Tesseract, EasyOCR) + a check that any text in the image is intentional and correct.

---

### 8. Diversity / mode coverage

**What it tests:** Across many prompts of the same category, are outputs diverse or all same-mode?

**Tools:** Image embedding distance distributions, FID-style metrics.

---

## Recommended tools

### Image-gen specific eval

- **[VBench](https://github.com/Vchitect/VBench)** — comprehensive video generation eval (16 dimensions).
- **[T2I-CompBench](https://github.com/Karine-Huang/T2I-CompBench)** — compositionality.
- **[GenAI-Bench](https://github.com/linzhiqiu/genai-bench)** — compositional T2I.
- **[HPSv2](https://github.com/tgxs002/HPSv2)** — Human Preference Score v2.
- **[PickScore](https://github.com/yuvalkirstain/PickScore)** — preference scoring.
- **[ImageReward](https://github.com/THUDM/ImageReward)** — preference scorer trained on human ratings.
- **[DSG](https://github.com/j-min/DSG)** — Davidsonian scene graph for fine-grained T2I eval.
- **[VQAScore](https://github.com/linzhiqiu/CLIP-FlanT5)** — VQA-based T2I alignment.
- **[VPEval](https://github.com/aliasvishnu/VPEval)** — programmatic T2I eval.

### Quality metrics

- **[FID](https://github.com/mseitzer/pytorch-fid)** — Fréchet Inception Distance.
- **[CLIP-FID](https://github.com/kynkaat/role-of-imagenet)**, **[CMMD](https://github.com/sayakpaul/cmmd-pytorch)** — improvements on FID.
- **[InceptionV3](https://github.com/keras-team/keras-applications)** — for IS.

### Embedding models

- **[CLIP](https://github.com/openai/CLIP)** — OpenAI.
- **[OpenCLIP](https://github.com/mlfoundations/open_clip)** — open implementations.
- **[DINOv2](https://github.com/facebookresearch/dinov2)** — Meta's vision foundation model.
- **[SigLIP](https://huggingface.co/google/siglip-so400m-patch14-384)** — Google's improvement.

### Identity / face

- **[InsightFace](https://github.com/deepinsight/insightface)** — face recognition.
- **[DeepFace](https://github.com/serengil/deepface)** — wraps multiple backends.

### Safety / NSFW

- **[NudeNet](https://github.com/notAI-tech/NudeNet)** — NSFW classifier.
- **[Stable Diffusion safety checker](https://github.com/CompVis/stable-diffusion)** — original.
- **[falconsai/nsfw-image-detection](https://huggingface.co/Falconsai/nsfw_image_detection)** — small CNN.

### General LLM eval frameworks (with multimodal)

- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — supports image outputs via custom function rules.
- **[DeepEval](https://github.com/confident-ai/deepeval)** — multimodal metrics.
- **[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)** — multimodal-friendly.
- **[OmniEvalKit](https://github.com/OpenBMB/OmniEvalKit)** — modular toolbox across modalities.
- **[GAGE](https://github.com/HiThink-Research/GAGE)** — unified eval engine for diffusion models.

### Datasets / benchmarks

- **[GenEval](https://github.com/djghosh13/geneval)** — object-focused T2I eval.
- **[PartiPrompts](https://github.com/google-research/parti)** — challenging prompts.
- **[DrawBench](https://imagen.research.google/)** — Google's benchmark prompts.
- **[Pick-a-Pic](https://huggingface.co/datasets/yuvalkirstain/pickapic_v2)** — preference dataset.

### Observability

- **[Phoenix](https://github.com/Arize-ai/phoenix)** — supports multimodal traces.
- **[Langfuse](https://github.com/langfuse/langfuse)** — works with image outputs as base64 / URLs.

---

## Sample fidelity-judge prompt

```markdown
You are a vision-LM evaluator. Score from 0-100 how well the generated image
matches the textual prompt.

Specifically rate:
- All described objects are present (40 points)
- Counts are correct (20 points)
- Spatial relationships are correct (20 points)
- Colors and attributes are correct (20 points)

Output JSON:
{
  "score": <0-100>,
  "objects_present": [...],
  "objects_missing": [...],
  "spatial_correct": <bool>,
  "attributes_correct": <bool>,
  "rationale": "<one sentence>"
}

Prompt: {{prompt}}
Image: <attached>
```

---

## Failure-mode catalog (image-gen-specific)

See [FAILURE-MODES.md#image-gen](../FAILURE-MODES.md#image-gen).

- **Garbled text in image.** Words rendered as gibberish.
- **Mangled hands / fingers.** Classic anatomical mismatch.
- **Compositional mismatch.** "Two cats and a dog" → image has 1 cat 2 dogs.
- **Spatial inversion.** "Red ball above blue cube" → blue cube above red ball.
- **Style bleed-through.** Persistent style from training data leaking into outputs even when not requested.
- **Identity drift.** Same person prompt → different faces across batch.
- **NSFW slip on innocuous prompts.** Triggered by specific token combinations.
- **Watermark hallucination.** Model invents watermark text from training data.

---

## Run this in 60 seconds

```bash
cd snippets/image-gen
export OPENAI_API_KEY=...   # for DALL-E or compatible

python evaluate.py
```

The snippet generates 5 images from a small prompt set and runs a CLIP-based fidelity check + an NSFW classifier. See [snippets/image-gen/](../snippets/image-gen/).

---

## Maturity ladder for image-gen testing

- **L0** — vibes ("looks cool").
- **L1** — manual rating spreadsheet.
- **L2** — automated CLIP / FID / preference-score eval against a small prompt set.
- **L3** — merge-gating bundle: fidelity + safety + style consistency + cost / latency.
- **L4** — continuous + human-in-the-loop preference + per-version drift on PartiPrompts-style holdouts.

L3 is the realistic bar; L4 typically only at consumer-scale image-gen platforms.

---

## See also

- [multimodal.md](multimodal.md) — image+text understanding (the inverse direction)
- [code-gen.md](code-gen.md) — for code that uses image-gen APIs
