# Make bearshape ready for a verified beartype 0.23.0rc0 release


This ExecPlan was accepted for implementation on 8 September 2026. The target release is bearshape `0.1.0rc0`, independently versioned from beartype. It follows the repository's `PLANS.md`. Keep `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` current during execution. The user authorized implementation, isolated worktrees, and separate focused PRs for independent changes. Merge still requires user validation; publication and administrative transfer require separate authorization.

The audited checkout is `/Users/ale/Code/bearshape`, at `f43e00d2fe1714ae87d9f736f2a35692713ed0d4` on `main`. The maintained copy is `plans/2026-09-08-production-readiness.md` on `codex/rc0-roadmap`. Each feature PR carries a smaller self-contained ExecPlan and its own validation results. The audit remains evidence, not the specification for every implementation detail; all essential findings and acceptance criteria are included below.

## Purpose / Big Picture


bearshape should give numerical Python developers reliable runtime relationships between array shapes and dtypes while preserving useful backend types in editors and static analysis. Its principal users are NumPy, JAX, PyTorch, and CuPy developers, and library authors who expose typed numerical APIs to other people. Existing beartype users should be able to adopt it through ordinary decoration or package instrumentation without learning a second general-purpose checking framework.

After this work, a user must be able to install the built distribution with exactly beartype `0.23.0rc0`, catch inconsistent input and output dimensions, perform independent checks without stale state, and use supported annotations in real calls accepted by supported static checkers. A failed speculative validation must not contaminate a later successful one. An annotation advertising backend convertibility must reflect that backend's actual conversion rules. Maintainers must be able to reproduce these properties from the release artifacts and a documented test matrix.

Keep the product focused. Shape equality, arithmetic dimensions, broadcasting, and tree-structure relationships remain runtime contracts. Static checking preserves backend identity, dtype information where the backend exposes it, accepted input families, and function signatures. Do not promise static shape arithmetic, add another shape syntax, build a replacement for beartype, or introduce speculative features to justify a redesign.

The recommended release policy is to make `0.23.0rc0` the minimum beartype version, with a proposed dependency range `>=0.23.0rc0,<0.24` and an exact `==0.23.0rc0` required test lane. The accepted implementation plan raises the beartype floor to rc0; 0.20–0.22 compatibility lanes will be retired. Preserve the existing ordinary annotation syntax and decorator modes. Targeted changes to previously incorrect conversion or typing behavior are proposed where the contract cannot otherwise be made honest; describe their migration impact before accepting them.

## Progress


- [x] (2026-09-08) Completed the production audit and preserved its evidence outside the repository.
- [x] (2026-09-08) Prepared this implementation proposal without changing the repository.
- [x] (2026-09-08) M0: Accepted independent `0.1.0rc0` versioning, active goal, and focused branches/worktrees/PRs #12–#30.
- [x] (2026-09-08) M1: PR #13 makes exact rc0 normally installable; locked suite and exact-candidate CPU endpoint suites pass. Subsequent PRs preserve failing-before regressions.
- [ ] M2: Import-hook repair is implemented in PR #14. Native composite-alternative rollback is not feasible through the inspected rc0 leaf callbacks; the owner selected supported upstream integration with a later candidate allowed. Full composition remains required.
- [ ] M3: Invocation-owned state and diagnostic replay removal are implemented in PR #15 (1,043 runtime tests on exact rc0 endpoints; 91.31% dev coverage). Whole-alternative rollback remains a release blocker.
- [x] (2026-09-08) M4: PR #16 fixes seven converter false positives; thirteen oracle cases and 1,047 runtime tests pass on exact rc0 endpoints. CuPy GPU proof is now supplied by PR #26 and the exact hosted artifact runs under M6.
- [x] M5: PR #17 implements four-engine positive/negative/inference conformance on Python 3.10–3.14. PR #19 corrects Like/Shaped inputs and PR #20 replaces nominal Tree stubs; all four checkers pass real positive/negative/inference fixtures on Python 3.10–3.14. The owner accepted explicitly limited native CuPy static support alongside verified GPU runtime.
- [x] (2026-09-08) M6: #21 proves framework/minimal behavior; #26 passes 95 real CUDA tests at both endpoints, including the exact hosted artifact. #29 supplies 17 feature/test families, four default/wrapped-signature cases at both endpoints, and matched performance/profile evidence with no material regression.
- [x] (2026-09-08) M7: #23 implements locked reusable validation across nine platform runtime lanes, five four-checker lanes and twelve compatibility factors, strict preflight/required gates, CPU resolution and aligned hooks. All hosted checks pass; #30 updates the artifact/Pages actions to Node 24 and passes the final validation-only run.
- [x] (2026-09-08) M8: #18/#25 prove distribution contents and normal installs. The hosted release artifact passes 1,097 installed-consumer tests per endpoint (one absent-CuPy skip). #24 fixes Markdown rendering and executes all 29 notebook code cells at both endpoints; #29 adds the rendered handoff report.
- [ ] M9: #28 gates immutable workflow/tag/package identity, validates the complete candidate and reuses its exact artifacts. Actual validation-only run 34221337124 completed 38 jobs successfully and skipped publication. #29 prepares the full handoff/admin proposal. Remaining: supported native-union integration and administrative controls. The approved history is integrated in main through PR #31.

## Surprises & Discoveries


The existing suite is substantial but does not establish the advertised contract. On Python 3.10.20 with beartype 0.22.9 it reported 1,064 passed and five skip records. Runtime-only runs with exact rc0 on Python 3.10.20 and 3.14.5 each reported 1,034 passed and five skip records, while independent probes reproduced four runtime defect families. The candidate tests used isolated environments or an overlay; they did not prove that current package metadata permits installation. It does not.

The import-hook wrapper changes the immediate caller frame that upstream uses to discover the package. A mocked forwarding test passes while an actual package is left unchecked. Cached validators also hold mutable replay state after boolean-only failures, including a strong reference to a failed array. Successful leaf checks in failed union alternatives bind dimensions beyond the alternative's lifetime. These are separate failures; fixing the dependency bound does not fix them.

Checker success can hide information loss. Locked ty 0.0.40 accepts the current fixtures while reducing tested aliases to Unknown and missing deliberately wrong inputs. The audit's ty 0.0.79 probe restores the tested useful information. All tested checkers reject ordinary calls through the current nominal Tree representation. An upstream helper with a promising name is not proof of a usable static tree model: optree's dynamic runtime type construction also requires real consumer testing.

The repository layout is already reasonable: about 5,114 source lines across 16 implementation/public modules plus the package initializer. Combined coverage was 91.04%, with 89.39% branch coverage. CuPy had no local runtime coverage. The five skip records include an unavailable entire CuPy test module and four platform-specific extended-precision cases.

Build and workflow success also hid release defects. LICENSE is absent from both archives. The publication workflow builds an arbitrary selected ref without a test gate. The audited GitHub response reported main unprotected; organization rulesets, environment approval rules, and PyPI publisher configuration were not inspected. Documentation built successfully with malformed rendered tables and admonitions. CPU Torch compatibility jobs installed CUDA-related dependencies despite the root project's CPU index configuration.

Implementation discovery (2026-09-08): a failed native union alternative can bind a dimension in a bearshape leaf and then fail in an ordinary `str` check. rc0's generated boolean union expression has no bearshape-visible whole-alternative entry/exit boundary. Frame-owned memo state fixes independent-call leakage and diagnostic object retention, but does not solve this separate compositional failure. No bytecode heuristic, upstream monkeypatch, hidden expected failure, or reduced contract was introduced. The owner now selected supported upstream integration, permitting a later candidate and retaining full composition.

## Decision Log

Decision (2026-09-08, owner): “First option. Merge approved.” Preserve full
native union composition through supported upstream integration, allowing a
later beartype candidate; accept explicit limited CuPy native static support.
This supersedes prior pending-choice statements. Exact rc0 remains the current
validation baseline until a concrete replacement passes the integration matrix.
The owner also requested shared agent-file and tool guidance updates. Merge
approval persists for that scope; publication, settings changes, ownership
transfer and upstream communications remain separately authorized operations.



Decision: Preserve the package boundaries and primary product direction. Rationale: the defects concern contracts, integration, and validation; the audit found no justification for a broad file-layout rewrite. Date/author: 2026-09-08, Codex proposal.

Decision: Recommend rc0 as the beartype floor and test that exact candidate explicitly. Rationale: one supported integration generation reduces private-integration complexity before organizational maintenance begins. Status: accepted with implementation authorization. If older releases must remain supported, retain their matrix lanes and prove every semantic fix there; do not silently lower acceptance. Date/author: 2026-09-08, Codex proposal.

Decision: Preserve named dimensions, existing backend imports, ordinary bracket syntax, the distinction between strict and Like aliases, and both existing check decorator modes. Rationale: these are useful product surface. Incorrect accepts or rejects may need targeted correction, with an explicit migration note. Status: accepted; any newly discovered public API redesign still requires a concrete decision. Date/author: 2026-09-08, Codex proposal.

Decision: Put a bounded architecture feasibility milestone before a large memo rewrite. Rationale: beartype evaluates native union branches; leaf validators cannot assume they receive branch entry and exit notifications. A successful prototype must demonstrate the needed boundary on unmodified rc0. Date/author: 2026-09-08, Codex proposal.

Decision: Treat checker support as positive calls, expected rejection, and useful inferred types. Rationale: accepted declarations alone passed the existing tests while hiding practical incompatibilities. Proposed tested versions begin with pyright 1.1.411, mypy 2.3.1, ty 0.0.79, and pyrefly 1.2.0, with existing pyright/mypy floor lanes retained where they satisfy the stronger suite. These are observed starting points, not claims that every earlier version fails or every later version works. Date/author: 2026-09-08, Codex proposal.

Decision: Use separate feature branches, matching worktrees, and early draft PRs for independent changes. Rationale: the user explicitly requested independent review units on 2026-09-08. Keep prerequisites visible for dependent PRs, and validate the combined result in an integration worktree before release. Maintain this roadmap on its own PR; user merge validation was granted on 2026-09-08. Date/author: 2026-09-08, user decision.

Decision: Separate code readiness, publication, and administrative transfer. Rationale: a green PR is not authorization to publish a package or change ownership/access. Prepare concrete review material first and perform those external actions only with the corresponding authorization. Date/author: 2026-09-08, Codex proposal.

## Outcomes & Retrospective


Implementation outcome: sixteen focused implementation/evidence PRs and separate roadmap/validation aggregates preserve independent review. Normal exact-rc0 installation, caller-sensitive claw behavior, invocation lifetime, selected backend conversion, four-checker consumers, Like and Tree static inputs, framework/GPU behavior, locked CI, rendered/executed docs, archives and publication gates are implemented and validated. The owner approved merging the reviewed work on 2026-09-08; PR #31 integrated every reviewed head into main at df81f00e2f62bda956244e680c980f87db1d4671, with all 36 main CI jobs passing. PR #33 corrects defects found by installing and exercising the actual Git hooks. The exact hosted wheel passes CPU/checker consumers and real CUDA tests; the release dry run never enters publication. Native whole-alternative union rollback remains incorrect because rc0 exposes no reliable whole-alternative boundary, and CuPy native typing lacks adequate upstream stubs. The open union integration and administrative protections prevent a production-ready verdict. Do not trade them for green test counts.

## Context and Orientation


The `src/bearshape/` package separates public backend modules from shared validation. `numpy.py`, `jax.py`, `torch.py`, and `cupy.py` expose array and Like aliases. NumPy intentionally has the widest surface, including scalar-like types and structured dtype factories. `optree.py` and JAX's Tree surface expose tree checking. Root `__init__.py` exports dimensions and shared tools and must not import optional numerical backends.

`_dimensions.py` represents dimension expressions. `_shape.py` parses and checks shape specifications. `_dtypes.py` normalizes and compares dtypes. `_array_types.py` implements array validators and conversion checks. `_tree.py` validates leaves and tree structure. `_runtime_hints.py` supplies common validation/failure helpers including `ReplayFailureState`. `_memo.py` discovers and manages the dimension memo: a mutable record of dimension names and tree structures already bound during a check. `_decorator.py` provides explicit memo management and optional combined beartype decoration. `claw.py` exposes package instrumentation.

A transaction here means recording bindings before a speculative check, committing them if that check succeeds, and restoring them if it fails. A branch is one alternative of a union such as `A | B`. The transaction must encompass the entire alternative, not just a failing leaf. A validation invocation is one decorated call, including its parameter and return checks, one independent DOOR check, or an explicitly shared manual context; diagnostic rechecking of that invocation may need its original state, while a later independent call must start independently. Explicit `check_context()` intentionally shares bindings across manual checks inside its block. Its currently documented child-task sharing behavior must not be changed implicitly.

Tests mostly live in feature files such as `tests/test_memo.py`, `test_numpy.py`, `test_tree.py`, and `test_decorator.py`. `tests/test_typecheck.py` runs the checker fixtures in `tests/typing/`. `tests/conftest.py` selects backend tests using environment factors and filenames. `pyproject.toml` owns package metadata, dependency groups, and several checker settings; `uv.lock` owns normal development resolution. `tox.toml` and `tools/validate_tox_env.py` define and validate compatibility environments. `.pre-commit-config.yaml` uses prek-specific builtins and priorities despite its conventional filename. `.github/workflows/` contains CI, compatibility, docs, and publication workflows. `zensical.toml` builds `docs/`.

Use the repository's two-space Python indentation. Do not move these modules merely for symmetry. Introduce a shared helper only when it removes repeated real logic, and keep integration-specific assumptions in one small private location.

## Plan of Work


### M0 — Set the release contract and execution boundary


Implementation is now authorized. Record the accepted beartype floor and targeted correction policy here. Create separate feature branches and worktrees under `/Users/ale/Code/bearshape-worktrees/`; the first are `codex/rc0-roadmap` and `codex/rc0-compat`. Recheck the base commit and uncommitted work first; if main has moved, review the delta from the audited SHA rather than discarding it. Commit the initial maintained plan, open an early draft PR, and start an implementation goal explicitly tied to the accepted plan.

Add a concise supported-behavior statement to the maintained plan before code changes. Plain beartype decoration, package instrumentation, DOOR checks, and explicit check contexts are required integration surfaces. Keep bare `@check` as memo management and `@check(conf=...)` as combined checking. Generator and async-generator functions remain explicitly unsupported by `check`; ordinary functions and coroutines remain supported. Root imports remain independent of NumPy, JAX, Torch, CuPy, and optree. Static shape equality is not promised.

Acceptance is a reviewable draft PR containing the plan and a recorded compatibility policy, with no unspecified general API redesign. Administrative transfer and actual package publication remain outside automatic execution.

### M1 — Establish exact-rc0 installation and failing contract tests


Address A01 in `pyproject.toml`, `uv.lock`, `tox.toml`, and `tools/validate_tox_env.py`. Under the proposed policy use `beartype>=0.23.0rc0,<0.24`; exact-rc0 tox environments must install `beartype==0.23.0rc0`. Do not rely on prerelease selection by a loose resolver, a source overlay, `PYTHONPATH`, or `--no-deps` to prove compatibility. Keep runtime dependencies limited to beartype and typing_extensions unless a concrete fix demonstrates a necessary additional dependency.

Introduce explicit `py310-bt023rc0-cpu` and `py314-bt023rc0-cpu` environments first. The `cpu` factor means all four CPU-testable components: NumPy, JAX, Torch, and optree. Resolve backend versions appropriate to each interpreter; a Python 3.14 job cannot install a dependency floor with no 3.14 wheel. Log exact imported versions and paths, and fail if an expected backend is absent. The audit proved runtime execution with NumPy 2.2.6/JAX 0.6.2/Torch 2.12.0/optree 0.19.1 on 3.10 and NumPy 2.5.3/JAX 0.11.1/Torch 2.14.0/optree 0.20.0 on 3.14. Use these as reproducibility references, not universal cross-Python pins.

Promote the audit's minimal failures into repository tests before correcting behavior. Put actual package-instrumentation tests in a focused new `tests/test_claw.py`; state lifetime and branch rollback belong in `tests/test_memo.py`, with array/tree variants in their existing feature files. Add Like failures to `tests/test_torch.py` and `tests/test_jax.py`. The failing assertions must describe desired user behavior, not internal implementation choices. Temporary expected failures may be used on the draft branch only if strict, explained, and removed before claiming the finding closed.

Acceptance: ordinary resolver installation with exact rc0 succeeds, the existing runtime baseline remains green in the two endpoint environments, and the newly promoted tests reproduce A02–A05 on the audited implementation. Save both initial failure and eventual passing evidence. Do not lower existing coverage thresholds or erase unrelated failures to establish this baseline.

### M2 — Prove integration feasibility and fix caller-package instrumentation


Address A02 first with the smallest supported change in `src/bearshape/claw.py`: directly re-export upstream `beartype_this_package` as `bearshape_this_package`, preserving the caller frame and public import name. If actual rc0 behavior prevents that solution, use a correctly targeted public upstream hook with an explicit package target and prove its discovery; do not add a second implicit stack-search system. Remove the forwarding mock as the primary proof, retaining it only if it still tests distinct behavior.

The integration test must create and import real temporary packages in isolated subprocesses so beartype's global import-hook registration cannot contaminate other tests. In a subsequently imported submodule, valid inputs must pass, inconsistent `F32[N]` parameters must raise `BeartypeCallHintParamViolation`, and an inconsistent annotated return must raise the corresponding return violation. Exercise supplied configuration, both an unrelated sibling package and a nested submodule, and the documented import order.

Run a bounded feasibility investigation for A03 and A04 before committing to a new state architecture. Read the installed rc0 code generation and error-reporting paths. Relevant upstream locations in the audited wheel include `beartype/_check/code/_pep/pep484/codepep484604union.py`, `beartype/_check/error/_pep/errpep484604.py`, and `beartype/_check/error/_nonpep/errnonpeptype.py`. These are research references, not permission to monkeypatch upstream internals. Find a stable way to identify logical check lifetime, diagnostic replay, and entry/exit of an entire speculative union alternative.

Prototype only these boundaries in small focused experiments, retaining a prototype in production only after it meets the acceptance contract. It must handle ordinary `@beartype`, `@check(conf=...)`, boolean `is_bearable`, raising `die_if_unbearable`, and real claw instrumentation on exact rc0 at both Python endpoints. A wrapper-only prototype does not establish the plain-beartype contract. A leaf-only snapshot does not establish branch rollback. Arbitrary replay counts, bytecode offsets, tracing the entire process, or matching a particular generated local-variable spelling are not adequate foundations.

The promotion gate is explicit: demonstrate that failed alternatives undo all their bindings, successful alternatives keep theirs, and diagnostics cannot be mistaken for subsequent independent calls. Test nested composites and permutations with a uniquely valid branch. Where more than one branch succeeds but implies different bindings, record the exact supported selection semantics; do not promise function-wide backtracking or textual union order that upstream does not guarantee.

If unmodified rc0 cannot provide a reliable solution within the required integration surfaces, record a blocking design result with the minimal failing example and evidence. Continue independent work, but do not declare M3 or release readiness complete. Prepare a concrete choice for the user and receiving maintainers: an upstream-supported integration change and revised beartype target, or a deliberately reduced/enforced composition contract with migration consequences. A documentation warning alone does not repair silent wrong behavior, and adopting either alternative requires explicit acceptance. Stop this investigation after demonstrating the missing boundary rather than building a replacement type checker.

### M3 — Make state lifetime, diagnostics, and rollback correct


Implement the design proven in M2 in `_memo.py`, `_runtime_hints.py`, `_array_types.py`, `_tree.py`, and `_decorator.py` as needed. Keep cached annotation definitions immutable with respect to per-call validation results. `ReplayFailureState` must no longer retain a failed user object globally until a future unrelated call happens to clear it. Any retained diagnostic information must have a defined owner and termination path. Do not fix retention by losing the useful original expected/actual dimension message.

A transaction must restore dimensions and tree-structure bindings together when the enclosing supported operation fails. Preserve successful bindings across parameters and into return validation. Independent nested decorated calls must not overwrite their caller's bindings; an explicit `check_context()` must continue sharing deliberately. Restore state in exceptions and coroutine cancellation. Honor the existing explicit-context child-task contract or present any proposed change separately; task-local storage by itself does not make shared mutable values isolated.

The minimum observable regression is that a failed `tuple[F32[N], F32[N]]` check on vectors of lengths two and three is followed by a successful independent `F32[N]` check on the same length-three object. Repeat with boolean-only checks, formatted exceptions, a changed shape on the same object where supported, recursion, and interleaved threads. Use separate explicit contexts for the promised isolated async-task scenario. A weak-reference test must show that after the failing invocation and user references end, garbage collection releases the array without another validation being required. Release exception/traceback references in that test before attributing retention to bearshape.

The union regression uses `tuple[F32[N], I32[N]] | tuple[F32[C], F32[C]]` followed by an `F32[N]` parameter. Two float32 length-two arrays in the pair and a float32 length-three final parameter must pass because only the second alternative succeeds. A genuinely inconsistent input must still fail. Cover nested tuple/union and supported tree-leaf variants; verify diagnostics do not introduce new bindings or change the result. Maintain useful argument/return locations and expected-versus-observed details in messages without freezing all upstream formatting in snapshots.

Acceptance: promoted A03/A04 regressions pass on exact rc0 in every required integration surface, lifetime tests release their objects, and existing dimension/shape/tree/decorator tests remain correct. An unsupported M2 boundary remains an open release blocker, never a silent fallback.

### M4 — Make Like mean conversion the target backend can perform


Address A05 in `_array_types.py` and each backend module. Define Like acceptance in terms of the documented converter, its supported input families, the existing casting policy, and the resulting shape/dtype. Validation may perform a conversion to inspect the result, but it must not replace the function's original argument. Same-kind casting is not a promise of lossless conversion; preserve that distinction. A mutable or stateful foreign object can change after checking, so describe convertibility at validation time.

Remove the generic NumPy fallback when it turns a failed target-backend conversion into acceptance. Narrow trusted fast paths to cases demonstrated equivalent to the target converter; belonging to `np.ndarray` alone is insufficient for Torch or JAX. Keep strict array checks based on backend identity and metadata without conversion. Preserve existing factory parameters unless a targeted API change is proven necessary and accepted. Catch real conversion failures narrowly enough to retain actionable information; do not mask bugs in shape/dtype logic with broad fallback handling.

Use the backend converter as the test oracle. Torch Like must reject a negative-stride NumPy array or non-native-endian array if the documented Torch conversion rejects it. Torch and JAX ShapedLike must reject NumPy string arrays that their converters reject. A NumPy-only `__array__` object must not become Torch-convertible by an undocumented fallback. Also test valid lists, scalars, native arrays, empty inputs, non-contiguous supported views, booleans, complex values, structured dtypes, and invalid protocol implementations where relevant to each backend's existing surface.

Check rank and dimension binding after conversion, consistent cast-policy decisions, and rollback when conversion or subsequent validation fails. For native Torch tensors, validation must not silently detach gradients or mutate device/dtype; strict JAX checks must not transfer arrays to the host. GPU/device-specific conversion claims remain subject to M6's GPU gate. Document unavoidable allocation costs for Like checks.

Acceptance: every positive conversion fixture has a successful target-converter counterpart under the stated policy, every negative counterexample rejects, valid existing inputs remain accepted unless a documented defect correction deliberately narrows them, and the downstream typing model in M5 describes those same input families.

### M5 — Prove useful typing at real consumer call sites


Address A06 in the backend `TYPE_CHECKING` branches, `_decorator.py`, checker configuration, `tests/typing/`, and `tests/test_typecheck.py`. Keep ordinary NumPy strict aliases informative about dtype and backend. JAX and Torch should preserve native Array/Tensor methods and return types to the degree provided by their upstream stubs. Do not invent static shape guarantees by attaching dimension parameters that checkers ignore.

First extend the fixture harness with three kinds of proof: accepted consumer calls, deliberately rejected calls, and exact or bounded inferred-type assertions. Keep current valid fixtures in `tests/typing/`; add invalid fixtures under `tests/typing_negative/` so normal source checking does not fail on intentional errors. Group related fixtures and invoke each checker once per relevant group where possible, rather than launching the same checker afresh for every file. Parse its supported diagnostic output and match the intended location/category; do not count any nonzero process exit as a successful negative test. A crash, missing import, or wrong interpreter is a test failure.

Use real variables from normal backend construction, not only declarations or contextually typed literals. Check `F32[N]` rejects an integer-dtype array and a string, that a valid `np.ndarray` consumer retains native array methods, and that decorated functions retain parameter names, arity, return type, and coroutine behavior. Include controls using direct backend types so a backend-stub limitation can be distinguished from bearshape information loss. Scope existing broad Unknown/Any and missing-import suppressions as narrowly as practical; the public conformance fixtures must not pass merely because the library disappears into Any or Unknown.

Fix the `check` overload's omitted/None configuration mismatch while preserving `Callable[P, R]` behavior through ParamSpec. Establish a tested checker baseline beginning with pyright 1.1.411, mypy 2.3.1, ty 0.0.79, and pyrefly 1.2.0. Retain pyright 1.1.408/1.1.409 and mypy 1.19.1 compatibility lanes if they pass the strengthened contract. Raise the documented ty floor to a version actually proven useful. Integrate pyrefly as supported only after the complete fixture contract passes. Do not add zuban in this program.

Prototype Tree typing before replacing the current fake nominal class. `Tree[int]` must accept ordinary integer leaves and documented nested containers supplied through already-typed variables. Test lists, tuples, dictionaries, mixed nesting, invalid leaves, and the existing custom-node runtime surface. Account for mutable-container variance: a recursively defined alias that only accepts a freshly contextualized literal is insufficient. Do not replace Tree with Any, or assume that a general Sequence alias is correct when it also admits strings that are runtime leaves. Do not assume an upstream dynamic PyTree factory is checker-compatible without running the same tests.

Promote the smallest model that works across the supported checkers. If arbitrary registered custom nodes cannot be represented faithfully, retain their runtime support and define a documented explicit static escape using the user's own node type together with separately expressed runtime checking. If this requires a new public form or a meaningful narrowing of the documented Tree contract, record and obtain acceptance before adopting it. This gate is satisfied by an honest tested support boundary, not by claiming every runtime tree is statically representable.

Align Like inputs with conversion rather than the target dtype alone: NumPy F32Like under same-kind casting must not statically reject every float64 array that runtime accepts. Preserve useful distinctions between numeric input families; do not broaden all inputs to object. JAX/Torch Like must accept their documented scalar/list input families where runtime does. NumPy Shaped must reflect its actual broad dtype surface, including tested nonnumeric dtypes. CuPy typing needs both an absent-backend import-boundary check and a real installed-CuPy consumer fixture; a minimal shape/dtype protocol is not proof that native CuPy methods survive.

Acceptance: all four selected checkers pass the valid and inference suite, reject the designated invalid examples for the intended reasons, and behave consistently at every advertised Python target. Run the same consumer suite against the installed wheel outside the checkout in M8. Advanced fixed-literal/arithmetic/broadcast/Value syntax must either have a demonstrated checker-safe spelling or be explicitly documented as runtime-only; declaration acceptance alone does not establish support.

### M6 — Close feature and framework validation gaps before optimization


Build a concise feature-to-test map covering existing named, anonymous, fixed, arithmetic, and broadcast dimensions; Scalar and Value; dtype families, byte order, structured fields, datetime/timedelta; strict and Like arrays; explicit and automatic memo contexts; and tree leaf/structure binding. Use the current feature tests first. Add cases where a public promise lacks proof, especially negative examples and interactions exposed by M3/M4; do not reorganize all tests or duplicate them merely to increase counts.

Verify annotation evaluation and decoration on the Python 3.10 and 3.14 endpoints, including postponed annotations, forward references, wrapped functions, methods, return checks, defaults, and coroutines. Keep unsupported generator behavior explicit. For Value expressions, preserve the current allowed expression operations and lexical lookup behavior; test rejected operations and missing names without widening the evaluator. Avoid introducing evaluation of arbitrary Python strings.

Exercise a small representative JAX jit/vmap/grad workload and a Torch autograd/compile workload using the documented decorator order and real numerical output. Define whether validation occurs on each Python call or during tracing/compilation; do not promise checks on every compiled invocation unless tests demonstrate that. Use small CPU examples. Platform or compiler limitations may justify a documented integration boundary, but a skipped example cannot support a claim that the transformation works.

Validate root import in a clean environment containing only declared runtime dependencies, then validate each backend with its own dependencies installed. Installing one backend must not make another optional backend mandatory. Test the custom strict-array factory without NumPy. Import-path isolation and source-tree absence are essential to this proof.

CuPy requires a real CUDA-capable runner for runtime signoff. Run strict dtype/shape, Like conversion, device behavior, and tree integration where advertised, logging GPU, CUDA, CuPy, and Python versions. If no suitable runner exists, retain the API but label its runtime verification status precisely and withhold an equal production-support claim. Do not broaden the release statement based on CPU skips. Whether to delay the release or approve an explicitly limited CuPy support statement is a release decision.

Measure performance after correctness. Reproduce a small benchmark comparing bare beartype backend checks, strict bearshape checks, explicit context decoration, and Like checks, using matched interpreter/hardware and tiny versus large arrays. The audit observed roughly 20.4 microseconds for a representative strict input/return call and about 14 microseconds with explicit decoration; these are observations, not universal thresholds. Profile scope/signature discovery only if it remains a material cost. Cache or avoid repeated work when lifetime correctness permits it; do not add a caching framework or trade semantic correctness for a headline speedup. Record medians and spread, and investigate material regressions rather than imposing a noisy wall-clock CI assertion.

Acceptance: each maintained feature has positive and negative evidence, representative framework behavior is accurately documented, optional boundaries hold, and the performance report distinguishes metadata-only checks from conversion and tree traversal costs.

### M7 — Make dependencies, hooks, tox, and CI enforce the same contract


Address A10 using `pyproject.toml`, `uv.lock`, `tox.toml`, `tools/validate_tox_env.py`, `tests/conftest.py`, `.pre-commit-config.yaml`, and the CI/compatibility workflows. Keep normal jobs locked and interpreter-matched. A deliberate latest-dependency canary may resolve newer versions separately and report its resolved set, but it must not silently change the required release baseline. Update the environment-name validator whenever factors change, and verify both valid names and actual installable version pairs.

Retain targeted backend-floor environments: NumPy 2.2, JAX 0.5, Torch 2.6, and optree 0.14 on interpreters where they install. Add exact-rc0 current-backend CPU coverage on Python 3.10 through 3.14. Proposed required PR coverage includes Linux endpoint CPU suites, all advertised Python typing targets, supported dependency floors, hooks, docs build, and artifact checks. Main/release validation adds the intermediate Python runtime environments and macOS/Windows endpoint core/NumPy/optree runs. Run additional JAX/Torch platform lanes where supported wheels exist and the project advertises those combinations; document narrower boundaries instead of silently skipping. CuPy is a separate GPU requirement or recorded support limitation.

Configure CPU Torch resolution explicitly for tox-created environments: the root `tool.uv.sources` mapping does not automatically establish the source used by every dependency-install command. Use the appropriate platform-specific CPU distribution source without changing users' own CUDA environments. Log the selected Torch wheel/build and verify that dedicated Linux CPU jobs do not pull the unnecessary CUDA dependency set observed in the audit.

Reduce incidental installations with deliberate groups. Documentation-only jobs should use `uv sync --locked --only-group docs` and `uv run --locked --only-group docs zensical build --clean`. Ordinary developer defaults can remain convenient, but document minimal runtime, typing, and docs commands accurately. Ensure checker executables come from the intended environment and log their versions; resolving a Python symlink must not accidentally select tools from a different installation.

Use prek as the documented hook runner, since the configuration uses its builtins and priorities. Run the relevant local checks in CI, including secret scanning and actionlint. Prefer a locked local checker entry for pre-push over a separately drifting pyright hook version. Where hooks fix files, CI must fail on the resulting diff. Keep fast formatting/lint checks before expensive tests and avoid redundant complete test-suite launches. Pin external actions consistently to reviewed commits with an update mechanism; update existing tooling rather than inventing a workflow generator.

Keep matrix definitions understandable. Share a reusable validation workflow or small existing configuration source where it removes real duplication, but do not introduce a framework just to describe a few factors. Provide one final required validation status that fails if a required job fails, is unexpectedly skipped, or is cancelled. Environment-dependent skips must be classified: missing an expected installed backend is failure; unsupported platform precision and an explicitly excluded GPU suite are visible limitations. Preserve the existing coverage gate and report branch coverage separately.

Acceptance: a draft-PR CI run exercises the declared PR contract, a validation-only full matrix can be run before release, workflow names agree with tox validation, hooks leave the checkout clean, and CPU jobs install the intended dependency families. Record counts, versions, skips, and job links; do not infer success from the aggregate badge alone.

### M8 — Publish an accurate contract and test the actual distributions


Address A07 and A09 in `pyproject.toml`, `README.md`, `docs/`, `zensical.toml`, examples, and `CHANGELOG.md`. Add `license-files = ["LICENSE"]`, remove the redundant deprecated license classifier, and inspect actual wheel and source archive contents. Keep `py.typed` in the wheel. Include the source tests and their needed pytest/configuration files deliberately in the source distribution so a downstream maintainer can build and test it; exclude audit outputs, virtual environments, caches, generated site files, and irrelevant development artifacts.

Build the source distribution, build a wheel from that source distribution, and install the resulting wheel outside every source checkout. With normal dependency resolution and an exact rc0 constraint, run runtime smoke/integration checks and the consumer typing suite. Check archive metadata, the included license, public exports, installed version, optional import boundaries, and absence of accidental editable/source imports. Both Python endpoints must perform the exact-candidate artifact test. Do not validate one wheel and publish a freshly rebuilt different wheel.

Keep README short: purpose, installation, one valid beartype example, and links to backend/typing contracts. Fix the NDArray spelling, use Python-3.10-compatible syntax in universal examples, repair malformed tables and admonitions, and remove or correct the missing favicon reference. Replace hardcoded coverage claims with maintained evidence or omit them. Render representative pages and inspect their visible result; a successful Zensical exit code is insufficient. Add a narrow rendered-output smoke check only for meaningful regressions such as tables/admonitions disappearing, not snapshots of every layout detail.

Document strict versus Like behavior, same-kind casting, backend input families, Tree runtime/static boundaries, automatic versus explicit contexts, decorator order, tracing/compilation behavior, and all version/platform limitations agreed earlier. Explain the bare-check mode accurately. Execute maintained example code on the Python floor where claimed, and execute the existing notebook in an isolated environment with outputs reviewed; stale stored notebook output is not execution evidence. If a formatter damages valid documentation syntax, demonstrate and fix that round trip rather than assuming which tool caused the existing damage.

Update CHANGELOG for actual user-visible milestone changes, including compatibility-floor changes and migration notes. Do not preannounce unimplemented behavior. Use the user-approved `0.1.0rc0` candidate version. PyPI currently lists `0.0.1`; do not overwrite or reuse it. A final `0.1.0` release and publication still require a release decision.

Acceptance: wheel and sdist carry LICENSE and correct metadata, a rebuilt-from-sdist wheel installs and passes outside the checkout with exact rc0, static consumers retain useful types, rendered docs match tested behavior, and release notes describe all meaningful corrections without unsupported claims.

### M9 — Gate publication and prepare a reviewable ownership handoff


Address A08 in `.github/workflows/pypi.yml` and reusable validation configuration. Resolve a requested release tag/ref to an immutable commit. Verify the tag/version relationship, run the required validation against that commit, build and validate the artifacts, and publish only those artifacts after the protected release decision. The publish job must need successful validation, not merely a build. Avoid a second rebuild between validation and upload. Preserve OIDC trusted publishing and minimal permissions; do not introduce a long-lived upload token.

Provide a validation-only path that executes release checks and produces inspectable artifacts without publication. Test that a failed required validation prevents the publish job from becoming eligible. Restrict accepted publication refs/events intentionally; an arbitrary dispatch ref must not bypass release rules. Handle prerelease status deliberately, including the fact that the integration target is a release candidate. Record artifact hashes, source commit, resolved dependency versions, and validation results in the release evidence.

Prepare a handoff note for the user and receiving maintainers: product scope, support matrix, unresolved limitations, module map, integration assumptions on beartype, release procedure, and the mapping from audit findings A01–A10 to fixing commits/tests. Inventory repository protection, required checks, release-environment reviewers, trusted publisher repository/workflow/environment identity, documentation hosting, and package ownership. Read current settings before proposing concrete changes; the audit did not inspect all organization controls. Do not claim source changes alone establish these administrative protections.

Keep links pointing to the current real repository until the actual transfer is coordinated, then update repository/docs/badge metadata and confirm redirects as part of an explicitly authorized handoff. Never send messages to maintainers, transfer ownership, change access controls, or publish a release merely because this plan contains a handoff milestone. Prepare all unaffected work and the precise settings proposal first.

At the final review, provide the complete diff, CI and artifact evidence, compatibility/migration notes, and any remaining support limitations. Obtain the user's validation before merging, as required by AGENTS.md. After explicit merge approval, merge and clean up the implementation branch/worktree only when local changes and evidence are preserved. Actual publication and transfer follow their corresponding authorization and verified settings. If settings or GPU access remain unresolved, distinguish code readiness from release readiness instead of declaring the full objective achieved.

Acceptance: the exact reviewed commit cannot publish through the supported workflow without its required validation, artifacts are traceable to that commit, all P1 findings are fixed or replaced by an explicitly accepted enforceable contract, and the user has a concrete handoff packet and an accurate readiness verdict.

## Concrete Steps


Use the following command patterns in each focused worktree; replace the original umbrella branch/path with the actual feature branch/path tracked below. Use `/Users/ale/Code/bearshape` only for initial inspection and worktree creation. Before creation, inspect `git status --short`, `git worktree list`, and `git branch --list codex/production-readiness`. If the branch/worktree already exists, inspect and reuse the intended one; do not overwrite it.

    git -C /Users/ale/Code/bearshape rev-parse HEAD
    git -C /Users/ale/Code/bearshape log --oneline f43e00d2fe1714ae87d9f736f2a35692713ed0d4..HEAD
    git -C /Users/ale/Code/bearshape worktree add -b codex/production-readiness /Users/ale/Code/bearshape-production-readiness HEAD

After authorization, copy this document into the new worktree's `plans/2026-09-08-production-readiness.md`, commit that plan, push the implementation branch, and open the draft PR with a prose body stored in a file and passed through `gh pr create --draft --body-file`. Describe the final intended behavior and current draft status. Use the goal tool for the explicitly authorized implementation goal; do not fake it with a comment or create a recurring automation.

All remaining project commands run from `/Users/ale/Code/bearshape-production-readiness`. After a deliberate dependency edit, regenerate the lock once with `uv lock`, inspect the diff, and then use locked commands:

    uv sync --locked
    uv run --locked python -c 'import beartype; print(beartype.__version__, beartype.__file__)'
    uv run --locked pytest -n auto tests/test_memo.py tests/test_decorator.py tests/test_tree.py
    uv run --locked pytest -n auto tests/test_claw.py tests/test_numpy.py tests/test_jax.py tests/test_torch.py
    uv run --locked pytest -n auto tests/test_typecheck.py
    uv run --locked pyright src tests/typing
    uv run --locked mypy src tests/typing
    uv run --locked ty check src tests/typing
    uv run --locked pyrefly check src tests/typing

The new claw test file and pyrefly command become valid once their milestones add the file/dependency/configuration. The ordinary checker commands cover positive/inference fixtures; `tests/test_typecheck.py` must also exercise `tests/typing_negative/` and verify intended rejection. A checker process crash must be reported as failure, never as an expected error.

After M1 defines the proposed environments, run:

    uv run --locked tox run -e py310-bt023rc0-cpu
    uv run --locked tox run -e py314-bt023rc0-cpu

The final M7 matrix extends the same convention to `py311-bt023rc0-cpu`, `py312-bt023rc0-cpu`, and `py313-bt023rc0-cpu`, with named backend-floor and checker environments listed explicitly in the maintained plan once resolved. Avoid combining factors whose package versions cannot install on that interpreter. Every rc0 environment must log `0.23.0rc0` as the imported version.

Before final review run the full suite, configured coverage environment, hooks, workflow checks, and documentation build:

    uv run --locked pytest -n auto tests
    uv run --locked tox run -e dev
    uv run --locked prek run -a
    uv run --locked prek run -a --stage pre-push
    uv run --locked prek run actionlint -a --stage manual
    uv run --locked --only-group docs zensical build --clean
    git diff --check
    git status --short

Hook stages may repeat the full suite while the old configuration remains; M7 should eliminate redundant launches without removing distinct validation. Some hooks modify files: review the diff, rerun the affected checks, and record a clean result. Rendered documentation must then be inspected for actual tables, admonitions, examples, and links.

Build distributions into a fresh version-specific evidence directory outside the checkout. For example, after selecting an unused directory for the current candidate:

    uv build --out-dir /tmp/bearshape-release-candidate/dist

Use `uv venv` to create separate Python 3.10 and 3.14 artifact environments. Select the one wheel/sdist from the fresh output by its actual name; do not use a wildcard that could match stale releases. Run `uv pip install --python <environment-python> <wheel-path> 'beartype==0.23.0rc0'` with normal dependency resolution. Extract the source distribution into a fresh directory and run `uv build --wheel <extracted-source-directory> --out-dir <fresh-rebuilt-wheel-directory>`. The executing agent must replace these placeholders with actual recorded paths and names in this living section once available. Run consumer tests from an independent directory with source/editable paths absent, and verify `bearshape.__file__` resolves inside the artifact environment.

Expected final observations are behavioral: mismatched inputs/returns raise; the previously poisoned independent check returns true; the union example succeeds without leaked N; backend conversion counterexamples reject; valid typed calls retain useful backend types; designated invalid calls produce their intended diagnostics; the installed rc0 version is exact; and license/py.typed are present. Test counts will increase from the audited baseline and should be recorded as observed, not invented in advance.

## Validation and Acceptance


Every audit finding has a closing proof. A01 closes through normal exact-rc0 wheel installation and the candidate matrix. A02 closes through actual imported-package parameter and return failures. A03 closes through independent boolean checks, diagnostic correctness, memory-release evidence, and supported concurrent-context scenarios. A04 closes through whole-alternative rollback in the required integration surfaces or an explicitly accepted, enforceable revised contract; a skipped or documented known failure does not count as fixed.

A05 closes when the target converter and Like acceptance agree on both positive and negative backend fixtures. A06 closes when supported checkers accept real valid callers, reject deliberate errors, preserve useful types, and document runtime-only syntax accurately. A07 closes through inspected wheel/sdist contents and rebuilt-from-source installation. A08 closes through tested publication dependencies plus verified or explicitly pending administrative controls. A09 closes through correctly rendered and executed documentation examples. A10 closes through an observed matrix run, locked routine dependencies, intended CPU packages, and visible skip/support accounting.

The release gate requires all P1 findings to be resolved under the accepted contract, every required CI job successful for the exact candidate commit, normal artifact installation with exact rc0 at both Python endpoints, complete archive metadata/license, and no unsupported parity claim for CuPy or static shape inference. Python support means the relevant declared interpreter matrix actually ran. Checker support means the complete consumer contract ran on the declared tool versions. Beartype support means exact rc0 was used; a range in metadata is not proof for future versions.

Maintain readable failure messages and the optional dependency boundary throughout. Do not accept blanket ignores, xfails, removed annotations, disabled checks, lowered coverage gates, or a conversion to Any as substitutes for fixing a finding. If a genuine upstream limitation requires a support change, make it an explicit reviewed release decision with tests for the replacement boundary.

## Idempotence and Recovery


Work only in the isolated worktree for the current feature. Preserve the original checkout and audit evidence. Commit small coherent changes after targeted validation so a failed experiment can be reverted independently. Never use a hard reset or forced branch replacement to recover from unexpected local work. If an experiment does not meet its promotion gate, remove its production path while retaining the minimal regression and a concise result in this plan.

Use fresh artifact directories for each candidate and record commit/hash/version. Delete only task-created temporary environments after evidence is preserved; do not remove unrelated caches or environments. A lock regeneration is deliberate and reviewed, whereas normal checks use the existing lock. Installing a candidate in an isolated environment must not upgrade the user's normal workspace environment accidentally.

If source or dependencies change after validation, rerun the affected checks and any release-artifact checks whose inputs changed. Do not repeatedly run unrelated expensive suites after their inputs remain unchanged. Before merging or releasing, validate the final commit. If external settings or GPU access block the final gate, keep their exact unresolved status visible and continue independent work; do not manufacture success or repeatedly ask for the same approval.

## Artifacts and Notes


The original evidence is `/Users/ale/Code/bearshape-audit-2026-09-08/AUDIT.md` and its `evidence/` directory. Preserve it unchanged. During implementation, record concise logs for initial failing regressions, passing targeted runs, complete matrix runs, checker versions/diagnostics, artifact contents/hashes, and representative rendered docs. Use PR/CI artifacts for large logs rather than checking virtual environments or full build output into the repository.

Two minimal contracts summarize the highest-risk regressions. The first checks lifetime:

    a = np.ones(2, dtype=np.float32)
    b = np.ones(3, dtype=np.float32)
    assert not is_bearable((a, b), tuple[F32[N], F32[N]])
    assert is_bearable(b, F32[N])

The second checks a failed alternative's bindings:

    @beartype
    def f(
      pair: tuple[F32[N], I32[N]] | tuple[F32[C], F32[C]],
      y: F32[N],
    ):
      return y

    # Both pair members are float32 with length 2; y is float32 with length 3.
    # The second alternative succeeds and must not leave N bound by the first.
    assert f((a, a), b) is b

These snippets assume imports of NumPy, beartype, beartype.door.is_bearable, bearshape's N/C, and bearshape.numpy's F32/I32. The full repository regressions must also verify real rejection cases so an implementation cannot pass merely by disabling validation.

The final handoff packet must include the readiness verdict, accepted support matrix, known limitations, migration notes, fixing commits for A01–A10, validation links, artifact hashes, and the concrete remaining administrative actions. Summarize results for maintainers who have not read the conversation.

## Interfaces and Dependencies


Keep `bearshape.claw.bearshape_this_package` callable under its current public import name with upstream-compatible keyword configuration. Prefer aliasing the upstream function to preserve caller-package discovery. Keep `check(fn, /)` preserving `Callable[P, R]` and `check(*, conf=...)` returning a decorator with the same signature preservation; describe and type the existing None/omitted configuration behavior truthfully. Keep `check_context()` a synchronous and asynchronous context manager with explicit shared bindings and reliable cleanup.

Keep strict backend annotations nominally related to their actual backend array class and dtype where supported. Keep Like as an input contract that validates but does not replace the argument. Keep NumPy's scalar-like, structured dtype, and broad Shaped surface in its backend module. Keep runtime tree structure checking explicit, and admit only the static promises demonstrated by M5. No new public transaction, replay, or backend-registration abstraction is prescribed: first solve the proven private integration problem with the smallest maintainable design.

Use uv, tox/tox-uv, pytest, pyright, mypy, ty, pyrefly, prek, and the existing Zensical documentation system. Additional runtime dependencies, a new checker framework, a new documentation generator, or a replacement for beartype are outside this plan unless a later accepted decision establishes their necessity. NumPy, JAX, Torch, CuPy, and optree remain user-selected optional backends. Pin reproducible development/CI resolutions while maintaining an honest documented support range.

Revision note — 2026-09-08: Initial proposal derived from the completed audit. The plan makes rc0 installation, invocation/branch feasibility, real consumer typing, backend conversion, and tested release artifacts explicit acceptance gates. Implementation has not started.

## Implementation PR map


The roadmap PR owns this living program. Planned independent changes are rc0 compatibility/release metadata; caller-package claw integration; validation lifetime and composite feasibility; backend conversion; consumer typing; CI/dependency enforcement; documentation; distribution contents; and publication gates. Runtime feature/performance evidence accompanies the relevant fixes. Where one change requires another, use an explicit dependent PR and record its base. Merge approval was granted on 2026-09-08 and executed through PR #31; every reviewed head is preserved and its main gate passed.

Revision note — 2026-09-08 implementation start: User selected `0.1.0rc0`, independent versioning, and separate PRs. These decisions supersede the original single-PR proposal. Goal created; implementation work is beginning.

Revision note — 2026-09-08: Recorded implemented PRs and validation evidence, with the unresolved native-union design decision and remaining typing/artifact/docs work stated explicitly.

Revision note — 2026-09-08: Recorded PRs #19–#22, combined runtime/checker validation, minimal installation and actual H200 baseline evidence. CuPy native creation/reshape returns Any or Unknown under all four installed checkers because the backend lacks ndarray stubs; no full static-support claim was added. GPU transfer was initially blocked, then approved after proving the payload matched the public repository commit.


## Implemented review map and current release boundary


PR #12 owns this roadmap. Focused PRs #13–#21 cover rc0 compatibility, caller import hooks, validation lifetime, conversion, checker conformance, archive contents, Like inputs, Tree consumers and framework/minimal validation. #22 is their validation aggregate. Focused #23–#26 add CI, docs, installed consumers and CUDA proofs; #27 aggregates them without modifying their actual PR bases. #28 adds the publication gate, #29 the feature/performance/handoff evidence, and #30 the observed Node runtime maintenance. Preserve the prerequisite relationships in each PR before requesting merge approval.

The validated release run https://github.com/acecchini/bearshape/actions/runs/34221337124 used source 3ee4c1d8a0c3d22f537a24b447a9d75e025a5b2d. Wheel SHA256 c1806203da013c9eaf2482a309c686a984c0a7031a495efbd100a824536b57d2; sdist SHA256 e2454095144fb4bb5a08d3bd998d0f6a8bee4bc5ad81dfab763c339ca91666df. Both Python endpoints passed 1,097 installed consumer tests with one absent-CuPy skip, and the exact same wheel passed 95 GPU tests per endpoint on H200/CUDA 12.9/CuPy 14.2.0. Later source changes require their own archive identity and applicable validation.

Matched normally installed baseline/candidate measurements on CPython 3.10.20 with NumPy 2.2.6 and optree 0.19.1 show strict checks around 19.8 microseconds versus 21.8 in the baseline, explicit checks around 14 microseconds, and expected conversion/tree scaling. Scope/signature discovery remains costly; no speculative cache was added while the composition boundary is unresolved. Evidence files performance-matched-*.json and performance-profile.log record versions, origins, medians and spread.

Read-only controls inspection found main unprotected, no repository rulesets, and no approval reviewers on pypi; its policies allow main and v* tags with admin bypass. PyPI publisher configuration remains unverified. docs/maintainers/production-readiness.md in #29 gives the exact proposed protections, release process, module/support map, migrations and A01–A10 review links. No owner settings, package publication, repository transfer or messages to other maintainers occurred.

Revision note — 2026-09-08: Updated M6–M9 and the outcome with the completed independent PRs, exact installed/GPU artifact evidence, actual release dry run, performance observations and remaining release decisions. #30 final hosted action validation is complete.

Revision note — 2026-09-08: Final validation-only run https://github.com/acecchini/bearshape/actions/runs/34223582731 completed 38 required jobs and skipped publication. It passes 1,101 installed-consumer tests per endpoint (one absent-CuPy skip), validates Pages packaging without deployment, and retains the exact GPU-validated wheel SHA256 c1806203da013c9eaf2482a309c686a984c0a7031a495efbd100a824536b57d2. Source 6f40e4a484b70535c58e2c86a645a64ab1079143; sdist SHA256 38d89d4ce1b351601ff8602a9a27b4e9af46db056be3ac0eaf41a68ac56a3706. The former Node 20 runtime warning is gone; the current upstream downloader still emits a Buffer() deprecation notice, recorded without suppression. All independent implementation work is prepared for review; full production readiness still depends on the explicit contract decisions and owner validation.

Revision note — 2026-09-08 owner approval: recorded accepted union/CuPy policies
and merge authorization; PR #31 updates AGENTS/CLAUDE, PLANS, contributor/tool
commands and Pages deployment semantics. A later dependency is allowed but no
available fix is claimed. Historical exact-rc0 acceptance records remain proof
of the tested baseline, not a restriction against the newly selected path.

Revision note — 2026-09-08 merge execution: PR #31 integrated the complete
approved history without squashing. Main run 34229683377 passed all 36 jobs;
Pages run 34229683120 built and skipped deployment. Dependent PRs were closed
as integrated after ancestry verification. Twenty clean merged worktrees and
local branches were removed with generated evidence preserved. PR #33 fixes
actual hook stage routing and Git environment isolation, adds four regressions
(23 release-tool cases total), and passed hosted run 34231187384. The root
checkout's hook installation is active; its temporary checkout-path setting
introduced by the old fixture was restored and verified clean.

An isolated normal install of upstream beartype main at
a2729e0e358bf963ee6f177e300ae08a622d05d6 reports 0.23.0rc1 and still fails the
native-union probe. Keep the current rc0 lock; the owner allows a later candidate
but no working supported integration exists in either tested version. The
production goal remains incomplete for that integration and release controls.
