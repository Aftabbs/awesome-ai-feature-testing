# Voice & speech (ASR / TTS)

Voice features split into two halves: speech-to-text (ASR / STT) and text-to-speech (TTS). Each has its own eval discipline. Voice agents (full conversational voice) layer on top of both.

This page covers: ASR/transcription, TTS, voice agents, audio classification, voice cloning.

---

## Testing patterns

### 1. ASR — Word Error Rate (WER)

**What it tests:** Fraction of words mis-transcribed.

**Tools:** [JiWER](https://github.com/jitsi/jiwer), [whisper-eval-kit](https://github.com/openai/whisper), [SpeechBrain](https://github.com/speechbrain/speechbrain).

**When to use:** Always for ASR. Stratify by accent, noise environment, domain.

**Cost / effort:** Low if you have ground-truth transcripts; medium to build them.

---

### 2. ASR — Character Error Rate / Locale-Aware

**What it tests:** WER over-penalizes minor differences in CJK/Arabic; CER is fairer for those locales.

**Tools:** JiWER (`jiwer.cer`), language-specific evaluators.

---

### 3. ASR — Domain & accent stratification

**What it tests:** WER on noisy industrial audio, accented English, code-switched speech.

**Tools:** [Common Voice](https://github.com/common-voice/common-voice), [VoxPopuli](https://github.com/facebookresearch/voxpopuli), [Edinburgh accent dataset](https://huggingface.co/datasets/edinburghcstr/ami).

**When to use:** Any production ASR. Stratification by demographic is a fairness floor.

---

### 4. TTS — Mean Opinion Score (MOS) / pseudo-MOS

**What it tests:** Subjective quality.

**Tools:** [UTMOS](https://github.com/sarulab-speech/UTMOS22), [SpeechMetrics](https://github.com/aliutkus/speechmetrics), [MOSNet](https://github.com/lochenchou/MOSNet).

---

### 5. TTS — Intelligibility (round-trip ASR)

**What it tests:** Run TTS output back through ASR; check if WER ≈ 0.

**Tools:** Any ASR + JiWER.

---

### 6. TTS — Pronunciation correctness

**What it tests:** Does the model pronounce difficult words / proper nouns correctly?

**Tools:** [eSpeak NG](https://github.com/espeak-ng/espeak-ng) for phoneme comparison; manual eval for proper nouns.

---

### 7. Voice — End-to-end intent capture

**What it tests:** From audio in to executed intent: did the right action happen?

**Tools:** Custom function checks against a labeled intent set.

---

### 8. Audio — PII redaction at transcription time

**What it tests:** Was PII in the audio redacted from the transcript before downstream use?

**Tools:** Microsoft Presidio over the transcript + pattern-based detectors.

---

### 9. Voice — Wakeword false-positive / false-negative

**What it tests:** Does the wakeword detector trigger when it should, and not when it shouldn't?

**Tools:** [Porcupine](https://github.com/Picovoice/porcupine), [openWakeWord](https://github.com/dscripka/openWakeWord).

---

## Recommended tools

### ASR-specific

- **[JiWER](https://github.com/jitsi/jiwer)** — WER / CER.
- **[whisper](https://github.com/openai/whisper)** — OpenAI's ASR with eval scripts.
- **[whisper.cpp](https://github.com/ggerganov/whisper.cpp)** — efficient implementation.
- **[Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)** — faster OSS port.
- **[NeMo](https://github.com/NVIDIA/NeMo)** — NVIDIA's speech / NLP toolkit.
- **[SpeechBrain](https://github.com/speechbrain/speechbrain)** — speech processing toolkit with many evaluators.
- **[ESPnet](https://github.com/espnet/espnet)** — end-to-end speech processing.
- **[asr-leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)** — HF benchmark.

### TTS-specific

- **[UTMOS](https://github.com/sarulab-speech/UTMOS22)** — predicted MOS.
- **[SpeechMetrics](https://github.com/aliutkus/speechmetrics)** — package wrapping many metrics.
- **[NISQA](https://github.com/gabrielmittag/NISQA)** — speech quality assessment.
- **[Coqui TTS](https://github.com/coqui-ai/TTS)** — TTS framework with eval support.
- **[XTTS](https://github.com/coqui-ai/TTS/blob/dev/TTS/tts/configs/xtts_config.py)** — voice cloning eval.

### Voice agent / end-to-end

- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — supports voice via custom function rules; pair with JiWER for WER.
- **[Picovoice tools](https://github.com/Picovoice)** — wakeword / on-device voice eval.

### PII for transcripts

- **[Microsoft Presidio](https://github.com/microsoft/presidio)** — works on transcripts; configure for the locale.
- **[pii-codex](https://github.com/EdyVision/pii-codex)** — PII detection toolkit.

### Datasets

- **[LibriSpeech](https://www.openslr.org/12/)** — read English speech.
- **[Common Voice](https://github.com/common-voice/common-voice)** — Mozilla's multilingual.
- **[VoxPopuli](https://github.com/facebookresearch/voxpopuli)** — multilingual EU parliament.
- **[GigaSpeech](https://github.com/SpeechColab/GigaSpeech)** — large-scale English.
- **[CHiME-7](https://www.chimechallenge.org/current/index)** — challenging real-world.
- **[AMI](https://huggingface.co/datasets/edinburghcstr/ami)** — meeting recordings.
- **[VocalSound](https://github.com/YuanGongND/vocalsound)** — non-speech vocal sounds.
- **[FLEURS](https://huggingface.co/datasets/google/fleurs)** — 102-language ASR.

---

## Sample evaluator (Python)

```python
import jiwer
from openai import OpenAI

client = OpenAI()

def transcribe_and_score(audio_path: str, gold_transcript: str) -> dict:
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(model="whisper-1", file=f)

    pred = result.text

    return {
        "audio": audio_path,
        "gold": gold_transcript,
        "pred": pred,
        "wer": jiwer.wer(gold_transcript, pred),
        "cer": jiwer.cer(gold_transcript, pred),
    }
```

---

## Failure-mode catalog (voice-specific)

See [FAILURE-MODES.md#voice](../FAILURE-MODES.md#voice).

- **Background voice misattribution.** Coworker speaks; ASR captures their words as the user's.
- **Echo / Bluetooth duplication.** "delete delete the the note."
- **Code-switch failure.** En/Es mid-sentence → ASR picks one and mis-transcribes the other.
- **Long-tail PII capture.** Account numbers / addresses in background speech end up in transcripts.
- **Wake-word over-trigger.** "Cleaner" or "computer" triggers Alexa; common in real homes.
- **TTS pronunciation of proper noun drift.** Brand name pronounced wrong; persists across versions.
- **Silence misinterpretation.** Pause in speech → ASR ends transcription early.
- **Numeric / date relative-resolution.** "Tomorrow" not bound to a date.

---

## Run this in 60 seconds

```bash
cd snippets/voice
export OPENAI_API_KEY=...

# Transcribe 5 audio samples and compute WER vs. gold
python evaluate.py
```

See [snippets/voice/](../snippets/voice/).

---

## Maturity ladder for voice testing

- **L0** — listen by ear.
- **L1** — WER on a small held-out set.
- **L2** — stratified WER (accent / domain / noise) + TTS MOS.
- **L3** — merge-gating bundle: WER + intelligibility + PII + intent-capture.
- **L4** — continuous production scoring + drift detection per ASR / TTS model.

L3 is the realistic bar for production voice agents; L2 for pure ASR / TTS shipping.

---

## See also

- [agents.md](agents.md) — for voice agents
- [chatbots.md](chatbots.md) — for the conversational layer
- [classifiers.md](classifiers.md) — for intent classification on transcripts
