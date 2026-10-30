"""Kruskal's algorithm for computing Minimum Spanning Trees (MST)."""
from collections.abc import Mapping
from typing import Hashable, Iterable, List, Set, Tuple, TypeVar, Union

from structures.disjoint_set import DisjointSet

T = TypeVar("T", bound=Hashable)


def kruskal(
    graph_or_edges: Union[Mapping[T, Mapping[T, float]], Iterable[Tuple[T, T, float]]],
) -> Tuple[float, List[Tuple[T, T, float]]]:
    """Compute the Minimum Spanning Forest (or Tree) using Kruskal's algorithm.

    Iterates over edges sorted by increasing weight and includes edges that
    connect previously disjoint components using a Disjoint Set (Union-Find).

    Args:
        graph_or_edges: Either an adjacency mapping {u: {v: weight}} or an
            iterable of edge tuples (u, v, weight).

    Returns:
        A tuple (total_weight, mst_edges) where mst_edges is the list of
        edges forming the minimum spanning tree or forest.

    Time Complexity: O(E log E) where E is the number of edges.
    Space Complexity: O(V + E) where V is vertices, E is edges.
    """
    if isinstance(graph_or_edges, Mapping):
        edge_list: List[Tuple[T, T, float]] = []
        seen: Set[frozenset[T]] = set()
        for u, neighbors in graph_or_edges.items():
            for v, weight in neighbors.items():
                pair = frozenset({u, v})
                if pair not in seen:
                    seen.add(pair)
                    edge_list.append((u, v, float(weight)))
    else:
        edge_list = [(u, v, float(w)) for u, v, w in graph_or_edges]

    edge_list.sort(key=lambda edge: edge[2])

    ds: DisjointSet[T] = DisjointSet()
    mst_edges: List[Tuple[T, T, float]] = []
    total_weight: float = 0.0

    for u, v, weight in edge_list:
        if u == v:
            continue
        ds.add(u)
        ds.add(v)
        if ds.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight

    return total_weight, mst_edges
