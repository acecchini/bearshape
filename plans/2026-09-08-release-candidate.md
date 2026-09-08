# Validate the full independent PR set together


Maintain this ExecPlan according to PLANS.md. This branch is a review and validation aggregate; it is not approval to merge any focused PR.

## Purpose / Big Picture


The focused CI, documentation, installation and GPU changes must work together on top of the runtime/typing corrections. A fresh branch preserves all original review branches while providing one candidate for complete validation and the publication-gate work.

## Progress


- [x] (2026-09-08) Created codex/release-candidate from documentation PR #24.
- [ ] Open the aggregate draft PR against #22.
- [ ] Combine installed-consumer PR #25 and CuPy PR #26, preserving every contract and test.
- [ ] Run hooks and observe the complete hosted candidate matrix.
- [ ] Record results and keep user merge approval pending.

## Surprises & Discoveries


Focused PRs have explicit dependent bases. Pushing a merge into a PR's own base can close it automatically; this separate aggregate prevents that while preserving the original commits. CI #23 and docs #24 are already green independently. Installed checks pass 1,074 tests at both endpoints. GPU candidate validation is in progress.

## Decision Log


Decision: Create a new aggregate instead of merging into #22 or #23. Rationale: preserve independent review and the user's required merge validation. Date: 2026-09-08.

Decision: Resolve additive workflow/changelog overlaps without changing runtime behavior. Rationale: both notebook and installed-consumer jobs must remain required, and every focused change must retain its release note.

## Outcomes & Retrospective


Integration pending. A04 whole native-union rollback and CuPy static release policy remain open. Green integration checks cannot establish production readiness while those decisions remain unresolved.

## Context and Orientation


Worktree /Users/ale/Code/bearshape-worktrees/release-candidate, branch codex/release-candidate. Base #22 includes PRs #13–21. This branch begins at docs #24, which already contains CI #23. The shared .github/workflows/validate.yml runs platform runtime, four checkers, dependency floors, quality, docs, notebooks, archive integrity and minimal installs. #25 adds full installed consumers; #26 adds CUDA cases skipped explicitly in CPU lanes.

## Plan of Work


Merge the committed heads of codex/installed-consumers and codex/cupy-runtime into this new branch with merge commits. Keep all changelog entries. Resolve the shared workflow by retaining both notebook and installed jobs and including both in the final required gate. No parent feature branch is modified.

Run the full hooks, workflow lint and hosted matrix. Review any failures against the actual merged source. Record the final commit, job results and artifact hashes. Publication workflow changes remain in a separate dependent PR.

## Concrete Steps


From this worktree use git merge --no-ff with each verified local feature branch. Review git diff and run uv run --locked prek run -a plus the manual actionlint hook. Push this branch only, then inspect its CI job results.

## Validation and Acceptance


All required runtime, checker, compatibility, quality, docs, notebook, distribution, minimal and installed jobs must succeed. The package remains version 0.1.0rc0 with exact beartype rc0 validation. Preserve the source commit history and original PR bases. No merge into main or release publication occurs.

## Idempotence and Recovery


Only this isolated aggregate is mutated. Conflict resolutions are reviewable; abort a merge if its intended behavior is unclear. Do not reset another worktree or delete evidence. User validation remains required for merge.

## Artifacts and Notes


Use /Users/ale/Code/bearshape-implementation-2026-09-08/evidence/release-candidate-* for validation evidence. The focused PRs retain their own detailed ExecPlans and logs.

## Interfaces and Dependencies


No additional public API or dependency changes beyond the focused PRs. Keep the locked uv workflow and optional backend boundaries intact.
