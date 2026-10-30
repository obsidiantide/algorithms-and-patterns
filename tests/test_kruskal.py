"""Unit tests for Kruskal's algorithm."""
import pytest
from algorithms.graphs.kruskal import kruskal


def test_empty_graph():
    assert kruskal([]) == (0.0, [])
    assert kruskal({}) == (0.0, [])


def test_single_edge():
    edges = [("A", "B", 3.5)]
    weight, mst = kruskal(edges)
    assert weight == 3.5
    assert mst == [("A", "B", 3.5)]


def test_simple_triangle_cycle():
    edges = [
        ("A", "B", 1.0),
        ("B", "C", 2.0),
        ("A", "C", 3.0),
    ]
    weight, mst = kruskal(edges)
    assert weight == 3.0
    assert len(mst) == 2
    assert ("A", "B", 1.0) in mst
    assert ("B", "C", 2.0) in mst
    assert ("A", "C", 3.0) not in mst


def test_adjacency_mapping_input():
    graph = {
        "A": {"B": 1.0, "C": 4.0},
        "B": {"A": 1.0, "C": 2.0, "D": 5.0},
        "C": {"A": 4.0, "B": 2.0, "D": 1.0},
        "D": {"B": 5.0, "C": 1.0},
    }
    weight, mst = kruskal(graph)
    assert weight == 4.0
    assert len(mst) == 3


def test_disconnected_forest():
    edges = [
        ("A", "B", 1.0),
        ("C", "D", 2.0),
    ]
    weight, mst = kruskal(edges)
    assert weight == 3.0
    assert len(mst) == 2


def test_negative_weights():
    edges = [
        ("A", "B", -5.0),
        ("B", "C", 3.0),
        ("A", "C", 2.0),
    ]
    weight, mst = kruskal(edges)
    assert weight == -3.0
    assert len(mst) == 2
    assert ("A", "B", -5.0) in mst
    assert ("A", "C", 2.0) in mst


def test_self_loops_and_duplicate_edges():
    edges = [
        ("A", "A", 0.0),
        ("A", "B", 5.0),
        ("A", "B", 2.0),
    ]
    weight, mst = kruskal(edges)
    assert weight == 2.0
    assert mst == [("A", "B", 2.0)]


def test_integer_vertices():
    edges = [
        (1, 2, 10.0),
        (2, 3, 15.0),
        (1, 3, 5.0),
    ]
    weight, mst = kruskal(edges)
    assert weight == 15.0
    assert mst == [(1, 3, 5.0), (1, 2, 10.0)]
