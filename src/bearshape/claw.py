"""Import hook integration with ``beartype.claw``.

Since bearshape's frame-based memo works automatically with ``@beartype``,
you can use ``beartype.claw`` directly. This module provides a convenience
alias for discoverability::

    # In your package's __init__.py:
    from bearshape.claw import bearshape_this_package

    bearshape_this_package()

    # All subsequently imported submodules get @beartype automatically,
    # and bearshape array annotations are checked with cross-arg consistency.
"""

from __future__ import annotations

from beartype.claw import beartype_this_package as bearshape_this_package

__all__ = ["bearshape_this_package"]
