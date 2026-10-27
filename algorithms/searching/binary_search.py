"""Binary search implementations with type hints and edge case handling."""
from typing import Sequence, TypeVar, Optional

T = TypeVar("T")


def binary_search(arr: Sequence[T], target: T) -> Optional[int]:
    """Perform standard binary search on a sorted sequence.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None


def find_leftmost(arr: Sequence[T], target: T) -> int:
    """Find index of leftmost insertion point for target in sorted sequence."""
    left, right = 0, len(arr)
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def find_rightmost(arr: Sequence[T], target: T) -> int:
    """Find index of rightmost insertion point for target in sorted sequence."""
    left, right = 0, len(arr)
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left


def search_range(arr: Sequence[T], target: T) -> Optional[tuple[int, int]]:
    """Find starting and ending index of a target in sorted sequence.

    Returns:
        A tuple of (start_idx, end_idx) if target is present, otherwise None.
    """
    left = find_leftmost(arr, target)
    right = find_rightmost(arr, target) - 1
    if left <= right and left < len(arr) and arr[left] == target:
        return (left, right)
    return None
