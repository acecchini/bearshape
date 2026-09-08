# Prepare the production review and ownership handoff evidence


Maintain this ExecPlan according to PLANS.md. This focused evidence PR follows publication gate #28 and closes independent M6/M9 documentation and measurement work. It does not authorize merge, publication, settings changes or transfer.

## Purpose / Big Picture


Receiving maintainers need a concise, accurate map of what bearshape does, which behavior is tested, where the implementation lives, and which release decisions remain. Provide reproducible performance observations and a review packet tied to fixing PRs and artifact evidence, without claiming unresolved compatibility is complete.

## Progress


- [x] (2026-09-08) Created codex/handoff-evidence and matching worktree from 3ee4c1d.
- [ ] Open focused draft PR and map public features to existing positive/negative tests.
- [ ] Add a small repeatable benchmark and compare exact-rc0 baseline/candidate on matched Python and hardware.
- [ ] Write support/module/audit-finding and administrative handoff evidence.
- [ ] Validate docs, hooks and current combined artifacts/hosted checks.
- [ ] Present remaining contract decisions and obtain user validation before merge.

## Surprises & Discoveries


Most features already have focused positive/negative tests; wholesale test reorganization would add churn. The fixes needed new actual caller, lifecycle, converter and checker proofs. Real CuPy 14.2.0 accepts structured arrays through its converter, contradicting an old comment; 95 GPU tests now pass at both Python endpoints. Native CuPy typing and native union-alternative rollback remain separate unresolved release decisions.

## Decision Log


Decision: Keep a concise feature-to-test map and link existing tests instead of duplicating them for coverage counts. Rationale: maintainers should see the contract and closing evidence directly. Date: 2026-09-08.

Decision: Record medians and min/max for ordinary successful checks, Like conversion, Value, trees, nesting and diagnostic failures. Rationale: metadata checks, conversion and leaf traversal have different scaling. Use no noisy timing threshold in CI and make no universal speed claim. Benchmark ordinary already-correct cases while explicitly retaining the unresolved union blocker.

Decision: Keep ownership URLs pointed at the real current repository and document exact proposed settings without changing them. Rationale: transfer and access controls require explicit owner authorization. Record PyPI publisher configuration as unverified until an authorized administrator checks it.

## Outcomes & Retrospective


Evidence work pending. Production readiness remains withheld for A04 and the CuPy static support decision. The final review must distinguish implemented/validated source changes from administrative release readiness and merge approval.

## Context and Orientation


Worktree /Users/ale/Code/bearshape-worktrees/handoff-evidence, branch codex/handoff-evidence. Runtime code is under src/bearshape; tests are organized by shape/dimensions/dtypes/memo/decorator/backend/tree/checker contracts. The shared workflow proves the CPU platform matrix and normally installed artifacts. GPU logs under /Users/ale/Code/bearshape-implementation-2026-09-08/evidence prove real CuPy behavior separately.

The audit benchmark used Python 3.10.20, NumPy and exact beartype 0.23.0rc0. The rc0-compat worktree retains the old runtime with the rc0 floor; its .tox/py310-bt023rc0-cpu interpreter is suitable for a matched baseline. The current candidate uses the same interpreter generation and hardware. Verify dependency versions and source origins before comparing.

## Plan of Work


Add tools/benchmark_runtime.py using timeit, statistics and existing NumPy/optree dependencies. Report interpreter/platform, package versions/origin, call counts, repeat count and medians/min/max. Use tiny and million-element native arrays, cap conversion/failure repetitions appropriately, and vary tree leaf count. Do not mutate runtime behavior or add optimization caches.

Inspect the public-feature tests and record representative positive/negative classes in docs/maintainers/production-readiness.md. Include intended users and deployment boundaries, module map, backend/checker/platform support evidence, private beartype integration assumptions, A01–A10 closing PRs, migrations, known blockers and artifact/CI links. Add the page to documentation navigation and keep the README short.

Record the inspected main/ruleset/environment state and exact proposed controls: reviewed required validation status, protected release tags, pypi reviewers and tag-only policy, OIDC publisher identity, docs hosting and package owners. No administrative mutation occurs. Complete the release validation-only run and preserve its artifact identity in the report when available.

## Concrete Steps


Run the benchmark script with the rc0-compat Python 3.10 interpreter and the current candidate's Python 3.10 environment, using the same script and machine. Save JSON outputs under evidence/performance-*. Compare only matched workloads and versions.

Run uv run --locked prek run -a, the manual actionlint hook, the clean docs build and tools/check_docs.py. Inspect the feature map's referenced test classes and final hosted jobs. Update this plan and the roadmap with verified counts and open decisions.

## Validation and Acceptance


Every maintained feature family has identifiable positive/negative evidence, with runtime-only syntax and upstream static limitations explicit. The benchmark is reproducible and reports spread; no speed claim depends on mismatched environments. The handoff report maps all audit findings to fixes or explicit blockers, includes source/artifact identity and observed CI/GPU results, and states administrative controls accurately. User validation and unresolved contract decisions remain visible.

## Idempotence and Recovery


Measurements and documentation can be repeated without changing runtime or external ownership. Use task-local files and environments; do not overwrite audit evidence. Do not merge any actual PR base, publish packages, change protections or contact maintainers. Preserve the original checkout and all focused PR review boundaries.

## Artifacts and Notes


Store measurement and handoff evidence under /Users/ale/Code/bearshape-implementation-2026-09-08/evidence. The report should link public PRs and Actions runs; local logs supply detailed supporting evidence. Keep actual final candidate hashes distinct from earlier validation artifacts.

## Interfaces and Dependencies


No runtime dependency or public API changes. The benchmark uses standard timing tools plus the existing optional CPU backends. The report and navigation use the existing Zensical site and corrected Markdown formatter configuration.
