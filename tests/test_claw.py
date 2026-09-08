"""Exercise caller-package instrumentation in independent Python processes."""

from __future__ import annotations

import subprocess
import sys
import textwrap
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
  from pathlib import Path


@pytest.mark.parametrize("custom_conf", [False, True])
def test_instruments_caller_package(tmp_path: Path, custom_conf: bool) -> None:
  package = tmp_path / "instrumented"
  nested = package / "nested"
  nested.mkdir(parents=True)
  conf = (
    "BeartypeConf(violation_param_type=ValueError, "
    "violation_return_type=TypeError, is_color=False)"
    if custom_conf
    else "BeartypeConf(is_color=False)"
  )
  (package / "__init__.py").write_text(
    "from beartype import BeartypeConf\n"
    "from bearshape.claw import bearshape_this_package\n"
    f"bearshape_this_package(conf={conf})\n"
  )
  (nested / "__init__.py").write_text("")
  (nested / "arrays.py").write_text(
    textwrap.dedent("""\
      import numpy as np
      from bearshape import N
      from bearshape.numpy import F32

      def agree(x: F32[N], y: F32[N]) -> F32[N]:
          return y

      def wrong_return(x: F32[N]) -> F32[N]:
          return np.ones(x.shape[0] + 1, dtype=np.float32)
      """)
  )
  (tmp_path / "unrelated.py").write_text(
    "def unchecked(value: int) -> int:\n    return value\n"
  )
  param_error = "ValueError" if custom_conf else "BeartypeCallHintParamViolation"
  return_error = "TypeError" if custom_conf else "BeartypeCallHintReturnViolation"
  script = textwrap.dedent(f"""\
    import numpy as np
    from beartype.roar import (
        BeartypeCallHintParamViolation, BeartypeCallHintReturnViolation,
    )
    from instrumented.nested.arrays import agree, wrong_return
    from unrelated import unchecked

    a = np.ones(2, dtype=np.float32)
    b = np.ones(3, dtype=np.float32)
    assert agree(a, a) is a
    assert unchecked('still unchecked') == 'still unchecked'
    try:
        agree(a, b)
    except {param_error}:
        pass
    else:
        raise AssertionError('caller-package parameter was not checked')
    try:
        wrong_return(a)
    except {return_error}:
        pass
    else:
        raise AssertionError('caller-package return was not checked')
    """)
  result = subprocess.run(
    [sys.executable, "-c", script],
    cwd=tmp_path,
    capture_output=True,
    text=True,
    timeout=30,
  )
  assert result.returncode == 0, result.stdout + result.stderr
