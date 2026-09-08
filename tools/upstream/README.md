# Native union integration proposal

The `test_union_transactions.py` suite exercises the proposed beartype
`__beartype_snapshot__` protocol. It runs explicitly because the required
upstream change has not shipped. These tests are real failures on published
beartype `0.23.0rc0`; they have no skips or expected-failure markers. Passing
the normal rc0 CI suite does not prove this integration.

The bearshape adapter exposes one shared snapshot getter on its runtime-hint
metaclass. The getter captures the active memo's single dimensions, variadic
dimensions and tree structures, and returns a rollback callback. Existing leaf
validation remains necessary for rc0 and bare `isinstance` calls.

The local upstream proposal is based on beartype commit
`a2729e0e358bf963ee6f177e300ae08a622d05d6`; its tested patch commit is
`4aef992d1cd0a6d09fe5c3784523c44e0874b178`. Both identify themselves as
development `0.23.0rc1`. Neither that version string nor these instructions
imply upstream acceptance or publication. The patch is supplied separately for
maintainer review; it is not vendored into bearshape or applied at import time.

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
stateful runtime hint must expose the snapshot hook.

Local CPU runs do not establish CUDA coverage for the changed artifacts. The
handoff report and ExecPlan record interpreter versions, checks and availability
separately from earlier GPU evidence.
