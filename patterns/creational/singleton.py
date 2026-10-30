"""Singleton Pattern implementations ensuring a single instance of a class."""
from __future__ import annotations

import functools
import threading
from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar

T = TypeVar("T")


class SingletonMeta(type):
    """Thread-safe implementation of the Singleton pattern using a metaclass.

    Ensures only a single instance of the class exists across threads.
    """

    _instances: Dict[type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls) -> None:
        """Clear the cached singleton instance for this class."""
        with cls._lock:
            cls._instances.pop(cls, None)

    def is_instantiated(cls) -> bool:
        """Check if an instance of this singleton has been created."""
        return cls in cls._instances


class SingletonWrapper(Generic[T]):
    """Thread-safe singleton wrapper class returned by the @singleton decorator."""

    def __init__(self, cls: Type[T]) -> None:
        self._wrapped = cls
        self._instance: Optional[T] = None
        self._lock = threading.Lock()
        functools.update_wrapper(self, cls)

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self._wrapped(*args, **kwargs)
        return self._instance

    def clear(self) -> None:
        """Clear the cached singleton instance."""
        with self._lock:
            self._instance = None

    def is_instantiated(self) -> bool:
        """Check if the singleton instance has been created."""
        return self._instance is not None

    def __getattr__(self, name: str) -> Any:
        return getattr(self._wrapped, name)


def singleton(cls: Type[T]) -> SingletonWrapper[T]:
    """Thread-safe decorator converting a class into a singleton."""
    return SingletonWrapper(cls)
