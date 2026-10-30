"""LRU (Least Recently Used) Cache implementation using Doubly Linked List & Hash Map."""
from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class Node:
    key: Any
    value: Any
    prev: Optional["Node"] = None
    next: Optional["Node"] = None


class LRUCache:
    """Least Recently Used (LRU) Cache.

    Provides O(1) get, put, peek, and delete operations.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive integer")
        self.capacity = capacity
        self.cache: Dict[Any, Node] = {}
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def __len__(self) -> int:
        return len(self.cache)

    def __contains__(self, key: Any) -> bool:
        return key in self.cache

    def _remove(self, node: Node) -> None:
        prev_node = node.prev
        next_node = node.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_to_front(self, node: Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def get(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        if key not in self.cache:
            return default
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def peek(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        """Retrieve value without updating recency order."""
        if key not in self.cache:
            return default
        return self.cache[key].value

    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self._add_to_front(node)
        self.cache[key] = node

        if len(self.cache) > self.capacity:
            lru_node = self.tail.prev
            if lru_node and lru_node != self.head:
                self._remove(lru_node)
                del self.cache[lru_node.key]

    def delete(self, key: Any) -> bool:
        """Remove a key from the cache. Returns True if removed, False otherwise."""
        if key not in self.cache:
            return False
        node = self.cache.pop(key)
        self._remove(node)
        return True

    def clear(self) -> None:
        """Clear all entries from the cache."""
        self.cache.clear()
        self.head.next = self.tail
        self.tail.prev = self.head
