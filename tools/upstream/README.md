# Native union integration proposal

The `test_union_transactions.py` suite exercises the proposed beartype
`__beartype_state__` protocol. It runs explicitly because the required upstream
change has not shipped. These tests are real failures on published beartype
`0.23.0rc0`; they have no skips or expected-failure markers. Passing the normal
rc0 CI suite does not prove this integration.

The bearshape adapter exposes the existing `get_memo` function as a shared state
getter on its runtime-hint metaclass. It returns the active `ShapeMemo`, whose
`snapshot()` and `restore(token)` methods cover single dimensions, variadic
dimensions and tree structures. State is located once per checking expression.
Existing leaf validation remains necessary for rc0 and bare `isinstance` calls.

The original local proposal at upstream commit
`4aef992d1cd0a6d09fe5c3784523c44e0874b178` used a callback per snapshot. It
remains historical comparison evidence. The optimized proposal replaces that
interface with a state getter, compiles checking functions once, keeps simple
rollback records, and avoids unnecessary root snapshots and stateless-path
setup. Both proposals are based on upstream
`a2729e0e358bf963ee6f177e300ae08a622d05d6`, which identifies itself as
development `0.23.0rc1`. This version string does not imply acceptance or
publication. The optimized patch and exact commit are recorded in the focused
ExecPlan. Neither proposal is vendored or applied at import time.

## Reproduce

Apply the supplied patch to a clean checkout of the upstream base commit. From
this bearshape checkout, export the locked tools and backends while excluding
the upstream package being tested:

```sh
uv export --locked --no-hashes --no-emit-project --no-emit-package beartype \
  --output-file /tmp/bearshape-union-requirements.txt
uv venv /tmp/bearshape-union-env --python 3.10
UV_TORCH_BACKEND=cpu uv pip install \
  --python /tmp/bearshape-union-env/bin/python \
  -r /tmp/bearshape-union-requirements.txt \
  /path/to/patched/beartype .
/tmp/bearshape-union-env/bin/python tools/probe_union.py
/tmp/bearshape-union-env/bin/python -m pytest \
  tests/ tools/upstream/test_union_transactions.py -n auto
```

Repeat in a separate Python 3.14 environment. The probe must pass, the new
regressions must pass without skips, and the existing runtime and four-checker
suite must remain green. Use the environment's interpreter directly: a later
`uv run --locked` would restore the published dependency from the lock.

To observe the published dependency's unresolved failure directly:

```sh
uv run --locked python tools/probe_union.py
uv run --locked pytest tools/upstream/test_union_transactions.py -n 0
```

Both commands currently fail. This is baseline evidence, not successful
validation. Once an upstream-supported release exists, update the dependency
floor, lock, exact-version preflight and shared CI together, and move these
regressions into the required `tests/` suite. Do not retain a separate optional
integration lane after adopting the dependency that fixes the defect.

## Verified behavior

The 22 integration cases cover selected and rejected alternatives, earlier
bindings, nested unions, parameters and returns, explicit scopes, Like and
variadic annotations, tree structure bindings, async calls, cancellation, thread
isolation, object release, `Annotated` predicates, container sampling, and
aliases resolved after decoration. Negative cases still reject wrong values and
dimensions with useful beartype violations.

The proposal preserves the upstream ordering and sampling rules. A later
argument failure does not cause a search for a different earlier alternative.
Hidden state changes inside arbitrary predicates are not discovered; the
stateful runtime hint must expose the state hook. Completed transactions release
their state references and are ignored by subsequent checks using a copied
execution context; the upstream proposal includes regressions for both cases.

Local CPU runs do not establish CUDA coverage for the changed artifacts. The
handoff report and ExecPlan record interpreter versions, checks and availability
separately from earlier GPU evidence.

## Measure overhead

Run the same benchmark script in each normally installed environment:

```sh
/path/to/environment/bin/python tools/upstream/benchmark_transactions.py \
  --calls 20000 --repeats 7
/path/to/environment/bin/python tools/benchmark_runtime.py \
  --calls 10000 --repeats 5
```

The transaction benchmark verifies each case before timing it. An incorrect
baseline is recorded as `correct: false`; its failure is not presented as a
faster valid implementation. The synthetic plugin fixture supports both local
proposal interfaces solely to compare their bookkeeping using identical inputs.
The actual bearshape adapter exposes only the current proposed interface.

Compare original bearshape with rc0 and the first proposal, then optimized
bearshape with rc0 and the optimized proposal. PR #35 independently reduces
frame-discovery work; include it in both sides of the latter comparison to avoid
attributing that improvement to upstream. Record versions, source commits and
artifact hashes, and keep raw repeat samples. Timing has no CI threshold.

The owner requested further optimization before any upstream contact and has a
direct Zulip contact. Discussion material is prepared locally for the owner; no
message has been sent.
