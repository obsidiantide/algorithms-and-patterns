"""Cross-check every sorting implementation against the built-in sorted()."""
import random

import pytest

from algorithms.sorting.heap_sort import heap_sort
from algorithms.sorting.merge_sort import merge_sort
from algorithms.sorting.quick_sort import quick_sort

SORTS = [heap_sort, merge_sort, quick_sort]


@pytest.mark.parametrize("sort", SORTS)
@pytest.mark.parametrize("seed", range(20))
def test_random_integers_match_sorted(sort, seed):
    rng = random.Random(seed)
    data = [rng.randint(-100, 100) for _ in range(rng.randint(0, 60))]
    assert sort(list(data)) == sorted(data)


@pytest.mark.parametrize("sort", SORTS)
def test_many_duplicates(sort):
    rng = random.Random(7)
    data = [rng.choice([0, 1, 2]) for _ in range(200)]
    assert sort(list(data)) == sorted(data)


@pytest.mark.parametrize("sort", SORTS)
def test_floats_and_strings(sort):
    floats = [3.5, -1.25, 0.0, 2.75, -1.25]
    words = ["pear", "apple", "fig", "apple"]
    assert sort(list(floats)) == sorted(floats)
    assert sort(list(words)) == sorted(words)


@pytest.mark.parametrize("sort", SORTS)
def test_reverse_and_sorted_inputs(sort):
    data = list(range(100))
    assert sort(list(data)) == data
    assert sort(data[::-1]) == data
