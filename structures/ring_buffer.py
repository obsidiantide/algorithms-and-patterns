"""Fixed-size Circular Buffer (Ring Buffer) implementation."""
from typing import Generic, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class RingBuffer(Generic[T]):
    """Fixed-capacity circular buffer with O(1) append, popleft, and indexing.

    Time Complexity:
        append: O(1)
        popleft: O(1)
        peek: O(1)
        getitem: O(1)
    Space Complexity: O(capacity)
    """

    def __init__(self, capacity: int, overwrite: bool = True) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.overwrite = overwrite
        self._buffer: List[Optional[T]] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self.capacity

    def append(self, item: T) -> None:
        """Append an item to the buffer, evicting oldest if full and overwrite is True."""
        if self.is_full():
            if not self.overwrite:
                raise OverflowError("RingBuffer is full")
            self._head = (self._head + 1) % self.capacity
        else:
            self._size += 1

        self._buffer[self._tail] = item
        self._tail = (self._tail + 1) % self.capacity

    def popleft(self) -> T:
        """Remove and return the oldest element from the buffer."""
        if self.is_empty():
            raise IndexError("popleft from empty RingBuffer")
        item = self._buffer[self._head]
        self._buffer[self._head] = None
        self._head = (self._head + 1) % self.capacity
        self._size -= 1
        return item  # type: ignore[return-value]

    def peek(self) -> T:
        """Return the oldest element without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty RingBuffer")
        return self._buffer[self._head]  # type: ignore[return-value]

    def __getitem__(self, index: int) -> T:
        """Retrieve element by 0-based offset from oldest (supports negative indexing)."""
        if index < -self._size or index >= self._size:
            raise IndexError("RingBuffer index out of range")
        if index < 0:
            index += self._size
        return self._buffer[(self._head + index) % self.capacity]  # type: ignore[return-value]

    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self._buffer[(self._head + i) % self.capacity]  # type: ignore[misc]

    def clear(self) -> None:
        """Clear all elements from the buffer."""
        self._buffer = [None] * self.capacity
        self._head = 0
        self._tail = 0
        self._size = 0
