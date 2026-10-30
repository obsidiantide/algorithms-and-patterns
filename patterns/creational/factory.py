"""Factory Pattern implementation supporting registration and dynamic instantiation."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Generic, List, TypeVar

T = TypeVar("T")


class ObjectFactory(Generic[T]):
    """Generic extensible object factory supporting registration and creation."""

    def __init__(self) -> None:
        self._creators: Dict[str, Callable[..., T]] = {}

    def register(self, key: str, creator: Callable[..., T]) -> None:
        """Register a creator function or class under a case-insensitive key."""
        normalized = key.strip().lower()
        if not normalized:
            raise ValueError("Factory key must be non-empty")
        self._creators[normalized] = creator

    def register_builder(self, key: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
        """Decorator to register a creator callable."""
        def decorator(creator: Callable[..., T]) -> Callable[..., T]:
            self.register(key, creator)
            return creator
        return decorator

    def unregister(self, key: str) -> None:
        """Unregister a creator by key."""
        self._creators.pop(key.strip().lower(), None)

    def is_registered(self, key: str) -> bool:
        """Check whether a creator is registered for the given key."""
        return key.strip().lower() in self._creators

    def registered_keys(self) -> List[str]:
        """Return a sorted list of registered keys."""
        return sorted(self._creators.keys())

    def create(self, key: str, *args: Any, **kwargs: Any) -> T:
        """Instantiate an object using the registered creator."""
        creator = self._creators.get(key.strip().lower())
        if creator is None:
            available = ", ".join(self.registered_keys()) or "none"
            raise ValueError(f"Unknown factory key: '{key}'. Available: {available}")
        return creator(*args, **kwargs)

    def __len__(self) -> int:
        return len(self._creators)

    def __contains__(self, key: str) -> bool:
        return self.is_registered(key)


class Notifier(ABC):
    """Abstract base class for notification dispatchers."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> str:
        """Send a notification message to the recipient."""


class EmailNotifier(Notifier):
    """Email notification dispatcher."""

    def send(self, recipient: str, message: str) -> str:
        return f"Email sent to {recipient}: {message}"


class SMSNotifier(Notifier):
    """SMS notification dispatcher."""

    def send(self, recipient: str, message: str) -> str:
        return f"SMS sent to {recipient}: {message}"


class NotificationFactory(ObjectFactory[Notifier]):
    """Pre-configured factory for common notification channels."""

    def __init__(self) -> None:
        super().__init__()
        self.register("email", EmailNotifier)
        self.register("sms", SMSNotifier)
