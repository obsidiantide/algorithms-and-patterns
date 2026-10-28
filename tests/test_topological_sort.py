"""Unit tests for topological sort algorithm."""
import pytest
from algorithms.graphs.topological_sort import CycleError, topological_sort


def _is_valid_order(graph, order):
    index = {node: i for i, node in enumerate(order)}
    for u, neighbors in graph.items():
        for v in neighbors:
            if index[u] >= index[v]:
                return False
    return True


def test_empty_graph():
    assert topological_sort({}) == []


def test_single_node_no_edges():
    assert topological_sort({"A": []}) == ["A"]


def test_linear_chain():
    graph = {"A": ["B"], "B": ["C"], "C": ["D"], "D": []}
    order = topological_sort(graph)
    assert order == ["A", "B", "C", "D"]
    assert _is_valid_order(graph, order)


def test_diamond_dag():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    order = topological_sort(graph)
    assert len(order) == 4
    assert _is_valid_order(graph, order)
    assert order[0] == "A"
    assert order[-1] == "D"


def test_implicit_target_nodes():
    # Target node "B" is not an explicit key in graph
    graph = {"A": ["B"]}
    order = topological_sort(graph)
    assert order == ["A", "B"]
    assert _is_valid_order(graph, order)


def test_disconnected_components():
    graph = {
        1: [2],
        2: [],
        3: [4],
        4: [],
    }
    order = topological_sort(graph)
    assert len(order) == 4
    assert _is_valid_order(graph, order)


def test_complex_dag():
    graph = {
        "build": ["test", "lint"],
        "test": ["deploy"],
        "lint": ["deploy"],
        "prepare": ["build"],
        "deploy": [],
    }
    order = topological_sort(graph)
    assert len(order) == 5
    assert _is_valid_order(graph, order)
    assert order.index("prepare") < order.index("build")
    assert order.index("deploy") == len(order) - 1


def test_cycle_detection_simple():
    graph = {"A": ["B"], "B": ["A"]}
    with pytest.raises(CycleError, match="at least one cycle"):
        topological_sort(graph)


def test_cycle_detection_self_loop():
    graph = {"A": ["A"]}
    with pytest.raises(CycleError, match="at least one cycle"):
        topological_sort(graph)


def test_cycle_detection_subgraph_cycle():
    graph = {
        "entry": ["node1"],
        "node1": ["node2"],
        "node2": ["node1"],
    }
    with pytest.raises(CycleError):
        topological_sort(graph)
