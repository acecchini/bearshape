# Rename Project Identity to Bearshape

This ExecPlan is a living document. The sections `Progress`,
`Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must
be kept up to date as work proceeds.

This repository contains `PLANS.md` at the repository root. This document must
be maintained in accordance with `PLANS.md`.

## Purpose / Big Picture

The project is moving from its previous public identity to Bearshape. After this
plan is complete, users should install the PyPI distribution named
`bearshape`, import `bearshape` in Python code, read docs that consistently say
Bearshape, and see CI, tox, type-checker fixtures, docs, notebooks, and
packaging all validate that new identity.

This is intentionally a broad cleanup task. The goal is not to add new runtime
features; the goal is to make the library's public name, package metadata,
source package, tests, examples, docs, and release path coherent before deeper
production refactors begin.

## Progress

- [x] (2026-05-29 08:49Z) Created branch `codex/bearshape-rename` in worktree
  `/Users/ale/Code/bearshape-rename` from merged `origin/main`.
- [x] (2026-05-29 08:51Z) Pushed the branch and opened draft PR #6 targeting
  `main`.
- [x] (2026-05-29 09:04Z) Built a complete rename inventory from code, tests,
  docs, packaging, workflows, notebooks, and lock/config files.
- [x] (2026-05-29 09:05Z) Built the rename inventory, moved the package and
  public docs/example paths, and replaced the previous identifier across source,
  tests, docs, examples, workflows, lock/config files, and plan artifacts.
- [x] (2026-05-29 09:08Z) Decided not to add a short-lived compatibility
  surface for the previous import package.
- [x] (2026-05-29 09:10Z) Updated `README.md`, docs, notebooks, and
  `CHANGELOG.md` with concise Bearshape-facing text.
- [x] (2026-05-29 09:12Z) Ran `uv sync`; the environment rebuilt the editable
  distribution as `bearshape` and removed the previous installed distribution.
- [x] (2026-05-29 09:15Z) Verified direct imports and absence of the previous
  import package in the uv environment.
- [x] (2026-05-29 09:22Z) Validated hooks, runtime tests, direct type checkers,
  docs build, `tox -e dev`, and package build artifacts.
- [x] (2026-05-29 09:31Z) Recorded final PR #6 check evidence and asked the
  user for validation before merge.
- [x] Record final PR check evidence and ask the user for validation before
  merge.
- [x] Decide whether any short-lived compatibility surface for the previous
  import package is needed; default is no compatibility shim unless the user
  explicitly asks for one.
- [x] Update `README.md`, docs, notebooks, and `CHANGELOG.md` with concise
  user-facing rename notes.
- [x] Regenerate lock or generated files only when required by metadata changes.
- [x] Validate hooks, runtime tests, type-checker integration, docs build, and
  relevant tox environments.

## Surprises & Discoveries

- Observation: This work starts after the baseline audit and hook/CI hygiene
  PRs were merged into `main`.
  Evidence: branch `codex/bearshape-rename` was created from `origin/main` at
  commit `17bd2ee`, the merge commit for PR #4.
- Observation: A broad replacement also touched the worktree `.git` pointer
  file because it is a file, not a directory, in linked worktrees.
  Evidence: git commands failed until `.git` was restored to point at the
  original checkout's worktree metadata. Follow-up audits exclude both `.git`
  and `.git/**`.
- Observation: Live PyPI was not modified during this PR task.
  Evidence: no `uv publish` command was run. Local metadata, lockfile, built
  wheel/sdist names, and the GitHub trusted-publishing workflow now target
  `bearshape`.

## Decision Log

- Decision: Treat this as a clean public rename to `bearshape`.
  Rationale: The user asked to rename the repo, PyPI package, and project
  identity to Bearshape before release. Carrying a long-lived compatibility
  import alias for the previous identity would preserve stale surface area and
  add maintenance cost. If a compatibility shim is needed, it should be
  short-lived, explicit, tested, and documented as transitional.
  Date/Author: 2026-05-29 / Codex

- Decision: Keep feature behavior unchanged during this rename.
  Rationale: A repository-wide rename is already high risk. Runtime semantics,
  typing semantics, and backend behavior should remain stable so failures point
  to rename mistakes rather than unrelated feature work.
  Date/Author: 2026-05-29 / Codex

- Decision: Do not publish to PyPI during the PR.
  Rationale: Publishing is irreversible release work and should happen only
  after the PR is reviewed, merged, tagged, and explicitly approved.
  Date/Author: 2026-05-29 / Codex

## Outcomes & Retrospective

The rename is implemented locally in PR #6 and awaits user validation before
merge. The source package is `src/bearshape/`, the distribution metadata is
`bearshape`, docs and examples use Bearshape, and no compatibility package for
the previous import name was added.

Local validation passed:

- `uv --cache-dir .uv-cache sync`
- `uv --cache-dir .uv-cache run python -c "import bearshape; print(bearshape.__name__, bearshape.__version__)"`
- `uv --cache-dir .uv-cache run python -c "import bearshape.numpy as bnp; print(bnp.__name__)"`
- `uv --cache-dir .uv-cache run python -c "import importlib.util; print(importlib.util.find_spec('<previous import>'))"`
- old-name audit with `.git`, `site`, `.venv`, and `.tox` excluded: no matches
- `uv --cache-dir .uv-cache run pytest -n auto tests/`: 1063 passed, 5 skipped
- `uv --cache-dir .uv-cache run pyright src tests/typing`: 0 errors
- `uv --cache-dir .uv-cache run mypy src tests/typing`: no issues
- `uv --cache-dir .uv-cache run ty check src tests/typing`: all checks passed
- `uv --cache-dir .uv-cache run mkdocs build --clean`
- `uv --cache-dir .uv-cache run prek run -a`
- `uv --cache-dir .uv-cache run tox run -e dev`: 1063 passed, 5 skipped,
  coverage 91.20%
- `uv --cache-dir .uv-cache build`: built `bearshape-0.0.1.tar.gz` and
  `bearshape-0.0.1-py3-none-any.whl`

CuPy runtime validation remains deferred locally because this machine has no
CUDA GPU and `cupy` is not installed.

PR #6 validation passed on GitHub during this run:

- GitGuardian Security Checks
- Spell Check with Typos
- ruff
- test
- typecheck
- typecheck-compat
- `py310-bt022-jax05`
- `py310-bt022-numpy22`
- `py310-bt022-optree014`
- `py310-bt022-torch26`
- `py313-bt022-jax09`
- `py313-bt022-numpy24`
- `py313-bt022-optree019`
- `py313-bt022-torch210`
- `py313-bt022-type-mypy119`
- `py313-bt022-type-pyright1408`
- `py313-bt022-type-ty`

## Context and Orientation

The repository implements a runtime shape and dtype checking library whose
target Python import package and PyPI distribution name are both `bearshape`.

Important files and directories:

- `src/bearshape/` contains the target source package.
- `tests/` contains runtime tests and type-checker integration tests. Imports
  and expected strings in this tree must match the new package name.
- `tests/typing/` contains public static typing fixtures. These are product
  contract artifacts and must import the new package.
- `docs/`, `mkdocs.yml`, and `README.md` are user-facing docs. They must say
  Bearshape and show `bearshape` imports.
- `examples/` contains notebooks or examples that may embed package names in
  cells, metadata, or outputs.
- `pyproject.toml` owns package metadata, build-backend module name, uv config,
  checker settings, and dependency groups.
- `tox.toml` and `.github/workflows/` own release confidence and CI matrix
  behavior.
- `CHANGELOG.md` must record the major user-visible rename.
- `AGENTS.md` already describes the new Bearshape mission and should remain
  concise.

Use "distribution name" to mean the name users install from PyPI, as in
`uv add bearshape`. Use "import package" to mean the Python module users import,
as in `import bearshape`. This plan changes both.

## Plan of Work

First, build an inventory. Search for exact and case-insensitive references to
the previous identifier, GitHub URLs, docs paths, import statements, module
names, wheel names, notebook text, and generated docs references. Record the
counts and notable categories in this plan before editing.

Second, rename the source package to `src/bearshape/` and update all imports,
module references, doctest snippets, type-checker fixtures, and beartype claw
references. Update `pyproject.toml` so the project name is `bearshape` and the
uv build-backend module name is `bearshape`.

Third, update tests and typing fixtures. Runtime tests should import
`bearshape` and backend modules such as `bearshape.numpy`, `bearshape.jax`,
`bearshape.torch`, `bearshape.cupy`, and `bearshape.optree`. Typing fixtures
must use the same public syntax under the new import name. Expected error
messages should be updated only when they mention module names; semantics should
not change.

Fourth, update docs and examples. Rewrite the README as a concise Bearshape
intro. Update docs pages, MkDocs nav entries, module API paths, notebooks, and
examples so every shown command and import is real. Keep docs short and avoid
promising future behavior.

Fifth, update release and CI configuration. Check `.github/workflows/pypi.yml`,
docs workflows, tox environment names or descriptions, package build outputs,
and any lockfile metadata. Regenerate `uv.lock` only if `uv sync --locked` or
package metadata validation shows it is stale.

Sixth, validate in layers. Run fast hooks first, then runtime and typing tests,
then docs build, then relevant tox environments. CuPy runtime tests remain
deferred locally because the machine has no CUDA GPU.

## Concrete Steps

Run commands from the rename worktree:

    cd /Users/ale/Code/bearshape-rename

Confirm branch and status:

    git branch --show-current
    git status --short --branch

Build the inventory:

    rg -n --hidden --glob '!.git' --glob '!.git/**' <old-name-patterns> .
    find src -maxdepth 2 -type d -print

Rename source package and imports using file-aware edits, not blind global
replacement. Use `git mv` for package and docs/example path moves. Use
structured tooling when practical for notebooks and generated metadata.

Validate progressively:

    uv sync
    uv run prek run -a
    uv run pytest -n auto tests/test_typecheck.py
    uv run pytest -n auto tests/
    uv run pyright src tests/typing
    uv run mypy src tests/typing
    uv run ty check src tests/typing
    uv run mkdocs build --clean

Run relevant tox environments after the basic suite is green:

    uv run tox run -e dev
    uv run tox run -e py310-bt022-numpy22
    uv run tox run -e py313-bt022-numpy24
    uv run tox run -e py313-bt022-type-pyright1408
    uv run tox run -e py313-bt022-type-mypy119
    uv run tox run -e py313-bt022-type-ty

## Validation and Acceptance

The rename is accepted when Bearshape is the only production identity and all
changed surfaces prove it.

Required evidence:

- `python -c "import bearshape; print(bearshape.__name__)"` prints
  `bearshape`.
- `python -c "import bearshape.numpy as bnp; print(bnp.__name__)"` prints
  `bearshape.numpy` in an environment with NumPy installed.
- The package metadata names the distribution `bearshape`.
- No package for the previous import name exists unless an explicit
  transitional compatibility shim is approved and documented.
- Public docs and examples use `bearshape`.
- `uv run prek run -a` passes.
- Runtime tests and type-checker integration pass.
- Direct pyright, mypy, and ty runs pass.
- Docs build succeeds.
- Relevant tox environments pass.
- PR CI is green.

CuPy runtime validation is not required on this local machine because there is
no CUDA GPU. Any CuPy rename changes must still be syntax-checked and included
in CI or future GPU validation plans where possible.

## Idempotence and Recovery

This rename should be performed in small commits or amendable milestones. If a
rename command partially succeeds, inspect `git status --short` and use
file-scoped fixes rather than broad reset commands. Do not delete user-created
work outside `/Users/ale/Code/bearshape-rename`.

If generated files change unexpectedly, inspect the diff before keeping them.
Keep generated or lockfile changes only when a validation command proves they
are required.

## Artifacts and Notes

Initial setup evidence:

    Worktree: /Users/ale/Code/bearshape-rename
    Branch: codex/bearshape-rename
    Base: origin/main at 17bd2ee
    Draft PR: https://github.com/acecchini/bearshape/pull/6

Merged setup PRs:

    PR #5 Hook and CI hygiene before rename: merged into codex/baseline-audit
    PR #4 Baseline audit before Bearshape rename: merged into main

## Interfaces and Dependencies

Use the existing toolchain: `uv`, `pytest`, `prek`, `ruff`, `pyright`, `mypy`,
`ty`, `tox`, and MkDocs. Do not add runtime dependencies for the rename.

Public import paths at the end of this plan should include:

    import bearshape
    import bearshape.numpy
    import bearshape.jax
    import bearshape.torch
    import bearshape.cupy
    import bearshape.optree

The PyPI distribution name should be:

    bearshape

## Revision Notes

- 2026-05-29: Created the initial rename ExecPlan after merging the baseline
  audit and hook/CI hygiene setup stack into `main`.
- 2026-05-29: Updated the plan with draft PR #6 after pushing
  `codex/bearshape-rename`.
