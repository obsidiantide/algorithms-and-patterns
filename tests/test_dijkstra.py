"""Unit tests for Dijkstra's shortest path algorithm."""
import pytest
from algorithms.graphs.dijkstra import dijkstra, shortest_path


def test_single_node():
    graph = {"A": {}}
    distances, predecessors = dijkstra(graph, "A")
    assert distances == {"A": 0.0}
    assert predecessors == {"A": None}
    assert shortest_path(graph, "A", "A") == (0.0, ["A"])


def test_linear_and_alternative_paths():
    graph = {
        "A": {"B": 3.0, "C": 10.0},
        "B": {"C": 2.0},
        "C": {},
    }
    dist, path = shortest_path(graph, "A", "C")
    assert dist == 5.0
    assert path == ["A", "B", "C"]


def test_unreachable_node():
    graph = {"A": {"B": 1.0}, "B": {}, "C": {}}
    distances, _ = dijkstra(graph, "A")
    assert "C" not in distances
    with pytest.raises(ValueError, match="No path found"):
        shortest_path(graph, "A", "C")


def test_negative_weight_raises():
    with pytest.raises(ValueError, match="Negative edge weight"):
        dijkstra({"A": {"B": -1.0}}, "A")


def test_non_comparable_vertex_types():
    class Node:
        def __init__(self, name: str):
            self.name = name

    n1, n2, n3 = Node("1"), Node("2"), Node("3")
    distances, _ = dijkstra({n1: {n2: 1.0, n3: 1.0}}, n1)
    assert distances[n2] == 1.0
    assert distances[n3] == 1.0


def test_early_stopping():
    graph = {"A": {"B": 1.0, "C": 10.0}, "B": {}, "C": {"D": 1.0}, "D": {}}
    distances, _ = dijkstra(graph, "A", target="B")
    assert "B" in distances
    assert "D" not in distances
