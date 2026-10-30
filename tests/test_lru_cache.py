"""Unit tests for LRUCache."""
import pytest
from structures.lru_cache import LRUCache


def test_lru_cache_basic():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert cache.get("b") is None  # Evicted
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_lru_cache_update_existing():
    cache = LRUCache(2)
    cache.put("x", 10)
    cache.put("x", 20)
    assert cache.get("x") == 20
    assert len(cache) == 1


def test_lru_cache_invalid_capacity():
    with pytest.raises(ValueError, match="Capacity must be positive integer"):
        LRUCache(0)
    with pytest.raises(ValueError, match="Capacity must be positive integer"):
        LRUCache(-5)


def test_lru_cache_get_default():
    cache = LRUCache(2)
    assert cache.get("missing") is None
    assert cache.get("missing", "default_val") == "default_val"


def test_lru_cache_len_and_contains():
    cache = LRUCache(2)
    assert len(cache) == 0
    assert "x" not in cache

    cache.put("x", 1)
    assert len(cache) == 1
    assert "x" in cache
    assert "y" not in cache

    cache.put("y", 2)
    assert len(cache) == 2
    assert "y" in cache

    cache.put("z", 3)
    assert len(cache) == 2
    assert "x" not in cache
    assert "y" in cache
    assert "z" in cache


def test_lru_cache_peek():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)

    # peek should not refresh recency
    assert cache.peek("a") == 1
    assert cache.peek("missing", -1) == -1

    # inserting "c" should evict "a" because peek("a") did not mark it as recently used
    cache.put("c", 3)
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_lru_cache_delete():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)

    assert cache.delete("a") is True
    assert len(cache) == 1
    assert cache.get("a") is None
    assert cache.delete("a") is False

    # After deleting "a", inserting "c" should not evict "b"
    cache.put("c", 3)
    assert len(cache) == 2
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_lru_cache_clear():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert len(cache) == 2

    cache.clear()
    assert len(cache) == 0
    assert cache.get("a") is None
    assert cache.get("b") is None

    # Cache should continue working after clear
    cache.put("x", 42)
    assert len(cache) == 1
    assert cache.get("x") == 42
