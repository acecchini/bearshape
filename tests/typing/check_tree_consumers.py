"""Real container calls shared by the optree and JAX tree annotations."""

from __future__ import annotations

from collections import OrderedDict
from typing import TYPE_CHECKING, NamedTuple, TypeAlias

import numpy as np
from beartype import beartype
from jax.tree_util import register_pytree_node_class
from typing_extensions import assert_type

from bearshape import N
from bearshape.jax import Tree as JaxTree
from bearshape.numpy import F32
from bearshape.optree import Tree

if TYPE_CHECKING:
  from numpy.typing import NDArray


@beartype
def optree_int(value: Tree[int]) -> Tree[int]:
  return value


@beartype
def jax_int(value: JaxTree[int]) -> JaxTree[int]:
  return value


@beartype
def optree_array(value: Tree[F32[N]]) -> Tree[F32[N]]:
  return value


@beartype
def jax_array(value: JaxTree[F32[N]]) -> JaxTree[F32[N]]:
  return value


@beartype
def string_leaf(value: Tree[str]) -> Tree[str]:
  return value


class Pair(NamedTuple):
  first: int
  second: int


items: list[int] = [1, 2]
nested: list[list[int]] = [[1, 2]]
mapping: dict[str, list[int]] = {"x": items}
values: tuple[int, list[int]] = (1, items)
ordered: OrderedDict[str, int] = OrderedDict(x=1)
empty_list: list[int] = []
empty_dict: dict[str, int] = {}
array: NDArray[np.float32] = np.ones(3, dtype=np.float32)
arrays: dict[str, list[NDArray[np.float32]]] = {"x": [array, array]}

optree_int(1)
optree_int(items)
optree_int(nested)
optree_int(mapping)
optree_int(values)
optree_int(ordered)
optree_int(Pair(1, 2))
optree_int(None)
optree_int(empty_list)
optree_int(empty_dict)
optree_int(())
assert_type(optree_array(arrays), Tree[F32[N]])
optree_array(array)
string_leaf("a leaf")
string_leaf(["first", "second"])
jax_int(1)
jax_int(items)
jax_int(nested)
jax_int(mapping)
jax_int(values)
jax_int(ordered)
jax_int(Pair(1, 2))
jax_int(None)
jax_int(empty_list)
jax_int(empty_dict)
jax_int(())
assert_type(jax_array(arrays), JaxTree[F32[N]])
jax_array(array)

if TYPE_CHECKING:
  assert_type(optree_int(items), Tree[int])
  assert_type(jax_int(items), JaxTree[int])

# A registry cannot be inferred statically. Use the existing conditional-alias
# pattern to keep a custom node's concrete type and its runtime leaf check.


@register_pytree_node_class
class Batch:
  def __init__(self, data: NDArray[np.float32]) -> None:
    self.data = data

  def tree_flatten(self) -> tuple[tuple[NDArray[np.float32]], None]:
    return (self.data,), None

  @classmethod
  def tree_unflatten(
    cls, _auxiliary: None, children: tuple[NDArray[np.float32]]
  ) -> Batch:
    return cls(children[0])


if TYPE_CHECKING:
  BatchTree: TypeAlias = Batch
else:
  BatchTree = JaxTree[F32[N]]


@beartype
def custom_node(value: BatchTree) -> BatchTree:
  return value


assert_type(custom_node(Batch(array)), Batch)

assert optree_int(items) is items
assert items == [1, 2]
