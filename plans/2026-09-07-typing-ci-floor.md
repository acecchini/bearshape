# Keep typing checks aligned with supported Python versions

This ExecPlan is a living document maintained according to `PLANS.md`. Update Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective as work proceeds.

## Purpose / Big Picture


Bearshape promises Python 3.10 and newer, but its default type checkers currently target Python 3.12. A target is the Python version whose annotation rules a checker evaluates; it is distinct from the interpreter running that checker. This gap allowed unsupported standard-library typing imports to pass CI. PR #10 replaces those imports with typing_extensions backports. This companion change makes ordinary checker commands enforce Python 3.10 and makes the existing automated compatibility tests evaluate every supported target, 3.10 through 3.14.

## Progress


- [x] (2026-09-07) Review PR #10 at 63bb0fa98aea5bd4060bc240227f711928f73939; reproduce 480 Python 3.10 errors on main and zero with the fix.
- [x] (2026-09-07) Audit checker configuration, CI, nightly, publishing, tox, test selection, and fixture coverage; authorize the reviewed external CI run under the user's instruction.
- [x] (2026-09-07) Create codex/typing-ci-floor and its isolated worktree based on PR #10.
- [ ] Open the companion draft PR with this plan before implementation.
- [ ] Set checker defaults to 3.10 and parameterize whole-tree typing tests across 3.10 through 3.14.
- [ ] Validate every checker, representative tox environments, repository hooks, and GitHub CI; address concrete failures within scope.
- [ ] Merge PR #10 and the CI companion only after applicable checks pass, refresh local main, and remove owned worktrees and branches.

## Surprises & Discoveries


The existing tox environments run checker tooling on Python 3.13 but inherit a Python 3.12 target. Their comment incorrectly treats type stubs as version-independent. The existing tests already exercise all backend aliases, including CuPy's static protocol, so new duplicate annotation fixtures are unnecessary. The typecheck-compat job already runs tests/test_typecheck.py, and tox's type environments collect that same file. Extending these tests therefore covers PR, push, and nightly pipelines without adding another workflow matrix.

PR #10's GitHub CI was awaiting approval for an external contribution. The user explicitly authorized auditing and changing CI and merging when green; the reviewed workflow has now been approved. CuPy runtime coverage remains unavailable on this CPU-only Mac and the existing CPU GitHub runners.

## Decision Log


Decision: Adopt Python 3.10 as the pyright, mypy, and ty default target, and explicitly exercise targets 3.10, 3.11, 3.12, 3.13, and 3.14 in each checker's whole-tree pytest test. Rationale: floor checking prevents the reported bug, while the small existing test extension preserves confidence at newer targets without multiplying workflow jobs. Date/author: 2026-09-07, Codex.

Decision: Preserve PR #10 and open a companion branch based on its reviewed commit. Rationale: the CI change depends on the backports, and separate merges preserve contributor credit and a focused final CI diff. Merge PR #10 with its commits preserved, then merge the companion after its final base and checks are verified. Date/author: 2026-09-07, Codex.

Decision: Treat the user's latest instruction as authorization to enable CI and merge once review and checks pass; no additional merge confirmation is required. Rationale: the user expressly delegated these decisions after the initial review. Date/author: 2026-09-07, Codex.

## Outcomes & Retrospective


Audit and plan complete. Implementation and final validation are pending. The original backport review passed all three checkers across five targets, the CPU runtime suite, hooks, lock validation, package build, and isolated minimum-dependency imports on Python 3.10 and 3.14.

## Context and Orientation


The main checkout is /Users/ale/Code/bearshape. Work for this plan takes place in /Users/ale/Code/bearshape-typing-ci-floor on codex/typing-ci-floor. The reviewed contribution is https://github.com/acecchini/bearshape/pull/10. The companion branch initially includes that contribution until PR #10 lands.

pyproject.toml contains [tool.pyright] and [tool.mypy]; ty.toml contains ty's [environment]. tests/test_typecheck.py runs each supported checker against individual fixtures and against src plus tests/typing. tests/conftest.py restricts tox type environments to these tests. tox.toml names three checker environments on Python 3.13. .github/workflows/ci.yml and .github/workflows/nightly.yml already invoke these tests or environments. Existing tests/typing/check_annotations*.py and check_like_types.py exercise the public backend aliases involved in PR #10.

## Plan of Work


Milestone 1 is the audit and a reviewable draft PR containing this plan. Check that the branch starts at the reviewed PR commit and that source behavior is untouched.

Milestone 2 changes pythonVersion and python_version in pyproject.toml and python-version in ty.toml to 3.10. Add a short comment explaining that this is the supported floor. In tests/test_typecheck.py, define the five supported targets and parameterize each existing test_*_source_tree method. Pass pyright --pythonversion, mypy --python-version, and ty check --python-version explicitly. Individual fixture tests retain ordinary default commands. Update the test module's description and tox.toml's misleading comment. Add a concise CHANGELOG.md entry describing persistent floor and target coverage. No new runtime or annotation API is needed.

Milestone 3 validates the complete typing tests, relevant tox checker environments, hooks, and hosted CI. Failures must be understood rather than suppressed. If the audit reveals another concrete CI blocker, record its cause and the smallest repair before changing the plan's scope. Confirm the GitHub head commit before merge. Once all applicable checks pass, merge PR #10, verify the companion against the updated base, and merge it. Finish with a clean, current local main.

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

Use gh pr checks and gh run view with the exact PR or run identifiers returned by GitHub. Do not merge a changed head without reviewing and validating it. Use merge commits to preserve the shared contribution in the companion's ancestry. After both PRs land, run git pull --ff-only from /Users/ale/Code/bearshape and verify git status --short --branch.

## Validation and Acceptance


The five whole-tree targets must pass for each of the three checkers, and the 27 individual fixture checks must pass using the new 3.10 defaults: 42 typing tests in total. Ordinary pyright, mypy, and ty commands must pass without a version override. The regression evidence is the original source producing 480 errors under Python 3.10 while the backport source passes; the permanent test now always exercises that target regardless of future default configuration drift.

Run all three declared tox checker environments to verify the distinction between checker interpreter and target works with the actual configured dependency versions. Repository hooks and the dependency lock must pass without unexpected edits. Require the complete applicable PR CI to succeed. Skipped event-specific jobs are expected; failed, cancelled, or awaiting-approval applicable jobs are not green. CPU backends remain tested; CuPy runtime remains explicitly unproven.

## Idempotence and Recovery


All edits remain in the isolated worktree. Retry failed checks after correcting their evidenced cause. Do not overwrite main or the contributor's branch. A failed check leaves both PRs open. Avoid force-pushing unless an explicitly reviewed branch update requires it. Remove only the worktrees and local/remote companion branch created for this review, after successful merges and a clean status. The preserved shapix backup is outside this task.

## Artifacts and Notes


Prior independent review evidence:

    main, pyright target 3.10: 480 errors
    PR #10, pyright/mypy/ty targets 3.10 through 3.14: all pass
    typing_extensions 4.6.0 with built wheel: root imports pass on Python 3.10 and 3.14

## Interfaces and Dependencies


No public interface or additional dependency is introduced by the companion change. It uses pytest parameterization and the existing supported CLI flags of pyright, mypy, and ty. PR #10 remains responsible for the typing_extensions runtime dependency and source imports. Neither change makes root import load a numerical backend.

Revision note (2026-09-07): Initial plan records the audited coverage gap, focused implementation, validation criteria, and user-authorized merge conditions before implementation.
