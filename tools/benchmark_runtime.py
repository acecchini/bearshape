"""Measure representative runtime costs without imposing a timing gate."""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import timeit
from collections.abc import Callable
from functools import partial
from importlib.metadata import version

import numpy as np
from beartype import BeartypeConf, beartype
from beartype.roar import BeartypeCallHintParamViolation

import bearshape
from bearshape import N, Value, check
from bearshape.numpy import F32, F32Like
from bearshape.optree import Tree


def bare(value: np.ndarray) -> np.ndarray:
  return value


@beartype
def native(value: np.ndarray) -> np.ndarray:
  return value


@beartype
def strict(value: F32[N]) -> F32[N]:
  return value


@check(conf=BeartypeConf())
def explicit(value: F32[N]) -> F32[N]:
  return value


@beartype
def like(value: F32Like[N]) -> object:
  return value


@check(conf=BeartypeConf())
def value_dimension(size: int, value: F32[Value("size")]) -> F32[Value("size")]:  # noqa: ARG001
  """The size argument is consumed by the Value annotations."""
  return value


@check(conf=BeartypeConf())
def nested(value: F32[N]) -> F32[N]:
  return strict(value)


@beartype
def tree(value: Tree[F32[N]]) -> Tree[F32[N]]:
  return value


def diagnostic(value: np.ndarray) -> None:
  try:
    strict(value)
  except BeartypeCallHintParamViolation:
    return
  message = "Benchmark's invalid input unexpectedly passed"
  raise AssertionError(message)


def measure(
  label: str, call: Callable[[], object], *, calls: int, repeats: int
) -> dict[str, str | int | float]:
  call()
  samples = [
    seconds * 1_000_000 / calls
    for seconds in timeit.repeat(call, number=calls, repeat=repeats)
  ]
  return {
    "case": label,
    "calls_per_repeat": calls,
    "repeats": repeats,
    "median_us": statistics.median(samples),
    "min_us": min(samples),
    "max_us": max(samples),
  }


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--calls", type=int, default=10_000)
  parser.add_argument("--repeats", type=int, default=5)
  args = parser.parse_args()
  if args.calls < 1 or args.repeats < 1:
    parser.error("calls and repeats must be positive")
  results = []
  for size in (3, 1_000_000):
    array = np.ones(size, dtype=np.float32)
    results.extend(
      measure(
        f"{function.__name__}/{size}",
        partial(function, array),
        calls=args.calls,
        repeats=args.repeats,
      )
      for function in (bare, native, strict, explicit, like, nested)
    )
    results.append(
      measure(
        f"value/{size}",
        partial(value_dimension, size, array),
        calls=args.calls,
        repeats=args.repeats,
      )
    )
    sequence = array.tolist()
    results.append(
      measure(
        f"like-sequence/{size}",
        partial(like, sequence),
        calls=min(args.calls, max(5, 5_000_000 // size)),
        repeats=args.repeats,
      )
    )
    invalid = np.ones(size, dtype=np.int32)
    results.append(
      measure(
        f"diagnostic/{size}",
        partial(diagnostic, invalid),
        calls=min(args.calls, 1_000),
        repeats=args.repeats,
      )
    )
  for leaves in (1, 100):
    arrays = [np.ones(3, dtype=np.float32) for _ in range(leaves)]
    results.append(
      measure(
        f"tree/{leaves}",
        partial(tree, arrays),
        calls=max(1, args.calls // leaves),
        repeats=args.repeats,
      )
    )
  evidence = {
    "python": sys.version,
    "platform": platform.platform(),
    "machine": platform.machine(),
    "bearshape_origin": bearshape.__file__,
    "versions": {
      package: version(package)
      for package in ("bearshape", "beartype", "numpy", "optree")
    },
    "results": results,
  }
  json.dump(evidence, sys.stdout, indent=2)
  sys.stdout.write("\n")


if __name__ == "__main__":
  main()
