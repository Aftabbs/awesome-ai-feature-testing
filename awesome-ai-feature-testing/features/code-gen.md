# Code generation & code review

Code-gen and code-review features have a unique gift: their outputs can be deterministically tested. Compile, lint, run, type-check. Most other AI features lean heavily on LLM-as-judge; code can lean on real compilers.

This page covers: code completion, function generation, scaffolders, refactoring assistants, code reviewers, test generators.

---

## Testing patterns

### 1. Compilation / parse-clean

**What it tests:** Does the generated code compile / parse without syntax errors?

**Tools:** Language-native compilers and parsers. `python -c`, `tsc --noEmit`, `cargo check`, `go build`, etc. Wrap in BehaviorCI `function` rule, DeepEval custom assertion, or Promptfoo Python assertion.

**When to use:** Always.

**Cost / effort:** Low. Trivial to wire.

---

### 2. Lint clean

**What it tests:** Does the code pass linters configured for the target style?

**Tools:** Language-native linters (`ruff`, `eslint`, `clippy`, `golangci-lint`). Wrap as a function check.

---

### 3. Type-check pass

**What it tests:** Does the code type-check?

**Tools:** `mypy`, `pyright`, `tsc`, language-server-based checks.

---

### 4. Test execution (the gold standard)

**What it tests:** Does generated code pass a known test suite? Does generated test code itself pass on the corresponding implementation?

**Tools:** Sandboxed test runners. [HumanEval](https://github.com/openai/human-eval), [MBPP](https://github.com/google-research/google-research/tree/master/mbpp), [SWE-Bench](https://github.com/princeton-nlp/SWE-bench), [LiveCodeBench](https://github.com/LiveCodeBench/LiveCodeBench).

**When to use:** When you can hermetically run the code (a sandbox container per case).

---

### 5. Cross-reference consistency

**What it tests:** When code-gen produces multiple files, do imports resolve, do class names match, do generated tests reference real symbols?

**Tools:** AST-walk function checks. `import` resolver. `treesitter`-based cross-doc checks.

---

### 6. No-secrets / no-unsafe-primitives

**What it tests:** No hardcoded API keys, passwords. No `eval()`, `exec()`, `shell=True` unless explicitly required.

**Tools:** [trufflehog](https://github.com/trufflesecurity/trufflehog), [gitleaks](https://github.com/gitleaks/gitleaks), regex-based BehaviorCI `must-not-contain`.

---

### 7. Vulnerability check (deps)

**What it tests:** Do generated dependencies have known CVEs?

**Tools:** [OSV](https://osv.dev/), [Snyk OSS](https://github.com/snyk/snyk), [Dependabot](https://github.com/dependabot).

---

### 8. Diff/edit precision (for editing-style features)

**What it tests:** When the model proposes an edit, does the edit apply cleanly? Does it modify only the intended region?

**Tools:** [Aider's edit-format eval](https://aider.chat/docs/leaderboards/), custom diff hunk checks.

---

### 9. Style match (for refactoring)

**What it tests:** Does the refactor match the team's style (naming, indentation, commenting)?

**Tools:** Lint configurations + a style judge.

---

### 10. Behavior preservation (for refactoring)

**What it tests:** Does the refactored code preserve the original's behavior?

**Tools:** Run the same test suite against pre- and post-refactor code; compare outputs.

---

### 11. Code review precision/recall (for code-review features)

**What it tests:** Does the AI reviewer flag real issues (precision) and not miss them (recall)?

**Tools:** [CRSurvey](https://github.com/microsoft/cr-survey), [SWE-bench reviewer extensions](https://github.com/princeton-nlp/SWE-bench), labeled PR datasets.

---

## Recommended tools

### Code-gen-specific

- **[HumanEval](https://github.com/openai/human-eval)** — OpenAI's classic.
- **[MBPP](https://github.com/google-research/google-research/tree/master/mbpp)** — Google's beginner Python problems.
- **[SWE-Bench](https://github.com/princeton-nlp/SWE-bench)** — real-world GitHub issues benchmark.
- **[LiveCodeBench](https://github.com/LiveCodeBench/LiveCodeBench)** — contamination-free.
- **[BigCodeBench](https://github.com/bigcode-project/bigcodebench)** — practical task solving.
- **[ClassEval](https://github.com/FudanSELab/ClassEval)** — class-level code-gen.
- **[CodeContests](https://github.com/google-deepmind/code_contests)** — competitive programming.
- **[DS-1000](https://github.com/HKUNLP/DS-1000)** — data science specific.
- **[Aider polyglot leaderboard](https://aider.chat/docs/leaderboards/)** — multi-lang edit-format eval.

### General LLM eval w/ code support

- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — `function` rule type for compile/lint/test integration.
- **[DeepEval](https://github.com/confident-ai/deepeval)** — `MetricCollection` with code-gen-specific metrics.
- **[Promptfoo](https://github.com/promptfoo/promptfoo)** — Python/JS assertions for code execution.
- **[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)** — research-grade with sandbox support.

### Compiler / linter primitives

- **Python**: ruff, mypy, pyright, pylint, bandit (security)
- **TypeScript**: tsc, eslint, biome
- **Rust**: clippy, cargo
- **Go**: golangci-lint, staticcheck
- **Java**: spotbugs, checkstyle
- **C/C++**: clang-tidy, cppcheck

### Sandbox / execution environments

- **[OpenHands sandbox](https://github.com/All-Hands-AI/OpenHands)** — sandboxed agent execution.
- **[Modal](https://modal.com/)** — fast serverless sandbox.
- **[E2B](https://github.com/e2b-dev/E2B)** — code-interpreter sandbox.
- **[Daytona](https://github.com/daytonaio/daytona)** — dev-environment-as-a-service.

### Vulnerability / security

- **[trufflehog](https://github.com/trufflesecurity/trufflehog)** — secret detection.
- **[gitleaks](https://github.com/gitleaks/gitleaks)** — secret scanning.
- **[OSV](https://osv.dev/)** — vulnerability lookup.
- **[Bandit](https://github.com/PyCQA/bandit)** — Python security.
- **[Semgrep](https://github.com/semgrep/semgrep)** — static analysis with custom rules.

### Code review evaluators

- **[Greptile evals](https://github.com/greptileai/eval)** — code-review benchmark.
- **[CRSurvey](https://github.com/microsoft/cr-survey)** — code-review benchmark.

---

## Sample rubric (Python backend scaffolder)

```yaml
behaviors:
  - id: handler-compiles
    type: function
    function: src.evals.checks.python_compiles
    pass_threshold: 100
    weight: 3

  - id: ruff-clean
    type: function
    function: src.evals.checks.ruff_clean
    pass_threshold: 100
    weight: 2

  - id: tests-pass
    type: function
    function: src.evals.checks.pytest_runs
    pass_threshold: 100
    weight: 3

  - id: cross-refs-resolve
    type: function
    function: src.evals.checks.imports_resolve
    pass_threshold: 100
    weight: 3

  - id: no-secrets
    type: must-not-contain
    patterns:
      - regex: '(?i)(api_key|secret|password)\s*=\s*[\"''][^\"'']{8,}'
    pass_threshold: 100
    weight: 5

  - id: no-unsafe
    type: must-not-contain
    patterns: [{ regex: '\\beval\\s*\\(' }, { regex: 'shell\\s*=\\s*True' }]
    pass_threshold: 100
    weight: 5

aggregate:
  pass_threshold: 0.95
```

See the [code-gen cookbook](https://github.com/Aftabbs/claude-code-rules-for-ai-features/blob/main/cookbook/code-gen-feature.md) for the full version.

---

## Failure-mode catalog (code-gen-specific)

See [FAILURE-MODES.md#code-gen](../FAILURE-MODES.md#code-gen).

- **Hallucinated import.** Imports an unused / non-existent module.
- **Test with `assert True`.** Generated test passes but tests nothing.
- **Migration that doesn't roll forward.** Migration syntactic-fine, semantically broken.
- **API-key in example.** Real-looking test key in generated code.
- **Cross-framework drift.** Asked Flask, generated FastAPI snippets.
- **Pydantic v1 in v2 codebase.** Wrong major version syntax.
- **`def` for async route.** FastAPI/Express handler not actually async.
- **Missing CORS preflight.** Public endpoint without CORS posture.
- **Test order dependence.** Tests pass alone, fail in suite.

---

## Run this in 60 seconds

```bash
cd snippets/code-gen
export OPENAI_API_KEY=...

# Generate 5 small Python functions and verify compile + lint + test
python evaluate.py
```

See [snippets/code-gen/](../snippets/code-gen/).

---

## Maturity ladder for code-gen testing

- **L0** — vibes ("looks right").
- **L1** — compile / lint check.
- **L2** — full function-rubric: compile + lint + tests + cross-refs.
- **L3** — merge-gating bundle + sandboxed execution + vuln + secret check.
- **L4** — continuous scoring on production prompts + adversarial test gen + style judge.

L3 is the realistic bar for production code-gen.

---

## See also

- [agents.md](agents.md) — for agent-driven code editors
- [classifiers.md](classifiers.md) — for upstream intent classification
