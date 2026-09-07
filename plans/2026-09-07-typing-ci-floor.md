# Keep typing checks aligned with supported Python versions

This ExecPlan is a living document maintained according to `PLANS.md`. Update Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective as work proceeds.

## Purpose / Big Picture


Bearshape promises Python 3.10 and newer, but its default type checkers currently target Python 3.12. A target is the Python version whose annotation rules a checker evaluates; it is distinct from the interpreter running that checker. This gap allowed unsupported standard-library typing imports to pass CI. PR #10 replaces those imports with typing_extensions backports. This companion change makes ordinary checker commands enforce Python 3.10 and runs the existing automated compatibility tests in each supported Python environment, 3.10 through 3.14, targeting the interpreter whose dependencies are installed.

## Progress


- [x] (2026-09-07) Review PR #10 at 63bb0fa98aea5bd4060bc240227f711928f73939; reproduce 480 Python 3.10 errors on main and zero with the fix.
- [x] (2026-09-07) Audit checker configuration, CI, nightly, publishing, tox, test selection, and fixture coverage; authorize the reviewed external CI run under the user's instruction.
- [x] (2026-09-07) Create codex/typing-ci-floor and its isolated worktree based on PR #10.
- [x] (2026-09-07) Open companion draft PR #11 with this plan before implementation.
- [x] (2026-09-07) Set checker defaults to 3.10; prototype cross-target tests and discover NumPy stub incompatibility in Python 3.13 tox.
- [x] (2026-09-07) Match each suite target to its interpreter and add a Python 3.10-3.14 typecheck-compat environment matrix.
- [x] (2026-09-07) Validate all three default checkers, 30 local typing tests, six structured dtype tests, all three declared tox checker environments, hooks, lock consistency, and actionlint.
- [ ] Complete the final hosted CI run for the dtype annotation repair; the preceding revision already passed all five Python typing jobs and the coverage-enabled test job.
- [ ] Merge PR #10 and the CI companion only after applicable checks pass, refresh local main, and remove owned worktrees and branches.

## Surprises & Discoveries


The existing tox environments run checker tooling on Python 3.13 but inherit a Python 3.12 target. Their comment incorrectly treats type stubs as version-independent. The existing tests already exercise all backend aliases, including CuPy's static protocol, so new duplicate annotation fixtures are unnecessary. The typecheck-compat job already runs tests/test_typecheck.py, and tox's type environments collect that same file. The compatibility job will use five Python environments; tox retains its current runtime and checker-version matrices. Each test invocation targets its active interpreter to match its dependency stubs.

PR #10's GitHub CI was awaiting approval for an external contribution. The user explicitly authorized auditing and changing CI and merging when green; the reviewed workflow has now been approved. CuPy runtime coverage remains unavailable on this CPU-only Mac and the existing CPU GitHub runners.

## Decision Log


Decision: Keep Python 3.10 defaults for ordinary commands, and run the compatibility suite on each supported interpreter with an explicit matching checker target. Rationale: on Python 3.13 tox, NumPy 2.4 stubs contain Python 3.12 type statements; mypy correctly rejects them when forcibly targeting 3.10. Separate compatible environments test the actual supported combinations without suppressing dependency errors. The initial five-targets-in-one-environment prototype passed with the Python 3.10 locked dependencies but failed in the newer tox environment, so replace it with five workflow environments. Date/author: 2026-09-07, Codex.

Decision: Preserve PR #10 and open a companion branch based on its reviewed commit. Rationale: the CI change depends on the backports, and a companion change preserves contributor credit while exposing the CI audit for review. The original PR cannot become green with its floating Ruff workflow. Validate the combined PR #11 and merge it with a merge commit; it contains PR #10 unchanged, preserves contributor authorship, and makes that contribution reachable from main. Verify GitHub marks PR #10 merged through the same history. Do not bypass failing checks: the complete final tree must pass the repaired workflow. Date/author: 2026-09-07, Codex.

Decision: Treat the user's latest instruction as authorization to enable CI and merge once review and checks pass; no additional merge confirmation is required. Rationale: the user expressly delegated these decisions after the initial review. Date/author: 2026-09-07, Codex.

## Outcomes & Retrospective


Implementation and local validation are complete. The final hosted run is the remaining merge gate. Hosted CI identified a pre-existing lint blocker: ruff-action resolved Ruff 0.16.6 from >=0.15.9, while uv.lock contains 0.15.15. New suppression-comment rules fail unchanged source, preventing all downstream tests. Fix the version drift through the lock, not by weakening lint or editing unrelated source.

The original backport review passed all three checkers across five targets, the CPU runtime suite, hooks, lock validation, package build, and isolated minimum-dependency imports on Python 3.10 and 3.14.

## Context and Orientation


The main checkout is /Users/ale/Code/bearshape. Work for this plan takes place in /Users/ale/Code/bearshape-typing-ci-floor on codex/typing-ci-floor. The reviewed contribution is https://github.com/acecchini/bearshape/pull/10. The companion branch includes that unchanged contribution and will merge it through preserved commit history.

pyproject.toml contains [tool.pyright] and [tool.mypy]; ty.toml contains ty's [environment]. tests/test_typecheck.py runs each supported checker against individual fixtures and against src plus tests/typing. tests/conftest.py restricts tox type environments to these tests. tox.toml names three checker environments on Python 3.13. .github/workflows/ci.yml and .github/workflows/nightly.yml already invoke these tests or environments. Existing tests/typing/check_annotations*.py and check_like_types.py exercise the public backend aliases involved in PR #10.

## Plan of Work


Milestone 1 is the audit and a reviewable draft PR containing this plan. Check that the branch starts at the reviewed PR commit and that source behavior is untouched.

Milestone 2 also replaces the floating astral-sh/ruff-action steps in .github/workflows/ci.yml with setup-uv and uv run --locked --only-group dev ruff check/format commands. This reads the existing uv.lock instead of independently resolving the broad Ruff lower bound. The same setup-uv revision already used by the workflow is retained.

Milestone 2 changes pythonVersion and python_version in pyproject.toml and python-version in ty.toml to 3.10. Add a short comment explaining that this is the supported floor. In tests/test_typecheck.py, derive PYTHON_TARGET from sys.version_info and pass pyright --pythonversion, mypy --python-version, and ty check --python-version to both individual fixtures and whole-tree checks. In .github/workflows/ci.yml, give typecheck-compat a Python 3.10 through 3.14 matrix and pass each version to uv run --python. Ordinary default checker commands still run at 3.10 in the separate typecheck job. Update the test module's description and tox.toml's misleading comment. Add a concise CHANGELOG.md entry describing persistent floor and target coverage. No new public runtime or annotation API is needed. The existing DtypeSpec.structured factory also replaces its mypy-only suppression with a DTypeLike cast, as established by the latest ty diagnostic.

Milestone 3 validates the complete typing tests, relevant tox checker environments, hooks, and hosted CI. Failures must be understood rather than suppressed. If the audit reveals another concrete CI blocker, record its cause and the smallest repair before changing the plan's scope. Confirm the GitHub head commit before merge. Once all applicable checks pass for the combined tree, merge PR #11 with a merge commit and verify both the original contribution and the CI improvements are present on main, including PR #10 status. Finish with a clean, current local main.

## Concrete Steps


All development commands below run in /Users/ale/Code/bearshape-typing-ci-floor:

    uv sync --locked --no-group docs --no-group notebook
    uv run --no-sync pytest -n auto tests/test_typecheck.py
    uv run --no-sync pyright src tests/typing
    uv run --no-sync mypy src tests/typing
    uv run --no-sync ty check src tests/typing
    uv run --no-sync tox run -e py313-bt022-type-pyright1408,py313-bt022-type-mypy119,py313-bt022-type-ty
    uv run --no-sync prek run -a
    uv lock --check

Use gh pr checks and gh run view with the exact PR or run identifiers returned by GitHub. Do not merge a changed head without reviewing and validating it. Use a merge commit for PR #11 to preserve the contributor commit in main history and verify PR #10 is consequently marked merged. After both changes land, run git pull --ff-only from /Users/ale/Code/bearshape and verify git status --short --branch.

## Validation and Acceptance


Each Python matrix environment must pass 30 typing tests: nine individual fixtures and one whole-tree check for each of three checkers. Across Python 3.10 through 3.14 this is 150 checks, each using dependencies compatible with its interpreter. Ordinary pyright, mypy, and ty commands must pass without a version override. The regression evidence is the original source producing 480 errors under Python 3.10 while the backport source passes; the permanent Python 3.10 matrix environment explicitly targets 3.10 regardless of future default configuration drift.

Run all three declared tox checker environments to verify the distinction between checker interpreter and target works with the actual configured dependency versions. Repository hooks and the dependency lock must pass without unexpected edits. Require the complete applicable PR CI to succeed. Skipped event-specific jobs are expected; failed, cancelled, or awaiting-approval applicable jobs are not green. CPU backends remain tested; CuPy runtime remains explicitly unproven.

## Idempotence and Recovery


All edits remain in the isolated worktree. Retry failed checks after correcting their evidenced cause. Do not overwrite main or the contributor's branch. A failed check leaves both PRs open. Avoid force-pushing unless an explicitly reviewed branch update requires it. Remove only the worktrees and local/remote companion branch created for this review, after successful merges and a clean status. The preserved shapix backup is outside this task.

## Artifacts and Notes


Prior independent review evidence:

    main, pyright target 3.10: 480 errors
    PR #10, pyright/mypy/ty targets 3.10 through 3.14: all pass
    typing_extensions 4.6.0 with built wheel: root imports pass on Python 3.10 and 3.14
    final local typing suite: 30 passed
    structured dtype regression subset: 6 passed
    Python 3.13 tox: pyright1408 and mypy119 pass; ty passes after DTypeLike repair
    hosted run 34162541944: all five Python typing jobs and coverage-enabled test job passed before final repair

## Interfaces and Dependencies


The latest ty 0.0.78 with NumPy 2.5.3 exposed an existing no-matching-overload diagnostic at DtypeSpec.structured: its object argument is passed to np.dtype with a mypy-only suppression. Replace that suppression with a cast to numpy.typing.DTypeLike, imported only under TYPE_CHECKING to preserve the root optional-dependency boundary. NumPy continues to validate and reject values at runtime. Run all three checkers and the existing structured dtype tests after this typing-only repair.

No public interface or additional dependency is introduced by the companion change. It uses pytest parameterization and the existing supported CLI flags of pyright, mypy, and ty. PR #10 remains responsible for the typing_extensions runtime dependency and source imports. Neither change makes root import load a numerical backend.

Revision note (2026-09-07): Initial plan records the audited coverage gap, focused implementation, validation criteria, and user-authorized merge conditions before implementation.

Revision note (2026-09-07): Hosted PR #10 run 32062266937 proved floating Ruff drift blocks downstream tests. Add lock-based lint execution and validate/merge the combined tree in PR #11, preserving the original contribution commit.

Revision note (2026-09-07): The first tox run exposed NumPy 2.4 stub syntax errors with a forced 3.10 target. Replace cross-target tests in one environment with a real Python 3.10-3.14 CI environment matrix and matching explicit checker flags for all existing fixtures.

Revision note (2026-09-07): The final Python 3.13 tox run passed pyright and mypy but latest ty identified an existing dtype constructor annotation mismatch. Add a precise DTypeLike cast at that dynamic boundary rather than suppressing the checker or pinning away the diagnostic.

Revision note (2026-09-07): Record completed local validation and the final narrow annotation repair. The final combined commit must still pass hosted CI before merge.
