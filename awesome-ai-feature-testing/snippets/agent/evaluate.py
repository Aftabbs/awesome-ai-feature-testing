"""
Agent eval starter — tool-call correctness + loop bound.

3 mocked tools (calculator, weather, calendar). 5 tasks. Checks:
- did the agent call the right tool(s)?
- did the agent stay within the 5-call budget?
"""

from __future__ import annotations

import json
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).parent
client = OpenAI()
MAX_TOOL_CALLS = 5


def calculator(expression: str) -> str:
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"error: {e}"


def weather(city: str) -> str:
    canned = {"Paris": "18°C, light rain", "Tokyo": "26°C, sunny", "Mumbai": "32°C, humid"}
    return canned.get(city, f"unknown city: {city}")


def calendar_check(date: str) -> str:
    return f"{date}: 2 events scheduled"


TOOLS = {
    "calculator": calculator,
    "weather": weather,
    "calendar_check": calendar_check,
}

OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a Python arithmetic expression",
            "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "weather",
            "description": "Get weather for a city",
            "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calendar_check",
            "description": "Check calendar for a given date (YYYY-MM-DD)",
            "parameters": {"type": "object", "properties": {"date": {"type": "string"}}, "required": ["date"]},
        },
    },
]


def run_agent(task: str) -> tuple[list[str], str]:
    messages = [
        {"role": "system", "content": "You are a helpful agent. Use tools when needed. Be concise."},
        {"role": "user", "content": task},
    ]
    calls: list[str] = []

    for _ in range(MAX_TOOL_CALLS):
        rsp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=OPENAI_TOOLS,
            tool_choice="auto",
        )
        msg = rsp.choices[0].message

        if not msg.tool_calls:
            return calls, msg.content or ""

        messages.append(msg.model_dump(exclude_unset=True))
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments or "{}")
            calls.append(name)
            result = TOOLS[name](**args)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})

    return calls, "[loop bound exceeded]"


def main() -> None:
    tasks = [json.loads(l) for l in (ROOT / "tasks.jsonl").read_text().splitlines() if l.strip()]

    rows = []
    for task in tasks:
        calls, answer = run_agent(task["task"])
        expected = set(task["expected_tools"])
        got = set(calls)
        tools_ok = expected <= got
        within_budget = len(calls) <= MAX_TOOL_CALLS

        rows.append({"id": task["id"], "tools_ok": tools_ok, "within_budget": within_budget, "calls": calls})
        print(
            f"{task['id']:>10}  tools={'PASS' if tools_ok else 'FAIL'}  "
            f"loop={'PASS' if within_budget else 'FAIL'}  "
            f"calls={','.join(calls)}"
        )

    n = len(rows)
    print()
    print(f"Tool-call correctness: {sum(r['tools_ok'] for r in rows)}/{n}")
    print(f"Loop bound:            {sum(r['within_budget'] for r in rows)}/{n}")


if __name__ == "__main__":
    main()
