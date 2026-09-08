"""Measure checked union behavior; label incorrect baselines instead of timing them."""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import timeit
from collections.abc import Callable
from importlib.metadata import version

import numpy as np
from beartype import BeartypeConf, beartype
from beartype.door import is_bearable
from beartype.roar import BeartypeCallHintParamViolation

from bearshape import C, N, check, check_context
from bearshape._memo import get_memo
from bearshape.numpy import F32


@beartype
def strict(value: F32[N]) -> F32[N]:
  return value


@check(conf=BeartypeConf())
def explicit(value: F32[N]) -> F32[N]:
  return value


@beartype
def union(_pair: tuple[F32[N], str] | tuple[F32[C], int], _last: F32[N]) -> None:
  pass


@check(conf=BeartypeConf())
def union_explicit(
  _pair: tuple[F32[N], str] | tuple[F32[C], int], _last: F32[N]
) -> None:
  pass


@beartype
def native(value: int | str) -> int | str:
  return value


@beartype
def forward(value: LaterNative) -> object:
  return value


@beartype
def unselected(value: int | NeverResolved) -> object:  # noqa: F821
  return value


class LaterNative:
  pass


_bindings: dict[str, int] = {}


class _State:
  def snapshot(self) -> dict[str, int]:
    return _bindings.copy()

  def restore(self, old: dict[str, int]) -> None:
    _bindings.clear()
    _bindings.update(old)


_state = _State()


def _get_state() -> _State:
  return _state


def _old_snapshot() -> Callable[[], None]:
  # The fixture supports both local proposals for matched comparisons.
  before = _state.snapshot()
  return lambda: _state.restore(before)


class _StatefulMeta(type):
  __beartype_state__ = staticmethod(_get_state)
  __beartype_snapshot__ = staticmethod(_old_snapshot)

  def __instancecheck__(cls, value: object) -> bool:
    if not isinstance(value, list):
      return False
    return _bindings.setdefault(cls.__name__, len(value)) == len(value)


class StateA(metaclass=_StatefulMeta):
  pass


class StateB(metaclass=_StatefulMeta):
  pass


@beartype
def plugin_leaf(_value: StateA) -> None:
  pass


@beartype
def plugin_union(_value: tuple[StateA, str] | tuple[StateB, int]) -> None:
  pass


def plugin_second() -> None:
  plugin_union(([1], 1))
  if _bindings != {"StateB": 1}:
    msg = "Plugin union retained rejected state"
    raise AssertionError(msg)


_array2 = np.ones(2, dtype=np.float32)
_array3 = np.ones(3, dtype=np.float32)
_union_hint = tuple[F32[N], str] | tuple[F32[C], int]
_nested_hint = tuple[_union_hint, str] | tuple[tuple[F32[N], int], int]


def all_failed() -> None:
  with check_context():
    if is_bearable((_array2, None), _union_hint):
      msg = "Invalid union accepted"
      raise AssertionError(msg)
    if get_memo().single:
      msg = "Failed union retained state"
      raise AssertionError(msg)


def nested() -> None:
  with check_context():
    if not is_bearable(((_array2, 1), 1), _nested_hint):
      msg = "Valid nested union rejected"
      raise AssertionError(msg)
    if get_memo().single != {"N": 2}:
      msg = "Nested union retained rejected state"
      raise AssertionError(msg)


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--calls", type=int, default=20_000)
  parser.add_argument("--repeats", type=int, default=7)
  args = parser.parse_args()
  if args.calls < 1 or args.repeats < 1:
    parser.error("calls and repeats must be positive")
  later = LaterNative()
  cases: dict[str, Callable[[], object]] = {
    "native": lambda: native(1),
    "forward-resolved-stateless": lambda: forward(later),
    "forward-unselected": lambda: unselected(1),
    "plugin-leaf": lambda: plugin_leaf([1]),
    "plugin-union-second": plugin_second,
    "strict": lambda: strict(_array2),
    "explicit": lambda: explicit(_array2),
    "union-first": lambda: union((_array2, "yes"), _array2),
    "union-second": lambda: union((_array2, 1), _array3),
    "union-explicit-second": lambda: union_explicit((_array2, 1), _array3),
    "union-all-failed": all_failed,
    "union-nested": nested,
  }
  results = []
  for name, call in cases.items():
    _bindings.clear()
    try:
      call()
    except (AssertionError, BeartypeCallHintParamViolation) as error:
      results.append({"case": name, "correct": False, "reason": str(error)})
      continue
    samples = [
      seconds * 1_000_000 / args.calls
      for seconds in timeit.repeat(call, number=args.calls, repeat=args.repeats)
    ]
    results.append({
      "case": name,
      "correct": True,
      "median_us": statistics.median(samples),
      "samples_us": samples,
    })
  evidence = {
    "python": sys.version,
    "platform": platform.platform(),
    "versions": {p: version(p) for p in ("bearshape", "beartype", "numpy")},
    "calls": args.calls,
    "repeats": args.repeats,
    "results": results,
  }
  json.dump(evidence, sys.stdout, indent=2)
  sys.stdout.write("\n")


if __name__ == "__main__":
  main()
