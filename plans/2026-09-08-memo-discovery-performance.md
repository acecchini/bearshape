# Reduce the cost of locating the active checking frame


This living ExecPlan follows `PLANS.md` and continues the existing production-readiness goal. Keep Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective current.

## Purpose / Big Picture


Array validation repeatedly searches for the beartype frame that owns shared dimension bindings. The search currently materializes every visited frame's local-variable mapping, including unrelated library frames. Rejecting impossible candidates using their code metadata first should reduce this cost while preserving exactly which frame owns the memo. This also reduces the cost of the proposed upstream union transactions, which introduce additional call frames.

The owner requested substantially lower overhead before contacting the upstream maintainer. This change is independent of the proposed integration and therefore has its own branch, worktree and PR. It keeps the published beartype 0.23.0rc0 dependency and all public behavior unchanged. No merge, release, transfer or maintainer contact is authorized for this new change.

## Progress


- [x] (2026-09-08) Profiled the initial upstream proposal: frame discovery is a material part of repeated checks.
- [x] (2026-09-08) Created `codex/memo-discovery-performance` and `/Users/ale/Code/bearshape-worktrees/memo-discovery-performance` from main `795ec391123437beb5167de1e1519411dbabe479`.
- [ ] Open a draft PR before implementation.
- [ ] Filter impossible frame candidates before reading frame locals; add focused evidence for decorated functions, DOOR checkers and unrelated frames.
- [ ] Run memo/lifetime/decorator regressions, CPU runtime tests, all four static consumer checkers and hooks with the locked toolchain.
- [ ] Benchmark identical inputs with and without this change, using both rc0 and the local upstream proposal. Record the two effects separately.
- [ ] Present the focused change for review; merge remains pending user validation.

## Surprises & Discoveries


The first transaction prototype magnified existing frame-search work: both its snapshot getter and the ordinary validator independently locate the checking scope. Profiling 10,000 strict calls showed 420,000 candidate-frame inspections. This is evidence about the initial prototype, not a portable latency claim.

## Decision Log


Decision: Change only candidate rejection in frame discovery, and keep scope parsing, Value expression handling, frame ownership and the transaction protocol out of this PR. Rationale: the filter is independently useful and can be assessed without changing library behavior or coupling release decisions. Date/author: 2026-09-08, Codex.

## Outcomes & Retrospective


Implementation and validation are pending. The acceptance criterion is the same memo owner and lifetime with lower measured frame-search cost, not a new caching scheme.

## Context and Orientation


`src/bearshape/_memo.py` finds the live decorated call or DOOR checker frame. `_is_beartype_wrapper_frame` currently reads `frame.f_locals` before determining whether the code can be such a wrapper. Beartype function wrappers declare `__beartype_func`, `args` and `kwargs`; DOOR checker names begin with `__beartype_checker_` and expose pith locals. `get_memo` stores the memo in the live frame, while explicit scopes use context variables. Preserve these paths and their priority.

`tests/test_memo.py` and `tests/test_decorator.py` cover scope, nested calls, cancellation and lifetime. Do not replace live frame ownership with a global cache, scan bytecode for union decisions, or cache argument objects. Python code-variable names are a cheap candidate filter; the existing live values remain the final validity check.

## Plan of Work


First open the draft PR with this plan. Then inspect the wrapper code metadata before accessing local values. Reject code that declares neither the decorated-function marker nor a DOOR checker name. Preserve all existing checks for candidates. Add a focused regression that checks both real checking surfaces and confirms ordinary helper frames are rejected without reading their local mappings. Use a minimal frame stand-in only for proving the latter property, alongside existing real-frame behavioral coverage.

Finally run targeted tests, the full CPU runtime suite, all four checker consumers and hooks. Build a normal wheel for matched benchmarks and combined integration validation outside this worktree. Keep timing assertions out of CI because wall-clock noise is unsuitable for a unit-test gate.

## Concrete Steps


From this worktree, initialize and validate with:

    uv sync --locked
    uv run --locked prek install
    uv run --locked pytest tests/test_memo.py tests/test_decorator.py -q
    uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
    uv run --locked pytest tests/test_typecheck.py -q
    uv run --locked prek run -a

Benchmark artifacts and comparisons belong under `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/union-transactions/optimization/`. Record source commits, interpreter and package versions, commands and result distributions. Preserve the initial proposal artifacts rather than overwriting them.

## Validation and Acceptance


Normal decorated functions, standalone DOOR checks, explicit scopes, nested calls, async calls and failures keep their original memo ownership. Existing weak-reference tests continue to prove objects are released. Frame rejection avoids local mapping access for impossible candidates, without rejecting real beartype wrappers. Runtime, static consumer and hook checks pass. Matched benchmarks show the cost separately from changes in the upstream transaction machinery.

## Idempotence and Recovery


Use the isolated worktree and locked environment. Keep main unchanged. Record changes in normal commits and preserve clean unmerged work for review. No backend is imported by root import as a result of this change. Earlier CPU/GPU results do not automatically validate newly built artifacts.

## Artifacts and Notes


This is a dependent investigation within the union optimization work, but the code change applies independently to the published rc0 baseline. Exact validation and performance results will be added as measured.

## Interfaces and Dependencies


No new dependencies or API. `_is_beartype_wrapper_frame(frame: types.FrameType) -> bool` keeps its signature and final recognition rules. The optional fast rejection uses code metadata only; it does not infer validation outcomes or union boundaries.

Revision note — 2026-09-08: Created the plan before implementation to isolate the independent frame-search improvement.
