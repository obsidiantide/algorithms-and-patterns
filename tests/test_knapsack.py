"""Unit tests for 0-1 Knapsack problem."""
import pytest
from algorithms.dynamic.knapsack import knapsack_01, knapsack_01_items


def test_empty_items():
    assert knapsack_01([], [], 10) == 0
    assert knapsack_01_items([], [], 10) == (0, [])


def test_zero_capacity():
    assert knapsack_01([1, 2, 3], [10, 20, 30], 0) == 0
    assert knapsack_01_items([1, 2, 3], [10, 20, 30], 0) == (0, [])


def test_single_item_fits():
    assert knapsack_01([5], [10], 5) == 10
    assert knapsack_01_items([5], [10], 5) == (10, [0])


def test_single_item_does_not_fit():
    assert knapsack_01([5], [10], 4) == 0
    assert knapsack_01_items([5], [10], 4) == (0, [])


def test_standard_knapsack():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5
    max_val = knapsack_01(weights, values, capacity)
    assert max_val == 7

    val, chosen = knapsack_01_items(weights, values, capacity)
    assert val == 7
    assert chosen == [0, 1]
    assert sum(weights[i] for i in chosen) <= capacity
    assert sum(values[i] for i in chosen) == val


def test_all_items_fit():
    weights = [1, 2, 3]
    values = [6, 10, 12]
    capacity = 10
    assert knapsack_01(weights, values, capacity) == 28
    val, chosen = knapsack_01_items(weights, values, capacity)
    assert val == 28
    assert chosen == [0, 1, 2]


def test_zero_weight_item():
    weights = [0, 2, 3]
    values = [5, 10, 15]
    capacity = 2
    assert knapsack_01(weights, values, capacity) == 15
    val, chosen = knapsack_01_items(weights, values, capacity)
    assert val == 15
    assert 0 in chosen


def test_invalid_arguments():
    with pytest.raises(ValueError, match="same length"):
        knapsack_01([1, 2], [10], 5)

    with pytest.raises(ValueError, match="cannot be negative"):
        knapsack_01([1], [10], -1)

    with pytest.raises(ValueError, match="weights cannot be negative"):
        knapsack_01([-1], [10], 5)

    with pytest.raises(ValueError, match="values cannot be negative"):
        knapsack_01([1], [-10], 5)
