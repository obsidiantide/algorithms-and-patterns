"""Longest Common Subsequence (LCS) dynamic programming implementations."""
from typing import List, Sequence, TypeVar

T = TypeVar("T")


def lcs_length(s1: Sequence[T], s2: Sequence[T]) -> int:
    """Compute the length of the longest common subsequence between two sequences.

    Time Complexity: O(m * n)
    Space Complexity: O(min(m, n))
    """
    if not s1 or not s2:
        return 0

    if len(s1) < len(s2):
        s1, s2 = s2, s1

    n = len(s2)
    dp = [0] * (n + 1)

    for elem1 in s1:
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if elem1 == s2[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = temp

    return dp[n]


def longest_common_subsequence(s1: Sequence[T], s2: Sequence[T]) -> List[T]:
    """Reconstruct the longest common subsequence between two sequences.

    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    """
    m, n = len(s1), len(s2)
    if m == 0 or n == 0:
        return []

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result: List[T] = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()
    return result


def lcs_string(s1: str, s2: str) -> str:
    """Compute the longest common subsequence of two strings.

    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    """
    return "".join(longest_common_subsequence(s1, s2))
