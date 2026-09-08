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

## Check release archives

Build the source distribution first, then build the wheel from that archive:

```bash
uv build --sdist
uv build dist/bearshape-<version>.tar.gz --wheel
uv run --locked --only-group dev python tools/check_distribution.py \
  dist/bearshape-<version>-py3-none-any.whl dist/bearshape-<version>.tar.gz
```

Replace `<version>` with the project version. The check verifies license text,
metadata, inline typing information, matching package contents, and downstream
test inputs. It prints artifact hashes for release evidence. The source archive
includes the tests, lockfile and configuration needed to run `uv sync --locked`
and `uv run --locked pytest`. CuPy still requires a separate CUDA environment.

## Candidate validation

CI and nightly use `.github/workflows/validate.yml`. Current locked CPU backends
run on Python 3.10–3.14 on Linux, with endpoint jobs on macOS and Windows.
Four-checker consumer tests run on every supported Python on Linux. Separate tox
jobs exercise backend and checker floors with exact beartype 0.23.0rc0.
`tools/validate_runtime.py` fails if an expected backend is absent or Torch is a
CUDA/ROCm build in a CPU lane. Optional local skips do not establish support.

Use `uv run --locked prek run -a` for the normal hooks and
`uv run --locked prek run actionlint -a --stage manual` for workflow checks.
Pre-push checks use the locked four-checker harness and runtime suite. The
required CI gate accepts only successful completion of every required job. CuPy
GPU validation remains a separate hardware-backed requirement.

To validate the installed artifact after building the sdist and its wheel, run:

```bash
uv run --locked python tools/check_installed.py \
  dist/*.whl dist/*.tar.gz --python 3.10
```

Repeat with `--python 3.14`. The command installs locked dependencies and the
wheel normally in a temporary environment, then runs copied runtime and checker
fixtures with no package source directory. It reports artifact hashes and
installed module origins. `--installed-package` is an explicit pytest mode for
this consumer check; ordinary source validation continues to include `src`.

## Validate and publish a release

Run a validation-only workflow before making a release decision:

```bash
gh workflow run pypi.yml --ref main -f ref=<reviewed-commit> -F publish=false
```

This resolves one commit, runs the complete shared matrix, and produces
`candidate-distributions` plus `release-evidence`. The evidence records the
source SHA, version, artifact hashes and run URL. A failed required check
prevents publication. GPU runtime evidence and open contract decisions still
require review; CPU CI does not replace them.

Publication requires a canonical `v<project-version>` tag already in `main`
history. Both the workflow and package must come from that exact tag and commit.
Versions use `X.Y.Z` with an optional `aN`, `bN` or `rcN` suffix. A GitHub
release must be marked as a prerelease exactly when its version has such a
suffix. After explicit owner approval, publish that GitHub release, or dispatch
the workflow from the same tag with `publish=true`. Publishing downloads the
same tested distributions and does not rebuild them. Only that job receives OIDC
permission and enters the `pypi` environment.

Before enabling publication, configure required review for `pypi`, prevent
self-approval and administrator bypass, and limit its deployment policy to
release tags. Protect `main` and release tags, and require the final validation
check on pull requests. Confirm the PyPI trusted publisher identifies the actual
repository owner/name, `pypi.yml`, and environment `pypi`. The workflow does not
create these controls. The 2026-09-08 inspection found unprotected `main`, no
repository rulesets and no `pypi` approval reviewers; PyPI configuration remains
unverified. Ownership transfer requires rechecking publisher identity and docs
hosting before changing public URLs.
