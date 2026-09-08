"""Nonnumeric and incompatible-family inputs must remain visible errors."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from bearshape import N
from bearshape.jax import F32Like as JaxF32Like
from bearshape.numpy import F32Like, I8Like, U8Like
from bearshape.torch import F32Like as TorchF32Like

if TYPE_CHECKING:
  from numpy.typing import NDArray


def numpy_float(value: F32Like[N]) -> None:
  pass


def numpy_integer(value: I8Like[N]) -> None:
  pass


def numpy_unsigned(value: U8Like[N]) -> None:
  pass


def jax_float(value: JaxF32Like[N]) -> None:
  pass


def torch_float(value: TorchF32Like[N]) -> None:
  pass


complexes: NDArray[np.complex64] = np.ones(3, dtype=np.complex64)
floats: NDArray[np.float64] = np.ones(3, dtype=np.float64)
integers: NDArray[np.int32] = np.ones(3, dtype=np.int32)
numpy_float(complexes)  # expect: argument
numpy_integer(floats)  # expect: argument
numpy_unsigned(integers)  # expect: argument
numpy_float("not numeric")  # expect: argument
numpy_float({"x": 1})  # expect: argument
jax_float("not numeric")  # expect: argument
jax_float({"x": 1})  # expect: argument
torch_float("not numeric")  # expect: argument
torch_float({"x": 1})  # expect: argument
