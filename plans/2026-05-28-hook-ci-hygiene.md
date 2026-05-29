# Hook and CI hygiene before bearshape rename

This ExecPlan is a living document. The sections `Progress`,
`Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must
be kept up to date as work proceeds.

This repository contains `PLANS.md` at the repository root. This document must
be maintained in accordance with `PLANS.md`.

## Purpose / Big Picture

The baseline audit found that the core runtime and typing tests pass, but the
local hook suite and PR spelling job are not green. This matters because the
next major task is the bearshape rename, which will touch many files. Before
that larger rename, the formatting, spelling, and workflow checks should be
predictable so the rename diff is not mixed with hook noise.

After this change, a maintainer should be able to run the local hook command and
inspect PR checks without seeing known hygiene failures unrelated to product
behavior. CuPy runtime validation remains out of scope because it requires a
CUDA-capable GPU environment.

## Progress

- [x] (2026-05-28 13:29Z) Created branch `codex/hook-ci-hygiene` in worktree
  `/Users/ale/Code/bearshape-hook-ci-hygiene`, stacked on
  `codex/baseline-audit`.
- [x] (2026-05-28 13:32Z) Pushed the branch and opened draft PR #5 targeting
  `codex/baseline-audit`.
- [x] (2026-05-28 13:34Z) Reproduced the local `uv run prek run -a` failure in
  this clean worktree.
- [x] (2026-05-28 13:35Z) Inspected the spelling behavior for `npt.NDArray`.
- [x] (2026-05-28 13:36Z) Decided the smallest configuration changes that make
  hook and CI behavior intentional.
- [x] (2026-05-28 13:37Z) Implemented the scoped hygiene fixes.
- [x] (2026-05-28 13:39Z) Validated local hooks, typing integration, and docs
  build.
- [x] (2026-05-28 13:42Z) Pushed the cleanup commit and inspected PR checks.
- [x] (2026-05-28 13:51Z) Diagnosed remaining compatibility-matrix failures.
- [x] (2026-05-28 14:26Z) Replaced impossible Python/backend matrix products
  with explicit installable CI and tox environments.
- [x] (2026-05-28 14:33Z) Validated hooks and the Python 3.10 replacement
  backend jobs locally.
- [x] (2026-05-28 14:39Z) Pushed the matrix fix and inspected PR checks.
- [x] (2026-05-28 14:39Z) Updated this plan with final PR check evidence and
  follow-up work.

## Surprises & Discoveries

- Observation: This branch is intentionally stacked on `codex/baseline-audit`.
  Evidence: the baseline audit PR contains `AGENTS.md`, `PLANS.md`, and the
  baseline ExecPlan; those files are needed for the workflow but are not yet on
  `main`.
- Observation: `uv sync` succeeded in this worktree and installed the locked
  development environment, with only the existing packaging warning about the
  deprecated MIT license classifier.
- Observation: The first `uv run prek run -a` failed because hooks rewrote or
  rejected non-product files. Evidence: `end-of-file-fixer` touched `PLANS.md`,
  markdown hooks failed on `PLANS.md` and plan files, `typos` wanted to rewrite
  valid `npt.NDArray` notebook text, and Prettier rewrote the large
  `docs/assets/js/tesseract.js` asset.
- Observation: `uv run typos .` is not available from the project environment.
  Evidence: the command failed to spawn `typos`. The usable local spelling path
  is the configured `prek` hook, and PR CI runs its own `typos .` action.
- Observation: `docs/stylesheets/extra.css` and `mkdocs.yml` receive small,
  deterministic Prettier normalizations. Evidence: the CSS diff only wraps long
  declarations and radial-gradient arguments; the MkDocs diff normalizes nested
  nav indentation. `uv run mkdocs build --clean` still succeeds.
- Observation: After the hook cleanup commit, PR #5 passed spelling, ruff,
  typecheck, typecheck-compat, locked dev tests, and most compatibility jobs,
  but failed `py310-bt022-numpy24` and `py310-bt022-jax09` before tests ran.
  Evidence: CI logs show NumPy 2.4.1+ and JAX 0.9 require Python 3.11+, while
  those jobs ran on Python 3.10.20.

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
- Decision: Exclude `AGENTS.md`, `PLANS.md`, and `plans/*.md` from `mdformat`
  and `markdownlint-fix`.
  Rationale: These files are workflow instructions and living ExecPlans with
  intentionally prescriptive formatting. Generic markdown reflow and lint rules
  were rewriting or rejecting plan structure instead of finding product issues.
  The exclusion is narrow and keeps markdown hooks active for docs and README
  files.
  Date/Author: 2026-05-28 / Codex
- Decision: Add `ND` to `tool.typos.default.extend-words`.
  Rationale: `npt.NDArray` is valid NumPy typing syntax and must not be
  rewritten to `npt.ANDArray`. A narrow accepted word preserves the public
  typing example without disabling spelling checks elsewhere.
  Date/Author: 2026-05-28 / Codex
- Decision: Exclude `docs/assets/js/tesseract.js` from Prettier.
  Rationale: The hook rewrites a large visual asset in a branch whose purpose is
  CI hygiene. That churn would obscure the actual fix. Smaller Prettier
  normalizations in CSS and MkDocs configuration are kept because they are
  deterministic, readable, and validated by the docs build.
  Date/Author: 2026-05-28 / Codex
- Decision: Use explicit CI and default tox compatibility environments instead
  of product matrices that generate unsatisfiable Python/backend pairs.
  Rationale: Python support and backend release floors move independently.
  Python 3.10 should still be covered with supported backend floor versions,
  while Python 3.12 and 3.13 cover current backend ceiling versions. This keeps
  CI meaningful without pretending Python 3.10 can install NumPy 2.4 or JAX 0.9.
  Date/Author: 2026-05-28 / Codex

## Outcomes & Retrospective

Local hook hygiene is now explicit. `uv run prek run -a` passes from a clean
hook hygiene worktree after the narrow exclusions and spelling configuration.
The typing integration suite still passes, and the docs still build.

The first PR check pass proved that the hook hygiene failures are fixed. The
remaining red checks were compatibility-matrix dependency resolution failures,
not product test failures. The matrix now enumerates installable floor and
ceiling jobs explicitly, and PR #5 is green after the matrix fix.

CuPy runtime validation remains intentionally deferred because the local machine
has no CUDA GPU.

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
`npt.NDArray` in `examples/bearshape_tour.ipynb` as `ND` should be `AND`.

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
    The PR spelling job failed on npt.NDArray in examples/bearshape_tour.ipynb.

Draft PR evidence:

    PR: https://github.com/acecchini/bearshape/pull/5
    Base: codex/baseline-audit

Reproduction evidence:

    uv sync
    Resolved 99 packages and built bearshape successfully.
    Warning: License classifiers are deprecated; use license expressions.

    uv run prek run -a
    end-of-file-fixer modified PLANS.md.
    markdownlint-fix failed on PLANS.md and plan files.
    typos wanted to rewrite npt.NDArray to npt.ANDArray.
    prettier rewrote docs/assets/js/tesseract.js.

    uv run typos .
    Failed to spawn: typos

Validation evidence:

    uv run prek run -a
    All configured hooks passed.

    uv run pytest -n auto tests/test_typecheck.py
    30 passed in 36.91s

    uv run mkdocs build --clean
    Documentation built successfully in 0.29 seconds.
    MkDocs emitted the existing Material for MkDocs 2.0 compatibility warning.

PR check evidence after the hook cleanup commit:

    Spell Check with Typos: passed
    ruff: passed
    typecheck: passed
    typecheck-compat: passed
    test: passed
    py310-bt022-numpy24: failed during dependency resolution
    py310-bt022-jax09: failed during dependency resolution

Compatibility failure evidence:

    py310-bt022-numpy24 tried to install numpy>=2.4,<2.5 on Python 3.10.20.
    NumPy 2.4.0 is yanked and NumPy 2.4.1+ requires Python >=3.11.

    py310-bt022-jax09 tried to install jax[cpu]>=0.9,<0.10 on Python 3.10.20.
    JAX 0.9 requires Python >=3.11.

Matrix fix validation evidence:

    uv run tox list
    Listed explicit default tox environments without the unsatisfiable
    Python 3.10 latest-backend pairs.

    uv run prek run -a
    All configured hooks passed.

    uv run tox run -e py310-bt022-numpy22
    690 passed, 46 skipped

    uv run tox run -e py310-bt022-jax05
    206 passed, 21 skipped, 18 warnings

    uv run tox run -e py310-bt022-torch26
    206 passed, 24 skipped

    uv run tox run -e py310-bt022-optree014
    202 passed, 33 skipped

PR check evidence after the matrix fix:

    GitGuardian Security Checks: passed
    Spell Check with Typos: passed
    ruff: passed
    typecheck: passed
    typecheck-compat: passed
    test: passed
    py310-bt022-numpy22: passed
    py310-bt022-jax05: passed
    py310-bt022-torch26: passed
    py310-bt022-optree014: passed
    py313-bt022-numpy24: passed
    py313-bt022-jax09: passed
    py313-bt022-torch210: passed
    py313-bt022-optree019: passed
    py313-bt022-type-pyright1408: passed
    py313-bt022-type-mypy119: passed
    py313-bt022-type-ty: passed
    push-only matrix jobs: skipped on pull_request, as expected

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
- 2026-05-28: Updated the plan after reproducing local hook failures, applying
  narrow hook configuration fixes, and validating local hooks, type-check
  integration, and docs build. The plan still needs final PR check evidence
  after the cleanup commit is pushed.
- 2026-05-28: Updated the plan after diagnosing PR compatibility-matrix
  failures and replacing unsatisfiable product matrices with explicit
  floor-on-Python-3.10 and ceiling-on-newer-Python environments.
- 2026-05-28: Updated the plan with final PR check evidence after the matrix
  fix turned PR #5 green.
