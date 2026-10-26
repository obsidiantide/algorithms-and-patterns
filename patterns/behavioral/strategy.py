"""Strategy Pattern implementation for serialization formats."""
from abc import ABC, abstractmethod
import json
from typing import Dict, Any


class SerializationStrategy(ABC):
    """Abstract base class for serialization strategies."""

    @abstractmethod
    def serialize(self, data: Dict[str, Any]) -> str:
        """Serialize a dictionary into a string format."""
        pass


class JSONStrategy(SerializationStrategy):
    """Serializes data into formatted JSON string."""

    def serialize(self, data: Dict[str, Any]) -> str:
        return json.dumps(data, indent=2)


class KeyValueStrategy(SerializationStrategy):
    """Serializes data into newline-separated key=value pairs."""

    def serialize(self, data: Dict[str, Any]) -> str:
        return "\n".join(f"{k}={v}" for k, v in data.items())


class SerializerContext:
    """Context that delegates serialization to an interchangeable strategy."""

    def __init__(self, strategy: SerializationStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SerializationStrategy) -> None:
        """Switch the current serialization strategy at runtime."""
        self.strategy = strategy

    def export(self, data: Dict[str, Any]) -> str:
        """Serialize data using the current strategy."""
        return self.strategy.serialize(data)
