# Rename Shapix to Bearshape

This ExecPlan is a living document. The sections `Progress`,
`Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must
be kept up to date as work proceeds.

This repository contains `PLANS.md` at the repository root. This document must
be maintained in accordance with `PLANS.md`.

## Purpose / Big Picture

The project is moving from the temporary Shapix identity to Bearshape. After
this plan is complete, users should install the PyPI distribution named
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
- [ ] Build a complete rename inventory from code, tests, docs, packaging,
  workflows, notebooks, and lock/config files.
- [ ] Rename package metadata, source package, imports, tests, typing fixtures,
  docs, examples, workflows, and release configuration from Shapix to Bearshape.
- [ ] Decide whether any short-lived compatibility surface for `shapix` imports
  is needed; default is no compatibility shim unless the user explicitly asks
  for one.
- [ ] Update `README.md`, docs, notebooks, and `CHANGELOG.md` with concise
  user-facing rename notes.
- [ ] Regenerate lock or generated files only when required by metadata changes.
- [ ] Validate hooks, runtime tests, type-checker integration, docs build, and
  relevant tox environments.
- [ ] Record final PR check evidence and ask the user for validation before
  merge.

## Surprises & Discoveries

- Observation: This work starts after the baseline audit and hook/CI hygiene
  PRs were merged into `main`.
  Evidence: branch `codex/bearshape-rename` was created from `origin/main` at
  commit `17bd2ee`, the merge commit for PR #4.

## Decision Log

- Decision: Treat this as a clean public rename from `shapix` to `bearshape`.
  Rationale: The user asked to rename the repo, PyPI package, and project
  identity to Bearshape before release. Carrying a long-lived `shapix` import
  alias would preserve stale identity and add maintenance surface. If a
  compatibility shim is needed, it should be short-lived, explicit, tested, and
  documented as transitional.
  Date/Author: 2026-05-29 / Codex

- Decision: Keep feature behavior unchanged during this rename.
  Rationale: A repository-wide rename is already high risk. Runtime semantics,
  typing semantics, and backend behavior should remain stable so failures point
  to rename mistakes rather than unrelated feature work.
  Date/Author: 2026-05-29 / Codex

## Outcomes & Retrospective

This section is incomplete until the rename is implemented and validated. At
completion, it must state what changed, what commands passed, what CI proved,
what remains deferred, and whether any `shapix` compatibility surface exists.

## Context and Orientation

The repository currently implements a runtime shape and dtype checking library
under the Python import package `shapix` and the PyPI distribution name
`shapix-rt`. The target import package and distribution name are both
`bearshape`.

Important files and directories:

- `src/shapix/` contains the current source package. This should become
  `src/bearshape/`.
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
`shapix`, `Shapix`, `shapix-rt`, GitHub URLs, docs paths, import statements,
module names, wheel names, notebook text, and generated docs references. Record
the counts and notable categories in this plan before editing.

Second, rename the source package. Move `src/shapix/` to `src/bearshape/` and
update all imports, module references, doctest snippets, type-checker fixtures,
and beartype claw references. Update `pyproject.toml` so the project name is
`bearshape` and the uv build-backend module name is `bearshape`.

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

    rg -n "shapix|Shapix|SHAPIX|shapix-rt|acecchini/shapix" .
    find src -maxdepth 2 -type d -print

Rename source package and imports using file-aware edits, not blind global
replacement. Use `git mv src/shapix src/bearshape` for the package directory.
Use structured tooling when practical for notebooks and generated metadata.

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
- `src/shapix/` no longer exists unless an explicit transitional compatibility
  shim is approved and documented.
- Public docs and examples use `bearshape`, not `shapix`.
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
