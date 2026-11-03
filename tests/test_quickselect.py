"""Unit tests for quickselect algorithm."""
import random
import pytest
from algorithms.searching.quickselect import quickselect


def test_quickselect_basic():
    arr = [7, 10, 4, 3, 20, 15]
    sorted_arr = sorted(arr)
    for k in range(len(arr)):
        assert quickselect(arr, k) == sorted_arr[k]


def test_quickselect_single_element():
    assert quickselect([42], 0) == 42


def test_quickselect_preserves_input():
    original = [5, 2, 8, 1, 9]
    copy = list(original)
    _ = quickselect(original, 2)
    assert original == copy


def test_quickselect_duplicates():
    arr = [3, 1, 2, 3, 1, 3, 2, 1]
    sorted_arr = sorted(arr)
    for k in range(len(arr)):
        assert quickselect(arr, k) == sorted_arr[k]


def test_quickselect_all_identical():
    arr = [5, 5, 5, 5, 5]
    assert quickselect(arr, 0) == 5
    assert quickselect(arr, 2) == 5
    assert quickselect(arr, 4) == 5


def test_quickselect_negatives_and_floats():
    arr = [-3.5, 0.0, 12.2, -10.1, 4.0]
    sorted_arr = sorted(arr)
    for k in range(len(arr)):
        assert quickselect(arr, k) == sorted_arr[k]


def test_quickselect_strings_and_tuples():
    arr = ("banana", "apple", "date", "cherry")
    sorted_arr = sorted(arr)
    for k in range(len(arr)):
        assert quickselect(arr, k) == sorted_arr[k]


def test_quickselect_randomized_large():
    rng = random.Random(42)
    arr = [rng.randint(-1000, 1000) for _ in range(100)]
    sorted_arr = sorted(arr)
    for k in [0, 1, 25, 50, 75, 98, 99]:
        assert quickselect(arr, k) == sorted_arr[k]


def test_quickselect_invalid_bounds():
    with pytest.raises(IndexError, match="empty sequence"):
        quickselect([], 0)

    arr = [1, 2, 3]
    with pytest.raises(IndexError, match="out of range"):
        quickselect(arr, -1)
    with pytest.raises(IndexError, match="out of range"):
        quickselect(arr, 3)
