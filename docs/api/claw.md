---
description: Alias for beartype.claw for package-wide instrumentation.
---

# `bearshape.claw`

`bearshape.claw` contains one public helper:

```python
from bearshape.claw import bearshape_this_package
```

## `bearshape_this_package`

`bearshape_this_package(*, conf: BeartypeConf = BeartypeConf()) -> None`

It is a direct alias for `beartype.claw.beartype_this_package`, preserving
upstream caller-package discovery and configuration.

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
