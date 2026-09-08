# Roll back failed native union alternatives


This is a living ExecPlan governed by `PLANS.md`. Keep Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective current. It continues the existing production-readiness goal rather than starting a duplicate goal.

## Purpose / Big Picture


A valid call must not fail because a rejected union alternative left dimension or tree-structure bindings behind. For `tuple[F32[N], str] | tuple[F32[C], int]`, a length-two float array paired with an integer selects the second alternative. A later `F32[N]` argument of length three must succeed: the rejected first alternative must not retain N=2. Successful alternatives must still bind dimensions, and wrong shapes, dtypes, ordinary values and return values must still fail.

The user requested resolving this defect after approving the earlier implementation merge and choosing full native composition through a supported beartype integration. Preserve native annotations and beartype's checking and sampling policy. No monkeypatch, bytecode inference, replacement checker, weakened composition contract, or hidden expected failure is acceptable.

## Progress


- [x] (2026-09-08) Read the current agent contract, roadmap, prior feasibility evidence, bearshape memo/checker implementation and beartype union generator.
- [x] (2026-09-08) Created branch `codex/union-transactions` and matching worktree at `/Users/ale/Code/bearshape-worktrees/union-transactions` from main `795ec391123437beb5167de1e1519411dbabe479`.
- [x] (2026-09-08) Committed the plan and opened draft PR #34 before implementation.
- [x] (2026-09-08) Initial regressions reproduced 12 failures and two passes on published rc0 before implementation; expanded the suite to 22 behavioral cases.
- [x] (2026-09-08) Implemented the snapshot protocol in isolated upstream commit `4aef992d1cd0a6d09fe5c3784523c44e0874b178`, based on `a2729e0e358bf963ee6f177e300ae08a622d05d6`. No upstream message, fork push or PR submitted.
- [x] (2026-09-08) Connected the shared runtime-hint metaclass to existing memo snapshots. All 22 integration cases pass, including late aliases, sampling, cancellation and thread isolation.
- [x] (2026-09-08) Normally installed packages passed 1,124 tests plus five existing CPU skip records on each of Python 3.10.20 and 3.14.5, including all four checkers. Upstream serial unit tests passed 426/439 with 20/7 pre-existing skips. Upstream pyright passed.
- [x] (2026-09-08) Hooks and docs passed. Final sdist-extracted consumers outside the checkout passed 1,124 tests with five existing CPU skip records on each endpoint. Minimal wheel environments passed with no optional backends. Final normal-install benchmarks and artifact hashes are recorded below.
- [x] (2026-09-08) Prepared the concrete upstream patch and submission text locally and updated the handoff and agent/tool guidance.
- [ ] Obtain authorization to submit the upstream proposal; acceptance/publication and a later supported dependency migration remain external steps, not a completed release fix.

## Surprises & Discoveries


The exact published beartype 0.23.0rc0 and the previously inspected upstream development commit `a2729e0e358bf963ee6f177e300ae08a622d05d6` both use ordinary boolean expressions for union alternatives. A successful bearshape leaf can bind a name before a following plain `str` check fails. The leaf receives no notification of that failure. Existing leaf snapshot/restore is necessary but insufficient.

Creating the new worktree succeeded, but its post-checkout hook could not find `prek` before that worktree's environment existed. Initialize the environment with locked uv and install hooks normally; do not bypass validation.

## Decision Log


Decision: Implement and test the smallest upstream source extension needed if no existing public rc0 interface can expose the required boundary. Rationale: the owner explicitly selected supported integration; a local source patch is a reviewable step toward that outcome, while runtime patching installed beartype internals would violate the contract. Date/author: 2026-09-08, Codex.

Decision: Keep the published dependency baseline and normal lock unchanged during prototyping. Rationale: an unpublished local extension is not a released supported API. A later version floor can change only when a concrete compatible dependency is normally available. Date/author: 2026-09-08, Codex.

Decision: Prepare any upstream proposal locally before seeking permission to submit it. Rationale: the request authorizes implementing a fix but not sending messages to external maintainers. Earlier merge approval covered earlier reviewed work; this new feature remains reviewable in its own draft PR. Date/author: 2026-09-08, Codex.

## Outcomes & Retrospective


A working local fix now passes the original example and all 22 expanded integration cases on both Python endpoints. The small bearshape adapter uses a proposed upstream snapshot hook; the source extension owns branch boundaries, exception cleanup, diagnostic replay and lazy-reference registration. Published rc0 still fails because it does not implement this hook. Final archives, normal-install consumers, minimal environments, hooks and docs have been validated. Upstream submission approval, acceptance/publication and dependency migration remain outstanding. PR #34 is intentionally a draft, and no new feature merge or publication was performed.

## Context and Orientation


`src/bearshape/_memo.py` owns ShapeMemo, the dictionaries binding single dimensions, variadic dimensions and tree structures. It supports snapshot and restore. Automatic memo ownership is the live beartype checking frame; `check_context` and `check` also support explicit scopes. `_runtime_hints.py` creates hint classes with metaclass instance checking. `_array_types.py` and `_tree.py` restore state when their individual checks fail and isolate diagnostic callbacks. `_decorator.py` manages explicit synchronous and asynchronous call scopes. `tools/probe_union.py` is the unresolved integration reproducer.

The inspected public upstream clone is `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/beartype-upstream-review`. Create a separate branch/worktree for changes rather than changing this recorded checkout. Upstream `beartype/_check/code/_pep/pep484/codepep484604union.py` builds the union expression. `beartype/_check/code/codemain.py` visits the annotation tree and substitutes child expressions. Diagnostic traversal is under `beartype/_check/error/`. Its public plugin documentation and tests are the appropriate place to describe and prove any new opt-in state integration, without depending on bearshape or NumPy in upstream tests.

A transaction here means taking snapshots of participating validator state, evaluating an entire alternative, retaining state only on success, and restoring it on rejection or an exception. Nested transactions must restore only their own additions. Diagnostics must report failures without permanently modifying live checking state.

## Plan of Work


### Milestone 1: Failing behavioral evidence


Commit this plan and open a bearshape draft PR. Add regression cases for plain-type rejection after a successful shape check, alternative order, earlier bindings, nested alternatives, all alternatives failing, return checking, and explicit scopes. Run against the unmodified locked candidate and preserve failures outside temporary worktrees. Keep incomplete upstream-dependent cases visibly separate until they can run as required checks against an available dependency; do not mark them xfail.

### Milestone 2: Upstream integration prototype


Design a narrowly scoped opt-in protocol on stateful runtime hints. Generate transaction boundaries only when participating hints require them; ordinary stateless annotation code should retain its existing path. Use beartype's own type traversal and checking expressions, and preserve short-circuit order and sampling. Cover exceptions with actual `try/finally` behavior rather than only boolean suffixes. Integrate diagnostic traversal so a failed check cannot poison later checks or alter its own explanation. Test with a tiny upstream-only stateful hint and inspect generated code for scope and evaluation-count regressions. Record the concrete API and modifications here once proven.

### Milestone 3: Bearshape integration and reviewable delivery


Expose the new opt-in callback from bearshape runtime hints using existing memo snapshots. Normally install the patched upstream and bearshape into isolated environments. Run the expanded regression suite, existing lifetime/weak-reference tests, CPU backend tests, all four static consumer checkers, and relevant package consumers on Python 3.10 and 3.14. Preserve the known failing published-rc0 baseline and successful patched-version evidence separately. Update CHANGELOG, relevant agent instructions, the runtime contract and handoff report to describe precise availability. Prepare the upstream patch with its test results and a concise proposed PR description for approval.

## Concrete Steps


From `/Users/ale/Code/bearshape-worktrees/union-transactions`:

    uv sync --locked
    uv run --locked prek install
    uv run --locked python tools/probe_union.py

The initial probe should fail with `dimension 'N' expected 2 but got 3`. After a complete integration fix, the same call must succeed unchanged.

Run focused tests first, then the existing routes when changes warrant them:

    uv run --locked pytest tests/test_memo.py tests/test_decorator.py -q
    uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto
    uv run --locked pytest tests/test_typecheck.py -q
    uv run --locked prek run -a

Do not use `uv run --locked` to silently replace a patched dependency installation during its integration tests. Use a separate environment with explicit normal installs and invoke that environment's interpreter directly. Document the exact commands and source commits once established.

## Validation and Acceptance


The original valid call succeeds. Rejected alternatives discard single, variadic and tree-structure bindings. Selected alternatives retain bindings used by later arguments and returns. Bindings from earlier arguments survive rollback. Nested unions and containers work with repeated objects and repeated calls. Explicit and automatic contexts, async calls, cancellation and thrown validator exceptions leave no leaked state. Negative checks still raise useful beartype violations rather than desynchronization errors. Upstream ordinary annotations keep their prior behavior and do not pay runtime transaction costs when no participating stateful hints occur.

A passing local prototype is not enough to claim published rc0 compatibility. Completion must state whether the needed upstream API exists in a released artifact. If upstream acceptance/publication is pending, deliver the concrete tested patch and bearshape integration while leaving that release gate open.

## Idempotence and Recovery


Use isolated worktrees and virtual environments. Do not edit shared installed dependency files, published artifacts, main, or existing evidence. Keep logs and patch artifacts under `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/union-transactions/`. Preserve worktrees while review or upstream acceptance is outstanding. Do not publish releases, deploy Pages, transfer ownership, modify account settings or contact upstream maintainers without explicit authorization.

## Artifacts and Notes


Baseline main is `795ec391123437beb5167de1e1519411dbabe479`. Prior upstream baseline is `a2729e0e358bf963ee6f177e300ae08a622d05d6`, reporting development version 0.23.0rc1. Exact source identities, regression outputs, generated-code evidence and patch files will be recorded here as milestones finish.

## Interfaces and Dependencies


No new third-party runtime dependencies. Use existing ShapeMemo snapshot/restore and upstream public plugin conventions. The proposed upstream protocol must remain optional, avoid imports of bearshape/backends, deduplicate shared state providers, clean up on all outcomes and avoid retaining caller objects after checks end. Its final callable signatures, discovery rules, diagnostic behavior and supported scope must be specified before promotion from prototype.

Revision note — 2026-09-08: Created the focused plan before implementing the union rollback fix.

## Implementation discoveries and concrete interface


The optional upstream hook is `__beartype_snapshot__() -> Callable[[], None]`. All bearshape hint classes expose the same static getter object, so their shared state is snapshotted once per boundary. The getter returns a closure holding the active ShapeMemo and a copy of its three binding maps. It imports no optional backend and no upstream private API. Existing leaf rollback remains for published rc0 and bare Python instance checking.

Upstream collects getter identities during its existing sanitized code-generation traversal. Union alternatives receive deferred start/commit/rollback expression boundaries only when a descendant opts into state or could resolve lazily. One closure around the complete expression preserves the lexical scope of generated assignment expressions; a separate closure per alternative would lose variables shared by the generator's sampling logic. ExitStack unwinds failed branches and exceptions, including a broken plugin rollback. Diagnostic traversal uses the same getter set, retains successful sibling bindings while describing a failure, and restores all diagnostic changes afterward.

Late aliases required additional evidence. The first prototype passed 14 cases but failed an alias defined after decoration. Lazy references now enrol a newly discovered getter in active transactions before validation mutates state. The generator retains beartype's existing preference for concrete classes before unresolved proxies, so `Optional["NotYetDefined"]` still accepts None. No unused reference is resolved eagerly. Transactions use ContextVar tracking and invocation-owned snapshots, not a global binding cache.

Upstream tests exposed dedicated NoReturn and legacy tuple diagnostic paths outside the ordinary expression generator. These retain their original special handling. A parallel run also hit an existing shared bytecode-cache cleanup race; the upstream project's suite passes serially without modifying or skipping that fixture. Test-only dynamic classes require distinct qualified names because upstream caches some hint representations.

The first benchmark observed a cost for stateful hints (strict small-array call about 20 to 31 microseconds), while a native NumPy-only annotation remained about 0.11 microseconds. This is a correctness-versus-overhead tradeoff for the upstream proposal; final matched normal-install measurements are pending. No portable performance guarantee is made.

The local patch file is `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/union-transactions/beartype-stateful-hints.patch`. Apply it to a clean checkout of the recorded upstream base with `git apply --check` followed by `git apply`; normal-install both packages into an isolated interpreter as documented in `tools/upstream/README.md`. The patch must be accepted and published upstream before dependency metadata, lock and required CI are migrated. Do not turn this local result into a released-rc0 compatibility claim.

Revision note — 2026-09-08: Recorded the working callback design, successful endpoint suites, upstream patch commit, discovered alias/diagnostic paths and remaining artifact/review steps.

## Final local evidence


The final 22-case suite passes serially on Python 3.10.20 and 3.14.5. With published rc0, the suite records 20 failures and two passes; the hook alone does not change that dependency's behavior. Initial archive validation exposed a pre-existing upstream cache collision between dynamically recreated `Is` validators sharing a qualified name. The ValueError and cancellation fixtures now use distinct module-level functions, so they reliably exercise both exception classes in one process. Runtime code did not change during this fixture correction.

Normally installed immutable wheels, with tests and configuration extracted from the final bearshape source archive into `consumer-final310` and `consumer-final314` outside the checkout, passed 1,124 tests and five existing CPU skip records on each interpreter. These commands include `--installed-package`, all four checker consumers, and the explicitly named upstream integration suite. The five skips are CuPy and four unavailable macOS dtype-precision cases. The earlier broad suites also checked the bearshape source. New GPU evidence is deferred until candidate validation after the upstream dependency is available; old GPU artifacts do not validate this changed wheel.

The built bearshape wheel is byte-identical before and after the fixture-only correction. SHA256 identities:

    bearshape-0.1.0rc0-py3-none-any.whl
      0393873fa2bf0e55cfa9b26fe718ad19759bbd314a5150a5bde1e21640d7b163
    bearshape-0.1.0rc0.tar.gz
      70624c97463c090c91e162e9332cf2af09339c9e63a348d485f5b72122e9f95c
    beartype-0.23.0rc1-py3-none-any.whl
      18b7179c8d45828f20b909e733b0999ac50906c0d064c57150c39efafc6819e5
    beartype-0.23.0rc1.tar.gz
      5904fbe8883b703269e202bc7ec1db0b23d8e857bbc2b7b251af8b4974b223a3
    beartype-stateful-hints.patch
      7784b95c8f338190ecf1b83e4a65ee3104c5c16d663c97077e67c27bc5621f2e

All files are under the evidence root given above, in `bearshape-dist-final`, `beartype-dist`, and the top-level patch file. `distribution-check-final.json` verifies wheel/source consistency. `installed-final310.log` and `installed-final314.log` contain the archive-consumer results. `minimal310.log` and `minimal314.log` prove the optional-import boundary. `upstream-pyright-final.json` reports 477 analyzed source files with zero errors or warnings. `upstream-serial310.log` and `upstream-serial314.log` contain the complete upstream suite results; the final callback typing and context-token cleanup also passed its focused protocol tests.

Matched normal-install benchmarks used the same Python 3.10.20, NumPy 2.2.6, optree 0.19.1 and bearshape wheel, changing only rc0 versus the patched beartype wheel. Each ordinary case ran 10,000 calls per repeat for five repeats. Median strict small-array calls changed from 18.974 to 31.272 microseconds, Like from 9.817 to 15.711, one-leaf Tree from 30.866 to 42.871, and diagnostics from 115.403 to 142.045 (diagnostics use the tool's 1,000-call cap). Native-only annotations remained below 0.2 microseconds in both runs; their generated expression has no transaction operations. These are host-specific observations. The roughly 12-microsecond strict-call cost is an explicit review tradeoff, not hidden behind correctness results.

Hosted rc0 CI run 34239118985 passed for implementation head `983f7dc0983378662acd0b22924c09489389db87`. That does not test the unpublished upstream extension. The final fixture/report follow-up will receive its own normal CI run; local patched-wheel evidence is tracked independently.

Revision note — 2026-09-08: Recorded final installed-archive verification, fixture correction, hashes, minimal imports, performance tradeoff and the remaining upstream approval/release boundary.
