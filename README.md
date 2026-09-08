# bearshape

[![Python 3.10-3.14](docs/assets/images/python_versions_badge.svg)](https://www.python.org/)
[![Docs](https://img.shields.io/badge/docs-live-526CFE?style=flat-square&logo=readthedocs&logoColor=white&labelColor=1F2937)](https://acecchini.github.io/bearshape/)

Runtime shape and dtype checking for NumPy, JAX, PyTorch, CuPy, and
tree-structured containers, powered by
[beartype](https://github.com/beartype/beartype).

```python
from beartype import beartype
from bearshape import N, C
from bearshape.numpy import F32


@beartype
def normalize(x: F32[N, C]) -> F32[N, C]:
  return x / x.sum(axis=1, keepdims=True)
```

bearshape turns annotations such as `F32[N, C]`, `F32Like[~B, C]`,
`F32[Value("size")]`, and `Tree[F32[N], T]` into runtime-validated contracts.
Named dimensions are shared within a function call, so mismatched shapes fail at
the boundary instead of later in array code.

## Install

```bash
pip install bearshape
```

bearshape keeps the root import lightweight. Install the array backend packages
you use explicitly:

```bash
pip install bearshape numpy
pip install bearshape numpy torch
pip install bearshape numpy jax
pip install bearshape numpy cupy
pip install bearshape numpy optree
```

## What It Checks

- strict array type, dtype, and shape contracts
- backend-aware `Like[...]` conversion checks
- scalar-like values and constrained runtime `Value(...)` dimensions
- tree leaf and structure annotations through JAX or OpTree
- annotation syntax exercised by pyright, mypy, ty, and pyrefly consumer
    fixtures

## Public Surface

Import dimensions, `Value`, `Scalar`, `DtypeSpec`, `check`, and `check_context`
from `bearshape`.

Import backend aliases from backend modules:

```python
from bearshape.numpy import F32, F32Like
from bearshape.jax import Tree
from bearshape.torch import I64
```

The root package does not import NumPy or any backend. Backend modules require
their own runtime dependencies.

## Development

```bash
uv sync --locked
uv run --locked prek run -a
uv run --locked pytest tests/ -n auto
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for checker, backend and artifact
validation. CuPy runtime tests require CUDA hardware. The
[static typing guide](https://acecchini.github.io/bearshape/features/static-typing/)
distinguishes checker-supported annotations from runtime-only shape expressions.
