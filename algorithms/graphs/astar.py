"""A* pathfinding on a 2D grid."""
import heapq
from typing import Dict, List, Optional, Sequence, Tuple

Cell = Tuple[int, int]

_MOVES_4: Tuple[Cell, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))


def manhattan(a: Cell, b: Cell) -> int:
    """Manhattan distance, an admissible heuristic for 4-directional moves."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_grid(
    grid: Sequence[Sequence[int]],
    start: Cell,
    goal: Cell,
) -> Optional[List[Cell]]:
    """Find a shortest 4-directional path on a grid with A*.

    ``grid[row][col]`` is 0 for a free cell and any non-zero value for a wall.
    Returns the list of cells from ``start`` to ``goal`` inclusive, or ``None``
    if the goal is unreachable.

    Time Complexity: O(R * C * log(R * C))
    Space Complexity: O(R * C)
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    def free(cell: Cell) -> bool:
        r, c = cell
        return 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0

    if not free(start) or not free(goal):
        raise ValueError("start and goal must be free cells inside the grid")

    best_cost: Dict[Cell, int] = {start: 0}
    parents: Dict[Cell, Optional[Cell]] = {start: None}
    closed = set()
    counter = 0
    pq: List[Tuple[int, int, Cell]] = [(manhattan(start, goal), counter, start)]

    while pq:
        _, _, cell = heapq.heappop(pq)
        if cell in closed:
            continue
        if cell == goal:
            path: List[Cell] = []
            node: Optional[Cell] = cell
            while node is not None:
                path.append(node)
                node = parents[node]
            path.reverse()
            return path
        closed.add(cell)

        for dr, dc in _MOVES_4:
            nxt = (cell[0] + dr, cell[1] + dc)
            if not free(nxt):
                continue
            cost = best_cost[cell] + 1
            if cost < best_cost.get(nxt, float("inf")):
                best_cost[nxt] = cost
                parents[nxt] = cell
                counter += 1
                heapq.heappush(pq, (cost + manhattan(nxt, goal), counter, nxt))
    return None
