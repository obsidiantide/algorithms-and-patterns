"""Unit tests for FenwickTree (Binary Indexed Tree)."""
import pytest
from structures.fenwick_tree import FenwickTree


def test_init_and_properties():
    ft_empty = FenwickTree(0)
    assert len(ft_empty) == 0 and ft_empty.to_list() == []
    with pytest.raises(IndexError, match="Index out of range"):
        ft_empty.prefix_sum(0)

    ft = FenwickTree(5)
    assert len(ft) == 5 and ft.to_list() == [0, 0, 0, 0, 0]
    assert ft.prefix_sum(4) == 0

    values = [1, 3, 5, 7, 9, 11]
    ft_vals = FenwickTree(values)
    assert len(ft_vals) == 6 and ft_vals.to_list() == values
    assert ft_vals.prefix_sum(0) == 1 and ft_vals.prefix_sum(2) == 9
    assert ft_vals.prefix_sum(5) == sum(values)


def test_validation():
    with pytest.raises(ValueError, match="Size must be non-negative"):
        FenwickTree(-1)

    ft = FenwickTree([1, 2, 3])
    for fn, args in [
        (ft.add, (3, 10)), (ft.add, (-1, 10)),
        (ft.prefix_sum, (3,)), (ft.prefix_sum, (-1,)),
        (ft.range_sum, (0, 3)), (ft.range_sum, (-1, 1)),
    ]:
        with pytest.raises(IndexError, match="Index out of range"):
            fn(*args)

    with pytest.raises(ValueError, match="left index cannot be greater than right index"):
        ft.range_sum(2, 1)


def test_range_sum_and_floats():
    ft = FenwickTree([3, 2, -1, 6, 5, 4, -3, 3, 7, 2])
    assert ft.range_sum(0, 0) == 3
    assert ft.range_sum(1, 3) == 7
    assert ft.range_sum(3, 7) == 15
    assert ft.range_sum(0, 9) == 28

    ft_float = FenwickTree([1.5, 2.5, 3.0])
    assert ft_float.prefix_sum(1) == 4.0
    assert ft_float.range_sum(1, 2) == 5.5


def test_point_add_and_set_with_indexing():
    ft = FenwickTree([10, 20, 30, 40])
    assert ft[-1] == 40 and ft[-4] == 10
    with pytest.raises(IndexError, match="Index out of range"):
        _ = ft[-5]

    ft.add(1, 5)
    assert ft[1] == 25 and ft.to_list() == [10, 25, 30, 40]

    ft.set(-1, 99)
    assert ft[3] == 99 and ft.to_list() == [10, 25, 30, 99]
    assert ft.range_sum(0, 3) == 164
