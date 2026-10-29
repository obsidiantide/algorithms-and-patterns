"""Unit tests for coin change dynamic programming implementations."""
import pytest
from algorithms.dynamic.coin_change import coin_change_min, coin_change_ways


def test_zero_amount():
    assert coin_change_min([1, 2, 5], 0) == 0
    assert coin_change_ways([1, 2, 5], 0) == 1


def test_empty_coins():
    assert coin_change_min([], 0) == 0
    assert coin_change_ways([], 0) == 1
    assert coin_change_min([], 5) == -1
    assert coin_change_ways([], 5) == 0


def test_standard_min_coins():
    assert coin_change_min([1, 2, 5], 11) == 3
    assert coin_change_min([2], 3) == -1
    assert coin_change_min([1], 0) == 0
    assert coin_change_min([1], 1) == 1
    assert coin_change_min([1], 2) == 2


def test_standard_ways():
    assert coin_change_ways([1, 2, 5], 5) == 4
    assert coin_change_ways([2], 3) == 0
    assert coin_change_ways([10], 10) == 1


def test_duplicate_coins():
    assert coin_change_min([1, 2, 2, 5], 11) == 3
    assert coin_change_ways([1, 2, 2, 5], 5) == 4


def test_no_solution():
    assert coin_change_min([5, 10], 3) == -1
    assert coin_change_ways([5, 10], 3) == 0


def test_invalid_arguments():
    with pytest.raises(ValueError, match="amount cannot be negative"):
        coin_change_min([1, 2], -1)

    with pytest.raises(ValueError, match="amount cannot be negative"):
        coin_change_ways([1, 2], -1)

    with pytest.raises(ValueError, match="coin denominations must be strictly positive"):
        coin_change_min([1, 0, 5], 5)

    with pytest.raises(ValueError, match="coin denominations must be strictly positive"):
        coin_change_min([1, -2, 5], 5)

    with pytest.raises(ValueError, match="coin denominations must be strictly positive"):
        coin_change_ways([0], 5)
