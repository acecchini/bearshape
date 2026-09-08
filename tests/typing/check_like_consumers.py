"""Ordinary convertible inputs retain useful results after explicit conversion."""

from __future__ import annotations

import jax
import jax.numpy as jnp
import numpy as np
import torch
from beartype import beartype
from numpy.typing import NDArray
from typing_extensions import assert_type

from bearshape import C, N, Scalar
from bearshape.jax import F32Like as JaxF32Like
from bearshape.numpy import F32, C64Like, F32Like, I8Like, Shaped, ShapedLike, U8Like
from bearshape.torch import F32Like as TorchF32Like


@beartype
def numpy_float(value: F32Like[N]) -> F32[N]:
  return np.asarray(value, dtype=np.float32)


@beartype
def numpy_integer(value: I8Like[N]) -> NDArray[np.int8]:
  return np.asarray(value, dtype=np.int8)


@beartype
def numpy_unsigned(value: U8Like[N]) -> NDArray[np.uint8]:
  return np.asarray(value, dtype=np.uint8)


@beartype
def numpy_complex(value: C64Like[N]) -> NDArray[np.complex64]:
  return np.asarray(value, dtype=np.complex64)


@beartype
def numpy_shaped(value: Shaped[N]) -> Shaped[N]:
  return value


@beartype
def numpy_shaped_like(value: ShapedLike[N]) -> Shaped[N]:
  return np.asarray(value)


@beartype
def jax_float(value: JaxF32Like[N]) -> jax.Array:
  return jnp.asarray(value, dtype=jnp.float32)


@beartype
def jax_matrix(value: JaxF32Like[N, C]) -> jax.Array:
  return jnp.asarray(value, dtype=jnp.float32)


@beartype
def jax_scalar(value: JaxF32Like[Scalar]) -> jax.Array:
  return jnp.asarray(value, dtype=jnp.float32)


@beartype
def torch_float(value: TorchF32Like[N]) -> torch.Tensor:
  return torch.as_tensor(value, dtype=torch.float32)


@beartype
def torch_matrix(value: TorchF32Like[N, C]) -> torch.Tensor:
  return torch.as_tensor(value, dtype=torch.float32)


@beartype
def torch_scalar(value: TorchF32Like[Scalar]) -> torch.Tensor:
  return torch.as_tensor(value, dtype=torch.float32)


floats: NDArray[np.float64] = np.ones(3, dtype=np.float64)
integers: NDArray[np.int32] = np.ones(3, dtype=np.int32)
unsigned: NDArray[np.uint64] = np.ones(3, dtype=np.uint64)
booleans: NDArray[np.bool_] = np.ones(3, dtype=np.bool_)
vector: list[float] = [1.0, 2.0]
matrix: list[list[float]] = [[1.0, 2.0], [3.0, 4.0]]
strings: NDArray[np.str_] = np.array(["one", "two"])
objects: NDArray[np.object_] = np.array([object()], dtype=object)
dates: NDArray[np.datetime64] = np.array(["2026-01-01"], dtype="datetime64[D]")
records: NDArray[np.void] = np.zeros(2, dtype=[("x", np.float32)])

assert_type(numpy_float(floats), NDArray[np.float32])
numpy_float(integers)
numpy_float(booleans)
numpy_float(vector)
numpy_integer(integers)
numpy_integer(unsigned)
numpy_integer(booleans)
numpy_unsigned(unsigned)
numpy_unsigned(booleans)
numpy_complex(floats)
numpy_shaped(strings)
numpy_shaped(objects)
numpy_shaped(dates)
numpy_shaped(records)
numpy_shaped_like(strings)
numpy_shaped_like(["one", "two"])
assert_type(jax_float(vector), jax.Array)
jax_float(floats)
jax_float(jnp.ones(3))
jax_matrix(matrix)
jax_scalar(1.0)
jax_scalar(np.float32(1))
assert_type(torch_float(vector), torch.Tensor)
torch_float(floats)
torch_float(torch.ones(3))
torch_matrix(matrix)
torch_scalar(1.0)
torch_scalar(np.float32(1))
