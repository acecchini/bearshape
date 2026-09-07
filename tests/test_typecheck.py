"""Type-checker compatibility tests.

Runs pyright, mypy, and ty against both:

- sample files under ``tests/typing/`` that exercise the public annotation
  surface and its documented ``TYPE_CHECKING`` workarounds
- the ``src/`` tree itself, so source-level checker regressions are caught too

Use the current interpreter as the checker target so third-party stubs match
the installed dependencies. CI runs this suite on Python 3.10 through 3.14.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TYPING_DIR = ROOT / "tests" / "typing"
WHOLE_TREE_TARGETS = ["src", "tests/typing"]
PYTHON_TARGET = f"{sys.version_info.major}.{sys.version_info.minor}"

# ---------------------------------------------------------------------------
# All files tested by all three checkers
# ---------------------------------------------------------------------------

ALL_FILES = [
  "check_imports.py",
  "check_decorator.py",
  "check_like_types.py",
  "check_make_array_type.py",
  "check_tree.py",
  "check_annotations.py",
  "check_annotations_jax.py",
  "check_annotations_torch.py",
  "check_annotations_cupy.py",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _tool_path(tool: str) -> str | None:
  env_tool = Path(sys.executable).resolve().parent / tool
  if env_tool.exists():
    return str(env_tool)
  return shutil.which(tool)


def _skip_if_missing(tool: str) -> None:
  if _tool_path(tool) is None:
    pytest.skip(f"{tool} not installed")


def _run(tool: str, *args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
  executable = _tool_path(tool)
  assert executable is not None, f"{tool} not installed"
  return subprocess.run(
    [executable, *args], capture_output=True, text=True, timeout=120, cwd=cwd
  )


def _run_mypy(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
  # Give each invocation its own cache directory so xdist workers do not race
  # through the shared .mypy_cache during the typecheck suite.
  with tempfile.TemporaryDirectory(prefix="bearshape-mypy-cache-") as cache_dir:
    return _run("mypy", "--show-traceback", "--cache-dir", cache_dir, *args, cwd=cwd)


# ---------------------------------------------------------------------------
# Pyright
# ---------------------------------------------------------------------------


@pytest.mark.typecheck
class TestPyright:
  @pytest.mark.parametrize("filename", ALL_FILES)
  def test_pyright(self, filename: str) -> None:
    _skip_if_missing("pyright")
    result = _run(
      "pyright", "--pythonversion", PYTHON_TARGET, str(TYPING_DIR / filename)
    )
    assert result.returncode == 0, (
      f"pyright failed on {filename}:\n{result.stdout}\n{result.stderr}"
    )

  def test_pyright_source_tree(self) -> None:
    _skip_if_missing("pyright")
    result = _run("pyright", "--pythonversion", PYTHON_TARGET, *WHOLE_TREE_TARGETS)
    assert result.returncode == 0, (
      f"pyright failed on source tree for Python {PYTHON_TARGET}:\n{result.stdout}\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# Mypy
# ---------------------------------------------------------------------------


@pytest.mark.typecheck
class TestMypy:
  @pytest.mark.parametrize("filename", ALL_FILES)
  def test_mypy(self, filename: str) -> None:
    _skip_if_missing("mypy")
    result = _run_mypy("--python-version", PYTHON_TARGET, str(TYPING_DIR / filename))
    assert result.returncode == 0, (
      f"mypy failed on {filename}:\n{result.stdout}\n{result.stderr}"
    )

  def test_mypy_source_tree(self) -> None:
    _skip_if_missing("mypy")
    result = _run_mypy("--python-version", PYTHON_TARGET, *WHOLE_TREE_TARGETS)
    assert result.returncode == 0, (
      f"mypy failed on source tree for Python {PYTHON_TARGET}:\n{result.stdout}\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# ty
# ---------------------------------------------------------------------------


@pytest.mark.typecheck
class TestTy:
  @pytest.mark.parametrize("filename", ALL_FILES)
  def test_ty(self, filename: str) -> None:
    _skip_if_missing("ty")
    result = _run(
      "ty", "check", "--python-version", PYTHON_TARGET, str(TYPING_DIR / filename)
    )
    assert result.returncode == 0, (
      f"ty failed on {filename}:\n{result.stdout}\n{result.stderr}"
    )

  def test_ty_source_tree(self) -> None:
    _skip_if_missing("ty")
    result = _run("ty", "check", "--python-version", PYTHON_TARGET, *WHOLE_TREE_TARGETS)
    assert result.returncode == 0, (
      f"ty failed on source tree for Python {PYTHON_TARGET}:\n{result.stdout}\n{result.stderr}"
    )
