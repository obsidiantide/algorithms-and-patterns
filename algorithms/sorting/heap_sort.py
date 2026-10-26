"""In-place HeapSort implementation with type hints."""
from typing import List, TypeVar

T = TypeVar("T")


def _sift_down(arr: List[T], start: int, end: int) -> None:
    """Repair max-heap property for subtree rooted at start within arr[0:end]."""
    root = start
    while (left := 2 * root + 1) < end:
        swap = root
        if arr[swap] < arr[left]:
            swap = left
        right = left + 1
        if right < end and arr[swap] < arr[right]:
            swap = right
        if swap == root:
            break
        arr[root], arr[swap] = arr[swap], arr[root]
        root = swap


def heap_sort(arr: List[T]) -> List[T]:
    """Sort a list in ascending order using in-place heap sort.

    Time Complexity: O(n log n)
    Space Complexity: O(1)
    Stable: No
    """
    n = len(arr)
    for start in range((n - 2) // 2, -1, -1):
        _sift_down(arr, start, n)

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down(arr, 0, end)

    return arr
