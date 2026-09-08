# Scope validation state to the check that owns it


Maintain this living ExecPlan according to `PLANS.md`. This PR implements the validation-lifetime portion of the accepted production goal and records the separate composite-union feasibility result.

## Purpose / Big Picture


A failed manual check must not poison the next independent check or retain its array. A single decorated call must still share dimensions across arguments and returns and provide accurate errors. Current cached validator objects carry mutable ReplayFailureState between calls. Investigate storing call state in its live invocation rather than on shared annotation instances.

## Progress


- [x] (2026-09-08) Read current memo, replay, array, tree, decorator and upstream error paths.
- [x] (2026-09-08) Opened PR #15 and reproduced eight failures in nine new regression cases.
- [x] (2026-09-08) External prototype passed existing runtime tests on exact rc0 at Python 3.10/3.14.
- [x] (2026-09-08) Demonstrated that frame lifetime does not fix native union rollback; no branch transaction callback is exposed by the inspected rc0 union generator. A04 remains a release gate.
- [x] (2026-09-08) Implemented live-frame memo ownership and removed global/cached replay state; runtime, checker, coverage and hook validation passed.
- [ ] Record unresolved contract gates and obtain user validation before merge.

## Surprises & Discoveries


ReplayFailureState is cached per annotation and strongly references a failed object after boolean-only composite checks. The memo uses a thread-local stack with frame tokens and bytecode positions to approximate invocation lifetime. The live frame already has stable identity through an injected local token, suggesting direct frame ownership may remove stale global state. This is a hypothesis until endpoint and diagnostic tests pass.

## Decision Log


Decision: Prototype state attached to the active check frame before adopting a replacement. Rationale: avoid global references to user objects, bytecode-position bookkeeping, or guessed replay counters. Preserve explicit check_context sharing and nested call independence. Date: 2026-09-08.

Decision: Native composite unions require a separate feasibility result. Rationale: a successful leaf can bind N before another leaf rejects its enclosing branch, and beartype owns the union's control flow. Do not pretend leaf rollback fixes whole-alternative rollback.

## Outcomes & Retrospective


A03 is fixed locally. All 1,043 runtime tests pass on baseline and both exact-rc0 endpoints; all 30 current typing tests pass. The required dev tox environment passed 1,073 tests with five expected skip records and 91.31% combined coverage. Nine new lifetime cases pass, including object release and mutation. Hooks passed. A04 remains open: frame ownership provides invocation lifetime but cannot observe a native union alternative failing after a successful leaf.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/validation-lifetime`, branch `codex/validation-lifetime`, base `f43e00d`. `_memo.py` stores ShapeMemo dimension/structure bindings and explicit context stacks. `_runtime_hints.py::ReplayFailureState` stores cached failures. `_ArrayChecker`, `_ArrayLikeChecker`, and `_TreeChecker` snapshot bindings around their checks. `_decorator.py` brackets explicit calls and coroutine execution. Feature tests include tests/test_memo.py, test_decorator.py, test_numpy.py, and test_tree.py.

## Plan of Work


First reproduce: two float32 vectors with lengths two and three fail `is_bearable((a,b), tuple[F32[N],F32[N]])`, after which the independent `is_bearable(b,F32[N])` must succeed. Repeat for Like and tree hints where their contracts bind the same dimension. Add weak-reference tests that discard user and traceback references, collect garbage, and require the failed array to be released without a later validation. Add valid/failing decorated and DOOR diagnostics so disabling validation cannot pass.

In an external prototype, replace automatic memo bookkeeping with state owned by the live check frame and disable cached failure replay. Run existing runtime tests in-process so prototype monkeypatches actually apply. Verify parameter/return, tree, explicit-context, nested-call and coroutine error paths at Python 3.10 and 3.14 with rc0. Promote only a design preserving accurate violations; if diagnostic traversal creates a distinct checker invocation, identify a reliable lifetime boundary before implementation. Do not hold a frame globally or rely on generated instruction offsets.

For union feasibility reproduce `tuple[F32[N],I32[N]] | tuple[F32[C],F32[C]]` followed by an F32[N] argument. Two length-two float arrays in the pair and a length-three final array should pass through the second alternative. Inspect rc0's native union generation and public hooks for whole-alternative transactions. Record a minimal demonstrated blocker if upstream offers no usable boundary; keep independent work moving and present a concrete contract/upstream choice before claiming A04 resolved.

After a successful prototype, replace obsolete replay/global-stack code with the smallest private design, update behavior-based tests, remove tests specific only to retired bookkeeping, and update CHANGELOG. Preserve root optional imports and the documented intentional sharing of inherited explicit contexts.

## Concrete Steps


Run targeted and full tests in the feature worktree with uv-managed environments:

    uv sync --locked
    uv run --locked pytest -n 0 tests/test_memo.py tests/test_decorator.py tests/test_tree.py
    uv run --locked pytest -n auto tests --ignore=tests/test_typecheck.py
    uv run --locked pytest -n auto tests/test_typecheck.py
    uv run --locked prek run -a

Use existing isolated rc0 Python 3.10/3.14 environments with this worktree's source path for candidate validation. Before/after prototype logs live in the external implementation evidence directory. Record exact commands and outcomes below.

## Validation and Acceptance


Independent checks of the reused object succeed after composite failure, arrays are released after their invocation ends, and valid checks remain valid while wrong dtype/shape/returns still reject with useful details. Explicit contexts, nested calls, threads, async cleanup/cancellation, and supported tree checks preserve their contract on rc0 at both endpoints. A union prototype must roll back the entire failed alternative; otherwise A04 remains an explicit release blocker. No permanent xfail or disabled check counts as a fix.

## Idempotence and Recovery


Keep prototypes outside source until their promotion gate passes. Never patch installed beartype or mutate the main checkout. Revert an unsuccessful experiment in this worktree without resetting unrelated work. Preserve minimal failing probes and evidence even if their architecture is discarded.

## Artifacts and Notes


Evidence directory: `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/`. Store prototype commands, missing-boundary evidence, baseline failures and final passing logs. Record any public API decision explicitly before implementing it.

## Interfaces and Dependencies


Keep public check/check_context and array/tree syntax unchanged. Runtime dependencies remain beartype and typing_extensions. Per-call state must not live on cached hint definitions. Diagnostic replay must belong to the current invocation; future calls cannot be mistaken for replay.

Revision note — 2026-09-08: Added the lifetime and union feasibility plan before experimentation.

## Composite union feasibility result


The inspected exact-rc0 generator `beartype/_check/code/_pep/pep484/codepep484604union.py` expands union alternatives into native boolean expressions. Its corresponding snippets in `_data/check/code/pep/datacodepep484604.py` provide no callback entering, committing, or rolling back an entire alternative. The public instance-check and diagnostic hooks see leaves. For `tuple[F32[N], str] | tuple[F32[C], int]`, the first alternative can bind N and then fail at the plain str test without calling another bearshape validator. Resetting N at the next leaf would also erase legitimate earlier-argument bindings in other annotations.

The external prototype independently confirms the original audit example still rejects a valid length-three final argument after a length-two successful C alternative. A03 is therefore independently fixable; A04 needs an upstream composition boundary or a deliberately accepted/enforced alternative API/contract. No upstream code was modified, no unsupported workaround was added, and no failing union test was hidden as a passing regression. This remains a production-release blocker for the promised general native-composition semantics.

Validation evidence — 2026-09-08: `lifetime-before.log` records eight failures and one existing-success control; `lifetime-after.log` records 187 targeted passes; runtime endpoint logs each record 1,043 passes/five expected skips. `lifetime-checkers.log`: 30 passed. `lifetime-coverage.log`: 1,073 passed/five skips, 91.31% coverage. `lifetime-mutation.log`: nine passes using supported ndarray.resize on NumPy 2.5. `lifetime-hooks.log`: passed. Source shrank by removing ReplayFailureState and thread-local frame bookkeeping.
