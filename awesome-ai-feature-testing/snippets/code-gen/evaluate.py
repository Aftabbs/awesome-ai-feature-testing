"""
Code-gen eval starter — compile + lint + test for 5 small tasks.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).parent
client = OpenAI()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def generate(task: dict) -> str:
    rsp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate Python 3.12 code that satisfies the user's task. "
                    "Return ONLY a Python module body, no markdown fences, no explanation."
                ),
            },
            {"role": "user", "content": task["description"]},
        ],
    )
    return rsp.choices[0].message.content or ""


def compile_check(code: str, tmp: Path) -> bool:
    src = tmp / "solution.py"
    src.write_text(code)
    result = subprocess.run(
        ["python", "-m", "py_compile", str(src)],
        capture_output=True,
    )
    return result.returncode == 0


def lint_check(tmp: Path) -> bool:
    result = subprocess.run(
        ["ruff", "check", str(tmp / "solution.py"), "--quiet"],
        capture_output=True,
    )
    return result.returncode == 0


def test_check(tmp: Path, task: dict) -> bool:
    test_file = tmp / "test_solution.py"
    test_file.write_text(task["test_code"])
    result = subprocess.run(
        ["pytest", "-x", "-q", str(test_file)],
        cwd=str(tmp),
        capture_output=True,
    )
    return result.returncode == 0


def main() -> None:
    tasks = load_jsonl(ROOT / "tasks.jsonl")

    rows = []
    for task in tasks:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            code = generate(task)
            compiles = compile_check(code, tmp)
            lints = lint_check(tmp) if compiles else False
            tests = test_check(tmp, task) if compiles else False
            rows.append({"id": task["id"], "compiles": compiles, "lints": lints, "tests": tests})
            print(
                f"{task['id']:>10}  compile={'PASS' if compiles else 'FAIL'}  "
                f"lint={'PASS' if lints else 'FAIL'}  tests={'PASS' if tests else 'FAIL'}"
            )

    n = len(rows)
    print()
    print(f"Compile: {sum(r['compiles'] for r in rows)}/{n}")
    print(f"Lint:    {sum(r['lints'] for r in rows)}/{n}")
    print(f"Tests:   {sum(r['tests'] for r in rows)}/{n}")


if __name__ == "__main__":
    main()
