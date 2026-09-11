# Reduce the cost of locating the active checking frame


This living ExecPlan follows `PLANS.md` and continues the existing production-readiness goal. Keep Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective current.

## Purpose / Big Picture


Array validation repeatedly searches for the beartype frame that owns shared dimension bindings. The search currently materializes every visited frame's local-variable mapping, including unrelated library frames. Rejecting impossible candidates using their code metadata first should reduce this cost while preserving exactly which frame owns the memo. This also reduces the cost of the proposed upstream union transactions, which introduce additional call frames.

The owner requested substantially lower overhead before contacting the upstream maintainer. This change is independent of the proposed integration and therefore has its own branch, worktree and PR. It keeps the published beartype 0.23.0rc0 dependency and all public behavior unchanged. No merge, release, transfer or maintainer contact is authorized for this new change.

## Progress


- [x] (2026-09-08) Profiled the initial upstream proposal: frame discovery is a material part of repeated checks.
- [x] (2026-09-08) Created `codex/memo-discovery-performance` and `/Users/ale/Code/bearshape-worktrees/memo-discovery-performance` from main `795ec391123437beb5167de1e1519411dbabe479`.
- [x] (2026-09-08) Opened draft PR #35 before implementation.
- [x] (2026-09-08) Added the candidate filter and regression proving unrelated frames do not materialize locals. Existing real decorated/DOOR behavior remains covered.
- [x] (2026-09-08) Targeted tests passed; full CPU runtime tests passed 1,094 with five existing skips; all eight four-checker harness cases passed; hooks passed.
- [x] (2026-09-08) Matched installed comparisons show the rc0 strict-check baseline improving by about 13% on 3.10 and 27% on 3.14. Combined upstream effects are recorded separately.
- [ ] Present the focused change for review; merge remains pending user validation.

## Surprises & Discoveries


The first transaction prototype magnified existing frame-search work: both its snapshot getter and the ordinary validator independently locate the checking scope. Profiling 10,000 strict calls showed 420,000 candidate-frame inspections. This is evidence about the initial prototype, not a portable latency claim.

## Decision Log


Decision: Change only candidate rejection in frame discovery, and keep scope parsing, Value expression handling, frame ownership and the transaction protocol out of this PR. Rationale: the filter is independently useful and can be assessed without changing library behavior or coupling release decisions. Date/author: 2026-09-08, Codex.

## Outcomes & Retrospective


The focused filter passes existing real-frame behavior, lifetime, CPU and static consumer tests, plus a regression that forbids reading unrelated-frame locals. Matched measurements and normally installed combination tests have passed; both PRs remain unmerged for review. No new cache or lifetime mechanism was introduced.

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


## Final evidence


Implementation commit `344d390c4099685cc3ea6519f5bb8b5bde0fb13e` is isolated in
draft PR #35. Local integration commit
`c53d14f99d71fd4884282642b98e8bd63bd7b871` combines it with PR #34 solely for
validation. Main and both PR branches were not merged together.

On published beartype rc0, the strict parameter/return baseline changed from
19.546 to 16.955 microseconds on Python 3.10.20 and from 18.262 to 13.358 on
3.14.5: approximately 13% and 27% lower total latency. Each value is the median
of 14 samples of 20,000 calls, across two process runs in reversed scenario
order. This is a host measurement with no timing gate or portable guarantee.
The optimized adapter's proposed hook is ignored by rc0 on both sides, so the
measured runtime change is the frame filter.

The independent branch passed 1,094 CPU runtime tests, all eight four-checker
harness cases and hooks, with five existing CPU skip records. The combined
normally installed artifacts passed 1,125 tests from sdist-extracted consumers
outside the source checkout on each Python endpoint, including the 22 upstream
integration cases. Minimal environments passed with no optional backends.
No new CUDA coverage is claimed.

Detailed measurements, commands, hashes and final hosted CI states are retained
under `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/union-transactions/optimization/`.
The combined wheel SHA256 is
`a0cb17c0b4a67b49f6e6cc10ee76e0f911ad9441877e994cdd6f495366325851`.
The source archive SHA256 is
`ac4cf3b1b87c700fece1fbdb35f5b7503b90b199606e4367b4dbdb2193a5c2f0`.
Merge approval remains pending for this independent change.

Revision note — 2026-09-08: Added matched baseline timings and installed
combination evidence, keeping this change separate from upstream integration
and release acceptance.
