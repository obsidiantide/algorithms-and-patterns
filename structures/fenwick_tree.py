"""Binary Indexed Tree (Fenwick Tree) implementation for prefix and range sum queries."""
from typing import List, Sequence, Union

Number = Union[int, float]


class FenwickTree:
    """Binary Indexed Tree (Fenwick Tree) supporting prefix and range queries.

    Provides O(log n) point updates and range sum queries with O(n) construction.

    Time Complexity:
        build: O(n)
        add / set: O(log n)
        prefix_sum: O(log n)
        range_sum: O(log n)
        getitem: O(log n)
    Space Complexity: O(n)
    """

    def __init__(self, size_or_values: Union[int, Sequence[Number]]) -> None:
        if isinstance(size_or_values, int):
            if size_or_values < 0:
                raise ValueError("Size must be non-negative")
            self._size = size_or_values
            self._tree: List[Number] = [0] * (self._size + 1)
        else:
            values = list(size_or_values)
            self._size = len(values)
            self._tree = [0] * (self._size + 1)
            for i, val in enumerate(values, start=1):
                self._tree[i] += val
                parent = i + (i & -i)
                if parent <= self._size:
                    self._tree[parent] += self._tree[i]

    def __len__(self) -> int:
        return self._size

    def _query(self, i: int) -> Number:
        total: Number = 0
        while i > 0:
            total += self._tree[i]
            i -= i & -i
        return total

    def add(self, index: int, delta: Number) -> None:
        """Add delta to the element at index (0-based)."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        i = index + 1
        while i <= self._size:
            self._tree[i] += delta
            i += i & -i

    def prefix_sum(self, index: int) -> Number:
        """Compute the sum of elements from index 0 to index inclusive (0-based)."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        return self._query(index + 1)

    def range_sum(self, left: int, right: int) -> Number:
        """Compute the sum of elements in range [left, right] inclusive (0-based)."""
        if left < 0 or left >= self._size or right < 0 or right >= self._size:
            raise IndexError("Index out of range")
        if left > right:
            raise ValueError("left index cannot be greater than right index")
        return self._query(right + 1) - self._query(left)

    def __getitem__(self, index: int) -> Number:
        """Retrieve element at 0-based index (supports negative indexing)."""
        if index < -self._size or index >= self._size:
            raise IndexError("Index out of range")
        if index < 0:
            index += self._size
        return self.range_sum(index, index)

    def set(self, index: int, value: Number) -> None:
        """Update the element at index to a new value."""
        if index < -self._size or index >= self._size:
            raise IndexError("Index out of range")
        if index < 0:
            index += self._size
        current = self[index]
        self.add(index, value - current)

    def to_list(self) -> List[Number]:
        """Return list of all elements in the Fenwick tree."""
        return [self[i] for i in range(self._size)]
