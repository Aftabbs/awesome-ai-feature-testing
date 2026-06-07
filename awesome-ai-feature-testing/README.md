# Awesome AI Feature Testing [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
 
> Testing patterns, tools, prompts, and eval examples — organized by AI feature, not by tool category. 

[![License: CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Refresh: weekly](https://img.shields.io/badge/Refresh-weekly-blue)](.github/workflows/refresh.yml)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Most "awesome AI eval" lists are organized by **tool**: here are 80 evaluation libraries, pick one. That's the wrong question. The right question is: **I'm building a chatbot — what do I test, how, with what?**

This list answers that question. Eleven categories, each with: testing patterns, recommended tools, sample prompts and golden datasets, eval rubrics, and a failure-mode catalog.

If you ship AI features, this is your starting page.

---

## Contents

### By feature

- [Chatbots & conversational agents](features/chatbots.md)
- [RAG & grounded QA](features/rag.md)
- [Summarizers & rewriters](features/summarizers.md)
- [Code generation & code review](features/code-gen.md)
- [Image & video generation](features/image-gen.md)
- [Voice & speech (ASR/TTS)](features/voice.md)
- [Agents & tool-use](features/agents.md)
- [Multimodal & vision](features/multimodal.md)
- [Classifiers & structured-output extractors](features/classifiers.md)
- [Translation & localization](features/translation.md)
- [Search & ranking](features/search.md)

### Cross-cutting

- [Maturity matrix — how solved is testing in each category](MATURITY.md)
- [Failure-mode catalog — 88+ documented failure modes](FAILURE-MODES.md)
- [Tool fit matrix — which tool fits which feature](TOOL-FIT.md)
- [Machine-readable index — `data/tools.csv`, `data/patterns.yaml`](data/)
- [Runnable 60-second starters — one per feature](snippets/)

### Background

- [Why feature-organized?](#why-feature-organized) — the motivation
- [How this list is curated](CONTRIBUTING.md)
- [Part of the AI Quality stack](#part-of-the-ai-quality-stack)

---

## Why feature-organized?

If you search "awesome LLM evaluation" today you find 6 lists, all organized by tool category: harnesses, frameworks, benchmarks, observability platforms. Useful when you already know what you need. Less useful when you're a developer asking "I'm shipping a code-gen feature next week, what do I test?"

This list is the answer to that. Each feature category is a self-contained mini-playbook:

- **Testing patterns** — what kinds of tests this feature needs, in what order
- **Recommended tools** — linked, with star/license/last-commit badges
- **Sample prompts and golden datasets** — open-licensed seed datasets
- **Eval rubrics** — LLM-as-judge templates with scoring criteria
- **Failure-mode catalog** — what breaks, with a 1-line repro for each
- **Run this in 60 seconds** — a runnable snippet you can paste

The same tools (DeepEval, Promptfoo, BehaviorCI, Inspect AI, OpenEvals) appear in multiple categories with different recommendations because they fit different feature types differently.

---

## How to use this list

- **Building something new?** Open the feature page, read the "Testing patterns" section first, then pick a tool, then run the 60-second starter.
- **Debugging a regression?** Check the feature's failure-mode catalog. ~70% of "weird" AI bugs fit a documented failure mode.
- **Picking a tool?** [TOOL-FIT.md](TOOL-FIT.md) — which tool fits your feature.
- **Auditing a team's coverage?** [MATURITY.md](MATURITY.md) — assess each of your features against the L0–L4 maturity ladder.
- **Submitting a tool, pattern, or failure mode?** [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Quick links by feature

| Feature | Pattern count | Tool count | Failure modes | 60-sec starter |
|---|---|---|---|---|
| [Chatbots](features/chatbots.md) | 12 | 22 | 9 | ✓ |
| [RAG](features/rag.md) | 14 | 28 | 10 | ✓ |
| [Summarizers](features/summarizers.md) | 9 | 15 | 8 | ✓ |
| [Code-gen](features/code-gen.md) | 11 | 19 | 9 | ✓ |
| [Image-gen](features/image-gen.md) | 8 | 14 | 8 | ✓ |
| [Voice](features/voice.md) | 9 | 16 | 8 | ✓ |
| [Agents](features/agents.md) | 13 | 24 | 10 | ✓ |
| [Multimodal](features/multimodal.md) | 8 | 13 | 7 | ✓ |
| [Classifiers](features/classifiers.md) | 10 | 17 | 9 | ✓ |
| [Translation](features/translation.md) | 8 | 12 | 6 | ✓ |
| [Search](features/search.md) | 9 | 16 | 8 | ✓ |
| **Total** | **111** | **196** | **92** | **11** |

(Count is v1.0 baseline. The machine-readable index at `data/tools.csv` is the source of truth and refreshes weekly.)

---

## Curation principles

This is an opinionated list, not a tool dump.

1. **Every entry has a one-paragraph "why".** No naked links.
2. **Active maintenance preferred.** Tools without a commit in 12 months are listed but flagged.
3. **Open core preferred.** Closed-source platforms with no open implementation are listed in a separate "commercial" section — under each feature — and not mixed with open tools.
4. **De-duplicated.** A tool that appears in 8 feature pages is fine; a tool that's just a variant of another well-known tool gets one listing.
5. **Real failure modes only.** Failure modes have a repro. "AI sometimes hallucinates" is not a failure mode; "RAG returns top-1 stale doc with high confidence on entity-disambiguation queries" is.

---

## Refresh schedule

- **Weekly**: GitHub stars, last-commit date, and license fields refreshed via [.github/workflows/refresh.yml](.github/workflows/refresh.yml).
- **Monthly**: human review of new tool submissions and failure-mode reports.
- **Quarterly**: maturity matrix updated; cross-cutting reorganization.

---

## Contributing

PRs welcome on:

- New tools (with a 1-paragraph "why it matters")
- New testing patterns (per feature)
- New failure modes (with repro)
- New 60-second starter snippets
- Translations of feature pages

See [CONTRIBUTING.md](CONTRIBUTING.md) for the bar.

---

## Part of the AI Quality stack

- **[claude-code-rules-for-ai-features](https://github.com/Aftabbs/claude-code-rules-for-ai-features)** — opinionated CLAUDE.md / AGENTS.md with 10 commandments for shipping AI features
- **[ai-quality-handbook](https://github.com/Aftabbs/ai-quality-handbook)** — the single-file definitive guide to shipping AI features safely
- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — the merge-gate tool that implements behavioral testing as a CI artifact (maintained by this list's author)

---

## License

Content is **CC-BY-SA-4.0**. Code (scripts, snippets, workflows) is **MIT**.

You may copy and modify with credit + share-alike.
