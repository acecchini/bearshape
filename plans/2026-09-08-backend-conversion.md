# Validate Like inputs with the target backend's converter


Maintain this ExecPlan according to `PLANS.md`. This independent PR addresses audit A05 for the accepted bearshape `0.1.0rc0` release.

## Purpose / Big Picture


A backend Like annotation should accept an input only when its documented converter can produce an array satisfying the shape and casting policy at validation time. The current generic NumPy fallback accepts inputs that Torch/JAX reject, and trusting every NumPy array bypasses backend constraints such as native byte order and supported dtype.

## Progress


- [x] (2026-09-08) Inspected shared conversion and backend trust paths.
- [ ] Open draft PR and reproduce backend conversion counterexamples.
- [ ] Remove misleading fallback and narrow default backend trust.
- [ ] Validate positive/negative conversion, casting, shape and argument preservation.
- [ ] Record runtime/checker/hook evidence and remaining CuPy limitation.

## Surprises & Discoveries


Torch rejects negative-stride and non-native-endian NumPy arrays, while its current F32Like accepts them. JAX/Torch reject NumPy string arrays while ShapedLike accepts them. A NumPy-only __array__ protocol can be accepted by fallback after Torch conversion fails. These defects reproduce on both baseline and exact beartype rc0.

## Decision Log


Decision: Call the selected backend converter without a fallback that changes its meaning. Rationale: fallback acceptance does not establish the public target-backend contract. Keep NumPy as the default only when no converter is configured. Date: 2026-09-08.

Decision: Default backend trust includes only its native array class, not all NumPy arrays. Rationale: backend-native metadata checks avoid unnecessary conversion, while foreign input requires actual conversion proof. Explicit custom trusted_types remains a factory-author assertion and must be documented as such.

## Outcomes & Retrospective


Implementation pending. This PR must show actual converter/validator agreement for the observed counterexamples and ordinary valid inputs. CuPy source consistency can be reviewed locally; CUDA runtime behavior remains unverified until a GPU run.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/backend-conversion`, branch `codex/backend-conversion`, base `f43e00d`. `_array_types.py::_ArrayLikeChecker._convert` currently falls back to np.asarray after converter failure. `_validate` bypasses conversion for trusted arrays. `jax.py`, `torch.py`, and `cupy.py` define backend converters and trust tuples. `tests/test_jax.py`, `test_torch.py`, `test_numpy.py`, and `test_cupy.py` cover their surfaces. `docs/features/like-types.md` describes conversion/casting.

## Plan of Work


Add failing regression tests comparing actual converter failure with Like rejection for negative strides, non-native byte order, string dtype and NumPy-only protocols. Cover custom converter failure on inputs NumPy would accept. Then select exactly one converter in `_convert`, retaining useful failure details, and narrow the backend trust tuples to native arrays. A configured custom converter without an explicit trust declaration must not be bypassed by the default NumPy fast path.

Keep strict validators unchanged and preserve same-kind casting semantics. Like validation does not replace the function argument; test original-object identity, supported lists/scalars/views and native Torch autograd preservation. Run converter-oracle tests for backend-supported numeric and unsupported nonnumeric inputs. Revise tests asserting the obsolete NumPy trust tuple into behavioral checks or the corrected explicit contract. Update docs and CHANGELOG with the rejected false positives, converter semantics and potential validation allocation.

## Concrete Steps


Run from this worktree:

    uv sync --locked
    uv run --locked pytest -n 0 tests/test_torch.py tests/test_jax.py -k ConversionContract
    uv run --locked pytest -n auto tests --ignore=tests/test_typecheck.py
    uv run --locked pytest -n auto tests/test_typecheck.py
    uv run --locked prek run -a

Save regression failures before source changes, then run the complete runtime suite with the isolated exact-rc0 Python 3.10/3.14 interpreters and this worktree's source path. Do not treat these source checks as installed-artifact validation; the integration/release milestone handles that separately.

## Validation and Acceptance


The converter and Like result agree for every new oracle case under the selected casting policy. Invalid values reject with useful conversion details; valid existing inputs pass unless correcting a documented false positive. Argument identity, dtype/device and autograd are preserved for native Torch inputs. Rank/dimension checks still run after conversion, and native strict checks do not convert. Current checker fixtures and hooks pass. CuPy remains an explicit GPU validation gate.

## Idempotence and Recovery


Use the isolated feature worktree and pytest temporary state. Do not modify user arrays in validation or silently detach gradients. Keep explicit factory parameters stable. Preserve main and require user validation before merge.

## Artifacts and Notes


Record results in `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/` and summarize observed counts here. Separate lifetime correction is PR #15; this PR must not duplicate that source change.

## Interfaces and Dependencies


Public backend Like names and make_array_like_type parameters remain available. `asarray=None` selects NumPy conversion. A custom trusted_types tuple explicitly declares which inputs may bypass that converter, so its author must ensure that assertion is valid. Root imports remain backend-independent. No new runtime dependency is introduced.

Revision note — 2026-09-08: Added focused conversion plan before implementation.
