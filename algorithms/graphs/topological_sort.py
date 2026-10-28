"""Topological sort implementation using Kahn's algorithm."""
from collections import deque
from typing import Dict, Iterable, List, Mapping, TypeVar

T = TypeVar("T")


class CycleError(ValueError):
    """Raised when a graph contains a directed cycle and cannot be topologically sorted."""
    pass


def topological_sort(graph: Mapping[T, Iterable[T]]) -> List[T]:
    """Perform a topological sort on a directed acyclic graph (DAG) using Kahn's algorithm.

    Args:
        graph: Adjacency mapping where each key is a vertex and the value is an
            iterable of its outgoing neighboring vertices (successors).

    Returns:
        A list of vertices in topological order.

    Raises:
        CycleError: If the graph contains a cycle (not a DAG).

    Time Complexity: O(V + E)
    Space Complexity: O(V + E)
    """
    in_degree: Dict[T, int] = {}
    adjacency: Dict[T, List[T]] = {}

    for node, neighbors in graph.items():
        if node not in in_degree:
            in_degree[node] = 0
        if node not in adjacency:
            adjacency[node] = []
        for neighbor in neighbors:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
            adjacency[node].append(neighbor)
            if neighbor not in in_degree:
                in_degree[neighbor] = 0
            if neighbor not in adjacency:
                adjacency[neighbor] = []

    queue: deque[T] = deque([node for node, deg in in_degree.items() if deg == 0])
    result: List[T] = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adjacency[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(in_degree):
        raise CycleError("Graph contains at least one cycle")

    return result
