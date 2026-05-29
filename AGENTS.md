# bearshape agents

bearshape is a runtime shape and dtype checking library moving toward a
production-ready release under the beartype organization. The package, docs,
examples, and site use the lowercase public identity `bearshape` everywhere.

This file is for Codex and Claude agents. Keep it short, directive, and free of
AI slop. Humans should learn the project from `README.md` and `docs/`; agents
should use this file to avoid damaging the codebase.

## Operating Rules

Think before coding.

- State assumptions before changing behavior.
- If intent is ambiguous, ask instead of guessing.
- If several interpretations are plausible, name them and explain the tradeoff.
- Push back on overcomplicated requests when a smaller design is enough.
- Do not hide uncertainty behind confident prose.

Write production code.

- No speculative features.
- No generic abstractions without repeated, real use.
- No duplicate logic when one clear helper is better.
- No unused modules, methods, parameters, tests, docs, or compatibility shims.
- No broad error handling for impossible states.
- No comments that merely restate the code.
- Every changed line must serve the plan or the user's request.

Prefer clarity over cleverness.

- Use explicit names and simple control flow.
- Keep error messages specific and useful.
- Keep public syntax stable unless an approved plan says otherwise.
- Preserve optional dependency boundaries.
- Do not make root import depend on NumPy, JAX, Torch, CuPy, or optree.

## Current Mission

The repo is in cleanup and rename mode. Broad refactors are allowed at the
beginning because the goal is to remove accumulated slop and regain control of
the whole project. Once the architecture, tests, CI, packaging, docs, and release
path are stable, switch back to surgical changes by default.

The target state is lean production quality:

- package and public identity renamed to `bearshape`
- runtime behavior correct for NumPy, JAX, PyTorch, CuPy, and tree containers
- static typing behavior coherent across pyright, mypy, ty, and planned pyrefly
- zuban considered only through an explicit plan
- tests organized by feature and edge case, including expected failures
- hooks, CI, tox, docs, packaging, and uv-based PyPI publishing rebuilt for release
- `CHANGELOG.md` updated for every feature or major user-visible action

Do not advertise support that tests, typing fixtures, and docs do not prove.

## Workflow For Major Work

Major work means any feature, public API change, rename step, packaging change,
CI change, docs contract change, large refactor, or release task.

For major work:

1. Create a feature branch.
2. Create a matching worktree so parallel work stays isolated.
3. Open a PR early.
4. Write an ExecPlan following `PLANS.md` before implementation.
5. Ask clarifying questions while writing the plan if the goal or acceptance is
   unclear.
6. Start a /goal for the plan and execute it milestone by milestone.
7. Keep the ExecPlan updated as a living document.
8. Validate thoroughly.
9. Ask the user for validation before merge.
10. After explicit approval, merge, delete the branch, and delete the worktree.

Small local fixes may skip the branch/worktree/PR/ExecPlan workflow only when the
user clearly asks for a narrow edit and the risk is low.

## Product Contract

bearshape provides runtime shape and dtype checking powered by beartype.
Annotations such as named dimensions, anonymous dimensions, fixed integer
dimensions, arithmetic dimensions, broadcastable dimensions, `Scalar`,
`Value(...)`, backend array aliases, `Like[...]`, scalar-like aliases, and
`Tree[...]` are product surface.

The two maintained surfaces are equal:

- Runtime behavior: validators, decorators, import boundaries, conversion rules,
  tree handling, and error messages.
- Static behavior: annotation syntax accepted by supported type checkers.

If code, tests, docs, examples, and typing fixtures disagree, resolve the
contract explicitly. Do not leave drift in place.

## Boundaries To Preserve

Root module:

- Keep root import lightweight.
- Keep backend-specific behavior out of the root unless an approved plan changes
  the public API.
- Do not widen the root API just to make examples shorter.

Backend modules:

- NumPy owns the broadest surface: strict arrays, Like types, scalar-like types,
  structured dtypes, and related factories.
- JAX, Torch, and CuPy keep backend-specific arrays and conversion behavior.
- Tree support remains explicit and tested; do not blur runtime-only structure
  syntax with checker-supported syntax.

High-risk areas:

- memo discovery and lifetime
- decorator behavior, including async paths and metadata preservation
- shape token parsing and `Value(...)` expression evaluation
- dtype normalization, byte order, structured dtype, datetime, and timedelta
- tree validation and structure binding
- `TYPE_CHECKING` scaffolding and typing fixtures

Touch these areas only with focused tests and clear validation.

## Testing And Validation

Use `uv`. Run targeted checks while developing; use broader checks before asking
for review.

Common commands:

- `uv sync`
- `uv run pytest -n auto tests/...`
- `uv run pytest -n auto tests/test_typecheck.py`
- `uv run pyright src tests/typing`
- `uv run mypy src tests/typing`
- `uv run ty check src tests/typing`
- `uv run prek run -a`

`tox` is primarily for CI and release confidence. Run relevant tox environments
when changing the matrix, dependencies, packaging, or release workflow.

NumPy, JAX, Torch, and optree tests should run locally on CPU. CuPy needs a
CUDA-capable GPU and is deferred until an appropriate environment exists. Do not
treat CuPy coverage as proven by local CPU runs; mark it explicitly in plans,
tests, and CI work.

Validation must prove behavior, not just absence of syntax errors. For bugs,
write the failing regression first when practical. For features, cover normal
use, edge cases, and expected failures. For typing changes, update fixtures and
run every supported checker.

## Docs And Examples

Docs are contract artifacts, but they should be concise.

- Build docs from actual code behavior.
- Keep `README.md` short: identity, purpose, install, minimal examples, links.
- Keep examples accurate and test-backed when practical.
- Document runtime-only syntax explicitly.
- Update `CHANGELOG.md` for every feature and major user-visible change.
- Do not use docs to promise future behavior.

## Style

Use the existing style unless a cleanup plan changes it. This repository uses
2-space indentation in Python. Keep edits small inside a milestone even when the
overall refactor is large. Remove slop when it is in scope: dead code, duplicate
paths, pointless wrappers, stale tests, stale docs, and fake generality.

Before finishing, ask: would this diff make the library easier to trust? If not,
simplify or explain why the complexity is necessary.
