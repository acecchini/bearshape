# Hook and CI hygiene before Bearshape rename

This ExecPlan is a living document. The sections `Progress`,
`Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must
be kept up to date as work proceeds.

This repository contains `PLANS.md` at the repository root. This document must
be maintained in accordance with `PLANS.md`.

## Purpose / Big Picture

The baseline audit found that the core runtime and typing tests pass, but the
local hook suite and PR spelling job are not green. This matters because the
next major task is the Shapix to Bearshape rename, which will touch many files.
Before that larger rename, the formatting, spelling, and workflow checks should
be predictable so the rename diff is not mixed with hook noise.

After this change, a maintainer should be able to run the local hook command and
inspect PR checks without seeing known hygiene failures unrelated to product
behavior. CuPy runtime validation remains out of scope because it requires a
CUDA-capable GPU environment.

## Progress

- [x] (2026-05-28 13:29Z) Created branch `codex/hook-ci-hygiene` in worktree
  `/Users/ale/Code/bearshape-hook-ci-hygiene`, stacked on
  `codex/baseline-audit`.
- [ ] Push the branch and open a draft PR targeting `codex/baseline-audit`.
- [ ] Reproduce the local `uv run prek run -a` failure in this clean worktree.
- [ ] Reproduce or inspect the PR spelling failure on `npt.NDArray`.
- [ ] Decide the smallest configuration or content changes that make hook and
  CI behavior intentional.
- [ ] Implement the scoped hygiene fixes.
- [ ] Validate local hooks and relevant CI checks.
- [ ] Update this plan with evidence and follow-up work.

## Surprises & Discoveries

- Observation: This branch is intentionally stacked on `codex/baseline-audit`.
  Evidence: the baseline audit PR contains `AGENTS.md`, `PLANS.md`, and the
  baseline ExecPlan; those files are needed for the workflow but are not yet on
  `main`.

## Decision Log

- Decision: Target this PR at `codex/baseline-audit`, not `main`.
  Rationale: Hook and CI hygiene is the next task after the baseline audit and
  depends on the workflow files introduced there. Stacking keeps the cleanup
  isolated without duplicating setup work on `main`.
  Date/Author: 2026-05-28 / Codex
- Decision: Keep CuPy runtime validation out of this plan.
  Rationale: CuPy requires CUDA GPU support. This plan is about hook and CI
  hygiene that can be validated locally and in ordinary PR CI.
  Date/Author: 2026-05-28 / Codex

## Outcomes & Retrospective

This section is incomplete until the fixes and validation are done. It should
state exactly which local hooks and PR checks are green, which checks remain
deferred or intentionally failing, and what follow-up work should happen before
the Bearshape rename.

## Context and Orientation

The previous ExecPlan at `plans/2026-05-28-baseline-audit.md` recorded the
baseline. The important findings for this plan are that `uv sync`, non-CuPy
pytest, typechecker integration, direct pyright, direct mypy, direct ty, and
`tox run -e dev` all pass. The known hygiene issues are separate from runtime
correctness.

Local hook configuration lives in `.pre-commit-config.yaml`. The project uses
`prek`, not the older `pre-commit` CLI. Markdown lint configuration lives in
`.markdownlint.jsonc`. Package and checker configuration live in
`pyproject.toml`. GitHub workflows live in `.github/workflows/`.

The baseline audit found two concrete hygiene problems. First, running
`uv run prek run -a` modified files and then failed, including markdown lint
failures involving `PLANS.md` and the baseline audit ExecPlan. Second, PR CI
spelling failed because the GitHub workflow runs `typos .` and reports
`npt.NDArray` in `examples/shapix_tour.ipynb` as `ND` should be `AND`.

The current worktree starts from the committed baseline audit branch and is
clean. A different worktree, `/Users/ale/Code/bearshape-baseline-audit`, still
contains hook-generated uncommitted edits from the previous audit run. Do not
use that dirty worktree for implementation in this plan.

## Plan of Work

First, reproduce the local hook failure from this clean worktree. Run
`uv run prek run -a` and record which hooks modify files and which hooks fail.
Inspect the resulting diff before keeping any formatter changes.

Second, inspect the spelling failure. Use the PR logs if available and run the
same spelling command locally when possible. Determine whether the fix belongs
in typos configuration, notebook content, or workflow alignment. The expected
candidate is an intentional `typos` ignore for the identifier fragment `ND`
when it appears in `NDArray`, because `npt.NDArray` is valid NumPy typing
syntax.

Third, resolve the markdown hook conflict. The solution must make `PLANS.md`
and plan files compatible with the configured hooks without weakening linting
broadly. Prefer narrow markdownlint configuration or file-specific hook
exclusions only when they match the purpose of ExecPlans.

Fourth, reduce formatter churn. If prettier, mdformat, or other hooks rewrite
generated or asset files, decide whether those files should be formatted,
excluded, or committed as intentional normalization. Do not accept large
generated-asset churn without a reason.

Fifth, validate. Run `uv run prek run -a`. Then run targeted checks affected by
the changes, such as `uv run pytest -n auto tests/test_typecheck.py` if typing
fixtures or config change. Inspect PR checks after pushing.

## Concrete Steps

Run all commands from the hook hygiene worktree:

    cd /Users/ale/Code/bearshape-hook-ci-hygiene

Confirm branch and status:

    git branch --show-current
    git status --short --branch

Reproduce local hooks:

    uv run prek run -a

Inspect hook-generated diffs:

    git status --short
    git diff --stat
    git diff -- .pre-commit-config.yaml .markdownlint.jsonc pyproject.toml
    git diff -- PLANS.md plans/2026-05-28-hook-ci-hygiene.md

Inspect spelling behavior:

    uv run typos .

If `typos` is not available through `uv run`, use the hook command through
`prek` and record the limitation instead of adding a new dependency just for the
audit.

Validate after fixes:

    uv run prek run -a
    uv run pytest -n auto tests/test_typecheck.py

## Validation and Acceptance

This plan is accepted when hook and CI hygiene is explicit and reproducible.

Required evidence:

- The branch and draft PR exist.
- The local `prek` failure has been reproduced or, if already fixed by the
  first change, explained with evidence.
- The `npt.NDArray` spelling failure has a narrow, documented fix.
- Markdown lint and ExecPlan formatting no longer conflict.
- Formatter churn in generated or asset files is either avoided, intentionally
  committed, or documented as a follow-up.
- `uv run prek run -a` passes locally, or any remaining failure is explicitly
  out of scope with a precise reason.
- Relevant PR checks pass, especially spelling, ruff, typecheck, and
  typecheck-compat.

## Idempotence and Recovery

The hook command may rewrite files. Always inspect `git diff --stat` before
staging. If hooks create broad unrelated churn, do not commit it blindly. Either
exclude the generated files with a narrow configuration change or ask the user
whether the normalization should be accepted.

This branch is stacked on `codex/baseline-audit`. If the baseline audit branch
changes, rebase or recreate this worktree only after inspecting the diff.

## Artifacts and Notes

Initial branch evidence:

    Worktree: /Users/ale/Code/bearshape-hook-ci-hygiene
    Branch: codex/hook-ci-hygiene
    Base: codex/baseline-audit at e0522b0

Known failure evidence from the baseline audit:

    uv run prek run -a failed.
    end-of-file-fixer modified PLANS.md.
    markdownlint-fix failed on PLANS.md and the baseline audit ExecPlan.
    The PR spelling job failed on npt.NDArray in examples/shapix_tour.ipynb.

## Interfaces and Dependencies

The plan should use the existing toolchain: `uv`, `prek`, `typos`,
`markdownlint-fix`, `mdformat`, `prettier`, `ruff`, pytest, and GitHub Actions.
Do not add new runtime dependencies. If a dev-only dependency or hook version
change is needed, explain why and validate it through the hook suite.

Files most likely to change are `.pre-commit-config.yaml`,
`.markdownlint.jsonc`, `pyproject.toml`, `.github/workflows/ci.yml`, and
possibly the notebook or docs files that trigger spelling or formatter issues.

## Revision Notes

- 2026-05-28: Created the initial hook and CI hygiene ExecPlan stacked on the
  baseline audit branch.
