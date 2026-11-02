"""Unit tests for Kadane's algorithm."""
import pytest

from algorithms.dynamic.kadane import max_subarray, max_subarray_sum


def test_empty_input():
    with pytest.raises(ValueError, match="arr cannot be empty"):
        max_subarray_sum([])
    with pytest.raises(ValueError, match="arr cannot be empty"):
        max_subarray([])


def test_single_element():
    assert max_subarray_sum([5]) == 5
    assert max_subarray([5]) == (5, 0, 0)

    assert max_subarray_sum([-3]) == -3
    assert max_subarray([-3]) == (-3, 0, 0)

    assert max_subarray_sum([0]) == 0
    assert max_subarray([0]) == (0, 0, 0)


def test_all_positive():
    arr = [1, 2, 3, 4, 5]
    assert max_subarray_sum(arr) == 15
    assert max_subarray(arr) == (15, 0, 4)


def test_all_negative():
    arr = [-8, -3, -6, -2, -5, -4]
    assert max_subarray_sum(arr) == -2
    assert max_subarray(arr) == (-2, 3, 3)


def test_classic_mixed_cases():
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    max_sum, start, end = max_subarray(arr)
    assert max_sum == 6
    assert (start, end) == (3, 6)
    assert max_subarray_sum(arr) == 6
    assert sum(arr[start : end + 1]) == 6


def test_with_zeros():
    arr = [0, -1, 2, 0, -1, 3, 0]
    max_sum, start, end = max_subarray(arr)
    assert max_sum == 4
    assert max_subarray_sum(arr) == 4
    assert sum(arr[start : end + 1]) == 4


def test_floats():
    arr = [1.5, -2.0, 3.5, 2.5, -1.0]
    max_sum, start, end = max_subarray(arr)
    assert max_sum == 6.0
    assert max_subarray_sum(arr) == 6.0
    assert sum(arr[start : end + 1]) == 6.0


def test_sequence_types():
    tpl = (-2, 5, -1, 4)
    assert max_subarray_sum(tpl) == 8
    assert max_subarray(tpl) == (8, 1, 3)
