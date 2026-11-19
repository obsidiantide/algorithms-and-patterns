"""Helpers shared by the weighted shortest-path algorithms."""
from typing import Hashable, List, Mapping, Set, Tuple, TypeVar

T = TypeVar("T", bound=Hashable)


class NegativeCycleError(ValueError):
    """Raised when a negative-weight cycle is detected."""


def collect_edges(
    graph: Mapping[T, Mapping[T, float]],
) -> Tuple[Set[T], List[Tuple[T, T, float]]]:
    """Flatten an adjacency mapping into ``(vertices, edges)``.

    Vertices that only appear as edge targets are included. Weights are
    converted to ``float``; NaN weights are rejected because they silently
    break relaxation comparisons.
    """
    vertices: Set[T] = set()
    edges: List[Tuple[T, T, float]] = []
    for u, neighbors in graph.items():
        vertices.add(u)
        for v, weight in neighbors.items():
            w = float(weight)
            if w != w:
                raise ValueError(f"edge weight {u!r} -> {v!r} is NaN")
            vertices.add(v)
            edges.append((u, v, w))
    return vertices, edges
