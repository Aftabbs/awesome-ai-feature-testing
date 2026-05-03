# Contributing

Thanks for considering a contribution. The goal of this list is **opinionated curation**, not exhaustive listing. We accept, reject, and reorganize entries based on the principles below.

## What we accept

### New tool submissions

Open a PR or use the `Add a tool` issue template. Required:

- **Name** and link
- **Which feature page** it belongs on (or `cross-cutting`)
- **One paragraph** of why it matters — what does it do, what does it do better than alternatives, what's its trade-off
- **License** (open core preferred; closed listed in a separate section)
- **Stars / last-commit date** (you don't need to fill these — the weekly refresh script populates `data/tools.csv` automatically)

### New testing patterns

A "pattern" is a reusable recipe for testing some aspect of a feature category. Format on the feature page:

```markdown
### <Pattern name>

**What it tests:** <one sentence>
**Tools that support it:** <links>
**When to use:** <one paragraph>
**Cost / effort:** <low|medium|high — briefly why>
**Common pitfalls:** <bullet list>
```

### New failure modes

A failure mode entry needs:

- A short, memorable name (e.g. "Sycophancy spiral", "Cite-but-contradict")
- A one-line description
- A 1-line repro (input → bad output)
- A recommended test (a behavior bundle line, a regex, a function check)
- The feature category it belongs to

PRs adding speculative failure modes ("the AI might hallucinate") are rejected. Real failure modes have repros.

### New 60-second starter snippets

A starter snippet:

- Lives at `snippets/<feature>/test_<feature>.<ext>`
- Runs in <60 seconds with one API key
- Demonstrates 1–3 testing patterns from the feature page
- Includes a small (≤20 row) seed dataset
- Has a `README.md` in the snippet directory explaining what it tests

### Translations

Each feature page can be translated into other languages. Filename: `features/<feature>.<lang>.md`. Submit one PR per language. Patterns & failure modes do not need translation in v1.

## What we don't accept (without discussion)

### Exhaustive listings

If the new tool isn't materially different from an existing entry, we won't add it. We refuse to be a vendor directory.

### Marketing content

Tool blurbs that read like landing-page copy ("the leading platform for...", "AI-powered evaluation") get rewritten or rejected.

### Duplicate failure modes

Many failure modes are restatements of the same root cause. Before adding, check the failure-mode catalog and see if your case fits an existing entry — extending the existing entry's repros is the right move.

## PR checklist

- [ ] No emojis added
- [ ] No marketing language
- [ ] One-paragraph "why" for any new tool
- [ ] Any new failure mode has a 1-line repro
- [ ] Any new snippet runs in <60s with one API key
- [ ] Links work; check with `make link-check`

## Style

- Per-feature pages: imperative voice, short paragraphs, tables only when truly tabular
- Tools sorted within a category alphabetically (the `refresh.yml` re-sorts after adding stars data)
- Markdown linting via `markdownlint` enforced in CI

## Code of conduct

- Disagreements on tool placement / pattern wording are welcome via PR or issue.
- Sock-puppet PRs to add a maintainer's own tool with inflated descriptions get the tool delisted and the maintainer banned.
- This is an opinionated list. We reject more PRs than we accept and explain why.
