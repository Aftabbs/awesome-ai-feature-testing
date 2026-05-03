# Agents & tool-use

Agents are the hardest features to keep aligned. Failures compound across tool calls, state spans turns, and the eval surface area multiplies. Treat agents as multi-component systems where each step has its own contract.

This page covers: tool-using LLMs, multi-step planners, ReAct-style agents, agentic workflows, browser agents, computer-use agents.

---

## Testing patterns

### 1. Tool-call correctness

**What it tests:** When the model invokes a tool, are the arguments correctly typed and sensibly formed?

**Tools:** Schema validation (JSONSchema, Pydantic), [function-calling-leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html), [BFCL](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html).

---

### 2. Tool-selection accuracy

**What it tests:** Given a goal, does the agent select the right tool from many options?

**Tools:** [BFCL](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html), [τ-bench (TauBench)](https://github.com/sierra-research/tau-bench).

---

### 3. Loop-bound enforcement

**What it tests:** Does the agent terminate within a configured tool-call budget?

**Tools:** Custom function check on trace.

---

### 4. State / memory consistency

**What it tests:** Across multi-turn agent runs, does the agent remember earlier decisions and not contradict them?

**Tools:** [SWE-Bench](https://github.com/princeton-nlp/SWE-bench) (long-horizon), [GAIA](https://huggingface.co/datasets/gaia-benchmark/GAIA), trace-comparison evaluators.

---

### 5. Plan / trajectory quality

**What it tests:** Beyond final answer, is the *path* the agent took sensible?

**Tools:** Trace LLM-as-judge ("does this trajectory look like an expert's plan?"), [AgentBench](https://github.com/THUDM/AgentBench).

---

### 6. Subagent dispatch correctness

**What it tests:** When dispatching to a subagent, are the right tasks delegated?

**Tools:** Trace evaluators with explicit role-assignment checks.

---

### 7. Final answer quality

**What it tests:** Does the agent produce the correct end output?

**Tools:** Standard task-specific evaluators (depends on the agent's job).

---

### 8. No-prohibited-action

**What it tests:** Does the agent avoid forbidden actions (e.g. hitting paywalled URLs, deleting records)?

**Tools:** Tool-call audit log + custom checks.

---

### 9. Cost-bounded execution

**What it tests:** Does the agent terminate before exceeding a budget?

**Tools:** Trace cost tracking via Phoenix / Langfuse + threshold check.

---

### 10. Error recovery

**What it tests:** When a tool returns an error, does the agent recover sensibly (retry, alternate tool, give up cleanly)?

**Tools:** Inject synthetic tool errors; observe behavior.

---

### 11. Browser / computer-use specific

**What it tests:** For browser/computer agents — clicks the right element, fills the right form field, doesn't break out of the sandbox.

**Tools:** [WebArena](https://github.com/web-arena-x/webarena), [WebVoyager](https://github.com/MinorJerry/WebVoyager), [VisualWebArena](https://github.com/web-arena-x/visualwebarena), [OSWorld](https://github.com/xlang-ai/OSWorld).

---

### 12. Adversarial robustness

**What it tests:** Resistance to prompt injection in tool outputs (a webpage that says "ignore prior instructions").

**Tools:** [Garak](https://github.com/leondz/garak), [PyRIT](https://github.com/Azure/PyRIT), [InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent).

---

### 13. Citation / attribution (for research agents)

**What it tests:** Does each claim have a verifiable source URL?

**Tools:** Custom function (URL resolves) + LLM-as-judge for "does source support claim?"

---

## Recommended tools

### Agent-specific eval

- **[AgentBench](https://github.com/THUDM/AgentBench)** — comprehensive agent benchmark.
- **[GAIA](https://huggingface.co/datasets/gaia-benchmark/GAIA)** — general AI assistants benchmark.
- **[τ-bench (TauBench)](https://github.com/sierra-research/tau-bench)** — tool-using agent benchmark.
- **[BFCL](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)** — function calling.
- **[ToolBench](https://github.com/OpenBMB/ToolBench)** — tool-using LLM training/eval.
- **[Vivaria](https://github.com/METR/vivaria)** — METR's agent evaluation tool.
- **[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)** — agent-friendly research-grade.
- **[Harbor](https://github.com/harbor-framework/harbor)** — agent eval + RL environments.
- **[BehaviorCI](https://github.com/Aftabbs/BehaviourCI)** — bundle-level pass/fail; pair with trace-aware evaluators.

### Browser / computer use

- **[WebArena](https://github.com/web-arena-x/webarena)** — realistic web tasks.
- **[VisualWebArena](https://github.com/web-arena-x/visualwebarena)** — visual variant.
- **[WebVoyager](https://github.com/MinorJerry/WebVoyager)** — multimodal browser agent.
- **[OSWorld](https://github.com/xlang-ai/OSWorld)** — full OS desktop benchmark.
- **[Mind2Web](https://github.com/OSU-NLP-Group/Mind2Web)** — generalist web agent.
- **[BrowserGym](https://github.com/ServiceNow/BrowserGym)** — gym for browser agents.

### Long-horizon / SWE benchmarks

- **[SWE-Bench](https://github.com/princeton-nlp/SWE-bench)** — software-engineering issues.
- **[OpenHands benchmarks](https://github.com/All-Hands-AI/OpenHands)** — coding agent.
- **[Claw-Eval](https://github.com/claw-eval/claw-eval)** — human-verified agent tasks.

### Adversarial / red-team

- **[Garak](https://github.com/leondz/garak)** — vulnerability scanner.
- **[PyRIT](https://github.com/Azure/PyRIT)** — Microsoft red team.
- **[InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent)** — prompt injection on tool outputs.
- **[AgentDojo](https://github.com/ethz-spylab/agentdojo)** — adversarial agent eval.

### Observability with strong agent support

- **[Phoenix](https://github.com/Arize-ai/phoenix)** — agent traces.
- **[Langfuse](https://github.com/langfuse/langfuse)** — agent traces with cost.
- **[Opik](https://github.com/comet-ml/opik)** — agent debug & evaluate.
- **[Helicone](https://github.com/Helicone/helicone)** — request-level observability.
- **[OpenLIT](https://github.com/openlit/openlit)** — OpenTelemetry-native; works for agent traces.

### Sandbox runners

- **[E2B](https://github.com/e2b-dev/E2B)** — code interpreter sandbox.
- **[Modal](https://modal.com/)** — serverless sandbox.
- **[Daytona](https://github.com/daytonaio/daytona)** — dev environments.

### Frameworks (each with own eval helpers)

- **[LangGraph](https://github.com/langchain-ai/langgraph)** — graph orchestration; has eval examples.
- **[CrewAI](https://github.com/crewAIInc/crewAI)** — role-based agent crews.
- **[AutoGen](https://github.com/microsoft/autogen)** — multi-agent conversations.
- **[smolagents](https://github.com/huggingface/smolagents)** — minimal agent framework with eval scripts.

---

## Sample rubric (research agent)

```yaml
behaviors:
  - id: every-claim-cited
    type: semantic
    judge: evals/judges/citation-judge.yml
    pass_threshold: 85
    weight: 3

  - id: citations-resolve
    type: function
    function: src.evals.checks.urls_resolve
    pass_threshold: 95
    weight: 3

  - id: tool-call-limit
    type: function
    function: src.evals.checks.tool_calls_le_12
    pass_threshold: 100
    weight: 2

  - id: no-paywalled
    type: function
    function: src.evals.checks.no_paywalled_domains
    pass_threshold: 100
    weight: 3

  - id: insufficient-data-on-empty
    type: function
    function: src.evals.checks.empty_returns_insufficient
    pass_threshold: 100
    weight: 2

aggregate:
  pass_threshold: 0.88

gates:
  cost_p95_max_absolute_usd: 0.40
  latency_p95_max_absolute_ms: 90000
```

See the [agent cookbook](https://github.com/Aftabbs/claude-code-rules-for-ai-features/blob/main/cookbook/agent-feature.md) for the full version.

---

## Failure-mode catalog (agent-specific)

See [FAILURE-MODES.md#agents](../FAILURE-MODES.md#agents).

- **Endless retry loop.** Agent keeps retrying a failing tool.
- **Tool-call hallucination.** Agent describes a tool call without invoking it.
- **Citation hallucination on no-result.** Empty search result → invented citation.
- **Subagent role drift.** Spawned subagent ignores its role boundary.
- **Plan abandonment.** Agent ditches its own plan mid-execution.
- **Indirect prompt injection.** Webpage / tool output contains instructions; agent follows them.
- **Cost runaway.** Tool calls compound; budget blown silently.
- **Stateful drift.** Long-running session loses constraint set in turn 1.
- **Action without confirmation.** Destructive action (delete, send, pay) executed without escalation.
- **Cross-tool leak.** Sensitive output from tool A passed verbatim to tool B without sanitization.

---

## Run this in 60 seconds

```bash
cd snippets/agent
export OPENAI_API_KEY=...

# A 5-task agent benchmark with mocked tools — checks tool-call correctness + loop bound
python evaluate.py
```

See [snippets/agent/](../snippets/agent/).

---

## Maturity ladder for agent testing

- **L0** — vibes ("the demo worked").
- **L1** — task success on a small set.
- **L2** — task success + tool-call correctness + loop bound.
- **L3** — merge-gating bundle: success + tool + cost + adversarial.
- **L4** — continuous + recorded-replay shadow + per-step bundles + drift detection.

L3 is the bar for production agents; few teams are at L4 in 2026.

---

## See also

- [chatbots.md](chatbots.md) — for conversational layer
- [code-gen.md](code-gen.md) — for coding agents
- [rag.md](rag.md) — for retrieval-augmented agents
- [voice.md](voice.md) — for voice agents
