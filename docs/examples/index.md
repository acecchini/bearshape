---
description: Copyable examples covering the main bearshape runtime and typing patterns.
---

# Examples

## bearshape Tour Notebook

The tour notebook is still the broadest runnable walkthrough in the repository:

- basic `@beartype` usage
- named dimensions and cross-argument consistency
- return checking
- fixed, variadic, broadcastable, anonymous, and symbolic dimensions
- `Value(...)`
- checker-only alias tricks for fixed literal dims and other runtime-only shape
    tokens
- custom array types
- explicit memo helpers
- tree annotations

[:material-notebook: View on GitHub](https://github.com/beartype/bearshape/blob/main/examples/bearshape_tour.ipynb){
.md-button .md-button--primary }

## Example 1: Plain `@beartype`

```python
import numpy as np
from beartype import beartype
from bearshape import C, N
from bearshape.numpy import F32

@beartype
def normalize(x: F32[N, C]) -> F32[N, C]:
  return x / x.sum(axis=1, keepdims=True)

normalize(np.ones((4, 3), dtype=np.float32))  # OK
normalize(np.ones((4,), dtype=np.float32))  # Raises
```

## Example 2: `@bearshape.check` when plain `@beartype` is not enough

```python
import bearshape
import numpy as np
from beartype import beartype
from bearshape import Value
from bearshape.numpy import F32

@bearshape.check
@beartype
async def make_batch(size: int) -> F32[Value("size")]:  # type: ignore[valid-type]
  return np.ones(size, dtype=np.float32)
```

Use this pattern when:

- extra decorators or framework wrappers make frame detection brittle
- `Value(...)` needs an explicit memo scope across `await`
- you want one decorator that applies both memo handling and `BeartypeConf`

## Example 3: Custom dimensions that stay checker-friendly

```python
import typing as tp
from beartype import beartype
from bearshape import Dimension, N
from bearshape.numpy import F32, I64

if tp.TYPE_CHECKING:
  Vocab: tp.TypeAlias = int
  Embed: tp.TypeAlias = int
else:
  Vocab = Dimension("Vocab")
  Embed = Dimension("Embed")

@beartype
def embed_lookup(tokens: I64[N], table: F32[Vocab, Embed]) -> F32[N, Embed]:
  return table[tokens]
```

## Example 4: Tree leaf and structure checking

```python
from beartype import beartype
from bearshape import N, T
from bearshape.numpy import F32
from bearshape.optree import Tree
import optree

@beartype
def accumulate(params: Tree[F32[N], T],
               grads: Tree[F32[N], T]) -> Tree[F32[N]]:  # type: ignore[valid-type]
  return optree.tree_map(lambda p, g: p + g, params, grads)
```

Use leaf-only `Tree[F32[N]]` when you want cleaner static typing. Add structure
symbols like `T` when you want runtime structure equality too.

## Example 5: Like inputs and scalar ranges

```python
from beartype import beartype
from bearshape import Scalar
from bearshape.numpy import F32Like, U8ScalarLike
import numpy as np

@beartype
def to_scalar_array(x: F32Like[Scalar]) -> float:
  return float(np.asarray(x, dtype=np.float32))

@beartype
def clamp_pixel(value: U8ScalarLike) -> int:
  return int(value)
```

## Verify the tour locally

Run `uv run --locked python tools/check_notebook.py` to execute all cells in a
fresh kernel from the selected environment. The executed copy is written under
`build/`; checked-in output is cleared so it cannot be mistaken for current
validation. Expected rejection examples assert the relevant beartype exception.
