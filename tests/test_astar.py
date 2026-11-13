import pytest

from algorithms.graphs.astar import astar_grid, manhattan
from collections import deque


def bfs_length(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    dist = {start: 0}
    q = deque([start])
    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            return dist[(r, c)]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (r + dr, c + dc)
            if 0 <= n[0] < rows and 0 <= n[1] < cols and grid[n[0]][n[1]] == 0 and n not in dist:
                dist[n] = dist[(r, c)] + 1
                q.append(n)
    return None


def test_manhattan():
    assert manhattan((0, 0), (3, 4)) == 7


def test_straight_line_on_open_grid():
    grid = [[0] * 4 for _ in range(4)]
    path = astar_grid(grid, (0, 0), (0, 3))
    assert path == [(0, 0), (0, 1), (0, 2), (0, 3)]


def test_start_equals_goal():
    assert astar_grid([[0]], (0, 0), (0, 0)) == [(0, 0)]


def test_routes_around_wall():
    grid = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    path = astar_grid(grid, (0, 0), (0, 2))
    assert path[0] == (0, 0) and path[-1] == (0, 2)
    assert len(path) - 1 == 6
    assert all(grid[r][c] == 0 for r, c in path)


def test_unreachable_goal_returns_none():
    grid = [
        [0, 1, 0],
        [0, 1, 0],
    ]
    assert astar_grid(grid, (0, 0), (0, 2)) is None


@pytest.mark.parametrize("start,goal", [((0, 1), (2, 2)), ((0, 0), (5, 5)), ((-1, 0), (0, 0))])
def test_invalid_endpoints_raise(start, goal):
    grid = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
    with pytest.raises(ValueError):
        astar_grid(grid, start, goal)


def test_path_steps_are_adjacent_and_optimal_vs_bfs():
    grid = [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    start, goal = (0, 0), (4, 0)
    path = astar_grid(grid, start, goal)
    for a, b in zip(path, path[1:]):
        assert manhattan(a, b) == 1
    assert len(path) - 1 == bfs_length(grid, start, goal)
