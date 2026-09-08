"""Tests for _memo.py — frame-based and explicit memo management."""

from __future__ import annotations

import threading

import numpy as np
import pytest
from beartype import beartype
from beartype.roar import BeartypeCallHintParamViolation

from bearshape import C, N, Value
from bearshape._memo import ShapeMemo, get_memo, pop_memo, push_memo
from bearshape.numpy import F32


class TestExplicitMemo:
  def test_push_pop(self) -> None:
    memo = push_memo()
    assert isinstance(memo, ShapeMemo)
    assert memo.single == {}
    pop_memo()

  def test_nested_push_pop(self) -> None:
    outer = push_memo()
    outer.single["N"] = 10
    inner = push_memo()
    # Inner memo is independent
    assert inner.single == {}
    inner.single["N"] = 5
    pop_memo()
    # Outer is restored
    assert outer.single["N"] == 10
    pop_memo()

  def test_explicit_takes_priority(self) -> None:
    memo = push_memo()
    # get_memo should return the explicit one
    got = get_memo(_depth=0)
    assert got is memo
    pop_memo()


class TestFrameBasedMemo:
  def test_plain_is_bearable_uses_checker_frame(
    self, monkeypatch: pytest.MonkeyPatch
  ) -> None:
    """Plain is_bearable() should anchor memos to the generated checker frame."""
    from beartype.door import is_bearable

    import bearshape._array_types as array_types
    import bearshape._memo as memo_mod

    seen_frames: list[str | None] = []
    original_get_memo = array_types.get_memo

    def tracked_get_memo(*args: object, **kwargs: object) -> ShapeMemo:
      frame = memo_mod._find_beartype_wrapper_frame(_depth=2)
      seen_frames.append(None if frame is None else frame.f_code.co_name)
      return original_get_memo(*args, **kwargs)

    monkeypatch.setattr(array_types, "get_memo", tracked_get_memo)

    assert is_bearable(np.ones((3,), dtype=np.float32), F32[N])
    assert any(
      name is not None and name.startswith("__beartype_checker_")
      for name in seen_frames
    )

  def test_sequential_calls_get_fresh_memos(self) -> None:
    """Calling the same function twice should not reuse stale bindings."""

    @beartype
    def g(x: F32[N]) -> F32[N]:
      return x

    # First call: N=3
    g(np.ones((3,), dtype=np.float32))
    # Second call: N=7 — must NOT fail against N=3
    g(np.ones((7,), dtype=np.float32))
    # Third call: N=1
    g(np.ones((1,), dtype=np.float32))

  def test_repeated_boolean_calls_have_independent_memos(self) -> None:
    from beartype.door import is_bearable

    for size in range(1, 100):
      array = np.ones(size, dtype=np.float32)
      assert is_bearable((array, array), tuple[F32[N], F32[N]])

  def test_sequential_cross_arg(self) -> None:
    """Sequential calls with multiple args each get independent memos."""

    @beartype
    def f(x: F32[N, C], y: F32[N, C]) -> F32[N, C]:
      return x + y

    f(np.ones((2, 5), dtype=np.float32), np.ones((2, 5), dtype=np.float32))
    f(np.ones((10, 20), dtype=np.float32), np.ones((10, 20), dtype=np.float32))

  def test_nested_calls_independent(self) -> None:
    """Nested function calls get their own memos."""

    @beartype
    def inner(x: F32[N]) -> F32[N]:
      return x * 2

    @beartype
    def outer(x: F32[N, C], y: F32[N]) -> F32[N]:
      return inner(y)

    result = outer(np.ones((4, 3), dtype=np.float32), np.ones((4,), dtype=np.float32))
    assert result.shape == (4,)

  def test_cross_arg_mismatch_detected(self) -> None:
    @beartype
    def f(x: F32[N], y: F32[N]) -> F32[N]:
      return x + y

    with pytest.raises(BeartypeCallHintParamViolation):
      f(np.ones((3,), dtype=np.float32), np.ones((5,), dtype=np.float32))

  def test_nested_plain_value_return_uses_nearest_wrapper_scope(self) -> None:
    """Nested plain @beartype calls must resolve Value(...) from the right frame."""

    @beartype
    def inner(size: int) -> F32[Value("size")]:  # type: ignore[valid-type]
      return np.ones(size, dtype=np.float32)

    @beartype
    def outer(size: int) -> F32[Value("size")]:  # type: ignore[valid-type]
      inner(size + 2)
      return np.ones(size, dtype=np.float32)

    result = outer(4)
    assert result.shape == (4,)

  def test_async_plain_value_return_uses_wrapper_scope(self) -> None:
    """Async plain @beartype must keep Value(...) bound to the wrapper scope."""
    import asyncio

    @beartype
    async def f(size: int) -> F32[Value("size")]:  # type: ignore[valid-type]
      return np.ones(size, dtype=np.float32)

    result = asyncio.run(f(4))
    assert result.shape == (4,)


class TestThreadSafety:
  def test_threads_have_independent_memos(self) -> None:
    """Each thread should have its own memo."""
    results: list[bool] = []
    errors: list[str] = []

    @beartype
    def f(x: F32[N]) -> F32[N]:
      return x

    def worker(size: int) -> None:
      try:
        f(np.ones((size,), dtype=np.float32))
        results.append(True)
      except Exception as e:  # noqa: BLE001
        errors.append(str(e))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(1, 6)]
    for t in threads:
      t.start()
    for t in threads:
      t.join()

    assert len(errors) == 0, f"Thread errors: {errors}"
    assert len(results) == 5


class TestMemoEdgeCases:
  def test_bindings_str_empty(self) -> None:
    from bearshape._memo import bindings_str

    memo = ShapeMemo()
    assert bindings_str(memo) == ""

  def test_bindings_str_with_structures(self) -> None:
    from bearshape._memo import bindings_str

    memo = ShapeMemo(single={"N": 3}, structures={"T": "some_spec"})
    formatted = bindings_str(memo)
    assert "N=3" in formatted
    # structures are not included in bindings_str
    assert "T" not in formatted

  def test_pop_empty_is_safe(self) -> None:
    from bearshape._memo import _explicit_stack, pop_memo

    # Ensure stack is empty, then verify pop on empty doesn't corrupt state
    assert _explicit_stack.get() == ()
    pop_memo()
    assert _explicit_stack.get() == ()

  def test_get_memo_without_explicit_returns_frame_based(self) -> None:
    """Without explicit stack, get_memo should use frame detection."""
    memo = get_memo(_depth=0)
    assert isinstance(memo, ShapeMemo)

  def test_many_sequential_calls_no_leak(self) -> None:
    """Rapidly calling the same function many times shouldn't leak memos."""

    @beartype
    def f(x: F32[N]) -> F32[N]:
      return x

    for i in range(1, 50):
      f(np.ones(i, dtype=np.float32))


class TestIndependentCheckLifetime:
  @pytest.mark.parametrize("kind", ["strict", "like", "tree"])
  def test_failed_composite_does_not_poison_reused_object(self, kind: str) -> None:
    from beartype.door import is_bearable

    from bearshape.numpy import F32Like

    if kind == "tree":
      pytest.importorskip("optree")
      from bearshape.optree import Tree

      hint = Tree[F32[N]]
    else:
      hint = F32[N] if kind == "strict" else F32Like[N]

    a = np.ones(2, dtype=np.float32)
    b = np.ones(3, dtype=np.float32)
    assert not is_bearable((a, b), tuple[hint, hint])
    for _ in range(3):
      assert is_bearable(b, hint)
    assert is_bearable(a, hint)

  @pytest.mark.parametrize("kind", ["strict", "like", "tree"])
  def test_boolean_failure_releases_array(self, kind: str) -> None:
    import gc
    import weakref

    from beartype.door import is_bearable

    from bearshape.numpy import F32Like

    if kind == "tree":
      pytest.importorskip("optree")
      from bearshape.optree import Tree

      hint = Tree[F32[N]]
    else:
      hint = F32[N] if kind == "strict" else F32Like[N]

    def fail_once() -> weakref.ReferenceType[np.ndarray]:
      a = np.ones(2, dtype=np.float32)
      b = np.ones(3, dtype=np.float32)
      reference = weakref.ref(b)
      assert not is_bearable((a, b), tuple[hint, hint])
      return reference

    reference = fail_once()
    gc.collect()
    assert reference() is None

  def test_door_diagnostic_and_subsequent_check(self) -> None:
    from beartype.door import die_if_unbearable, is_bearable
    from beartype.roar import BeartypeDoorHintViolation

    a = np.ones(2, dtype=np.float32)
    b = np.ones(3, dtype=np.float32)
    with pytest.raises(BeartypeDoorHintViolation, match="expected 2 but got 3"):
      die_if_unbearable((a, b), tuple[F32[N], F32[N]])
    assert is_bearable(b, F32[N])

  def test_failed_check_does_not_follow_object_mutation(self) -> None:
    from beartype.door import is_bearable

    a = np.ones(2, dtype=np.float32)
    b = np.ones(6, dtype=np.float32)
    assert not is_bearable((a, b), tuple[F32[N], F32[N]])
    b.resize((2, 3))
    assert is_bearable(b, F32[N, C])
    b.resize((6,))
    assert is_bearable(b, F32[N])

  def test_interleaved_thread_failures_remain_independent(self) -> None:
    from concurrent.futures import ThreadPoolExecutor

    from beartype.door import is_bearable

    barrier = threading.Barrier(2)

    def worker(size: int) -> bool:
      a = np.ones(size, dtype=np.float32)
      b = np.ones(size + 1, dtype=np.float32)
      assert not is_bearable((a, b), tuple[F32[N], F32[N]])
      barrier.wait(timeout=5)
      return is_bearable(b, F32[N])

    with ThreadPoolExecutor(max_workers=2) as pool:
      assert all(pool.map(worker, (2, 7)))


class TestStateProtocol:
  def test_shared_getter_restores_the_active_context(self) -> None:
    from bearshape import check_context

    getter = F32[N].__beartype_state__
    assert getter is F32[C].__beartype_state__
    with check_context():
      memo = get_memo()
      memo.single["earlier"] = 7
      state = getter()
      assert state is memo
      snapshot = state.snapshot()
      assert isinstance(np.ones(2, dtype=np.float32), F32[N])
      memo.variadic["axes"] = (False, (2, 3))
      memo.structures["tree"] = ("leaf",)
      state.restore(snapshot)
      assert memo.single == {"earlier": 7}
      assert memo.variadic == {}
      assert memo.structures == {}
