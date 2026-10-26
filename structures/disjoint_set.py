"""Disjoint Set Union (Union-Find) data structure with path compression and union by rank."""
from typing import Dict, Generic, Iterable, List, Optional, Set, TypeVar

T = TypeVar("T")


class DisjointSet(Generic[T]):
    """Disjoint Set (Union-Find) data structure supporting near O(1) operations.

    Uses path compression and union by rank (inverse Ackermann time complexity).
    """

    def __init__(self, elements: Optional[Iterable[T]] = None) -> None:
        self._parent: Dict[T, T] = {}
        self._rank: Dict[T, int] = {}
        self._num_sets: int = 0
        if elements is not None:
            for elem in elements:
                self.add(elem)

    def __len__(self) -> int:
        """Return the total number of tracked elements."""
        return len(self._parent)

    def __contains__(self, item: T) -> bool:
        """Check if an element exists in the disjoint set."""
        return item in self._parent

    @property
    def num_sets(self) -> int:
        """Return the number of disjoint sets."""
        return self._num_sets

    def add(self, x: T) -> bool:
        """Add a new element to its own set.

        Returns True if added, False if already present.
        """
        if x in self._parent:
            return False
        self._parent[x] = x
        self._rank[x] = 0
        self._num_sets += 1
        return True

    def find(self, x: T) -> T:
        """Find the representative of the set containing x with path compression."""
        if x not in self._parent:
            raise KeyError(f"Element {x!r} not in disjoint set")
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        curr = x
        while curr != root:
            parent = self._parent[curr]
            self._parent[curr] = root
            curr = parent
        return root

    def union(self, x: T, y: T) -> bool:
        """Merge sets containing x and y using union by rank.

        Returns True if sets were merged, False if already in the same set.
        """
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False

        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x

        self._parent[root_y] = root_x
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1

        self._num_sets -= 1
        return True

    def connected(self, x: T, y: T) -> bool:
        """Check whether x and y belong to the same set."""
        return self.find(x) == self.find(y)

    def subsets(self) -> List[Set[T]]:
        """Return all disjoint sets as a list of sets."""
        groups: Dict[T, Set[T]] = {}
        for elem in self._parent:
            root = self.find(elem)
            groups.setdefault(root, set()).add(elem)
        return list(groups.values())
