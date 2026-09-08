# Prove the normally installed candidate artifact


Maintain this ExecPlan according to `PLANS.md`. This focused artifact-consumer PR is stacked on CI PR #23 and implements the remaining installation proof in M8.

## Purpose / Big Picture


The package users install must pass the same runtime and static consumer contracts as the checkout. Build the wheel from the source archive, normally install it with exact beartype 0.23.0rc0, and run copied downstream tests outside every source checkout. Keep the resulting hashes and module origins traceable to the candidate commit.

## Progress


- [x] (2026-09-08) Created isolated branch/worktree from the combined CI candidate.
- [ ] Open early draft PR and inspect archive/test configuration.
- [ ] Add explicit installed-package mode for consumer checker tests.
- [ ] Maintain isolated sdist-derived consumer validation with normal wheel installation.
- [ ] Run runtime, positive/negative/inference checks on Python 3.10 and 3.14.
- [ ] Require artifact consumer validation in shared CI and preserve the same built artifact.
- [ ] Record hashes, origins and results; obtain user validation before merge.

## Surprises & Discoveries


Source tests currently assume a src directory in the checker target list. The archive already ships tests and configuration, but copied installed-package checks must omit that source target explicitly. The CI work exposed a hard-coded pyright venv override that could conceal the actual environment; its fix is present in this base.

## Decision Log


Decision: Add an explicit pytest installed-package option rather than infer mode from a missing source directory. Rationale: an accidental missing source tree must not silently reduce normal validation. Date: 2026-09-08.

Decision: Copy only downstream tests/configuration from the source archive into a temporary consumer directory, leaving package source absent. Rationale: source imports can mask incomplete wheels and missing typing markers. Install the wheel normally, with declared dependencies and exact beartype; never bypass resolution with --no-deps.

Decision: Reuse the candidate-distributions artifact from the shared build job. Rationale: consumer validation and subsequent publication must refer to the same bytes. Keep publication changes in a separate PR.

## Outcomes & Retrospective


Implementation pending. Existing minimal-wheel and archive-content checks prove useful subsets; this milestone establishes combined runtime and checker behavior from the installed artifact.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/installed-consumers`, branch `codex/installed-consumers`, base CI `f396e72`. `tools/check_distribution.py` checks license, metadata, package bytes and source-test inclusion. `tests/test_typecheck.py` runs four positive/negative batches. `tests/conftest.py` owns pytest filtering; `pytest.toml` configures importlib mode. The shared workflow builds one sdist-derived wheel and makes it available as candidate-distributions.

## Plan of Work


Add --installed-package to pytest and make only the positive source/checker batch omit src in that explicit mode. Runtime and negative fixtures stay unchanged. Build and inspect archives, then create a fresh normal virtual environment for the selected interpreter. Export locked runtime/backend/checker/test dependencies without the editable project, install those dependencies and the actual wheel with exact beartype.

Extract downstream tests and required configuration into a temporary directory without src. Verify bearshape imports from the new environment's site-packages, no editable project is installed, and exact versions/hashes are reported. Run the full CPU runtime suite plus every checker against copied fixtures. Fail on missing tools, unexpected diagnostics or source origins. Keep optional CuPy skips explicit; separate GPU evidence remains required.

Wire endpoint consumer jobs to the existing distribution artifact and include them in the required gate. Save concise results and hashes. Run hooks and workflow lint, then inspect hosted results.

## Concrete Steps


From this worktree build sdist and then its wheel, using tools/check_distribution.py before installing. Use a separate temporary consumer root and normal uv pip installation. Run copied tests with:

    python -I -m pytest tests/ --installed-package -n 4

Record actual checker imports and ensure their interpreter paths point to the consumer environment. Use the maintained command from CI at both endpoints.

## Validation and Acceptance


The consumer directory contains no src/bearshape. Normal wheel resolution permits exact beartype rc0. Runtime tests and all four checker batches pass under Python 3.10 and 3.14, with only documented absent-CuPy/platform skips. Report artifact SHA256 and installed module paths. The final CI gate requires both endpoint results and no rebuild occurs between artifact validation stages.

## Idempotence and Recovery


Use disposable directories and local virtual environments only. Do not modify system Python, main, release tags or ownership. Keep feature PRs separate and require user validation before merge.

## Artifacts and Notes


Evidence goes under `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/installed-*`. Store the checked wheel/sdist hashes and copied-consumer logs. These results complement, but do not replace, exact GPU runtime tests or the unresolved native-union contract decision.

## Interfaces and Dependencies


No public runtime API or dependency change is planned. The pytest option is for downstream artifact validation. Use the existing locked backend/checker/test groups and standard-library archive/process tools for orchestration.
