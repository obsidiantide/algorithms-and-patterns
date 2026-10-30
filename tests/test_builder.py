"""Unit tests for the Builder Pattern implementation."""
import pytest
from patterns.creational.builder import QueryBuilder, QueryDirector


def test_builder_basic_select():
    query = QueryBuilder().from_table("users").build()
    assert str(query) == "SELECT * FROM users"


def test_builder_full_query():
    query = (
        QueryBuilder()
        .from_table("users")
        .select("id", "username")
        .where("active = 1")
        .where("age >= 18")
        .order_by("username", "desc")
        .limit(10)
        .build()
    )
    assert (
        str(query)
        == "SELECT id, username FROM users WHERE active = 1 AND age >= 18 ORDER BY username DESC LIMIT 10"
    )


def test_builder_validation():
    builder = QueryBuilder()
    with pytest.raises(ValueError, match="Target table must be set"):
        builder.build()

    with pytest.raises(ValueError, match="Table name must be non-empty"):
        builder.from_table("   ")

    with pytest.raises(ValueError, match="Field name must be non-empty"):
        builder.select("   ")

    with pytest.raises(ValueError, match="Condition must be non-empty"):
        builder.where("   ")

    with pytest.raises(ValueError, match="Direction must be 'ASC' or 'DESC'"):
        builder.order_by("id", "INVALID")

    with pytest.raises(ValueError, match="Limit must be non-negative"):
        builder.limit(-1)


def test_builder_resets_after_build():
    builder = QueryBuilder().from_table("orders").select("total")
    q1 = builder.build()
    assert str(q1) == "SELECT total FROM orders"

    with pytest.raises(ValueError, match="Target table must be set"):
        builder.build()


def test_query_director():
    director = QueryDirector(QueryBuilder())
    q_all = director.build_select_all("products", limit=5)
    assert str(q_all) == "SELECT * FROM products LIMIT 5"

    q_id_int = director.build_by_id("products", 42)
    assert str(q_id_int) == "SELECT * FROM products WHERE id = 42 LIMIT 1"

    q_id_str = director.build_by_id("products", "sku-123")
    assert str(q_id_str) == "SELECT * FROM products WHERE id = 'sku-123' LIMIT 1"
