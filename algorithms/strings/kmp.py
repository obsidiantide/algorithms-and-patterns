"""Knuth-Morris-Pratt substring search."""
from typing import List


def build_prefix_table(pattern: str) -> List[int]:
    """Build the KMP failure function for ``pattern``.

    ``table[i]`` is the length of the longest proper prefix of
    ``pattern[: i + 1]`` that is also its suffix.

    Time Complexity: O(m)
    Space Complexity: O(m)
    """
    table = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = table[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        table[i] = k
    return table


def kmp_search(text: str, pattern: str) -> List[int]:
    """Return the start indices of all (possibly overlapping) occurrences.

    An empty pattern matches at every position ``0..len(text)``.

    Time Complexity: O(n + m)
    Space Complexity: O(m)

    Args:
        text: The string to search in.
        pattern: The string to look for.

    Returns:
        Sorted list of indices where ``pattern`` occurs in ``text``.
    """
    if not pattern:
        return list(range(len(text) + 1))

    table = build_prefix_table(pattern)
    matches: List[int] = []
    k = 0
    for i, ch in enumerate(text):
        while k > 0 and ch != pattern[k]:
            k = table[k - 1]
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            matches.append(i - k + 1)
            k = table[k - 1]
    return matches
