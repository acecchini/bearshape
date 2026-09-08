# Align agent guidance and merge the approved production work


This living ExecPlan follows `PLANS.md`. Keep Progress, Surprises & Discoveries,
Decision Log, and Outcomes & Retrospective current.

## Purpose / Big Picture


A contributor or coding agent should be able to choose the correct validation
commands, preserve the package contracts, and finish approved work without
following retired rename instructions. The owner approved merging the existing
production PRs and selected preserving full union composition through supported
upstream integration, allowing a later beartype candidate. The recommended
limited native CuPy static policy is accepted alongside verified GPU runtime.
This changes release acceptance, not the installed dependency by guesswork.

## Progress


- [x] (2026-09-08) Re-read repository instructions, inspect all 19 open PR heads,
  and confirm applicable checks are green.
- [x] (2026-09-08) Create `codex/agent-workflow` and a matching worktree from the
  tested `codex/action-runtimes` head.
- [x] (2026-09-08) Opened draft PR #31 against `codex/action-runtimes` before implementation.
- [x] (2026-09-08) Reconciled current agent instructions, contributor commands, plan policy,
  tooling guidance and accepted release decisions.
- [ ] Validate instructions and changed workflows; run hosted candidate checks.
- [ ] Merge the approved history while preserving every focused PR head, verify
  main CI and clean up merged branches/worktrees safely.
- [ ] Record remaining upstream integration and administrative release work.

## Surprises & Discoveries


`CLAUDE.md` is a tracked symlink to `AGENTS.md`; there are no repository-owned
skills or `.claude`, `.codex`, or `.agents` configurations. Do not invent global
skill copies or rewrite personal memories. `CONTRIBUTING.md` still names retired
`bt022` tox environments and describes CI tiers that now share one matrix.
`docs.yml` currently deploys on every main push, although this approval covers
merging rather than publishing the candidate documentation.

## Decision Log


The owner said “First option. Merge approved” and requested agent-file/tooling
updates on 2026-09-08. Apply the previously recommended first choices: full
native union composition through supported upstream integration, with a later
beartype candidate allowed; explicit limited CuPy static support. Preserve the
current rc0 lock and exact test lane until an available integration is proven.
Do not adopt unsupported composition restrictions or claim the defect fixed.

Keep one authoritative `AGENTS.md` and its existing Claude symlink. Add local
operational guidance for the existing tools, rather than a speculative skill or
new framework. Existing approval covers merging this requested maintenance once
validated; publication, settings changes and ownership transfer remain separate.

## Outcomes & Retrospective


Implementation and merging are in progress. The original production goal is
not complete until the native composite-union defect is resolved and the
release/handoff acceptance is satisfied. Successful CPU/GPU evidence is retained.

## Context and Orientation


Work runs in `/Users/ale/Code/bearshape-worktrees/agent-workflow`, initially based
on PR #30. The original checkout `/Users/ale/Code/bearshape` is clean main.
`AGENTS.md` is the shared Codex/Claude contract. `PLANS.md` defines living plans.
`CONTRIBUTING.md` is the human command reference. `tools/` contains archive,
installed-consumer, docs/notebook, release-identity and environment validators.
`.github/workflows/validate.yml` is the shared required matrix. Prior focused
implementation PRs are #13–21, #23–26 and #28–30; #12 is the roadmap and #22/#27
are aggregates that preserve their commits and integration resolutions.

## Plan of Work


First open the PR with this plan. Rewrite the short shared agent contract for
maintenance, actual four-checker support, explicit runtime/static boundaries,
locked uv commands, proof requirements and permission persistence. Add a brief
repository-specific section to `PLANS.md` and `tools/README.md` documenting the
existing tools and their dependencies. Correct contributor examples and link
all agent/tool guidance to a single command reference.

Record the accepted union and CuPy decisions in the roadmap and current handoff
report. Retain dated historical evidence in earlier plans; add a clear pointer
to the current decision record rather than rewriting old test results. Restrict
Pages deployment to an explicit manual dispatch while retaining validation on
push. Update the changelog for the maintenance and deployment behavior.

Bring any missing approved heads into this worktree with merge commits. Verify
that the resulting package tree matches the tested candidate before the scoped
maintenance edits. After local and hosted checks pass, merge this PR into #30,
then use the validated aggregate history to merge all approved work to main.
Retain all focused commits and verify each PR head is reachable before deleting
its clean worktree and local/remote branch. Avoid intermediate main states that
would publish docs automatically.

## Concrete Steps


From the worktree, stage and commit the plan, push `codex/agent-workflow`, and
open a draft PR against `codex/action-runtimes`. Use `uv sync --locked` followed
by `uv run --locked prek run -a` and
`uv run --locked prek run actionlint -a --stage manual`. Build docs with
`uv run --locked --only-group docs zensical build --clean` and run
`uv run --locked --only-group docs python tools/check_docs.py`.

Inspect the existing tools' actual `--help`, tox listing and checker harness
before documenting commands. Confirm that Claude resolves the shared file and
that no current command names retired bt022 environments. Run the full shared
hosted matrix before the approved merge, then inspect main's required gate.
Use merge commits and exact expected head SHAs for the GitHub merge operation.

## Validation and Acceptance


An agent entering the repository must find the supported Python/checker/optional
backend boundaries and a working command route without importing optional
backends from the root. The tools guide must accurately state which checks
build/install/execute code and which artifacts and dependencies they need.
Pages pushes must build but skip deployment; only explicit manual dispatch may
deploy. No PyPI release, ownership transfer, settings change or upstream message
is part of these merges. All focused heads must remain in main history. Local
hooks/docs and hosted required validation must pass before work is reported done.

## Idempotence and Recovery


Read status and compare commits before every merge/cleanup. Stop if a worktree
contains user changes. Keep evidence outside disposable worktrees. Use ordinary
merge commits and revert a scoped commit if correction is required; never force
main or erase another contributor's work. A later candidate requires its own
proven integration, updated dependency/lock and complete release validation.

## Artifacts and Notes


Existing evidence lives in
`/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/`. The prior final
wheel SHA256 is `c1806203da013c9eaf2482a309c686a984c0a7031a495efbd100a824536b57d2`.
Its real GPU tests and the full hosted run 34223582731 remain historical proof;
new source archive/tool changes require fresh artifact consumers.

## Interfaces and Dependencies


No public Python API or runtime dependency changes are planned here. Existing
uv, prek, tox, pytest and four checker engines remain authoritative. GitHub CLI
operations use the existing repository connection. Agent guidance remains plain
Markdown with the existing Claude symlink. No new skill runtime is needed.

Revision note (2026-09-08): created before implementation to carry the owner's
contract choices and merge authorization into the maintained repository.

Revision note (2026-09-08): incorporated every reviewed PR head, resolving only
CuPy plan progress text; verified src/tests/tools/dependency/workflow bytes were
unchanged before maintenance. Added the standalone union reproducer and checked
PyPI: rc0 is the only published 0.23 candidate. Current guidance records the
owner's selected path without inventing a newer version or reducing support.

## Merge-record follow-up


PR #31 merged the complete approved history into main at
`df81f00e2f62bda956244e680c980f87db1d4671`. Main CI run 34229683377 passed all 36
jobs; Pages run 34229683120 built successfully and skipped deployment. GitHub
marked main-based PRs merged automatically. Dependent PRs were closed with an
integration record after verifying their heads are ancestors of main; GitHub
refused retargeting them because they contained no new commits.

The same authorized plan now continues on `codex/merge-record`, in its matching
worktree, to record the actual merge outcome and upstream development-head
failure and remove clean merged worktrees/branches. Open the bookkeeping PR
before editing the handoff/roadmap. Runtime code, package metadata, dependencies
and release settings stay as tested. Validate hooks, docs and hosted checks,
then merge this evidence update under the existing owner approval.

Lifecycle discovery (2026-09-08): installing the configured hooks on main
exposed a real worktree commit failure. With no default stage restriction,
`check-illegal-windows-names` ran at `commit-msg` and rejected
`../../bearshape/.git/worktrees/merge-record/COMMIT_EDITMSG`. The attempted
plan commit did not happen. The configuration installs a commit-message shim
without defining any actual commit-message validators. Remove that generated
unused shim, commit this plan with the normal pre-commit checks, open the PR,
then scope unspecified hooks to pre-commit and remove commit-msg from the
installation list. Retain explicit pre-push, post-checkout/merge/rewrite and
manual actionlint stages. Verify the real lifecycle after the fix and document
how existing contributors remove the stale shim. No checks will be bypassed.
