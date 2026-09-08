# Make static Like inputs reflect ordinary backend conversion


Maintain this ExecPlan according to `PLANS.md`. This PR addresses the Like/Shaped part of audit A06 and depends on the checker harness in PR #17. Its base is `codex/checker-conformance`; runtime conversion correctness remains separate PR #16.

## Purpose / Big Picture


Users should be able to pass float64 NumPy arrays to F32Like and ordinary numeric lists/scalars to JAX/Torch Like functions without spurious static errors. Strict annotations still describe native backend arrays. Like describes convertible input, so its inferred type must include those input forms rather than pretending conversion has replaced the argument.

## Progress


- [x] (2026-09-08) Created isolated branch/worktree and inspected the current aliases and converter contract.
- [ ] Open draft PR and add failing real consumer fixtures.
- [ ] Align NumPy casting families and broad Shaped dtype typing.
- [ ] Model JAX/Torch numeric scalar, array, and nested-sequence inputs.
- [ ] Run positive/negative/inference checks on four engines and runtime controls.
- [ ] Update docs, changelog and validation evidence.

## Surprises & Discoveries


Current NumPy Like aliases use the destination precision as the allowed input dtype, even though same-kind casting permits other widths and lower numeric kinds. JAX/Torch Like aliases are only the native Array/Tensor type. NumPy Shaped excludes strings and object arrays despite their valid runtime shape checks. The existing public NumPy ArrayLike template uses NumPy's nested-sequence protocol, which must be exercised with already-typed nested lists and deliberate invalid strings/dictionaries.

## Decision Log


Decision: Preserve numeric families and widen input dtype widths according to same-kind casting; keep scalar/list support explicit. Rationale: accepting all objects would hide ordinary mistakes, while exact destination dtype gives false rejections. Runtime remains responsible for shape, representable backend dtypes, byte order, device and value-dependent conversion constraints. Date: 2026-09-08.

Decision: Use concrete native/NumPy array types for JAX/Torch inputs and numeric nested sequences, without treating every NumPy __array__ protocol as proof of Torch conversion. Rationale: PR #16 demonstrates that a NumPy-only protocol can be rejected by Torch. No new public factory parameter or runtime syntax is introduced.

## Outcomes & Retrospective


Implementation pending. Native Tree and CuPy static models remain independent work. Like return types describe original convertible values; callers must explicitly convert before using backend-only methods. Do not suppress such meaningful errors in old fixtures.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/static-like-inputs`, branch `codex/static-like-inputs`, base `3eac024`. `src/bearshape/numpy.py` defines the public ArrayLike template and all NumPy static aliases. `jax.py` and `torch.py` define their TYPE_CHECKING aliases. `tests/typing/check_conformance.py` and `tests/typing_negative/` are checked by the four-engine harness in `tests/test_typecheck.py`. Add separate Like consumer files to those fixture directories and focused runtime controls under each backend's existing test file.

## Plan of Work


Create positive calls using already-typed float64/int32 arrays, numeric scalars, tuples, lists and nested lists. Include NumPy Shaped inputs with string/object/datetime/structured dtypes and useful backend result inference. Add intended errors for nonnumeric strings, dictionaries and incompatible numeric kinds where the backend's static dtype information supports rejection. Save the initial four-checker failures.

Change only TYPE_CHECKING alias definitions for NumPy Like families: bool inputs remain boolean, unsigned integer inputs admit booleans/unsigned integers, signed integer inputs admit booleans/integers, real inputs admit booleans/integers/floats, and complex inputs admit all numeric kinds. Destination precision and actual casting remain runtime checks. Shaped permits every NumPy generic dtype. Use private reusable aliases only where they remove repeated real family definitions.

For JAX/Torch, include native arrays, NumPy numeric arrays/scalars and numeric nested sequences in their Like aliases. Preserve meaningful scalar numeric families where feasible, while native backend dtype is not statically parameterized. Check the nested-sequence model across all four engines before promotion. Correct existing fixtures that use backend-only methods on unconverted Like inputs by converting explicitly. Add runtime controls for newly statically accepted typical calls and update concise static/Like docs.

## Concrete Steps


From this worktree:

    uv sync --locked
    uv run --locked pytest tests/test_typecheck.py -n 4
    uv run --locked pytest tests/test_numpy.py tests/test_jax.py tests/test_torch.py -n 4
    uv run --locked tox run -e dev
    uv run --locked prek run -a

Save initial failures before alias changes. Repeat all four checker batches with interpreter-matched Python 3.10–3.14 environments and the maintained floor checker lanes. Later integration combines the corrected runtime converter and exact beartype rc0 dependency.

## Validation and Acceptance


All four checkers accept the documented ordinary input families through already-typed variables, preserve strict-array result types after explicit conversion, and reject designated invalid inputs for the intended reason. Existing public syntax remains accepted. Runtime controls prove the newly accepted examples, while docs clearly identify runtime-only shape/casting/device constraints. Hooks and the full existing runtime suite pass. No whole-input object/Any alias or broad new checker suppression is an acceptable shortcut.

## Idempotence and Recovery


Keep source changes isolated from the runtime-conversion branch until integration. Negative fixtures must never execute as Python programs. Keep before/after checker evidence. Require user validation before merge and do not widen Tree/CuPy claims in this PR.

## Artifacts and Notes


Use `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/static-like-*.log` for initial failures and final checks. Record the actual supported family boundary and any backend-stub limitation discovered during implementation.

## Interfaces and Dependencies


Retain the public NumPy ArrayLike template and named strict/Like aliases. Use existing NumPy typing helpers and typing_extensions.TypeAliasType for Python 3.10 syntax compatibility. Add no runtime dependency or root import. Keep backend-specific static input aliases private.

Revision note — 2026-09-08: Added focused Like/Shaped typing plan before implementation.
