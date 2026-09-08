"""Integration regressions requiring the proposed beartype snapshot protocol.

Run explicitly with the patched upstream installed. These are real failures on
published rc0; they are neither skipped nor marked as expected failures.
"""

from __future__ import annotations

import asyncio
import gc
import weakref
from collections.abc import Callable

import numpy as np
import pytest
from beartype import BeartypeConf, beartype
from beartype.door import die_if_unbearable, is_bearable
from beartype.roar import (
  BeartypeCallHintParamViolation,
  BeartypeCallHintReturnViolation,
  BeartypeDoorHintViolation,
)

from bearshape import C, N, check, check_context
from bearshape._memo import get_memo
from bearshape.numpy import F32, F32Like


def array(size: int) -> np.ndarray:
  return np.ones(size, dtype=np.float32)


@pytest.mark.parametrize("mode", ["automatic", "explicit", "combined"])
def test_failed_alternative_discards_binding(mode: str) -> None:
  def choose(pair: tuple[F32[N], str] | tuple[F32[C], int], y: F32[N]) -> None:
    pass

  if mode == "combined":
    checked = check(conf=BeartypeConf())(choose)
  else:
    checked = beartype(choose)
    if mode == "explicit":
      checked = check(checked)
  checked((array(2), 1), array(3))
  with pytest.raises(BeartypeCallHintParamViolation):
    checked((array(2), "selected first"), array(3))


def test_selected_alternative_retains_binding() -> None:
  @beartype
  def choose(pair: tuple[F32[N], str] | tuple[F32[C], int], y: F32[C]) -> None:
    pass

  choose((array(2), 1), array(2))
  with pytest.raises(BeartypeCallHintParamViolation, match="expected 2 but got 3"):
    choose((array(2), 1), array(3))


def test_preserve_earlier_argument_bindings() -> None:
  @beartype
  def choose(
    first: F32[N], pair: tuple[F32[C], str] | tuple[F32[C], int], last: F32[N]
  ) -> None:
    pass

  choose(array(3), (array(2), 1), array(3))
  with pytest.raises(BeartypeCallHintParamViolation, match="expected 3 but got 4"):
    choose(array(3), (array(2), 1), array(4))


def test_nested_union_discards_selected_inner_alternative_on_outer_failure() -> None:
  hint = (
    tuple[tuple[F32[N], str] | tuple[F32[C], int], str] | tuple[tuple[F32[N], int], int]
  )
  with check_context():
    assert is_bearable(((array(2), 1), 1), hint)
    assert get_memo().single == {"N": 2}
    assert is_bearable(array(3), F32[C])


def test_all_alternatives_fail_without_poisoning_context() -> None:
  hint = tuple[F32[N], str] | tuple[F32[C], int]
  with check_context():
    assert not is_bearable((array(2), None), hint)
    assert get_memo().single == {}
    assert is_bearable(array(3), F32[N])
    assert is_bearable(array(4), F32[C])


def test_diagnostics_restore_state_and_explain_repeated_dimensions() -> None:
  hint = tuple[F32[N], F32[N]] | tuple[F32[C], str]
  with check_context():
    with pytest.raises(BeartypeDoorHintViolation, match="expected 2 but got 3"):
      die_if_unbearable((array(2), array(3)), hint)
    assert get_memo().single == {}
    assert is_bearable(array(4), F32[N])


def test_return_union_commits_only_selected_alternative() -> None:
  @beartype
  def choose() -> tuple[tuple[F32[N], str] | tuple[F32[C], int], F32[N]]:
    return (array(2), 1), array(3)

  choose()

  @beartype
  def wrong() -> tuple[tuple[F32[N], str] | tuple[F32[C], int], F32[C]]:
    return (array(2), 1), array(3)

  with pytest.raises(BeartypeCallHintReturnViolation, match="expected 2 but got 3"):
    wrong()


def test_like_alternatives_roll_back() -> None:
  hint = tuple[F32Like[N], str] | tuple[F32Like[C], int]
  with check_context():
    assert is_bearable(([1.0, 2.0], 1), hint)
    assert get_memo().single == {"C": 2}
    assert is_bearable([1.0, 2.0, 3.0], F32Like[N])


def test_variadic_alternatives_roll_back() -> None:
  hint = tuple[F32[~N], str] | tuple[F32[~C], int]
  with check_context():
    assert is_bearable((np.ones((2, 3), dtype=np.float32), 1), hint)
    assert get_memo().variadic == {"C": (False, (2, 3))}
    assert is_bearable(array(4), F32[~N])


def test_tree_structure_alternatives_roll_back() -> None:
  from bearshape import S, T
  from bearshape.optree import Tree

  hint = tuple[Tree[F32[N], T], str] | tuple[Tree[F32[C], S], int]
  with check_context():
    assert is_bearable(([array(2)], 1), hint)
    assert set(get_memo().structures) == {"S"}
    assert get_memo().single == {"C": 2}
    assert is_bearable({"new": array(3)}, Tree[F32[N], T])


def test_async_calls_keep_independent_bindings() -> None:
  @check
  @beartype
  async def choose(pair: tuple[F32[N], str] | tuple[F32[C], int], y: F32[N]) -> F32[N]:
    await asyncio.sleep(0)
    return y

  async def run() -> None:
    results = await asyncio.gather(*(choose((array(2), 1), array(i)) for i in (3, 4)))
    assert [len(result) for result in results] == [3, 4]

  asyncio.run(run())


def test_success_does_not_retain_array() -> None:
  @beartype
  def choose(pair: tuple[F32[N], str] | tuple[F32[C], int], y: F32[N]) -> None:
    pass

  def invoke() -> weakref.ReferenceType[np.ndarray]:
    y = array(3)
    ref = weakref.ref(y)
    choose((array(2), 1), y)
    return ref

  ref = invoke()
  gc.collect()
  assert ref() is None


@beartype
def _late_alias_choose(
  pair: tuple[_LateN, str] | tuple[_LateC, int], y: _LateN
) -> None:
  pass


_LateN = F32[N]
_LateC = F32[C]


def test_late_resolved_aliases() -> None:
  _late_alias_choose((array(2), 1), array(3))


@pytest.mark.parametrize("container", ["list", "dict"])
def test_union_nested_in_container(container: str) -> None:
  alternative = tuple[F32[N], str] | tuple[F32[C], int]
  value = (array(2), 1)
  if container == "list":
    hint, obj = list[alternative], [value]
  else:
    hint, obj = dict[str, alternative], {"item": value}
  with check_context():
    assert is_bearable(obj, hint)
    assert get_memo().single == {"C": 2}
    assert is_bearable(array(3), F32[N])


def test_annotated_predicate_rejection_rolls_back_shape() -> None:
  from typing import Annotated

  from beartype.vale import Is

  hint = (
    Annotated[tuple[F32[N], int], Is[lambda pair: pair[1] < 0]] | tuple[F32[C], int]
  )
  with check_context():
    assert is_bearable((array(2), 1), hint)
    assert get_memo().single == {"C": 2}


def test_sampled_union_value_is_evaluated_once() -> None:
  class Samples(list):
    reads = 0

    def __getitem__(self, index: int) -> object:
      self.reads += 1
      return super().__getitem__(index)

  samples = Samples([(array(2), 1)])
  with check_context():
    assert is_bearable(samples, list[tuple[F32[N], str] | tuple[F32[C], int]])
    assert samples.reads == 1
    assert get_memo().single == {"C": 2}


def _raise_value_error(_pair: object) -> bool:
  message = "validator failed"
  raise ValueError(message)


def _raise_cancellation(_pair: object) -> bool:
  raise asyncio.CancelledError


@pytest.mark.parametrize(
  "validator,exception_type",
  [(_raise_value_error, ValueError), (_raise_cancellation, asyncio.CancelledError)],
)
def test_exception_after_shape_binding_restores_context(
  validator: Callable[[object], bool], exception_type: type[BaseException]
) -> None:
  from typing import Annotated

  from beartype.vale import Is

  hint = Annotated[tuple[F32[N], int], Is[validator]] | tuple[F32[C], str]
  with check_context():
    assert is_bearable(array(7), F32[C])
    with pytest.raises(exception_type):
      is_bearable((array(2), 1), hint)
    assert get_memo().single == {"C": 7}


def test_interleaved_thread_transactions_keep_independent_contexts() -> None:
  from concurrent.futures import ThreadPoolExecutor
  from threading import Barrier

  barrier = Barrier(2)
  hint = tuple[F32[N], str] | tuple[F32[C], int]

  def worker(size: int) -> bool:
    with check_context():
      assert is_bearable((array(size), 1), hint)
      barrier.wait(timeout=5)
      assert get_memo().single == {"C": size}
      return is_bearable(array(size + 1), F32[N])

  with ThreadPoolExecutor(max_workers=2) as pool:
    assert all(pool.map(worker, (2, 7)))
