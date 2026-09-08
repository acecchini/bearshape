"""Real consumers must retain backend, dtype, and decorated-call information."""

from __future__ import annotations

import jax
import jax.numpy as jnp
import numpy as np
import torch
from beartype import BeartypeConf
from numpy.typing import NDArray
from typing_extensions import assert_type

from bearshape import N, check
from bearshape.jax import F32 as JaxF32
from bearshape.numpy import F32
from bearshape.torch import F32 as TorchF32


def numpy_identity(value: F32[N]) -> F32[N]:
  return value


def jax_identity(value: JaxF32[N]) -> JaxF32[N]:
  return value


def torch_identity(value: TorchF32[N]) -> TorchF32[N]:
  return value


array = np.ones(3, dtype=np.float32)
assert_type(numpy_identity(array), NDArray[np.float32])
assert_type(numpy_identity(array).dtype, np.dtype[np.float32])
assert_type(jax_identity(jnp.ones(3)), jax.Array)
assert_type(torch_identity(torch.ones(3)), torch.Tensor)


@check
def scale(value: int, *, factor: float = 1.0) -> float:
  return value * factor


@check(conf=BeartypeConf())
async def async_identity(value: int) -> int:
  return value


assert_type(scale(2, factor=1.5), float)


async def check_async_result() -> None:
  assert_type(await async_identity(1), int)
