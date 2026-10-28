"""0-1 Knapsack problem dynamic programming implementation."""
from typing import List, Sequence, Tuple


def knapsack_01(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    """Compute the maximum total value obtainable within the given capacity.

    Time Complexity: O(n * W)
    Space Complexity: O(W)
    """
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")
    if capacity < 0:
        raise ValueError("capacity cannot be negative")
    if any(w < 0 for w in weights):
        raise ValueError("weights cannot be negative")
    if any(v < 0 for v in values):
        raise ValueError("values cannot be negative")
    if capacity == 0 or not weights:
        return 0

    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for cap in range(capacity, w - 1, -1):
            if dp[cap - w] + v > dp[cap]:
                dp[cap] = dp[cap - w] + v

    return dp[capacity]


def knapsack_01_items(
    weights: Sequence[int], values: Sequence[int], capacity: int
) -> Tuple[int, List[int]]:
    """Compute maximum value and return the indices of selected items.

    Time Complexity: O(n * W)
    Space Complexity: O(n * W)
    """
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")
    if capacity < 0:
        raise ValueError("capacity cannot be negative")
    if any(w < 0 for w in weights):
        raise ValueError("weights cannot be negative")
    if any(v < 0 for v in values):
        raise ValueError("values cannot be negative")

    n = len(weights)
    if capacity == 0 or n == 0:
        return 0, []

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for cap in range(capacity + 1):
            if w <= cap:
                dp[i][cap] = max(dp[i - 1][cap], dp[i - 1][cap - w] + v)
            else:
                dp[i][cap] = dp[i - 1][cap]

    max_value = dp[n][capacity]
    selected_indices: List[int] = []
    curr_cap = capacity
    for i in range(n, 0, -1):
        if dp[i][curr_cap] != dp[i - 1][curr_cap]:
            selected_indices.append(i - 1)
            curr_cap -= weights[i - 1]

    selected_indices.reverse()
    return max_value, selected_indices
