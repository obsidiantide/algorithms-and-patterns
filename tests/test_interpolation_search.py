"""Unit tests for interpolation search algorithm."""
from algorithms.searching.interpolation_search import interpolation_search


def test_interpolation_search_found():
    arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    assert interpolation_search(arr, 10) == 0
    assert interpolation_search(arr, 50) == 4
    assert interpolation_search(arr, 90) == 8


def test_interpolation_search_not_found():
    arr = [10, 20, 30, 40, 50]
    assert interpolation_search(arr, 5) is None
    assert interpolation_search(arr, 25) is None
    assert interpolation_search(arr, 55) is None


def test_interpolation_search_empty():
    assert interpolation_search([], 42) is None


def test_interpolation_search_single_element():
    assert interpolation_search([42], 42) == 0
    assert interpolation_search([42], 10) is None
    assert interpolation_search([42], 99) is None


def test_interpolation_search_negative_numbers():
    arr = [-100, -50, -20, 0, 15, 35, 70]
    assert interpolation_search(arr, -100) == 0
    assert interpolation_search(arr, -20) == 2
    assert interpolation_search(arr, 0) == 3
    assert interpolation_search(arr, 70) == 6
    assert interpolation_search(arr, -30) is None
    assert interpolation_search(arr, -120) is None


def test_interpolation_search_all_identical():
    arr = [5, 5, 5, 5, 5]
    assert interpolation_search(arr, 5) in range(len(arr))
    assert interpolation_search(arr, 4) is None
    assert interpolation_search(arr, 6) is None


def test_interpolation_search_large_uniform_sequence():
    arr = list(range(0, 10000, 5))
    assert interpolation_search(arr, 0) == 0
    assert interpolation_search(arr, 5000) == 1000
    assert interpolation_search(arr, 9995) == 1999
    assert interpolation_search(arr, 5001) is None


def test_interpolation_search_tuple_input():
    data = (1, 3, 5, 7, 9)
    assert interpolation_search(data, 5) == 2
    assert interpolation_search(data, 6) is None
