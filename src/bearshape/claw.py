"""Import hook integration with ``beartype.claw``.

Since bearshape's frame-based memo works automatically with ``@beartype``,
you can use ``beartype.claw`` directly. This module provides a convenience
wrapper for discoverability::

    # In your package's __init__.py:
    from bearshape.claw import bearshape_this_package

    bearshape_this_package()

    # All subsequently imported submodules get @beartype automatically,
    # and bearshape array annotations are checked with cross-arg consistency.
"""

from __future__ import annotations

from beartype import BeartypeConf

__all__ = ["bearshape_this_package"]
from beartype.claw import beartype_this_package as _beartype_this_package


def bearshape_this_package(*, conf: BeartypeConf = BeartypeConf()) -> None:
  """Instrument the calling package with ``@beartype`` for runtime checking.

  This is a thin wrapper around ``beartype.claw.beartype_this_package``
  that exists as a semantic entry point for bearshape users.
  """
  _beartype_this_package(conf=conf)
