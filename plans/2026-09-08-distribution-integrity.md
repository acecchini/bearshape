# Ship complete, testable source and wheel distributions

Owner update (2026-09-08): the reviewed implementation and recorded validation
are approved for merge. This supersedes earlier pending-approval statements.
Full native union composition remains required through supported upstream
integration, with a later candidate allowed; limited CuPy native static support
is accepted. Current merge execution and remaining release gates are tracked in
`plans/2026-09-08-agent-workflow.md` and the production-readiness roadmap.



Maintain this ExecPlan according to `PLANS.md`. This independent PR addresses audit A07 for the accepted bearshape `0.1.0rc0` release; version and beartype metadata are separate PR #13.

## Purpose / Big Picture


A downstream user must receive the actual MIT license notice with the installed package. A maintainer receiving the source archive must be able to rebuild the wheel and run the included regression suite without retrieving missing configuration from GitHub. Check the real archives, not just the source metadata.

## Progress


- [x] (2026-09-08) Created isolated feature worktree and reviewed uv's inclusion rules and the audit evidence.
- [x] (2026-09-08) Opened PR #18 and reproduced missing License-File metadata/license with the new archive check.
- [x] (2026-09-08) Included license/testing inputs, added the archive validator and required CI job.
- [x] (2026-09-08) Rebuilt and normally installed the wheel in an external consumer; root imports no optional backend. Copied archive tests pass against the installed wheel: 652 passed, seven explicit missing-backend/platform skips.
- [x] (2026-09-08) All hooks pass; recorded hashes and retained exact-rc0 integrated artifact validation as a separate release gate.

## Surprises & Discoveries


The original wheel and sdist contain `License-Expression: MIT` but omit LICENSE. uv includes license files only when declared, and its default source archive omits the repository tests/configuration. A successful build alone does not prove either property.

## Decision Log


Decision: Keep uv_build, declare `license-files = ["LICENSE"]`, remove the redundant license classifier, and explicitly include the existing tests and their configuration in the sdist. Rationale: this corrects artifact contents without replacing the build backend or adding runtime dependencies. Date: 2026-09-08.

Decision: Add one small archive validation command usable by CI/release work. Check the license bytes and metadata, package typing marker, expected modules, and source test inputs. Build a wheel from the produced source archive before installation. Rationale: publishing must validate the exact artifact it will upload, without rebuilding after approval.

## Outcomes & Retrospective


Implemented complete source/wheel contents with executable archive checks. The unchanged artifacts fail, while the rebuilt artifacts pass and support 652 installed-wheel tests. Exact beartype rc0 installation requires integrating PR #13 because this independent branch retains main's old dependency bound. Record this distinction rather than treating a source overlay or dependency-free install as distribution proof.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/distribution-integrity`, branch `codex/distribution-integrity`, base `f43e00d`. `pyproject.toml` owns build metadata and source inclusion. `LICENSE` contains the notice. The module tree is `src/bearshape`, with `py.typed` declaring inline typing information. `tests/`, `pytest.toml`, `tox.toml`, `ty.toml`, `ruff.toml`, `tools/`, and `uv.lock` support downstream validation. Add `tools/check_distribution.py` for inspecting a wheel and source archive.

## Plan of Work


First build the unchanged project into an evidence directory. Implement archive checks and show that the old archives fail because their license is absent. Then declare the license files and source inclusion in pyproject. Include tests, tools, checker/pytest/tox configuration, the lockfile, contributor instructions and changelog. Exclude caches, virtual environments, audit evidence and generated docs by retaining deliberate inclusion rather than adding the entire repository.

Build the sdist with `uv build --sdist`, then pass that archive to `uv build --wheel`. Inspect both archives with the new command, including matching license/version metadata and the package typing marker. Record SHA-256 hashes. Install the rebuilt wheel with normal dependency resolution in a fresh environment outside all checkouts; prove imports originate in that environment and root import loads no optional backend. Run representative runtime tests copied from the source archive, and verify that those tests do not load source from the original checkout.

Add contributor commands for reproducible archive inspection and update CHANGELOG. The broader CI/release PR will invoke this command for its built artifacts and extend installed-wheel proof to the integrated checker suite and exact candidate on both Python endpoints.

## Concrete Steps


From this worktree:

    uv build --sdist --out-dir /Users/ale/Code/bearshape-implementation-2026-09-08/evidence/distribution-before
    uv build /absolute/path/to/bearshape-0.0.1.tar.gz --wheel --out-dir /absolute/path/to/artifacts
    python tools/check_distribution.py /absolute/path/to/artifacts/bearshape-0.0.1-py3-none-any.whl /absolute/path/to/artifacts/bearshape-0.0.1.tar.gz
    uv run --locked prek run -a

Use the actual filenames produced by each build. No publication command is part of this work. Preserve all before/after artifacts under the implementation evidence directory.

## Validation and Acceptance


The unchanged archives fail the license check. Corrected wheel and sdist contain identical LICENSE text and matching license/version metadata; wheel contains all package modules and py.typed; sdist contains a runnable test/configuration set. A rebuilt wheel installs normally outside the source tree and imports from site-packages. Core NumPy and tree consumer checks succeed with installed optional dependencies. Hooks leave no uncommitted formatting changes. Integration must repeat the normal installation with beartype 0.23.0rc0 before final release signoff.

## Idempotence and Recovery


Use separate output directories so old and new archives remain inspectable. Do not clear or overwrite user releases. Fresh temporary consumers avoid editable import leakage. Do not merge without user validation or publish without explicit authorization.

## Artifacts and Notes


Evidence is under `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/`: `distribution-before-check.log` fails for the absent License-File; `distribution-after-check.json` records the matching archive check and hashes; `distribution-install.log` shows a normal wheel install and site-packages import with only declared dependencies before optional NumPy/optree installation; `distribution-installed-tests.log` reports 652 passed and seven explicit platform/missing-JAX/Torch skips; `distribution-hooks-final.log` is clean. The isolated consumer is `/Users/ale/Code/bearshape-implementation-2026-09-08/distribution-consumer`; it contains no package source tree. Its tests came from the sdist.

## Interfaces and Dependencies


The archive validator accepts a wheel path followed by an sdist path and exits nonzero for missing/mismatched required contents. Use Python's standard library for archive/metadata/hash inspection. Keep runtime dependencies and public API unchanged. Test/archive tooling uses uv, already the project's supported development tool.

Revision note — 2026-09-08: Added focused distribution plan before implementation.

Revision note — 2026-09-08: Implemented archive integrity checks and recorded normal external wheel installation plus downstream runtime evidence. Final combined rc0 artifacts remain an integration requirement.

Revision note (2026-09-08): reconciled completed milestone/hosted evidence and
explicit owner merge approval. The combined artifact, checker and GPU proofs
are in `docs/maintainers/production-readiness.md`; this update does not mark
the unresolved native-union integration or release administration complete.
