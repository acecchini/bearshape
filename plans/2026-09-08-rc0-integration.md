# Validate the combined release candidate


Maintain this ExecPlan according to `PLANS.md`. This branch combines the focused production-readiness PRs for integration evidence. Their individual PRs remain the review units; this draft is not authorization to merge them into main.

## Purpose / Big Picture


Prove that the runtime fixes, static aliases, packaging and framework checks work together under bearshape 0.1.0rc0 and exact beartype 0.23.0rc0. Enable focused CI, docs and release follow-up PRs against a common candidate tree while main stays unchanged.

## Progress


- [x] (2026-09-08) Created isolated integration branch/worktree from main.
- [ ] Open draft integration PR.
- [ ] Combine PRs #13–#21 and resolve overlapping configuration/docs changes explicitly.
- [ ] Run all four checkers, runtime tests, hooks and candidate Python endpoints together.
- [ ] Build and normally install the combined sdist-derived wheel outside the checkout.
- [ ] Validate corrected GPU behavior using a verified public candidate artifact.
- [ ] Record evidence and remaining release blockers without implying merge approval.

## Surprises & Discoveries


Independent PRs touch shared changelog, CI and typing sections. Backend conversion removes runtime NumPy imports, while static Like aliases still require NumPy inside TYPE_CHECKING. Integration must preserve both optional dependency boundaries and checker names. Whole-native-union rollback and the scope of CuPy static support remain unresolved decisions documented in the feature plans.

## Decision Log


Decision: Use a temporary integration branch, preserving original feature commits and individual PRs. Rationale: source-level passes from isolated branches cannot establish combined behavior. Main merges still require the user's validation. Date: 2026-09-08.

Decision: Resolve overlap by reading each side's intended behavior and keeping focused changes together. Rationale: blanket ours/theirs resolution could discard fixes or reintroduce obsolete dependency factors.

## Outcomes & Retrospective


Integration pending. A green aggregate does not establish production readiness while an explicit release blocker remains unresolved.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/rc0-integration`, branch `codex/rc0-integration`, base main `f43e00d`. PRs #13–#21 cover candidate compatibility, caller-sensitive claw integration, memo lifetime, backend conversion, checker conformance, distribution integrity, Like/Shaped static inputs, recursive Tree inputs and framework/minimal validation. The roadmap is PR #12.

## Plan of Work


Merge the feature branches into this isolated branch in dependency order, keeping their identities. Resolve changelog entries additively, retain rc0 factors alongside the four-checker updates, and retain corrected Like/Tree documentation. Put static-only NumPy imports inside TYPE_CHECKING after backend conversion import cleanup.

Run the combined runtime and checker suites, exact-candidate Python endpoints, and all hooks. Build sdist then wheel; inspect metadata, package bytes and license using the maintained distribution checker. Normally install that wheel outside all source checkouts and execute representative consumers and the minimal smoke command. Publish the integration branch only as a reviewable draft. Any remote artifact validation must have verified source/public provenance and stay inside an isolated environment.

Separate subsequent CI, documentation and publication changes into their own worktrees and PRs stacked on this integration tree. Keep the final handoff record tied to exact commits, versions, artifact hashes and actual support limits.

## Concrete Steps


Use git merge --no-ff for each feature branch here, inspect conflicts and commit the resolution. Then run:

    uv sync --locked
    uv run --locked pytest tests/ -n 4
    uv run --locked tox run -e py310-bt023rc0-cpu,py314-bt023rc0-cpu
    uv run --locked prek run -a
    uv build --sdist
    uv build dist/*.tar.gz --wheel
    uv run --locked python tools/check_distribution.py dist/*.whl dist/*.tar.gz

Record external installed-consumer commands and package origins separately from source validation.

## Validation and Acceptance


Every combined change remains traceable to a focused PR. All supported checker cases execute, negative diagnostics remain effective, runtime regressions pass, and packaging/minimal checks use normal installation of the validated wheel. The exact beartype candidate is asserted. Main, release tags, package publication and ownership settings remain subject to their separate approval requirements.

## Idempotence and Recovery


This worktree isolates conflicts and generated artifacts from main and the feature branches. Abort an unresolved merge rather than discarding unrelated edits. Do not force-update another contributor's branch or remove worktrees until approved merges are complete.

## Artifacts and Notes


Evidence goes under `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/integration-*`. GPU baseline logs cover the earlier compatibility wheel only; they must not be presented as evidence for combined conversion/lifetime fixes.

## Interfaces and Dependencies


No new public API is introduced by integration. Preserve all optional imports, Python 3.10 syntax and the existing four-checker test harness. Changes needed to resolve integration must be documented here and, when substantive, returned to the owning feature PR.
