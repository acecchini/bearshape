# Prove framework transformations and minimal runtime imports


Maintain this ExecPlan according to `PLANS.md`. This independent validation PR covers the framework/import-boundary portion of M6 and is stacked on exact-candidate compatibility PR #13.

## Purpose / Big Picture


ML users need to know when validation occurs around JAX transformations and Torch compilation, and users of custom array classes should not need to install an unrelated backend. Maintain small behavioral tests of those boundaries and document the actual execution behavior.

## Progress


- [x] (2026-09-08) Created isolated branch/worktree from exact-rc0 compatibility.
- [x] (2026-09-08) Opened draft PR #21 and inspected backend transform behavior with small CPU probes.
- [x] (2026-09-08) Added four JAX and two Torch transformation tests with valid and invalid calls.
- [x] (2026-09-08) Normally installed candidate wheel passes minimal custom-array checks on Python 3.10.20 and 3.14.5.
- [x] (2026-09-08) Current suite, JAX/Torch floors, exact-candidate endpoint probes, hooks and docs build pass.
- [x] (2026-09-08) Added framework placement guide and recorded validation evidence.
- [ ] Obtain hosted CI results and user validation before merge.

## Surprises & Discoveries


The existing runtime suite validates metadata but does not establish JAX jit/vmap/grad or Torch compile behavior. Transform placement changes whether Python validation runs at an outer call or while tracing the function. The configured h200 host is available; separate preliminary GPU validation has now passed 83 existing CuPy tests with the normally installed candidate wheel and exact beartype rc0. Comprehensive CuPy/static validation remains separate from this CPU transform PR.

## Decision Log


Decision: Add observed behavior tests without promising static shape inference or checks inside every compiled execution. Rationale: framework tracing and compilation are separate execution models; tests must demonstrate the placement/limits. Date: 2026-09-08.

Decision: Use small CPU arrays, JAX transformations, and Torch's eager compile backend to test the compiler front end. Rationale: no GPU or platform-specific native compiler is needed for these maintained checks. Do not claim this proves every compiler backend or dynamic-shape mode.

Decision: Add an isolated minimal-install smoke command, using only declared runtime dependencies and a custom shape/dtype object. Rationale: source checkout imports with all developer dependencies cannot prove the lightweight root contract.

## Outcomes & Retrospective


Six maintained transformation cases pass on Python 3.10 and 3.14 with exact beartype 0.23.0rc0. The development suite passes 1,070 tests with five platform/optional skips and 91.04% coverage. Floor lanes pass 210 JAX tests and 208 Torch tests; their 21/24 skips cover intentionally absent other backends and unavailable extended precision. JAX 0.5 emits 18 existing FutureWarnings for None conversion; these do not come from the new transformation cases. The framework guide builds without issues.

Minimal normally installed wheels pass custom-array acceptance, shape/dtype/return rejection and optional-import assertions on Python 3.10.20 and 3.14.5. These environments contain only bearshape, exact beartype rc0 and typing_extensions. These tests establish the documented placements, not exhaustive framework compatibility.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/framework-validation`, branch `codex/framework-validation`, base `346347b`. `tests/test_jax.py` and `tests/test_torch.py` own backend tests and are selected by existing tox factors. `src/bearshape/_memo.py` discovers beartype frames; `_decorator.py` adds explicit contexts. No behavior changes are initially planned here. Add `tools/smoke_minimal.py` and a concise framework guide linked from the docs navigation.

## Plan of Work


Probe beartype placement inside/outside JAX jit and verify valid results, shape/dtype rejection, and tracing versus repeated execution. Exercise vmap over validated row functions and gradients of a validated scalar loss. Keep dimension annotations consistent with the function's logical unbatched input shape.

Exercise native Torch autograd through strict validation and torch.compile with backend="eager" for a small validated function. Verify valid outputs and wrong metadata rejection; characterize graph breaks or unsupported fullgraph placement rather than asserting optimization properties. Keep optional compiler/tool availability separate from normal eager/autograd support. Promote observed supported cases into the existing backend test files so their dependency-floor tox lanes execute them.

Create a minimal-install smoke command that imports the installed root, verifies no optional backend module was imported, builds a custom array annotation through the public factory, and demonstrates correct/incorrect shape and dtype calls. Run it with Python's isolated mode from a fresh environment containing the normally installed wheel plus exact beartype rc0 and no NumPy/JAX/Torch/CuPy/optree. Verify the package is imported from that environment's site-packages. Add a focused CI job to reproduce this proof; broader CI consolidation can reuse it later.

Document actual supported placement and tracing/compilation limitations in a concise guide, and update CHANGELOG for the validated support contract. Run current/floor backend tests and exact-candidate Python endpoints. Preserve known native-union rollback work as a separate release blocker.

## Concrete Steps


From this worktree:

    uv sync --locked
    uv run --locked pytest tests/test_jax.py tests/test_torch.py -n 4
    uv run --locked tox run -e py310-bt023rc0-jax05,py310-bt023rc0-torch26
    uv run --locked prek run -a

Use an external fresh environment for `python -I tools/smoke_minimal.py`; installing the project with no dependencies or using PYTHONPATH does not establish artifact compatibility. The artifact can be normally installed with an exact beartype constraint. Record the actual installed version and source path.

## Validation and Acceptance


Each maintained transform case demonstrates a valid result and a relevant rejection, with tracing behavior documented accurately. The NumPy-free custom-array smoke command passes on normally installed candidate wheels at the Python endpoints. Existing runtime/checker/hooks pass. Backend-floor test runs execute the added cases. No CUDA support, fullgraph compilation, dynamic-shape specialization, or per-compiled-invocation check is claimed without corresponding evidence.

## Idempotence and Recovery


Use tiny arrays, temporary install environments and isolated worktrees. Do not alter framework global defaults, existing GPU workloads, system Python packages or package ownership. Keep main unchanged and obtain user validation before merge.

## Artifacts and Notes


Record `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/framework-*.log` and minimal-install logs. GPU baseline evidence is `cupy-remote-baseline.log` and is explicitly preliminary; source integrity was verified against the public PR before transfer.

## Interfaces and Dependencies


Use existing beartype/bearshape public annotations and JAX/Torch APIs already in dependency groups. No runtime dependency or public API addition is planned. Runtime shape relationships remain distinct from static backend/dtype information. The minimal smoke script relies only on Python and the declared runtime dependencies.

Revision note — 2026-09-08: Added focused framework/import validation plan before implementation.

Revision note — 2026-09-08: Recorded implemented transformation and minimal-install contracts, endpoint/floor results and existing JAX warning scope.
