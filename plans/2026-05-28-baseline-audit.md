# Baseline audit before Bearshape rename

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds.

This repository contains `PLANS.md` at the repository root. This document must be maintained in accordance with `PLANS.md`.

## Purpose / Big Picture

The project is being renamed from Shapix to Bearshape and prepared for a production-quality release under the beartype organization. Before changing package names, public APIs, CI, tox, docs, or implementation internals, this audit records what works today and what is already broken. The result should let a future contributor separate pre-existing failures from regressions introduced by the rename and cleanup work.

After this plan is complete, a maintainer should be able to read this file and know the current local baseline: which tests pass, which tests fail, which type checkers fail, which hooks fail, what coverage is deferred, and which areas should become separate follow-up plans.

## Progress

- [x] (2026-05-28 09:01Z) Created branch `codex/baseline-audit` in worktree `/Users/ale/Code/bearshape-baseline-audit`.
- [x] (2026-05-28 09:01Z) Added the agent workflow files needed for this audit: `AGENTS.md`, `CLAUDE.md` as a symlink to `AGENTS.md`, and `PLANS.md`.
- [x] (2026-05-28 09:01Z) Pushed `codex/baseline-audit` to GitHub. GitHub reported that the repository moved from `acecchini/shapix` to `acecchini/bearshape`.
- [ ] Open a draft PR for `codex/baseline-audit` against `main`.
- [ ] Run `uv sync` and record whether the locked development environment installs cleanly.
- [ ] Run local runtime tests with CuPy deferred because this machine does not currently have a CUDA-capable GPU.
- [ ] Run the current type-checking contract: `tests/test_typecheck.py`, pyright, mypy, and ty.
- [ ] Run local hooks with `uv run prek run -a`.
- [ ] Audit packaging, tox, CI, docs, README, CHANGELOG, and public import names for drift from the Bearshape target.
- [ ] Write a current contract map that links runtime features, typing fixtures, docs, and tests.
- [ ] Summarize follow-up work as separate candidate ExecPlans.

## Surprises & Discoveries

- Observation: The remote still appears locally as `https://github.com/acecchini/shapix.git`, but pushing reports that the repository moved.
  Evidence: `git push -u origin codex/baseline-audit` printed `This repository moved. Please use the new location: https://github.com/acecchini/bearshape.git`.
- Observation: Automatic PR creation is not available yet in this local session.
  Evidence: the GitHub connector timed out during startup twice, and `gh auth status` reported that the local token for account `acecchini` is invalid.

## Decision Log

- Decision: Start with a baseline audit rather than a rename.
  Rationale: Renaming first would mix pre-existing failures with rename regressions. The audit creates a factual starting point.
  Date/Author: 2026-05-28 / Codex
- Decision: Defer CuPy runtime validation locally.
  Rationale: CuPy needs a CUDA-capable GPU, and the current machine does not have one. CuPy coverage must be tracked explicitly instead of implied by CPU test runs.
  Date/Author: 2026-05-28 / Codex
- Decision: Keep this PR mostly non-invasive.
  Rationale: The purpose is to observe the current baseline. Fixes discovered during the audit should become separate, scoped plans unless a small workflow fix is required to complete the audit itself.
  Date/Author: 2026-05-28 / Codex

## Outcomes & Retrospective

This section is intentionally incomplete. Fill it in after the validation commands and contract audit are complete. It should compare the observed baseline against the project goal: a lean, production-ready Bearshape release with runtime behavior, static typing, docs, CI, tox, hooks, packaging, and publishing all aligned.

## Context and Orientation

The current repository is still named `shapix` in source paths and package metadata. The desired public identity is `bearshape`. The root package currently lives under `src/shapix/`, with backend modules for NumPy, JAX, Torch, CuPy, and optree-backed tree validation. The package metadata currently lives in `pyproject.toml`, tox configuration in `tox.toml`, GitHub workflows in `.github/workflows/`, documentation under `docs/`, and public examples in `README.md` plus docs pages.

The runtime product surface is runtime shape and dtype checking powered by beartype. Runtime behavior includes validators, decorators, shape matching, dtype matching, backend-specific conversion rules, tree validation, and error messages.

The static product surface is the annotation syntax accepted by type checkers. The current required checkers are pyright, mypy, and ty. Pyrefly is planned for addition after a separate plan. Zuban is only a possible future consideration and should not be added in this audit unless the user explicitly expands scope.

CuPy is a special backend for validation. Unlike NumPy, JAX CPU, Torch CPU, and optree, CuPy requires CUDA GPU support. This local audit must record CuPy as deferred instead of treating it as passed.

## Plan of Work

First, establish the repository workflow baseline. Confirm the branch and worktree, record the pushed branch, and open a draft PR if credentials allow it. If PR creation remains blocked by local authentication or connector availability, record the blocker and continue the audit without making code changes.

Second, install the current development environment with `uv sync`. Record whether dependency resolution and installation succeed. If installation fails because of local cache, network, or tool availability, record the exact failure and retry only when the retry is a clear environment fix rather than a code change.

Third, run the runtime test suite that can be exercised on this machine. Run all non-CuPy tests with pytest and `-n auto`. Do not run `tests/test_cupy.py` as proof of local support because this machine lacks a CUDA-capable GPU.

Fourth, run the static typing surface. Execute `tests/test_typecheck.py`, then run pyright, mypy, and ty directly against `src` and `tests/typing`.

Fifth, run hooks with `uv run prek run -a`. Record each failure as a current baseline issue. Do not fix hook output in this audit unless the hook failure prevents further audit commands from running.

Sixth, inspect contract artifacts. Read `pyproject.toml`, `tox.toml`, `.github/workflows/*.yml`, `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `docs/`, `src/shapix/`, `tests/`, and `tests/typing/`. Record obvious drift, duplicate or stale surfaces, rename requirements, missing test coverage, and docs that advertise behavior not proven by tests.

Seventh, update this ExecPlan with the observed results. The final audit should identify follow-up plans, not implement all fixes in one PR.

## Concrete Steps

Run all commands from the repository root of the audit worktree:

    cd /Users/ale/Code/bearshape-baseline-audit

Confirm branch and status:

    git branch --show-current
    git status --short --branch
    git remote -v

Install the current locked development environment:

    uv sync

Run local runtime tests except CuPy:

    uv run pytest -n auto tests/test_decorator.py tests/test_memo.py tests/test_dimensions.py tests/test_shape.py tests/test_dtypes.py tests/test_numpy.py tests/test_jax.py tests/test_torch.py tests/test_tree.py tests/test_coverage_edges.py

Run the typing contract:

    uv run pytest -n auto tests/test_typecheck.py
    uv run pyright src tests/typing
    uv run mypy src tests/typing
    uv run ty check src tests/typing

Run hooks:

    uv run prek run -a

Inspect repo contract artifacts:

    rg -n "shapix|shapix-rt|Shapix|bearshape|Bearshape" pyproject.toml tox.toml README.md CHANGELOG.md CONTRIBUTING.md docs src tests .github
    rg -n "cupy|CuPy|CUDA|gpu|GPU" pyproject.toml tox.toml README.md docs tests .github
    rg -n "pyright|mypy|ty|pyrefly|zuban" pyproject.toml tox.toml tests docs .github

## Validation and Acceptance

This audit is accepted when this file contains a factual current baseline with command outcomes. The acceptance is not that the suite passes. The acceptance is that the current state is known, reproducible, and split into follow-up work.

Required evidence:

- `uv sync` result recorded.
- Non-CuPy pytest result recorded.
- CuPy explicitly marked as deferred until CUDA GPU validation exists.
- `tests/test_typecheck.py` result recorded.
- Direct pyright, mypy, and ty results recorded.
- `prek` hook result recorded.
- Rename drift from `shapix` / `shapix-rt` to `bearshape` inventoried.
- CI, tox, packaging, docs, and typing fixture issues inventoried.
- Follow-up candidate ExecPlans listed with clear scopes.

## Idempotence and Recovery

The audit commands are read-only except for environment installation, caches, and generated test artifacts. They can be rerun safely. If `uv sync` or test commands fail because of missing dependencies, record the exact error first. Do not delete caches, rewrite lockfiles, or change dependency ranges unless a separate plan approves that work.

If local GitHub PR creation remains blocked, use the pushed branch URL as the recovery path:

    https://github.com/acecchini/bearshape/pull/new/codex/baseline-audit

## Artifacts and Notes

Initial branch evidence:

    Worktree: /Users/ale/Code/bearshape-baseline-audit
    Branch: codex/baseline-audit
    Initial commit: 2c5f93f Add agent workflow instructions
    Pushed branch: origin/codex/baseline-audit
    Remote move notice: https://github.com/acecchini/bearshape.git

PR creation evidence:

    gh auth status reported an invalid local token for acecchini.
    The GitHub connector timed out during startup twice.

## Interfaces and Dependencies

The audit should not add runtime dependencies. It uses the existing project toolchain declared in `pyproject.toml`: uv for environment management, pytest for tests, pyright, mypy, and ty for static typing, prek for hooks, and tox for CI-oriented matrix validation. Pyrefly and zuban are out of scope for this audit except as future work items.

The main files and directories under inspection are:

- `pyproject.toml` for package metadata, dependency groups, checker settings, and uv build settings.
- `tox.toml` for version and backend matrix validation.
- `.github/workflows/` for CI, docs, nightly, and PyPI publishing workflows.
- `src/shapix/` for the current runtime package.
- `tests/` for runtime behavior.
- `tests/typing/` for static typing fixtures.
- `README.md`, `docs/`, `CONTRIBUTING.md`, and `CHANGELOG.md` for public contract artifacts.

## Revision Notes

- 2026-05-28: Created the initial baseline audit ExecPlan after setting up the branch and worktree. This version records the intended audit process, known PR creation blocker, and CuPy deferral.
