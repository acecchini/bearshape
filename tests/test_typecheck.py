"""Check source, inferred consumer types, and intentional consumer errors.

Every supported checker is required in the development environment. Tox factors
select one checker explicitly; a missing executable is never a passing skip.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
NEGATIVE_DIR = ROOT / "tests" / "typing_negative"
PYTHON_TARGET = f"{sys.version_info.major}.{sys.version_info.minor}"
CHECKERS = ("pyright", "mypy", "ty", "pyrefly")
TOX_FACTORS = os.environ.get("TOX_ENV_NAME", "").split("-")
SELECTED_CHECKERS = (
  tuple(
    tool
    for tool in CHECKERS
    if any(re.fullmatch(rf"{tool}\d*", f) for f in TOX_FACTORS)
  )
  if "type" in TOX_FACTORS
  else CHECKERS
)
DIAGNOSTIC_CATEGORIES = {
  "reportArgumentType": "argument",
  "reportCallIssue": "call",
  "arg-type": "argument",
  "call-arg": "call",
  "invalid-argument-type": "argument",
  "too-many-positional-arguments": "call",
  "bad-argument-type": "argument",
  "bad-argument-count": "call",
}


def _run(tool: str, targets: list[str]) -> subprocess.CompletedProcess[str]:
  # Resolving sys.executable follows the venv symlink out to the base Python.
  env_tool = Path(sys.executable).parent / (tool + (".exe" if os.name == "nt" else ""))
  executable = str(env_tool) if env_tool.exists() else shutil.which(tool)
  assert executable is not None, f"Required checker {tool} is not installed"
  with tempfile.TemporaryDirectory(prefix="bearshape-typecheck-") as cache:
    arguments = {
      "pyright": [
        "--pythonversion",
        PYTHON_TARGET,
        "--pythonpath",
        sys.executable,
        "--outputjson",
      ],
      "mypy": [
        "--python-version",
        PYTHON_TARGET,
        "--python-executable",
        sys.executable,
        "--cache-dir",
        cache,
        "--show-traceback",
        "--output",
        "json",
      ],
      "ty": [
        "check",
        "--python-version",
        PYTHON_TARGET,
        "--python",
        sys.executable,
        "--output-format",
        "gitlab",
      ],
      "pyrefly": [
        "check",
        "--python-version",
        PYTHON_TARGET,
        "--python-interpreter-path",
        sys.executable,
        "--output-format",
        "json",
      ],
    }
    result = subprocess.run(
      [executable, *arguments[tool], *targets],
      capture_output=True,
      text=True,
      timeout=180,
      cwd=ROOT,
    )
  assert result.returncode in {0, 1}, (
    f"{tool} did not complete normally:\n{result.stdout}\n{result.stderr}"
  )
  return result


def _diagnostics(tool: str, output: str) -> Counter[tuple[str, int, str]]:
  records = []
  if tool == "pyright":
    records.extend(
      (error["file"], error["range"]["start"]["line"] + 1, error.get("rule", "unknown"))
      for error in json.loads(output)["generalDiagnostics"]
    )
  elif tool == "mypy":
    for line in output.splitlines():
      error = json.loads(line)
      if error["severity"] == "error":
        records.append((error["file"], error["line"], error["code"]))
  elif tool == "ty":
    for error in json.loads(output):
      location = error["location"]
      records.append((
        location["path"],
        location["positions"]["begin"]["line"],
        error["check_name"],
      ))
  else:
    records.extend(
      (error["path"], error["line"], error["name"])
      for error in json.loads(output)["errors"]
    )
  return Counter(
    (
      str((ROOT / path).resolve().relative_to(ROOT)),
      line,
      DIAGNOSTIC_CATEGORIES.get(code, code),
    )
    for path, line, code in records
  )


@pytest.mark.typecheck
@pytest.mark.parametrize("tool", SELECTED_CHECKERS)
def test_valid_consumers_and_source(tool: str) -> None:
  result = _run(tool, ["src", "tests/typing"])
  assert result.returncode == 0, (
    f"{tool} rejected valid code on Python {PYTHON_TARGET}:\n{result.stdout}\n{result.stderr}"
  )


@pytest.mark.typecheck
@pytest.mark.parametrize("tool", SELECTED_CHECKERS)
def test_invalid_consumers(tool: str) -> None:
  expected = Counter()
  targets = []
  for path in sorted(NEGATIVE_DIR.glob("*.py")):
    if path.name == "__init__.py":
      continue
    relative = str(path.relative_to(ROOT))
    targets.append(relative)
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
      if match := re.search(r"# expect: (argument|call)\s*$", line):
        expected[relative, line_number, match[1]] += 1
  assert expected, "Negative fixtures must declare expected diagnostics"
  result = _run(tool, targets)
  assert result.returncode == 1, f"{tool} accepted invalid consumer calls"
  assert _diagnostics(tool, result.stdout) == expected, (
    f"{tool} reported different errors from the fixture contract:\n{result.stdout}\n{result.stderr}"
  )
