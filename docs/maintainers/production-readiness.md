# Production review and ownership handoff

This is the 8 September 2026 review record for **bearshape 0.1.0rc0**. The
candidate is independently versioned from beartype and requires
`beartype>=0.23.0rc0,<0.24`. Exact `0.23.0rc0` remains the current required test
target until a supported replacement is implemented and validated.

**Release readiness is withheld.** Native composite-union rollback remains
incorrect with published rc0. A tested local upstream patch is now prepared; its
availability and validation are recorded below. The owner selected full
composition through supported upstream integration and permits a later beartype
candidate; explicitly limited native CuPy static support is accepted. The owner
approved merging the reviewed production work on 8 September 2026. PR #31
integrated all reviewed heads into main at
`df81f00e2f62bda956244e680c980f87db1d4671`; its post-merge CI passed all 36
jobs. Repository/publication protections still require configuration, and
publication or ownership transfer requires separate authorization.

## Purpose and intended users

bearshape checks array shape, dtype and related tree constraints at Python API
boundaries using beartype. Its main users are scientific Python developers,
model and numerical-library authors, and application teams that want useful
runtime failures alongside editor/type-checker support. It complements native
NumPy, JAX, Torch and CuPy types while retaining backend operations.

Use it around meaningful function and module boundaries. Strict checks inspect
metadata; tree checks visit leaves; Like checks may convert data and allocate or
transfer memory. It is not a static shape prover, a replacement array backend,
or an untrusted-expression sandbox. `Value` expressions are developer-authored
contracts; permitted attribute access can invoke ordinary Python behavior.

The next evolution should close the integration boundary with beartype and
maintain the tested annotation contract. New syntax, additional checker engines
and speculative caching are not needed for this release. Zuban is outside the
selected support contract. A future addition needs an explicit plan and real
positive, negative and inference fixtures.

## Observed support

<!-- markdownlint-disable MD013 -->

| Surface         | Evidence                                                                                                    | Boundary                                                                                                       |
| --------------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| CPython         | Linux 3.10–3.14; macOS/Windows 3.10 and 3.14 CPU jobs                                                       | Other interpreter implementations are unverified                                                               |
| beartype        | Exact 0.23.0rc0 in required lanes and normal installs                                                       | Native composite-union rollback blocks full compatibility; the metadata range is not proof for future releases |
| NumPy           | Locked current and 2.2 floor; strict/Like/scalar/structured/endian/temporal tests                           | Extended precision depends on platform                                                                         |
| JAX             | Locked current and 0.5 floor; jit/vmap/grad numerical and violation cases                                   | Checks inside JIT run while tracing; see [frameworks](../features/frameworks.md)                               |
| Torch           | Locked current and 2.6 floor; autograd and compile cases                                                    | Compile evidence uses `backend="eager"` with outer Python validation                                           |
| optree          | Locked current and 0.14 floor; containers and structure binding                                             | Default registry only; no custom namespace API                                                                 |
| CuPy            | 95 tests on H200, CUDA 12.9, CuPy 14.2.0, Python 3.10.20/3.14.3                                             | Other GPU/driver combinations and multiple-device behavior are unverified; native static typing is limited     |
| Static checkers | pyright, mypy, ty and pyrefly positive/negative/inference batches on Python 3.10–3.14 and configured floors | Dimensions are runtime constraints; advanced syntax and native CuPy limitations are explicit                   |
| Minimal install | Normally installed wheel with only declared dependencies at Python endpoints                                | Root import loads none of NumPy/JAX/Torch/CuPy/optree; custom strict arrays work without NumPy                 |

<!-- markdownlint-enable MD013 -->

The locked checker versions are pyright 1.1.411, mypy 2.3.1, ty 0.0.79 and
pyrefly 1.2.0. Separate floors exercise pyright 1.1.408 and mypy 1.19, plus the
selected ty/pyrefly versions. The harness checks exact diagnostic locations and
categories, including deliberate invalid calls; a checker crash or missing tool
fails the run. See [static typing](../features/static-typing.md) for accepted
annotation forms.

## Implementation map

<!-- markdownlint-disable MD013 -->

| Module                                      | Responsibility and maintenance boundary                                                 |
| ------------------------------------------- | --------------------------------------------------------------------------------------- |
| `__init__.py`, `_imports.py`                | Lightweight public identity, factories/symbols and explicit optional-dependency loading |
| `_dimensions.py`, `_shape.py`               | Shape tokens, arithmetic and bounded parsing of permitted expressions                   |
| `_dtypes.py`                                | Dtype families, structured equality, byte order and normalization                       |
| `_runtime_hints.py`                         | Runtime hint classes and useful instance-check failure reporting                        |
| `_array_types.py`                           | Strict and Like validation, selected converters and failed-leaf rollback                |
| `_memo.py`                                  | Invocation-owned automatic state, explicit ContextVars and scope lookup                 |
| `_decorator.py`                             | Memo-only/combined decorator modes, metadata, async cleanup and explicit contexts       |
| `_tree.py`, `optree.py`                     | Tree leaves and structures with explicit traversal backend                              |
| `numpy.py`, `jax.py`, `torch.py`, `cupy.py` | Backend aliases, conversion boundaries and static declarations                          |
| `_typing.py`                                | Shared static input families; no runtime backend imports                                |
| `claw.py`                                   | Direct re-export of the caller-sensitive upstream import hook                           |

<!-- markdownlint-enable MD013 -->

Automatic memo discovery recognizes generated beartype frames and stores state
in the live frame's locals. This is an integration assumption on upstream code
generation, covered at exact rc0 across the declared CPython matrix. Explicit
contexts use ContextVars; child tasks inherit live memo references unless they
create their own context. Failed leaf checks restore their own mutations, and
diagnostic formatting restores state without retaining failed user objects.

A leaf callback cannot observe rejection of an entire surrounding native union
alternative after a later ordinary type check fails. Neither global replay
caches nor bytecode guesses provide that missing boundary. No upstream
monkeypatch or replacement type-checker implementation was introduced.

## Feature-to-test map

Paths below are relative to the repository root. Each row identifies existing
positive and negative evidence, not merely annotation declarations.

<!-- markdownlint-disable MD013 -->

| Contract                                                            | Representative tests                                                                                                                                                                                                           |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Named/fixed/anonymous dimensions and rank                           | `tests/test_shape.py`: `TestNamedDim`, `TestFixedDim`, `TestAnonymous`; `tests/test_numpy.py`: `TestCrossArgConsistency`                                                                                                       |
| Arithmetic, variadics and broadcasting                              | `tests/test_shape.py`: `TestSymbolicDim`, `TestVariadicDim`, `TestNamedDimEdgeCases`; `tests/test_numpy.py`: `TestBroadcastableDims`, `TestMultipleVariadicRejected`                                                           |
| Scalar and invalid token combinations                               | `tests/test_dimensions.py`: `TestMixedScalarRejection`, `TestScalarArithmeticRejection`, `TestBooleanDimRejection`                                                                                                             |
| Value lookup, arithmetic and rejected expressions                   | `tests/test_shape.py`: `TestValueDim`, `TestSymbolicEdgeCases`; `tests/test_numpy.py`: `TestValueExpressions`; `tests/test_decorator.py`: `TestValueWithCheckDecorator`                                                        |
| Dtype families, byte order, structured fields and temporal units    | `tests/test_dtypes.py`: `TestDtypeSpecMatches`, `TestByteorderMatching`, `TestShapedVoidAndStructured`, `TestDatetimeTimedelta`; `tests/test_numpy.py`: `TestStructuredDtypeIntegration`, `TestStructuredLikeDtypeEnforcement` |
| Scalar-like range/casting and boolean rejection                     | `tests/test_numpy.py`: `TestScalarLikeBoundariesExtended`, `TestScalarLikeCastingVariants`, `TestNumericScalarBooleanRejection`                                                                                                |
| Strict versus Like backend conversion                               | Backend `Test*ConversionContract` classes; NumPy `TestCustomConversionContract`; CuPy `TestCuPyConverterContract`                                                                                                              |
| Return checks, nested calls and readable diagnostics                | `tests/test_numpy.py`: `TestReturnViolations`, `TestNestedCalls`, `TestDiagnosticMessages`; corresponding backend tests                                                                                                        |
| Invocation lifetime, independent checks, memory release and threads | `tests/test_memo.py`: `TestIndependentCheckLifetime`, `TestThreadSafety`, `TestFrameBasedMemo`                                                                                                                                 |
| Decorator metadata, modes, async cancellation and task contexts     | `tests/test_decorator.py`: `TestDecoratorEdgeCases`, `TestAsyncCheckDecorator`, `TestMemoIsolation`, `TestCheckRejectsGenerators`, `TestCallBoundaryContracts`                                                                 |
| Tree leaf dtype/shape, structures and return constraints            | `tests/test_tree.py`: `TestBasicTree`, `TestCrossLeafConsistency`, `TestStructureBindingFailures`, `TestMultiLevelFailures`, `TestReturnTypeFailures`                                                                          |
| Real import-hook caller discovery                                   | `tests/test_claw.py`: `test_instruments_caller_package` imports actual temporary packages/submodules with default/custom configuration                                                                                         |
| Framework transformations and device behavior                       | `tests/test_jax.py`: `TestJaxTransformations`; `tests/test_torch.py`: `TestTorchTransformations`; `tests/test_cupy.py`: `TestCuPyDeviceBehavior`, `TestCuPyTrees`                                                              |
| Optional imports and custom backend operation                       | `tests/test_coverage_edges.py`: `TestOptionalBackendImports`, `TestVersionExport`; `tools/smoke_minimal.py` from a minimal installed wheel                                                                                     |
| Static consumers and expected failures                              | `tests/test_typecheck.py`, `tests/typing/check_*consumers.py`, `tests/typing_negative/invalid_*calls.py`                                                                                                                       |
| Documentation and distributions                                     | `tests/test_examples.py`, `tools/check_docs.py`, `tools/check_notebook.py`, `tools/check_distribution.py`, `tools/check_installed.py`                                                                                          |
| Publication identity and bypass rejection                           | `tests/test_release.py`: 23 cases using disposable Git histories, events and foreign hook environments                                                                                                                         |

<!-- markdownlint-enable MD013 -->

The endpoint and platform jobs exercise these files with the actual interpreter
and dependencies. Expected missing-CuPy and platform-precision skips are
visible; preflight checks fail if an expected CPU backend is absent. The
native-union case below remains outside the passing contract and blocks release
rather than being hidden behind an expected-failure marker.

## Audit findings and independent review units

<!-- markdownlint-disable MD013 -->

| Finding                                | Change and closing evidence                                                                                                                                                                                                | Status                                               |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| A01: exact rc0 installation            | [#13](https://github.com/acecchini/bearshape/pull/13), [#25](https://github.com/acecchini/bearshape/pull/25): normal resolver installs and endpoint artifact consumers                                                     | Implemented and validated                            |
| A02: caller-package import hook        | [#14](https://github.com/acecchini/bearshape/pull/14): direct alias and real package import violations                                                                                                                     | Implemented and validated                            |
| A03: stale state and retained failures | [#15](https://github.com/acecchini/bearshape/pull/15): live-frame ownership, independent failures, mutation, weak references and threads                                                                                   | Implemented and validated                            |
| A04: composite alternative rollback    | Exact hosted wheel still rejects the valid example below                                                                                                                                                                   | **Release blocker; upstream path selected**          |
| A05: converter fallback and trust      | [#16](https://github.com/acecchini/bearshape/pull/16), [#26](https://github.com/acecchini/bearshape/pull/26): actual backend converter oracles and GPU cases                                                               | Implemented and validated                            |
| A06: consumer typing                   | [#17](https://github.com/acecchini/bearshape/pull/17), [#19](https://github.com/acecchini/bearshape/pull/19), [#20](https://github.com/acecchini/bearshape/pull/20): four engines, Like inputs and structural Tree callers | CPU surfaces validated; limited CuPy policy accepted |
| A07: incomplete distributions          | [#18](https://github.com/acecchini/bearshape/pull/18), [#25](https://github.com/acecchini/bearshape/pull/25): license, typing marker, source inputs and installed consumers                                                | Implemented and validated                            |
| A08: publication without validation    | [#28](https://github.com/acecchini/bearshape/pull/28): immutable workflow/package identity, full gate and same artifacts                                                                                                   | Code validated; administrative controls pending      |
| A09: documentation drift               | [#24](https://github.com/acecchini/bearshape/pull/24): formatter round trip, rendered structures, executed snippets/notebook                                                                                               | Implemented and validated                            |
| A10: hooks/CI/dependency drift         | [#23](https://github.com/acecchini/bearshape/pull/23): locked reusable matrix, CPU resolution, four-checker pre-push and strict aggregate gate                                                                             | Implemented and validated                            |

<!-- markdownlint-enable MD013 -->

[#21](https://github.com/acecchini/bearshape/pull/21) supplies framework/minimal
proofs. [#22](https://github.com/acecchini/bearshape/pull/22) and
[#27](https://github.com/acecchini/bearshape/pull/27) are validation aggregates
that preserve focused PR branches. Merge prerequisites and living decisions are
recorded in each PR's ExecPlan and the roadmap in
[#12](https://github.com/acecchini/bearshape/pull/12).

The approved history is integrated through
[#31](https://github.com/acecchini/bearshape/pull/31), preserving every reviewed
head without squashing. GitHub marked main-based PRs merged automatically;
dependent PRs were closed with an integration record after ancestor
verification. Twenty clean worktrees and their local branches were removed after
preserving coverage/build evidence; the corresponding remote branches were
deleted with expected-head checks. The original checkout remains on main.

Actual hook installation then exposed two defects addressed in
[#33](https://github.com/acecchini/bearshape/pull/33): file checks ran at the
commit-message stage and rejected a worktree Git path, and inherited Git
repository variables redirected disposable release-test commands. File hooks now
default to pre-commit, the unused commit-message shim is removed, and Git
commands explicitly targeting another repository clear Git's local environment
variables. CI checks installed stage routing; four new cases cover foreign Git
environments and ensure fixture construction preserves the hook owner's config
and HEAD. Real commits and pre-push runtime/checker checks pass. Hosted run
[34231187384](https://github.com/acecchini/bearshape/actions/runs/34231187384)
passed the complete matrix at `0717df2f2194cdcb10bcf37ba291c09117c42238`.

The main Pages run
[34229683120](https://github.com/acecchini/bearshape/actions/runs/34229683120)
built successfully and skipped deployment. Contributor instructions now require
an explicit docs dispatch and explain removal of an old commit-message shim.

### Accepted native-union integration path

This valid call is still rejected by the tested wheel with exact rc0:

```python
import numpy as np
from beartype import beartype
from bearshape import C, N
from bearshape.numpy import F32


@beartype
def choose(pair: tuple[F32[N], str] | tuple[F32[C], int], y: F32[N]) -> None:
    pass


choose((np.ones(2, dtype=np.float32), 1), np.ones(3, dtype=np.float32))
```

The first alternative binds `N=2`, then fails its `str` check. The second
alternative succeeds and should bind only `C=2`. `y` should then establish
`N=3`, but the failed alternative's binding survives and rejects it.

The owner selected an upstream-supported whole-alternative integration boundary
and permits a later beartype candidate. Preserve full composition. A warning,
bytecode heuristic, monkeypatch or restricted annotation contract does not close
this defect. On 8 September 2026, PyPI offered only `0.23.0rc0` in the 0.23
series; the approval is a direction, not evidence of an available fix. An
isolated normal install of upstream development commit
[`a2729e0`](https://github.com/beartype/beartype/commit/a2729e0e358bf963ee6f177e300ae08a622d05d6)
identifies itself as `0.23.0rc1` and still rejects the same valid call. That
unpublished revision is evidence of the remaining defect, not a supported new
compatibility floor.

Run `uv run --locked python tools/probe_union.py` from the repository root to
reproduce the current failure with version information. Its nonzero exit is
explicit blocker evidence. A later candidate must preserve bindings from earlier
successful parameters, discard a whole failed alternative's shape/tree state,
commit successful alternatives, isolate diagnostic checks and restore state on
exceptions. Cover nested unions, return checks, explicit/automatic scopes, async
paths and object lifetime before changing the compatibility floor and rerunning
the complete normal-install matrix. No upstream message or patch has been
submitted on the owner's behalf.

### Tested local union fix, pending upstream review

The follow-up implementation in PR #34 exposes a shared snapshot callback from
bearshape runtime hints and pairs it with a local beartype source extension.
Upstream patch commit `4aef992d1cd0a6d09fe5c3784523c44e0874b178`, based on
`a2729e0e358bf963ee6f177e300ae08a622d05d6`, adds complete-alternative
transactions, exception cleanup and isolated diagnostic replay. Lazy forward
references join active transactions before mutating state, while unselected
references remain unresolved. There is no runtime monkeypatch or replacement
type checker.

The original probe and all 22 explicit integration cases pass with the patch.
Normally installed packages passed 1,124 combined runtime, static-checker and
integration tests on both Python 3.10.20 and 3.14.5, with five existing CPU skip
records per interpreter (CuPy plus four platform precision cases). Upstream's
own serial unit suite passed 426 tests on Python 3.10 and 439 on Python 3.14,
with 20 and seven pre-existing skip records respectively. Upstream pyright
reports no errors. The focused plan records final artifact identities and
performance measurements. Final archive-extracted consumers independently passed
the same 1,124 tests per endpoint, and minimal installs passed without optional
backends. A matched benchmark measured strict small-array calls at about 19
microseconds with rc0 and 31 with the patch; this overhead is an explicit
upstream review tradeoff.

This demonstrates a working local fix, not compatibility provided by published
rc0. The dependency metadata and lock are unchanged, and the new integration
suite under `tools/upstream/` is explicitly invoked rather than silently skipped
or marked xfail. Normal rc0 CI can remain green while that separate suite fails
on rc0. After upstream acceptance and release, adopt the concrete dependency
across metadata, lock, preflight and CI, move the cases into the required suite,
and rerun candidate validation including CUDA. The patch has not been submitted
upstream, and no package has been published or ownership transferred.

See `tools/upstream/README.md` in the repository for commands.

### CuPy static boundary

CuPy 14.2.0 supplies neither `py.typed` nor usable native ndarray stubs. A real
installed-CuPy consumer reveals Unknown/Any for ordinary native operations:
strict pyright/mypy report missing typing information, while ty/pyrefly can
accept the code with Unknown. The protocol fallback proves only its small
structural surface; it does not establish native method inference.

The owner accepted explicitly limited static CuPy support alongside the verified
GPU runtime behavior. This is no longer an open release-policy decision. Keep
the limitation visible in typing docs and release notes; do not claim native
method inference or parity with NumPy/JAX/Torch. Any future stronger typing
claim needs actual installed-CuPy positive, negative and inference consumers.

## Validated artifact identity

The hook follow-up run
[34231187384](https://github.com/acecchini/bearshape/actions/runs/34231187384)
validated source `0717df2f2194cdcb10bcf37ba291c09117c42238`. Both Python
endpoint consumers passed **1,105 tests**, with one explicit absent-CuPy skip
each. Its wheel SHA256 remains
`c1806203da013c9eaf2482a309c686a984c0a7031a495efbd100a824536b57d2`, identical to
the GPU-tested artifact. Its updated sdist SHA256 is
`19b7e7252f2c64e4ea014e92a14b7a25a8409db20612205da257c1d04df9e85b`. The earlier
release-specific runs below remain evidence of publication gating; no
publication was triggered by these merges.

The actual
[validation-only release run](https://github.com/acecchini/bearshape/actions/runs/34221337124)
completed with 38 successful jobs and its sole publishing job intentionally
skipped. It ran all
runtime/checker/floor/docs/notebook/archive/minimal/installed checks against
source commit `3ee4c1d8a0c3d22f537a24b447a9d75e025a5b2d`. The `release-evidence`
artifact records:

```text
version: 0.1.0rc0
wheel SHA256:
c1806203da013c9eaf2482a309c686a984c0a7031a495efbd100a824536b57d2
sdist SHA256:
e2454095144fb4bb5a08d3bd998d0f6a8bee4bc5ad81dfab763c339ca91666df
```

The wheel was built from the source archive and installed normally outside the
checkout at both Python endpoints. The exact same wheel also passed all 95 CuPy
GPU cases on both endpoints without skips. The consumer driver copies the
archive's own lockfile, tests and tooling, leaves package source absent, and
verifies site-packages origins and exact beartype rc0. The same artifact pair is
what the publisher would download; it does not rebuild distributions. Later
source changes produce their own source-archive hashes and require their
applicable validation before publication.

The subsequent
[Node 24 validation run](https://github.com/acecchini/bearshape/actions/runs/34223582731)
also completed 38 successful jobs and skipped publication. It includes the four
additional call-boundary cases: 1,101 installed-consumer tests pass at each
endpoint with one absent-CuPy skip. Its source is
`6f40e4a484b70535c58e2c86a645a64ab1079143`; its wheel is byte-identical to the
GPU-validated wheel above. Its updated source archive has SHA256:

```text
38d89d4ce1b351601ff8602a9a27b4e9af46db056be3ac0eaf41a68ac56a3706
```

[#30](https://github.com/acecchini/bearshape/pull/30) updates artifact/Pages
actions to reviewed Node 24 releases. Required docs validation successfully
packaged the 46-file Pages archive, including this report and the logo. The
inspected action logs no longer contain the Node 20 deprecation warning. Actual
Pages deployment remains unperformed during this review. The current upstream
download action still emits a `Buffer()` deprecation notice; no suppression was
added. Artifact digest verification and all consumers passed.

## Performance observations

A matched comparison uses normally installed baseline/candidate wheels on the
same macOS arm64 host, CPython 3.10.20, beartype 0.23.0rc0, NumPy 2.2.6, optree
0.19.1 and typing_extensions 4.16.0. The baseline is the rc0-floor artifact
before runtime corrections; the candidate is the hosted artifact identified
above. Five repetitions report medians and min/max, without a CI timing gate.

<!-- markdownlint-disable MD013 -->

| Workload                | Baseline median (µs) | Candidate median (µs) | Candidate min–max (µs) |
| ----------------------- | -------------------- | --------------------- | ---------------------- |
| `native/3`              | 0.120                | 0.120                 | 0.119–0.124            |
| `strict/3`              | 21.827               | 19.818                | 19.702–20.084          |
| `strict/1000000`        | 21.732               | 19.730                | 19.668–19.761          |
| `explicit/3`            | 14.554               | 14.042                | 13.979–14.076          |
| `like/3`                | 11.356               | 10.208                | 10.177–10.223          |
| `value/3`               | 16.295               | 15.770                | 15.730–15.795          |
| `nested/3`              | 44.192               | 40.943                | 40.873–41.015          |
| `like-sequence/1000000` | 13950.325            | 13596.900             | 13385.142–13735.867    |
| `tree/1`                | 34.232               | 32.245                | 32.095–34.930          |
| `tree/100`              | 517.754              | 487.143               | 485.315–488.897        |
| `diagnostic/3`          | 124.950              | 120.643               | 119.869–122.627        |

<!-- markdownlint-enable MD013 -->

Run `uv run --locked python tools/benchmark_runtime.py` to reproduce the
workloads. The script records versions, origins and per-case call counts.
Ordinary cases use 10,000 calls per repetition; expensive sequence conversions,
100-leaf trees and diagnostics use explicit smaller counts recorded in JSON. The
results are local observations, not cross-platform guarantees or a comparison
with another shape library.

Strict native checks show little dependence on element count. Sequence
conversion scales with data size; tree validation scales with leaf count.
Profiling the strict path identifies scope/frame discovery and repeated
signature inspection as remaining costs. No new cache or optimization was
introduced while the composition boundary is unresolved. Prefer checks at
meaningful API boundaries and revisit scope work after the integration contract
is settled.

## Migration and administrative handoff

Users move from the prior beartype generation to the rc0 floor. Backend Like
validation now obeys the selected converter and retains the original argument;
values accepted only through a NumPy fallback may be rejected. Like/Tree static
annotations accept the tested ordinary callers while preserving useful native
types. Bare `@check` remains memo-only; combine it with `@beartype` or use
`@check(conf=...)` for checking. Public identity remains lowercase `bearshape`.

Read-only GitHub inspection on 2026-09-08 found no protection on `main`, no
repository rulesets, and no required approval reviewers on `pypi`. That
environment currently permits `main` branches and `v*` tags, with administrator
bypass enabled. `github-pages` permits `docs`/`main` branches. These controls
were not changed. PyPI publisher configuration and package ownership have not
been verified through an authenticated package-owner interface.

Before publication, the owner and receiving organization should approve and
apply the following concrete settings:

1. Protect `main` with reviewed pull requests, stale-approval dismissal, blocked
    force-push/deletion, and the observed `validate / Required validation`
    check from the final CI workflow. Verify the exact check identity after the
    PR set is merged; do not require a stale job name.
1. Protect release tags against unreviewed creation, replacement and deletion.
    Add named receiving maintainers or a designated release team as the
    authorized release actors.
1. Require release-review approval on `pypi`, prevent self-review, disallow
    administrator bypass, and restrict deployments to approved version tags.
    The publish workflow must itself run from the matching tag and commit.
1. Verify the PyPI trusted publisher's repository owner/name, workflow
    `pypi.yml` and environment `pypi`. Reconfigure the identity for the
    receiving organization during an explicitly authorized transfer; retain
    OIDC rather than adding an upload token.
1. Confirm GitHub/PyPI ownership and recovery access with the actual receiving
    maintainers. Coordinate GitHub Pages hosting, its deployment environment,
    redirects and repository/package metadata. Update public URLs only after
    the transfer is real, then verify them.
1. Complete the selected upstream union integration. Run the final immutable
    candidate validation, inspect hashes and GPU evidence, then separately
    authorize the prerelease publication and ownership operations.

The repository changes make these steps reviewable; they do not perform them.
See the repository's `CONTRIBUTING.md` for validation-only, tag-based release
and explicitly dispatched Pages deployment procedures. `AGENTS.md` and the
`CLAUDE.md` symlink share current agent guidance; `tools/README.md` documents
the existing validators. PR #31 aligns those files with the accepted decisions.
