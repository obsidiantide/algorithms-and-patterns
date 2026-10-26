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
