---
description: How bearshape annotations map onto pyright, mypy, ty, and pyrefly.
---

# Static Typing

bearshape supports **pyright**, **mypy**, **ty**, and **pyrefly**. The
repository runs all four against the typing fixtures in `tests/typing/` via
`tests/test_typecheck.py`.

At a high level:

- under `TYPE_CHECKING`, backend array aliases resolve to real static array
    types such as `numpy.typing.NDArray`, `jax.Array`, `torch.Tensor`, or
    `cupy.ndarray`
- pre-defined dimensions such as `N`, `C`, and `Scalar` are represented in a
    checker-friendly way
- some syntax is still inherently runtime-only and needs either targeted ignores
    or checker-only aliases

## Works directly

These patterns are part of the tested public typing surface:

```python
from beartype import beartype
from bearshape import C, N, Scalar, __, check
from bearshape.numpy import F32

@beartype
def f(x: F32[N, C]) -> F32[N, C]:
  return x

@beartype
def scalar(x: F32[Scalar]) -> F32[Scalar]:
  return x

@beartype
def keep_last(x: F32[__, C]) -> F32[__, C]:
  return x

@check
async def async_identity(x: F32[N]) -> F32[N]:
  return x
```

This also extends to:

- backend aliases from `bearshape.jax`, `bearshape.torch`, and `bearshape.cupy`
- `Like` aliases such as `F32Like[N, C]`
- leaf-only tree annotations such as `Tree[F32[N, C]]`
- the public `ArrayLike` template and backend `ScalarLike` aliases

## What is runtime-only

The following syntax is valid at runtime but is still beyond what the static
checkers model directly:

<!-- markdownlint-disable MD013 -->

| Pattern | Example | Typical workaround | | -------------------------- |
-------------------- | ----------------------------------------------- | | Fixed
integer literal dims | `F32[N, 3, H, W]` | targeted `# type: ignore` or
checker-only alias | | Arithmetic dims | `F32[N + 2]` | targeted
`# type: ignore` or checker-only alias | | `Value(...)` dims |
`F32[Value("size")]` | targeted `# type: ignore` | | Variadic dims |
`F32[~B, C]` | targeted `# type: ignore` or checker-only alias | | Broadcastable
dims | `F32[+N, C]` | targeted `# type: ignore` or checker-only alias | | Tree
structure args | `Tree[F32[N], T]` | targeted `# type: ignore` |

<!-- markdownlint-enable MD013 -->

Example:

```python
from beartype import beartype
from bearshape import N, Value
from bearshape.numpy import F32

@beartype
def pad(x: F32[N]) -> F32[N + 2]:  # type: ignore[valid-type]
  ...

@beartype
def sized(size: int) -> F32[Value("size")]:  # type: ignore[valid-type]
  ...
```

Prefer narrow, annotation-local ignores like these instead of weakening global
checker strictness for an entire project.

That is also the main repo-tested baseline in `tests/typing/`.

## Checker-only aliases for runtime-only tokens

When you use runtime-only tokens frequently, you can keep signatures cleaner by
defining a checker-only placeholder under `TYPE_CHECKING` and binding it to the
real runtime token in the `else` branch.

### Fixed integer literals

```python
import typing as tp
from beartype import beartype
from bearshape import Dimension, H, N, W
from bearshape.numpy import F32

if tp.TYPE_CHECKING:
  Three = tp.Literal[3]
else:
  Three = Dimension(3)

@beartype
def process_rgb(x: F32[N, Three, H, W]) -> F32[N, Three, H, W]:
  return x
```

### Variadic, broadcastable, and symbolic aliases

```python
import typing as tp
from beartype import beartype
from bearshape import B, C, N
from bearshape.numpy import F32

if tp.TYPE_CHECKING:
  VariadicBatch = tp.Literal["VariadicBatch"]
  BroadcastN = tp.Literal["BroadcastN"]
  PaddedN = tp.Literal["PaddedN"]
else:
  VariadicBatch = ~B
  BroadcastN = +N
  PaddedN = N + 2

@beartype
def softmax(x: F32[VariadicBatch, C]) -> F32[VariadicBatch, C]:
  return x

@beartype
def broadcast_add(x: F32[N, C], y: F32[BroadcastN, C]) -> F32[N, C]:
  return x

@beartype
def pad(x: F32[N]) -> F32[PaddedN]:
  return x
```

Notes:

- the checker-side placeholder name is arbitrary; it just needs to be a stable
    alias object
- this is an advanced convenience pattern, not the only supported approach
- if you only need the syntax occasionally, a targeted `# type: ignore` is
    simpler and more explicit

## Custom dimensions

Custom dimensions are runtime objects. To make them usable in annotations across
all four checkers, define a checker-only alias:

```python
import typing as tp
from beartype import beartype
from bearshape import Dimension, N
from bearshape.numpy import F32, I64

if tp.TYPE_CHECKING:
  type Vocab = int
  type Embed = int
else:
  Vocab = Dimension("Vocab")
  Embed = Dimension("Embed")

@beartype
def embed(tokens: I64[N], table: F32[Vocab, Embed]) -> F32[N, Embed]:
  return table[tokens]
```

This is the simplest checker-only alias pattern and the one most users should
keep in their toolbox first.

## Tree annotations

`Tree[Leaf]` supports ordinary leaves, lists, tuples (including named tuples),
dictionaries and None. Existing typed containers such as `list[int]` and
`dict[str, list[int]]` can be passed to `Tree[int]`. Wrong leaves, including
strings hidden inside a numeric tree, are checked by the consumer fixtures. An
empty container or None has no leaves for the default backend traversal.

The static model describes container behavior; it cannot infer backend node
registration or tree structure. The selected backend must actually recognize a
custom container. For a registered JAX node, keep its concrete static type with
the existing conditional-alias pattern:

```python
from typing import TYPE_CHECKING, TypeAlias

from bearshape import N
from bearshape.jax import Tree
from bearshape.numpy import F32

# Batch is your concrete class, registered with jax.tree_util.
if TYPE_CHECKING:
  BatchTree: TypeAlias = Batch
else:
  BatchTree = Tree[F32[N]]
```

The executable fixture `tests/typing/check_tree_consumers.py` contains the
complete registered class and a decorated consumer. Tree structure arguments
such as `Tree[F32[N], T]` remain runtime-only; use a checker-only leaf alias as
shown above when you need a named structure constraint.

The optree backend uses its default registry. A class registered only in an
optree namespace is not automatically recognized by this Tree annotation.

## Convertible input and native result types

NumPy Like annotations describe convertible numeric families, including other
precisions accepted by same-kind casting. JAX/Torch Like annotations include
numeric scalars, NumPy arrays and nested sequences as well as native arrays.
Convert the value explicitly to obtain a native array result. Like validation
does not convert the function argument for you.

The consumer fixtures test these calls, inferred results and expected errors
with pyright, mypy, ty and pyrefly. NumPy Shaped retains ndarray methods while
allowing nonnumeric dtypes. Runtime validates dimension relationships and
value/device-dependent conversion constraints.

Backend ScalarLike aliases describe Python and NumPy scalar values. For a
backend-native scalar array, use a shaped alias with Scalar, such as
`F32Like[Scalar]`.
