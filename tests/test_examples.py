"""Execute consumer examples in addition to checking their annotations."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_like_consumer_example_runs() -> None:
  subprocess.run(
    [sys.executable, "-m", "tests.typing.check_like_consumers"],
    check=True,
    cwd=Path(__file__).resolve().parents[1],
    capture_output=True,
    text=True,
    timeout=60,
  )
