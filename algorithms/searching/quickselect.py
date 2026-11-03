"""Quickselect algorithm for finding the k-th smallest element."""
import random
from typing import List, Sequence, TypeVar

T = TypeVar("T")


def quickselect(arr: Sequence[T], k: int) -> T:
    """Find the k-th smallest element (0-indexed) in an unordered sequence.

    Uses randomized 3-way partitioning (Dutch National Flag) to handle duplicates
    efficiently while maintaining O(n) average time complexity.

    Time Complexity:
        Average: O(n)
        Worst: O(n^2)
    Space Complexity: O(n) auxiliary to preserve input sequence

    Args:
        arr: Sequence of comparable elements.
        k: 0-based rank of the element to return (0 <= k < len(arr)).

    Returns:
        The k-th smallest element in arr.

    Raises:
        IndexError: If k is out of range [0, len(arr) - 1] or arr is empty.
    """
    if not arr:
        raise IndexError("quickselect on empty sequence")
    if k < 0 or k >= len(arr):
        raise IndexError(f"index k={k} out of range for sequence of length {len(arr)}")

    items: List[T] = list(arr)
    low, high = 0, len(items) - 1

    while low <= high:
        pivot_idx = random.randint(low, high)
        pivot = items[pivot_idx]

        lt, i, gt = low, low, high
        while i <= gt:
            if items[i] < pivot:
                items[lt], items[i] = items[i], items[lt]
                lt += 1
                i += 1
            elif items[i] > pivot:
                items[i], items[gt] = items[gt], items[i]
                gt -= 1
            else:
                i += 1

        if k < lt:
            high = lt - 1
        elif k > gt:
            low = gt + 1
        else:
            return items[k]

    return items[k]
