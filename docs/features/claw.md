---
description: Package-wide instrumentation with beartype.claw — no per-function decorators.
---

<!-- markdownlint-disable-file MD046 -->

# Import Hook (beartype.claw)

If you want package-wide instrumentation rather than decorating individual
functions, use `beartype.claw` or bearshape's thin wrapper around it.

## Usage

=== "Via bearshape"

    ```python
    from bearshape.claw import bearshape_this_package
    bearshape_this_package()
    ```

=== "Via beartype directly"

    ```python
    from beartype.claw import beartype_this_package
    beartype_this_package()
    ```

`bearshape_this_package()` is a semantic wrapper around
`beartype.claw.beartype_this_package()`. Runtime behavior is the same.

## What it gives you

Once called in `your_package.__init__`, all subsequently imported submodules in
that package are instrumented as if their annotated callables had been decorated
with `@beartype`.

```python
# your_package/__init__.py
from bearshape.claw import bearshape_this_package
bearshape_this_package()

# your_package/model.py
from bearshape import N, C
from bearshape.numpy import F32

def forward(x: F32[N, C]) -> F32[N, C]:
  ...
```

Because bearshape integrates through standard beartype validators, the usual
cross-argument dimension semantics still apply.

## Configuration

Pass a `BeartypeConf` to customize the checking behavior:

```python
from beartype import BeartypeConf
from bearshape.claw import bearshape_this_package

bearshape_this_package(conf=BeartypeConf(
  is_color=False,
))
```

## When to use

<!-- markdownlint-disable MD013 -->

| Approach | Best for | | --------------------------------------- |
---------------------------------------- | | `@beartype` per function |
Fine-grained control, specific functions | | `beartype.claw` /
`bearshape_this_package` | Entire packages, library-wide checking |

<!-- markdownlint-enable MD013 -->
