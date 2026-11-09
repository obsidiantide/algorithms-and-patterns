import random

import pytest

from structures.segment_tree import SegmentTree


def test_range_sum_basic():
    tree = SegmentTree([1, 2, 3, 4, 5])
    assert tree.range_sum(0, 4) == 15
    assert tree.range_sum(1, 3) == 9
    assert tree.range_sum(2, 2) == 3


def test_set_and_update():
    tree = SegmentTree([1, 2, 3, 4])
    tree.set(1, 10)
    assert tree[1] == 10
    assert tree.range_sum(0, 3) == 18
    tree.update(3, -4)
    assert tree.range_sum(2, 3) == 3


def test_single_element_and_len():
    tree = SegmentTree([7])
    assert len(tree) == 1
    assert tree.range_sum(0, 0) == 7


def test_empty_tree_rejects_queries():
    tree = SegmentTree([])
    assert len(tree) == 0
    with pytest.raises(IndexError):
        tree.range_sum(0, 0)


def test_invalid_indices():
    tree = SegmentTree([1, 2, 3])
    with pytest.raises(IndexError):
        tree.range_sum(-1, 1)
    with pytest.raises(IndexError):
        tree.range_sum(0, 3)
    with pytest.raises(IndexError):
        tree.range_sum(2, 1)
    with pytest.raises(IndexError):
        tree.set(3, 0)


def test_matches_naive_on_random_operations():
    rng = random.Random(42)
    for n in (1, 2, 5, 8, 13):
        data = [rng.randint(-50, 50) for _ in range(n)]
        tree = SegmentTree(data)
        for _ in range(100):
            if rng.random() < 0.5:
                i, v = rng.randrange(n), rng.randint(-50, 50)
                data[i] = v
                tree.set(i, v)
            else:
                l = rng.randrange(n)
                r = rng.randrange(l, n)
                assert tree.range_sum(l, r) == sum(data[l:r + 1])
