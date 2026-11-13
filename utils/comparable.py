"""Shared typing helpers for ordering-based algorithms."""
from typing import Any, Protocol


class Comparable(Protocol):
    """Anything that supports the rich ordering operators."""

    def __lt__(self, other: Any) -> bool: ...

    def __le__(self, other: Any) -> bool: ...

    def __gt__(self, other: Any) -> bool: ...

    def __ge__(self, other: Any) -> bool: ...
