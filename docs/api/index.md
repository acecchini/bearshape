---
description: Public module-level reference for bearshape.
---

# API Reference

This section is intentionally organized by import boundary, not by internal
implementation file.

## Modules

<!-- markdownlint-disable MD013 -->

| Module | What it exports | | -------------------------------- |
\---------------------------------------------------------------------------------------------------------------------------------------------------------------
| | **[`bearshape`](bearshape.md)** | Lightweight root API: dimension symbols,
structure symbols, `DtypeSpec`, `make_array_type`, `make_array_like_type`,
`check`, `check_context`, and `__version__` | |
**[`bearshape.numpy`](numpy.md)** | NumPy array aliases, `Like` aliases,
`ScalarLike` aliases, `Structured`, `ArrayLike`, and `make_scalar_like_type` | |
**[`bearshape.jax`](jax.md)** | JAX array aliases, JAX `Like` aliases, NumPy
`ScalarLike` re-exports, `make_scalar_like_type`, `Tree`, and `Structure` | |
**[`bearshape.torch`](torch.md)** | PyTorch array aliases, Torch `Like` aliases,
NumPy `ScalarLike` re-exports, and `make_scalar_like_type` | |
**[`bearshape.cupy`](cupy.md)** | CuPy array aliases, CuPy `Like` aliases, NumPy
`ScalarLike` re-exports, and `make_scalar_like_type` | |
**[`bearshape.optree`](optree.md)** | Explicit `Tree` backend using OpTree plus
`Structure` | | **[`bearshape.claw`](claw.md)** | Thin wrapper around
`beartype.claw.beartype_this_package` |

<!-- markdownlint-enable MD013 -->

## Important boundaries

- The root `bearshape` import is optional-dependency-safe and does **not**
    require NumPy.
- `Tree` is not exported from the root module. Import it from `bearshape.optree`
    or `bearshape.jax`.
- `make_scalar_like_type` is not exported from the root module. Import it from
    `bearshape.numpy` or a backend module that re-exports it.
