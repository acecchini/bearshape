# Verify the corrected CuPy runtime on CUDA


Maintain this ExecPlan according to `PLANS.md`. This independent validation PR is based on integration PR #22, which includes the lifetime and converter corrections.

## Purpose / Big Picture


CuPy users need evidence from actual GPU arrays. Prove strict shape/dtype validation, backend conversion, preservation of device/native objects, and optree containers against a normally installed candidate wheel with exact beartype 0.23.0rc0. CPU skips cannot establish this contract.

## Progress


- [x] (2026-09-08) Created codex/cupy-runtime and matching worktree from b2a1df0.
- [x] (2026-09-08) Opened draft PR #26 and added 12 conversion/device/tree cases.
- [ ] Publish public test/source commits and build their source-derived wheel.
- [ ] Run baseline and new GPU cases on Python 3.10 and 3.14; record artifacts and versions.
- [ ] Validate hooks/hosted checks and obtain user validation before merge.

## Surprises & Discoveries


The baseline already passed 83 CuPy tests on H200 with CuPy 14.2.0 and both Python endpoints. That artifact predates the lifetime/conversion corrections, so it is insufficient evidence for the combined candidate. The first corrected-candidate run passed 94 tests and exposed one incorrect new test assumption: CuPy 14.2.0 accepts structured host arrays. Verified dtype preservation and generic Shaped/Like acceptance, then corrected the test and stale module comment. Native CuPy 14.2.0 has no py.typed marker or ndarray stubs; the static support decision remains separate and pending.

## Decision Log


Decision: Add GPU behavioral tests to tests/test_cupy.py without changing runtime or static promises. Rationale: the combined corrections require device-backed verification; this milestone does not authorize a reduced static contract. Date: 2026-09-08.

Decision: Use the configured h200 host, its isolated /tmp/bearshape-production-2026-09-08 environments and CUDA_VISIBLE_DEVICES=6 after checking availability. Rationale: use a free GPU without touching other users' processes or global packages. Transfer only public committed package/test content with recorded provenance.

## Outcomes & Retrospective


Implementation pending. A04 native union rollback and CuPy static support remain separate release decisions; successful GPU tests cannot close them.

## Context and Orientation


Worktree /Users/ale/Code/bearshape-worktrees/cupy-runtime, branch codex/cupy-runtime. tests/test_cupy.py owns existing GPU tests. src/bearshape/cupy.py selects cp.asarray and trusts only native CuPy arrays. src/bearshape/_array_types.py now obeys the selected converter and rolls back failed leaf validation. bearshape.optree.Tree validates all leaves and shared structure using optree's default registry.

The isolated remote Python 3.14 environment is /tmp/bearshape-production-2026-09-08/cupy-baseline/.venv; Python 3.10 is /tmp/bearshape-production-2026-09-08/cupy-python310. CUDA_PATH is /usr/local/cuda-12.9. Existing baseline tests and artifacts are public; verify new file bytes against the new public commit before transfer.

## Plan of Work


Add observable cases comparing Like acceptance with cp.asarray for valid noncontiguous/endian host arrays and unsupported string/object arrays and supported structured arrays. Test that validation leaves a native device array's identity, device and allocation unchanged, including nondefault CUDA streams. Exercise nested optree containers, inconsistent leaf shapes/dtypes, structure binding and failed-check recovery on device arrays.

Build a source archive and wheel from that archive. Normally install the wheel with exact beartype rc0 in each isolated endpoint environment, then run copied tests outside source checkouts. Require real CuPy/optree imports and an available GPU before pytest; an importorskip-only exit is not proof. Record source commit, artifact SHA256, installed origin, versions, GPU and CUDA data.

## Concrete Steps


From the worktree run uv build --sdist and uv build --wheel with the resulting archive, then tools/check_distribution.py. Publish the authorized draft PR commit first and verify public provenance before transferring the wheel and tests.

On h200 run the selected environment's Python with CUDA_VISIBLE_DEVICES=6 and CUDA_PATH=/usr/local/cuda-12.9. Normally install the candidate and beartype==0.23.0rc0. Use python -I -m pytest against the copied test_cupy.py. Run the maintained hooks and inspect hosted PR checks locally.

## Validation and Acceptance


Both endpoints must pass existing and added GPU tests without missing-CuPy/optree skips. Valid host values must convert with cp.asarray and satisfy Like; unsupported values must fail both conversion and validation. Native validation must preserve object/device/pointer and tree checks must reject inconsistent shapes, dtypes and structures. Logs must prove site-packages imports and exact beartype. Report the tested CuPy/CUDA/GPU versions without implying every driver or multi-GPU combination is covered.

## Idempotence and Recovery


Use isolated task directories and selected free device only. Never kill unrelated processes, install global packages, change main, merge, publish a package or transfer ownership. Retry failed validation after understanding its cause and preserve the logs.

## Artifacts and Notes


Save evidence under /Users/ale/Code/bearshape-implementation-2026-09-08/evidence/cupy-candidate-*. Include a provenance record and exact commands so maintainers can rerun on another CUDA host.

## Interfaces and Dependencies


No public API changes. Tests use NumPy, CuPy, optree, beartype and pytest. CuPy remains outside CPU dependency groups. The configured GPU environment has CuPy 14.2.0; explicit optree installation is required for the additional container cases.
