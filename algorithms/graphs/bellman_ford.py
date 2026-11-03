"""Bellman-Ford shortest path algorithm with negative cycle detection."""
from typing import Dict, Hashable, List, Mapping, Optional, Set, Tuple, TypeVar

T = TypeVar("T", bound=Hashable)


class NegativeCycleError(ValueError):
    """Raised when a negative-weight cycle is detected."""
    pass


def bellman_ford(
    graph: Mapping[T, Mapping[T, float]],
    start: T,
) -> Tuple[Dict[T, float], Dict[T, Optional[T]]]:
    """Compute shortest distances and predecessors using the Bellman-Ford algorithm.

    Supports negative edge weights and detects negative-weight cycles reachable from start.

    Time Complexity: O(V * E)
    Space Complexity: O(V)
    """
    vertices: Set[T] = {start}
    edges: List[Tuple[T, T, float]] = []

    for u, neighbors in graph.items():
        vertices.add(u)
        for v, weight in neighbors.items():
            vertices.add(v)
            edges.append((u, v, float(weight)))

    distances: Dict[T, float] = {start: 0.0}
    predecessors: Dict[T, Optional[T]] = {start: None}

    # Relax edges up to |V| - 1 times
    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, weight in edges:
            if u in distances:
                new_dist = distances[u] + weight
                if v not in distances or new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = u
                    updated = True
        if not updated:
            break

    # Check for negative-weight cycles reachable from start
    for u, v, weight in edges:
        if u in distances:
            if distances[u] + weight < distances.get(v, float("inf")):
                raise NegativeCycleError(
                    f"Negative-weight cycle detected reachable from {start!r}"
                )

    return distances, predecessors


def shortest_path(
    graph: Mapping[T, Mapping[T, float]],
    start: T,
    target: T,
) -> Tuple[float, List[T]]:
    """Find the shortest path and its total distance from start to target.

    Time Complexity: O(V * E)
    Space Complexity: O(V)
    """
    distances, predecessors = bellman_ford(graph, start)
    if target not in distances:
        raise ValueError(f"No path found from {start!r} to {target!r}")

    path: List[T] = []
    curr: Optional[T] = target
    while curr is not None:
        path.append(curr)
        curr = predecessors.get(curr)
    path.reverse()
    return distances[target], path
