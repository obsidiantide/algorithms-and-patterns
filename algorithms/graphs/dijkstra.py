"""Dijkstra's shortest path algorithm implementation."""
import heapq
from typing import Dict, Hashable, List, Mapping, Optional, Tuple, TypeVar

T = TypeVar("T", bound=Hashable)


def dijkstra(
    graph: Mapping[T, Mapping[T, float]],
    start: T,
    target: Optional[T] = None,
) -> Tuple[Dict[T, float], Dict[T, Optional[T]]]:
    """Compute shortest distances and predecessors using Dijkstra's algorithm.

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)
    """
    distances: Dict[T, float] = {start: 0.0}
    predecessors: Dict[T, Optional[T]] = {start: None}
    visited = set()
    counter = 0
    pq: List[Tuple[float, int, T]] = [(0.0, counter, start)]

    while pq:
        curr_dist, _, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        if target is not None and u == target:
            break

        for v, weight in graph.get(u, {}).items():
            if weight < 0:
                raise ValueError(f"Negative edge weight: {u} -> {v} ({weight})")
            distance = curr_dist + weight
            if distance < distances.get(v, float("inf")):
                distances[v] = distance
                predecessors[v] = u
                counter += 1
                heapq.heappush(pq, (distance, counter, v))

    return distances, predecessors


def shortest_path(
    graph: Mapping[T, Mapping[T, float]],
    start: T,
    target: T,
) -> Tuple[float, List[T]]:
    """Find the shortest path and its total distance from start to target."""
    distances, predecessors = dijkstra(graph, start, target=target)
    if target not in distances:
        raise ValueError(f"No path found from {start!r} to {target!r}")

    path: List[T] = []
    curr: Optional[T] = target
    while curr is not None:
        path.append(curr)
        curr = predecessors.get(curr)
    path.reverse()
    return distances[target], path
