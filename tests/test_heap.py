"""Unit tests for binary min/max heap."""
import pytest
from structures.heap import MinHeap, MaxHeap, BinaryHeap


def test_min_heap_operations():
    heap = MinHeap()
    for val in [5, 3, 8, 1, 2, 9]:
        heap.push(val)
    assert len(heap) == 6
    assert bool(heap) is True
    assert [heap.pop() for _ in range(len(heap))] == [1, 2, 3, 5, 8, 9]
    assert len(heap) == 0
    assert bool(heap) is False


def test_min_heap_heapify():
    items = [10, 4, 15, 2, 1, 8]
    heap = MinHeap(items)
    assert heap.peek() == 1
    assert [heap.pop() for _ in range(len(items))] == [1, 2, 4, 8, 10, 15]


def test_max_heap():
    heap = MaxHeap([5, 1, 12, 7, 3])
    assert heap.peek() == 12
    assert [heap.pop() for _ in range(5)] == [12, 7, 5, 3, 1]


def test_empty_heap_raises():
    heap = MinHeap()
    with pytest.raises(IndexError):
        heap.peek()
    with pytest.raises(IndexError):
        heap.pop()


def test_pushpop():
    heap = MinHeap([3, 5, 7])
    assert heap.pushpop(1) == 1
    assert heap.peek() == 3
    assert heap.pushpop(4) == 3
    assert heap.peek() == 4
    assert [heap.pop() for _ in range(len(heap))] == [4, 5, 7]


def test_binary_heap_with_tuples():
    pairs = [(2, "b"), (1, "a"), (3, "c")]
    heap = BinaryHeap(pairs, min_heap=True)
    assert [heap.pop() for _ in range(3)] == [(1, "a"), (2, "b"), (3, "c")]
