"""Floyd-Warshall all-pairs shortest path algorithm."""
from typing import Dict, Hashable, List, Mapping, Optional, Set, Tuple, TypeVar

T = TypeVar("T", bound=Hashable)


class NegativeCycleError(ValueError):
    """Raised when a negative-weight cycle is detected."""
    pass


def floyd_warshall(
    graph: Mapping[T, Mapping[T, float]],
) -> Tuple[Dict[T, Dict[T, float]], Dict[T, Dict[T, Optional[T]]]]:
    """Compute all-pairs shortest paths and next-hop pointers using Floyd-Warshall.

    Supports negative edge weights and detects negative-weight cycles.

    Time Complexity: O(V^3)
    Space Complexity: O(V^2)
    """
    vertices: Set[T] = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors.keys())

    vertex_list = list(vertices)
    distances: Dict[T, Dict[T, float]] = {
        u: {v: float("inf") for v in vertex_list} for u in vertex_list
    }
    next_node: Dict[T, Dict[T, Optional[T]]] = {
        u: {v: None for v in vertex_list} for u in vertex_list
    }

    for u in vertex_list:
        distances[u][u] = 0.0
        next_node[u][u] = u

    for u, neighbors in graph.items():
        for v, weight in neighbors.items():
            w = float(weight)
            if w < distances[u][v]:
                distances[u][v] = w
                next_node[u][v] = v

    for k in vertex_list:
        dist_k = distances[k]
        for i in vertex_list:
            dist_i_k = distances[i][k]
            if dist_i_k == float("inf"):
                continue
            dist_i = distances[i]
            next_i = next_node[i]
            for j in vertex_list:
                dist_k_j = dist_k[j]
                if dist_k_j == float("inf"):
                    continue
                new_dist = dist_i_k + dist_k_j
                if new_dist < dist_i[j]:
                    dist_i[j] = new_dist
                    next_i[j] = next_i[k]

    for v in vertex_list:
        if distances[v][v] < 0.0:
            raise NegativeCycleError(
                f"Negative-weight cycle detected involving vertex {v!r}"
            )

    return distances, next_node


def shortest_path(
    graph: Mapping[T, Mapping[T, float]],
    start: T,
    target: T,
) -> Tuple[float, List[T]]:
    """Find the shortest path and its total distance from start to target.

    Time Complexity: O(V^3)
    Space Complexity: O(V^2)
    """
    distances, next_node = floyd_warshall(graph)

    if start not in distances or target not in distances:
        raise ValueError(f"No path found from {start!r} to {target!r}")

    if distances[start][target] == float("inf"):
        raise ValueError(f"No path found from {start!r} to {target!r}")

    path: List[T] = [start]
    curr = start
    while curr != target:
        succ = next_node[curr][target]
        if succ is None:
            raise ValueError(f"No path found from {start!r} to {target!r}")
        path.append(succ)
        curr = succ

    return distances[start][target], path
