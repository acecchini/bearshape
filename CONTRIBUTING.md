# Contributing

## Local Development

```bash
uv sync
uv run prek install
uv run prek run -a
uv run pytest -n auto tests/
uv run pytest -n auto tests/test_typecheck.py
uv run pyright src tests/typing
uv run mypy src tests/typing
uv run ty check src tests/typing
```

Use `-n auto` by default. Use `-n0` only when debugging a narrow failure that
needs serial execution.

CuPy runtime tests require CUDA and are deferred on CPU-only machines.

## Tox Environments

Runtime environments use:

```text
{python}-{beartype}-{backend}
```

Examples:

```bash
uv run tox run -e py310-bt022-numpy22
uv run tox run -e py313-bt022-numpy24
uv run tox run -e py313-bt022-jax09
```

Type-checking environments use:

```text
{python}-{beartype}-type-{checker}
```

Examples:

```bash
uv run tox run -e py313-bt022-type-pyright1408
uv run tox run -e py313-bt022-type-mypy119
uv run tox run -e py313-bt022-type-ty
```

The `type` factor installs all supported backends so public typing fixtures can
resolve imports.

## CI Tiers

- Pull requests run installable Python/backend floor and ceiling jobs plus the
    current type-checker contract.
- Pushes to `main` broaden runtime and checker coverage.
- Nightly jobs cover the wider compatibility matrix.

When adding a backend version, update `tox.toml`, `tools/validate_tox_env.py`,
and the GitHub workflow matrix together.
