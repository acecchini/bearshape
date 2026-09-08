"""Exercise an installed bearshape wheel without any optional backend.

Run with the isolated Python from a fresh environment containing only the wheel
and its declared runtime dependencies: python -I tools/smoke_minimal.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from importlib.metadata import version
from importlib.util import find_spec
from pathlib import Path

from beartype import beartype
from beartype.roar import (
  BeartypeCallHintParamViolation,
  BeartypeCallHintReturnViolation,
)

import bearshape
from bearshape import DtypeSpec, N, make_array_type

BACKENDS = ("numpy", "jax", "torch", "cupy", "optree")


@dataclass
class CustomArray:
  shape: tuple[int, ...]
  dtype: str = "float32"


FloatArray = make_array_type(
  CustomArray, DtypeSpec("FloatArray", frozenset({"float32"}))
)


@beartype
def pair(x: FloatArray[N], _y: FloatArray[N]) -> FloatArray[N]:
  return x


@beartype
def wrong_return(x: FloatArray[N]) -> FloatArray[N]:
  return CustomArray((x.shape[0] + 1,))


def _expect_param_failure(x: CustomArray, bad: CustomArray) -> None:
  try:
    pair(x, bad)
  except BeartypeCallHintParamViolation:
    pass
  else:
    sys.exit("Custom array metadata mismatch was accepted")


def main() -> None:
  location = Path(bearshape.__file__).resolve()
  if not location.is_relative_to(Path(sys.prefix)):
    sys.exit(f"Imported bearshape outside the consumer environment: {location}")
  if present := [backend for backend in BACKENDS if find_spec(backend) is not None]:
    sys.exit(f"Minimal consumer unexpectedly has optional backends: {present}")
  x = CustomArray((3,))
  if pair(x, CustomArray((3,))) is not x:
    sys.exit("Validation replaced the custom array argument")
  _expect_param_failure(x, CustomArray((4,)))
  _expect_param_failure(x, CustomArray((3,), "int32"))
  try:
    wrong_return(x)
  except BeartypeCallHintReturnViolation:
    pass
  else:
    sys.exit("Custom array return mismatch was accepted")
  if imported := sorted(set(BACKENDS).intersection(sys.modules)):
    sys.exit(f"Root/custom-array validation imported optional backends: {imported}")
  json.dump(
    {
      "bearshape": version("bearshape"),
      "beartype": version("beartype"),
      "python": sys.version,
      "module": str(location),
      "optional_backends": [],
    },
    sys.stdout,
    indent=2,
  )
  sys.stdout.write("\n")


if __name__ == "__main__":
  main()
