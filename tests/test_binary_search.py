"""Unit tests for binary search algorithms."""
from algorithms.searching.binary_search import (
    binary_search,
    find_leftmost,
    find_rightmost,
    search_range,
)


def test_binary_search_found():
    arr = [1, 3, 5, 7, 9, 11]
    assert binary_search(arr, 7) == 3
    assert binary_search(arr, 1) == 0
    assert binary_search(arr, 11) == 5


def test_binary_search_not_found():
    arr = [1, 3, 5, 7, 9]
    assert binary_search(arr, 4) is None
    assert binary_search(arr, 0) is None
    assert binary_search(arr, 12) is None


def test_binary_search_empty():
    assert binary_search([], 1) is None


def test_find_leftmost():
    arr = [1, 2, 4, 4, 4, 5, 8]
    assert find_leftmost(arr, 4) == 2
    assert find_leftmost(arr, 3) == 2
    assert find_leftmost(arr, 0) == 0
    assert find_leftmost(arr, 10) == len(arr)
    assert find_leftmost([], 5) == 0


def test_find_rightmost():
    arr = [1, 2, 4, 4, 4, 5, 8]
    assert find_rightmost(arr, 4) == 5
    assert find_rightmost(arr, 3) == 2
    assert find_rightmost(arr, 0) == 0
    assert find_rightmost(arr, 10) == len(arr)
    assert find_rightmost([], 5) == 0


def test_search_range():
    arr = [1, 2, 4, 4, 4, 5, 8]
    assert search_range(arr, 4) == (2, 4)
    assert search_range(arr, 1) == (0, 0)
    assert search_range(arr, 8) == (6, 6)
    assert search_range(arr, 3) is None
    assert search_range(arr, 0) is None
    assert search_range(arr, 9) is None
    assert search_range([], 1) is None


def test_search_range_all_identical():
    arr = [7, 7, 7, 7]
    assert search_range(arr, 7) == (0, 3)
    assert search_range(arr, 6) is None
