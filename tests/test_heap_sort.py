"""Unit tests for heap sort algorithm."""
import random
from algorithms.sorting.heap_sort import heap_sort


def test_heap_sort_empty_and_single():
    assert heap_sort([]) == []
    assert heap_sort([42]) == [42]


def test_heap_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    assert heap_sort(arr) == [1, 2, 3, 4, 5]


def test_heap_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
    assert heap_sort(arr) == [1, 2, 3, 4, 5]


def test_heap_sort_all_duplicates():
    arr = [7, 7, 7, 7, 7]
    assert heap_sort(arr) == [7, 7, 7, 7, 7]


def test_heap_sort_many_duplicates():
    arr = [3, 1, 2, 3, 1, 3, 2, 1]
    assert heap_sort(arr) == [1, 1, 1, 2, 2, 3, 3, 3]


def test_heap_sort_negatives():
    arr = [-5, 3, -1, 0, 2, -10]
    assert heap_sort(arr) == [-10, -5, -1, 0, 2, 3]


def test_heap_sort_strings():
    arr = ["banana", "apple", "cherry", "date"]
    assert heap_sort(arr) == ["apple", "banana", "cherry", "date"]


def test_heap_sort_in_place():
    arr = [3, 1, 2]
    result = heap_sort(arr)
    assert result is arr
    assert result == [1, 2, 3]


def test_heap_sort_random_list():
    random.seed(42)
    arr = [random.randint(-1000, 1000) for _ in range(150)]
    expected = sorted(arr)
    assert heap_sort(arr) == expected
