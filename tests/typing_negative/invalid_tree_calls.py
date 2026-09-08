"""Wrong leaves must not disappear inside recursive Tree types."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from bearshape import N
from bearshape.jax import Tree as JaxTree
from bearshape.numpy import F32
from bearshape.optree import Tree

if TYPE_CHECKING:
  from numpy.typing import NDArray


def optree_int(value: Tree[int]) -> None:
  pass


def jax_int(value: JaxTree[int]) -> None:
  pass


def optree_array(value: Tree[F32[N]]) -> None:
  pass


def jax_array(value: JaxTree[F32[N]]) -> None:
  pass


strings: list[str] = ["wrong"]
nested: dict[str, list[str]] = {"x": strings}
wrong_tuple: tuple[int, str] = (1, "wrong")
wrong_array: NDArray[np.int32] = np.ones(3, dtype=np.int32)
arrays: list[NDArray[np.int32]] = [wrong_array]
optree_int("wrong")  # expect: argument
optree_int(strings)  # expect: argument
optree_int(nested)  # expect: argument
optree_int(wrong_tuple)  # expect: argument
optree_int({1, 2})  # expect: argument
optree_array(wrong_array)  # expect: argument
optree_array(arrays)  # expect: argument
jax_int("wrong")  # expect: argument
jax_int(strings)  # expect: argument
jax_int(nested)  # expect: argument
jax_int(wrong_tuple)  # expect: argument
jax_int({1, 2})  # expect: argument
jax_array(wrong_array)  # expect: argument
jax_array(arrays)  # expect: argument
