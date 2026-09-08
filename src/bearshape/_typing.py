"""Static input families shared by backend TYPE_CHECKING branches."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from typing import Any, TypeAlias, TypeVar

  import numpy as np
  from numpy._typing import _NestedSequence
  from numpy.typing import NDArray

  UnsignedDtype: TypeAlias = np.bool_ | np.unsignedinteger[Any]
  IntegerDtype: TypeAlias = np.bool_ | np.integer[Any]
  RealDtype: TypeAlias = IntegerDtype | np.floating[Any]
  NumericDtype: TypeAlias = np.bool_ | np.number[Any]

  _Array = TypeVar("_Array")
  _Scalar = TypeVar("_Scalar")
  _Dtype = TypeVar("_Dtype", bound=np.generic)

  # NumPy __array__ alone does not establish convertibility to another backend.
  BackendLike: TypeAlias = (
    _Array
    | _Scalar
    | _Dtype
    | NDArray[_Dtype]
    | _NestedSequence[_Array | _Scalar | _Dtype | NDArray[_Dtype]]
  )
