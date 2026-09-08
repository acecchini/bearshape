# Instrument the actual caller package through bearshape.claw


Maintain this ExecPlan according to `PLANS.md`. This independent PR closes audit finding A02 under the accepted `0.1.0rc0` production goal.

## Purpose / Big Picture


Calling `bearshape_this_package()` in a user's package initializer must instrument that package's subsequently imported modules. Currently the forwarding wrapper makes upstream discover `bearshape.claw` as the caller instead, so invalid inputs return normally. Preserve the public import name while allowing beartype to inspect the real calling package.

## Progress


- [x] (2026-09-08) Read the wrapper and its mocked forwarding test.
- [ ] Open the draft PR and reproduce unchecked real-package calls.
- [ ] Replace forwarding with a direct upstream alias and update docs/changelog.
- [ ] Validate parameter, return, configuration, nested-module and sibling-package behavior on baseline and exact rc0.
- [ ] Record evidence and request user validation before merge.

## Surprises & Discoveries


The current forwarding mock verifies only that conf reaches a function. It cannot detect the wrong caller-package discovery. Real isolated package imports are required. Import-hook registration is process-global, so use subprocesses to prevent test contamination.

## Decision Log


Decision: Directly re-export `beartype.claw.beartype_this_package` as `bearshape_this_package`. Rationale: preserve upstream signature and caller discovery with no additional stack-search logic. Date: 2026-09-08.

## Outcomes & Retrospective


Implementation pending. Success means bad input and return shapes raise real beartype violations after package instrumentation, with the documented valid calls still succeeding.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/claw-caller`, branch `codex/claw-caller`, base `f43e00d`. `src/bearshape/claw.py` contains the forwarding function; `tests/test_coverage_edges.py::TestClawWrapper` mocks its callee. `tests/conftest.py` restricts backend-specific tox collection by filename, so include the new `tests/test_claw.py` in the NumPy suite. Runtime arrays and dimensions come from `bearshape.numpy` and package root.

## Plan of Work


First write `tests/test_claw.py` to create a temporary package whose initializer calls the public hook, then imports a nested module containing functions annotated with F32[N]. A subprocess imports that package and exercises valid equal shapes, invalid second parameters, invalid returns, configuration that changes violation types, and an unrelated sibling package which must remain unchecked. Run the new tests before changing source and save the failing results.

Then replace the forwarding function with the direct alias. Remove the obsolete forwarding mock and its unused imports, revise wrapper terminology in relevant claw documentation, and add the behavioral fix to CHANGELOG. Keep this PR independent from the metadata floor PR; run the normal baseline suite plus isolated exact-rc0 source tests, and revalidate their combined installed artifact in the program's integration stage.

## Concrete Steps


Run from this worktree:

    uv sync --locked
    uv run --locked pytest -n 0 tests/test_claw.py
    uv run --locked pytest -n auto tests/test_claw.py tests/test_coverage_edges.py
    uv run --locked pyright src tests/typing
    uv run --locked mypy src tests/typing
    uv run --locked ty check src tests/typing
    uv run --locked prek run -a

Use the goal's isolated exact-rc0 interpreter with this worktree's source path to run `tests/test_claw.py` on Python 3.10 and 3.14. Record actual paths/results; this source test proves the fix on rc0, while normal artifact installation belongs to the compatibility/integration PRs.

## Validation and Acceptance


The unmodified wrapper fails the real-package regression. The alias makes parameter and return mismatches raise the intended configured violation classes in subsequently imported nested modules, valid calls pass, and unrelated packages stay unaffected. All supported checker and formatting checks remain green. No backend is newly required for root import.

## Idempotence and Recovery


Each test uses pytest temporary paths and a subprocess, without globally registering hooks in the parent test runner. Preserve the main checkout and use only this feature worktree. No merge occurs before user validation.

## Artifacts and Notes


Save failing and passing logs under `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/`. This finding is independently reproducible on beartype 0.22.9 and 0.23.0rc0.

## Interfaces and Dependencies


The public name stays `bearshape.claw.bearshape_this_package`, including upstream's keyword-only conf argument. There is no additional runtime dependency and no new root export. Tests use NumPy and pytest already included in development dependencies.

Revision note — 2026-09-08: Added focused plan before implementing the caller-package fix.
