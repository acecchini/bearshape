---
description: Install bearshape with your preferred array backend.
---

<!-- markdownlint-disable-file MD046 -->

# Installation

## Requirements

- **Python** >= 3.10
- **beartype** >= 0.23.0rc0, < 0.24, installed automatically with `bearshape`

## Install with pip

```bash
pip install bearshape
```

The distribution name and import package are both `bearshape`:

```python
import bearshape
```

bearshape intentionally does **not** use extras such as `bearshape[numpy]`.
Install `bearshape` and your backend packages explicitly.

=== "NumPy"

    ```bash
    pip install bearshape numpy
    ```

=== "PyTorch"

    ```bash
    pip install bearshape numpy torch
    ```

=== "JAX"

    ```bash
    pip install bearshape numpy jax
    ```

=== "CuPy"

    ```bash
    pip install bearshape numpy cupy
    ```

=== "NumPy + OpTree"

    ```bash
    pip install bearshape numpy optree  # or install jax and use bearshape.jax.Tree
    ```

!!! note `bearshape.jax`, `bearshape.torch`, and `bearshape.cupy` require `numpy`

alongside the backend. The lightweight root import `import bearshape` does not.

## Install with uv

```bash
uv add bearshape
```

## Optional dependencies

| Package | Purpose | | -------- |
------------------------------------------------------------ | | `numpy` | NumPy
array aliases, `ScalarLike`, and backend dtype helpers | | `torch` | PyTorch
tensor aliases and Torch `Like` types | | `jax` | JAX array aliases, JAX `Like`
types, and JAX `Tree` | | `cupy` | CuPy array aliases and CuPy `Like` types | |
`optree` | Explicit OpTree backend via `bearshape.optree.Tree` |

## Import boundaries

The root package is designed to stay optional-dependency-safe:

```python
import bearshape

print(bearshape.__version__)
print(bearshape.N, bearshape.C)
```

That works even in a plain source checkout without installed package metadata.
In that case `__version__` falls back to a non-empty string such as `0+unknown`.

Backend modules are stricter:

- `bearshape.numpy` needs `numpy`
- `bearshape.jax` needs `jax` and `numpy`
- `bearshape.torch` needs `torch` and `numpy`
- `bearshape.cupy` needs `cupy` and `numpy`
- `bearshape.optree` needs `optree`

## Verify installation

```python
import bearshape
print(bearshape.__version__)
```

Then verify the backend you actually plan to use:

```python
from bearshape import N, C
from bearshape.numpy import F32
```
