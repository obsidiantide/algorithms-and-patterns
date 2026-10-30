"""Builder Pattern implementation for step-by-step query construction."""
from __future__ import annotations
from typing import Any, List, Optional


class Query:
    """Represents a structured SQL query object."""

    def __init__(self) -> None:
        self.table: Optional[str] = None
        self.fields: List[str] = []
        self.conditions: List[str] = []
        self.order_by_field: Optional[str] = None
        self.order_direction: str = "ASC"
        self.limit_count: Optional[int] = None

    def to_sql(self) -> str:
        """Render the query to a SQL string."""
        if not self.table:
            raise ValueError("Target table must be set")
        fields_str = ", ".join(self.fields) if self.fields else "*"
        sql = f"SELECT {fields_str} FROM {self.table}"
        if self.conditions:
            sql += f" WHERE {' AND '.join(self.conditions)}"
        if self.order_by_field:
            sql += f" ORDER BY {self.order_by_field} {self.order_direction}"
        if self.limit_count is not None:
            sql += f" LIMIT {self.limit_count}"
        return sql

    def __str__(self) -> str:
        return self.to_sql()


class QueryBuilder:
    """Fluent builder for assembling SQL queries step by step."""

    def __init__(self) -> None:
        self._query: Query = Query()

    def reset(self) -> QueryBuilder:
        """Reset the builder state for constructing a new query."""
        self._query = Query()
        return self

    def from_table(self, table: str) -> QueryBuilder:
        """Set the target table name."""
        if not table.strip():
            raise ValueError("Table name must be non-empty")
        self._query.table = table.strip()
        return self

    def select(self, *fields: str) -> QueryBuilder:
        """Add one or more fields to select."""
        for field in fields:
            if not field.strip():
                raise ValueError("Field name must be non-empty")
            self._query.fields.append(field.strip())
        return self

    def where(self, condition: str) -> QueryBuilder:
        """Add a WHERE clause condition."""
        if not condition.strip():
            raise ValueError("Condition must be non-empty")
        self._query.conditions.append(condition.strip())
        return self

    def order_by(self, field: str, direction: str = "ASC") -> QueryBuilder:
        """Specify ordering field and direction."""
        direction = direction.upper()
        if direction not in ("ASC", "DESC"):
            raise ValueError("Direction must be 'ASC' or 'DESC'")
        self._query.order_by_field = field.strip()
        self._query.order_direction = direction
        return self

    def limit(self, count: int) -> QueryBuilder:
        """Set the maximum number of records to return."""
        if count < 0:
            raise ValueError("Limit must be non-negative")
        self._query.limit_count = count
        return self

    def build(self) -> Query:
        """Validate and return the constructed Query instance."""
        if not self._query.table:
            raise ValueError("Target table must be set before building")
        result = self._query
        self.reset()
        return result


class QueryDirector:
    """Director defining reusable query construction recipes."""

    def __init__(self, builder: QueryBuilder) -> None:
        self.builder = builder

    def build_select_all(self, table: str, limit: Optional[int] = None) -> Query:
        """Construct a query selecting all rows from a table."""
        self.builder.reset().from_table(table)
        if limit is not None:
            self.builder.limit(limit)
        return self.builder.build()

    def build_by_id(self, table: str, record_id: Any) -> Query:
        """Construct a query to fetch a single record by id."""
        val = f"'{record_id}'" if isinstance(record_id, str) else str(record_id)
        return self.builder.reset().from_table(table).where(f"id = {val}").limit(1).build()
