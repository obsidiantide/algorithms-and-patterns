"""Kadane's algorithm for the maximum subarray problem."""
from typing import Sequence, Tuple, Union

Number = Union[int, float]


def max_subarray_sum(arr: Sequence[Number]) -> Number:
    """Compute the maximum contiguous subarray sum using Kadane's algorithm.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not arr:
        raise ValueError("arr cannot be empty")

    max_ending_here = max_so_far = arr[0]
    for x in arr[1:]:
        max_ending_here = max(x, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far


def max_subarray(arr: Sequence[Number]) -> Tuple[Number, int, int]:
    """Compute the maximum contiguous subarray sum and its [start, end] indices.

    Returns a tuple of (max_sum, start_index, end_index) where indices are inclusive.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not arr:
        raise ValueError("arr cannot be empty")

    max_ending_here = max_so_far = arr[0]
    start = end = curr_start = 0

    for i in range(1, len(arr)):
        x = arr[i]
        if x > max_ending_here + x:
            max_ending_here = x
            curr_start = i
        else:
            max_ending_here += x

        if max_ending_here > max_so_far:
            max_so_far = max_ending_here
            start = curr_start
            end = i

    return max_so_far, start, end
