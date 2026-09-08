# Verify useful public typing with four checker engines


Maintain this ExecPlan according to `PLANS.md`. This independent PR establishes the checker harness and tested tool baseline for audit A06. Tree and broader Like models remain separate implementation PRs.

## Purpose / Big Picture


A checker must accept valid consumer calls, reject deliberately wrong calls, and retain useful inferred types. Existing fixtures mostly accept declarations; locked ty 0.0.40 reduces tested aliases to Unknown. Add meaningful consumer proof and integrate pyrefly without masking errors.

## Progress


- [x] (2026-09-08) Inspected current checker harness, configuration and audited tool results.
- [ ] Open draft PR and reproduce information loss with consumer fixtures.
- [ ] Update the tested tool baseline and correct check's configuration overload.
- [ ] Implement positive, negative, and inferred-type checks with verified diagnostics.
- [ ] Validate every advertised Python target, tox checker selection and hooks.
- [ ] Record results and remaining annotation-model work.

## Surprises & Discoveries


Current tests start each checker per fixture and then again on the whole source tree. They can pass while aliases lose useful types. `_tool_path` resolves the Python symlink before locating tools, which can select the wrong interpreter installation. Pyrefly 1.2.0 reports a mismatch between check's omitted overload configuration and the implementation's None default.

## Decision Log


Decision: Group fixtures and require valid, invalid and inferred-type evidence. Rationale: fewer redundant checker invocations with stronger user-visible proof. Expected invalid input must fail at the intended location/category, not merely cause a nonzero process exit. Date: 2026-09-08.

Decision: Start with audited pyright 1.1.411, mypy 2.3.1, ty 0.0.79 and pyrefly 1.2.0; preserve proven pyright/mypy floor lanes. Rationale: ty's old locked version loses the tested alias information, and pyrefly is the planned fourth engine. Supported tools do not imply untested Tree/Like contracts are solved.

## Outcomes & Retrospective


Implementation pending. This PR will establish tool integration and core array/decorator conformance. Static Tree acceptance, broader Like inputs and CuPy native typing remain explicitly open under the production roadmap.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/checker-conformance`, branch `codex/checker-conformance`, base `f43e00d`. `tests/test_typecheck.py` runs checkers from the current interpreter with the matching Python target. Valid fixtures live in `tests/typing/`; create `tests/typing_negative/` for deliberate errors. `pyproject.toml` and `uv.lock` own tools; `tox.toml`, `tools/validate_tox_env.py` and CI route compatibility jobs. `src/bearshape/_decorator.py` owns check's ParamSpec-preserving overloads.

## Plan of Work


Add a valid consumer fixture proving strict NumPy dtype/backend information and preserved decorated function/async signatures with assert_type. Add deliberate wrong dtype, wrong scalar type and wrong call shape cases under tests/typing_negative. Run the valid fixture with old ty and save the failure showing information loss before changing tools.

Update the static group and lock to the audited starting versions. Type check's optional keyword conf as BeartypeConf or None with the actual default, preserving existing memo-only and combined modes. Add pyrefly to tox/CI and marker documentation. The harness must locate executables beside sys.executable before searching PATH, target the current interpreter, log versions when needed, and fail if an expected selected checker is missing.

Batch source and positive/inference fixtures per checker. Run negative fixtures separately, parse supported diagnostics into source file/line/category, and compare with explicit expected-error markers. Reject crashes, unexpected diagnostics, missing imports, or success on deliberate errors. Restrict a single-checker tox environment to its selected checker; regular development and Python compatibility jobs run all four. Keep negative files outside normal src/tests/typing targets.

## Concrete Steps


Run from this worktree:

    uv sync --locked
    uv run --locked ty check tests/typing/check_conformance.py
    uv lock
    uv sync --locked
    uv run --locked pytest -n 0 tests/test_typecheck.py
    uv run --locked tox run -e py313-bt022-type-pyright1408,py313-bt022-type-mypy119,py313-bt022-type-ty,py313-bt022-type-pyrefly
    uv run --locked prek run -a

This branch starts independently from the pre-rc0 main revision, so its tox names initially use bt022; reconcile them with the separate rc0 PR in integration. Run the checker suite using interpreter-matched environments for Python 3.10–3.14. Record actual command output and selected checker versions.

## Validation and Acceptance


All four engines accept valid strict-array/decorator consumer calls and preserve their asserted types. Wrong dtype, wrong scalar type and invalid call signatures produce the intended diagnostics in every selected engine. Invalid fixture crashes or missing tools fail the harness. Existing source/fixtures pass, Python targets use matching backends/stubs, and current floor checker environments retain their proved behavior. No Any/Unknown workaround, broad new ignore or removed annotation counts as conformance.

## Idempotence and Recovery


Preserve the original checkout and lock resolutions unrelated to the deliberate tool updates. Use per-invocation mypy caches where concurrent tests would race. Do not execute negative consumer fixtures as Python programs. No merge without user validation.

## Artifacts and Notes


Save initial and final checker logs in `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/`; record tool versions and the expected-diagnostic contract here. Subsequent Tree/Like PRs extend the same harness instead of creating independent test frameworks.

## Interfaces and Dependencies


Keep ParamSpec-based decorator signature preservation and the existing public annotation syntax. Runtime dependencies remain unchanged. Checker tools are development dependencies. Use typing_extensions.assert_type for the Python 3.10-compatible inference fixtures.

Revision note — 2026-09-08: Added focused checker-conformance plan before implementation.
