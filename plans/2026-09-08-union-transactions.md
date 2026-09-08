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
- [x] (2026-09-08) Profiled and reduced the local proposal overhead before maintainer contact, preserving rollback, diagnostics, lazy aliases, sampling and state lifetime.
- [x] (2026-09-08) Validated optimized normal installations and archive consumers on both endpoints, recorded matched comparisons, and prepared a local Zulip draft without sending it.
- [x] (2026-09-08) Reproduced and fixed copied-context state retention and stale parent registration; repeated affected installed tests and matched benchmarks against final upstream head.
- [ ] Upstream acceptance/publication and a later supported dependency migration remain external steps, not a completed release fix.

## Surprises & Discoveries


The exact published beartype 0.23.0rc0 and the previously inspected upstream development commit `a2729e0e358bf963ee6f177e300ae08a622d05d6` both use ordinary boolean expressions for union alternatives. A successful bearshape leaf can bind a name before a following plain `str` check fails. The leaf receives no notification of that failure. Existing leaf snapshot/restore is necessary but insufficient.

Creating the new worktree succeeded, but its post-checkout hook could not find `prek` before that worktree's environment existed. Initialize the environment with locked uv and install hooks normally; do not bypass validation.

## Decision Log


Decision: Implement and test the smallest upstream source extension needed if no existing public rc0 interface can expose the required boundary. Rationale: the owner explicitly selected supported integration; a local source patch is a reviewable step toward that outcome, while runtime patching installed beartype internals would violate the contract. Date/author: 2026-09-08, Codex.

Decision: Keep the published dependency baseline and normal lock unchanged during prototyping. Rationale: an unpublished local extension is not a released supported API. A later version floor can change only when a concrete compatible dependency is normally available. Date/author: 2026-09-08, Codex.

Decision: Prepare any upstream proposal locally before seeking permission to submit it. Rationale: the request authorizes implementing a fix but not sending messages to external maintainers. Earlier merge approval covered earlier reviewed work; this new feature remains reviewable in its own draft PR. Date/author: 2026-09-08, Codex.

## Outcomes & Retrospective


The optimized local proposal retains the rollback contract and reduces added strict-check overhead by 57% on Python 3.10 and 74% on Python 3.14. It uses the smaller state-object adapter and an upstream checker compiled once at decoration. Draft PR #35 isolates the independent frame filter. Normally installed combined artifacts passed 1,125 tests on each endpoint, including all four checkers and 22 integration cases, with five existing CPU skip records. Upstream's final source passed 434/447 unit tests, including 22 protocol tests with 600 independent-reference cases and two copied-context regressions, and pyright. Remaining nested ordinary-reference overhead is disclosed below. No upstream contact, merge into main, publication or transfer occurred. Upstream acceptance, publication and coordinated dependency adoption remain release prerequisites.

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


## Performance follow-up authorized by the owner


The owner requested a deeper investigation and substantially lower overhead before contacting the beartype maintainer. The owner has a direct Zulip contact; prepare discussion material locally, but do not send it or submit upstream. Continue the existing draft PR and matching worktrees because this refines the same unmerged integration. Preserve the initial committed patch and immutable wheel evidence for comparison.

Profile the initial normally installed proposal against published rc0 before editing. Extend measurement to successful first and later union alternatives, rejection, nested unions, explicit scopes, multiple domains and stateless forward references. Time setup separately from repeated checking; compare equal interpreters, packages and inputs. A faster incorrect rc0 result is not a correctness equivalent.

First replace avoidable per-call bookkeeping if profiling confirms it is material. Consider a direct path for a single known state provider without internal union boundaries, compact callback storage, and avoiding repeated state lookup. Keep the public callback interface small; any interface change must be justified by measured improvement and equivalent semantics. Do not make unselected references eager, drop exception cleanup, weaken negative tests or remove runtime composition. Record rejected approaches as well as measured improvements.

Then validate focused regressions and upstream tests, followed by normal installed packages on Python 3.10 and 3.14, CPU backends, four checkers, archive/minimal consumers, hooks and docs as affected. Add behavioral regressions for newly discovered risks. Preserve the original package artifacts and record optimized hashes separately under evidence/union-transactions/optimization/. Report both total latency and the change in added overhead, including remaining costs. Do not impose unstable wall-clock CI thresholds.

Decision: Optimize this tested local proposal before any upstream contact. Rationale: the current extra cost is material for a runtime checker; a smaller design with measurements will make the owner's maintainer discussion more useful. The user's Zulip contact does not authorize sending a message. Date/author: 2026-09-08, Codex.

Revision note — 2026-09-08: Reopened the local optimization milestone at the owner's request; existing completed evidence remains historical baseline, not proof of the next revision.


## Optimization design and current evidence


The current proposal supersedes the original `__beartype_snapshot__` callback
with `__beartype_state__()`, returning a library-owned object with `snapshot()`
and `restore(token)` methods. A token is an opaque saved-state value. Bearshape
now exposes its existing `get_memo` function directly; no new memo wrapper or
per-snapshot closure is needed. Locate known state once per checking expression
and reuse it across alternatives. Validate newly discovered domains before use.

The upstream generator compiles one checking function at decoration. It retains
one scope for assignment expressions and receives the original sampled random
integer. Compact restore/token lists replace per-checkpoint ExitStacks; general
unwinding is retained on the exceptional path when a restore method fails. A
root union uses its alternatives' complete boundaries without another duplicate
checkpoint. Leading stateless native alternatives are checked once before state
setup. Root forward references delegate to the resolved hint, while nested lazy
references still enrol domains in active checks before mutation.

The original prototype's published-rc0 compatibility status has not changed.
The initial patch and artifacts remain historical evidence. No upstream message
has been sent. The independent frame filter lives in draft PR #35, branch
`codex/memo-discovery-performance`; validate its combination on a separate local
integration branch before any merge approval. It filters code metadata before
reading unrelated frame locals and introduces no state cache.

Initial profiling attributed a material part of the cost to repeated frame
inspection. A bookkeeping-only prototype reduced a 54-microsecond corrected
second-alternative case to about 45; reusing state then reduced it to about 39.
These are exploratory measurements, not the final matched artifact comparison.
The maintained `tools/upstream/benchmark_transactions.py` reports incorrect rc0
cases explicitly and covers native checks, resolved/unselected references,
synthetic plugin checks, automatic/explicit array checks and nested/rejected
unions. Final comparisons must use the same script and package versions.

Discovery: compiling a fresh helper for a root forward reference changed the
upstream uncached-expression equality contract. Delegating such roots directly
to the existing resolver both preserved that contract and removed unnecessary
transaction setup for ordinary references. The upstream tests remain intact.
A transient missing import and an unsupported pytest override were corrected;
final validation uses the project's supported options and explicit Python
interpreter/version arguments for pyright.

Decision: Prefer a state object over per-snapshot callbacks. Rationale: this
reuses the library's existing snapshot/restore interface, avoids repeated scope
lookups and closure creation, and keeps state ownership with the library.
Decision: Preserve complete boundaries but eliminate redundant checkpoints and
stateless setup. Rationale: equivalent outcomes can be proved by regressions
without weakening composition or exception cleanup. Date/author: 2026-09-08, Codex.

Revision note — 2026-09-08: Recorded the optimized interface, rejected redundant
work, independent PR #35 and the distinction between exploratory and final
performance evidence.


## Optimized delivery and final comparison


The final upstream head is `76e27706fb137c6a676ee7b79a66d8b3092b52ad`, against
`a2729e0e358bf963ee6f177e300ae08a622d05d6`. The independent frame filter is
`344d390c4099685cc3ea6519f5bb8b5bde0fb13e`. Local validation commit
`c53d14f99d71fd4884282642b98e8bd63bd7b871` combines both bearshape changes.
Its normally installed wheel and sdist are recorded under
`evidence/union-transactions/optimization/` outside these worktrees. The
benchmark script at `46e7f4d657b5272cc0be8543848e794fefb45f41` adds a
measurement-only nested-reference case after that package build; package code
and runtime tests are unchanged. The PR branches remain independent.

Matched medians pool 14 samples per correct case: 20,000 calls per sample, seven
repeats in each of two process runs, reversing scenario order in the second run.
Python 3.10.20 uses NumPy 2.2.6; Python 3.14.5 uses NumPy 2.4.6. Both use
optree 0.19.1 and typing_extensions 4.15.0. Runtime imports and decoration are
not timed. The manifest preserves exact commands, script hash and versions.

For strict parameter/return checks, original bearshape with rc0 measured
18.442/17.736 microseconds on 3.10/3.14, and the first working proposal measured
30.451/30.240. Optimized bearshape with rc0 measured 16.384/13.208, and the
final working combination measured 21.589/16.418. Thus added transaction
overhead fell from 12.009/12.504 to 5.206/3.209 microseconds, a 57%/74% reduction
after accounting separately for the frame filter. The filter alone improves the
rc0 strict baseline by about 11%/26% in this repeat.

Correct second-alternative calls fell from 51.499/52.596 to 32.908/25.489
microseconds. Explicit-scope fallback calls fell from 39.986/45.178 to
21.048/15.042, and nested union calls from 25.569/23.746 to 14.717/11.752.
An unselected ordinary reference remains close to the rc0 baseline. Nested ordinary
references still add about 0.74/0.42 microseconds over rc0, approximately
2.0x/1.9x their small baseline; this remains a maintainer discussion point.
Ordinary root references retain a smaller hook lookup cost. No zero-overhead
or portable latency guarantee is claimed.

The final archive consumers, with no source directory available, passed 1,125
tests on each endpoint. There were four unavailable platform precision cases
and one skipped CuPy module; this provides no new CUDA evidence. Minimal
normal installations passed with no optional backends. Distribution integrity,
hooks and documentation passed. Upstream passed 434 tests with 20 existing
skips on 3.10 and 447 with seven on 3.14; pyright checked 477 source files with
zero errors and warnings for each interpreter target. Its 22 protocol tests
include 600 deterministic comparisons of nested acceptance and final bindings
against an independent reference.

The combined bearshape wheel SHA256 is
`a0cb17c0b4a67b49f6e6cc10ee76e0f911ad9441877e994cdd6f495366325851`; the sdist is
`ac4cf3b1b87c700fece1fbdb35f5b7503b90b199606e4367b4dbdb2193a5c2f0`. The optimized
beartype wheel is
`0db860846b16c6fbb61f0b494dd0b30065cbd683d063356a3dbf5ae928da6d20`; its sdist is
`8bacac19c91d0150943a6c9be90149302d4f2b6849add2b97d972005ee3954dc`.

`OPTIMIZATION.md` contains the full report, `RESULTS.json` the source/artifact
record, `benchmark-summary.json` the samples, and `benchmark-manifest.json` the
commands, all under the optimization evidence directory. `ZULIP-DRAFT.md` is
prepared for the owner; it has not been sent. Normal hosted CI still uses rc0
and does not prove this unpublished upstream integration. Final PR-head CI
results are recorded in the external results file when available.

Revision note — 2026-09-08: Closed the requested local optimization milestone
with matched measurements, immutable artifacts and expanded correctness proof;
kept upstream acceptance and release adoption explicitly outstanding.


## Final copied-context correction


The lifetime review found that `copy_context()` could retain an invocation's
state after its transaction completed. A later root forward-reference check
could then mistake the completed transaction for a live parent and omit root
rollback. Two focused regressions failed before the fix, preserved in
`copied-context-before.log`. Completed transactions now clear their getters and
state objects, and new checks ignore parents whose transaction token has closed.
Both regressions pass. All 22 upstream protocol cases also pass against the
normally installed wheel outside the upstream source checkout on both endpoints.

The final source, artifact hashes, 1,125 consumer results per endpoint and matched
benchmarks above include this correction. The earlier optimization evidence is
preserved under `optimization/before-context-lifetime/`, including the first
matched comparison cited by PR #35. No earlier artifact evidence was discarded.

Revision note — 2026-09-08: Added failing copied-context lifetime evidence,
corrected cleanup, repeated affected installed validation and refreshed the
matched timing matrix against the final upstream patch.
