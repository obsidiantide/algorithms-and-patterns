"""Unit tests for Floyd-Warshall all-pairs shortest path algorithm."""
import pytest
from algorithms.graphs.floyd_warshall import (
    NegativeCycleError,
    floyd_warshall,
    shortest_path,
)


def test_single_node():
    graph = {"A": {}}
    distances, next_node = floyd_warshall(graph)
    assert distances == {"A": {"A": 0.0}}
    assert next_node == {"A": {"A": "A"}}
    assert shortest_path(graph, "A", "A") == (0.0, ["A"])


def test_all_pairs_distances():
    graph = {
        "A": {"B": 3.0, "C": 8.0},
        "B": {"C": 2.0},
        "C": {},
    }
    dist, next_node = floyd_warshall(graph)
    assert dist["A"]["A"] == 0.0
    assert dist["A"]["B"] == 3.0
    assert dist["A"]["C"] == 5.0
    assert dist["B"]["C"] == 2.0
    assert dist["C"]["A"] == float("inf")
    assert next_node["A"]["C"] == "B"


def test_positive_weights_path():
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
        floyd_warshall(graph)


def test_unreachable_node():
    graph = {"A": {"B": 1.0}, "B": {}, "C": {}}
    dist, _ = floyd_warshall(graph)
    assert dist["A"]["C"] == float("inf")
    with pytest.raises(ValueError, match="No path found"):
        shortest_path(graph, "A", "C")


def test_non_existent_node_raises():
    graph = {"A": {"B": 1.0}, "B": {}}
    with pytest.raises(ValueError, match="No path found"):
        shortest_path(graph, "A", "Z")
