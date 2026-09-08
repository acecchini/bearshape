# Contributing

## Local Development

```bash
uv sync --locked
uv run --locked prek install
uv run --locked prek run -a
uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
uv run --locked pytest tests/test_typecheck.py -q
```

The checker harness runs pyright, mypy, ty and pyrefly against source and real
positive/negative/inference consumers, with interpreter-matched settings. Direct
checker commands are useful for debugging but do not replace that harness. Use
`-n auto` for runtime tests; use `-n0` for narrow serial debugging.

The default groups include CPU NumPy/JAX/Torch/optree, all four checkers, tests,
docs, notebook and development tools. Use exact
`uv sync --locked --only-group <group>` or a fresh venv when proving dependency
isolation: `uv run --only-group` can retain packages from earlier runs. CuPy
runtime validation needs real CUDA hardware. The
[handoff report](docs/maintainers/production-readiness.md) records GPU evidence
and the accepted limits of native CuPy static typing.

Agent instructions are shared by `AGENTS.md` and the `CLAUDE.md` symlink.
`PLANS.md` describes major-work plans; [tools/README.md](tools/README.md)
describes the validation scripts, their inputs and what their results prove.

## Tox environments and CI

Runtime factors use `{python}-{beartype}-{backend}`; checker factors use
`{python}-{beartype}-type-{checker}`. For example:

```bash
uv run --locked tox list
uv run --locked tox run -e py310-bt023rc0-cpu
uv run --locked tox run -e py314-bt023rc0-cpu
uv run --locked tox run -e py310-bt023rc0-numpy22
uv run --locked tox run -e py313-bt023rc0-type-pyright1408
uv run --locked tox run -e py313-bt023rc0-type-mypy119
uv run --locked tox run -e py313-bt023rc0-type-ty
uv run --locked tox run -e py313-bt023rc0-type-pyrefly
```

Type environments install all CPU backends. CuPy is not part of those lanes.
`dev` uses the current lock; explicit backend/checker factors exercise the
configured compatibility ranges. Every candidate lane requires exact beartype
0.23.0rc0 today. The owner permits a later candidate for supported native-union
integration; the current rc0 defect remains a release blocker.

Pull requests, main pushes, nightly and candidate validation use the same
required matrix in `.github/workflows/validate.yml`. When adding a version,
update `tox.toml`, `tools/validate_tox_env.py`, the runtime preflight, lockfile
and shared workflow as applicable. The dependency range alone does not prove
compatibility with a new version.

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

## Documentation validation and deployment

```bash
uv run --locked --only-group docs zensical build --clean
uv run --locked --only-group docs python tools/check_docs.py
uv run --locked python tools/check_notebook.py
```

CI validates rendered structures, snippets and notebook execution. Main/docs
pushes build Pages artifacts but do not deploy them. After explicit deployment
approval, dispatch `docs.yml` from the reviewed `main` or `docs` branch. Only
its deployment job receives Pages/OIDC write permissions and enters the
`github-pages` environment. Merging code does not authorize deployment.
