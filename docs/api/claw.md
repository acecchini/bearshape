---
description: Thin wrapper around beartype.claw for package-wide instrumentation.
---

# `bearshape.claw`

`bearshape.claw` contains one public helper:

```python
from bearshape.claw import bearshape_this_package
```

## `bearshape_this_package`

`bearshape_this_package(*, conf: BeartypeConf = BeartypeConf()) -> None`

It forwards directly to `beartype.claw.beartype_this_package`, but gives
bearshape users a semantic entry point that matches the rest of the library.

### Example

```python
# your_package/__init__.py
from bearshape.claw import bearshape_this_package

bearshape_this_package()
```

All subsequently imported submodules in `your_package` are instrumented with
beartype, so bearshape array annotations start working there automatically.

### Custom configuration

```python
from beartype import BeartypeConf
from bearshape.claw import bearshape_this_package

bearshape_this_package(conf=BeartypeConf(
  is_color=False,
))
```
