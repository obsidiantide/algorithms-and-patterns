"""Unit tests for RingBuffer."""
import pytest
from structures.ring_buffer import RingBuffer


def test_init_and_validation():
    rb = RingBuffer(3)
    assert len(rb) == 0 and rb.is_empty() and not rb.is_full() and not rb
    with pytest.raises(ValueError, match="Capacity must be positive"):
        RingBuffer(0)
    with pytest.raises(ValueError, match="Capacity must be positive"):
        RingBuffer(-1)


def test_append_and_fifo_popleft():
    rb = RingBuffer(3)
    rb.append("a")
    rb.append("b")
    assert len(rb) == 2 and bool(rb) and rb.peek() == "a"
    assert rb.popleft() == "a" and rb.popleft() == "b" and rb.is_empty()
    with pytest.raises(IndexError, match="popleft from empty RingBuffer"):
        rb.popleft()
    with pytest.raises(IndexError, match="peek from empty RingBuffer"):
        rb.peek()


def test_overwrite_behavior():
    rb = RingBuffer(3, overwrite=True)
    for v in (1, 2, 3):
        rb.append(v)
    assert rb.is_full()
    rb.append(4)
    assert len(rb) == 3 and list(rb) == [2, 3, 4] and rb.peek() == 2
    rb.append(5)
    assert list(rb) == [3, 4, 5]


def test_no_overwrite_overflow():
    rb = RingBuffer(2, overwrite=False)
    rb.append(10)
    rb.append(20)
    assert rb.is_full()
    with pytest.raises(OverflowError, match="RingBuffer is full"):
        rb.append(30)
    assert list(rb) == [10, 20]


def test_indexing_and_iteration():
    rb = RingBuffer(3)
    for c in ("x", "y", "z"):
        rb.append(c)
    rb.append("w")  # Overwrites 'x' -> ['y', 'z', 'w']
    assert rb[0] == "y" and rb[1] == "z" and rb[2] == "w"
    assert rb[-1] == "w" and rb[-3] == "y"
    with pytest.raises(IndexError, match="RingBuffer index out of range"):
        _ = rb[3]
    with pytest.raises(IndexError, match="RingBuffer index out of range"):
        _ = rb[-4]


def test_clear():
    rb = RingBuffer(2)
    rb.append(1)
    rb.append(2)
    rb.clear()
    assert len(rb) == 0 and rb.is_empty()
    rb.append(3)
    assert rb.popleft() == 3
