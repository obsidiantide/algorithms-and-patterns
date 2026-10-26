"""Binary min/max heap implementation with type hints."""
from typing import Generic, Iterable, List, Optional, TypeVar

T = TypeVar("T")


class BinaryHeap(Generic[T]):
    """Binary heap supporting min-heap or max-heap ordering."""

    def __init__(self, items: Optional[Iterable[T]] = None, *, min_heap: bool = True) -> None:
        self.min_heap = min_heap
        self._data: List[T] = list(items) if items is not None else []
        if self._data:
            self._heapify()

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def _prioritizes(self, a: T, b: T) -> bool:
        return (a < b) if self.min_heap else (a > b)

    def peek(self) -> T:
        """Return root element without removing it."""
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    def push(self, item: T) -> None:
        """Push an element onto the heap."""
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> T:
        """Remove and return the root element."""
        if not self._data:
            raise IndexError("pop from empty heap")
        root = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return root

    def pushpop(self, item: T) -> T:
        """Push item and return popped root element."""
        if self._data and self._prioritizes(self._data[0], item):
            item, self._data[0] = self._data[0], item
            self._sift_down(0)
        return item

    def _heapify(self) -> None:
        for idx in reversed(range(len(self._data) // 2)):
            self._sift_down(idx)

    def _sift_up(self, idx: int) -> None:
        parent = (idx - 1) // 2
        while idx > 0 and self._prioritizes(self._data[idx], self._data[parent]):
            self._data[idx], self._data[parent] = self._data[parent], self._data[idx]
            idx, parent = parent, (parent - 1) // 2

    def _sift_down(self, idx: int) -> None:
        n = len(self._data)
        while True:
            best, left, right = idx, 2 * idx + 1, 2 * idx + 2
            if left < n and self._prioritizes(self._data[left], self._data[best]):
                best = left
            if right < n and self._prioritizes(self._data[right], self._data[best]):
                best = right
            if best == idx:
                break
            self._data[idx], self._data[best] = self._data[best], self._data[idx]
            idx = best


class MinHeap(BinaryHeap[T]):
    """Binary min-heap where smallest element is at the root."""
    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        super().__init__(items, min_heap=True)


class MaxHeap(BinaryHeap[T]):
    """Binary max-heap where largest element is at the root."""
    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        super().__init__(items, min_heap=False)
