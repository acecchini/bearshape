---
description: Public module-level reference for bearshape.
---

# API Reference

This section is intentionally organized by import boundary, not by internal
implementation file.

## Modules

<!-- markdownlint-disable MD013 -->

| Module                              | What it exports                                                     |
| ----------------------------------- | ------------------------------------------------------------------- |
| **[`bearshape`](bearshape.md)**     | Dimensions, structures, dtype specs, factories and memo helpers     |
| **[`bearshape.numpy`](numpy.md)**   | NumPy arrays, Like and ScalarLike aliases, Structured and ArrayLike |
| **[`bearshape.jax`](jax.md)**       | JAX arrays, Like aliases, ScalarLike re-exports and Tree            |
| **[`bearshape.torch`](torch.md)**   | Torch arrays, Like aliases and ScalarLike re-exports                |
| **[`bearshape.cupy`](cupy.md)**     | CuPy arrays, Like aliases and ScalarLike re-exports                 |
| **[`bearshape.optree`](optree.md)** | Explicit Tree backend and Structure                                 |
| **[`bearshape.claw`](claw.md)**     | Caller-preserving alias of beartype_this_package                    |

<!-- markdownlint-enable MD013 -->

## Important boundaries

- The root `bearshape` import is optional-dependency-safe and does **not**
    require NumPy.
- `Tree` is not exported from the root module. Import it from `bearshape.optree`
    or `bearshape.jax`.
- `make_scalar_like_type` is not exported from the root module. Import it from
    `bearshape.numpy` or a backend module that re-exports it.
