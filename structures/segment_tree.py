"""Segment tree supporting range sum queries and point updates."""
from typing import List, Sequence, Union

Number = Union[int, float]


class SegmentTree:
    """Iterative (bottom-up) segment tree for range sums.

    Time Complexity:
        build: O(n)
        update / set: O(log n)
        range_sum: O(log n)
    Space Complexity: O(n)
    """

    def __init__(self, values: Sequence[Number]) -> None:
        self._size = len(values)
        self._tree: List[Number] = [0] * (2 * self._size)
        self._tree[self._size:] = list(values)
        for i in range(self._size - 1, 0, -1):
            self._tree[i] = self._tree[2 * i] + self._tree[2 * i + 1]

    def __len__(self) -> int:
        return self._size

    def _check(self, index: int) -> None:
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

    def __getitem__(self, index: int) -> Number:
        self._check(index)
        return self._tree[self._size + index]

    def set(self, index: int, value: Number) -> None:
        """Set the element at index (0-based) to value."""
        self._check(index)
        i = index + self._size
        self._tree[i] = value
        while i > 1:
            i //= 2
            self._tree[i] = self._tree[2 * i] + self._tree[2 * i + 1]

    def update(self, index: int, delta: Number) -> None:
        """Add delta to the element at index (0-based)."""
        self.set(index, self[index] + delta)

    def range_sum(self, left: int, right: int) -> Number:
        """Sum of elements in the inclusive range [left, right] (0-based)."""
        if left < 0 or right >= self._size or left > right:
            raise IndexError("Invalid range")
        total: Number = 0
        lo, hi = left + self._size, right + self._size + 1
        while lo < hi:
            if lo & 1:
                total += self._tree[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                total += self._tree[hi]
            lo //= 2
            hi //= 2
        return total
