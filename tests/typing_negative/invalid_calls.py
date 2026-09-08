"""Each marked call must produce its intended diagnostic."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from bearshape import N, check
from bearshape.numpy import F32

if TYPE_CHECKING:
  from numpy.typing import NDArray


def needs_float32(value: F32[N]) -> F32[N]:
  return value


@check
def decorated(value: int) -> int:
  return value


integer_array: NDArray[np.int32] = np.ones(3, dtype=np.int32)
needs_float32(integer_array)  # expect: argument
needs_float32("wrong backend")  # expect: argument
decorated("wrong argument")  # expect: argument
decorated(1, 2)  # expect: call
