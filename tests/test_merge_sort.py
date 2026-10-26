"""Unit tests for merge sort algorithm."""
import random
from dataclasses import dataclass
from algorithms.sorting.merge_sort import merge_sort


def test_merge_sort_empty_and_single():
    assert merge_sort([]) == []
    assert merge_sort([42]) == [42]


def test_merge_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    assert merge_sort(arr) == [1, 2, 3, 4, 5]


def test_merge_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
    assert merge_sort(arr) == [1, 2, 3, 4, 5]


def test_merge_sort_duplicates():
    arr = [3, 1, 2, 3, 1, 3, 2, 1]
    assert merge_sort(arr) == [1, 1, 1, 2, 2, 3, 3, 3]


def test_merge_sort_negatives():
    arr = [-5, 3, -1, 0, 2, -10]
    assert merge_sort(arr) == [-10, -5, -1, 0, 2, 3]


def test_merge_sort_strings():
    arr = ["banana", "apple", "cherry", "date"]
    assert merge_sort(arr) == ["apple", "banana", "cherry", "date"]


def test_merge_sort_does_not_mutate_input():
    original = [4, 2, 1, 3]
    copy = list(original)
    result = merge_sort(original)
    assert original == copy
    assert result == [1, 2, 3, 4]


def test_merge_sort_random_list():
    random.seed(42)
    arr = [random.randint(-1000, 1000) for _ in range(150)]
    assert merge_sort(arr) == sorted(arr)


def test_merge_sort_stability():
    @dataclass
    class Record:
        key: int
        label: str

        def __le__(self, other: "Record") -> bool:
            return self.key <= other.key

    records = [
        Record(2, "first_2"),
        Record(1, "first_1"),
        Record(2, "second_2"),
        Record(1, "second_1"),
    ]
    sorted_records = merge_sort(records)
    assert [r.label for r in sorted_records] == [
        "first_1",
        "second_1",
        "first_2",
        "second_2",
    ]
