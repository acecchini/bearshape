---
description: Where runtime validation occurs around framework transformations.
---

# Framework transformations

Runtime shape checks run when Python reaches a beartype wrapper. JAX tracing and
Torch compilation can change when that happens.

## JAX

Put `@beartype` outside `@jax.jit` to check the Python call's inputs and
outputs:

```python
import jax
from beartype import beartype
from bearshape import N
from bearshape.jax import F32

@beartype
@jax.jit
def add(x: F32[N], y: F32[N]) -> F32[N]:
  return x + y
```

With the opposite order, `@jax.jit` outside `@beartype`, validation runs while
JAX traces the function. Repeated execution of a cached compiled function does
not repeat the Python validator. New shapes/dtypes can trigger tracing again. Do
not rely on runtime value expressions involving traced values to behave like
ordinary Python values.

The maintained CPU tests also cover `jax.vmap` over validated row functions and
`jax.grad` of a validated scalar loss. For `vmap`, write the annotation for the
logical row seen by the mapped function. A batch of rows with shape `(B, C)`
passes a row of shape `(C,)` to that function.

## Torch

Place the beartype wrapper outside the compiled callable to check each Python
entry and returned result:

```python
import torch
from beartype import beartype
from bearshape import N
from bearshape.torch import F32

@beartype
@torch.compile(backend="eager")
def add(x: F32[N], y: F32[N]) -> F32[N]:
  return x + y
```

The maintained compiler test uses Torch's eager backend to exercise the compiler
front end. It verifies correct results, wrong shape/dtype rejection and
autograd. This does not establish every compiler backend, fullgraph mode or
dynamic-shape specialization. Strict validation preserves the original tensor
and its gradient history. Like validation checks convertibility; it does not
replace the argument with the converted tensor.

These contracts are tested in `tests/test_jax.py` and `tests/test_torch.py`,
including the maintained backend version floors. Calls made from a transformed
or compiled caller still follow that framework's tracing rules.
