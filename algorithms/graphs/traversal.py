"""Breadth-first search (BFS) and depth-first search (DFS) graph traversals."""
from collections import deque
from typing import Dict, Iterable, List, Mapping, Optional, Set, TypeVar

T = TypeVar("T")


def bfs(graph: Mapping[T, Iterable[T]], start: T) -> List[T]:
    """Perform breadth-first search traversal starting from a given vertex.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    visited: Set[T] = {start}
    queue: deque[T] = deque([start])
    order: List[T] = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, ()):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def dfs(graph: Mapping[T, Iterable[T]], start: T) -> List[T]:
    """Perform depth-first search traversal starting from a given vertex.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    visited: Set[T] = set()
    stack: List[T] = [start]
    order: List[T] = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            neighbors = list(graph.get(node, ()))
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)

    return order


def shortest_path(
    graph: Mapping[T, Iterable[T]], start: T, target: T
) -> Optional[List[T]]:
    """Find the shortest unweighted path between start and target using BFS.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    if start == target:
        return [start]

    visited: Set[T] = {start}
    queue: deque[T] = deque([start])
    predecessors: Dict[T, T] = {}

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, ()):
            if neighbor not in visited:
                visited.add(neighbor)
                predecessors[neighbor] = node
                if neighbor == target:
                    path: List[T] = []
                    curr: Optional[T] = target
                    while curr is not None:
                        path.append(curr)
                        curr = predecessors.get(curr)
                    path.reverse()
                    return path
                queue.append(neighbor)

    return None
