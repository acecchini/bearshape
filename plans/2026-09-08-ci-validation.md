# Make CI reproduce the release support contract

Owner update (2026-09-08): the reviewed implementation and recorded validation
are approved for merge. This supersedes earlier pending-approval statements.
Full native union composition remains required through supported upstream
integration, with a later candidate allowed; limited CuPy native static support
is accepted. Current merge execution and remaining release gates are tracked in
`plans/2026-09-08-agent-workflow.md` and the production-readiness roadmap.



Maintain this ExecPlan according to `PLANS.md`. This focused CI PR is stacked on integration draft #22 and implements M7. Documentation formatting and publication authorization remain separate PRs.

## Purpose / Big Picture


Maintainers need a single reproducible validation workflow that tests the candidate on supported interpreters and platforms, fails when expected backends/checkers are missing, and cannot report success after a required job fails or is skipped. CPU jobs should install CPU Torch. Local hooks and hosted checks should execute the same maintained tools.

## Progress


- [x] (2026-09-08) Created matching branch/worktree from the combined candidate.
- [x] (2026-09-08) Opened PR #23 and inspected actual uv/tox installer configuration.
- [x] (2026-09-08) Added shared workflow with nine platform runtime lanes, five current checker lanes and twelve floor lanes.
- [x] (2026-09-08) Backend preflight asserts exact rc0 and CPU Torch; tox forwards UV_TORCH_BACKEND=cpu.
- [x] (2026-09-08) Full hooks/actionlint run in CI; validation/docs actions pinned with weekly update configuration. Publication action changes remain in M9.
- [x] (2026-09-08) All hosted required jobs pass at 688e669; local dev and candidate endpoints pass; gate probes reject failure, skip and cancellation.
- [x] (2026-09-08) Recorded implementation, hosted results and the reproduced pyright environment defect.
- [x] (2026-09-08) Obtain user validation before merge.

## Surprises & Discoveries


The root uv source mapping does not control tox's uv pip installs, so Linux CPU compatibility lanes currently install CUDA Torch dependencies. The current PR workflow duplicates typing runs, differs from nightly, lacks a final required gate, and runs only a subset of local hooks. Docs deployment installs default development dependency groups despite its docs-only purpose. The installed uv supports UV_TORCH_BACKEND=cpu; validate that tox forwards it before claiming CPU-only behavior.

## Decision Log


Decision: Keep one reusable validation workflow used by PR/push and nightly, accepting a ref for later immutable release validation. Rationale: shared checks prevent publishing from relying on a weaker, separate test path. Default caller ref remains the exact event SHA. Date: 2026-09-08.

Decision: Exercise current locked CPU backends on Python 3.10–3.14 under Linux and both endpoints on macOS/Windows, subject to demonstrated backend wheel availability. Keep explicit dependency/checker floor lanes on Linux. Rationale: checkers and backends have interpreter-specific wheels; cross-platform claims require actual jobs.

Decision: Make missing expected backends and non-CPU Torch fatal in their CPU lanes. Rationale: importorskip remains useful for optional local environments but cannot establish a required support lane.

Decision: Use full commit pins for external actions with a maintained update configuration. Run the locked prek suite plus actionlint, and fail if formatting/locking changed tracked files. Rationale: local and hosted tool drift already caused failures during the audit.

## Outcomes & Retrospective


All 32 required hosted jobs pass at implementation commit 688e669, including the aggregate gate, plus the external secret scan. Local development tests pass 1,074 cases with five documented skips and 91.62% coverage; exact-candidate CPU endpoint lanes each pass 1,066 runtime tests. The narrower tox-driver install exposed pyright environment routing that a populated developer environment hid; removing the fixed venv selection makes the selected interpreter authoritative. A successful CPU matrix does not prove CuPy GPU execution or resolve the native-union integration blocker.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/ci-validation`, branch `codex/ci-validation`, base integration `b2a1df0`. `.github/workflows/ci.yml` and `nightly.yml` duplicate matrices. `tox.toml` defines candidate/floor factors; `tests/conftest.py` filters optional backend suites. `tests/test_typecheck.py` executes all four checker positive/negative batches. `tools/check_distribution.py` and `tools/smoke_minimal.py` provide independent artifact/minimal checks.

## Plan of Work


Introduce `.github/workflows/validate.yml` with explicit quality, current-runtime, checker, compatibility-floor, docs, distribution/minimal jobs and an always-running required gate. Keep CI/nightly as small callers of this common workflow. Parameterize only the checkout ref needed by release validation, rather than generating matrices in a separate framework.

Add a small backend preflight command that imports requested modules, reports actual versions/origins, asserts exact beartype and verifies CPU Torch when selected. Reuse it in locked CPU jobs and tox before tests. Configure tox's uv installer with CPU backend selection and inspect generated commands plus Linux package resolution. Preserve absent-backend skips only outside the selected lane.

Run all normal prek hooks in quality, then manual actionlint. Replace the standalone unpinned pre-push pyright hook with the locked four-checker harness. Keep the existing local pytest pre-push behavior. Pin external actions, add weekly GitHub Actions updates, and limit docs deployment to the locked docs group. Add a changelog/contributor note describing the actual validation commands and support matrix.

## Concrete Steps


Run targeted tox configuration inspection and backend preflight first, then:

    uv run --locked tox run -e dev,py310-bt023rc0-cpu,py314-bt023rc0-cpu
    uv run --locked prek run -a
    uv run --locked prek run actionlint -a --stage manual

Push the draft to execute the hosted matrix. Read failed-job logs, fix demonstrated issues, and rerun only affected checks unless changes require broader validation. Test that the final gate accepts only success for every required job result.

## Validation and Acceptance


The current locked suite executes every selected backend and checker. Exact rc0 is asserted. Linux CPU Torch has no CUDA build, macOS/Windows endpoint results are recorded accurately, backend/checker floor jobs pass, distributions/minimal installs pass, docs build passes, and all hooks execute. Required failures/skips/cancellations cannot produce a green final gate. No branch protection or environment settings are changed by this PR.

## Idempotence and Recovery


Use only the isolated worktree and disposable test environments. Workflow edits may consume normal GitHub Actions runs but do not publish, deploy the candidate branch or change administrative settings. Keep main unchanged and request user validation before merge.

## Artifacts and Notes


Record `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/ci-*` and hosted run/job links. Use actual platform/version results when updating the final support matrix. The combined pre-CI baseline passed 1,074 tests with five skips and 91.62% coverage.

## Interfaces and Dependencies


Runtime dependencies remain beartype and typing_extensions. CI uses the locked uv/prek/checker toolchain, the existing test/backend groups and tox factors. The reusable workflow's checkout-ref input is for validation only and carries no publication permission.

Revision note — 2026-09-08: All nine hosted platform runtime lanes, current checker lanes, backend floors, docs, quality and artifacts passed. The pyright floor failed because hard-coded venvPath/venv overrode its explicit tox interpreter. Reproduced locally only after exact-syncing the driver to the test-only group; inexact uv run had retained backend packages and hidden the defect. Removed the redundant fixed environment selection, retaining explicit harness interpreter paths.

Revision note (2026-09-08): reconciled completed milestone/hosted evidence and
explicit owner merge approval. The combined artifact, checker and GPU proofs
are in `docs/maintainers/production-readiness.md`; this update does not mark
the unresolved native-union integration or release administration complete.
