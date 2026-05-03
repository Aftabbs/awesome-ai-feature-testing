# 60-second starter snippets

One runnable starter per feature category. Each:

- Runs in <60 seconds with one API key
- Uses 5–10 cases (small but representative)
- Demonstrates 2–4 testing patterns from the feature page
- Has its own `README.md`

## Categories

- [chatbot/](chatbot/) — multi-turn persona stability + PII + length
- [rag/](rag/) — faithfulness + groundedness + empty-retrieval handling
- [summarizer/](summarizer/) — faithfulness + length + anti-padding
- [code-gen/](code-gen/) — compile + lint + test execution
- [image-gen/](image-gen/) — CLIP fidelity + NSFW
- [voice/](voice/) — WER on a small held-out audio set
- [agent/](agent/) — tool-call correctness + loop bound
- [multimodal/](multimodal/) — VQA accuracy + caption faithfulness
- [classifier/](classifier/) — F1 + calibration
- [translation/](translation/) — sacreBLEU + COMET
- [search/](search/) — NDCG@10 + recall@10

## Provider keys

Most snippets accept any of:

- `GROQ_API_KEY` (free, fast — recommended for first run)
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`

The README in each subdirectory tells you which.

## Re-using the snippet pattern

Each snippet is a starting point. To adapt for your own use:

1. Copy the directory
2. Replace the small dataset with your real one
3. Adjust thresholds in the bundle YAML
4. Wire into your CI

For the full discipline (specs, baselines, shadow-promotion, etc.), see [claude-code-rules-for-ai-features](https://github.com/Aftabbs/claude-code-rules-for-ai-features).
