"""Levenshtein distance (edit distance) dynamic programming implementations."""
from typing import Sequence, TypeVar

T = TypeVar("T")


def levenshtein_distance(
    s1: Sequence[T],
    s2: Sequence[T],
    *,
    insertion_cost: int = 1,
    deletion_cost: int = 1,
    substitution_cost: int = 1,
) -> int:
    """Compute the minimum edit distance to transform s1 into s2.

    Supported operations: insertion, deletion, and substitution.

    Time Complexity: O(m * n)
    Space Complexity: O(min(m, n))
    """
    if insertion_cost < 0 or deletion_cost < 0 or substitution_cost < 0:
        raise ValueError("operation costs must be non-negative")

    # If transforming s1 -> s2 is inverted, insertion and deletion costs swap.
    # Keep s2 as the shorter sequence to achieve O(min(m, n)) space complexity.
    if len(s1) < len(s2):
        s1, s2 = s2, s1
        insertion_cost, deletion_cost = deletion_cost, insertion_cost

    m, n = len(s1), len(s2)
    if n == 0:
        return m * deletion_cost

    dp = [j * insertion_cost for j in range(n + 1)]

    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i * deletion_cost
        for j in range(1, n + 1):
            temp = dp[j]
            if s1[i - 1] == s2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = min(
                    dp[j] + deletion_cost,
                    dp[j - 1] + insertion_cost,
                    prev + substitution_cost,
                )
            prev = temp

    return dp[n]


def is_one_edit_distance(s1: Sequence[T], s2: Sequence[T]) -> bool:
    """Determine whether s1 and s2 are exactly one edit operation apart.

    Time Complexity: O(min(m, n))
    Space Complexity: O(1)
    """
    m, n = len(s1), len(s2)
    if abs(m - n) > 1:
        return False

    if m > n:
        return is_one_edit_distance(s2, s1)

    for i in range(m):
        if s1[i] != s2[i]:
            if m == n:
                return all(s1[k] == s2[k] for k in range(i + 1, m))
            return all(s1[k] == s2[k + 1] for k in range(i, m))

    return n == m + 1
