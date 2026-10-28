"""Unit tests for BFS and DFS graph traversals."""
from algorithms.graphs.traversal import bfs, dfs, shortest_path


def test_bfs_linear_graph():
    graph = {"A": ["B"], "B": ["C"], "C": []}
    assert bfs(graph, "A") == ["A", "B", "C"]


def test_bfs_branching():
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [],
        "E": [],
        "F": [],
    }
    assert bfs(graph, "A") == ["A", "B", "C", "D", "E", "F"]


def test_bfs_with_cycle():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A", "D"],
        "D": [],
    }
    assert bfs(graph, "A") == ["A", "B", "C", "D"]


def test_dfs_order():
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [],
        "E": [],
        "F": [],
    }
    assert dfs(graph, "A") == ["A", "B", "D", "E", "C", "F"]


def test_dfs_with_cycle():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A", "D"],
        "D": [],
    }
    assert dfs(graph, "A") == ["A", "B", "C", "D"]


def test_isolated_node():
    assert bfs({}, "A") == ["A"]
    assert dfs({}, "A") == ["A"]


def test_shortest_path_same_node():
    graph = {"A": ["B"]}
    assert shortest_path(graph, "A", "A") == ["A"]


def test_shortest_path_found():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["E"],
        "D": ["F"],
        "E": ["F"],
        "F": [],
    }
    path = shortest_path(graph, "A", "F")
    assert path == ["A", "B", "D", "F"]


def test_shortest_path_picks_fewest_edges():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "D": ["E"],
        "C": ["E"],
        "E": [],
    }
    assert shortest_path(graph, "A", "E") == ["A", "C", "E"]


def test_shortest_path_unreachable():
    graph = {"A": ["B"], "B": [], "C": []}
    assert shortest_path(graph, "A", "C") is None
