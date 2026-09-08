"""Reproduce the unresolved native composite-union rollback release blocker."""

from __future__ import annotations

import sys
from importlib.metadata import version

import numpy as np
from beartype import beartype

from bearshape import C, N
from bearshape.numpy import F32


@beartype
def choose(_pair: tuple[F32[N], str] | tuple[F32[C], int], _y: F32[N]) -> None:
  """Accept the second alternative without retaining the first one's N binding."""


def main() -> None:
  sys.stdout.write(
    f"Python {sys.version}; bearshape {version('bearshape')}; "
    f"beartype {version('beartype')}; NumPy {version('numpy')}\n"
  )
  sys.stdout.flush()
  choose((np.ones(2, dtype=np.float32), 1), np.ones(3, dtype=np.float32))
  sys.stdout.write("Native composite-union rollback probe passed\n")


if __name__ == "__main__":
  main()
