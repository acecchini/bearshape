---
description: Explicit Tree backend using OpTree.
---

# `bearshape.optree`

`bearshape.optree` provides the explicit OpTree-backed `Tree` annotation plus
the shared `Structure` type.

```python
from bearshape.optree import Tree, Structure
```

## `Tree`

At runtime, `Tree` validates pytree leaves and optional structure bindings using
OpTree.

```python
from beartype import beartype
from bearshape import N, T
from bearshape.numpy import F32
from bearshape.optree import Tree

@beartype
def update(params: Tree[F32[N], T],
           grads: Tree[F32[N], T]) -> Tree[F32[N]]:  # type: ignore[valid-type]
  ...
```

Static typing split:

- `Tree[F32[N]]` is checker-friendly
- `Tree[F32[N], T]` and any other structure-bearing form are runtime-only

## `Structure`

`Structure` is the same structure-symbol type exported from the root `bearshape`
module.

```python
from bearshape import Structure

Params = Structure("Params")
```

## When to use `bearshape.optree`

Use this module when:

- you want tree annotations without bringing in JAX
- you want an explicit, stable OpTree backend in a NumPy or Torch project
- you do not want tree behavior to depend on which optional packages happen to
    be installed
