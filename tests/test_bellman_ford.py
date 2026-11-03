"""Unit tests for Bellman-Ford shortest path algorithm."""
import pytest
from algorithms.graphs.bellman_ford import NegativeCycleError, bellman_ford, shortest_path


def test_single_node():
    graph = {"A": {}}
    distances, predecessors = bellman_ford(graph, "A")
    assert distances == {"A": 0.0}
    assert predecessors == {"A": None}
    assert shortest_path(graph, "A", "A") == (0.0, ["A"])


def test_positive_weights():
    graph = {
        "A": {"B": 4.0, "C": 2.0},
        "B": {"D": 2.0},
        "C": {"B": 1.0, "D": 5.0},
        "D": {},
    }
    dist, path = shortest_path(graph, "A", "D")
    assert dist == 5.0
    assert path == ["A", "C", "B", "D"]


def test_negative_weights_without_cycle():
    graph = {
        "A": {"B": 4.0, "C": 5.0},
        "B": {"C": -2.0, "D": 3.0},
        "C": {"D": 1.0},
        "D": {},
    }
    dist, path = shortest_path(graph, "A", "D")
    assert dist == 3.0
    assert path == ["A", "B", "C", "D"]


def test_negative_cycle_raises():
    graph = {
        "A": {"B": 1.0},
        "B": {"C": 2.0},
        "C": {"B": -3.0},
    }
    with pytest.raises(NegativeCycleError, match="Negative-weight cycle detected"):
        bellman_ford(graph, "A")


def test_unreachable_negative_cycle():
    graph = {
        "A": {"B": 2.0},
        "B": {},
        "X": {"Y": 1.0},
        "Y": {"X": -3.0},
    }
    distances, _ = bellman_ford(graph, "A")
    assert distances == {"A": 0.0, "B": 2.0}
    assert shortest_path(graph, "A", "B") == (2.0, ["A", "B"])


def test_unreachable_target():
    graph = {"A": {"B": 1.0}, "B": {}, "C": {}}
    distances, _ = bellman_ford(graph, "A")
    assert "C" not in distances
    with pytest.raises(ValueError, match="No path found"):
        shortest_path(graph, "A", "C")
