"""Unit tests for DisjointSet (Union-Find) data structure."""
import pytest
from structures.disjoint_set import DisjointSet


def test_init_and_add():
    ds = DisjointSet([1, 2, 3])
    assert len(ds) == 3
    assert ds.num_sets == 3
    assert 1 in ds and 2 in ds and 3 in ds
    assert 4 not in ds

    assert ds.add(4) is True
    assert ds.add(4) is False
    assert len(ds) == 4
    assert ds.num_sets == 4


def test_find_and_missing():
    ds = DisjointSet(["a", "b"])
    assert ds.find("a") == "a"
    with pytest.raises(KeyError):
        ds.find("c")


def test_union_and_connected():
    ds = DisjointSet(range(5))
    assert not ds.connected(0, 1)

    assert ds.union(0, 1) is True
    assert ds.connected(0, 1) is True
    assert ds.num_sets == 4

    assert ds.union(0, 1) is False
    assert ds.num_sets == 4

    assert ds.union(1, 2) is True
    assert ds.connected(0, 2) is True
    assert ds.num_sets == 3


def test_subsets():
    ds = DisjointSet(["apple", "banana", "cherry", "date"])
    ds.union("apple", "banana")
    ds.union("cherry", "date")

    subsets = ds.subsets()
    assert len(subsets) == 2
    assert {"apple", "banana"} in subsets
    assert {"cherry", "date"} in subsets


def test_path_compression_chain():
    ds = DisjointSet(range(10))
    for i in range(9):
        ds.union(i, i + 1)

    assert ds.num_sets == 1
    root = ds.find(0)
    for i in range(10):
        assert ds.find(i) == root
