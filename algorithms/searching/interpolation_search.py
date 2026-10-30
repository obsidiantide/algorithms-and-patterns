"""Interpolation search implementation for sorted numerical sequences."""
from typing import Optional, Sequence


def interpolation_search(arr: Sequence[int], target: int) -> Optional[int]:
    """Search for a target value in a sorted sequence of uniformly distributed integers.

    Interpolation search estimates the target's position based on its value relative
    to the values at the endpoints of the search window.

    Time Complexity:
        Average: O(log(log n)) for uniformly distributed elements
        Worst: O(n)
    Space Complexity: O(1)

    Args:
        arr: Sorted sequence of integers.
        target: Integer value to find.

    Returns:
        Index of target if found; None otherwise.
    """
    if not arr:
        return None

    low = 0
    high = len(arr) - 1

    while low <= high and arr[low] <= target <= arr[high]:
        if arr[low] == arr[high]:
            if arr[low] == target:
                return low
            return None

        pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return None
